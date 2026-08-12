#!/usr/bin/env python3
"""Append one transcribed IMDb page to the 9 Aug staging file and tick the ledger.

Why a helper: the Drive batch is 93 files, so the transcription runs across many
passes. Writing each entry straight to disk the moment it is read means a long
grind cannot lose work, and the ledger is the only reliable record of what has
actually been processed versus merely listed.

Usage (payload is JSON on stdin):
    py stage_add.py title  <drive_file_id> < entry.json
    py stage_add.py actor  <drive_file_id> < entry.json
    py stage_add.py status <drive_file_id> no_data "why"
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
STAGING = os.path.join(HERE, "staging")
LEDGER = os.path.join(STAGING, "drive_2026-08-09_ledger.json")
TITLES = os.path.join(STAGING, "imdb_candyjar_2026-08-09.json")
ACTORS = os.path.join(STAGING, "imdb_filmographies_2026-08-09.json")


def load(path, default):
    if not os.path.exists(path):
        return default
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save(path, obj):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def tick(file_id, status, credits=None, note=None):
    led = load(LEDGER, None)
    for row in led["files"]:
        if row["id"] == file_id:
            row["status"] = status
            if credits is not None:
                row["credits"] = credits
            if note:
                row["note"] = note
            save(LEDGER, led)
            return row["title"]
    raise SystemExit(f"file id {file_id} is not in the ledger")


def main():
    mode, file_id = sys.argv[1], sys.argv[2]

    if mode == "status":
        name = tick(file_id, sys.argv[3], note=(sys.argv[4] if len(sys.argv) > 4 else None))
        print(f"ledger: {name} -> {sys.argv[3]}")
        return

    entry = json.load(sys.stdin)
    path = TITLES if mode == "title" else ACTORS
    key = "titles" if mode == "title" else "people"
    doc = load(path, {
        "source": f"imdb_{'candyjar' if mode == 'title' else 'filmographies'}_2026-08-09",
        "note": ("Cast transcribed from Cyan's IMDb PDFs (Drive folder 1P6HAJ2z..., 9 Aug 2026). "
                 "CAST ONLY - no IMDb storyline or platform synopsis text is taken, and no Browse "
                 "caption is ever reworded from one."),
        key: [],
    })
    doc.setdefault(key, [])

    ident = entry.get("title") or entry.get("name")
    doc[key] = [e for e in doc[key] if (e.get("title") or e.get("name")) != ident]
    doc[key].append(entry)
    save(path, doc)

    n = len(entry.get("cast") or entry.get("credits") or [])
    name = tick(file_id, "done", credits=n)
    print(f"staged {ident!r}: {n} rows   ledger: {name} -> done")


if __name__ == "__main__":
    main()
