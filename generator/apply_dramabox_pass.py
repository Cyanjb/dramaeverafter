"""Apply the staged DramaBox pass: tropes onto titles.csv, links onto availability.csv.

WHAT IT DELIBERATELY DOES NOT DO
  - It does NOT create availability rows from a NAME match. A name match to DramaBox's
    catalogue is not evidence the title streams there: this genre re-shoots the same
    script per platform, and match_queue already carries that exact warning. Tropes
    survive that ambiguity (a different shoot of the same story has the same tropes);
    a watch link does not. So links are written ONLY to rows that are already
    platform_id=dramabox.
  - It does NOT touch a title whose bookId is claimed by two of our own rows. Those
    are the PineDrama twins and they need the twin ruling first.
  - It does NOT write the three tags that near-miss our existing vocabulary
    (childhood-sweetheart/-s, contract-lover/-s, athlete/-s). Storing them would
    publish a rival page beside the existing one, and build.py's canonicalisation
    folds case and spacing but CANNOT fold two different slugs.
  - It does NOT take synopses. The catalogue carries `introduction`; the caption rule
    forbids it.

Tropes are appended to the existing ';'-separated list, de-duplicated by SLUG so
'Second Chance' does not land beside an existing 'second chance'.

Usage:
    py generator/apply_dramabox_pass.py [--dry-run]
"""
import csv, io, json, os, re, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.environ.get("DEA_DATA") or os.path.join(HERE, "..", "data")
STAGED = os.path.join(HERE, "staging", "dramabox_pass_" + time.strftime("%Y-%m-%d") + ".json")
DRY = "--dry-run" in sys.argv

# Held back pending Cyan's singular/plural ruling - see docstring.
HOLD_TAGS = {"childhood-sweetheart", "contract-lover", "athlete"}


def slugify(s):
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", (s or "").lower())).strip("-")


def term_of(p):
    raw = open(p, "rb").read()
    crlf = raw.count(b"\r\n")
    return "\r\n" if crlf > raw.count(b"\n") - crlf else "\n"


def load(name):
    p = os.path.join(DATA, name)
    return list(csv.DictReader(open(p, newline="", encoding="utf-8-sig"))), term_of(p)


def save(name, rows, term):
    p = os.path.join(DATA, name)
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=list(rows[0].keys()), lineterminator=term)
    w.writeheader()
    w.writerows(rows)
    open(p, "w", encoding="utf-8", newline="").write(buf.getvalue())


def main():
    d = json.load(open(STAGED, encoding="utf-8"))
    collide = set(d["bookids_claimed_by_two_of_our_titles"])

    titles, t_term = load("titles.csv")
    av, a_term = load("availability.csv")
    by_id = {t["title_id"]: t for t in titles}
    dbx_rows = {r["title_id"]: r for r in av if r["platform_id"] == "dramabox"}

    # ---- tropes ----
    added_tropes, held, skipped_collide = 0, 0, 0
    touched_titles = set()
    for e in d["tropes_for_matched_titles"]:
        if e["book_id"] in collide:
            skipped_collide += 1
            continue
        t = by_id.get(e["title_id"])
        if t is None:
            continue
        have = {slugify(x) for x in (t["tropes"] or "").split(";") if x.strip()}
        cur = [x for x in (t["tropes"] or "").split(";") if x.strip()]
        for tag in e["tropes"]:
            s = slugify(tag)
            if s in HOLD_TAGS:
                held += 1
                continue
            if s in have:
                continue
            cur.append(tag.lower())
            have.add(s)
            added_tropes += 1
            touched_titles.add(t["title_id"])
        t["tropes"] = ";".join(cur)

    # ---- links + episode counts, ONLY on existing dramabox rows ----
    added_links, added_eps = 0, 0
    for e in d["links_for_rows_missing_one"]:
        if e["book_id"] in collide:
            continue
        r = dbx_rows.get(e["title_id"])
        if r is None or r["direct_link"].strip():
            continue
        r["direct_link"] = e["direct_link"]
        r["last_checked"] = time.strftime("%Y-%m-%d")
        added_links += 1
        t = by_id.get(e["title_id"])
        if t is not None and not (t["episode_count"] or "").strip() and e.get("episode_count"):
            t["episode_count"] = str(e["episode_count"])
            added_eps += 1

    print(f"tropes added            : {added_tropes}  across {len(touched_titles)} titles")
    print(f"  held (near-slug)      : {held}")
    print(f"  skipped (twin collide): {skipped_collide}")
    print(f"direct_links written    : {added_links}")
    print(f"episode_counts filled   : {added_eps}")

    if DRY:
        print("\n[dry-run] nothing written")
        return
    save("titles.csv", titles, t_term)
    save("availability.csv", av, a_term)
    print("\nwritten titles.csv, availability.csv")


if __name__ == "__main__":
    main()
