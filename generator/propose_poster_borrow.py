#!/usr/bin/env python3
"""Propose cross-platform poster borrows. PROPOSE ONLY, never writes.

The poster gap lives on platforms we cannot reach (DramaWave, ShortMax,
DramaBox, DramaPops, Shortical): app-only or bot-walled, so harvest_posters.py
cannot pull their og:image. But vertical dramas are heavily cross-listed and
the poster art is usually the same across platforms. So for a poster-less title
we look for the SAME title on a platform we DO have art for, and propose
borrowing that poster_ref.

This never touches titles.csv. It writes a proposal file for Cyan to rule on,
exactly like match_queue: a borrow is applied only after she confirms, because
a shared title string is not proof of the same show (generic names like "The
Arrangement" recur across unrelated dramas).

Match tiers, most confident first:
  exact      normalized title (hyphenless) identical, and the name is not generic
  article    identical after dropping a leading The/A/An
  generic    exact normalized match but the title is short or a known generic
             phrase, so it needs a human eye on the art itself

Usage:
    python3 propose_poster_borrow.py [--out <path>] [--min-views N]
"""
import csv, os, re, io, sys, json, argparse, unicodedata, datetime
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
csv.field_size_limit(10**7)

# Platforms we cannot reach for og:image (the poster gap). A poster-less title
# on any of these is a borrow candidate.
UNREACHABLE = {"dramawave", "shortmax", "dramabox", "dramapops", "shortical",
               "dreameshort", "flickreels", "idrama", "mymuse"}

# Generic title phrases: an exact name match here is weak evidence of same show.
GENERIC = {"the arrangement", "the glow up", "next door", "scandalous",
           "vicious", "breathe", "mason", "the words", "waterboy", "just one kiss"}


def norm(s):
    s = unicodedata.normalize("NFKD", s or "").replace("’", "'")
    s = re.sub(r"[^a-z0-9]+", " ", s.lower())
    return re.sub(r"\s+", " ", s).strip()


def nohyph(s):
    return norm(s).replace(" ", "")


def dearticle(s):
    return re.sub(r"^(the|a|an) ", "", norm(s)).strip()


def to_num(v):
    v = (v or "").strip().upper().replace(",", "")
    try:
        if v.endswith("M"):
            return float(v[:-1]) * 1e6
        if v.endswith("K"):
            return float(v[:-1]) * 1e3
        return float(v or 0)
    except ValueError:
        return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(HERE, "staging",
                    "poster_borrow_proposals_%s.json" % datetime.date.today()))
    ap.add_argument("--min-views", type=int, default=0,
                    help="only propose for target titles at or above this reach")
    args = ap.parse_args()

    titles = list(csv.DictReader(open(os.path.join(DATA, "titles.csv"))))
    by_id = {t["title_id"]: t for t in titles}
    avail = list(csv.DictReader(open(os.path.join(DATA, "availability.csv"))))
    plats = defaultdict(set)
    views = defaultdict(float)
    for a in avail:
        plats[a["title_id"]].add(a["platform_id"])
        views[a["title_id"]] = max(views[a["title_id"]], to_num(a.get("view_count")))

    def has_poster(t):
        return bool((t.get("poster_ref") or "").strip())

    # SOURCE pool: titles WITH a poster. Index every name string they carry.
    src_exact = defaultdict(list)   # nohyph(name) -> [title_id, ...]
    for t in titles:
        if not has_poster(t):
            continue
        names = [t["primary_title"]] + [x.strip() for x in (t.get("alt_titles") or "").split("|") if x.strip()]
        for nm in names:
            k = nohyph(nm)
            if k:
                src_exact[k].append(t["title_id"])

    # TARGET pool: poster-less titles on an unreachable platform.
    proposals = []
    for t in titles:
        if has_poster(t):
            continue
        tps = plats.get(t["title_id"], set())
        if not (tps & UNREACHABLE):
            continue
        if views[t["title_id"]] < args.min_views:
            continue
        cand_ids, tier = [], None
        k = nohyph(t["primary_title"])
        hits = [s for s in src_exact.get(k, []) if s != t["title_id"]]
        if hits:
            tier = "generic" if norm(t["primary_title"]) in GENERIC or len(k) <= 6 else "exact"
            cand_ids = hits
        else:
            # article-only difference: compare de-articled forms
            da = dearticle(t["primary_title"])
            for s in titles:
                if s["title_id"] == t["title_id"] or not has_poster(s):
                    continue
                if dearticle(s["primary_title"]) == da and da:
                    cand_ids.append(s["title_id"]); tier = "article"
        if not cand_ids:
            continue
        best = max(cand_ids, key=lambda sid: views[sid])
        src = by_id[best]
        proposals.append({
            "tier": tier,
            "target_slug": t["slug"],
            "target_title": t["primary_title"],
            "target_platforms": sorted(tps),
            "target_views": int(views[t["title_id"]]),
            "source_slug": src["slug"],
            "source_title": src["primary_title"],
            "source_platforms": sorted(plats.get(best, [])),
            "poster_ref": src["poster_ref"],
            "other_source_candidates": len(cand_ids) - 1,
        })

    order = {"exact": 0, "article": 1, "generic": 2}
    proposals.sort(key=lambda p: (order[p["tier"]], -p["target_views"]))
    doc = {
        "generated": str(datetime.date.today()),
        "policy": "PROPOSE ONLY. Nothing written to titles.csv. A borrow copies the "
                  "source poster_ref into the target after Cyan confirms same show. "
                  "Same title string is not proof; generic names need eyes on the art.",
        "count": len(proposals),
        "proposals": proposals,
    }
    io.open(args.out, "w", encoding="utf-8").write(json.dumps(doc, indent=1, ensure_ascii=False))
    tier_counts = defaultdict(int)
    for p in proposals:
        tier_counts[p["tier"]] += 1
    print("poster-borrow proposals: %d  %s" % (len(proposals), dict(tier_counts)))
    print("written: %s" % args.out)
    for p in proposals[:40]:
        print("  [%s] %-42s (%s) <- %-42s (%s)" % (
            p["tier"], p["target_slug"][:42], ",".join(p["target_platforms"]),
            p["source_slug"][:42], ",".join(p["source_platforms"])))


if __name__ == "__main__":
    main()
