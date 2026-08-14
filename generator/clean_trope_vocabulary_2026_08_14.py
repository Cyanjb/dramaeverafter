#!/usr/bin/env python3
"""The trope vocabulary cleanup, 14 Aug 2026. Cyan's rulings, one pass.

Raised by Cyan: "I see you have SM as a trope, what is that? 261 tropes is a lot.
I also notice you have some stuff tagged Secret Billionaire but not Billionaire?"
All three shared one cause: tags were taken from each platform's own vocabulary and
never reconciled, so the same idea sits under several spellings, sub-variants never
meet their parent, and platform content labels we never chose went live as pages.

Full diagnosis and the measured options are in TROPE-CLEANUP-PROPOSAL.md.

WHAT THIS DOES, in the order it must happen:

  1 CANONICALISE SPELLINGS. 41 concepts are stored under more than one spelling,
    hyphen vs space vs case ('underdog rise' 1615 / 'underdog-rise' 50). Cyan:
    "we only need one way of spelling, I think without the dash is fine." So for a
    PAIR, the spaced form wins. Singletons are left alone - 'sci-fi' and 'rom-com'
    are legitimately hyphenated and are not pairs.
    NOTE this is data tidying, not a page fix: build.py already folds hyphen, space
    and case onto one slug (see its comment at the TROPE_CANON block), so these
    were never two pages. An earlier draft of the proposal claimed 37 redirects
    were needed. That was wrong. No URL changes here at all.

  2 SEMANTIC FOLDS, each one ruled individually by Cyan. A sub-variant folds into
    its parent only where the modifier adds nothing a visitor would browse by:
        female ceo         -> CEO
        fake heiress       -> heiress
        secret heiress     -> heiress
        secret billionaire -> billionaire
        billionaires       -> billionaire
        hidden identity    -> secret identity
        campus bullying    -> bullying
    EXPLICITLY HELD DISTINCT by the same ruling, do not "tidy" these later:
        contract marriage, dark romance, office romance, family reunion.

  3 SINGULAR/PLURAL FOLDING. Cyan, 14 Aug: "Singular and plural tropes, it should
    be folded in." This OVERRULES the caution in merge_split_tropes.py, which said
    not to generalise plural folding because 'mate' and 'mates' differ in this
    genre. Her call, and it is recorded here so the reversal is not mistaken for
    drift. Any pair found is folded into the MORE FREQUENT side, and every pair is
    printed so the ruling stays auditable.

  4 THE THREE CONTENT LABELS. sm (212) and gay (190) are GoodShort-only and the
    data contradicts them - 118 of the sm titles also carry 'cute kids'. Both are
    deleted outright. bl is 356, of which 346 are GoodShort noise and 10 are Vigloo
    and look genuine ('An Omega Among Alphas', tagged cleanly as bl;romance), so
    the GoodShort 346 are dropped and the Vigloo 10 are KEPT. build.py's
    TROPE_ACRONYMS already renders it 'BL'.

  5 GOODSHORT DE-NOISING AT 50%, Cyan's ruling. GoodShort tags 35.1 tropes per
    title where every other source averages 3.3, and its commonest tags cover
    almost the whole catalogue (counterattack 98%, CEO 95%). A tag on 98% of a
    catalogue carries no information. SOURCE-SCOPED: a tag is dropped only from
    GoodShort rows, so CEO survives untouched wherever it is real. Measured before
    choosing: dropping GoodShort tags ENTIRELY would zero 1,820 titles and cost 88
    published pages, which is why that was not proposed.

  6 GENRES OUT OF THE TROPE FIELD, into the genres column that already exists.
    romance, fantasy, thriller, animation, drama, comedy, sci-fi, horror.
    anime (311) is DELETED rather than moved: all 311 are GoodShort, whose
    catalogue is live-action vertical drama - 'A Mother's Unbroken Tomorrow' is not
    anime. Checked against the titles before deciding, per Cyan's flag.

  7 REGENERATE tropes.csv from actual usage. title_count was wrong on 170 of 224
    rows (CEO declared 103 against 1,827 real), 117 tropes were in use but absent
    from the file, and 41 were declared with zero usage.

NOT DONE HERE, deliberately: avenge -> revenge. 'avenge' is not in our data at all;
it is a DRAMABOX tag, found in the cached DramaBox vocabulary. Cyan's ruling is
recorded in TROPE-CLEANUP-PROPOSAL.md and applies when the DramaBox tags are
imported, together with her singular/plural ruling on DramaBox's 'Billionaires',
'Childhood Sweetheart', 'Contract Lover' and 'Athlete'.

Usage:
    py generator/clean_trope_vocabulary_2026_08_14.py [--dry-run]
"""
import csv, io, os, re, sys, collections

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.environ.get("DEA_DATA") or os.path.join(os.path.dirname(HERE), "data")
DRY = "--dry-run" in sys.argv

