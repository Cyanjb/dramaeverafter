#!/usr/bin/env python3
"""Harvest cast lists from Vigloo content pages into credits.csv.

Recovers a method that was used on 2026-07-20 (369 people carry source
vigloo_2026-07-20) but was never written down: adapters.md has no Vigloo section.

WHERE THE CAST LIVES: Vigloo ships a schema.org TVSeries block in a
<script type="application/ld+json"> tag, and that block carries an "actor" array:

    "actor":[{"@type":"Person","name":"Jung Jaebin"}, ...]

This is easy to miss. Fetching the page through a summarising tool reports "no cast
anywhere on this page", because converting the page to text throws the JSON-LD away.
Always read the RAW html for structured data.

Names arrive display-formatted, so no camelCase expansion is needed (unlike My Drama).

Safety, per data/CONVENTIONS.md:
  - exact name match reuses the existing person
  - near-match (identical ignoring separators, or ~1 character apart) goes to
    match_queue and is NOT credited
  - new people enter as data_confidence=needs_check with a dated source
  - existing credits are never duplicated; per-file line endings preserved

Usage:
    python3 harvest_vigloo_cast.py [--limit N] [--dry-run]
"""
import csv, io, os, re, sys, time, json, argparse, difflib
from concurrent.futures import ThreadPoolExecutor
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "data")
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")
PLATFORM = "vigloo"
SOURCE = "vigloo_cast_" + time.strftime("%Y-%m-%d")
WORKERS = 5
TIMEOUT = 30
LD = re.compile(r'<script[^>]+application/ld\+json[^>]*>(.*?)</script>', re.S | re.I)
ACTOR_FALLBACK = re.compile(r'"actors?"\s*:\s*\[(.*?)\]', re.S | re.I)
NAME_IN = re.compile(r'"name"\s*:\s*"([^"]{2,60})"')


def rows(name):
    with open(os.path.join(DATA, name), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def term_of(path):
    raw = open(path, "rb").read()
    crlf = raw.count(b"\r\n")
    return "\r\n" if crlf > raw.count(b"\n") - crlf else "\n"

def save(name, fields, recs):
    p = os.path.join(DATA, name)
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=fields, lineterminator=term_of(p))
    w.writeheader(); w.writerows(recs)
    with open(p, "w", newline="", encoding="utf-8") as f:
        f.write(buf.getvalue())

def slug(s): return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
def loose(s): return re.sub(r"[^a-z0-9]", "", s.lower())

def fetch(url, tries=2):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html"})
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                return r.read().decode("utf-8", "ignore")
        except Exception:
            if i + 1 < tries:
                time.sleep(1.5)
    return None

