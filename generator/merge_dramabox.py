#!/usr/bin/env python3
"""Merge one DramaBox scrape staging file into data/, under the database rules.

The sibling of merge_scrape.py (ReelShort), and every rule in that file's
docstring holds here too; its helpers are imported rather than copied, so the
two cannot drift on matching, CSV line endings or the tag vocabulary.

  EXACT MATCH (the numeric bookId in a DramaBox direct_link we already hold, on
    any of the three hosts on file: www.dramaboxdb.com/movie/<id>/..,
    dramaboxdb.com/movie/<id>/.., www.dramabox.com/drama/<id>/..):
    view_count and view_count_date update freely (CONVENTIONS.md),
    last_checked and last_verified move to the scrape date, and a DATED
    snapshots.csv row is written. Everything else is fill-blank-only:
    episode_count, poster_ref, year, title_as_listed, source_urls.
  LINK NEVER CAPTURED: we hold 61 DramaBox rows with no link. A scraped book
    whose house slug is that title's id, or whose name (leading article off,
    letters and digits only) is that title's primary or alt title, and which is
    the only book in the run with that name, fills the blank link and refreshes
    it. That row already says the title streams on DramaBox; only its URL was
    missing. A (DUBBED) listing never fills a link this way (the held row may
    be the original). Any other name match is a near match (below).
  NEW TITLE: created as data_confidence=needs_check with the house slug of the
    DramaBox name (dub marker stripped), only when the book was CHOSEN, not
    swept (Cyan, 8 Aug: newest, most popular, or credited to someone we track):
      - on the trending chart (/channel/trending): most popular, by DramaBox's
        own ranking;
      - on the homepage rails: newest and featured, as ReelShort's home route;
      - credited to someone we track: a cast name on the title page, or the
        /name/ page it was found on, matches exactly one person in people.csv;
      - otherwise (the must-sees and hidden-gems channels) only above
        POPULAR_MIN real plays, or first shelved within NEW_DAYS.
    A book that was never read on its own title page this run (no detail
    fetch: the URL is unconfirmed and the play count unknown) is never created.
  DUBS: "<Name> (DUBBED)" is DramaBox's English dub of a Chinese production.
    It is filed under <Name>, availability version=english-dub, origin=chinese
    (adapters.md sec 11; CONVENTIONS.md, one page per show). A dub whose name
    matches a title we hold is a near match and goes to match_queue, where
    Cyan rules same (it becomes that title's english-dub row) or different.
  ORIGIN: english unless the listing is a dub, bookInfo.language is not
    ENGLISH, or every credited performer (two or more) has a romanised Chinese
    name (pinyin syllables with a common Chinese surname): DramaBox carries
    subtitled Chinese productions with no marker. The ones set that way are
    listed in the summary for a check.
  NEAR MATCH: a same slug, a slug that matches with the hyphens removed, or a
    name that matches an existing primary or alt title after dropping the
    leading article, goes to match_queue.csv with the evidence and is NOT
    created. NEVER AUTO-MERGE (adapters.md sec 9: same-name productions across
    platforms are usually different shows). A slug is never suffixed to dodge
    a collision.
  DELISTED (404 on a link we hold): reported. Nothing is deleted by a machine.
  CREDITS: DramaBox's title page lists the cast (performerList) and its /name/
    page lists a performer's titles. A credit is added only when the name
    matches exactly one person in people.csv, by name or aka_names ('|' or ';'
    separated), role=actor, and the (title, person) pair is not already held.
    A name we do not hold becomes a person (Cyan, 30 Sep 2026); a near-name is
    held for her ruling. A name that matches two people is reported.
  SYNOPSES stay in the staging JSON. synopsis_short is never written from a
    platform: the caption pipeline owns that column (no copied copy, 14 Aug).

Usage:
    python3 generator/merge_dramabox.py generator/staging/dramabox_2026-10-04.json [--dry-run] [--summary FILE]

DEA_DATA points it at another data/ directory (a copy, for a test). Exit 0 on
success, 1 on a malformed staging file or an integrity failure.
"""
import argparse, datetime, difflib, io, json, os, re, sys, unicodedata
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import merge_scrape as ms  # noqa: E402  (honours DEA_DATA at import)
from merge_scrape import load, save, bare, nohyphen, split_alts, views_num, TAG_ALIASES, UMBRELLAS, EXCLUDE_RE  # noqa: E402

