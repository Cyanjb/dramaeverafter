"""Add the CandyJar titles IMDb lists that we do not hold, and record the tt id on those we do.

Cyan's instruction: add them blank and fill synopses from CandyJar's own site later. So a
new row carries title, year, platform and the IMDb URL as its source, and NOTHING ELSE.
No synopsis, no poster, no genres, no tropes - inventing any of that is the failure mode
this project keeps refusing.

SLUGS ARE PERMANENT URLS, so a new slug is only minted when it collides with nothing. A
collision means the title probably already exists under a different primary_title and the
row is skipped for a human to look at, never auto-suffixed into a second page.

A NEAR-DUPLICATE GUARD, added after a dry run showed the naive version creating four
duplicate pages. IMDb and the platforms disagree about articles and subtitles:

  - ARTICLE ONLY ("Alpha's Doe" vs our "The Alpha's Doe", "Billionaire's Baby" vs
    "The Billionaire's Baby"). Same title, so the existing row is used.
  - ANYTHING ELSE that scores close ("The Arrangement: Parts 3 & 4" against our separate
    "The Arrangement 3" and "The Arrangement 4"; "Broken: Enemies Attract" against our
    CandyJar "Broken"). NOT created and NOT merged - queued for a ruling, because a
    combined two-part entry and two single-part entries are not obviously the same thing,
    and guessing either way corrupts real pages.

Existing titles get their IMDb URL written into source_urls if that field is empty, which
is the first time any title in the database records where it can be verified.
"""
import csv, io, os, re, sys, time, difflib, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.environ.get("DEA_DATA") or os.path.join(os.path.dirname(HERE), "data")
SOURCE = "imdb_candyjar_company_2026-08-03"
TODAY = time.strftime("%Y-%m-%d")

spec = importlib.util.spec_from_file_location("cj", os.path.join(HERE, "candyjar_company_list_2026_08_03.py"))
cj = importlib.util.module_from_spec(spec); spec.loader.exec_module(cj)

def slugify(s): return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
def norm(s):
    s = s.lower().replace("’", "'").replace("&", "and")
    return re.sub(r"[^a-z0-9]+", "", s)
def term_of(p):
    raw = open(p, "rb").read(); c = raw.count(b"\r\n")
    return "\r\n" if c > raw.count(b"\n") - c else "\n"
def load(n): return list(csv.DictReader(open(os.path.join(DATA, n), newline="", encoding="utf-8")))
def save(n, fields, recs):
    p = os.path.join(DATA, n); buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=fields, lineterminator=term_of(p))
    w.writeheader(); w.writerows(recs)
    open(p, "w", newline="", encoding="utf-8").write(buf.getvalue())

def stem(s):
    """Normalised key with a leading article dropped, so 'Alpha's Doe' meets 'The Alpha's Doe'."""
    n = norm(s)
    return n[3:] if n.startswith("the") else n

titles, avail, queue = load("titles.csv"), load("availability.csv"), load("match_queue.csv")
by_norm, by_stem = {}, {}
for t in titles:
    by_norm.setdefault(norm(t["primary_title"]), t)
    by_stem.setdefault(stem(t["primary_title"]), t)
used_ids = {t["title_id"] for t in titles} | {t["slug"] for t in titles}
have_av = {(a["title_id"], a["platform_id"]) for a in avail}
queued = {(q["candidate_a"], q["candidate_b"]) for q in queue}

new_titles, new_avail, tagged, collided, to_queue = [], [], [], [], []

for name, year, tt in cj.TITLES:
    url = f"https://www.imdb.com/title/{tt}/"
    t = by_norm.get(norm(name)) or by_stem.get(stem(name))
    if t is None:
        # Close but not article-only: do not create a second page for what may be the
        # same production, and do not merge either. Queue it.
        close = difflib.get_close_matches(norm(name), list(by_norm.keys()), n=1, cutoff=0.82)
        # Subtitle case, which similarity scoring misses entirely: IMDb's
        # "Broken: Enemies Attract" against our CandyJar "Broken" scores nowhere near the
        # cutoff, yet a title that is an existing title plus ": subtitle" is the single most
        # likely way the same production appears under two names.
        if not close and ":" in name:
            head = norm(name.split(":", 1)[0])
            if head in by_norm: close = [head]
        if close:
            other = by_norm[close[0]]
            pair = (other["title_id"], slugify(name))
            if pair not in queued:
                queued.add(pair)
                to_queue.append({"candidate_a": other["title_id"], "candidate_b": slugify(name),
                                 "evidence": f"IMDb's CandyJar company page (co1130595) lists '{name}' "
                                             f"({tt}); titles.csv has '{other['primary_title']}'. Same "
                                             f"platform, similar name, but a combined or renumbered part "
                                             f"is not obviously the same entry. Not added, not merged. "
                                             f"Source: {SOURCE}.",
                                 "status": "pending"})
            collided.append(f"{name}  ~  {other['primary_title']}")
            continue
    if t is not None:
        if not (t.get("source_urls") or "").strip():
            t["source_urls"] = url
            tagged.append(f"{t['primary_title']} -> {tt}")
        if (t["title_id"], "candyjar") not in have_av:
            new_avail.append({"title_id": t["title_id"], "platform_id": "candyjar",
                              "title_as_listed_on_platform": name, "direct_link": "",
                              "free_episode_count": "", "view_count": "", "view_count_date": "",
                              "last_checked": TODAY})
            have_av.add((t["title_id"], "candyjar"))
        continue
    tid = slugify(name)
    if tid in used_ids:
        collided.append(name); continue
    used_ids.add(tid)
    row = {k: "" for k in titles[0].keys()}
    row.update({"title_id": tid, "slug": tid, "primary_title": name, "year": year,
                "source_urls": url, "last_verified": TODAY,
                "data_confidence": "needs_check", "source": SOURCE, "origin": "english"})
    new_titles.append(row)
    new_avail.append({"title_id": tid, "platform_id": "candyjar",
                      "title_as_listed_on_platform": name, "direct_link": "",
                      "free_episode_count": "", "view_count": "", "view_count_date": "",
                      "last_checked": TODAY})

print(f"new titles: {len(new_titles)}")
for r in new_titles: print("   +", r["title_id"], r["year"], r["source_urls"])
print(f"new availability rows: {len(new_avail)}")
print(f"IMDb URL recorded on existing titles: {len(tagged)}")
print(f"near-duplicates queued instead of created: {len(collided)}")
for c in collided: print("   ", c)

if "--dry-run" in sys.argv:
    print("(dry run, nothing written)"); raise SystemExit

if new_titles or tagged: save("titles.csv", list(titles[0].keys()), titles + new_titles)
if new_avail: save("availability.csv", list(avail[0].keys()), avail + new_avail)
if to_queue: save("match_queue.csv", list(queue[0].keys()), queue + to_queue)
print(f"\nwrote {len(new_titles)} titles, {len(new_avail)} availability rows, "
      f"{len(tagged)} source URLs, {len(to_queue)} queued")
