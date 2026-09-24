#!/usr/bin/env python3
"""Fold English-dub listings into their original's page, and mark the rest as dubs.

    python3 generator/merge_dubs.py            dry run: print what would change
    python3 generator/merge_dubs.py --apply    write data/ and _redirects

Born 24 Sep 2026. Platforms list a dub as its own show: GoodShort's "[ENG DUB] X",
NetShort's "(Dubbed) X", PineDrama's "[Dubbed Version] X". The site gave each
its own page, so 222 GoodShort shows had two near-identical pages, and nothing
marked a dub as a dub, so the Browse origin filter could not find them. Cyan,
24 Sep: one page per show, and dubs findable in Browse and its filter.

What it does:
  PAIRED   a dub whose name, stripped of the marker, matches another title is
           folded into that title. Its availability rows move across with
           version=english-dub (a second GoodShort row is the point here, so
           unlike merge_title.py it never drops a same-platform row), credits
           and tropes merge, the dub's name joins alt_titles (so searching
           "eng dub" finds the page), empty fields on the original are filled
           from the dub, the dub row is removed and its URL 301s to the original.
  ALONE    a dub with no original on file keeps its page; its availability rows
           get version=english-dub so the Dubbed filter finds it.

availability.csv gains a `version` column if it lacks one ('' = original).
Safe to re-run: a finished pair is gone, an ALONE row is already marked.
"""
import argparse, csv, io, os, re, unicodedata
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
DATA = os.path.join(REPO, "data")
DUB = "english-dub"
MARKER = re.compile(r"^\s*(\[\s*eng\s*dub\s*\]|\(\s*dubbed\s*\)|\[\s*dubbed version\s*\])\s*", re.I)


def term_of(p):
    raw = open(p, "rb").read()
    c = raw.count(b"\r\n")
    return "\r\n" if c > raw.count(b"\n") - c else "\n"


def load(n):
    with open(os.path.join(DATA, n), newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        return list(r), list(r.fieldnames)


def save(n, fields, recs):
    p = os.path.join(DATA, n)
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=fields, lineterminator=term_of(p))
    w.writeheader()
    w.writerows(recs)
    open(p, "w", newline="", encoding="utf-8").write(buf.getvalue())


def fold(s):
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c)).lower()
    return re.sub(r"[^a-z0-9]", "", s.replace("�", ""))


def uniq(xs):
    seen, out = set(), []
    for x in xs:
        x = x.strip()
        if x and x.lower() not in seen:
            seen.add(x.lower()); out.append(x)
    return out


def main(apply):
    titles, tf = load("titles.csv")
    avail, af = load("availability.csv")
    credits, cf = load("credits.csv")
    snaps, sf = load("snapshots.csv")
    pinned, pf = load("pinned.csv")
    picks, kf = load("picks.csv")
    trope_rows, trf = load("tropes.csv")
    if "version" not in af:
        af.append("version")
        for a in avail: a["version"] = ""

    dubs = [t for t in titles if MARKER.match(t["primary_title"])]
    originals = defaultdict(list)
    for t in titles:
        if not MARKER.match(t["primary_title"]):
            originals[fold(t["primary_title"])].append(t)

    pairs, alone, ambiguous = [], [], []
    for d in dubs:
        base = originals.get(fold(MARKER.sub("", d["primary_title"])), [])
        if len(base) == 1: pairs.append((base[0], d))
        elif len(base) > 1: ambiguous.append((d, base))
        else: alone.append(d)

    av_by = defaultdict(list)
    for a in avail: av_by[a["title_id"]].append(a)
    gone, redirects = set(), []
    for keep, d in pairs:
        kid, did = keep["title_id"], d["title_id"]
        for a in av_by[did]:
            a["title_id"], a["version"] = kid, DUB
        have = {(c["person_id"], (c.get("role") or "").lower()) for c in credits if c["title_id"] == kid}
        for c in credits:
            if c["title_id"] == did:
                c["title_id"] = kid
                if (c["person_id"], (c.get("role") or "").lower()) in have: c["_drop"] = 1
        keep["tropes"] = ";".join(uniq((keep.get("tropes") or "").split(";") + (d.get("tropes") or "").split(";")))
        keep["alt_titles"] = ";".join(x for x in uniq((keep.get("alt_titles") or "").split(";")
                                      + [d["primary_title"]] + (d.get("alt_titles") or "").split(";"))
                                      if x != keep["primary_title"])
        keep["source_urls"] = ";".join(uniq((keep.get("source_urls") or "").split(";") + (d.get("source_urls") or "").split(";")))
        for f in ("synopsis_short", "poster_ref", "year", "episode_count", "genres", "status", "book", "imdb_id"):
            if not (keep.get(f) or "").strip() and (d.get(f) or "").strip():
                keep[f] = d[f]
        for r in pinned + picks:
            if r["title_id"] == did: r["title_id"] = kid
        gone.add(did)
        for src in (f"/titles/{d['slug']}.html", f"/titles/{d['slug']}"):
            redirects.append(f"{src}  /titles/{keep['slug']}.html  301")
    for d in alone:
        for a in av_by[d["title_id"]]:
            a["version"] = DUB

    print(f"dub listings: {len(dubs)}  paired with an original: {len(pairs)}  "
          f"alone (marked as dubs): {len(alone)}  ambiguous (left alone): {len(ambiguous)}")
    for keep, d in pairs[:5]:
        print(f"  {d['slug']}  ->  {keep['slug']}")
    for d, base in ambiguous:
        print(f"  AMBIGUOUS {d['slug']}: {[b['slug'] for b in base]}")
    if not apply:
        print("[dry run] nothing written"); return

    titles = [t for t in titles if t["title_id"] not in gone]
    credits = [c for c in credits if not c.pop("_drop", None)]
    pinned = list({(r["title_id"], r.get("rail", "")): r for r in pinned}.values())
    snaps = [s for s in snaps if s["title_id"] not in gone]   # a dub's own trend would muddle the original's
    tcount = Counter()
    for t in titles:
        for x in {x.strip().lower() for x in (t.get("tropes") or "").split(";") if x.strip()}:
            tcount[x] += 1
    for tr in trope_rows:
        tr["title_count"] = str(tcount.get((tr.get("name") or "").lower(), 0))
    save("titles.csv", tf, titles); save("availability.csv", af, avail); save("credits.csv", cf, credits)
    save("snapshots.csv", sf, snaps); save("pinned.csv", pf, pinned); save("picks.csv", kf, picks)
    save("tropes.csv", trf, trope_rows)

    p = os.path.join(REPO, "_redirects")
    lines = open(p, encoding="utf-8").read().split("\n")
    new = [r for r in redirects if r not in lines]
    if new:
        at = next((i for i, l in enumerate(lines) if l.startswith("# Extensionless root pages")), len(lines))
        while at > 0 and not lines[at - 1].strip(): at -= 1
        block = ["", "# English dubs folded into their original's page (merge_dubs.py)."] if not any(
            "merge_dubs.py" in l for l in lines) else []
        lines[at:at] = block + new
        open(p, "w", encoding="utf-8").write("\n".join(lines).rstrip("\n") + "\n")
    print(f"applied: {len(gone)} dub rows folded, {len(new)} redirects written")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    main(ap.parse_args().apply)
