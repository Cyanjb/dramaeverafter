"""Propose the DramaBox pass: watch links, episode counts, tropes and platform rows.

PROPOSES ONLY. Writes generator/staging/dramabox_pass_<date>.json and touches no
CSV. Three independent sources, deliberately kept separate in the output so each can
be accepted or rejected on its own:

  LINKS + EPISODES + TROPES  from the cached DramaBox catalogue (3,000 titles, every
                             one carrying tags). Matched to our titles by FULL
                             normalised name.
  PLATFORM ROWS              from the parsed IMDb company PDF, matched on tt. tt is
                             the safe key; the title string is not.

WHY NAME MATCHING IS QUEUED, NOT APPLIED. 83 of our titles share a name with another
row of ours, and a platform catalogue has its own collisions. Any name resolving to
two bookIds, or two of our titles resolving to one bookId, goes to `ambiguous` for a
human ruling. NEVER AUTO-MERGE.

TROPE GUARDS, from the My Drama harvest:
  - a platform's tag list mixes CONTENT with UI/merchandising labels. 'trending'
    cleared the 5+ bar on My Drama and would have published a page nothing can keep
    true. Candidates here are reported with counts so the vocabulary is read BEFORE
    it is stored, and an explicit DROP list is applied.
  - matching a vocabulary by exact slug CANNOT see a near miss. DramaBox ships BOTH
    'Avenge' and 'Revenge'. Near-slugs against our existing 224 tropes are flagged,
    never auto-merged - 'mate'/'mates' are genuinely different in this genre.

NO SYNOPSIS IS TAKEN. The catalogue carries `introduction`; the standing caption rule
forbids copying or rewording it, so it is not read here at all.

Usage:
    py generator/propose_dramabox_pass.py
"""
import csv, difflib, glob, json, os, re, time, collections

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.environ.get("DEA_DATA") or os.path.join(HERE, "..", "data")
CACHE = os.path.join(HERE, "staging", "_dramabox_cache")
OUT = os.path.join(HERE, "staging", "dramabox_pass_" + time.strftime("%Y-%m-%d") + ".json")
BASE = "https://www.dramaboxdb.com"

# UI / merchandising labels, not tropes. Read from the vocabulary report before editing.
DROP_TAGS = {"modern", "trending", "new", "hot", "popular", "completed", "ongoing",
             "all", "free", "exclusive", "recommended", "editor's choice"}


def norm(s):
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def slugify(s):
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", (s or "").lower())).strip("-")


def load_catalogue():
    """name -> {bookId: {...}} from the cached genre pages."""
    idx = {}
    for p in glob.glob(os.path.join(CACHE, "genre_0_p*.html")):
        h = open(p, encoding="utf-8").read()
        m = re.search(r'id="__NEXT_DATA__"[^>]*>(.*?)</script>', h, re.S)
        if not m:
            continue
        try:
            books = json.loads(m.group(1))["props"]["pageProps"].get("bookList", [])
        except Exception:
            continue
        for b in books:
            k = norm(b.get("bookName"))
            if not k:
                continue
            idx.setdefault(k, {})[str(b["bookId"])] = {
                "bookName": b.get("bookName"),
                "slug": b.get("bookNameLower") or slugify(b.get("bookName")),
                "chapterCount": b.get("chapterCount"),
                "tags": b.get("tags") or b.get("labels") or [],
                "views": b.get("viewCountDisplay"),
            }
    return idx