def cast_from(html):
    """Prefer real JSON parsing of the ld+json block; fall back to a regex sweep."""
    if not html:
        return []
    out, seen = [], set()
    for block in LD.findall(html):
        try:
            data = json.loads(block.strip())
        except Exception:
            continue
        for node in (data if isinstance(data, list) else [data]):
            if not isinstance(node, dict):
                continue
            actors = node.get("actor") or node.get("actors") or []
            if isinstance(actors, dict):
                actors = [actors]
            for a in actors:
                nm = (a.get("name") if isinstance(a, dict) else a) or ""
                nm = " ".join(str(nm).split())
                if 3 <= len(nm) <= 60 and nm.lower() not in seen:
                    seen.add(nm.lower()); out.append(nm)
    if not out:
        m = ACTOR_FALLBACK.search(html)
        if m:
            for nm in NAME_IN.findall(m.group(1)):
                nm = " ".join(nm.split())
                if 3 <= len(nm) <= 60 and nm.lower() not in seen:
                    seen.add(nm.lower()); out.append(nm)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    titles = {t["title_id"]: t for t in rows("titles.csv")}
    people, credits, queue = rows("people.csv"), rows("credits.csv"), rows("match_queue.csv")
    by_name = {p["name"].strip().lower(): p for p in people}
    by_loose = {}
    for p in people: by_loose.setdefault(loose(p["name"]), p)
    have_credit = {(c["title_id"], c["person_id"]) for c in credits}
    queued = {(q["candidate_a"], q["candidate_b"]) for q in queue}
    existing_ids = {p["person_id"] for p in people}
    credited = {c["title_id"] for c in credits}

    targets, seen_t = [], set()
    for a in rows("availability.csv"):
        if a["platform_id"] != PLATFORM: continue
        link = (a.get("direct_link") or "").strip()
        tid = a["title_id"]
        # Only titles we have no cast for at all.
        if link.startswith("http") and tid in titles and tid not in credited and tid not in seen_t:
            seen_t.add(tid); targets.append((tid, link))
    if args.limit: targets = targets[:args.limit]
    print(f"{len(targets)} Vigloo titles without cast to check")

    def work(item):
        tid, url = item
        return tid, cast_from(fetch(url))

    results = []
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        for i, r in enumerate(ex.map(work, targets), 1):
            results.append(r)
            if i % 20 == 0:
                print(f"  {i}/{len(targets)}  with cast: {sum(1 for _t,n in results if n)}", flush=True)

    new_credits, new_people, to_queue = [], [], []
    matched = created = 0
    for tid, names in results:
        for order, nm in enumerate(names):
            key = nm.strip().lower()
            person = by_name.get(key)
            if person is None:
                near = by_loose.get(loose(nm))
                if near is None:
                    close = difflib.get_close_matches(loose(nm), by_loose.keys(), n=1, cutoff=0.92)
                    if close: near = by_loose[close[0]]
                if near is not None and near["name"].strip().lower() != key:
                    pair = (near["person_id"], slug(nm))
                    if pair not in queued:
                        queued.add(pair)
                        why = ("identical once separators are ignored" if loose(nm) == loose(near["name"])
                               else "differs by about one character, likely a typo")
                        to_queue.append({"candidate_a": near["person_id"], "candidate_b": slug(nm),
                                         "evidence": f"Vigloo cast lists '{nm}'; people.csv has '{near['name']}' "
                                                     f"({why}). Seen on title {tid}. Not credited pending a ruling.",
                                         "status": "pending"})
                    continue
                pid = slug(nm)
                if not pid or pid in existing_ids: continue
                existing_ids.add(pid)
                person = {"person_id": pid, "slug": pid, "name": nm, "aka_names": "",
                          "role_type": "actor", "socials": "", "bio_short": "", "photo_ref": "",
                          "data_confidence": "needs_check", "source": SOURCE}
                new_people.append(person); by_name[key] = person
                by_loose.setdefault(loose(nm), person); created += 1
            else:
                matched += 1
            if (tid, person["person_id"]) in have_credit: continue
            have_credit.add((tid, person["person_id"]))
            new_credits.append({"title_id": tid, "person_id": person["person_id"],
                                "role": "lead" if order < 2 else "actor", "character_name": ""})

    got = sum(1 for _t, n in results if n)
    print(f"\ntitles that yielded a cast: {got}/{len(results)}")
    print(f"new credits {len(new_credits)} | people matched {matched} | people created {created}")
    print(f"near-duplicates queued (NOT credited): {len(to_queue)}")
    for q in to_queue[:8]: print("   ", q["evidence"][:105])

    if args.dry_run:
        for c in new_credits[:10]: print("   ", c["title_id"], "->", c["person_id"])
        print("(dry run, nothing written)")
        return
    if new_people: save("people.csv", list(people[0].keys()), people + new_people)
    if new_credits: save("credits.csv", list(credits[0].keys()), credits + new_credits)
    if to_queue: save("match_queue.csv", list(queue[0].keys()), queue + to_queue)
    print(f"\nwrote {len(new_credits)} credits, {len(new_people)} people, {len(to_queue)} queued")


if __name__ == "__main__":
    main()
