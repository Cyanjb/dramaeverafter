"""Add an imdb_id column to titles.csv and backfill it.

WHY THIS EXISTS. titles.csv had no IMDb id at all, so every cross-reference against
an IMDb source had to match on the TITLE STRING - the one thing the traps list says
never to match on ("two different shows called 'Off Limits' - match on tt, never on
name"). Without a tt column the 119 platform attributions waiting in the parsed
company catalogues cannot be applied safely, because 6 catalogue names map to more
than one production and 83 of our own titles share a name with another row.

FOUR SOURCES, APPLIED IN DESCENDING CONFIDENCE. A tt is only written into a blank
field, and a later, weaker tier never overwrites an earlier one:

  1 source_urls   58 titles already store an imdb.com/title/ URL. Direct provenance,
                  no matching of any kind. This is the only tier that is beyond doubt.
  2 title pages   the staged IMDb TITLE-page transcriptions, each carrying its own
                  imdb_id. Cyan opened these pages herself, so the page-to-title
                  binding is hers, not a guess. apply_cast_to is honoured.
  3 candyjar      the staged CandyJar company-page reading.
  4 catalogues    the six parsed IMDb company catalogues, matched on an
                  article-stripped name. ONLY where the name is unambiguous on BOTH
                  sides - one catalogue tt for that name, and one titles.csv row for
                  that name. Everything else is reported, never guessed.

A tt LANDING ON TWO OF OUR TITLES IS A FINDING, NOT AN ERROR. It means we hold one
production as two rows. The handover already suspected this of exercise-discretion /
she-s-the-undercover-boss (tt37748257), and the 73 -pinedrama rows are the same shape.
Those collisions are printed and NOT written, because writing them would silently
assert that two rows are one title.

Usage:  DEA_DATA=../data python add_imdb_ids.py [--dry-run]
"""
import csv, glob, io, json, os, re, sys, collections

DATA = os.environ.get("DEA_DATA") or os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
HERE = os.path.dirname(os.path.abspath(__file__))
DRIVE = os.path.join(HERE, "staging", "drive_2026-08-09")
TT = re.compile(r"(tt\d+)")


