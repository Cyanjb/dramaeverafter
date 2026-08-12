"""Convert the staged IMDb TITLE-page files into the {primary_title: [[actor, character]]}
shape that apply_imdb_pdf_cast.py --json consumes.

Four things this has to get right, each of which would corrupt data if skipped:

MOJIBAKE. Three transcribed names are UTF-8 read as latin-1 ('CÃ©line Planata',
'Arne KÃ¼bler', 'SÃ©lynne Silver'). people.csv currently has ZERO corrupted names,
so applying these as-is would be the first - and under a real person's name. The
repair is a deterministic re-decode, not a guess.

THE ACCENT COLLISION. Once repaired, 'Céline Planata' no longer exact-matches the
'Celine Planata' already in people.csv, and loose() strips the accented letter
rather than folding it, so she would arrive as a second person or a spurious queue
row. Where a name folds onto an existing person, the STORED spelling is emitted so
the applier matches exactly. The discrepancy is reported for a human ruling.

apply_cast_to. Two files name a different target than their own title, because the
IMDb page displays 'The Billionaire's Masquerade' (ReelShort) while being the
CandyJar production we hold as 'billionaire-s-masquerade'. Title-string matching
would put 7 people on the wrong show.

PER-ENTRY DO_NOT_APPLY. Individual cast rows carry their own skip flag, separate
from the two whole-file DO_NOT_APPLY PDFs (which this script never opens).

Titles are emitted under their titles.csv primary_title, since the applier keys on
that exactly and case-SENSITIVELY.
"""
import json, glob, os, csv, re, sys, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.abspath(os.path.join(HERE, "..", "..", "..", "data"))
OUT = os.path.join(HERE, "_cast_batch.json")


def demojibake(s):
    if not re.search(r"Ã|Â", s):
        return s
    try:
        return s.encode("latin-1").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return s


def fold(s):
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]", "", s.lower())


def bare(s):
    # Strip the article BEFORE collapsing, per the traps list: doing it after turns
    # "Alpha's Doe" into "lphasdoe" because the 'a' of "alphas" reads as the article.
    # IMDb drops articles the platforms keep - it lists "Alpha's Doe" for the title we
    # hold as "The Alpha's Doe".
    return fold(re.sub(r"^(the|a|an)\s+", "", (s or "").strip().lower()))


def rows(n):
    return list(csv.DictReader(open(os.path.join(DATA, n), newline="", encoding="utf-8")))


def main():
    titles = rows("titles.csv")
    people = rows("people.csv")
    by_exact_title = {t["primary_title"]: t for t in titles}
    by_id = {t["title_id"]: t for t in titles}
    by_fold_title, by_bare_title = {}, {}
    for t in titles:
        by_fold_title.setdefault(fold(t["primary_title"]), t)
        by_bare_title.setdefault(bare(t["primary_title"]), t)
        for a in (t.get("alt_titles") or "").split("|"):
            if a.strip():
                by_fold_title.setdefault(fold(a), t)
                by_bare_title.setdefault(bare(a), t)
    ppl_exact = {p["name"].strip().lower(): p for p in people}
    ppl_fold = {}
    for p in people:
        ppl_fold.setdefault(fold(p["name"]), p)

    batch, notes, unresolved = {}, [], []
    repaired = spelling = skipped_entries = 0

    files = [p for p in sorted(glob.glob(os.path.join(HERE, "*title*.json")))
             if "DO_NOT_APPLY" not in os.path.basename(p)]

    for path in files:
        d = json.load(open(path, encoding="utf-8"))
        base = os.path.basename(path)

        # apply_cast_to overrides the page's own title - it is the whole point of the field
        target = d.get("apply_cast_to")
        if target:
            t = by_id.get(target) or by_exact_title.get(target)
            if not t:
                unresolved.append(f"{base}: apply_cast_to='{target}' not found")
                continue
            notes.append(f"  -> {base}: apply_cast_to sends this to '{t['primary_title']}'")
        else:
            t = (by_exact_title.get(d["title"]) or by_fold_title.get(fold(d["title"]))
                 or by_bare_title.get(bare(d["title"])))
            if not t:
                unresolved.append(f"{base}: '{d['title']}' not in titles.csv")
                continue
            if t["primary_title"] != d["title"]:
                notes.append(f"  ~ {base}: IMDb '{d['title']}' -> ours '{t['primary_title']}'")

        cast = []
        for c in d["cast"]:
            if c.get("DO_NOT_APPLY"):
                skipped_entries += 1
                notes.append(f"  x {base}: cast entry skipped, DO_NOT_APPLY: {c.get('name')}")
                continue
            name = c["name"]
            fixed = demojibake(name)
            if fixed != name:
                repaired += 1
                notes.append(f"  # mojibake repaired: {name!r} -> {fixed!r}")
            # Prefer the spelling already in people.csv so the applier matches exactly
            if fixed.strip().lower() not in ppl_exact:
                m = ppl_fold.get(fold(fixed))
                if m and m["name"] != fixed:
                    notes.append(f"  ! spelling differs: IMDb {fixed!r} vs db {m['name']!r} "
                                 f"({m['person_id']}) - using the stored one, NOT renaming")
                    fixed = m["name"]
                    spelling += 1
            cast.append([fixed, demojibake(c.get("character") or "")])

        if not cast:
            continue
        # Two files can target one title; merge rather than clobber
        batch.setdefault(t["primary_title"], [])
        have = {a for a, _ in batch[t["primary_title"]]}
        batch[t["primary_title"]] += [x for x in cast if x[0] not in have]

    json.dump(batch, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"wrote {OUT}")
    print(f"  {len(batch)} titles, {sum(len(v) for v in batch.values())} cast entries")
    print(f"  mojibake repaired: {repaired} | spelling deferred to db: {spelling} "
          f"| cast entries skipped: {skipped_entries}")
    if unresolved:
        print(f"UNRESOLVED TITLES ({len(unresolved)}) - no cast emitted for these:")
        for x in unresolved:
            print("   ", x)
    if notes:
        print("NOTES:")
        for x in notes:
            print(x)


if __name__ == "__main__":
    main()
