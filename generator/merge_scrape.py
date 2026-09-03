#!/usr/bin/env python3
"""Merge one scrape staging file into data/, under the database rules.

The rules are the pipeline skill's Stage 3 and Cyan's standing rulings, and
every one of them is enforced here rather than remembered:

  EXACT MATCH (the book id in a direct_link we already hold): view_count and
    view_count_date update freely (CONVENTIONS.md), last_checked and
    last_verified move to the scrape date, and a snapshots.csv row is written
    with THE DATE (audit H2: 2,659 rows carried none). Every other field is
    fill-blank-only: episode_count, poster_ref, title_as_listed, source_urls.
  NEW TITLE: created as data_confidence=needs_check, origin=english (never
    blank, adapters.md sec 11), slug taken from ReelShort's own URL which is
    already the house slug style. Only when the book was seen on the homepage,
    the fandom blog, or an actor tag page: those are 'newest, most popular, or
    credited to someone we track', which is Cyan's rule (8 Aug) for choosing
    titles rather than sweeping a catalogue. A book seen only via a sitemap is
    listed in the report and never created.
  NEAR MATCH: a same slug, a slug that matches with the hyphens removed, or a
    title that matches an existing primary or alt title after dropping the
    leading article, goes to match_queue.csv with the evidence and is NOT
    created. NEVER AUTO-MERGE. Same-name productions across platforms are
    usually different shows (adapters.md sec 9), and a wrong merge deletes a
    published URL.
  DELISTED (404 on a link we hold): reported. Nothing is deleted by a machine.
  CREDITS: an actor tag page is ReelShort asserting that actor is in that
    title. A credit is added only when the name matches exactly one person in
    people.csv, role=actor, and the (title, person) pair is not already held.
    Nobody is created: a person is a published URL and a near-name is a
    ruling (READ FIRST, standing rules).
  SYNOPSES stay in the staging JSON. synopsis_short is never written from a
    platform: the caption pipeline owns that column (no copied copy, 14 Aug).

Usage:
    python3 generator/merge_scrape.py generator/staging/reelshort_2026-09-06.json [--dry-run] [--summary FILE]

Exit 0 on success, 1 on a malformed staging file. The summary is Markdown,
printed to stdout, appended to $GITHUB_STEP_SUMMARY when set, and written to
--summary when given.
"""
import argparse, csv, datetime, io, json, os, re, sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.environ.get("DEA_DATA") or os.path.join(os.path.dirname(HERE), "data")
PLATFORM = "reelshort"
STALE_DAYS = 45
MOVIE_RE = re.compile(r"/movie/([a-z0-9]+(?:-[a-z0-9]+)*)-([0-9a-f]{24})\b")
CREATE_ROUTES = {"tags", "home", "fandom", "wanted"}
# A book seen ONLY on a catalogue sweep (genre tag pages, a sitemap) is created
# when it is genuinely popular. Cyan's rule is newest, most popular, or credited
# to someone we track. The held ReelShort catalogue's median is 37.8M views and
# 506 of 566 rows sit above 10M (measured 3 Sep 2026), so 10M admits a title
# into the company it would keep. Below that it is counted, not imported.
POPULAR_MIN = 10_000_000


def views_num(s):
    s = (s or "").strip().upper().replace(",", "")
    if not s:
        return 0
    mult = {"B": 1e9, "M": 1e6, "K": 1e3}.get(s[-1], 1)
    try:
        return float(s[:-1] if s[-1] in "BMK" else s) * mult
    except ValueError:
        return 0
# CONVENTIONS.md: ReelTalk episodes, The Next ReelStar and other unscripted or
# interview content are excluded from titles.csv. The first live probe (3 Sep
# 2026) would have created seven ReelTalk episodes from actor tag pages.
EXCLUDE_RE = re.compile(r"^\s*(reel\s*talk|the next reelstar|reelstar|goodchat|reelshort (podcast|live))\b", re.I)


# --- CSV I/O, line endings preserved per file ---------------------------------

def path(n):
    return os.path.join(DATA, n)


def term_of(p):
    raw = open(p, "rb").read()
    c = raw.count(b"\r\n")
    return "\r\n" if c > raw.count(b"\n") - c else "\n"


def load(n):
    with open(path(n), newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        return list(r), list(r.fieldnames)


def save(n, fields, recs):
    p = path(n)
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=fields, lineterminator=term_of(p))
    w.writeheader()
    w.writerows(recs)
    open(p, "w", newline="", encoding="utf-8").write(buf.getvalue())


# --- matching -------------------------------------------------------------------

