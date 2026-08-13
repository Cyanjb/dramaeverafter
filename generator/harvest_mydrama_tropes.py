#!/usr/bin/env python3
"""Harvest My Drama TROPES from the ld+json the description pass already read.

WHY THIS EXISTS. Under the five-point bar (13 Aug) My Drama scores ZERO complete
out of 186, despite holding 184 watch links, 183 descriptions and 139 casts. One
field does that: not a single My Drama title has a trope. Zero across an entire
platform is not a content gap, it is the sec 18 signature - when one field is short
while its payload siblings are present, SUSPECT THE PARSER BEFORE THE SOURCE.

SEC 5's FIELD LIST IS INCOMPLETE, VERIFIED 13 AUG. It records name, slug,
description, totalEpisodes, cast, likes, rating, langs and coverUrl, and no genre
or tag field, which made this look like data My Drama simply does not publish. The
page says otherwise. The schema.org TVSeries node carries:

    genre    = ['Betrayal', 'Billionaire', 'Contract', 'Contract Marriage',
                'Enemies To Lovers', 'Love After Marriage', 'Mystery',
                'Toxic Relationship']
    keywords = the same list as one comma-joined string

Those are TROPES in our sense, not genres, and they sit in the SAME node the 9 Aug
description harvest read. That pass took `description` and walked straight past
them. This is the second time sec 5 has been wrong in a checkable way, after the
actor-pages-carry-photos guess, so prefer the page over the field list.

Note "seriesData" is GONE from the page entirely - My Drama restructured since the
17 July scrape. The ld+json route from sec 19 is now the only one, which is another
reason to read it rather than the streamed payload.

TROPES ARE FACTUAL CATEGORY LABELS, NOT PROSE, so taking them is not the thing the
caption rule forbids. The rule exists because a synopsis is creative expression;
a genre tag is an attribute. They are also mapped into OUR existing vocabulary
rather than stored as given.

VOCABULARY MAPPING MATTERS MORE THAN IT LOOKS. build.py canonicalises tropes by
SLUG and the trope page filename comes from that slug, so storing 'Enemies To
Lovers' beside our existing 'enemies to lovers' does not create a duplicate page -
it makes the most-frequent spelling win and silently changes the label on an
existing page. So every incoming value is resolved to the spelling we already use
for that slug, and only genuinely new slugs are stored, lowercased to match the
dominant convention.

SEPARATOR IS SEMICOLON. build.py's _raw_tropes splits on ';'. A pipe would read as
one enormous trope name.

Usage:
    py harvest_mydrama_tropes.py [--limit N] [--dry-run]
"""
import os, re, csv, sys, json, time, argparse, collections

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

# Reuse the audited reader rather than writing a second one. fetch() carries the
# retry and pacing; series_node() knows which @graph node is the title's.
from harvest_mydrama_descriptions import fetch, series_node, DATA, term_of

SOURCE = "mydrama_tropes_" + time.strftime("%Y-%m-%d")
STAGE = os.path.join(HERE, "staging", "mydrama_tropes_%s.json" % time.strftime("%Y-%m-%d"))


