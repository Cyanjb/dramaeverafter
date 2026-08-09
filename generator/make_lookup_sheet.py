#!/usr/bin/env python3
"""Regenerate LOOKUPS.md, the offline question sheet.

Sibling to make_worklists.py and generated for the same reason: a decision
recorded in the CSVs must leave the queue by itself, because the hand-written
predecessors kept asking for rulings that had already been made.

This file asks the questions a REFERENCE LOOKUP can answer in one glance --
"is this one production or two", "who is in this" -- as opposed to CAST-WANTED.md,
which asks for a saved IMDb page. The distinction matters because the two are
worked in different places: CAST-WANTED needs a browser and a PDF export, this
needs a name and thirty seconds.

Answers are written back INTO this file, on the ANSWER line under each question,
so one file goes out and the same file comes back. Nothing parses it yet -- the
returned sheet is read by whoever applies it, the same way the IMDb PDFs were.
The line format is kept regular (fixed keys, one value each) so that a parser
can be written against a real filled-in sheet rather than a guessed one.

Sourcing note, and the reason the ANSWER line asks where the answer came from:
individual facts are not ownable, so looking one up in any reference is ordinary
research, but a fact is only worth as much as its provenance. Recording IMDb
where IMDb confirms it means the row does not depend on whoever was consulted
first, and lets a later session re-check it. See doc 7 on VerticalVault: it is a
competitor, not a source, and the difference between consulting it and mirroring
it is volume and shape, not permission.

Usage:
    python3 make_lookup_sheet.py [--limit-cast N] [--dry-run]
"""
import csv, os, re, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
REPO = os.path.dirname(HERE)

# IMDb popularity rank from the co1130595 CandyJar company page, read 8 Aug 2026.
# Rank 1 is the most popular of the 59 titles credited to the company. Held here
# rather than in the CSVs because it is a snapshot of someone else's ordering, not
# a property of the title, and it will be stale the moment they recrawl.
CJ_RANK = {
    "grayson": 2, "study buddy": 3, "the ecstasy of faking it": 5,
    "don't say te amo": 10, "spoiled rotten": 11, "next door": 15,
    "secrets of vixen": 25, "the alpha's doe": 26, "beastly lights": 28,
    "luna graced": 31, "broken": 32, "my silent treasure": 34,
    "the all-american rejects: superfan": 36, "his muse": 38,
    "victory formation": 39, "hated by my mate": 42, "conflict of interest": 43,
    "half of my heart": 44, "enemies with benefits": 45, "the tutors": 46,
    "in love with mr. mafia": 47, "not all about you": 49,
    "exercise discretion": 52, "french kiss": 54, "our dirty little secret": 56,
    "new beginnings": 57, "secrets of siren": 58,
    "billionaire love start with lies": 59,
}


