"""Create the title rows queued by build_filmography_import_2026_08_13.py.

WHY THIS SCRIPT CREATES TITLES WHEN NOTHING ELSE IS ALLOWED TO. apply_imdb_filmography.py
refuses to create a title on purpose: IMDb never says which app a title streams on, and
platform is the one field that cannot be guessed. That objection does not apply here,
because the queue builder already paired every row with a PARSED IMDb COMPANY CATALOGUE,
which is where the platform comes from. The rule is unchanged - no title is created
without platform evidence - so this script simply carries the evidence the other one
lacked. Anything the builder could not place stays out, all 316 of them.

WHAT IT DELIBERATELY DOES NOT WRITE. No synopsis_short and no poster_ref. Both come from
the platform, neither is on an IMDb page, and the standing caption rule forbids inventing
or rewording either. A blank field is honest; a fabricated one is not. These land as
entries that can say WHO is in it and WHICH APP it is on, and cannot show art or plot.
They are deliberately incomplete under the 8 Aug quality bar and completeness.py will
score them as such.

CREDITS ARE NOT WRITTEN HERE EITHER. Once the title rows exist, re-running
apply_imdb_filmography.py over the same staged batch attaches them through the audited
matcher - the same near-match queueing, the same fill-blank-only character names. Doing
it that way rather than writing credits directly means this script adds no new way to
get a credit wrong.

Usage:
    DEA_DATA=../data py apply_filmography_import.py [--dry-run]
"""
import csv, io, os, re, sys, json, time

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.environ.get("DEA_DATA") or os.path.join(HERE, "..", "data")
QUEUE = os.path.join(HERE, "staging", "filmography_import_2026-08-13.json")
SOURCE = "imdb_filmography_import_" + time.strftime("%Y-%m-%d")
TODAY = time.strftime("%Y-%m-%d")
DRY = "--dry-run" in sys.argv


def loose(s):
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def bare(s):
    # Article stripped BEFORE spaces collapse - see apply_imdb_filmography.py.
    return loose(re.sub(r"^(the|a|an)\s+", "", (s or "").strip().lower()))


def term_of(p):
    """Line endings differ per file here (people.csv is CRLF, CONVENTIONS.md says LF
    and is wrong), so match whatever the file already uses instead of normalising it
    and producing a diff of every single row."""
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
    q = json.load(open(QUEUE, encoding="utf-8"))
    ready = q["ready"]

    titles, avail = load("titles.csv"), load("availability.csv")
    t_fields, a_fields = fields_of("titles.csv"), fields_of("availability.csv")

    used_ids = {t["title_id"] for t in titles}
    held_bare = {bare(t["primary_title"]) for t in titles}
    for t in titles:
        for a in (t.get("alt_titles") or "").split("|"):
            if a.strip():
                held_bare.add(bare(a))
    held_tt = {t["imdb_id"] for t in titles if t.get("imdb_id")}
    have_pair = {(a["title_id"], a["platform_id"]) for a in avail}

    new_t, new_a, skipped = [], [], []
    for c in ready:
        tid = c["title_id"]
        # Re-check at APPLY time. The queue was built against an earlier titles.csv and
        # 98 credits have landed since, so a row that was missing then may exist now.
        if tid in used_ids:
            skipped.append((tid, "title_id already exists")); continue
        if bare(c["primary_title"]) in held_bare:
            skipped.append((tid, "bare title already held under another id")); continue
        if c.get("imdb_id") and c["imdb_id"] in held_tt:
            skipped.append((tid, "imdb_id already held: " + c["imdb_id"])); continue

        row = {k: "" for k in t_fields}
        row.update({
            "title_id": tid,
            "slug": c["slug"],
            "primary_title": c["primary_title"],
            "year": c.get("year") or "",
            "origin": "english",
            "source": SOURCE,
            "last_verified": TODAY,
            # needs_check, not verified: the platform came from a company catalogue,
            # not from the platform's own listing, and nothing has been seen on-site.
            "data_confidence": "needs_check",
            "imdb_id": c.get("imdb_id") or "",
        })
        new_t.append(row)
        used_ids.add(tid)
        held_bare.add(bare(c["primary_title"]))
        if c.get("imdb_id"):
            held_tt.add(c["imdb_id"])

        pair = (tid, c["platform_id"])
        if pair not in have_pair:
            arow = {k: "" for k in a_fields}
            arow.update({
                "title_id": tid,
                "platform_id": c["platform_id"],
                "title_as_listed_on_platform": c["primary_title"],
                "last_checked": TODAY,
            })
            new_a.append(arow)
            have_pair.add(pair)

    print(f"queue READY        : {len(ready)}")
    print(f"titles to create   : {len(new_t)}")
    print(f"availability rows  : {len(new_a)}")
    print(f"skipped            : {len(skipped)}")
    for tid, why in skipped:
        print(f"    - {tid}: {why}")

    by_p = {}
    for a in new_a:
        by_p[a["platform_id"]] = by_p.get(a["platform_id"], 0) + 1
    print("by platform        :", by_p)

    if DRY:
        print("\n[dry-run] nothing written")
        return

    save("titles.csv", t_fields, titles + new_t)
    save("availability.csv", a_fields, avail + new_a)
    print("\nwritten")


if __name__ == "__main__":
    main()