def rows(n):
    return list(csv.DictReader(open(os.path.join(DATA, n), newline="", encoding="utf-8")))


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", (s or "").lower()).strip("-")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    titles = rows("titles.csv")
    avail = rows("availability.csv")
    t_by_id = {t["title_id"]: t for t in titles}

    # Our existing vocabulary: slug -> the spelling we already use most often.
    freq = collections.Counter()
    for t in titles:
        for x in (t.get("tropes") or "").split(";"):
            if x.strip():
                freq[x.strip()] += 1
    canon = {}
    for name, _ in sorted(freq.items(), key=lambda kv: (-kv[1], kv[0])):
        canon.setdefault(slug(name), name)
    print("existing vocabulary: %d spellings -> %d slugs" % (len(freq), len(canon)))

    todo = []
    for a in avail:
        if a["platform_id"] != "my-drama" or not (a.get("direct_link") or "").strip():
            continue
        t = t_by_id.get(a["title_id"])
        if t is not None and not (t.get("tropes") or "").strip():   # fill-blank-only
            todo.append((t, a["direct_link"]))
    if args.limit:
        todo = todo[:args.limit]
    print("My Drama titles with a link and no trope: %d" % len(todo))

    found, results, problems, new_slugs = 0, {}, [], collections.Counter()
    for i, (t, url) in enumerate(todo, 1):
        # fetch() returns (html, error) - it swallows the exception and reports it,
        # so an unchecked call yields a tuple and every parse silently fails.
        html, err = fetch(url)
        if err or not html:
            problems.append((t["title_id"], "fetch failed: %s" % err))
            continue
        node = series_node(html)
        if not node:
            problems.append((t["title_id"], "no TVSeries node"))
            continue

        # CONTROL: the node must be about the title we asked for. Cheap, and it is
        # what stops a redirect or a stale cache writing another show's tropes.
        name = (node.get("name") or "").strip()
        if slug(name) != slug(t["primary_title"]):
            problems.append((t["title_id"], "name mismatch: page says %r" % name[:60]))
            continue

        g = node.get("genre") or []
        if isinstance(g, str):
            g = [x.strip() for x in g.split(",")]
        vals, seen = [], set()
        for raw in g:
            raw = (raw or "").strip()
            s = slug(raw)
            if not s or s in seen:
                continue
            seen.add(s)
            if s in canon:
                vals.append(canon[s])            # our spelling wins
            else:
                vals.append(raw.lower())         # new slug, match the convention
                new_slugs[raw.lower()] += 1
        if not vals:
            problems.append((t["title_id"], "TVSeries node carries no genre"))
            continue
        results[t["title_id"]] = ";".join(vals)
        found += 1
        if i % 25 == 0:
            print("  %d/%d ..." % (i, len(todo)))
        time.sleep(1.0)                          # polite, serial

    print()
    print("titles with tropes recovered : %d of %d" % (found, len(todo)))
    print("problems                     : %d" % len(problems))
    for tid, why in problems[:15]:
        print("    - %s: %s" % (tid, why))
    if new_slugs:
        print()
        print("NEW trope slugs not already in our vocabulary (%d):" % len(new_slugs))
        for k, v in new_slugs.most_common(25):
            print("    %3d  %s" % (v, k))

        # A NEW SLUG THAT IS NEARLY AN EXISTING ONE IS THE DANGEROUS CASE, because
        # exact-slug matching above cannot see it and build.py cannot fold it: two
        # slugs means two pages competing for one concept. The 13 Aug run produced
        # 'vampires' beside an existing 'vampire' that carries 642 titles. Flag, do
        # NOT auto-merge - 'mate'/'mates' are genuinely different in this genre.
        import difflib
        warn = []
        for n in new_slugs:
            for existing in canon:
                a, b = slug(n).replace("-", ""), existing.replace("-", "")
                if a == b or difflib.SequenceMatcher(None, a, b).ratio() >= 0.87:
                    warn.append((n, canon[existing], freq[canon[existing]]))
        if warn:
            print()
            print("!! NEAR-DUPLICATE OF AN EXISTING TROPE - rule these before rebuilding:")
            for n, e, c in warn:
                print("    new %-22s <-> existing %-22s (%d titles)" % (n, e, c))

    payload = {
        "source": SOURCE,
        "read_from": "schema.org ld+json @graph, TVSeries node, genre[]",
        "rule": "Tropes are factual category labels, not prose. Mapped into our "
                "existing vocabulary by slug; only new slugs stored as given.",
        "recovered": results,
        "problems": problems,
        "new_slugs": dict(new_slugs),
    }
    os.makedirs(os.path.dirname(STAGE), exist_ok=True)
    json.dump(payload, open(STAGE, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("\nstaged -> %s" % STAGE)

    if args.dry_run:
        print("[dry-run] titles.csv not written")
        return 0

    fields = list(titles[0].keys())
    n = 0
    for t in titles:
        v = results.get(t["title_id"])
        if v and not (t.get("tropes") or "").strip():
            t["tropes"] = v
            t["source"] = t.get("source") or SOURCE
            n += 1
    import io
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=fields, lineterminator=term_of("titles.csv"))
    w.writeheader()
    w.writerows(titles)
    open(os.path.join(DATA, "titles.csv"), "w", newline="", encoding="utf-8").write(buf.getvalue())
    print("written: tropes filled on %d titles" % n)
    return 0


if __name__ == "__main__":
    sys.exit(main())
