#!/usr/bin/env python3
"""Cyan's trope rulings of 25 Sep 2026: five duplicate families merged, three tropes added.

MERGES, her words: "it should be reborn. Sweet love. Revenge. Secret identity.
Contract." Each family folds onto the name she picked:

    rebirth                                ->  reborn
    sweet, sweet-love, sweet-romance       ->  sweet love     (renamed: was "sweet")
    karma-payback, karma, counterattack    ->  revenge
    multiple-identities                    ->  secret identity
    contract lovers                        ->  contract

CONTRACT MARRIAGE STAYS ITS OWN TROPE. She raised that marriage contracts and
unmarried contract lovers are different; "just contract" is read as the home for
the unmarried ones. Folding 969 contract-marriage titles away is a separate call.

ADDED: plus size, mermaid, reverse harem. The no-guessing rule (14 Aug) holds:
a title is tagged here only when its own title or caption says it outright.
Everything borderline is left for her; see HANDOVER.md, 25 Sep. Mermaid titles also
get the high fantasy umbrella (UMBRELLAS in merge_scrape.py) now, not next run.
Existing "harem" (52) is NOT touched: it mixes male harems with reverse ones.

merge_scrape.py's TAG_ALIASES carries the same merges so ReelShort's own
"rebirth" tag (457 books) lands on reborn instead of recreating the old name.

Old trope URLs get 301s in _redirects. Idempotent: a second run changes nothing.

Usage:
    python3 merge_tropes_2026_09_25.py [--dry-run]
"""
import csv, io, os, sys, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data")
DRY = "--dry-run" in sys.argv

MERGE = {
    "rebirth": "reborn",
    "sweet": "sweet love",
    "sweet-love": "sweet love",
    "sweet-romance": "sweet love",
    "karma-payback": "revenge",
    "karma": "revenge",
    "counterattack": "revenge",
    "multiple-identities": "secret identity",
    "contract lovers": "contract",
}

# (trope_id, name, slug) for the renamed and new vocabulary rows.
NEW_ROWS = [
    ("sweet-love", "sweet love", "sweet-love"),
    ("plus-size", "plus size", "plus-size"),
    ("mermaid", "mermaid", "mermaid"),
    ("reverse-harem", "reverse harem", "reverse-harem"),
]

# Stated outright in the title or caption, checked one by one on 25 Sep.
ADD = {
    "plus size": [
        "the-hockey-captain-that-hates-me",      # "Plus-size figure skater"
        "xl-stands-for-xtra-love",               # "a chubby girl"
        "the-genius-and-the-bad-boy",            # "plus size Sophie"
        "the-mvp-s-plus-size-love",
        "keily",                                 # "the curvy girl"
        "the-xxl-diva-queen-s-revenge",
        "chubby-consort-strikes-back",
        "plus-size-plus-love",
        "slimming-revolution",                   # "nearly three hundred pounds"
        "after-the-330-pound-fat-wolf-left-the-alpha-went-crazy-with-regret",
        "the-mob-boss-s-plus-size-queen",
    ],
    "mermaid": [
        "the-ceo-s-mermaid-bride",
        "the-mermaid-queen-s-revenge",           # "East Sea mermaid princess"
        "my-merman-daddy-takes-me-home",         # "King of Atlantis", merman
        "i-chose-the-playboy-eel-to-abandon-my-shark-lover",  # ocean princess, shark lord
    ],
    "reverse harem": [
        "the-three-badasses-who-want-me",        # "three fiances, one choice"
        "the-alpha-and-beta-s-shared-mate",      # "Mated to the Alpha and the Beta"
    ],
}
UMBRELLA_FOR = {"mermaid": "high fantasy"}

REDIRECTS = [  # old slug -> target slug; only slugs that differ
    ("rebirth", "reborn"),
    ("sweet", "sweet-love"),
    ("sweet-romance", "sweet-love"),
    ("karma-payback", "revenge"),
    ("karma", "revenge"),
    ("counterattack", "revenge"),
    ("multiple-identities", "secret-identity"),
    ("contract-lovers", "contract"),
]