PLATFORM = "dramabox"
LABEL = "DramaBox"
STALE_DAYS = ms.STALE_DAYS
LINK_RE = re.compile(r"dramabox(?:db|app)?\.com/(?:[a-z]{2}(?:Hans)?/)?(?:movie|drama|video)/(\d{8,})", re.I)
CREATE_ROUTES = {"trending", "home"}
# The must-sees and hidden-gems channels are DramaBox's editorial shelves:
# ~140 books a week, most of them neither charting nor credited to anyone we
# track. They are created only when popular or new.
#
# POPULAR_MIN: measured on the first full run (28 Sep 2026, 346 books, every
# one read on its own title page). The 60 charting books had a median of 32.0M
# real plays (44 of 60 above 10M); the 104 books seen only on the must-sees and
# hidden-gems channels had a median of 29.6M, 76 of them above 10M. ReelShort's
# 10M bar would therefore import three quarters of two editorial shelves in one
# go, which is a sweep. 30M, about the chart's own median, admits a channel
# book only when it is as popular as a typical charting title: "most popular"
# by DramaBox's own yardstick. (Play counts are not comparable across
# platforms, adapters.md sec 29, so ReelShort's number is not borrowed.)
POPULAR_MIN = 30_000_000
# NEW_DAYS: "newest". A book first shelved within the last 30 days is a new
# release by any reading; DramaBox's firstShelfTime is on every title page.
NEW_DAYS = 30

# Romanised Chinese names, for the origin check. Surnames are the common ones;
# a token counts as pinyin when it splits wholly into pinyin syllables.
SURNAMES = set("""wang li zhang liu chen yang huang zhao wu zhou xu sun ma zhu hu guo he gao lin luo
zheng liang xie song tang han feng deng cao peng zeng xiao tian dong yuan pan yu jiang cai ye du cheng
wei su lu ding ren shen yao cui zhong tan fan jin shi liao jia xia fu fang bai zou meng xiong qin qiu
yin xue yan duan lei hou long tao gu mao hao gong shao wan qian dai mo kong xiang niu bao ning""".split())
_PY = re.compile(r"^(?:(?:zh|ch|sh|[bpmfdtnlgkhjqxrzcsyw])?(?:iang|iong|uang|ang|eng|ing|ong|ian|iao|uai|uan|"
                 r"ai|ei|ao|ou|an|en|er|in|un|ia|ie|iu|ua|uo|ui|ue|a|o|e|i|u|v))+$")


def pinyin_name(nm):
    toks = [t for t in re.split(r"[\s\-]+", (nm or "").lower()) if t]
    return len(toks) >= 2 and all(_PY.match(t) for t in toks) and any(t in SURNAMES for t in toks)


