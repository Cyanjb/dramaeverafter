#!/usr/bin/env python3
"""Set origin=chinese on GoodShort's translated shows, from GoodShort's own flag.

    python3 generator/goodshort_origin.py fetch     read each title's GoodShort page (resumable)
    python3 generator/goodshort_origin.py apply     dry run: what origin would change
    python3 generator/goodshort_origin.py apply --apply

Born 24 Sep 2026 (Cyan: "mark the chinese shows"). GoodShort's page data carries
a novelType on every book: ORIGINAL for its English-made shows (I'm the Mafia
Girl Boss, When the Wolf Fell in Love) and TRANSLATION for foreign productions
it subtitles or dubs (A Dazzling Beauty and its [ENG DUB]). It does not name
the country. TRANSLATION is read as Chinese on this evidence, checked the day
it was written: every sampled TRANSLATION poster shows a Chinese short-drama
cast (one a Chinese period drama), and viewers and archives file the sampled
titles as Chinese dramas. Korean and Japanese productions could in principle
slip in; set those by hand, and this tool never overwrites a non-english origin.

The record, generator/staging/goodshort_origin.json, keeps what the page said
for every title, so a ruling can be traced to its source.
"""
import csv, io, json, os, re, sys, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
RECORD = os.path.join(HERE, "staging", "goodshort_origin.json")


def load(n):
    with open(os.path.join(DATA, n), newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        return list(r), list(r.fieldnames)


def term_of(p):
    raw = open(p, "rb").read()
    c = raw.count(b"\r\n")
    return "\r\n" if c > raw.count(b"\n") - c else "\n"


def novel_type(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    s = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")
    bid = re.search(r"-(\d{8,})/?$", url).group(1)
    i = s.find(f'"bookId":"{bid}"')
    if i < 0:
        return None
    m = re.search(r'"novelType":"([A-Z_]+)"', s[i:i + 6000])
    return m.group(1) if m else None


def fetch():
    avail, _ = load("availability.csv")
    rec = json.load(open(RECORD, encoding="utf-8")) if os.path.exists(RECORD) else {}
    todo = {}
    for a in avail:
        link = (a.get("direct_link") or "").strip()
        if a["platform_id"] != "goodshort" or not link or a["title_id"] in rec:
            continue
        # The original's own listing first; a dub-only title has only its dub.
        if a["title_id"] not in todo or not (a.get("version") or ""):
            todo[a["title_id"]] = link
    print(f"{len(rec)} already recorded, {len(todo)} to fetch")
    for n, (tid, link) in enumerate(sorted(todo.items()), 1):
        try:
            nt = novel_type(link)
        except Exception as e:
            nt = f"ERROR {type(e).__name__}"
        rec[tid] = {"url": link, "novelType": nt, "fetched": time.strftime("%Y-%m-%d")}
        if n % 50 == 0 or n == len(todo):
            json.dump(rec, open(RECORD, "w", encoding="utf-8"), indent=1, sort_keys=True)
            print(f"  {n}/{len(todo)}", flush=True)
        time.sleep(1.0)
    json.dump(rec, open(RECORD, "w", encoding="utf-8"), indent=1, sort_keys=True)


def apply(write):
    rec = json.load(open(RECORD, encoding="utf-8"))
    titles, tf = load("titles.csv")
    tally, changed = {}, 0
    for t in titles:
        r = rec.get(t["title_id"])
        if not r:
            continue
        tally[r["novelType"]] = tally.get(r["novelType"], 0) + 1
        cur = (t.get("origin") or "").strip().lower() or "english"
        if r["novelType"] == "TRANSLATION" and cur == "english":
            t["origin"] = "chinese"; changed += 1
    print("GoodShort novelType:", tally)
    print(f"origin english -> chinese: {changed}")
    if write:
        p = os.path.join(DATA, "titles.csv")
        buf = io.StringIO()
        w = csv.DictWriter(buf, fieldnames=tf, lineterminator=term_of(p))
        w.writeheader(); w.writerows(titles)
        open(p, "w", newline="", encoding="utf-8").write(buf.getvalue())
        print("written")
    else:
        print("[dry run] nothing written")


if __name__ == "__main__":
    if sys.argv[1:2] == ["fetch"]: fetch()
    elif sys.argv[1:2] == ["apply"]: apply("--apply" in sys.argv)
    else: sys.exit(__doc__)
