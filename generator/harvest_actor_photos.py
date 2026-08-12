#!/usr/bin/env python3
"""Fill photo_ref for the fan-panel actors from ReelShort's own CDN.

Why this exists: data/popular_actors.csv carries the 38 actors Reddit fans
picked out, and 33 of them have no photo. The Popular Actors rail renders those
as blank tiles. TMDB is ruled out (commercial licence, $149, and this site runs
affiliate links), so the proven route is the platform CDN: all 109 photo_ref
values already on file are v-mps.crazymaplestudios.com /actorIMG/ URLs.

THE ROUTE, re-derived 9 Aug because nothing in the repo recorded it. A ReelShort
movie page embeds an "actor_info" object in its payload:

    "actor_info": {"imdb_id": "", "imdb_url": "",
                   "actors": [{"actor_name": "Grace Swanson",
                               "actor_pic":  "https://v-mps.crazymaplestudios.com/actorIMG/...jpg",
                               "inside_url": "...", "outside_url": "https://www.imdb.com/name/nm12867081/"}]}

Verified against a title crediting an actor whose photo we already hold: the
parse returns exactly the URL on file. Note the array is SPARSE -- True Luna
lists one actor for a much larger cast -- so coverage per page is partial and a
miss is normal, not a parse failure.

Safety rules, from data/CONVENTIONS.md and the standing rules:
  - FILL-BLANK-ONLY. An actor who already has a photo_ref is never rewritten.
  - NEVER ATTACH A REAL PERSON'S NAME (or face) WITHOUT EVIDENCE. Names are
    matched EXACTLY, case-insensitively. A near-match is reported and skipped,
    never guessed -- a wrong headshot on a real actor's page is the same class
    of error as a wrong credit.
  - Images are verified by MAGIC BYTES, not Content-Type: two CDNs in this
    project serve perfectly good images as application/octet-stream.
  - Line endings preserved per file (people.csv is CRLF on disk).

ROUTE 1 IS EXHAUSTED FOR THESE 33, measured 9 Aug rather than assumed: across the
80 ReelShort pages crediting a fan-panel actor, actor_info yielded 46 distinct
names and EVERY ONE already had a photo on file. 25 of those 80 pages carry no
actor_info at all. So the array is a curated subset, the existing 109 photos are
exactly that subset, and none of the 33 are in it. That is why route 2 exists.

ROUTE 2, THE FANDOM BLOG. reelshort.com/fandom is a WordPress site that publishes
actor profile pieces with headshots at /fandom/wp-content/uploads/YYYY/MM/. Its
REST search at /fandom/wp-json/wp/v2/search is open and returns structured hits.

THE SEARCH IS FUZZY AND WILL HAND YOU THE WRONG PERSON. Querying 'Ben Taylor'
returns an article about BEN ARMSTRONG. Attaching that headshot to Ben Taylor
would be exactly the false attribution the standing rules forbid, so a hit is
only taken when BOTH of these hold:
  - the article's URL slug contains the actor's full name slug, and
  - the image's own filename contains that same full name slug.
A name that only appears in an article's body is never enough.

Scope: by default this writes ONLY the actors listed in popular_actors.csv, which
is the task in hand. Pages are fetched per title, so photos for other actors turn
up incidentally; they are counted and reported, and --all opts into writing them.

Usage:
    py harvest_actor_photos.py --dry-run
    py harvest_actor_photos.py [--all] [--limit N] [--workers N] [--no-fandom]
"""
import argparse
import csv
import collections
import io
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "data")
STAGING = os.path.join(HERE, "staging")
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")
PLATFORM = "reelshort"
SOURCE = "reelshort_cdn_" + time.strftime("%Y-%m-%d")
TIMEOUT = 30

ACTOR_INFO_RE = re.compile(r'"actor_info"\s*:\s*(\{.*?"actors"\s*:\s*\[.*?\]\s*\})', re.S)
# Magic bytes for the formats a poster/headshot CDN plausibly serves.
MAGIC = {
    b"\xff\xd8\xff": "jpeg",
    b"\x89PNG\r\n\x1a\n": "png",
    b"GIF87a": "gif",
    b"GIF89a": "gif",
}


