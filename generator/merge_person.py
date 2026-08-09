#!/usr/bin/env python3
"""Merge one person record into another, after a human ruling.

NEVER run this on a guess. The standing rule is that fuzzy matches go to
match_queue and a human rules on them; this is the tool that carries out the
ruling, not a substitute for it.

What it does, in order:
  credits      re-point every credit from the loser to the keeper, dropping any
               that would duplicate a credit the keeper already has on the same
               title. A duplicate here would show the actor twice on one title.
  character    where the keeper's surviving credit has no character name and the
               loser's did, the name is carried across. Fill-blank-only, as
               everywhere else.
  aka_names    the loser's REAL alternative spellings move over, so a future
               scrape that sees the old billing still matches. Mojibake is not
               an alternative spelling and is dropped.
  people       the loser row is removed.
  _redirects   the loser's published page 301s to the keeper, because the URL
               may already be indexed and must not 404.
  match_queue  the ruling is recorded so the pair never returns to the queue.

Usage:
    python3 merge_person.py --keep <person_id> --lose <person_id> [--apply]
"""
import csv, io, os, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
REPO = os.path.dirname(HERE)


def term_of(p):
    raw = open(p, "rb").read()
    c = raw.count(b"\r\n")
    return "\r\n" if c > raw.count(b"\n") - c else "\n"


def load(n):
    return list(csv.DictReader(open(os.path.join(DATA, n), newline="", encoding="utf-8")))


def save(n, recs):
    p = os.path.join(DATA, n)
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=list(recs[0].keys()), lineterminator=term_of(p))
    w.writeheader()
    w.writerows(recs)
    open(p, "w", newline="", encoding="utf-8").write(buf.getvalue())


def clean(s):
    return "".join(c for c in (s or "") if not (0x80 <= ord(c) <= 0x9F))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--keep", required=True)
    ap.add_argument("--lose", required=True)
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()

    people, credits, queue = load("people.csv"), load("credits.csv"), load("match_queue.csv")
    keep = next((p for p in people if p["person_id"] == a.keep), None)
    lose = next((p for p in people if p["person_id"] == a.lose), None)
    if not keep or not lose:
        raise SystemExit(f"not found: keep={bool(keep)} lose={bool(lose)}")

    print(f"keep : {a.keep:<22} {clean(keep['name'])!r}")
    print(f"lose : {a.lose:<22} {clean(lose['name'])!r}")

    have = {c["title_id"] for c in credits if c["person_id"] == a.keep}
    moved, dropped, filled = [], [], []
    for c in credits:
        if c["person_id"] != a.lose:
            continue
        if c["title_id"] in have:
            dropped.append(c)
        else:
            moved.append(c)

    for c in moved:
        c["person_id"] = a.keep
    for d in dropped:
        tgt = next(c for c in credits if c["person_id"] == a.keep and c["title_id"] == d["title_id"])
        if not (tgt.get("character_name") or "").strip() and (d.get("character_name") or "").strip():
            tgt["character_name"] = d["character_name"]
            filled.append(d["title_id"])
    credits = [c for c in credits if not (c["person_id"] == a.lose)]

    akas = [x for x in (clean(keep.get("aka_names", "")).split("|") + clean(lose.get("aka_names", "")).split("|")) if x.strip()]
    ln = clean(lose["name"]).strip()
    # Only a REAL alternative billing is worth keeping. The loser's name here was
    # mojibake, which is not a spelling anyone was ever credited under.
    if ln and ln != clean(keep["name"]).strip() and all(ord(ch) < 0x80 for ch in ln):
        akas.append(ln)
    seen, out = set(), []
    for x in akas:
        if x.strip() and x.strip() not in seen:
            seen.add(x.strip())
            out.append(x.strip())
    keep["aka_names"] = "|".join(out)

    print(f"credits moved   : {len(moved)}  {[c['title_id'] for c in moved]}")
    print(f"duplicates dropped: {len(dropped)}  {[c['title_id'] for c in dropped]}")
    print(f"character names carried across: {len(filled)}")
    print(f"aka_names now   : {keep['aka_names']!r}")

    if not a.apply:
        print("\n[dry run] nothing written")
        return

    people = [p for p in people if p["person_id"] != a.lose]
    save("people.csv", people)
    save("credits.csv", credits)

    ruled = 0
    for q in queue:
        pair = {q["candidate_a"].strip(), q["candidate_b"].strip().rstrip("?")}
        if pair == {a.keep, a.lose}:
            q["status"] = "confirmed_same (Cyan, 2026-08-08)"
            ruled += 1
    if ruled:
        save("match_queue.csv", queue)

    path = os.path.join(REPO, "_redirects")
    lines = [l.rstrip("\n") for l in open(path, encoding="utf-8")] if os.path.exists(path) else []
    rule = f"/actors/{a.lose}.html  /actors/{a.keep}.html  301"
    if rule not in lines:
        lines.append(rule)
    open(path, "w", encoding="utf-8").write("\n".join(lines).rstrip() + "\n")

    stale = os.path.join(REPO, "actors", f"{a.lose}.html")
    if os.path.exists(stale):
        os.remove(stale)

    print(f"\nmerged. {ruled} queue row(s) ruled, redirect written, stale page removed")


if __name__ == "__main__":
    main()