def fold(s):
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def bare(s):
    # Article stripped BEFORE collapsing, per the traps list.
    return fold(re.sub(r"^(the|a|an)\s+", "", (s or "").strip().lower()))


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
    titles = load("titles.csv")
    fields = list(titles[0].keys())
    added_col = "imdb_id" not in fields
    if added_col:
        fields.append("imdb_id")
    for t in titles:
        t.setdefault("imdb_id", "")

    by_id = {t["title_id"]: t for t in titles}
    # A name is only usable if exactly ONE of our rows carries it.
    name_rows = collections.defaultdict(list)
    for t in titles:
        name_rows[bare(t["primary_title"])].append(t)
        for a in (t.get("alt_titles") or "").split("|"):
            if a.strip():
                name_rows[bare(a)].append(t)
    unique_name = {k: v[0] for k, v in name_rows.items() if len(v) == 1 and k}
    ambiguous_name = {k for k, v in name_rows.items() if len(v) > 1 and k}

    # proposals: title_id -> (tt, tier)
    prop, notes, skipped = {}, [], collections.Counter()

    def offer(t, tt, tier):
        if not t or not tt or not TT.fullmatch(tt):
            return
        cur = (t.get("imdb_id") or "").strip()
        if cur:
            if cur != tt:
                notes.append(f"  CONFLICT {t['title_id']}: holds {cur}, tier{tier} says {tt} - kept {cur}")
            return
        have = prop.get(t["title_id"])
        if have and have[0] != tt:
            notes.append(f"  CONFLICT {t['title_id']}: tier{have[1]} {have[0]} vs tier{tier} {tt} - kept tier{have[1]}")
            return
        if not have:
            prop[t["title_id"]] = (tt, tier)

    # ---- tier 1: an IMDb URL already stored on the row
    for t in titles:
        m = TT.search(t.get("source_urls") or "")
        if m:
            offer(t, m.group(1), 1)

    # ---- tier 2: staged IMDb title-page transcriptions
    for p in sorted(glob.glob(os.path.join(DRIVE, "*title*.json"))):
        if "DO_NOT_APPLY" in os.path.basename(p):
            continue
        d = json.load(open(p, encoding="utf-8"))
        tt = (d.get("imdb_id") or "").strip()
        if not tt:
            continue
        tgt = d.get("apply_cast_to")
        t = by_id.get(tgt) if tgt else None
        if t is None:
            t = unique_name.get(bare(d.get("title") or ""))
        if t is None:
            skipped["tier2 title not resolvable/unique"] += 1
            continue
        offer(t, tt, 2)

    # ---- tier 3: the staged CandyJar company reading
    cj = os.path.join(HERE, "staging", "imdb_candyjar_2026-08-09.json")
    if os.path.exists(cj):
        d = json.load(open(cj, encoding="utf-8"))
        for r in (d.get("titles") or []):
            if not isinstance(r, dict):
                continue
            tt = (r.get("imdb_id") or "").strip()
            nm = r.get("title") or r.get("primary_title") or ""
            if not tt:
                continue
            t = by_id.get(r.get("title_id") or "") or unique_name.get(bare(nm))
            if t is None:
                skipped["tier3 title not resolvable/unique"] += 1
                continue
            offer(t, tt, 3)

    # ---- tier 4: the six parsed company catalogues, unambiguous names only
    cat_tt = collections.defaultdict(set)
    cat_rows = []
    for p in sorted(glob.glob(os.path.join(DRIVE, "_*_clean.json"))):
        d = json.load(open(p, encoding="utf-8"))
        rows = d if isinstance(d, list) else (d.get("titles") or d.get("rows") or [])
        for r in rows:
            if isinstance(r, dict) and r.get("title") and r.get("imdb_id"):
                cat_rows.append((bare(r["title"]), r["imdb_id"].strip()))
                cat_tt[bare(r["title"])].add(r["imdb_id"].strip())
    for b, tt in cat_rows:
        if len(cat_tt[b]) > 1:
            skipped["tier4 catalogue name -> several tt"] += 1
            continue
        if b in ambiguous_name:
            skipped["tier4 our name is not unique"] += 1
            continue
        t = unique_name.get(b)
        if t is None:
            skipped["tier4 title not held"] += 1
            continue
        offer(t, tt, 4)

    # ---- one tt must not land on two of our titles
    per_tt = collections.defaultdict(list)
    for tid, (tt, tier) in prop.items():
        per_tt[tt].append(tid)
    for t in titles:
        cur = (t.get("imdb_id") or "").strip()
        if cur:
            per_tt[cur].append(t["title_id"])
    collisions = {tt: ids for tt, ids in per_tt.items() if len(set(ids)) > 1}
    for tt, ids in collisions.items():
        for tid in set(ids):
            prop.pop(tid, None)

    tier_n = collections.Counter(tier for _, tier in prop.values())
    for tid, (tt, _) in prop.items():
        by_id[tid]["imdb_id"] = tt

    filled = sum(1 for t in titles if (t.get("imdb_id") or "").strip())
    print(f"column added: {added_col}")
    print(f"imdb_id written this run : {len(prop)}")
    for tier in sorted(tier_n):
        label = {1: "source_urls (direct)", 2: "staged title pages", 3: "candyjar staging",
                 4: "company catalogues (name-matched)"}[tier]
        print(f"    tier {tier}  {tier_n[tier]:>4}  {label}")
    print(f"titles now carrying an imdb_id: {filled} of {len(titles)}")
    print()
    print("SKIPPED, by reason:")
    for k, v in skipped.most_common():
        print(f"    {v:>5}  {k}")
    print()
    print(f"ONE tt MATCHING TWO OF OUR TITLES ({len(collisions)}) - not written, these are "
          f"duplicate-row candidates:")
    for tt, ids in list(collisions.items())[:15]:
        print(f"    {tt}  ->  {sorted(set(ids))}")
    if notes:
        print()
        print("CONFLICTS:")
        for x in notes[:20]:
            print(x)

    if "--dry-run" in sys.argv:
        print("\n[dry-run] nothing written")
        return
    save("titles.csv", fields, titles)
    print("\nwritten")


if __name__ == "__main__":
    main()
