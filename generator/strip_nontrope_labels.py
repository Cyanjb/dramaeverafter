#!/usr/bin/env python3
"""Remove two labels the My Drama harvest imported that are not tropes.

My Drama's genre[] array mixes CONTENT attributes with UI labels. Almost all of it
is genuinely trope-shaped and consistent with a vocabulary that already carries
romance (116), fantasy (86), animation (46), drama (24) and comedy (17) - so
romcom, young adult, paranormal and celebrity all stay. Two do not:

  trending    22 titles. Not a content attribute at all - it is a recency label
              from My Drama's own merchandising. It clears the 5+ bar, so it WOULD
              have published /tropes/trending.html: a page that cannot ever be
              accurate, because trending-when is unanswerable and nothing on the
              site would update it. A trope page is a promise about content.

  male lead    2 titles. A cast descriptor. Below the 5+ publish bar so it renders
              no page, but it would still show as a chip on two title pages and sit
              in the A-Z vocabulary.

Both are NEW - neither existed in the vocabulary before the 13 Aug harvest, so this
removes nothing that predates it. The separator is ';' per build.py's _raw_tropes.

Usage:
    py strip_nontrope_labels.py [--dry-run]
"""
import csv, io, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "data")
DROP = {"trending", "male lead"}
DRY = "--dry-run" in sys.argv


def term_of(p):
    raw = open(p, "rb").read()
    c = raw.count(b"\r\n")
    return "\r\n" if c > raw.count(b"\n") - c else "\n"


def main():
    p = os.path.join(DATA, "titles.csv")
    titles = list(csv.DictReader(open(p, newline="", encoding="utf-8")))
    fields = list(titles[0].keys())

    changed = 0
    emptied = 0
    for t in titles:
        vals = [x.strip() for x in (t.get("tropes") or "").split(";") if x.strip()]
        keep = [x for x in vals if x.lower() not in DROP]
        if len(keep) != len(vals):
            changed += 1
            if not keep:
                emptied += 1
            t["tropes"] = ";".join(keep)

    print("titles touched            : %d" % changed)
    print("left with NO trope at all : %d" % emptied)

    if DRY:
        print("[dry-run] nothing written")
        return 0

    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=fields, lineterminator=term_of(p))
    w.writeheader()
    w.writerows(titles)
    open(p, "w", newline="", encoding="utf-8").write(buf.getvalue())
    print("written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
