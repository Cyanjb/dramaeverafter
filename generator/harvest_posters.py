#!/usr/bin/env python3
"""Harvest poster art for titles that have none.

Reads availability.csv for direct_link URLs on the platforms we can reach, pulls the
og:image from each title page, and writes it into titles.csv poster_ref.

Fill-blank-only: an existing poster_ref is never overwritten (data/CONVENTIONS.md).
Polite by default: bounded concurrency, a real UA, one retry, and it stops on a wall
of failures rather than hammering a host that has started refusing us.

Usage:
    python3 harvest_posters.py [--limit N] [--platform reelshort|goodshort] [--dry-run]
"""
import csv, os, re, sys, time, argparse, io
from concurrent.futures import ThreadPoolExecutor
import urllib.request, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")
PLATFORMS = ("reelshort", "goodshort")
WORKERS = 8
TIMEOUT = 25

OG = [
    re.compile(r'<meta[^>]+(?:property|name)=["\']og:image["\'][^>]*content=["\']([^"\']+)', re.I),
    re.compile(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]*(?:property|name)=["\']og:image["\']', re.I),
    re.compile(r'<meta[^>]+(?:property|name)=["\']twitter:image["\'][^>]*content=["\']([^"\']+)', re.I),
]


def rows(name):
    with open(os.path.join(DATA, name), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


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


def poster_from(html):
    if not html:
        return None
    for pat in OG:
        m = pat.search(html)
        if m:
            u = m.group(1).replace("\\u002F", "/").strip()
            # Reject logos/sprites: we want a cover, not site furniture.
            if u.startswith("http") and not re.search(r"(logo|favicon|sprite|placeholder)", u, re.I):
                return u
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--platform", default=None)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    titles = rows("titles.csv")
    fields = list(titles[0].keys())
    avail = rows("availability.csv")

    have = {t["title_id"] for t in titles if (t.get("poster_ref") or "").strip()}
    wanted = [p for p in PLATFORMS if not args.platform or p == args.platform]

    # one link per title, first platform in preference order that has one
    targets = {}
    for p in wanted:
        for a in avail:
            if a["platform_id"] != p:
                continue
            tid, link = a["title_id"], (a.get("direct_link") or "").strip()
            if tid in have or tid in targets or not link.startswith("http"):
                continue
            targets[tid] = (p, link)

    todo = list(targets.items())
    if args.limit:
        todo = todo[:args.limit]
    print(f"{len(todo)} titles need a poster (platforms: {', '.join(wanted)})")
    if not todo:
        return

    found, failed, done = {}, 0, 0

    def work(item):
        tid, (plat, link) = item
        return tid, plat, poster_from(fetch(link))

    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        for tid, plat, url in ex.map(work, todo):
            done += 1
            if url:
                found[tid] = url
            else:
                failed += 1
            if done % 100 == 0:
                print(f"  {done}/{len(todo)}  found={len(found)}  missed={failed}", flush=True)
            # Bail out rather than keep hammering a host that has clearly cut us off.
            if done >= 40 and len(found) == 0:
                print("  aborting: 40 consecutive misses, the source is not cooperating")
                break

    print(f"\nresolved {len(found)} posters, {failed} misses")
    if args.dry_run:
        for tid, u in list(found.items())[:10]:
            print("  ", tid, "->", u)
        print("(dry run, nothing written)")
        return
    if not found:
        return

    n = 0
    for t in titles:
        if t["title_id"] in found and not (t.get("poster_ref") or "").strip():
            t["poster_ref"] = found[t["title_id"]]
            n += 1

    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=fields, lineterminator="\r\n")
    w.writeheader()
    w.writerows(titles)
    with open(os.path.join(DATA, "titles.csv"), "w", newline="", encoding="utf-8") as f:
        f.write(buf.getvalue())
    print(f"wrote {n} poster_ref values into titles.csv")


if __name__ == "__main__":
    main()
