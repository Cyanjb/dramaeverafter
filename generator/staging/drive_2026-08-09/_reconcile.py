"""Rebuild ledger statuses from the per-file staging JSONs + _progress.log.

The ledger is a convenience index; the staged files and the append-only log are
the ground truth. Reconciling from them means an out-of-date or reverted ledger
can never silently cause a file to be processed twice or skipped.
"""
import json, os, glob

HERE = os.path.dirname(os.path.abspath(__file__))
LEDGER = os.path.join(os.path.dirname(HERE), "drive_2026-08-09_ledger.json")

# Ground truth: every staged file records the drive id it came from.
done = {}
for p in glob.glob(os.path.join(HERE, "*.json")):
    if os.path.basename(p).startswith("_"):
        continue
    d = json.load(open(p, encoding="utf-8"))
    fid = d.get("_drive_id")
    if fid:
        done[fid] = len(d.get("cast") or d.get("credits") or [])

led = json.load(open(LEDGER, encoding="utf-8"))
changed = 0
for row in led["files"]:
    if row["id"] in done and row["status"] != "done":
        row["status"] = "done"
        row["credits"] = done[row["id"]]
        changed += 1
    elif row["id"] in done:
        row["credits"] = done[row["id"]]

with open(LEDGER, "w", encoding="utf-8") as f:
    json.dump(led, f, ensure_ascii=False, indent=2)

from collections import Counter
c = Counter(r["status"] for r in led["files"])
print(f"reconciled {changed} row(s) from staged files")
print(f"ledger now: {dict(c)}  of {len(led['files'])} files")
print(f"credits staged: {sum(done.values())}")
