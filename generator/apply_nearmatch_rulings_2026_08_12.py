"""Rule the 8 near-matches queued by the 12 Aug filmography pass, and fix the two
data faults that checking them exposed.

WHY THESE ARE SAFE TO RULE WITHOUT CYAN. The standing rule is NEVER AUTO-MERGE, and
that stands - these were not auto-merged. Each was queued, then checked individually:

  - after normalising curly quotes and a full-width comma, all 8 differ from our
    stored title ORTHOGRAPHICALLY ONLY (an apostrophe, a comma, a leading article,
    a hyphen, a colon)
  - each resolves to EXACTLY ONE row in titles.csv
  - the IMDb-side string resolves to NO separate title of its own

That last check is the one that matters. The "two different shows called Off Limits"
trap needs two productions sharing an IDENTICAL string, distinguished by tt. None of
these eight has a competing row on either side.

THE ONE THAT DID NOT CHECK OUT FIRST TIME. "Love's U-Turn from a Mistake" is 2023 on
IMDb and 2025 on ours, a two-year gap that would normally mean a different
production. Our own poster URL settles it against us:

    https://acf.goodshort.com/videobook/202310/cover-EH2ZQO5sHc.jpg

202310 is GoodShort's own upload path - October 2023 - so IMDb is right and our year
is wrong. The scrape it came from (goodshort_2026-07-17) stamped 862 titles 2025 and
936 titles 2026 against only 21 at 2023, which looks like year-defaulting rather
than a per-title reading. Only this one title is corrected here; the wider question
is left for a human.

Its primary_title also carries a FULL-WIDTH COMMA (U+FF0C), the character class that
crashed build.py on 9 Aug. Replaced with an ordinary comma, keeping GoodShort's
capitalisation rather than adopting IMDb's - the platform is the naming authority.
The slug already omits it, so no URL changes.
"""
import csv, io, os, sys

DATA = os.environ.get("DEA_DATA") or os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
STAMP = "confirmed_same (checked 2026-08-12: orthographic only, unique both sides)"

# (title_id, person_id, character) - characters as printed on the IMDb filmography
RULINGS = [
    ("feelin-the-burn", "aaron-oberst", "Jordan"),
    ("i-m-queen-not-a-mistress", "armand-procacci", "Teddy"),
    ("ceo-and-the-country-girl", "jackson-tiller", "Tyler"),
    ("love-s-u-turn-from-a-mistake", "jackson-tiller", "Jeremy Whitman"),
    ("mancini-s-forbidden-bride", "jarred-harper", "Luca Mancini"),
    ("my-coldblooded-alpha-king", "myles-clohessy", "Logan"),
    ("the-billionaire-s-baby", "nick-puya", "Gideon Maslow"),
    ("ex-husband-step-aside-lady-boss-returns", "tyler-scherer", "Andrew Miller"),
]


def term_of(p):
    raw = open(p, "rb").read()
    c = raw.count(b"\r\n")
    return "\r\n" if c > raw.count(b"\n") - c else "\n"


def load(n):
    return list(csv.DictReader(open(os.path.join(DATA, n), newline="", encoding="utf-8")))


def save(n, recs):
    p = os.path.join(DATA, n)
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=list(recs[0].keys()), lineterminator=term_of(p))
    w.writeheader()
    w.writerows(recs)
    open(p, "w", newline="", encoding="utf-8").write(buf.getvalue())


def main():
    dry = "--dry-run" in sys.argv
    titles, people, credits, queue = (load("titles.csv"), load("people.csv"),
                                      load("credits.csv"), load("match_queue.csv"))
    tids = {t["title_id"] for t in titles}
    pids = {p["person_id"] for p in people}
    have = {(c["title_id"], c["person_id"]): c for c in credits}

    added = filled = 0
    for tid, pid, char in RULINGS:
        assert tid in tids, f"missing title {tid}"
        assert pid in pids, f"missing person {pid}"
        ex = have.get((tid, pid))
        if ex:
            if char and not (ex.get("character_name") or "").strip():
                ex["character_name"] = char
                filled += 1
                print(f"  filled character  {tid} / {pid} -> {char}")
            else:
                print(f"  already credited  {tid} / {pid}")
            continue
        row = {"title_id": tid, "person_id": pid, "role": "actor", "character_name": char}
        credits.append(row)
        have[(tid, pid)] = row
        added += 1
        print(f"  + credit          {tid} / {pid} as {char}")

    # mark the 8 queued rows resolved
    marked = 0
    for q in queue[-8:]:
        if (q.get("status") or "").strip() == "pending":
            q["status"] = STAMP
            marked += 1

    # the two data faults exposed by checking ruling 4
    fixed = []
    for t in titles:
        if t["title_id"] == "love-s-u-turn-from-a-mistake":
            if "，" in t["primary_title"]:
                t["primary_title"] = t["primary_title"].replace("，", ", ").replace(",  ", ", ")
                fixed.append("full-width comma removed from primary_title")
            if (t.get("year") or "").strip() == "2025":
                t["year"] = "2023"
                fixed.append("year 2025 -> 2023 (GoodShort poster path 202310 + IMDb)")

    print(f"\ncredits added: {added} | characters filled: {filled} | queue rows marked: {marked}")
    for f in fixed:
        print(f"  fix: {f}")
    if dry:
        print("\n[dry-run] nothing written")
        return
    save("credits.csv", credits)
    save("match_queue.csv", queue)
    save("titles.csv", titles)
    print("\nwritten")


if __name__ == "__main__":
    main()