def bare(s):
    """Leading article off FIRST, then everything but letters and digits.
    Order matters (READ FIRST trap: 'Alpha's Doe' -> 'lphasdoe' the other way)."""
    s = re.sub(r"^(the|a|an)\s+", "", (s or "").strip().lower())
    return re.sub(r"[^a-z0-9]", "", s)


def nohyphen(slug):
    return (slug or "").replace("-", "")


def split_alts(s):
    return [a.strip() for a in re.split(r"[|;]", s or "") if a.strip()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("staging")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--summary", default="")
    a = ap.parse_args()

    doc = json.load(io.open(a.staging, encoding="utf-8"))
    books = doc.get("books") or {}
    if not isinstance(books, dict):
        print("staging file has no books dict", file=sys.stderr)
        return 1
    today = (doc.get("scraped_at") or datetime.datetime.now(datetime.timezone.utc).isoformat())[:10]
    source = "%s_weekly_%s" % (PLATFORM, today)

    titles, tf = load("titles.csv")
    avail, af = load("availability.csv")
    snaps, sf = load("snapshots.csv")
    mq, mf = load("match_queue.csv")
    credits, cf = load("credits.csv")
    people, _ = load("people.csv")

    by_id = {t["title_id"]: t for t in titles}
    by_bare, by_nohyphen = {}, {}
    for t in titles:
        by_nohyphen.setdefault(nohyphen(t["slug"] or t["title_id"]), t["title_id"])
        by_bare.setdefault(bare(t["primary_title"]), t["title_id"])
        for alt in split_alts(t.get("alt_titles")):
            by_bare.setdefault(bare(alt), t["title_id"])
    link_rows = {}      # book_id -> availability row
    plat_rows = {}      # title_id -> availability row on this platform
    for r in avail:
        if r["platform_id"] != PLATFORM:
            continue
        plat_rows.setdefault(r["title_id"], r)
        m = MOVIE_RE.search(r.get("direct_link") or "")
        if m:
            link_rows[m.group(2)] = r
    snap_keys = {(s["title_id"], s["platform_id"], s["date"]) for s in snaps}
    credit_keys = {(c["title_id"], c["person_id"]) for c in credits}
    name_count = Counter(p["name"].strip().lower() for p in people)
    person_by_name = {p["name"].strip().lower(): p["person_id"] for p in people
                      if name_count[p["name"].strip().lower()] == 1}
    mq_text = "\n".join(r["candidate_b"] + " " + r["evidence"] for r in mq)

    n = Counter()
    new_titles, held, delisted_report, credits_added = [], [], [], []
    catalogue_only = 0

    def touch(t, row, b):
        """Exact-match update: counts, dates, fill-blank fields, snapshot."""
        if b.get("views"):
            if row.get("view_count") != b["views"]:
                n["views_changed"] += 1
            row["view_count"] = b["views"]
            row["view_count_date"] = today
            key = (t["title_id"], PLATFORM, today)
            if key not in snap_keys:
                snaps.append({"title_id": t["title_id"], "platform_id": PLATFORM,
                              "view_count": b["views"], "date": today})
                snap_keys.add(key)
                n["snapshots"] += 1
        row["last_checked"] = today
        if not row.get("title_as_listed_on_platform") and b.get("title"):
            row["title_as_listed_on_platform"] = b["title"]
        if not row.get("direct_link") and b.get("url"):
            row["direct_link"] = b["url"]
            n["links_filled"] += 1
        t["last_verified"] = today
        if not t.get("episode_count") and b.get("episodes"):
            t["episode_count"] = b["episodes"]
            n["episodes_filled"] += 1
        if not t.get("poster_ref") and b.get("poster"):
            t["poster_ref"] = b["poster"]
            n["posters_filled"] += 1
        if not t.get("year") and b.get("year"):
            t["year"] = b["year"]
            n["years_filled"] += 1
        if not t.get("source_urls") and b.get("url"):
            t["source_urls"] = b["url"]
        n["refreshed"] += 1

    def add_credits(tid, title_name, b):
        for actor in b.get("actors") or []:
            pid = person_by_name.get(actor.strip().lower())
            if not pid or (tid, pid) in credit_keys:
                continue
            credits.append({k: "" for k in cf} | {"title_id": tid, "person_id": pid,
                                                    "role": "actor", "character_name": ""})
            credit_keys.add((tid, pid))
            credits_added.append((title_name, actor))

    for bid, b in sorted(books.items()):
        if b.get("status") == 404:
            continue
        row = link_rows.get(bid)
        if row is not None:
            t = by_id.get(row["title_id"])
            if t is None:
                n["orphan_rows"] += 1
                continue
            if b.get("title") or b.get("views"):
                touch(t, row, b)
                if "tags" in (b.get("seen_via") or []):
                    add_credits(t["title_id"], t["primary_title"], b)
            continue

        # Not a link we hold. Is it a title we hold under this slug or name?
        if not b.get("title") or not b.get("slug"):
            n["no_data"] += 1
            continue
        if EXCLUDE_RE.match(b["title"]):
            n["excluded"] += 1
            continue
        if b.get("slug_guessed"):
            # The URL was inferred from the title and never confirmed by a
            # fetch; a wrong slug would become a permanent wrong URL.
            n["unconfirmed_url"] += 1
            continue
        slug, name, url = b["slug"], b["title"], b.get("url") or ""
        if not (set(b.get("seen_via") or []) & CREATE_ROUTES) and views_num(b.get("views")) < POPULAR_MIN:
            catalogue_only += 1
            continue
        existing = by_id.get(slug)
        if existing is not None and slug in plat_rows and not plat_rows[slug].get("direct_link"):
            # Our row on this platform, link never captured: fill it and refresh.
            touch(existing, plat_rows[slug], b)
            link_rows[bid] = plat_rows[slug]
            continue
        near = (existing["title_id"] if existing is not None else None) \
            or by_nohyphen.get(nohyphen(slug)) or by_bare.get(bare(name))
        if near:
            if slug in mq_text or (url and url in mq_text):
                n["already_queued"] += 1
                continue
            why = ("same slug" if near == slug else
                   "slug matches with hyphens removed" if by_nohyphen.get(nohyphen(slug)) == near
                   else "same title after dropping the leading article")
            ex = by_id[near]
            mq.append({"candidate_a": "%s (existing)" % near,
                       "candidate_b": "%s (ReelShort weekly scrape %s)" % (slug, today),
                       "evidence": "%s; existing '%s' source=%s; ReelShort lists '%s' at %s%s"
                                   % (why, ex["primary_title"], ex.get("source", ""), name, url,
                                      (", %s episodes" % b["episodes"]) if b.get("episodes") else ""),
                       "status": "pending"})
            mq_text += "\n" + slug + " " + url
            held.append((name, near, why))
            continue

        # Genuinely new, and chosen by a route Cyan's rule allows.
        t = {k: "" for k in tf}
        t.update({"title_id": slug, "slug": slug, "primary_title": name, "year": b.get("year") or "",
                  "episode_count": b.get("episodes") or "", "poster_ref": b.get("poster") or "",
                  "source_urls": url, "last_verified": today, "data_confidence": "needs_check",
                  "source": source, "origin": "english"})
        titles.append(t)
        by_id[slug] = t
        by_nohyphen[nohyphen(slug)] = slug
        by_bare[bare(name)] = slug
        r = {k: "" for k in af}
        r.update({"title_id": slug, "platform_id": PLATFORM, "title_as_listed_on_platform": name,
                  "direct_link": url, "view_count": b.get("views") or "",
                  "view_count_date": today if b.get("views") else "", "last_checked": today})
        avail.append(r)
        link_rows[bid] = r
        plat_rows[slug] = r
        if b.get("views"):
            snaps.append({"title_id": slug, "platform_id": PLATFORM, "view_count": b["views"], "date": today})
            snap_keys.add((slug, PLATFORM, today))
            n["snapshots"] += 1
        new_titles.append((name, slug, b.get("views") or "", ", ".join(sorted(b.get("seen_via") or []))))
        add_credits(slug, name, b)

    # CYAN'S RULINGS IN THE WANTED FILE. A line may carry flags after the URL or
    # slug: `ai=yes` or `ai=no`. The ai column is set by hand only (READ FIRST,
    # 1 Aug 2026); this file IS the hand, with her name and date in the comment.
    # Applied after creation so a title she names lands with its ruling.
    rulings_applied = []
    wanted_path = os.path.join(HERE, "staging", "%s_wanted.txt" % PLATFORM)
    if os.path.exists(wanted_path):
        for raw in io.open(wanted_path, encoding="utf-8"):
            line = raw.split("#", 1)[0].strip()
            if not line or "=" not in line:
                continue
            head, *flags = line.split()
            flags = dict(f.split("=", 1) for f in flags if "=" in f)
            if flags.get("ai") not in ("yes", "no"):
                continue
            m = MOVIE_RE.search(head)
            tid = None
            if m:
                row = link_rows.get(m.group(2))
                tid = row["title_id"] if row else (m.group(1) if m.group(1) in by_id else None)
            else:
                tid = head if head in by_id else by_nohyphen.get(nohyphen(head))
            if tid and by_id[tid].get("ai") != flags["ai"]:
                by_id[tid]["ai"] = flags["ai"]
                rulings_applied.append((tid, flags["ai"]))
            elif not tid:
                n["rulings_unmatched"] += 1

    for d in doc.get("delisted") or []:
        tid = d.get("title_id") or (link_rows.get(d.get("book_id"), {}) or {}).get("title_id", "")
        delisted_report.append((tid or "(not held)", d.get("url", "")))

    # Integrity before anything is written.
    ids = Counter(t["title_id"] for t in titles)
    dups = [k for k, v in ids.items() if v > 1]
    if dups:
        print("REFUSING TO WRITE: duplicate title_ids", dups[:5], file=sys.stderr)
        return 1

    cutoff = (datetime.date.fromisoformat(today) - datetime.timedelta(days=STALE_DAYS)).isoformat()
    stale = sum(1 for r in avail if r["platform_id"] == PLATFORM and (r.get("last_checked") or "") < cutoff)
    routes = doc.get("routes") or {}

    lines = ["## ReelShort weekly scrape, %s%s" % (today, " (dry run)" if a.dry_run else ""), ""]
    lines.append("| | |")
    lines.append("|---|---|")
    lines.append("| Requests | %s |" % doc.get("requests", "?"))
    lines.append("| Books seen | %d |" % len(books))
    lines.append("| Known titles refreshed | %d |" % n["refreshed"])
    lines.append("| View counts that moved | %d |" % n["views_changed"])
    lines.append("| Snapshot rows written | %d |" % n["snapshots"])
    lines.append("| New titles created | %d |" % len(new_titles))
    lines.append("| Held for a ruling (match_queue) | %d |" % len(held))
    lines.append("| Credits added | %d |" % len(credits_added))
    lines.append("| Episode counts / posters / links / years filled | %d / %d / %d / %d |"
                 % (n["episodes_filled"], n["posters_filled"], n["links_filled"], n["years_filled"]))
    lines.append("| Delisted (404, not deleted) | %d |" % len(delisted_report))
    lines.append("| Catalogue only (genre sweep or sitemap, under %dM views), not imported | %d |"
                 % (POPULAR_MIN // 1_000_000, catalogue_only))
    lines.append("| Excluded as unscripted (ReelTalk and kin) | %d |" % n["excluded"])
    lines.append("| Skipped: no title or slug / URL unconfirmed | %d / %d |" % (n["no_data"], n["unconfirmed_url"]))
    lines.append("| ReelShort rows still older than %d days | %d |" % (STALE_DAYS, stale))
    lines.append("| AI rulings applied from the wanted file / unmatched | %d / %d |"
                 % (len(rulings_applied), n["rulings_unmatched"]))
    lines.append("| Scrape errors | %d |" % len(doc.get("errors") or []))
    lines.append("")
    lines.append("Routes: " + ", ".join("%s %s" % (k, json.dumps(v)) for k, v in routes.items()))
    if new_titles:
        lines += ["", "### New titles (needs_check): each one needs a caption", "",
                  "These are live with no synopsis of ours. Platform text is never copied "
                  "(Cyan, 14 Aug). The synopsis each page published is banked in the staging "
                  "JSON as the fact source; `caption_pipeline.py next` picks them up by reach "
                  "and the /dea-captions skill writes them for Cyan's review.", ""]
        lines += ["- %s (`%s`) %s via %s" % (nm, sl, vw, via) for nm, sl, vw, via in new_titles]
    if held:
        lines += ["", "### Held for Cyan's ruling", ""]
        lines += ["- '%s' vs existing `%s`: %s" % h for h in held]
    if delisted_report:
        lines += ["", "### Delisted on ReelShort (404), left in place", ""]
        lines += ["- `%s` %s" % d for d in delisted_report[:50]]
    if rulings_applied:
        lines += ["", "### AI rulings applied (Cyan, via the wanted file)", ""]
        lines += ["- `%s` ai=%s" % r for r in rulings_applied]
    if credits_added:
        lines += ["", "### Credits added (exact name, one person)", ""]
        lines += ["- %s: %s" % c for c in credits_added[:60]]
    if doc.get("errors"):
        lines += ["", "### Errors", ""]
        lines += ["- %s" % json.dumps(e) for e in (doc["errors"])[:30]]
    summary = "\n".join(lines) + "\n"
    print(summary)
    if a.summary:
        io.open(a.summary, "w", encoding="utf-8").write(summary)
    step = os.environ.get("GITHUB_STEP_SUMMARY")
    if step:
        io.open(step, "a", encoding="utf-8").write(summary)

    if a.dry_run:
        print("[dry-run] nothing written")
        return 0
    save("titles.csv", tf, titles)
    save("availability.csv", af, avail)
    save("snapshots.csv", sf, snaps)
    save("match_queue.csv", mf, mq)
    save("credits.csv", cf, credits)
    print("written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
