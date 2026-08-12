"""Refresh the derived columns in data/popular_actors.csv.

The file is a CURATED list - which actors the Reddit fan panels named, and which
panel each came from. That part is human judgement and this script never touches it.

But two columns are DERIVED and go stale the moment a credits pass runs: `credits`
and `has_photo`. After the 12 Aug pass, 10 of 38 rows carried a wrong credit count
(Kasey Esser 17 when he actually had 23), and two actors excluded as "0 credits, a
tile reading 0 titles is a dead end" had since gained their first credit.

in_rail is only flipped in the direction the original rule intended: an actor who
now HAS a credit stops being a dead end and joins the rail. Nobody is ever removed
here - that is a curation decision, not a derived one.

Run this after any pass that adds credits or photos.

Usage:  python refresh_popular_actors.py [--dry-run]
"""
import csv, io, os, sys, collections

DATA = os.environ.get("DEA_DATA") or os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")


def term_of(p):
    raw = open(p, "rb").read()
    c = raw.count(b"\r\n")
    return "\r\n" if c > raw.count(b"\n") - c else "\n"


def load(n):
    return list(csv.DictReader(open(os.path.join(DATA, n), newline="", encoding="utf-8")))


def main():
    rows = load("popular_actors.csv")
    credits = collections.Counter(c["person_id"] for c in load("credits.csv"))
    photo = {p["person_id"]: (p.get("photo_ref") or "").strip() for p in load("people.csv")}

    changed_c = changed_p = promoted = 0
    for r in rows:
        now = credits.get(r["person_id"], 0)
        if str(now) != (r.get("credits") or "").strip():
            print(f"  credits  {r['name']:26} {r.get('credits'):>3} -> {now}")
            r["credits"] = str(now)
            changed_c += 1
        hp = "yes" if photo.get(r["person_id"]) else "no"
        if hp != (r.get("has_photo") or "").strip():
            print(f"  photo    {r['name']:26} {r.get('has_photo')} -> {hp}")
            r["has_photo"] = hp
            changed_p += 1
        # Only ever promote: the exclusion rule was about 0-credit dead ends.
        if r.get("in_rail") == "no" and now > 0:
            print(f"  in_rail  {r['name']:26} no -> yes ({now} credit(s), no longer a dead end)")
            r["in_rail"] = "yes"
            promoted += 1

    print(f"\ncredit counts corrected : {changed_c}")
    print(f"photo flags corrected   : {changed_p}")
    print(f"promoted into the rail  : {promoted}")
    print(f"rail size now           : {sum(1 for r in rows if r.get('in_rail') == 'yes')} of {len(rows)}")

    if "--dry-run" in sys.argv:
        print("\n[dry-run] nothing written")
        return
    p = os.path.join(DATA, "popular_actors.csv")
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=list(rows[0].keys()), lineterminator=term_of(p))
    w.writeheader()
    w.writerows(rows)
    open(p, "w", newline="", encoding="utf-8").write(buf.getvalue())
    print("\nwritten")


if __name__ == "__main__":
    main()
