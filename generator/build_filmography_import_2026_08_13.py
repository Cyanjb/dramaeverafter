"""Build the import queue for titles credited to actors we already track, limited to
those a parsed IMDb company catalogue can give a PLATFORM.

WHY THIS IS "CHOSEN, NOT SWEPT". The standing rule forbids bulk-adding whatever a
catalogue returns. This is not that. Every candidate has to clear TWO independent
filters: an actor we already feature is credited on it (from a filmography PDF Cyan
supplied), AND an IMDb company catalogue names its platform. A catalogue row alone
is not enough, and a credit alone is not enough.

WHY PLATFORM IS THE GATE. Measured 13 Aug: of 262 titles we already hold with no
availability row, ZERO have a poster and 13 of 262 have a synopsis. Platform, link,
poster and description all come from the platform, so a title imported without one
is permanently a page that cannot say where to watch. 165 of the 483 missing titles
can have one; the other 318 are deliberately left out.

TRAPS THIS CHECKS FOR, none of which a naive importer would catch:

  - a catalogue name that maps to MORE THAN ONE tt id (6 exist) - skipped, because
    which production the credit refers to is then unknown
  - a bare title that already exists in titles.csv - skipped, it is not missing
  - NEAR-DUPLICATES INSIDE THE IMPORT SET ITSELF. Armand Procacci's page lists both
    "Beyond the Holy Lie" and "Beyond the Holy Line", same character, same year,
    almost certainly one production entered twice on IMDb. Their bare names differ
    by one letter so no exact-match dedupe sees them. Anything within a small edit
    distance of another candidate is held back for a ruling.
  - a slug that would collide with an existing title_id

Nothing is written by this script. It produces a staging JSON for review.
"""
import csv, glob, json, os, re, collections, difflib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
DRIVE = os.path.join(ROOT, "generator", "staging", "drive_2026-08-09")
OUT = os.path.join(ROOT, "generator", "staging", "filmography_import_2026-08-13.json")


def loose(s):
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def bare(s):
    return loose(re.sub(r"^(the|a|an)\s+", "", (s or "").strip().lower()))


def slugify(s):
    # Matches CONVENTIONS.md: apostrophes become hyphens, ReelShort-style.
    return re.sub(r"[^a-z0-9]+", "-", (s or "").lower()).strip("-")


def rows(n):
    return list(csv.DictReader(open(os.path.join(DATA, n), newline="", encoding="utf-8")))


def main():
    titles = rows("titles.csv")
    held_bare = {bare(t["primary_title"]) for t in titles}
    for t in titles:
        for a in (t.get("alt_titles") or "").split("|"):
            if a.strip():
                held_bare.add(bare(a))
    used_ids = {t["title_id"] for t in titles}

    # 1. every credit from a staged filmography whose title we do NOT hold
    missing = collections.defaultdict(list)
    for p in sorted(glob.glob(os.path.join(DRIVE, "actor__*.json"))):
        d = json.load(open(p, encoding="utf-8"))
        for c in d["credits"]:
            b = bare(c["title"])
            if b and b not in held_bare:
                missing[b].append({"actor": d["name"], "person_id": d["person_id"],
                                   "title": c["title"], "character": c.get("character") or "",
                                   "year": c.get("year")})

    # 2. platform from the parsed company catalogues, unambiguous names only
    cat_tt = collections.defaultdict(set)
    cat = {}
    for p in sorted(glob.glob(os.path.join(DRIVE, "_*_clean.json"))):
        plat = os.path.basename(p).strip("_").replace("_clean.json", "")
        d = json.load(open(p, encoding="utf-8"))
        rs = d if isinstance(d, list) else (d.get("titles") or d.get("rows") or [])
        for r in rs:
            if isinstance(r, dict) and r.get("title"):
                b = bare(r["title"])
                cat_tt[b].add(r.get("imdb_id"))
                cat.setdefault(b, {"platform": plat, "imdb_id": r.get("imdb_id"),
                                   "catalogue_title": r["title"], "rank": r.get("rank")})

    cand, skipped = [], collections.Counter()
    for b, credits in missing.items():
        c = cat.get(b)
        if not c:
            skipped["no platform in any catalogue"] += 1
            continue
        if len(cat_tt[b]) > 1:
            skipped["catalogue name maps to several tt ids"] += 1
            continue
        # prefer the catalogue's own spelling for primary_title
        name = c["catalogue_title"]
        sl = slugify(name)
        if sl in used_ids:
            skipped["slug already exists"] += 1
            continue
        years = [x["year"] for x in credits if x.get("year")]
        cand.append({
            "title_id": sl, "slug": sl, "primary_title": name,
            "imdb_id": c["imdb_id"], "platform_id": c["platform"],
            "year": min(years) if years else "",
            "imdb_popularity_rank": c.get("rank"),
            "credited_actors": len({x["person_id"] for x in credits}),
            "credits": credits,
        })

    # 3. near-duplicates INSIDE the import set
    held = []
    names = [c["primary_title"] for c in cand]
    dupe_pairs = []
    for i, a in enumerate(names):
        for bnm in names[i + 1:]:
            if a == bnm:
                continue
            r = difflib.SequenceMatcher(None, bare(a), bare(bnm)).ratio()
            if r >= 0.93:
                dupe_pairs.append((a, bnm, round(r, 3)))
    flagged = {x for pair in dupe_pairs for x in pair[:2]}
    ready = [c for c in cand if c["primary_title"] not in flagged]
    held = [c for c in cand if c["primary_title"] in flagged]

    out = {
        "generated": "2026-08-13",
        "rule": "A title qualifies only if BOTH an actor we track is credited on it AND a parsed IMDb company catalogue names its platform. Chosen, not swept.",
        "caption_rule": "No synopsis and no poster are invented. Both come from the platform and neither is available here, so those fields stay blank.",
        "counts": {
            "distinct missing titles": len(missing),
            "candidates with a platform": len(cand),
            "READY to import": len(ready),
            "HELD as near-duplicates": len(held),
        },
        "skipped": dict(skipped),
        "near_duplicate_pairs": dupe_pairs,
        "held_for_ruling": held,
        "ready": sorted(ready, key=lambda x: (-x["credited_actors"], x["primary_title"])),
    }
    json.dump(out, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)

    print(f"wrote {OUT}")
    print(f"  distinct missing titles      : {len(missing)}")
    print(f"  have a platform              : {len(cand)}")
    print(f"  READY to import              : {len(ready)}")
    print(f"  HELD as near-duplicates      : {len(held)}")
    print()
    print("skipped:")
    for k, v in skipped.most_common():
        print(f"    {v:>4}  {k}")
    print()
    by_p = collections.Counter(c["platform_id"] for c in ready)
    print("ready, by platform:", dict(by_p))
    print()
    if dupe_pairs:
        print("NEAR-DUPLICATE PAIRS held back:")
        for a, b, r in dupe_pairs:
            print(f"    {r}  {a}   <->   {b}")
    print()
    print("top of the queue (most tracked actors crediting it):")
    for c in out["ready"][:10]:
        print(f"    {c['credited_actors']} actors  {c['platform_id']:10} {c['primary_title'][:44]:46} {c['year']}")


if __name__ == "__main__":
    main()
