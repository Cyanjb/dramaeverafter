#!/usr/bin/env python3
"""Harvest cast lists from My Drama series pages into credits.csv.

Why this exists: 2,269 of 3,407 titles have no cast at all. The gap is mostly
GoodShort (1,820), which publishes no cast anywhere on its pages, so those cannot
be filled from the platform. My Drama DOES ship a cast array in its Next.js
payload, so its ~186 titles are recoverable.

The payload gives camelCase tokens ("nazarGrabar"), not display names, so each is
expanded back to "Nazar Grabar" and then matched against people.csv.

Safety rules, from data/CONVENTIONS.md:
  - Never auto-merge a fuzzy name. Exact match reuses the existing person; a
    near-match (same slug once hyphens are stripped) goes to match_queue.csv for
    a human ruling and is NOT credited.
  - New people enter as data_confidence=needs_check with a dated source string.
  - Existing credits are never duplicated or overwritten.
  - Line endings are preserved per file (credits/match_queue CRLF, people CRLF
    despite CONVENTIONS.md claiming LF -- checked on disk, not assumed).

Usage:
    python3 harvest_mydrama_cast.py [--limit N] [--dry-run]
"""
import csv, io, os, re, sys, time, argparse, difflib
from concurrent.futures import ThreadPoolExecutor

import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "data")
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")
PLATFORM = "my-drama"
SOURCE = "mydrama_cast_" + time.strftime("%Y-%m-%d")
WORKERS = 6
TIMEOUT = 30
CAST_RE = re.compile(r'"cast"\s*:\s*\[(.*?)\]', re.S)
TOKEN_RE = re.compile(r'"([A-Za-z][A-Za-z0-9]{2,60})"')


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


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def loose(s):
    """Slug with separators removed, for near-match detection per CONVENTIONS.md."""
    return re.sub(r"[^a-z0-9]", "", s.lower())


def expand(token):
    """'nazarGrabar' -> 'Nazar Grabar'. Returns '' if it does not look like a name."""
    if not token or not token[0].isalpha():
        return ""
    parts = re.findall(r"[A-Z]?[a-z]+|[A-Z]+(?![a-z])", token)
    if len(parts) < 2:
        return ""
    words = [p if p.isupper() and len(p) > 1 else p.capitalize() for p in parts]
    name = " ".join(words)
    return name if 4 <= len(name) <= 60 else ""


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
    if not html:
        return []
    try:
        text = html.encode().decode("unicode_escape", errors="ignore")
    except Exception:
        text = html
    out, seen = [], set()
    for block in CAST_RE.findall(text):
        for tok in TOKEN_RE.findall(block):
            nm = expand(tok)
            if nm and nm.lower() not in seen:
                seen.add(nm.lower())
                out.append(nm)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    titles = {t["title_id"]: t for t in rows("titles.csv")}
    people = rows("people.csv")
    credits = rows("credits.csv")
    queue = rows("match_queue.csv")

    by_name = {p["name"].strip().lower(): p for p in people}
    by_loose = {}
    for p in people:
        by_loose.setdefault(loose(p["name"]), p)
    have_credit = {(c["title_id"], c["person_id"]) for c in credits}
    queued = {(q["candidate_a"], q["candidate_b"]) for q in queue}

    targets = []
    for a in rows("availability.csv"):
        if a["platform_id"] != PLATFORM:
            continue
        link = (a.get("direct_link") or "").strip()
        if link.startswith("http") and a["title_id"] in titles:
            targets.append((a["title_id"], link))
    seen_t = set()
    targets = [x for x in targets if not (x[0] in seen_t or seen_t.add(x[0]))]
    if args.limit:
        targets = targets[:args.limit]
    print(f"{len(targets)} My Drama titles to check")

    def work(item):
        tid, url = item
        return tid, cast_from(fetch(url))

    results = []
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        for i, (tid, names) in enumerate(ex.map(work, targets), 1):
            results.append((tid, names))
            if i % 40 == 0:
                got = sum(1 for _t, n in results if n)
                print(f"  {i}/{len(targets)}  with cast: {got}", flush=True)

    new_credits, new_people, to_queue = [], [], []
    matched = created = skipped_existing = 0

    for tid, names in results:
        for order, nm in enumerate(names):
            key = nm.strip().lower()
            person = by_name.get(key)
            if person is None:
                near = by_loose.get(loose(nm))
                if near is None:
                    # Separator-insensitive matching misses single-letter typos, and this
                    # source produced "Jakson Tiller" against an existing "Jackson Tiller".
                    # CONVENTIONS.md: hold the rarer spelling out and queue it.
                    close = difflib.get_close_matches(loose(nm), by_loose.keys(), n=1, cutoff=0.92)
                    if close:
                        near = by_loose[close[0]]
                if near is not None and near["name"].strip().lower() != key:
                    # Same person once separators are ignored, but spelled differently.
                    # Never auto-merge: hand it to a human.
                    pair = (near["person_id"], slug(nm))
                    if pair not in queued:
                        queued.add(pair)
                        why = ("identical once separators are ignored"
                               if loose(nm) == loose(near["name"])
                               else "differs by about one character, likely a typo")
                        to_queue.append({
                            "candidate_a": near["person_id"],
                            "candidate_b": slug(nm),
                            "evidence": f"My Drama cast lists '{nm}'; people.csv has '{near['name']}' "
                                        f"({why}). Seen on title {tid}. Not credited pending a ruling.",
                            "status": "pending",
                        })
                    continue
                pid = slug(nm)
                if pid in {p["person_id"] for p in people} | {p["person_id"] for p in new_people}:
                    continue
                person = {"person_id": pid, "slug": pid, "name": nm, "aka_names": "",
                          "role_type": "actor", "socials": "", "bio_short": "", "photo_ref": "",
                          "data_confidence": "needs_check", "source": SOURCE}
                new_people.append(person)
                by_name[key] = person
                by_loose.setdefault(loose(nm), person)
                created += 1
            else:
                matched += 1
            if (tid, person["person_id"]) in have_credit:
                skipped_existing += 1
                continue
            have_credit.add((tid, person["person_id"]))
            new_credits.append({"title_id": tid, "person_id": person["person_id"],
                                # Billing order is meaningful in this payload, but only the
                                # top two are safe to call leads; the rest stay generic.
                                "role": "lead" if order < 2 else "actor",
                                "character_name": ""})

    with_cast = sum(1 for _t, n in results if n)
    print(f"\ntitles with a cast array: {with_cast}/{len(results)}")
    print(f"new credits:      {len(new_credits)}")
    print(f"  matched existing people: {matched}")
    print(f"  new people created:      {created}")
    print(f"  credits already present: {skipped_existing}")
    print(f"near-duplicate names sent to match_queue (NOT credited): {len(to_queue)}")
    for q in to_queue[:8]:
        print("   ", q["evidence"][:110])

    if args.dry_run:
        print("\nsample new credits:")
        for c in new_credits[:10]:
            print("   ", c["title_id"], "->", c["person_id"], f"({c['role']})")
        print("\nsample new people:")
        for p in new_people[:10]:
            print("   ", p["person_id"], "|", p["name"])
        print("\n(dry run, nothing written)")
        return

    if new_people:
        write_csv("people.csv", list(people[0].keys()), people + new_people)
    if new_credits:
        write_csv("credits.csv", list(credits[0].keys()), credits + new_credits)
    if to_queue:
        write_csv("match_queue.csv", list(queue[0].keys()), queue + to_queue)
    print(f"\nwrote {len(new_credits)} credits, {len(new_people)} people, {len(to_queue)} match_queue rows")


if __name__ == "__main__":
    main()