def rows(name):
    with open(os.path.join(DATA, name), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def term_of(name):
    raw = open(os.path.join(DATA, name), "rb").read()
    crlf = raw.count(b"\r\n")
    return "\r\n" if crlf > raw.count(b"\n") - crlf else "\n"


def write_csv(name, fieldnames, records):
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=fieldnames, lineterminator=term_of(name))
    w.writeheader()
    w.writerows(records)
    with open(os.path.join(DATA, name), "w", newline="", encoding="utf-8") as f:
        f.write(buf.getvalue())


def fetch(url, tries=3, binary=False, cap=None, pace=0.0):
    """Fetch with retries.

    An EMPTY 200 body counts as a failure, not as content. The fandom host soft
    blocks under load by returning 200 with nothing in it, and treating that as
    a real response made 33 actors report 'search response unparseable' when the
    truth was simply that we had knocked too hard.
    """
    last = None
    for i in range(tries):
        try:
            if pace:
                time.sleep(pace)
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                data = r.read(cap) if cap else r.read()
            if not data:
                last = "empty body (soft block?)"
                if i + 1 < tries:
                    time.sleep(5.0 * (i + 1))
                continue
            return (data if binary else data.decode("utf-8", "ignore")), None
        except Exception as e:
            last = e
            if i + 1 < tries:
                time.sleep(1.5 * (i + 1))
    return None, repr(last)


CACHE = os.path.join(STAGING, ".fandom_cache")


def cached_fetch(url, **kw):
    """Disk-cache fandom reads so a rerun costs the host nothing."""
    os.makedirs(CACHE, exist_ok=True)
    key = re.sub(r"[^A-Za-z0-9]+", "_", url)[-120:] + ".txt"
    path = os.path.join(CACHE, key)
    if os.path.exists(path):
        body = open(path, encoding="utf-8").read()
        if body:
            return body, None
    body, err = fetch(url, **kw)
    if body:
        with open(path, "w", encoding="utf-8") as f:
            f.write(body)
    return body, err


def actors_on(html):
    """Return [(actor_name, actor_pic, imdb_url)] from a ReelShort movie page."""
    out = []
    for blob in ACTOR_INFO_RE.findall(html or ""):
        try:
            info = json.loads(blob)
        except Exception:
            continue
        for a in info.get("actors") or []:
            nm = (a.get("actor_name") or "").strip()
            pic = (a.get("actor_pic") or "").strip()
            if nm and pic.startswith("http"):
                out.append((nm, pic, (a.get("outside_url") or "").strip()))
    return out


