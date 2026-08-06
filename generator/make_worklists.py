#!/usr/bin/env python3
"""Regenerate the two manual worklists, CAST-WANTED.md and AI-CHECK.md.

Both were hand-written one-offs, so nothing removed a title once it was dealt
with. By 2026-08-02 that had gone visibly wrong: all four confirmed-AI titles
were still sitting in CAST-WANTED.md (two of them at slots 1 and 3), asking for
IMDb lookups on productions that have no human cast to find, and AI-CHECK.md
still listed three titles whose ruling had already been made. Generating them
from data/ instead means a decision recorded in the CSVs leaves the queue.

Neither file is consumed by anything; they exist purely to direct manual effort,
so the only cost of being wrong is Cyan's time. That is the thing worth guarding.

Usage:
    python3 make_worklists.py [--cast-limit N] [--dry-run]
"""
import csv, os, re, argparse, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
REPO = os.path.dirname(HERE)

# Platforms that publish cast for their own catalogue, so its absence is a real
# anomaly worth a poster check. Deliberately just these two:
#   reelshort  93% covered from the fandom blog - a gap here is genuinely odd
#   my-drama   75% covered from the Next.js payload - same
# Vigloo and CandyJar are excluded even though our coverage of them is partial.
# adapters.md sec 12 proved Vigloo's remaining titles publish no cast at all, and
# sec 7/13 that CandyJar publishes none on-platform (our 46% came from IMDb). Their
# blanks are already explained, so listing them would send a human to check ~100
# posters for a signal that was never there.
CAST_BEARING = {"reelshort", "my-drama"}


def rows(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as f:
        return list(csv.DictReader(f))


def views(s):
    """'132.3M' -> 132300000. Blank or unparseable -> 0."""
    m = re.match(r"^([\d.]+)\s*([KMB])?$", (s or "").strip().upper())
    if not m:
        return 0
    return int(float(m.group(1)) * {"K": 1e3, "M": 1e6, "B": 1e9, None: 1}[m.group(2)])


def views_label(n):
    if n >= 1e6:
        return f"{n / 1e6:.1f}M"
    if n >= 1e3:
        return f"{n / 1e3:.1f}K"
    return "n/a" if not n else str(n)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cast-limit", type=int, default=120)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    titles = rows("titles.csv")
    plat_name = {p["platform_id"]: p["name"] for p in rows("platforms.csv")}
    credited = {c["title_id"] for c in rows("credits.csv")}

    # Best-performing placement per title: the platform we would point a human at.
    best = {}
    for a in rows("availability.csv"):
        v = views(a["view_count"])
        cur = best.get(a["title_id"])
        if cur is None or v > cur[0]:
            best[a["title_id"]] = (v, a["platform_id"])

    ai_flag = lambda t: (t.get("ai") or "").strip().lower()
    uncredited = [t for t in titles if t["title_id"] not in credited]

    # --- CAST-WANTED: no cast, ranked by reach. Confirmed-AI titles are dropped;
    # there is no cast to find, so every minute spent on one is wasted.
    wanted = []
    for t in uncredited:
        if ai_flag(t) in ("yes", "y", "true", "1"):
            continue
        v, pid = best.get(t["title_id"], (0, ""))
        wanted.append((v, pid, t))
    wanted.sort(key=lambda r: -r[0])
    wanted = wanted[: args.cast_limit]

    out = ["# DramaEverAfter - cast wanted, highest impact first", ""]
    out += ["Save each IMDb page as PDF and hand them over. Click the search link, pick the",
            "result whose plot matches the synopsis shown, then save that page.", ""]
    out += [f"{len(uncredited)} titles have no cast at all. This lists the top {len(wanted)} by view",
            "count. Confirmed-AI titles are excluded - they have no cast to find.", ""]
    for i, (v, pid, t) in enumerate(wanted, 1):
        q = urllib.parse.quote_plus(t["primary_title"] + " ")
        out += [f"{i}. {t['primary_title']}",
                f"   app: {plat_name.get(pid, pid or 'unknown')}   views: {views_label(v)}",
                f"   plot: {(t['synopsis_short'] or '').strip()[:150]}",
                f"   search: https://www.imdb.com/find/?q={q}&s=tt", ""]

    # --- AI-CHECK: no cast on a platform that normally lists one. Anything already
    # ruled on, either way, stays out (build.py is_ai documents the tri-state).
    check = []
    for t in uncredited:
        if ai_flag(t):
            continue
        v, pid = best.get(t["title_id"], (0, ""))
        if pid in CAST_BEARING:
            check.append((v, pid, t))
    check.sort(key=lambda r: -r[0])

    yes = sorted(t["primary_title"] for t in titles if ai_flag(t) in ("yes", "y", "true", "1"))
    no = sorted(t["primary_title"] for t in titles if ai_flag(t) == "no")

    out2 = ["# AI-CHECK candidates", ""]
    out2 += ['Titles with NO cast on a platform that normally lists one. That is a CLUE, not proof:',
             'of the first three checked, two were AI and one (Love at Dangerous Speeds) was live-action.',
             "",
             'Open each poster. ReelShort stamps an "Ai GENERATE" badge top-right on AI titles.',
             "Tell me which ones have it and I will set ai=yes; tell me the clean ones and I will",
             "set ai=no, which keeps them off this list for good.", ""]
    out2 += [f"{len(check)} to check."]
    out2 += [f"Already confirmed AI ({len(yes)}): {', '.join(yes) if yes else 'none'}."]
    out2 += [f"Already confirmed NOT AI ({len(no)}): {', '.join(no) if no else 'none'}.", ""]
    for i, (v, pid, t) in enumerate(check, 1):
        out2 += [f"{i}. {t['primary_title']}",
                 f"   {plat_name.get(pid, pid)}   views: {views_label(v)}",
                 f"   poster: {(t['poster_ref'] or '').strip() or '(none on file)'}", ""]

    for path, body in (("CAST-WANTED.md", out), ("AI-CHECK.md", out2)):
        if args.dry_run:
            print(f"[dry-run] {path}: {len(body)} lines")
            continue
        with open(os.path.join(REPO, path), "w", encoding="utf-8") as f:
            f.write("\n".join(body).rstrip() + "\n")
    print(f"CAST-WANTED.md: {len(wanted)} of {len(uncredited)} uncredited titles")
    print(f"AI-CHECK.md   : {len(check)} to check, {len(yes)} confirmed AI, {len(no)} confirmed not")


if __name__ == "__main__":
    main()
