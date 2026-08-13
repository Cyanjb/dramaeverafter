#!/usr/bin/env python3
"""Create title rows for staged title__*.json files that name a PLATFORM and that
we do not already hold.

Generalises apply_stranded_titles.py, which did the same job for a hand-listed
three. The gate is unchanged and is the only one that matters: a title is created
only when the saved IMDb page names a platform in its production-company field.
Without that the row can never say where to watch, and platform is the one
attribute that cannot be inferred - which is why apply_imdb_filmography.py refuses
to create titles at all.

A staged file with "platform": null is SKIPPED and reported, never guessed. On the
13 Aug batch that is 'I Became Mrs Grayson by Bragging', whose production companies
are NVert Productions, Narval Films and YRBW Productions - three production houses
and no app. That title needs another source, not a guess.

No synopsis and no poster are written: neither is on an IMDb page, and the caption
rule forbids inventing either.

Usage:
    py create_titles_from_staged.py [--dry-run]
"""
import csv, io, os, re, sys, glob, json, time

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "data")
STAGE = os.path.join(HERE, "staging", "drive_2026-08-09")
DRY = "--dry-run" in sys.argv
TODAY = time.strftime("%Y-%m-%d")
SOURCE = "imdb_title_pdf_" + TODAY


def bare(s):
    s = re.sub(r"^(the|a|an)\s+", "", (s or "").strip().lower())
    return re.sub(r"[^a-z0-9]", "", s)


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", (s or "").lower()).strip("-")


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
    held = {bare(t["primary_title"]) for t in titles}
    for t in titles:
        for a in (t.get("alt_titles") or "").split("|"):
            if a.strip():
                held.add(bare(a))
    ids = {t["title_id"] for t in titles}
    pairs = {(a["title_id"], a["platform_id"]) for a in avail}

    new_t, new_a, skipped = [], [], []
    for p in sorted(glob.glob(os.path.join(STAGE, "title__*.json"))):
        if "DO_NOT_APPLY" in os.path.basename(p):
            continue
        d = json.load(open(p, encoding="utf-8"))
        name = d.get("title")
        plat = d.get("platform")
        if not name or bare(name) in held:
            continue
        if not plat:
            skipped.append((name, "no platform in the production-company field: %s"
                            % d.get("production_companies", "?")))
            continue
        tid = slugify(name)
        if tid in ids:
            skipped.append((name, "slug collision: %s" % tid))
            continue
        row = {k: "" for k in tf}
        row.update({"title_id": tid, "slug": tid, "primary_title": name,
                    "year": d.get("year") or "", "imdb_id": d.get("imdb_id") or "",
                    "origin": "english", "source": SOURCE, "last_verified": TODAY,
                    "data_confidence": "needs_check"})
        new_t.append(row)
        ids.add(tid)
        held.add(bare(name))
        if (tid, plat) not in pairs:
            a = {k: "" for k in af}
            a.update({"title_id": tid, "platform_id": plat,
                      "title_as_listed_on_platform": name, "last_checked": TODAY})
            new_a.append(a)
            pairs.add((tid, plat))
        print("  + %-44s %s" % (tid[:43], plat))

    print()
    print("titles to create :", len(new_t))
    print("availability rows:", len(new_a))
    print("skipped          :", len(skipped))
    for n, why in skipped:
        print("    - %-44s %s" % (n[:43], why))
    if DRY:
        print("\n[dry-run] nothing written")
        return 0
    if new_t:
        save("titles.csv", tf, titles + new_t)
        save("availability.csv", af, avail + new_a)
        print("\nwritten")
    return 0


if __name__ == "__main__":
    sys.exit(main())
