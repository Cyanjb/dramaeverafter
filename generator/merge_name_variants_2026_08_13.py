#!/usr/bin/env python3
"""Merge two IMDb name variants into the people we already hold, on Cyan's ruling
of 13 Aug - and record WHY each one is evidence rather than a hunch.

Both were queued rather than applied because NEVER AUTO-MERGE has no exception for
a strong resemblance. Cyan asked the right question - "doesn't IMDb tell you?" - and
it does, by two different routes:

  JESSE. people.csv already held nm5960414 in jesse-morales' socials, from the
  14 July ReelShort tag scrape. The saved PDF is nm5960414. THE SAME IMDb ID IS
  THE SAME PERSON; nothing further is needed and no judgement is involved.

  ROBERT. No nm id was on file, so the id route was unavailable. Cyan's second
  suggestion carried it instead - the same series listed under two names on two
  sites. Our robert-watkins has exactly ONE credit, on 'Meet My Brothers', whose
  alt_titles field literally reads "After Divorce I'm Spoiled by Three Brothers".
  Robert Palmer Watkins' IMDb page credits "After Divorce, I'm Spoiled by Three
  Brothers" as Dominic Lane (2026). match_queue already ruled those two titles
  confirmed_same. So both records are the same man on the same production, reached
  from two sources: ReelShort's official cast billed him "Robert Watkins", IMDb
  bills him "Robert Palmer Watkins".

DIRECTION OF THE MERGE: into the EXISTING person_id, never the new one. Those slugs
are published URLs - /actors/jesse-morales.html and /actors/robert-watkins.html are
live - and the traps list already records twelve people kept on their old slug for
exactly this reason. The IMDb spelling is preserved in aka_names instead.

The variant goes to aka_names and the nm id to socials where it was missing, per the
standing rule to record the id even when an answer was no.

Usage:
    py merge_name_variants_2026_08_13.py [--dry-run]
"""
import csv, io, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "data")
STAGE = os.path.join(HERE, "staging", "drive_2026-08-09")
DRY = "--dry-run" in sys.argv

MERGES = [
    {"staged": "jesse-a-morales", "into": "jesse-morales",
     "aka": "Jesse A. Morales", "nm": "nm5960414",
     "why": "IDENTICAL IMDb id. people.csv already held nm5960414 for jesse-morales "
            "and the saved PDF is nm5960414."},
    {"staged": "robert-palmer-watkins", "into": "robert-watkins",
     "aka": "Robert Palmer Watkins", "nm": "nm4981388",
     "why": "Same production under two title names. robert-watkins' only credit is "
            "'Meet My Brothers', alt_titles \"After Divorce I'm Spoiled by Three "
            "Brothers\"; the IMDb page credits \"After Divorce, I'm Spoiled by Three "
            "Brothers\" as Dominic Lane. Those titles are already ruled confirmed_same."},
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
    by_id = {p["person_id"]: p for p in people}
    mq, mf = load("match_queue.csv"), fields_of("match_queue.csv")

    for m in MERGES:
        tgt = by_id.get(m["into"])
        if not tgt:
            print("  !! target missing:", m["into"])
            continue

        # aka_names: append, never overwrite. NOTE the separator is inconsistent
        # across this column (37 single, 5 pipe, 2 semicolon); pipe is the majority
        # of the multi-value rows, so use it and do not rewrite the others.
        aka = [x.strip() for x in (tgt.get("aka_names") or "").split("|") if x.strip()]
        if m["aka"] not in aka:
            aka.append(m["aka"])
            tgt["aka_names"] = "|".join(aka)

        if m["nm"] and "imdb.com/name/" not in (tgt.get("socials") or ""):
            url = "https://www.imdb.com/name/%s/" % m["nm"]
            tgt["socials"] = "; ".join([x for x in [tgt.get("socials", "").strip(), url] if x])

        # Point the staged filmography at the person we are keeping, so the audited
        # applier attaches the credits with no new code path.
        p = os.path.join(STAGE, "actor__%s.json" % m["staged"])
        d = json.load(open(p, encoding="utf-8"))
        d["person_id"] = m["into"]
        d["MERGED_BY_RULING"] = ("Cyan, 13 Aug: merged into %s. %s" % (m["into"], m["why"]))
        if not DRY:
            json.dump(d, open(p, "w", encoding="utf-8"), indent=1, ensure_ascii=False)

        for r in mq:
            if m["staged"] in r["candidate_a"] and r["status"] == "pending":
                r["status"] = "confirmed_same (Cyan, 2026-08-13)"

        print("  %-24s -> %-18s aka=%r  credits on the page=%d"
              % (m["staged"], m["into"], tgt["aka_names"], len(d["credits"])))

    if DRY:
        print("\n[dry-run] nothing written")
        return 0
    save("people.csv", pf, people)
    save("match_queue.csv", mf, mq)
    print("\nwritten")
    return 0


if __name__ == "__main__":
    sys.exit(main())
