#!/usr/bin/env python3
"""Refill the My Drama synopsis_short values our 17 July scrape dropped.

Why this exists: adapters.md sec 18. 126 of 186 My Drama titles carry no
synopsis_short, which made My Drama look like a platform that publishes thin
metadata. It is not -- 125 of those 126 still have episode_count and 124 have
poster_ref, both of which sec 5 records as arriving in the SAME payload as the
description. The parser reached the block and wrote the neighbours. This is a
re-read, not new research, and it is the cheapest completeness win on the board:
a description is one of the four fields the quality bar counts.

WHERE THE TEXT COMES FROM, and why not the seriesData block sec 5 describes.
The page carries the same description twice: once inside the streamed Next.js
payload (escaped, so it needs a unicode unescape) and once inside a clean
schema.org ld+json @graph as the TVSeries node. This reads the ld+json, because
unescaping the payload by the usual html.encode().decode('unicode_escape') route
reinterprets each UTF-8 byte as latin-1 and silently produces the invisible C1
mojibake already on the traps list. The ld+json parses through json.loads with
its codepoints intact -- verified on 'A Match Made in Hell', whose fetched text
is byte-identical to the value already on file.

Safety rules, from data/CONVENTIONS.md:
  - FILL-BLANK-ONLY. Every non-blank field is left exactly as it is; a title that
    already has a synopsis_short is never rewritten, only compared.
  - last_verified and source are non-blank on every row and so are NOT touched.
    Provenance for this pass is recorded in generator/staging/ instead.
  - Line endings are preserved per file (titles.csv is CRLF on disk, checked
    rather than assumed).
  - No snapshots rows: sec 5 records that My Drama publishes no view counts.

The already-filled titles are re-read as a CONTROL. If the reader disagrees with
what is on file for those, the reader is wrong and the blanks it produces cannot
be trusted either, so a mismatch aborts the run before anything is written.

WHAT THE CONTROL MUST NOT DO IS CONFUSE ITS TWO FAILURE MODES, which is how the
first run of this script aborted on good data. A disagreement is either OUR
READER mangling characters, which is a bug and must stop the pass, or MY DRAMA
HAVING REWRITTEN THE COPY since 17 July, which is not a bug and says nothing
about the blanks. They are told apart by WHERE the two strings diverge: a reader
fault shows up at a punctuation mark or a non-ASCII character, a rewrite shows up
at a word. Measured 9 Aug against all 59 filled titles: 50 identical, 7 rewritten
outright, 1 differing only by a straight versus curly apostrophe, and 1 where OUR
stored copy is truncated mid-word. Only the encoding class gates the run.

Usage:
    py harvest_mydrama_descriptions.py --dry-run
    py harvest_mydrama_descriptions.py [--limit N] [--workers N]
"""
import argparse
import csv
import io
import json
import os
import re
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "data")
STAGING = os.path.join(HERE, "staging")
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")
PLATFORM = "my-drama"
SOURCE = "mydrama_desc_" + time.strftime("%Y-%m-%d")
TIMEOUT = 30