GOODSHORT = "goodshort_2026-07-17"
NOISE_THRESHOLD = 0.50

DROP_EVERYWHERE = {"sm", "gay", "anime"}
DROP_FROM_GOODSHORT_ONLY = {"bl"}
TO_GENRES = ["romance", "fantasy", "thriller", "animation", "drama", "comedy",
             "sci-fi", "horror"]
# A compound tag DECOMPOSES into every trope it actually contains, not just one.
# Cyan, 14 Aug, checking the secret heiress case: "that should be tagged hidden
# identity or secret identity, whichever one you kept, AND heiress. So it should
# have those two tags." Folding it to 'heiress' alone would silently drop the
# secret half, which is the browsable part.
SEMANTIC = {
    "female ceo": ["CEO"],
    "secret heiress": ["heiress", "secret identity"],
    "secret billionaire": ["billionaire", "secret identity"],
    "fake heiress": ["heiress", "secret identity"],
    "campus bullying": ["bullying", "campus"],
    "billionaires": ["billionaire"],
    "hidden identity": ["secret identity"],
}
HELD_DISTINCT = {"contract marriage", "dark romance", "office romance", "family reunion"}

# Kept on GoodShort titles despite clearing the noise threshold. Cyan, 14 Aug:
# these are popular tropes people browse by, and GoodShort is their ONLY source -
# so cutting them does not de-noise the page, it deletes the trope from the site.
# 'contract marriage' is hers too: "a very important trope, especially in the
# Chinese dramas", so it goes wherever it applies.
EXEMPT_FROM_NOISE_CUT = {"reborn", "toxic love", "sweet", "misunderstanding",
                         "cute kids", "contract marriage"}


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def term_of(p):
    raw = open(p, "rb").read()
    c = raw.count(b"\r\n")
    return "\r\n" if c > raw.count(b"\n") - c else "\n"


def split_field(v):
    return [x.strip() for x in (v or "").split(";") if x.strip()]


