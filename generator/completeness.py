#!/usr/bin/env python3
"""Score the database against Cyan's definition of a COMPLETE entry (13 Aug 2026):

    a title, a caption WE wrote, at least the leads, a link to the platform,
    and at least one trope.

This replaces "cast is the biggest gap" as the steering metric. A castless title
and a title with cast but no watch link are both incomplete, and counting only
cast hid the second kind entirely. The second target is BREADTH: every platform
should carry a decent number of usable entries, not just the two we scrape well.

TWO CRITERIA WERE ADDED ON 13 AUG and the headline number fell 26% -> 15%. That
is the metric ceasing to flatter itself, not the database getting worse.

  >=1 TROPE. Tropes are how this audience actually browses, and an entry with no
  trope is invisible to every trope page and every combo page on the site. 78% of
  titles already carry one, so the failures are concentrated in otherwise-finished
  entries and are cheap to fix.

  THE CAPTION MUST BE OURS. The old check measured LENGTH only (>=40 chars), so a
  scraper truncation counted as a description - which meant the metric was passing
  entries that violate the standing caption rule. Provenance cannot be fully
  verified after the fact, but the two known truncation shapes can: EXACTLY 300
  characters (687 rows, mostly GoodShort) or EXACTLY 300 bytes (27 rows, mostly
  CandyJar), both documented on the traps list. Those are proof the text is the
  platform's, not ours. This is a floor, not a guarantee: an untruncated synopsis
  copied verbatim would still pass, so the rule is enforced at WRITE time and this
  only catches the mechanical cases.

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
    ap.add_argument("--missing", choices=["cast", "link", "desc", "trope", "any"])
    args = ap.parse_args()

    titles, credits, avail = rows("titles.csv"), rows("credits.csv"), rows("availability.csv")
    plats = {p["platform_id"]: p["name"] for p in rows("platforms.csv")}

    cast = defaultdict(int)
    for c in credits:
        cast[c["title_id"]] += 1
    av = defaultdict(list)
    for a in avail:
        av[a["title_id"]].append(a)

    per = defaultdict(lambda: {"n": 0, "complete": 0, "cast": 0, "link": 0, "desc": 0, "trope": 0})
    gaps = defaultdict(list)

    for t in titles:
        tid = t["title_id"]
        rowsa = av.get(tid, [])
        syn = (t.get("synopsis_short") or "").strip()
        # The two documented scraper truncation shapes. Either one proves the text
        # came from the platform rather than from us, so it is not a caption.
        truncated = len(syn) == 300 or len(syn.encode("utf-8")) == 300
        has_cast = cast[tid] >= 2                      # "at least the leads"
        has_link = any((a.get("direct_link") or "").strip() for a in rowsa)
        has_desc = len(syn) >= 40 and not truncated
        has_trope = bool((t.get("tropes") or "").strip())
        for a in rowsa or [{"platform_id": "(no platform)"}]:
            p = a["platform_id"]
            per[p]["n"] += 1
            per[p]["cast"] += has_cast
            per[p]["link"] += has_link
            per[p]["desc"] += has_desc
            per[p]["trope"] += has_trope
            if has_cast and has_link and has_desc and has_trope and p != "(no platform)":
                per[p]["complete"] += 1
            else:
                miss = (([] if has_cast else ["cast"]) + ([] if has_link else ["link"])
                        + ([] if has_desc else ["desc"]) + ([] if has_trope else ["trope"]))
                gaps[p].append((t["primary_title"], ",".join(miss)))

    if args.platform:
        for name, miss in gaps.get(args.platform, [])[:60]:
            if not args.missing or args.missing == "any" or args.missing in miss:
                print(f"   {name[:52]:<54} missing: {miss}")
        return

    print(f"{'platform':<16}{'titles':>8}{'COMPLETE':>10}{'%':>6}   "
          f"{'cast':>6}{'link':>6}{'desc':>6}{'trope':>6}")
    print("-" * 68)
    order = sorted(per.items(), key=lambda kv: -kv[1]["n"])
    tot = totc = 0
    for p, d in order:
        pct = 100 * d["complete"] / d["n"] if d["n"] else 0
        print(f"{plats.get(p, p)[:15]:<16}{d['n']:>8}{d['complete']:>10}{pct:>5.0f}%   "
              f"{d['cast']:>6}{d['link']:>6}{d['desc']:>6}{d['trope']:>6}")
        if p != "(no platform)":
            tot += d["n"]
            totc += d["complete"]
    print("-" * 68)
    print(f"{'TOTAL':<16}{tot:>8}{totc:>10}{100*totc/tot if tot else 0:>5.0f}%")
    print("\nCyan's bar (13 Aug): a title, a caption WE wrote, 2+ cast, a watch link,"
          "\nand at least one trope. 'desc' excludes the 300-char and 300-byte scraper"
          "\ntruncations, which are the platform's text and not a caption.")
    usable = [p for p, d in per.items() if d["complete"] >= 50 and p != "(no platform)"]
    print(f"platforms with 50+ complete entries: {len(usable)} of {len(per) - 1}"
          f"  -> {', '.join(plats.get(p, p) for p in usable) or 'NONE'}")


if __name__ == "__main__":
    main()