from scrape_dramabox import house_slug, split_dub  # noqa: E402


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
    # Name, dub flag and house slug are re-derived from the listed title with
    # the scraper's own functions, so a file written by an older scraper (the
    # first one missed full-width brackets) is read by today's rules.
    for b in books.values():
        if b.get("title"):
            b["name"], b["dubbed"] = split_dub(b["title"])
            b["slug"] = house_slug(b["name"])
    today = (doc.get("scraped_at") or datetime.datetime.now(datetime.timezone.utc).isoformat())[:10]
    source = "%s_weekly_%s" % (PLATFORM, today)
    new_cutoff = (datetime.date.fromisoformat(today) - datetime.timedelta(days=NEW_DAYS)).isoformat()

    titles, tf = load("titles.csv")
    avail, af = load("availability.csv")
    snaps, sf = load("snapshots.csv")
    mq, mf = load("match_queue.csv")
    credits, cf = load("credits.csv")
    people, pf = load("people.csv")
    trope_rows, trf = load("tropes.csv")

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
        m = LINK_RE.search(r.get("direct_link") or "")
        if m:
            link_rows.setdefault(m.group(1), r)
    # Held DramaBox rows with no link, by bare name, for the link-fill rule.
    blank_by_bare = {}
    for tid, r in plat_rows.items():
        if (r.get("direct_link") or "").strip() or tid not in by_id:
            continue
        t = by_id[tid]
        for nm in [t["primary_title"], r.get("title_as_listed_on_platform", "")] + split_alts(t.get("alt_titles")):
            if bare(nm):
                blank_by_bare.setdefault(bare(nm), set()).add(tid)
    name_in_run = Counter(bare(b.get("name") or "") for b in books.values() if b.get("name"))
    snap_keys = {(s["title_id"], s["platform_id"], s["date"]) for s in snaps}
    credit_keys = {(c["title_id"], c["person_id"]) for c in credits}
    person_ids = {}
    for p in people:
        for nm in [p["name"]] + re.split(r"[|;]", p.get("aka_names") or ""):
            nm = " ".join(nm.split()).lower()
            if nm:
                person_ids.setdefault(nm, set()).add(p["person_id"])

    def person_of(nm):
        ids = person_ids.get(" ".join((nm or "").split()).lower()) or set()
        return next(iter(ids)) if len(ids) == 1 else ("" if not ids else None)

    mq_text = "\n".join(r["candidate_b"] + " " + r["evidence"] for r in mq)

    n = Counter()
    new_titles, held, delisted_report, credits_added, ambiguous_names = [], [], [], [], Counter()
    origin_from_cast, filled_links = [], []
    catalogue_only = []

    def cast_names(b):
        out = list(b.get("actors") or [])
        for nm in b.get("cast_pages") or []:
            if nm not in out:
                out.append(nm)
        return out

    def tracked(b):
        return [nm for nm in cast_names(b) if person_of(nm)]

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
            if b.get("dubbed") and "version" in row and not row.get("version"):
                row["version"] = "english-dub"
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

    new_people, held_people = [], []
    all_pids = {p["person_id"] for p in people}

    def create_person(actor):
        """Cyan, 30 Sep 2026: a new show's actors must get their pages. A name we
        do not hold becomes a person (needs_check); a name only CLOSE to one we
        hold is held for her ruling, never created."""
        key = " ".join(actor.split()).lower()
        fold = lambda x: re.sub(r"[^a-z0-9]", "", unicodedata.normalize("NFKD", x).encode("ascii", "ignore").decode().lower())
        same = {pid for nm, ids in person_ids.items() if fold(nm) == fold(key) for pid in ids}
        if len(same) == 1:                       # "Sofia López" is sofia-lopez
            return next(iter(same))
        close = difflib.get_close_matches(key, list(person_ids), n=1, cutoff=0.9)
        if close:
            held_people.append((actor.strip(), sorted(person_ids[close[0]])))
            return ""
        pid = re.sub(r"-{2,}", "-", re.sub(r"[^a-z0-9]+", "-", unicodedata.normalize("NFKD", actor)
                     .encode("ascii", "ignore").decode().lower())).strip("-")
        if not pid or pid in all_pids:
            return ""
        people.append({k2: "" for k2 in pf} | {"person_id": pid, "slug": pid, "name": " ".join(actor.split()),
                       "role_type": "actor", "data_confidence": "needs_check",
                       "source": "dramabox_weekly_%s" % today})
        all_pids.add(pid)
        person_ids[key] = {pid}
        new_people.append(actor.strip())
        return pid

    def add_credits(tid, title_name, b):
        for actor in cast_names(b):
            pid = person_of(actor)
            if pid is None:
                ambiguous_names[actor] += 1
                continue
            if not pid:
                pid = create_person(actor)
            if not pid or (tid, pid) in credit_keys:
                continue
            credits.append({k: "" for k in cf} | {"title_id": tid, "person_id": pid,
                                                    "role": "actor", "character_name": ""})
            credit_keys.add((tid, pid))
            credits_added.append((title_name, actor))

    def origin_of(b):
        if b.get("dubbed"):
            return "chinese", ""
        lang = (b.get("language") or "").upper()
        if lang and lang != "ENGLISH":
            return ("chinese" if lang.startswith("CHINESE") or lang in ("ZH", "ZHHANS") else "english"), "language " + lang
        names = b.get("actors") or []
        if len(names) >= 2 and all(pinyin_name(x) for x in names):
            return "chinese", "cast " + ", ".join(names)
        return "english", ""

    def priority(item):
        bid, b = item
        return (b.get("rank") or 999, bool(b.get("dubbed")), bid)

    for bid, b in sorted(books.items(), key=priority):
        if b.get("status") not in (200, None, ""):
            continue
        row = link_rows.get(bid)
        if row is not None:
            t = by_id.get(row["title_id"])
            if t is None:
                n["orphan_rows"] += 1
                continue
            if "detail" in (b.get("seen_via") or []) and (b.get("title") or b.get("views")):
                touch(t, row, b)
                add_credits(t["title_id"], t["primary_title"], b)
            else:
                n["known_not_read"] += 1
            continue

        name, title, url = b.get("name") or "", b.get("title") or "", b.get("url") or ""
        if not name:
            n["no_data"] += 1
            continue
        if "detail" not in (b.get("seen_via") or []) or b.get("status") != 200:
            # Never read on its own page this run: URL and play count unconfirmed.
            n["not_read"] += 1
            continue
        if EXCLUDE_RE.match(name):
            n["excluded"] += 1
            continue
        slug = b.get("slug") or house_slug(name)

        # A held DramaBox row with no link: fill it (see the docstring).
        cands = set()
        if slug in plat_rows and not (plat_rows[slug].get("direct_link") or "").strip():
            cands.add(slug)
        if name_in_run[bare(name)] == 1:
            cands |= blank_by_bare.get(bare(name), set())
        cands = {c for c in cands if not (plat_rows[c].get("direct_link") or "").strip()}
        # A (DUBBED) listing never fills a held row's link: that row may be the
        # original, and a dub is a second row on Cyan's ruling (match_queue).
        if len(cands) == 1 and not b.get("dubbed"):
            tid = cands.pop()
            touch(by_id[tid], plat_rows[tid], b)
            link_rows[bid] = plat_rows[tid]
            add_credits(tid, by_id[tid]["primary_title"], b)
            filled_links.append((tid, url))
            continue

        vias = set(b.get("seen_via") or [])
        views = views_num(b.get("views"))
        why_create = ("chart #%s" % b["rank"] if "trending" in vias and b.get("rank") else
                      "homepage" if vias & CREATE_ROUTES else
                      "credited to " + ", ".join(tracked(b)) if tracked(b) else
                      "%s plays" % b.get("views") if views >= POPULAR_MIN else
                      "new (%s)" % b.get("first_shelf") if (b.get("first_shelf") or "") >= new_cutoff else "")
        if not why_create:
            catalogue_only.append((name, b.get("views") or "", b.get("first_shelf") or ""))
            continue

        existing = by_id.get(slug)
        near = (existing["title_id"] if existing is not None else None) \
            or by_nohyphen.get(nohyphen(slug)) or by_bare.get(bare(name))
        if near:
            if re.search(r"(^|\s)%s \(%s" % (re.escape(slug), LABEL), mq_text, re.M) \
                    or re.search(r"/(?:movie|drama)/%s(?!\d)" % bid, mq_text):
                n["already_queued"] += 1
                continue
            why = ("same slug" if near == slug else
                   "slug matches with hyphens removed" if by_nohyphen.get(nohyphen(slug)) == near
                   else "same title after dropping the leading article")
            ex = by_id[near]
            mq.append({"candidate_a": "%s (existing)" % near,
                       "candidate_b": "%s (%s weekly scrape %s)" % (slug, LABEL, today),
                       "evidence": "%s; existing '%s' source=%s origin=%s; %s lists '%s' at %s%s%s%s"
                                   % (why, ex["primary_title"], ex.get("source", ""), ex.get("origin", ""),
                                      LABEL, title, url,
                                      (", %s episodes" % b["episodes"]) if b.get("episodes") else "",
                                      (", %s plays" % b["views"]) if b.get("views") else "",
                                      (", cast " + ", ".join(b["actors"][:4])) if b.get("actors") else "")
                                   + ("; DramaBox marks it (DUBBED): if same, it is that title's english-dub row"
                                      if b.get("dubbed") else ""),
                       "status": "pending"})
            mq_text += "\n%s (%s %s" % (slug, LABEL, url)
            held.append((title, near, why))
            continue

        # Genuinely new, and chosen by Cyan's rule.
        origin, origin_why = origin_of(b)
        if origin_why and origin != "english":
            origin_from_cast.append((slug, origin_why))
        t = {k: "" for k in tf}
        t.update({"title_id": slug, "slug": slug, "primary_title": name, "year": b.get("year") or "",
                  "episode_count": b.get("episodes") or "", "poster_ref": b.get("poster") or "",
                  "source_urls": url, "last_verified": today, "data_confidence": "needs_check",
                  "source": source, "origin": origin})
        titles.append(t)
        by_id[slug] = t
        by_nohyphen[nohyphen(slug)] = slug
        by_bare[bare(name)] = slug
        r = {k: "" for k in af}
        r.update({"title_id": slug, "platform_id": PLATFORM, "title_as_listed_on_platform": title,
                  "direct_link": url, "view_count": b.get("views") or "",
                  "view_count_date": today if b.get("views") else "", "last_checked": today})
        if "version" in r:
            r["version"] = "english-dub" if b.get("dubbed") else ""
        avail.append(r)
        link_rows[bid] = r
        plat_rows[slug] = r
        if b.get("views"):
            snaps.append({"title_id": slug, "platform_id": PLATFORM, "view_count": b["views"], "date": today})
            snap_keys.add((slug, PLATFORM, today))
            n["snapshots"] += 1
        new_titles.append((name, slug, b.get("views") or "", why_create, origin))
        add_credits(slug, name, b)

    # CYAN'S "SAME" RULINGS ON DRAMABOX WEEKLY-SCRAPE MATCH_QUEUE ROWS: link the
    # held title to the DramaBox page named in the evidence (fill-blank), with
    # version=english-dub when the listing was a dub, and take this run's counts.
    linked_same = []
    for r in mq:
        if "%s weekly scrape" % LABEL not in r.get("candidate_b", "") \
                or not r.get("status", "").startswith("confirmed_same"):
            continue
        m = LINK_RE.search(r.get("evidence", ""))
        tid = r["candidate_a"].split()[0]
        if not m or tid not in by_id or m.group(1) in link_rows:
            continue
        b = books.get(m.group(1)) or {}
        # DramaBox writes the marker with full-width brackets too, "（DUBBED）"
        # (Fortunes Unveiled, 6 Oct 2026); the scraper's own flag is the truth.
        dub = bool(b.get("dubbed")) or bool(re.search(r"[(（]DUBBED[)）]", r.get("evidence", "")))
        row = plat_rows.get(tid)
        if row is not None and (row.get("direct_link") or "").strip():
            # A second DramaBox listing of a title we already link. The dub of
            # an original we hold is exactly that: a second row, english-dub.
            if not dub:
                continue
            row = None
        if row is None:
            row = {k: "" for k in af}
            row.update({"title_id": tid, "platform_id": PLATFORM,
                        "title_as_listed_on_platform": b.get("title") or by_id[tid]["primary_title"]})
            if "version" in row:
                row["version"] = "english-dub" if dub else ""
            avail.append(row)
            plat_rows.setdefault(tid, row)
        row["direct_link"] = "https://www.dramaboxdb.com/movie/%s" % m.group(1)
        if b.get("url"):
            row["direct_link"] = b["url"]
        link_rows[m.group(1)] = row
        if b and b.get("status") == 200 and (b.get("title") or b.get("views")):
            touch(by_id[tid], row, b)
        else:
            row["last_checked"] = row.get("last_checked") or today
        linked_same.append((tid, row["direct_link"]))

    # TROPES FROM DRAMABOX'S OWN TAGS, vocabulary only (as merge_scrape.py).
    vocab = {}
    for tr in trope_rows:
        for key in (tr.get("name", ""), tr.get("slug", ""), tr.get("trope_id", "")):
            if key:
                vocab[re.sub(r"[^a-z0-9]", "", key.lower())] = tr.get("name") or tr.get("trope_id")

    def add_trope(t, name):
        have = [x.strip() for x in (t.get("tropes") or "").split(";") if x.strip()]
        if name.lower() not in {h.lower() for h in have}:
            t["tropes"] = ";".join(have + [name])
            return True
        return False

    tag_unknown, tags_applied = Counter(), 0
    for bid, b in books.items():
        row = link_rows.get(bid)
        t = by_id.get(row["title_id"]) if row else None
        if t is None or b.get("status") != 200:
            continue
        for tag in b.get("tags") or []:
            key = TAG_ALIASES.get(tag.lower(), tag.lower())
            name = vocab.get(re.sub(r"[^a-z0-9]", "", key))
            if not name:
                tag_unknown[tag] += 1
            elif add_trope(t, name):
                tags_applied += 1

    umbrella_added = Counter()
    for umb, members in UMBRELLAS.items():
        if re.sub(r"[^a-z0-9]", "", umb) not in vocab:
            continue
        for t in titles:
            have = {x.strip().lower() for x in (t.get("tropes") or "").split(";") if x.strip()}
            if have & members and umb not in have and add_trope(t, vocab[re.sub(r"[^a-z0-9]", "", umb)]):
                umbrella_added[umb] += 1

    tcount = Counter()
    for t in titles:
        for x in {x.strip().lower() for x in (t.get("tropes") or "").split(";") if x.strip()}:
            tcount[x] += 1
    for tr in trope_rows:
        tr["title_count"] = str(tcount.get((tr.get("name") or "").lower(), 0))

    for d in doc.get("delisted") or []:
        tid = d.get("title_id") or (link_rows.get(d.get("book_id"), {}) or {}).get("title_id", "")
        delisted_report.append((tid or "(not held)", d.get("url", "")))

    ids = Counter(t["title_id"] for t in titles)
    dups = [k for k, v in ids.items() if v > 1]
    if dups:
        print("REFUSING TO WRITE: duplicate title_ids", dups[:5], file=sys.stderr)
        return 1

    cutoff = (datetime.date.fromisoformat(today) - datetime.timedelta(days=STALE_DAYS)).isoformat()
    stale = sum(1 for r in avail if r["platform_id"] == PLATFORM and (r.get("last_checked") or "") < cutoff)
    routes = doc.get("routes") or {}

    lines = ["## %s weekly scrape, %s%s" % (LABEL, today, " (dry run)" if a.dry_run else ""), ""]
    lines.append("| | |")
    lines.append("|---|---|")
    lines.append("| Requests | %s |" % doc.get("requests", "?"))
    lines.append("| Books seen | %d |" % len(books))
    lines.append("| Known titles refreshed | %d |" % n["refreshed"])
    lines.append("| View counts that moved | %d |" % n["views_changed"])
    lines.append("| Snapshot rows written | %d |" % n["snapshots"])
    lines.append("| New titles created | %d |" % len(new_titles))
    lines.append("| Held for a ruling (match_queue) | %d |" % len(held))
    lines.append("| Already in match_queue, awaiting a ruling | %d |" % n["already_queued"])
    lines.append("| Credits added | %d |" % len(credits_added))
    lines.append("| New people (actor pages) created / close names held for a ruling | %d / %d |" % (len(new_people), len(held_people)))
    lines.append("| Blank DramaBox links filled on titles we hold | %d |" % len(filled_links))
    lines.append("| Episode counts / posters / links / years filled | %d / %d / %d / %d |"
                 % (n["episodes_filled"], n["posters_filled"], n["links_filled"], n["years_filled"]))
    lines.append("| Delisted (404, not deleted) | %d |" % len(delisted_report))
    lines.append("| Channel only (not charting, homepage or credited; under %dM plays; older than %d days), not imported | %d |"
                 % (POPULAR_MIN // 1_000_000, NEW_DAYS, len(catalogue_only)))
    lines.append("| Not read on its own page this run (unconfirmed), not imported / known links not read | %d / %d |"
                 % (n["not_read"], n["known_not_read"]))
    lines.append("| Excluded as unscripted | %d |" % n["excluded"])
    lines.append("| %s rows still older than %d days | %d |" % (LABEL, STALE_DAYS, stale))
    lines.append("| Tropes from %s's tags (vocabulary only) / tag names unknown | %d / %d |"
                 % (LABEL, tags_applied, len(tag_unknown)))
    lines.append("| Umbrella tropes added | %s |" % (", ".join("%s %d" % kv for kv in umbrella_added.items()) or "0"))
    lines.append("| Linked on Cyan's confirmed_same rulings | %d |" % len(linked_same))
    lines.append("| Cast names matching two or more people (no credit) | %d |" % len(ambiguous_names))
    lines.append("| Scrape errors | %d |" % len(doc.get("errors") or []))
    lines.append("")
    lines.append("Routes: " + ", ".join("%s %s" % (k, json.dumps(v)) for k, v in routes.items()))
    if new_titles:
        lines += ["", "### New titles (needs_check): each one needs a caption", "",
                  "Live with no synopsis of ours. Platform text is never copied (Cyan, 14 Aug); "
                  "DramaBox's introduction is banked in the staging JSON as the fact source for "
                  "`caption_pipeline.py next`.", ""]
        lines += ["- %s (`%s`) %s, %s, origin %s" % x for x in new_titles]
    if origin_from_cast:
        lines += ["", "### Origin set to chinese without a (DUBBED) marker (check these)", ""]
        lines += ["- `%s`: %s" % x for x in origin_from_cast]
    if held:
        lines += ["", "### Held for Cyan's ruling", ""]
        lines += ["- '%s' vs existing `%s`: %s" % h for h in held]
    if filled_links:
        lines += ["", "### DramaBox links filled on rows we held without one", ""]
        lines += ["- `%s` %s" % x for x in filled_links]
    if delisted_report:
        lines += ["", "### Delisted on %s (404), left in place" % LABEL, ""]
        lines += ["- `%s` %s" % d for d in delisted_report[:50]]
    if tag_unknown:
        lines += ["", "### %s tag names not in our vocabulary (Cyan decides; count of books)" % LABEL, ""]
        lines += ["- %s (%d)" % kv for kv in tag_unknown.most_common(40)]
    if linked_same:
        lines += ["", "### Linked to %s on Cyan's confirmed_same rulings" % LABEL, ""]
        lines += ["- `%s` %s" % x for x in linked_same]
    if credits_added:
        lines += ["", "### Credits added (exact name, one person)", ""]
        lines += ["- %s: %s" % c for c in credits_added[:80]]
    if ambiguous_names:
        lines += ["", "### Cast names that match more than one person (no credit)", ""]
        lines += ["- %s" % nm for nm in sorted(ambiguous_names)]
    if doc.get("errors"):
        lines += ["", "### Errors", ""]
        lines += ["- %s" % json.dumps(e) for e in (doc["errors"])[:30]]
    if held_people:
        lines += ["", "### Cast names close to someone we hold (not created; Cyan rules)", ""]
        lines += ["- %s ~ %s" % (a_, ", ".join(ids)) for a_, ids in held_people[:60]]
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
    save("people.csv", pf, people)
    save("tropes.csv", trf, trope_rows)
    print("written to", ms.DATA)
    return 0


if __name__ == "__main__":
    sys.exit(main())
