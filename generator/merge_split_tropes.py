#!/usr/bin/env python3
"""Merge three trope spellings the My Drama harvest split off from existing ones.

THE HARVEST MATCHED THE EXISTING VOCABULARY BY EXACT SLUG, which is the same key
build.py canonicalises on - so 'Enemies To Lovers' correctly resolved to our
'enemies to lovers'. But an exact-slug test cannot see a near miss, and My Drama
uses three spellings that differ from ours by a hyphen or an S:

    romcom          8   ->  rom-com           3    identical once hyphens collapse
    sport romance   9   ->  sports-romance   10    singular/plural
    vampires        7   ->  vampire         642    singular/plural

THE VAMPIRE ONE IS THE REASON THIS IS URGENT. 642 titles sit on 'vampire'. A
separate 'vampires' page would have taken 7 of them and looked like a real trope
page, while /tropes/vampire.html carried on showing the other 642 - two pages
competing for one concept, each incomplete, and nothing on the site saying so.
That is EXACTLY the failure build.py's canonicalisation was written to fix, where
"CEO"/"ceo" hid 1,945 titles across 40 pages. That fix folds CASE and SPACING onto
one slug; it cannot fold two genuinely different slugs, so it could not catch this.

TARGETS ARE THE SPELLING WE ALREADY USE MOST, matching build.py's rule that the
most-frequent spelling wins its slug. sports-romance is stored both ways already
('sports romance' 4, 'sports-romance' 6) so the hyphenated one wins on frequency.

DO NOT GENERALISE THIS INTO AUTOMATIC PLURAL FOLDING. 'mate' and 'mates' are
different in this genre, as are 'werewolf' and 'werewolves' arguably. These three
were checked individually against their counts. A near-slug match is a PROMPT to
look, not a licence to merge - the same reason fuzzy title matches go to
match_queue rather than being auto-merged.

Usage:
    py merge_split_tropes.py [--dry-run]
"""
import csv, io, os, re, sys, collections

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "data")
DRY = "--dry-run" in sys.argv

MERGE = {
    "romcom": "rom-com",
    "sport romance": "sports-romance",
    "vampires": "vampire",
}


def term_of(p):
    raw = open(p, "rb").read()
    c = raw.count(b"\r\n")
    return "\r\n" if c > raw.count(b"\n") - c else "\n"


def main():
    p = os.path.join(DATA, "titles.csv")
    titles = list(csv.DictReader(open(p, newline="", encoding="utf-8")))
    fields = list(titles[0].keys())

    n_titles = 0
    moved = collections.Counter()
    for t in titles:
        vals = [x.strip() for x in (t.get("tropes") or "").split(";") if x.strip()]
        if not vals:
            continue
        out, seen, hit = [], set(), False
        for v in vals:
            tgt = MERGE.get(v.lower(), v)
            if tgt != v:
                hit = True
                moved[v] += 1
            k = tgt.lower()
            if k not in seen:            # merging can create a duplicate in-row
                seen.add(k)
                out.append(tgt)
        if hit:
            n_titles += 1
            t["tropes"] = ";".join(out)

    print("titles touched:", n_titles)
    for k, v in moved.most_common():
        print("   %-16s -> %-16s on %d titles" % (k, MERGE[k.lower()], v))

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