def name_slug(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


FANDOM_SEARCH = "https://www.reelshort.com/fandom/wp-json/wp/v2/search?search={}&per_page=10"
UPLOAD_RE = re.compile(
    r'https://www\.reelshort\.com/fandom/wp-content/uploads/[^"\'\\ )]+?'
    r'\.(?:jpg|jpeg|png|webp)', re.I)
# WordPress emits resized copies as name-300x200.jpg alongside the original.
SIZED_RE = re.compile(r'-\d{2,4}x\d{2,4}(?=\.[a-z]+$)', re.I)


def fandom_photo(name):
    """Find a headshot on the fandom blog, or return (None, why-not).

    Evidence bar: the article slug AND the image filename must both contain the
    actor's full name slug. Anything weaker is refused.
    """
    slug = name_slug(name)
    body, err = cached_fetch(FANDOM_SEARCH.format(urllib.parse.quote(name)),
                             tries=4, pace=2.0)
    if body is None:
        return None, f"search failed: {err[:60]}"
    try:
        results = json.loads(body)
    except Exception:
        return None, "search response unparseable"
    if not results:
        return None, "no fandom article"

    articles = [r for r in results if slug in (r.get("url") or "").lower()]
    if not articles:
        titles_seen = "; ".join((r.get("title") or "")[:40] for r in results[:2])
        return None, f"no article slug matches the name (saw: {titles_seen})"

    for art in articles:
        html, err = cached_fetch(art["url"], tries=3, pace=2.0)
        if html is None:
            continue
        solo, shared = [], []
        for u in dict.fromkeys(UPLOAD_RE.findall(html)):
            fname = u.rsplit("/", 1)[-1].lower()
            stem = SIZED_RE.sub("", fname.rsplit(".", 1)[0])
            if stem == slug:
                solo.append(u)
            elif slug in stem:
                # e.g. jarred-harper-and-meg-bush.jpg: the actor IS in it, but so
                # is someone else, and an avatar tile cannot say which face is
                # which. Never auto-pick one; hand it back for a human call.
                shared.append(u)
        if solo:
            originals = [u for u in solo if not SIZED_RE.search(u)]
            return (originals or solo)[0], art["url"]
        if shared:
            return None, ("only a shared photo, needs a human call: "
                          + shared[0].rsplit("/", 1)[-1])
    return None, "article found but no image filename carries the name"


def is_image(url):
    """Confirm by magic bytes. Content-Type is not trusted on these CDNs."""
    data, err = fetch(url, tries=2, binary=True, cap=16)
    if data is None:
        return False, err
    for sig in MAGIC:
        if data.startswith(sig):
            return True, MAGIC[sig]
    return False, f"not an image (starts {data[:8]!r})"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true",
                    help="also write photos for actors outside popular_actors.csv")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--no-fandom", action="store_true",
                    help="skip the fandom-blog fallback route")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    people = rows("people.csv")
    by_id = {p["person_id"]: p for p in people}
    by_name = {}
    for p in people:
        by_name.setdefault(p["name"].strip().lower(), p)

    popular = {r["person_id"] for r in rows("popular_actors.csv")}
    wanted = {pid for pid in popular
              if pid in by_id and not by_id[pid]["photo_ref"].strip()}
    print(f"{len(popular)} fan-panel actors, {len(wanted)} of them with no photo_ref")

    titles = {t["title_id"]: t for t in rows("titles.csv")}
    links = {}
    for a in rows("availability.csv"):
        if a["platform_id"] == PLATFORM and (a.get("direct_link") or "").startswith("http"):
            links.setdefault(a["title_id"], a["direct_link"])

    by_person = collections.defaultdict(list)
    for c in rows("credits.csv"):
        if c["title_id"] in links:
            by_person[c["person_id"]].append(c["title_id"])

    # Fetch every ReelShort page that credits a target. The actor_info array is
    # sparse, so one actor may need several of their titles tried.
    pages, reasons = {}, {}
    for pid in sorted(wanted):
        tids = by_person.get(pid, [])
        if not tids:
            reasons[pid] = "no ReelShort title with a direct_link credits them"
            continue
        for t in tids:
            pages[t] = links[t]
    if args.limit:
        pages = dict(list(pages.items())[:args.limit])

    print(f"{len(pages)} ReelShort pages to read")
    for pid, why in reasons.items():
        print(f"   unreachable: {by_id[pid]['name']:28} {why}")

    def work(item):
        tid, url = item
        html, err = fetch(url)
        return tid, (actors_on(html) if html else []), err

    found = {}        # person_id -> (name, pic, imdb_url, tid)
    seen_names = collections.Counter()
    page_fail = []
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        for i, (tid, actors, err) in enumerate(ex.map(work, pages.items()), 1):
            if err:
                page_fail.append((tid, err))
            for nm, pic, imdb in actors:
                seen_names[nm] += 1
                person = by_name.get(nm.lower())
                if person is None:
                    continue
                if person["photo_ref"].strip():
                    continue
                found.setdefault(person["person_id"], (nm, pic, imdb, tid))
            if i % 20 == 0:
                print(f"  {i}/{len(pages)}  matched so far: {len(found)}", flush=True)

    # ---- route 2: fandom blog, for the targets actor_info did not cover.
    fandom_notes = {}
    if not args.no_fandom:
        missing = sorted(pid for pid in wanted if pid not in found)
        print(f"\nroute 2: {len(missing)} fan-panel actors not in actor_info, "
              f"trying the fandom blog")

        def fandom_work(pid):
            nm = by_id[pid]["name"]
            pic, note = fandom_photo(nm)
            return pid, nm, pic, note

        for pid, nm, pic, note in map(fandom_work, missing):
                if pic:
                    found[pid] = (nm, pic, "", note)   # note holds the article url
                    print(f"   FOUND {nm:28} {pic.rsplit('/', 1)[-1][:60]}")
                else:
                    fandom_notes[pid] = note
                    print(f"   none  {nm:28} {note[:80]}")

    targets = {pid: v for pid, v in found.items() if pid in wanted}
    extras = {pid: v for pid, v in found.items() if pid not in wanted}
    print(f"\ndistinct actor_info names seen: {len(seen_names)}")
    print(f"page fetch failures:            {len(page_fail)}")
    print(f"fan-panel actors matched:       {len(targets)}/{len(wanted)}")
    print(f"other photoless actors matched: {len(extras)}"
          f"{' (will be written, --all)' if args.all else ' (not written; pass --all)'}")

    write_set = dict(found) if args.all else dict(targets)

    # Verify every image before it goes anywhere near people.csv.
    print(f"\nverifying {len(write_set)} images by magic bytes...")
    verified, rejected = {}, []
    def check(item):
        pid, (nm, pic, imdb, tid) = item
        ok, what = is_image(pic)
        return pid, nm, pic, imdb, tid, ok, what
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        for pid, nm, pic, imdb, tid, ok, what in ex.map(check, write_set.items()):
            if ok:
                verified[pid] = (nm, pic, imdb, tid, what)
            else:
                rejected.append((nm, pic, what))
    print(f"  verified: {len(verified)}   rejected: {len(rejected)}")
    for nm, pic, what in rejected[:8]:
        print(f"   REJECT {nm:28} {what}  {pic}")

    still = sorted(by_id[p]["name"] for p in wanted if p not in verified)
    print(f"\nfan-panel actors still without a photo: {len(still)}")
    for n in still:
        print(f"   {n}")

    if args.dry_run:
        print("\nwould write:")
        for pid, (nm, pic, imdb, tid, kind) in sorted(verified.items()):
            print(f"   {nm:28} [{kind}] {pic}")
            src = (titles[tid]["primary_title"] if tid in titles else tid)
            print(f"   {'':28} from {src}" + (f"  imdb={imdb}" if imdb else ""))
        print("\n(dry run, nothing written)")
        return 0

    if not verified:
        print("\nnothing to write")
        return 0

    os.makedirs(STAGING, exist_ok=True)
    stage = os.path.join(STAGING, f"actor_photos_{time.strftime('%Y-%m-%d')}.json")
    with open(stage, "w", encoding="utf-8") as f:
        json.dump({
            "source": SOURCE,
            "platform": PLATFORM,
            "field": "photo_ref",
            "mode": "fill-blank-only",
            "read_from": "ReelShort movie page actor_info.actors[]",
            "photos": {pid: {"name": nm, "photo_ref": pic, "imdb_url": imdb,
                             "seen_on_title": tid, "image_type": kind}
                       for pid, (nm, pic, imdb, tid, kind) in sorted(verified.items())},
        }, f, ensure_ascii=False, indent=2)
    print(f"\nstaged -> {os.path.relpath(stage, os.path.dirname(HERE))}")

    written = 0
    for p in people:
        v = verified.get(p["person_id"])
        if v and not p["photo_ref"].strip():
            p["photo_ref"] = v[1]
            written += 1
    write_csv("people.csv", list(people[0].keys()), people)
    print(f"written: {written} photo_ref values into people.csv")

    # popular_actors.csv carries a has_photo flag that the rail build reads.
    pa = rows("popular_actors.csv")
    flipped = 0
    for r in pa:
        if r["person_id"] in verified and r["has_photo"].strip().lower() != "yes":
            r["has_photo"] = "yes"
            flipped += 1
    if flipped:
        write_csv("popular_actors.csv", list(pa[0].keys()), pa)
    print(f"popular_actors.csv has_photo flipped to yes: {flipped}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
