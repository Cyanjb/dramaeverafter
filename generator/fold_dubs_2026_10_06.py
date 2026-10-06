#!/usr/bin/env python3
"""Fold four DramaBox dub listings onto their originals' pages.

Cyan, 6 Oct 2026, on Fortunes Unveiled: "They're both the same. It's just
one's dubbed and one isn't." Her standing rule (CONVENTIONS.md, 24 Sep):
a dub belongs on the original's page as a second availability row with
version=english-dub. Four such pairs were on the rulings page, two because
DramaBox writes "（DUBBED）" with full-width brackets (now recognised).

Usage: python3 generator/fold_dubs_2026_10_06.py [--apply]
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from merge_scrape import load, save

DB = json.load(open(os.path.join(HERE, "staging", "dramabox_2026-09-28.json"), encoding="utf-8"))
BOOKS = {str(b["book_id"]): b for b in (DB["books"].values() if isinstance(DB["books"], dict) else DB["books"])}
FOLD = {"fortunes-unveiled-my-husband-is-a-big-shot": "41000103524"}
# the other three: dub book ids read from their match_queue evidence below
SLUGS = ["masked-magnate-the-dominant-son-in-law", "the-lost-heir-his-dawn-of-reckoning",
         "trails-of-hope-his-journey-back-home"]


def main(apply):
    import re
    A, af = load("availability.csv"); S, sf = load("snapshots.csv"); Q, qf = load("match_queue.csv")
    for r in Q:
        tid = r["candidate_a"].split(" (")[0]
        if r["status"] == "pending" and tid in SLUGS + list(FOLD) and "DUBBED" in r["candidate_b"] + r["evidence"]:
            m = re.search(r"/movie/(\d+)/", r["evidence"])
            if m and BOOKS.get(m.group(1), {}).get("dubbed"):
                FOLD[tid] = m.group(1)
                r["status"] = "confirmed_same (Cyan, 2026-10-06: dub of the original, folded as english-dub)"
    for tid, bid in FOLD.items():
        b = BOOKS[bid]
        if any(x["title_id"] == tid and bid in (x["direct_link"] or "") for x in A):
            print("already folded", tid); continue
        A.append({k: "" for k in af} | {"title_id": tid, "platform_id": "dramabox",
                  "title_as_listed_on_platform": b["title"], "direct_link": b.get("url") or "https://www.dramaboxdb.com/movie/%s" % bid,
                  "view_count": b.get("views") or "", "view_count_date": "2026-09-28" if b.get("views") else "",
                  "last_checked": "2026-10-06", "version": "english-dub"})
        if b.get("views"):
            S.append({k: "" for k in sf} | {"title_id": tid, "platform_id": "dramabox", "view_count": b["views"], "date": "2026-09-28"})
        print("folded dub", bid, "->", tid)
    if apply:
        save("availability.csv", af, A); save("snapshots.csv", sf, S); save("match_queue.csv", qf, Q); print("applied")


if __name__ == "__main__":
    main("--apply" in sys.argv)