def term_of(p):
    raw = open(p, "rb").read()
    c = raw.count(b"\r\n")
    return "\r\n" if c > raw.count(b"\n") - c else "\n"


def write_csv(p, fields, rows):
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=fields, lineterminator=term_of(p))
    w.writeheader()
    w.writerows(rows)
    open(p, "w", newline="", encoding="utf-8").write(buf.getvalue())


def main():
    tp = os.path.join(DATA, "titles.csv")
    titles = list(csv.DictReader(open(tp, newline="", encoding="utf-8")))
    tfields = list(titles[0].keys())
    by_id = {t["title_id"]: t for t in titles}

    moved, added = collections.Counter(), collections.Counter()
    missing = [tid for ids in ADD.values() for tid in ids if tid not in by_id]
    if missing:
        print("REFUSING: title_ids not found", missing, file=sys.stderr)
        return 1

    for t in titles:
        vals = [x.strip() for x in (t.get("tropes") or "").split(";") if x.strip()]
        out, seen = [], set()
        for v in vals:
            tgt = MERGE.get(v.lower(), v)
            if tgt != v:
                moved[v] += 1
            if tgt.lower() not in seen:          # merging can create a duplicate in-row
                seen.add(tgt.lower())
                out.append(tgt)
        for trope, ids in ADD.items():
            if t["title_id"] in ids:
                for name in [trope] + ([UMBRELLA_FOR[trope]] if trope in UMBRELLA_FOR else []):
                    if name not in seen:
                        seen.add(name)
                        out.append(name)
                        added[name] += 1
        t["tropes"] = ";".join(out)

    for k, v in moved.most_common():
        print("   %-20s -> %-16s on %d titles" % (k, MERGE[k.lower()], v))
    for k, v in added.most_common():
        print("   + %-18s on %d titles" % (k, v))

    # tropes.csv: drop merged-away rows, add/rename, recount everything.
    vp = os.path.join(DATA, "tropes.csv")
    vocab = list(csv.DictReader(open(vp, newline="", encoding="utf-8")))
    vfields = list(vocab[0].keys())
    gone = set(MERGE) - {"sweet-love"}
    vocab = [r for r in vocab if r["name"].lower() not in gone and r["trope_id"] != "sweet-love"]
    have = {r["trope_id"] for r in vocab}
    for tid, name, slug in NEW_ROWS:
        if tid not in have:
            vocab.append({"trope_id": tid, "name": name, "slug": slug, "description": "", "title_count": "0"})
    count = collections.Counter()
    for t in titles:
        for x in {x.strip().lower() for x in (t.get("tropes") or "").split(";") if x.strip()}:
            count[x] += 1
    for r in vocab:
        r["title_count"] = str(count.get(r["name"].lower(), 0))
    for n in ["reborn", "sweet love", "revenge", "secret identity", "contract",
              "plus size", "mermaid", "reverse harem", "high fantasy"]:
        print("   %-16s now %d titles" % (n, count.get(n, 0)))

    rp = os.path.join(ROOT, "_redirects")
    red = open(rp, encoding="utf-8").read()
    lines = []
    for old, new in REDIRECTS:
        for suffix in (".html", ""):
            line = "/tropes/%s%s  /tropes/%s.html  301" % (old, suffix, new)
            if "/tropes/%s%s " % (old, suffix) not in red:
                lines.append(line)

    if DRY:
        print("[dry-run] nothing written; %d redirect lines pending" % len(lines))
        return 0
    write_csv(tp, tfields, titles)
    write_csv(vp, vfields, vocab)
    if lines:
        if not red.endswith("\n"):
            red += "\n"
        red += "# Trope merges, Cyan 25 Sep 2026 (generator/merge_tropes_2026_09_25.py)\n"
        red += "\n".join(lines) + "\n"
        open(rp, "w", encoding="utf-8").write(red)
    print("written; %d redirect lines added" % len(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
