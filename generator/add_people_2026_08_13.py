#!/usr/bin/env python3
"""Create the three genuinely-new actors from the 13 Aug filmography parse, and
queue the two that collide with someone we already hold.

apply_imdb_filmography.py never creates a person - it attaches credits to people
that exist - so five parsed filmographies were being skipped entirely. Two of the
five are not new at all:

  Jesse A. Morales        vs existing jesse-morales      (23 credits, ratio 0.96)
  Robert Palmer Watkins   vs existing robert-watkins     (1 credit,   ratio 0.81)

BOTH ARE THE DOCUMENTED MIDDLE-NAME PATTERN - the traps list already records that
middle names defeat similarity matching (Megan Suzanne Beattie vs Megan Beattie)
and that the matcher therefore also compares first-plus-last word. Here first+last
is identical in both pairs.

THE JESSE EVIDENCE IS ABOUT AS STRONG AS IT GETS SHORT OF A RULING: 22 of the 23
credits on the saved page are titles we already hold, and our jesse-morales carries
exactly 23 credits. It is still queued rather than merged, because NEVER AUTO-MERGE
has no popularity exception and a wrong merge fuses two real people - the same
damage as the 14 full-width-comma rows already waiting for Cyan.

THE THREE THAT ARE CREATED each match at least one title we hold, so none of them
renders an actor page reading "0 titles" - the dead end that kept the zero-credit
fan-panel actors out of the Popular Actors rail:

  david-lovio            16 credits,  2 match
  marie-bach-hansen       2 credits,  1 match  (My Husband's Secret Crush)
  david-edwin-williams    1 credit,   1 match  (Fever Cage)

Both of those matched titles are themselves in the five unread title-page PDFs, so
the cast side will corroborate them.

Usage:
    py add_people_2026_08_13.py [--dry-run]
"""
import csv, io, os, sys, json, time

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "data")
STAGE = os.path.join(HERE, "staging", "drive_2026-08-09")
DRY = "--dry-run" in sys.argv
SOURCE = "imdb_filmography_" + time.strftime("%Y-%m-%d")

CREATE = ["david-lovio", "marie-bach-hansen", "david-edwin-williams"]

QUEUE = [
    ("jesse-a-morales (saved IMDb page, 23 credits)",
     "jesse-morales (existing person, 23 credits)",
     "Middle-initial variant; first+last word identical. 22 of the 23 credits on the "
     "saved page are titles we already hold, and jesse-morales carries exactly 23 "
     "credits. Almost certainly ONE person, but merging is one-way and NEVER "
     "AUTO-MERGE has no exception for a strong hunch. Same person?"),
    ("robert-palmer-watkins (saved IMDb page, 22 credits)",
     "robert-watkins (existing person, 1 credit)",
     "Middle-name variant; first+last word identical. 13 of the 22 credits are titles "
     "we hold. The existing robert-watkins has a single credit, so if they are the "
     "same person almost his whole filmography is currently missing. Same person?"),
]


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
    people, pf = load("people.csv"), fields_of("people.csv")
    have = {p["person_id"] for p in people}
    new = []
    for pid in CREATE:
        if pid in have:
            print("  skip, exists:", pid)
            continue
        d = json.load(open(os.path.join(STAGE, "actor__%s.json" % pid), encoding="utf-8"))
        row = {k: "" for k in pf}
        row.update({
            "person_id": pid, "slug": pid, "name": d["name"], "role_type": "actor",
            # The standing rule is to record the nm id even when an answer was no.
            "socials": "https://www.imdb.com/name/%s/" % d["nm"] if d.get("nm") else "",
            "data_confidence": "needs_check", "source": SOURCE,
        })
        new.append(row)
        print("  + %-24s %-22s nm=%s" % (pid, d["name"], d.get("nm") or "?"))

    mq, mf = load("match_queue.csv"), fields_of("match_queue.csv")
    existing = {(r["candidate_a"], r["candidate_b"]) for r in mq}
    added_q = 0
    for a, b, why in QUEUE:
        if (a, b) in existing:
            print("  already queued:", a[:40])
            continue
        mq.append({"candidate_a": a, "candidate_b": b, "evidence": why, "status": "pending"})
        added_q += 1
        print("  ? queued:", a[:44])

    print()
    print("people to create :", len(new))
    print("rulings queued   :", added_q)
    if DRY:
        print("[dry-run] nothing written")
        return 0
    if new:
        save("people.csv", pf, people + new)
    if added_q:
        save("match_queue.csv", mf, mq)
    print("written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
