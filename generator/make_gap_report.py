#!/usr/bin/env python3
"""Generate Cyan's three PRIORITISED gap worklists, so manual effort goes to the
things visitors actually land on rather than to whatever is alphabetically first.

    ACTORS-PHOTOS.md       actors with no photo, most-seen first
    ACTORS-FILMOGRAPHY.md  actors whose IMDb page has never been read
    TITLES-INCOMPLETE.md   titles failing the 5-point bar, and WHICH field is missing

WHY THESE THREE. They are the three questions Cyan cannot answer by looking at the
site: which faces are missing, which filmographies are unread, and which entries are
one field short. Everything else in the repo tells you what we HAVE.

RANKING IS BY REACH, AND THE VIEW COUNT IS A TRAP. view_count in availability.csv is
a DISPLAY STRING - '218.1M', '1.2K' - and int() on it silently yields zero, which
would rank every actor at 0 and look merely uninteresting rather than broken. 2,340
of 2,374 populated rows are non-numeric. views() below parses the suffix; it is the
same helper make_worklists.py uses and it is not optional.

AN ACTOR'S REACH is the summed views of every title they are credited on. That
rewards being in several big titles over being in one viral one, which is the same
reasoning behind blending the Popular Actors rail rather than ranking on views alone.

A TITLE'S REACH is the best view count across its platforms, because a title on two
apps is one title to a visitor.

THE FAN-PANEL FLAG IS AN INDEPENDENT SIGNAL and is shown, not summed into the score.
Reddit panels reflect an actual following; view counts reward whoever happened to be
in one viral title. Where they disagree that is worth Cyan seeing, not averaging away.

Nothing here is consumed by the build. These files exist purely to direct manual
effort, so the only cost of being wrong is Cyan's time - which is the thing to guard.

Usage:
    python3 make_gap_report.py [--limit N] [--dry-run]
"""
import csv, os, re, argparse
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
REPO = os.path.dirname(HERE)


