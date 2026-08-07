"""Apply credits from a manually-saved IMDb PERSON page (the reverse direction).

apply_imdb_pdf_cast.py reads a TITLE page: one title, many actors. This reads a
PERSON page: one actor, many titles. Craft doc 7 records that every credit in the
database to date came from the title direction and no filmography had ever been
read, while GoodShort sits at under 1% cast with no bulk route. One actor page can
carry 40+ credits, so this is the cheapest route into that gap.

A person page is also EASIER to parse correctly than a title page. Title pages lay
the cast out as a grid, and PDF text extraction interleaves the actor and character
columns, so the pairing has to be reconstructed. On a person page each credit is a
single row - title, type, character, year - so the actor-to-character pairing is
read directly rather than inferred.

Same safety rules as the rest of the project:
  - never creates a title. IMDb does not say which app a title is on, and platform
    is the one thing we cannot guess, so unmatched titles are only ever REPORTED.
  - near-matches go to match_queue for a human ruling, never auto-merged.
  - character names are fill-blank-only; an existing value is never overwritten.
  - non-vertical work (features, shorts, long-running TV) is filtered out upstream
    when staging, since a filmography mixes it in freely.

Usage:
    DEA_DATA=../data python3 apply_imdb_filmography.py staging/imdb_<date>.json [--dry-run]
"""
import csv, io, os, re, sys, json, time, difflib, argparse

DATA = os.environ.get("DEA_DATA") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
SOURCE = "imdb_filmography_" + time.strftime("%Y-%m-%d")


def loose(s):
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def term_of(p):
    raw = open(p, "rb").read()
    c = raw.count(b"\r\n")
    return "\r\n" if c > raw.count(b"\n") - c else "\n"


def load(n):
    return list(csv.DictReader(open(os.path.join(DATA, n), newline="", encoding="utf-8")))


def save(n, fields, recs):
    p = os.path.join(DATA, n)
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=fields, lineterminator=term_of(p))
    w.writeheader()
    w.writerows(recs)
    open(p, "w", newline="", encoding="utf-8").write(buf.getvalue())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("staging")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    batch = json.load(open(args.staging, encoding="utf-8"))
    titles, people, credits, queue = load("titles.csv"), load("people.csv"), load("credits.csv"), load("match_queue.csv")

    by_exact, by_loose = {}, {}
    for t in titles:
        by_exact[t["primary_title"].strip().lower()] = t
        by_loose.setdefault(loose(t["primary_title"]), t)
        for a in (t["alt_titles"] or "").split("|"):
            if a.strip():
                by_exact.setdefault(a.strip().lower(), t)
                by_loose.setdefault(loose(a), t)
    people_by_id = {p["person_id"]: p for p in people}
    existing = {(c["title_id"], c["person_id"]): c for c in credits}

    added, filled, unmatched, queued, skipped = [], [], [], [], []

    people_touched = 0
    for pid, rec in batch.items():
        person = people_by_id.get(pid)
        if not person:
            print(f"  ! person_id not in people.csv, skipping entirely: {pid}")
            continue
        # An IMDb person page also carries the two fields we are chronically short of.
        # Both fill-blank-only: an "Alternative names" line is IMDb recording a billing
        # variant itself, which is the evidence sec 10 of adapters.md wanted for the
        # Artem Plonder ruling, and socials have no other reliable source.
        for field, key in (("aka_names", "aka"), ("socials", "socials")):
            val = (rec.get(key) or "").strip()
            if val and not (person.get(field) or "").strip():
                person[field] = val
                people_touched += 1
        for title, character, year in rec["credits"]:
            key = title.strip().lower()
            t = by_exact.get(key)
            if not t:
                # Loose match: same letters and digits, different punctuation. Real in
                # this data ("Mr. Diazs Deaf Bride" vs "Mr. Diaz's Deaf Bride"), but it
                # is a judgement call, so it is queued rather than applied.
                lm = by_loose.get(loose(title))
                if lm:
                    queued.append((pid, title, lm["primary_title"], character))
                else:
                    unmatched.append((pid, title, character, year))
                continue
            ck = (t["title_id"], pid)
            if ck in existing:
                cur = existing[ck]
                if character and not (cur["character_name"] or "").strip():
                    cur["character_name"] = character
                    filled.append((t["primary_title"], person["name"], character))
                else:
                    skipped.append((t["primary_title"], person["name"]))
                continue
            row = {"title_id": t["title_id"], "person_id": pid, "role": "actor",
                   "character_name": character or ""}
            credits.append(row)
            existing[ck] = row
            added.append((t["primary_title"], person["name"], character))

    for pid, listed, near, character in queued:
        queue.append({"candidate_a": f"{listed} (IMDb, credited to {pid})",
                      "candidate_b": near,
                      "evidence": f"IMDb filmography {SOURCE}: punctuation-only difference, "
                                  f"character {character or 'n/a'}. Confirm same production.",
                      "status": "pending"})

    print(f"people  {people_touched} aka/socials fields filled")
    print(f"added   {len(added)} credits")
    print(f"filled  {len(filled)} blank character names")
    print(f"skipped {len(skipped)} already complete")
    print(f"queued  {len(queued)} near-matches for a ruling")
    print(f"UNMATCHED (not created - no platform evidence): {len(unmatched)}")
    for pid, title, character, year in unmatched:
        print(f"    {year}  {title}   [{character}]")

    if args.dry_run:
        print("\n[dry-run] nothing written")
        return
    save("credits.csv", ["title_id", "person_id", "role", "character_name"], credits)
    if people_touched:
        save("people.csv", list(people[0].keys()), people)
    if queued:
        save("match_queue.csv", ["candidate_a", "candidate_b", "evidence", "status"], queue)
    print("\nwritten")


if __name__ == "__main__":
    main()
