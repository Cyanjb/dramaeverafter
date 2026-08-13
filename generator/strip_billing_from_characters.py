#!/usr/bin/env python3
"""Remove the IMDb billing suffix from character_name on credits already written.

IMDb appends the BILLING VARIANT to a character when the actor was credited under
another name: "Kane Hudson (as Jesse Morales)". parse_imdb_person_pdf.py kept the
whole string on its first run, so eight credits went live with the suffix showing on
the actor page. The parser now splits it into a separate billed_as field; this
repairs the rows that were written before that.

The suffix is NOT thrown away without a thought - it is real aka evidence. In this
case it needs no action: every affected row bills Jesse as "Jesse Morales", which is
already the name we store, and that is itself further corroboration of the merge
ruled today (our page name matches how IMDb bills him on these eight titles, while
his IMDb profile name is "Jesse A. Morales").

Usage:
    py strip_billing_from_characters.py [--dry-run]
"""
import csv, io, os, re, sys, collections

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "data")
DRY = "--dry-run" in sys.argv
AS_RE = re.compile(r"\s*\(as ([^)]+)\)\s*$")


def term_of(p):
    raw = open(p, "rb").read()
    c = raw.count(b"\r\n")
    return "\r\n" if c > raw.count(b"\n") - c else "\n"


def main():
    p = os.path.join(DATA, "credits.csv")
    rows = list(csv.DictReader(open(p, newline="", encoding="utf-8")))
    fields = list(rows[0].keys())

    n = 0
    variants = collections.Counter()
    for r in rows:
        ch = r.get("character_name") or ""
        m = AS_RE.search(ch)
        if not m:
            continue
        variants[m.group(1).strip()] += 1
        r["character_name"] = ch[:m.start()].strip()
        n += 1
        print("   %-42s %-20s %r -> %r"
              % (r["title_id"][:41], r["person_id"], ch, r["character_name"]))

    print()
    print("credits repaired:", n)
    print("billing variants seen:", dict(variants))
    for v in variants:
        print("   NOTE: '%s' - check it against the stored name before treating it "
              "as a new aka" % v)
    if DRY:
        print("[dry-run] nothing written")
        return 0
    if n:
        buf = io.StringIO()
        w = csv.DictWriter(buf, fieldnames=fields, lineterminator=term_of(p))
        w.writeheader()
        w.writerows(rows)
        open(p, "w", newline="", encoding="utf-8").write(buf.getvalue())
        print("written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