def main():
    tp = os.path.join(DATA, "titles.csv")
    term = term_of(tp)
    with io.open(tp, encoding="utf-8-sig", newline="") as f:
        titles = list(csv.DictReader(f))
    fields = list(titles[0].keys())

    raw_usage = collections.Counter()
    for t in titles:
        for x in split_field(t.get("tropes")):
            raw_usage[x] += 1

    # --- step 1: spelling canonicalisation, spaced form wins a PAIR -------------
    groups = collections.defaultdict(list)
    for name in raw_usage:
        groups[slug(name)].append(name)
    spelling = {}
    for s, variants in groups.items():
        if len(variants) < 2:
            continue
        undashed = [v for v in variants if "-" not in v]
        pool = undashed or variants
        winner = max(pool, key=lambda v: (raw_usage[v], v))
        for v in variants:
            if v != winner:
                spelling[v] = winner
    print("STEP 1  spelling pairs collapsed: %d variants -> %d canonical"
          % (len(spelling), len(set(spelling.values()))))
    for v, w in sorted(spelling.items(), key=lambda kv: -raw_usage[kv[0]])[:10]:
        print("        %-26r -> %-26r (%d + %d)" % (v, w, raw_usage[v], raw_usage[w]))

    def expand(name):
        """A raw tag -> the list of canonical tropes it becomes (usually one)."""
        n = spelling.get(name, name)
        return SEMANTIC.get(n.lower(), [n])

    # --- step 3: singular/plural detection, after spelling ---------------------
    post = collections.Counter()
    for name, n in raw_usage.items():
        for c in expand(name):
            post[c] += n
    plural = {}
    for name in list(post):
        if name.lower() in HELD_DISTINCT:
            continue
        for other in (name + "s", name + "es"):
            match = next((k for k in post if k.lower() == other.lower()), None)
            if match and match != name:
                lo, hi = sorted([name, match], key=lambda k: post[k])
                plural[lo] = hi
    print("\nSTEP 3  singular/plural pairs folded: %d" % len(plural))
    for lo, hi in sorted(plural.items(), key=lambda kv: -post[kv[1]]):
        flag = "  <-- FLAG: documented as genuinely different" if lo.lower() in (
            "mate", "mates", "werewolf", "werewolves") else ""
        print("        %-24r=%-5d -> %-24r=%d%s" % (lo, post[lo], hi, post[hi], flag))

    def expand2(name):
        return [plural.get(c, c) for c in expand(name)]

    # --- step 5: GoodShort noise set, computed AFTER canonicalisation ----------
    gs = [t for t in titles if t.get("source") == GOODSHORT and split_field(t.get("tropes"))]
    gsv = collections.Counter()
    for t in gs:
        seen = set()
        for y in split_field(t.get("tropes")):
            seen.update(expand2(y))
        for x in seen:
            gsv[x] += 1
    over = {k for k, v in gsv.items() if v / float(len(gs)) >= NOISE_THRESHOLD}
    noisy = {k for k in over if k.lower() not in EXEMPT_FROM_NOISE_CUT}
    kept = sorted(over - noisy, key=lambda k: -gsv[k])
    print("\nSTEP 5  GoodShort titles: %d | over the %.0f%% line: %d | cut: %d | EXEMPT: %d"
          % (len(gs), NOISE_THRESHOLD * 100, len(over), len(noisy), len(kept)))
    for k in sorted(noisy, key=lambda k: -gsv[k]):
        print("        cut    %-26r %4d  (%.0f%%)" % (k, gsv[k], 100.0 * gsv[k] / len(gs)))
    for k in kept:
        print("        KEEP   %-26r %4d  (%.0f%%)  Cyan's exemption" % (k, gsv[k], 100.0 * gsv[k] / len(gs)))

    # --- apply ----------------------------------------------------------------
    genre_moved = collections.Counter()
    dropped = collections.Counter()
    changed = emptied = 0
    for t in titles:
        before = split_field(t.get("tropes"))
        if not before:
            continue
        is_gs = t.get("source") == GOODSHORT
        genres = split_field(t.get("genres"))
        out, seen = [], set()
        for x in before:
            for n in expand2(x):
                low = n.lower()
                if low in DROP_EVERYWHERE:
                    dropped[low] += 1
                    continue
                if is_gs and low in DROP_FROM_GOODSHORT_ONLY:
                    dropped[low + " (goodshort)"] += 1
                    continue
                if low in TO_GENRES:
                    if not any(g.lower() == low for g in genres):
                        genres.append(n)
                        genre_moved[low] += 1
                    continue
                if is_gs and n in noisy:
                    dropped["[goodshort noise] " + n] += 1
                    continue
                k = slug(n)
                if k and k not in seen:
                    seen.add(k)
                    out.append(n)
        after = ";".join(out)
        if after != (t.get("tropes") or "") or ";".join(genres) != (t.get("genres") or ""):
            changed += 1
        if before and not out:
            emptied += 1
        t["tropes"] = after
        t["genres"] = ";".join(genres)

    print("\nAPPLY   titles changed: %d | titles left with NO trope: %d" % (changed, emptied))
    print("        genres moved out of tropes: %s" % dict(genre_moved))
    print("        deleted labels: %s"
          % {k: v for k, v in dropped.items() if not k.startswith("[goodshort noise]")})
    print("        goodshort noise assignments removed: %d"
          % sum(v for k, v in dropped.items() if k.startswith("[goodshort noise]")))

    # --- step 7: regenerate tropes.csv from reality ----------------------------
    final = collections.Counter()
    for t in titles:
        for x in split_field(t.get("tropes")):
            final[x] += 1
    canon_by_slug = {}
    for name, n in sorted(final.items(), key=lambda kv: (-kv[1], kv[0])):
        canon_by_slug.setdefault(slug(name), (name, 0))
    counts = collections.Counter()
    for name, n in final.items():
        counts[slug(name)] += n

    tr_path = os.path.join(DATA, "tropes.csv")
    with io.open(tr_path, encoding="utf-8-sig", newline="") as f:
        old = list(csv.DictReader(f))
    desc = {r["trope_id"]: r.get("description", "") for r in old}
    new_rows = []
    for s in sorted(canon_by_slug):
        name = canon_by_slug[s][0]
        new_rows.append({"trope_id": s, "name": name, "slug": s,
                         "description": desc.get(s, ""), "title_count": counts[s]})
    print("\nSTEP 7  tropes.csv: %d rows -> %d rows (distinct slugs actually in use)"
          % (len(old), len(new_rows)))
    print("        publishable at 5+: %d" % sum(1 for r in new_rows if r["title_count"] >= 5))

    if DRY:
        print("\nDRY RUN - nothing written.")
        return

    with io.open(tp, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator=term)
        w.writeheader()
        w.writerows(titles)
    tterm = term_of(tr_path)
    with io.open(tr_path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["trope_id", "name", "slug", "description",
                                          "title_count"], lineterminator=tterm)
        w.writeheader()
        w.writerows(new_rows)
    print("\nwritten: data/titles.csv, data/tropes.csv")


if __name__ == "__main__":
    main()
