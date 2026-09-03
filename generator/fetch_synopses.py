#!/usr/bin/env python3
"""Fetch the full published synopsis for the next N titles in the caption queue.

WHY THIS EXISTS. Every title still to caption holds only a truncated first
sentence on disk (measured 2 Sep 2026: 0 of the next 129 had a usable source),
and the cloud sandbox cannot reach any platform domain. GitHub's runners can.
So this script runs in the fetch-synopses workflow, reads each title's own
platform page, and banks the text in a dated staging JSON that a writing
session then reads. It NEVER writes to data/.

Selection is the caption queue itself (caption_pipeline.build_queue, ranked by
reach, tier A excluded), so the file always covers the titles that matter next.

Politeness: one request at a time, a pause between requests, one retry, a
desktop user agent, and only the title's own direct_link. Fan and affiliate
sites are skipped: a synopsis from pinedrama is not a fact source.

Usage:
    python3 generator/fetch_synopses.py --count 129 --offset 0 --out generator/staging/facts_2026-09-02.json
    python3 generator/fetch_synopses.py --count 10 --list        # selection only, no network

Output entry per title_id:
    title, platform, url, status, route, text, episode_count, on_disk_len, fetched_at
route names which extractor won: nextdata (the __NEXT_DATA__ book object,
adapters.md sec 2), ldjson (schema.org description), og (og:description) or
meta (meta description). The longest candidate wins; the others are recorded
by length so a session can see when the page holds more than it took.
"""
import argparse, datetime, io, json, os, re, sys, time, urllib.request, urllib.error
from html import unescape

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import caption_pipeline as cp  # noqa: E402

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36")
SKIP_HOSTS = ("pinedrama.com", "dailymotion.com")
PAUSE = 1.5


def fetch(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": UA, "Accept": "text/html,application/xhtml+xml",
        "Accept-Language": "en-US,en;q=0.9"})
    last = None
    for attempt in (1, 2):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.status, r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            return e.code, ""
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(3)
    return 0, "error: %s" % last


def clean(s):
    s = unescape(s or "")
    s = re.sub(r"<[^>]+>", " ", s)
    return " ".join(s.split())


def walk(obj, out):
    """Every dict in a JSON tree, flattened."""
    if isinstance(obj, dict):
        out.append(obj)
        for v in obj.values():
            walk(v, out)
    elif isinstance(obj, list):
        for v in obj:
            walk(v, out)
    return out


def from_nextdata(html):
    m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.S)
    if not m:
        return []
    try:
        data = json.loads(m.group(1))
    except ValueError:
        return []
    found = []
    for d in walk(data, []):
        if "book_title" in d or "bookTitle" in d:
            for key in ("special_desc", "description", "desc", "intro", "introduction", "summary"):
                if isinstance(d.get(key), str) and d[key].strip():
                    ep = d.get("chapter_count") or d.get("chapterCount") or ""
                    found.append(("nextdata:" + key, clean(d[key]), str(ep)))
    return found


def from_ldjson(html):
    out = []
    for m in re.finditer(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', html, re.S):
        try:
            data = json.loads(m.group(1))
        except ValueError:
            continue
        for d in walk(data, []):
            if isinstance(d.get("description"), str) and d["description"].strip():
                ep = d.get("numberOfEpisodes") or ""
                out.append(("ldjson:" + str(d.get("@type", "")), clean(d["description"]), str(ep)))
    return out


def from_meta(html):
    out = []
    for prop, route in (("og:description", "og"), ("description", "meta")):
        m = (re.search(r'<meta[^>]+(?:property|name)="%s"[^>]+content="([^"]*)"' % prop, html, re.I)
             or re.search(r'<meta[^>]+content="([^"]*)"[^>]+(?:property|name)="%s"' % prop, html, re.I))
        if m and m.group(1).strip():
            out.append((route, clean(m.group(1)), ""))
    return out


def extract(html):
    cands = from_nextdata(html) + from_ldjson(html) + from_meta(html)
    if not cands:
        return "", "", "", {}
    best = max(cands, key=lambda c: len(c[1]))
    ep = next((c[2] for c in cands if c[2]), "")
    return best[0], best[1], ep, {c[0]: len(c[1]) for c in cands}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--count", type=int, default=45)
    ap.add_argument("--offset", type=int, default=0)
    ap.add_argument("--out", default="")
    ap.add_argument("--list", action="store_true", help="print the selection and exit")
    a = ap.parse_args()

    queue = [r for r in cp.build_queue() if r["tier"] != "A"][a.offset:a.offset + a.count]
    if a.list:
        for r in queue:
            print("%-8s %-6s %-50s %s" % (cp.views_label(r["reach"]), r["platform"], r["title"][:50], r["link"] or "NO LINK"))
        print("%d titles" % len(queue))
        return 0

    out_path = a.out or os.path.join(cp.STAGING, "facts_%s.json" % datetime.date.today().isoformat())
    results = {}
    if os.path.exists(out_path):
        results = json.load(io.open(out_path, encoding="utf-8"))
    stamp = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
    ok = fail = longer = 0
    for i, r in enumerate(queue, 1):
        tid, url = r["tid"], r["link"]
        entry = {"title": r["title"], "platform": r["platform"], "url": url, "reach": r["reach"],
                 "on_disk_len": len((r["facts"] or "").strip()), "fetched_at": stamp}
        if not url or any(h in url for h in SKIP_HOSTS):
            entry.update(status=0, route="", text="", episode_count="", note="no platform link")
            fail += 1
        else:
            status, html = fetch(url)
            route, text, ep, cands = extract(html) if status == 200 else ("", "", "", {})
            entry.update(status=status, route=route, text=text, episode_count=ep, candidates=cands)
            if text:
                ok += 1
                if len(text) > entry["on_disk_len"]:
                    longer += 1
            else:
                fail += 1
            time.sleep(PAUSE)
        results[tid] = entry
        print("%3d/%d %-6s %-46s %s %s %5d chars" % (i, len(queue), r["platform"], r["title"][:46],
                                                    entry["status"], entry.get("route") or "-", len(entry["text"])))
        sys.stdout.flush()
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    io.open(out_path, "w", encoding="utf-8", newline="\n").write(
        json.dumps(results, ensure_ascii=False, indent=1, sort_keys=True) + "\n")
    print("\nwrote %s: %d fetched, %d failed, %d longer than on disk" % (out_path, ok, fail, longer))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