def main():
    cat = load_catalogue()
    print(f"catalogue titles cached : {len(cat)}")

    titles = list(csv.DictReader(open(os.path.join(DATA, "titles.csv"), newline="", encoding="utf-8")))
    av = list(csv.DictReader(open(os.path.join(DATA, "availability.csv"), newline="", encoding="utf-8")))
    tropes = list(csv.DictReader(open(os.path.join(DATA, "tropes.csv"), newline="", encoding="utf-8")))
    our_slugs = {t["slug"] for t in tropes}

    by_id = {t["title_id"]: t for t in titles}
    dbx_rows = {r["title_id"]: r for r in av if r["platform_id"] == "dramabox"}

    # ---- vocabulary report, BEFORE anything is proposed ----
    vocab = collections.Counter()
    for hits in cat.values():
        for meta in hits.values():
            for tag in meta["tags"]:
                vocab[tag] += 1

    near = []
    for tag in vocab:
        s = slugify(tag)
        if s in our_slugs or s in DROP_TAGS:
            continue
        close = difflib.get_close_matches(s, our_slugs, n=2, cutoff=0.86)
        if close:
            near.append({"platform_tag": tag, "slug": s, "near_our_slugs": close,
                         "titles": vocab[tag]})
    # DramaBox ships both of these; they must not be folded together automatically
    internal = []
    tag_slugs = {slugify(t): t for t in vocab}
    for s, t in tag_slugs.items():
        for c in difflib.get_close_matches(s, [x for x in tag_slugs if x != s], n=1, cutoff=0.86):
            pair = tuple(sorted([t, tag_slugs[c]]))
            if pair not in [tuple(sorted(x["pair"])) for x in internal]:
                internal.append({"pair": list(pair),
                                 "counts": [vocab[pair[0]], vocab[pair[1]]]})

    # ---- match our titles to the catalogue by full normalised name ----
    links, tropes_out, ambiguous, unmatched = [], [], [], []
    seen_book = collections.Counter()
    for t in titles:
        hits = cat.get(norm(t["primary_title"]), {})
        if len(hits) > 1:
            ambiguous.append({"title_id": t["title_id"], "our_title": t["primary_title"],
                              "reason": "name maps to several bookIds",
                              "candidates": {k: v["bookName"] for k, v in hits.items()}})
            continue
        if not hits:
            continue
        bid, meta = next(iter(hits.items()))
        seen_book[bid] += 1
        row = dbx_rows.get(t["title_id"])
        clean = [x for x in meta["tags"] if slugify(x) not in DROP_TAGS]
        entry = {"title_id": t["title_id"], "our_title": t["primary_title"],
                 "platform_title": meta["bookName"], "book_id": bid}
        if clean:
            tropes_out.append(dict(entry, tropes=clean,
                                   slugs=[slugify(x) for x in clean]))
        if row is not None and not row["direct_link"].strip():
            links.append(dict(entry,
                              direct_link=f"{BASE}/movie/{bid}/{meta['slug']}",
                              episode_count=meta["chapterCount"], views=meta["views"]))
        elif row is None:
            unmatched.append(dict(entry, note="catalogue match but NO dramabox availability row"))

    # two of our titles pointing at one bookId is a collision, not a win
    collide = [b for b, n in seen_book.items() if n > 1]

    out = {
        "generated": time.strftime("%Y-%m-%d %H:%M"),
        "source": "cached dramaboxdb /genres/0 catalogue + parse_imdb_company_pdf.py",
        "caption_rule": "NO SYNOPSIS TAKEN. links, episode counts, view counts and tags only.",
        "APPLIES_NOTHING": True,
        "trope_vocabulary_READ_THIS_FIRST": {
            "distinct_tags": len(vocab),
            "dropped_as_ui_labels": sorted(t for t in vocab if slugify(t) in DROP_TAGS),
            "near_miss_against_our_tropes_DO_NOT_AUTOMERGE": near,
            "near_miss_within_dramabox_DO_NOT_AUTOMERGE": internal,
            "top_50": vocab.most_common(50),
        },
        "links_for_rows_missing_one": links,
        "tropes_for_matched_titles": tropes_out,
        "ambiguous_needs_ruling": ambiguous,
        "bookids_claimed_by_two_of_our_titles": collide,
        "catalogue_match_but_no_dramabox_row": unmatched,
    }
    json.dump(out, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)

    print(f"distinct tags in catalogue : {len(vocab)}")
    print(f"  dropped as UI labels     : {len(out['trope_vocabulary_READ_THIS_FIRST']['dropped_as_ui_labels'])}")
    print(f"  near-miss vs our tropes  : {len(near)}")
    print(f"  near-miss within DramaBox: {len(internal)}")
    print(f"LINKS proposed             : {len(links)}")
    print(f"TROPES proposed for titles : {len(tropes_out)}")
    print(f"ambiguous (ruling needed)  : {len(ambiguous)}")
    print(f"bookIds claimed twice      : {len(collide)}")
    print(f"match but no dramabox row  : {len(unmatched)}")
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    main()