LD_RE = re.compile(
    r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', re.S)

# Boilerplate that appears in the same @graph and must never reach a title row.
# The WebSite node's blurb is the one that would otherwise land on 126 titles.
BOILERPLATE = {
    "watch short-form vertical drama series online for free.",
}
MIN_LEN = 25
MAX_LEN = 1200


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


def fetch(url, tries=3):
    """My Drama resets the odd connection under concurrency; retry before giving up."""
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(
                url, headers={"User-Agent": UA, "Accept": "text/html"})
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                return r.read().decode("utf-8", "ignore"), None
        except Exception as e:
            last = e
            if i + 1 < tries:
                time.sleep(1.5 * (i + 1))
    return None, repr(last)


def series_node(html):
    """Return the TVSeries dict from the page's ld+json @graph, or None."""
    for block in LD_RE.findall(html or ""):
        try:
            obj = json.loads(block)
        except Exception:
            continue
        graph = obj.get("@graph", obj) if isinstance(obj, dict) else obj
        for node in (graph if isinstance(graph, list) else [graph]):
            if isinstance(node, dict) and node.get("@type") == "TVSeries":
                return node
    return None


def clean(text):
    """Normalise whitespace only. Never rewrite the platform's wording."""
    return re.sub(r"\s+", " ", (text or "")).strip()


TYPOGRAPHY = {"‘": "'", "’": "'", "“": '"', "”": '"',
              "–": "-", "—": "-", "…": "..."}


def fold(s):
    """Collapse typographic variants so a curly apostrophe does not read as corruption."""
    for a, b in TYPOGRAPHY.items():
        s = s.replace(a, b)
    return re.sub(r"\s+", " ", s).strip()


def divergence_kind(have, got):
    """Classify why a control title's stored text differs from what we just read.

    'encoding' is the only class that indicts the reader and stops the run.
    'benign'    - identical once curly quotes and dashes are folded.
    'truncated' - one is a strict prefix of the other, so OUR copy was cut short.
    'rewrite'   - My Drama changed the words. Not our problem, and not a reason
                  to distrust the blanks read from the same parser.
    """
    if any(0x80 <= ord(c) <= 0x9F or c == "�" for c in have + got):
        return "encoding"
    if fold(have) == fold(got):
        return "benign"
    a, b = fold(have), fold(got)
    if a.startswith(b) or b.startswith(a):
        return "truncated"
    return "rewrite"


def usable(desc):
    """Reject boilerplate, unfilled templates and implausible lengths."""
    if not desc:
        return False, "empty"
    if "{name}" in desc or "{description}" in desc:
        return False, "unfilled template"
    if desc.lower() in BOILERPLATE:
        return False, "site boilerplate"
    if len(desc) < MIN_LEN:
        return False, f"too short ({len(desc)})"
    if len(desc) > MAX_LEN:
        return False, f"too long ({len(desc)})"
    # An invisible C1 char or a replacement char means the decode went wrong
    # somewhere upstream; refuse rather than bake mojibake into 126 rows.
    bad = [c for c in desc if 0x80 <= ord(c) <= 0x9F or c == "�"]
    if bad:
        return False, f"mojibake ({len(bad)} C1/replacement chars)"
    return True, ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    titles = rows("titles.csv")
    by_id = {t["title_id"]: t for t in titles}

    targets, controls = [], []
    seen = set()
    for a in rows("availability.csv"):
        if a["platform_id"] != PLATFORM:
            continue
        tid, link = a["title_id"], (a.get("direct_link") or "").strip()
        if not link.startswith("http") or tid not in by_id or tid in seen:
            continue
        seen.add(tid)
        (targets if not (by_id[tid].get("synopsis_short") or "").strip()
         else controls).append((tid, link))

    if args.limit:
        targets = targets[:args.limit]
        controls = controls[:max(3, args.limit // 4)]

    print(f"{len(targets)} My Drama titles with a blank synopsis_short")
    print(f"{len(controls)} already filled, re-read as a control\n")

    def work(item):
        tid, url = item
        html, err = fetch(url)
        if html is None:
            return tid, url, None, err
        node = series_node(html)
        if node is None:
            return tid, url, None, "no TVSeries node in ld+json"
        return tid, url, clean(node.get("description")), None

    def run(items, label):
        out = []
        with ThreadPoolExecutor(max_workers=args.workers) as ex:
            for i, res in enumerate(ex.map(work, items), 1):
                out.append(res)
                if i % 25 == 0:
                    print(f"  {label} {i}/{len(items)}", flush=True)
        return out

    # ---- control first: if the reader cannot reproduce what is on file, stop.
    print("reading controls...")
    agree = ctrl_fail = 0
    encoding_faults, rewrites = [], []
    for tid, _url, desc, err in run(controls, "control"):
        if err or not desc:
            ctrl_fail += 1
            continue
        have = clean(by_id[tid]["synopsis_short"])
        if desc == have:
            agree += 1
            continue
        name = by_id[tid]["primary_title"]
        kind = divergence_kind(have, desc)
        if kind == "encoding":
            encoding_faults.append((name, have, desc))
        elif kind == "benign":
            agree += 1
        else:
            rewrites.append((tid, name, kind, have, desc))

    truncated = [r for r in rewrites if r[2] == "truncated"]
    print(f"\ncontrol: {agree} identical, {len(rewrites)} differ upstream "
          f"({len(truncated)} of them truncated on OUR side), "
          f"{len(encoding_faults)} encoding faults, {ctrl_fail} unreadable")
    for _tid, name, kind, have, got in rewrites[:10]:
        print(f"  {kind.upper()} {name}\n    on file: {have[:110]}\n    now:     {got[:110]}")
    for name, have, got in encoding_faults[:5]:
        print(f"  ENCODING {name}\n    on file: {have[:110]}\n    fetched: {got[:110]}")

    if agree == 0:
        print("\nABORT: no control title could be verified.")
        return 1
    # Only a reader fault gates the run. Upstream rewrites are a finding about
    # the platform, not a reason to distrust text read from that same platform.
    if len(encoding_faults) > max(1, agree * 0.05):
        print("\nABORT: the reader is mangling characters on titles we already "
              "hold, so its output for the blanks cannot be trusted either.")
        return 1

    # ---- the real pass
    print("\nreading blanks...")
    filled, rejected, failed = {}, [], []
    for tid, url, desc, err in run(targets, "blank"):
        if err:
            failed.append((tid, url, err))
            continue
        ok, why = usable(desc)
        if not ok:
            rejected.append((tid, why, (desc or "")[:80]))
            continue
        filled[tid] = desc

    print(f"\nusable descriptions: {len(filled)}/{len(targets)}")
    print(f"rejected:            {len(rejected)}")
    for tid, why, sample in rejected[:8]:
        print(f"   {by_id[tid]['primary_title'][:40]:42} {why:28} {sample!r}")
    print(f"fetch failures:      {len(failed)}")
    for tid, _u, err in failed[:8]:
        print(f"   {by_id[tid]['primary_title'][:40]:42} {err[:70]}")

    if args.dry_run:
        print("\nsample of what would be written:")
        for tid, d in list(filled.items())[:6]:
            print(f"\n  {by_id[tid]['primary_title']}\n    {d[:200]}")
        print("\n(dry run, nothing written)")
        return 0

    if not filled:
        print("\nnothing to write")
        return 0

    # Record the transcription in the repo before touching the database, so the
    # pass survives as evidence the same way the IMDb batches do.
    os.makedirs(STAGING, exist_ok=True)
    stage = os.path.join(STAGING, f"mydrama_desc_{time.strftime('%Y-%m-%d')}.json")
    with open(stage, "w", encoding="utf-8") as f:
        json.dump({
            "source": SOURCE,
            "platform": PLATFORM,
            "field": "synopsis_short",
            "mode": "fill-blank-only",
            "read_from": "schema.org ld+json @graph, TVSeries node",
            "control": {
                "identical": agree,
                "encoding_faults": len(encoding_faults),
                "unreadable": ctrl_fail,
                # Recorded, deliberately NOT applied: these titles already have a
                # description, and CONVENTIONS.md makes non-blank fields
                # fill-blank-only. Cyan decides whether to take the new copy.
                "changed_upstream_not_applied": [
                    {"title_id": t, "title": n, "kind": k, "on_file": h, "now_on_platform": g}
                    for t, n, k, h, g in rewrites
                ],
            },
            "descriptions": {tid: filled[tid] for tid in sorted(filled)},
        }, f, ensure_ascii=False, indent=2)
    print(f"\nstaged {len(filled)} descriptions -> {os.path.relpath(stage, os.path.dirname(HERE))}")

    written = 0
    for t in titles:
        d = filled.get(t["title_id"])
        # Re-check blankness against the row we are about to write, not the
        # snapshot taken before the fetch.
        if d and not (t.get("synopsis_short") or "").strip():
            t["synopsis_short"] = d
            written += 1

    write_csv("titles.csv", list(titles[0].keys()), titles)
    print(f"written: {written} synopsis_short values into titles.csv")
    return 0


if __name__ == "__main__":
    sys.exit(main())
