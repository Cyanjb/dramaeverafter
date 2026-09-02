#!/usr/bin/env python3
"""Turn a fetched facts JSON (from fetch_synopses.py) into a caption batch file.

caption_pipeline.py next writes a batch whose FACTS comments are whatever is on
disk, which is a truncated first sentence for nearly every title. This writes
the same shape of file from the FULL text the fetch-synopses workflow banked,
with SOURCES recorded as ('platform', url) so check() can audit provenance, and
EPISODES kept for the parked episode-count pass. CAPTIONS start empty; a writing
session fills them in.

Usage:
    python3 generator/make_batch.py generator/staging/facts_2026-09-02.json generator/staging/captions_2026_09_02_b4.py [--limit N]
"""
import io, json, sys, datetime


def main():
    src, dst = sys.argv[1], sys.argv[2]
    limit = int(sys.argv[sys.argv.index("--limit") + 1]) if "--limit" in sys.argv else 0
    facts = json.load(io.open(src, encoding="utf-8"))
    rows = [(tid, e) for tid, e in facts.items() if (e.get("text") or "").strip()]
    rows.sort(key=lambda kv: -(kv[1].get("reach") or 0))
    if limit:
        rows = rows[:limit]
    skipped = [tid for tid, e in facts.items() if not (e.get("text") or "").strip()]
    out = ["# -*- coding: utf-8 -*-",
           '"""Batch built by make_batch.py on %s from %s.' % (datetime.date.today().isoformat(), src.replace("\\", "/")),
           "",
           "Fill CAPTIONS. Each value is HOOK newline BODY. Facts are the title's own",
           "platform page, fetched in full by the fetch-synopses workflow; SOURCES records",
           "the url. Write to the exemplars in CAPTION-TRAINING.md, not to the rules.",
           '"""', "", "CAPTIONS = {"]
    for tid, e in rows:
        out.append("")
        out.append("    # %-8s %s" % (_views(e.get("reach") or 0), e["title"]))
        for line in _wrap(e["text"], 88):
            out.append("    # FACTS: %s" % line)
        if e.get("episode_count"):
            out.append("    # EPISODES: %s" % e["episode_count"])
        out.append("    %r:" % tid)
        out.append('        "",')
    out.append("}")
    out.append("")
    out.append("FACTS = {")
    for tid, e in rows:
        out.append("    %r: %r," % (tid, " ".join(e["text"].split())))
    out.append("}")
    out.append("")
    out.append("SOURCES = {")
    for tid, e in rows:
        out.append("    %r: ('platform', %r)," % (tid, e.get("url", "")))
    out.append("}")
    out.append("")
    out.append("EPISODES = {")
    for tid, e in rows:
        if e.get("episode_count"):
            out.append("    %r: %r," % (tid, str(e["episode_count"])))
    out.append("}")
    out.append("")
    io.open(dst, "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")
    print("wrote %s: %d titles with facts, %d skipped (no text): %s" % (dst, len(rows), len(skipped), ", ".join(skipped[:10])))


def _views(n):
    return "%.1fM" % (n / 1e6) if n >= 1e6 else ("%.1fK" % (n / 1e3) if n >= 1e3 else str(n))


def _wrap(text, width):
    words, line, out = " ".join(text.split()).split(" "), "", []
    for w in words:
        if len(line) + len(w) + 1 > width and line:
            out.append(line)
            line = w
        else:
            line = (line + " " + w).strip()
    if line:
        out.append(line)
    return out


if __name__ == "__main__":
    main()