def rows(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit-cast", type=int, default=40)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    titles = rows("titles.csv")
    credits = rows("credits.csv")
    avail = rows("availability.csv")
    queue = rows("match_queue.csv")

    t_by_id = {t["title_id"]: t for t in titles}
    cast_n = {}
    for c in credits:
        cast_n[c["title_id"]] = cast_n.get(c["title_id"], 0) + 1
    plats = {}
    for a in avail:
        plats.setdefault(a["title_id"], set()).add(a["platform_id"])

    # An unruled row is one whose status is neither confirmed_same nor
    # confirmed_different. Blank and 'pending' both mean nobody has decided;
    # they are only different in that blank predates the status column.
    def unruled(q):
        s = (q.get("status") or "").strip().lower()
        return not s.startswith("confirmed")

    pending = [q for q in queue if unruled(q)]

    out = [
        "# Lookups: questions, not page saves",
        "",
        f"{len(pending)} rulings and a cast list. Each one is a single question that a",
        "reference answers in a glance, which is why these are split out from",
        "CAST-WANTED.md - that file wants a saved IMDb page, this one wants a name.",
        "",
        "WRITE ANSWERS ON THE `ANSWER:` LINE and send this same file back. Anything",
        "left blank is simply skipped, so partial is fine and there is no need to",
        "work in order.",
        "",
        "Record WHERE the answer came from. A fact is not ownable and looking one up",
        "is ordinary research, but provenance is what makes the row re-checkable",
        "later, and a fact confirmed on IMDb no longer depends on whoever was asked",
        "first. `imdb`, `platform`, `vv`, or `own knowledge` are all fine.",
        "",
        "---",
        "",
        "## Part 1 - Same production, or two different ones?",
        "",
        "Nearly all of these are punctuation or article differences on a title we",
        "already hold. The question is whether the two names are ONE production. The",
        "fastest tell is the cast: same leads means same show. Answer SAME or DIFF.",
        "",
    ]

    plat_name = {p["platform_id"]: p["name"] for p in rows("platforms.csv")}

    def describe(ref):
        """candidate_a is usually a bare title_id, which is unreadable on a sheet a
        human works from. Resolve it to the title as we hold it, with the platform
        and cast size, so both sides of the question read the same way. Anything
        that is not a known id is already prose and passes through untouched."""
        t = t_by_id.get(ref.strip())
        if not t:
            return ref
        ps = ", ".join(sorted(plat_name.get(p, p) for p in plats.get(t["title_id"], []))) or "no platform"
        n = cast_n.get(t["title_id"], 0)
        return f'"{t["primary_title"]}" on {ps} ({n} cast on file)'

    for i, q in enumerate(pending, 1):
        a, b = q["candidate_a"], q["candidate_b"]
        ev = (q.get("evidence") or "").strip()
        out += [f"### {i}. OURS: {describe(a)}", f"    THEIRS: {b}"]
        if ev:
            out.append(f"    why asked: {ev}")
        out += ["    ANSWER:            (SAME / DIFF)", "    source:", ""]

    # CandyJar castless, most popular first. CandyJar publishes no cast and no view
    # counts, so IMDb popularity rank is the only ordering signal available for this
    # platform -- ranking by view_count would silently sort them all as zero.
    cj = [t for t in titles
          if "candyjar" in plats.get(t["title_id"], set())
          and not cast_n.get(t["title_id"], 0)]
    cj.sort(key=lambda t: (CJ_RANK.get(t["primary_title"].strip().lower(), 999),
                           t["primary_title"].lower()))
    cj = cj[:args.limit_cast]
    ranked = [t for t in cj if t["primary_title"].strip().lower() in CJ_RANK]
    unranked = [t for t in cj if t["primary_title"].strip().lower() not in CJ_RANK]

    out += [
        "---",
        "",
        f"## Part 2 - Who is in these? ({len(cj)} CandyJar titles with no cast at all)",
        "",
        "CandyJar publishes no cast on its own platform and no view counts either, so",
        "these are ordered by IMDb popularity rank rather than by audience size - the",
        "only ordering signal this platform gives. Rank 1 is the most popular of the",
        "59 titles credited to the company, so the top of this list is where a lookup",
        "buys the most.",
        "",
        "Lead names alone are worth having. Character names are worth more, because",
        "indexing roles rather than just actors is the edge chosen on 6 Aug.",
        "",
        "Format: `Actor Name = Character Name`, one per line, leads first.",
        "",
    ]

    def block(t, label):
        tid = t["title_id"]
        yr = (t.get("year") or "").strip()
        syn = (t.get("synopsis_short") or "").strip()
        lines = [f"### {label} {t['primary_title']}" + (f"  ({yr})" if yr else "")]
        if syn:
            lines.append(f"    plot: {syn[:150]}")
        lines += [f"    slug: {tid}", "    CAST:", "        ", "    source:", ""]
        return lines

    for t in ranked:
        block_label = f"[#{CJ_RANK[t['primary_title'].strip().lower()]}]"
        out += block(t, block_label)

    if unranked:
        out += [
            "---",
            "",
            f"### Not on the company page ({len(unranked)})",
            "",
            "These are CandyJar titles in the database that the co1130595 company page",
            "does not list, so they have no popularity rank and may sit under a second",
            "IMDb company entity. Worth finding, because if that entity exists it lists",
            "the rest of the catalogue too.",
            "",
        ]
        for t in unranked:
            out += block(t, "[--]")

    body = "\n".join(out).rstrip() + "\n"
    if args.dry_run:
        print(f"[dry-run] LOOKUPS.md: {len(out)} lines, "
              f"{len(pending)} rulings, {len(cj)} cast questions")
        return
    with open(os.path.join(REPO, "LOOKUPS.md"), "w", encoding="utf-8") as f:
        f.write(body)
    print(f"LOOKUPS.md: {len(pending)} rulings, {len(cj)} cast questions "
          f"({len(ranked)} ranked, {len(unranked)} unranked)")


if __name__ == "__main__":
    main()
