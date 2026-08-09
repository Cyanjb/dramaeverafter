#!/usr/bin/env python3
"""Score the database against Cyan's definition of a COMPLETE entry (8 Aug 2026):

    at least the leads, the platform, a link to watch it, and a description.

This replaces "cast is the biggest gap" as the steering metric. A castless title
and a title with cast but no watch link are both incomplete, and counting only
cast hid the second kind entirely. The second target is BREADTH: every platform
should carry a decent number of usable entries, not just the two we scrape well.

Usage:
    python3 completeness.py [--platform <id>] [--missing <field>]
"""
import csv, os, argparse
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")


def rows(n):
    with open(os.path.join(DATA, n), encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--platform")
    ap.add_argument("--missing", choices=["cast", "link", "desc", "any"])
    args = ap.parse_args()

    titles, credits, avail = rows("titles.csv"), rows("credits.csv"), rows("availability.csv")
    plats = {p["platform_id"]: p["name"] for p in rows("platforms.csv")}

    cast = defaultdict(int)
    for c in credits:
        cast[c["title_id"]] += 1
    av = defaultdict(list)
    for a in avail:
        av[a["title_id"]].append(a)

    per = defaultdict(lambda: {"n": 0, "complete": 0, "cast": 0, "link": 0, "desc": 0})
    gaps = defaultdict(list)

    for t in titles:
        tid = t["title_id"]
        rowsa = av.get(tid, [])
        has_cast = cast[tid] >= 2                      # "at least the leads"
        has_link = any((a.get("direct_link") or "").strip() for a in rowsa)
        has_desc = len((t.get("synopsis_short") or "").strip()) >= 40
        for a in rowsa or [{"platform_id": "(no platform)"}]:
            p = a["platform_id"]
            per[p]["n"] += 1
            per[p]["cast"] += has_cast
            per[p]["link"] += has_link
            per[p]["desc"] += has_desc
            if has_cast and has_link and has_desc and p != "(no platform)":
                per[p]["complete"] += 1
            else:
                miss = ([] if has_cast else ["cast"]) + ([] if has_link else ["link"]) + ([] if has_desc else ["desc"])
                gaps[p].append((t["primary_title"], ",".join(miss)))

    if args.platform:
        for name, miss in gaps.get(args.platform, [])[:60]:
            if not args.missing or args.missing == "any" or args.missing in miss:
                print(f"   {name[:52]:<54} missing: {miss}")
        return

    print(f"{'platform':<16}{'titles':>8}{'COMPLETE':>10}{'%':>6}   {'cast':>6}{'link':>6}{'desc':>6}")
    print("-" * 62)
    order = sorted(per.items(), key=lambda kv: -kv[1]["n"])
    tot = totc = 0
    for p, d in order:
        pct = 100 * d["complete"] / d["n"] if d["n"] else 0
        print(f"{plats.get(p, p)[:15]:<16}{d['n']:>8}{d['complete']:>10}{pct:>5.0f}%   "
              f"{d['cast']:>6}{d['link']:>6}{d['desc']:>6}")
        if p != "(no platform)":
            tot += d["n"]
            totc += d["complete"]
    print("-" * 62)
    print(f"{'TOTAL':<16}{tot:>8}{totc:>10}{100*totc/tot if tot else 0:>5.0f}%")
    print(f"\nCyan's bar: 2+ cast, a watch link, and a 40+ char description.")
    usable = [p for p, d in per.items() if d["complete"] >= 50 and p != "(no platform)"]
    print(f"platforms with 50+ complete entries: {len(usable)} of {len(per) - 1}"
          f"  -> {', '.join(plats.get(p, p) for p in usable) or 'NONE'}")


if __name__ == "__main__":
    main()
