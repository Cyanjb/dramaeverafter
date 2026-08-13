#!/usr/bin/env python3
"""Create the three titles whose IMDb page was read but whose row was never made,
and add one availability row that a previous pass claimed to add and did not.

WHY THESE THREE ARE SAFE TO CREATE. Each has a saved IMDb page naming its PLATFORM
in the production-company field, which is the one attribute that cannot be inferred
and the only reason apply_imdb_filmography.py refuses to create titles at all. Each
also has its cast already transcribed and waiting in _cast_batch.json, which has
been reporting them as UNRESOLVED on every run because the title row is missing.

  Forgive Me Father                 tt39392648  shortical  co1167893
  The Billion Dollar Baby           tt36242374  shortmax   co1065580 + filename
  You've Been Replaced, First Love  -           reelshort  filename AND page 7

The third is the strongest evidence in the whole batch: the FILENAME says ReelShort
(sec 23 makes that authoritative) and the PDF's own Details block independently says
"Production companies: Swzz Media Productions, ReelShort". Two sources agreeing.

SLUGS ARE PICKED, NOT ASKED. Cyan's standing instruction is not to bring her routine
decisions like slugs, so these take the obvious form and are recorded here instead:
forgive-me-father, the-billion-dollar-baby, you-ve-been-replaced-first-love.

FOURTH FIX, A REAL MISS. 'Torn Between My Stepbrothers' HAS a title row and its
staged JSON says dramabox, but its availability is EMPTY - the commit that
transcribed it says "it gains a platform" and it never did. Adding that row is what
the earlier pass intended.

NOT TOUCHED, DELIBERATELY: 'The Billionaire's Masquerade'. Its PDF says candyjar
while we hold it as reelshort. Sec 7 warns that a Galatea/CandyJar original sharing
a name with another platform's title is usually a DIFFERENT PRODUCTION, so adding
candyjar could merge two shows into one row. That goes to match_queue for a ruling,
which is what the never-auto-merge rule is for.

NO SYNOPSIS AND NO POSTER, per the caption rule - neither is on an IMDb page.

Usage:
    py apply_stranded_titles.py [--dry-run]
"""
import csv, io, os, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "data")
DRY = "--dry-run" in sys.argv
TODAY = time.strftime("%Y-%m-%d")
SOURCE = "imdb_pdf_stranded_" + TODAY


def demojibake(s):
    """'Le BÃ©bÃ©' is UTF-8 bytes read as latin-1. Repair, or leave alone if it is
    not that pattern - a blind round-trip would corrupt legitimate text."""
    try:
        fixed = s.encode("latin-1").decode("utf-8")
        return fixed if "Ã" in s or "Â" in s else s
    except (UnicodeEncodeError, UnicodeDecodeError):
        return s


NEW = [
    {"title_id": "forgive-me-father", "primary_title": "Forgive Me Father",
     "year": "2026", "imdb_id": "tt39392648", "platform": "shortical", "alt": ""},
    {"title_id": "the-billion-dollar-baby", "primary_title": "The Billion Dollar Baby",
     "year": "2025", "imdb_id": "tt36242374", "platform": "shortmax",
     "alt": demojibake("Le BÃ©bÃ© Ã  Milliard de Dollars")},
    {"title_id": "you-ve-been-replaced-first-love",
     "primary_title": "You've Been Replaced, First Love",
     "year": "2026", "imdb_id": "", "platform": "reelshort",
     "alt": "Has sido reemplazado, primer amor"},
]
AVAIL_ONLY = [("torn-between-my-stepbrothers", "dramabox")]


def term_of(p):
    raw = open(p, "rb").read()
    c = raw.count(b"\r\n")
    return "\r\n" if c > raw.count(b"\n") - c else "\n"


def load(n):
    return list(csv.DictReader(open(os.path.join(DATA, n), newline="", encoding="utf-8")))


def fields_of(n):
    with open(os.path.join(DATA, n), newline="", encoding="utf-8") as f:
        return next(csv.reader(f))


def save(n, fields, recs):
    p = os.path.join(DATA, n)
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=fields, lineterminator=term_of(p))
    w.writeheader()
    w.writerows(recs)
    open(p, "w", newline="", encoding="utf-8").write(buf.getvalue())


def main():
    titles, avail = load("titles.csv"), load("availability.csv")
    tf, af = fields_of("titles.csv"), fields_of("availability.csv")
    have_t = {t["title_id"] for t in titles}
    have_pair = {(a["title_id"], a["platform_id"]) for a in avail}

    new_t, new_a = [], []
    for n in NEW:
        if n["title_id"] in have_t:
            print("  skip, already exists:", n["title_id"])
            continue
        row = {k: "" for k in tf}
        row.update({"title_id": n["title_id"], "slug": n["title_id"],
                    "primary_title": n["primary_title"], "alt_titles": n["alt"],
                    "year": n["year"], "imdb_id": n["imdb_id"], "origin": "english",
                    "source": SOURCE, "last_verified": TODAY,
                    "data_confidence": "needs_check"})
        new_t.append(row)
        if (n["title_id"], n["platform"]) not in have_pair:
            a = {k: "" for k in af}
            a.update({"title_id": n["title_id"], "platform_id": n["platform"],
                      "title_as_listed_on_platform": n["primary_title"],
                      "last_checked": TODAY})
            new_a.append(a)

    for tid, plat in AVAIL_ONLY:
        if tid not in have_t:
            print("  skip avail, no title row:", tid)
            continue
        if (tid, plat) in have_pair:
            print("  skip avail, already present:", tid, plat)
            continue
        a = {k: "" for k in af}
        a.update({"title_id": tid, "platform_id": plat,
                  "title_as_listed_on_platform": tid.replace("-", " ").title(),
                  "last_checked": TODAY})
        new_a.append(a)

    print("titles to create   :", len(new_t))
    for r in new_t:
        print("   +", r["title_id"], "|", r["primary_title"])
    print("availability rows  :", len(new_a))
    for r in new_a:
        print("   +", r["title_id"], "->", r["platform_id"])

    if DRY:
        print("\n[dry-run] nothing written")
        return 0
    save("titles.csv", tf, titles + new_t)
    save("availability.csv", af, avail + new_a)
    print("\nwritten")
    return 0


if __name__ == "__main__":
    sys.exit(main())
