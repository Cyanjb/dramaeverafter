"""Write one transcribed IMDb page to its own small JSON + append a progress line.

Per-file outputs (rather than one growing document) keep each write cheap across
a 93-file grind, and the append-only log is the record of what has actually been
processed. Everything is reconciled into the ledger at the end.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(HERE, "_progress.log")

kind, file_id = sys.argv[1], sys.argv[2]
entry = json.load(sys.stdin)
entry["_drive_id"] = file_id
entry["_kind"] = kind

ident = entry.get("title") or entry.get("name")
slug = "".join(c if c.isalnum() else "-" for c in ident.lower()).strip("-")
path = os.path.join(HERE, f"{kind}__{slug}.json")
with open(path, "w", encoding="utf-8") as f:
    json.dump(entry, f, ensure_ascii=False, indent=2)

n = len(entry.get("cast") or entry.get("credits") or [])
with open(LOG, "a", encoding="utf-8") as f:
    f.write(f"{file_id}\t{kind}\t{ident}\t{n}\n")
print(f"OK {ident}: {n} rows -> {os.path.basename(path)}")