def rows(name):
    with open(os.path.join(DATA, name), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def views(s):
    """'132.3M' -> 132300000. Blank or unparseable -> 0."""
    m = re.match(r"^([\d.]+)\s*([KMB])?$", (s or "").strip().upper())
    if not m:
        return 0
    return int(float(m.group(1)) * {"K": 1e3, "M": 1e6, "B": 1e9, None: 1}[m.group(2)])


def label(n):
    if n >= 1e9:
        return f"{n / 1e9:.1f}B"
    if n >= 1e6:
        return f"{n / 1e6:.0f}M"
    if n >= 1e3:
        return f"{n / 1e3:.0f}K"
    return "-" if not n else str(n)


def imdb_of(person):
    """The nm id if we hold one. The standing rule is to record it even when the
    answer to a question was no, precisely so this lookup is possible."""
    m = re.search(r"(nm\d+)", person.get("socials") or "")
    return m.group(1) if m else ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=150)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    titles = rows("titles.csv")
    people = rows("people.csv")
    credits = rows("credits.csv")
    avail = rows("availability.csv")
    plats = {p["platform_id"]: p["name"] for p in rows("platforms.csv")}
    try:
        popular = {p["person_id"]: p for p in rows("popular_actors.csv")}
    except FileNotFoundError:
        popular = {}

    t_by_id = {t["title_id"]: t for t in titles}
    av = defaultdict(list)
    for a in avail:
        av[a["title_id"]].append(a)

    # A title's reach = its best view count across platforms.
    reach = {t["title_id"]: max([views(a.get("view_count")) for a in av[t["title_id"]]] or [0])
             for t in titles}

    # ---- actor aggregates -------------------------------------------------
    cast_n = defaultdict(int)
    for c in credits:
        cast_n[c["title_id"]] += 1

    a_titles = defaultdict(list)
    for c in credits:
        a_titles[c["person_id"]].append(c["title_id"])

    a_reach = {pid: sum(reach.get(t, 0) for t in set(ts)) for pid, ts in a_titles.items()}

    # Which filmographies have already been read? The staged per-actor files are the
    # record - a staging JSON stays in the repo after it is applied, so it is proof
    # the page was read, not proof of pending work.
    read = set()
    stage = os.path.join(HERE, "staging", "drive_2026-08-09")
    if os.path.isdir(stage):
        for f in os.listdir(stage):
            if f.startswith("actor__") and f.endswith(".json"):
                read.add(f[len("actor__"):-len(".json")])

    # ---- 1. actors needing a photo ----------------------------------------
    no_photo = [p for p in people if not (p.get("photo_ref") or "").strip()
                and a_titles.get(p["person_id"])]
    no_photo.sort(key=lambda p: (-a_reach.get(p["person_id"], 0),
                                 -len(set(a_titles[p["person_id"]])), p["name"]))

    L1 = ["# Actors who need a photo",
          "",
          f"{len(no_photo)} credited actors have no photo_ref. Ranked by REACH - the summed",
          "views of every title they are credited on - so the faces a visitor is most likely",
          "to meet come first. Regenerate with `py generator/make_gap_report.py`.",
          "",
          "Sources that are known to work, in order: the ReelShort fandom blog, Wikimedia",
          "Commons, then the platform's own actor page. NEVER a shared photo - a file named",
          "`x-and-y.jpg` shows two people and a 78px avatar cannot say which is which.",
          "",
          "| # | Actor | Reach | Titles | Fan panel | IMDb | Page |",
          "|--:|-------|------:|-------:|-----------|------|------|"]
    for i, p in enumerate(no_photo[:args.limit], 1):
        pid = p["person_id"]
        fan = popular.get(pid, {}).get("panel", "")
        nm = imdb_of(p)
        L1.append(f"| {i} | {p['name']} | {label(a_reach.get(pid, 0))} | "
                  f"{len(set(a_titles[pid]))} | {fan or '-'} | "
                  f"{'https://www.imdb.com/name/' + nm + '/' if nm else '-'} | "
                  f"/actors/{p['slug']}.html |")

    # ---- 2. actors whose filmography has never been read -------------------
    unread = [p for p in people
              if p["person_id"] not in read and a_titles.get(p["person_id"])]
    unread.sort(key=lambda p: (-a_reach.get(p["person_id"], 0),
                               -len(set(a_titles[p["person_id"]])), p["name"]))

    L2 = ["# Actors whose IMDb filmography has never been read",
          "",
          f"{len(unread)} of {len(people)} credited actors. {len(read)} have been read.",
          "",
          "WHY THIS IS THE HIGHEST-VALUE LIST. Measured 13 Aug across the 28 actors already",
          "read: IMDb credits them on 810 titles and we hold 476, so even a read actor is",
          "only 59% complete - and before the import it was 37%. The gap is NOT cast data,",
          "it is titles that do not exist in titles.csv. One saved IMDb page per actor is",
          "the only thing that closes it, and it is the one job only Cyan can do.",
          "",
          "HOW TO SAVE ONE: print the actor's IMDb page to PDF, keep the platform name in",
          "the filename if you know it, and Downloads is fine - Drive is not required.",
          "",
          "| # | Actor | Reach | Titles held | Fan panel | IMDb |",
          "|--:|-------|------:|------------:|-----------|------|"]
    for i, p in enumerate(unread[:args.limit], 1):
        pid = p["person_id"]
        nm = imdb_of(p)
        fan = popular.get(pid, {}).get("panel", "")
        L2.append(f"| {i} | {p['name']} | {label(a_reach.get(pid, 0))} | "
                  f"{len(set(a_titles[pid]))} | {fan or '-'} | "
                  f"{'https://www.imdb.com/name/' + nm + '/' if nm else 'search by name'} |")

    # ---- 3. titles failing the 5-point bar --------------------------------
    # Same five criteria as completeness.py. Kept in step with it by hand; if that
    # file's definition moves, this one has to move with it.
    gaps = []
    for t in titles:
        tid = t["title_id"]
        ra = av.get(tid, [])
        if not ra:
            continue                                   # no platform: a different problem
        syn = (t.get("synopsis_short") or "").strip()
        truncated = len(syn) == 300 or len(syn.encode("utf-8")) == 300
        miss = []
        if cast_n[tid] < 2:
            miss.append("cast")
        if not any((a.get("direct_link") or "").strip() for a in ra):
            miss.append("link")
        if not syn:
            miss.append("caption")
        elif truncated:
            miss.append("caption(copied)")
        elif len(syn) < 40:
            miss.append("caption(thin)")
        if not (t.get("tropes") or "").strip():
            miss.append("trope")
        if miss:
            gaps.append((reach.get(tid, 0), t, miss,
                         ", ".join(sorted({plats.get(a["platform_id"], a["platform_id"])
                                           for a in ra}))))
    gaps.sort(key=lambda g: (-g[0], g[1]["primary_title"]))

    one_short = [g for g in gaps if len(g[2]) == 1]
    L3 = ["# Titles that fail the 5-point quality bar",
          "",
          "The bar (Cyan, 13 Aug): a title, a caption WE wrote, at least the leads,",
          "a link to the platform, and at least one trope.",
          "",
          f"{len(gaps)} titles fail on at least one field. {len(one_short)} fail on ONE field",
          "only - those are the cheapest wins and they are listed first below.",
          "",
          "`caption(copied)` means the text is exactly 300 characters or 300 bytes, which is",
          "a scraper truncation - it is the platform's text, not ours, so it fails on",
          "copyright and on duplicate-content grounds both.",
          "",
          "## One field short",
          "",
          "| # | Title | Reach | Missing | Platform |",
          "|--:|-------|------:|---------|----------|"]
    for i, (r, t, miss, pl) in enumerate(one_short[:args.limit], 1):
        L3.append(f"| {i} | {t['primary_title']} | {label(r)} | {miss[0]} | {pl} |")

    L3 += ["", "## Two or more fields short", "",
           "| # | Title | Reach | Missing | Platform |",
           "|--:|-------|------:|---------|----------|"]
    for i, (r, t, miss, pl) in enumerate([g for g in gaps if len(g[2]) > 1][:args.limit], 1):
        L3.append(f"| {i} | {t['primary_title']} | {label(r)} | {', '.join(miss)} | {pl} |")

    out = (("ACTORS-PHOTOS.md", L1), ("ACTORS-FILMOGRAPHY.md", L2), ("TITLES-INCOMPLETE.md", L3))
    for path, body in out:
        if args.dry_run:
            print(f"[dry-run] {path}: {len(body)} lines")
            continue
        with open(os.path.join(REPO, path), "w", encoding="utf-8") as f:
            f.write("\n".join(body).rstrip() + "\n")

    print(f"ACTORS-PHOTOS.md      : {len(no_photo)} actors with no photo (showing {min(args.limit, len(no_photo))})")
    print(f"ACTORS-FILMOGRAPHY.md : {len(unread)} unread of {len(people)} ({len(read)} read)")
    print(f"TITLES-INCOMPLETE.md  : {len(gaps)} failing, {len(one_short)} of them one field short")


if __name__ == "__main__":
    main()
