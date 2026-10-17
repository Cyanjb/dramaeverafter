#!/usr/bin/env python3
"""Build the 14 Oct 2026 DramaBox staging file from Cyan's chosen list.

Also used 17 Oct 2026 for 5 DramaBox shows from her app screenshots (selection_1017).
Cyan, 14 Oct 2026: "check what else we have missed on DramaBox ... I am
looking for high performing, popular, trending and favorite shows", then
"sounds like a plan" to adding every missing DramaBox show with 10M+ real
plays plus the Reddit / wanted-file favourites found on DramaBox (127 books).

Inputs, made in the session:
  - a full scrape_dramabox.py run (trending, home, channels, known, cast,
    detail; 621 books, 0 errors), and
  - a walk of the English catalogue /genres/0/1..250 (2,894 books shelved
    since 29 Jul; its listing play counts are capped, so plays come from each
    /movie/ page).
  - the chosen book ids (selection.json: "selected", "need_detail").

This script reads the /movie/ page of every chosen book the scrape did not
already read (the merge never creates a book it has not read on its own
page), marks every chosen book with seen_via "cyan_list", and writes ONE
staging file holding the books we already hold (so their play counts
refresh; the weekly run has been 403 since 28 Sep) plus the chosen ones.
Books neither held nor chosen are left out, so the merge creates exactly
Cyan's list. merge_dramabox.py treats "cyan_list" as chosen.

Usage:
  python3 generator/select_dramabox_2026_10_14.py SCRAPE.json SELECTION.json OUT.json
"""
import datetime, io, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import scrape_dramabox as sd


def main(scrape_path, sel_path, out_path):
    doc = json.load(io.open(scrape_path, encoding="utf-8"))
    sel = json.load(io.open(sel_path, encoding="utf-8"))
    fetch = sd.Fetcher(tuple(sd.PAUSE))
    st, body = fetch.get(sd.BASE + "/robots.txt", check_robots=False)
    if st == 200:
        fetch.robots = sd.robots_rules(body)
    run = sd.Run(fetch)
    for bid, b in doc["books"].items():
        b = dict(b); vias = b.pop("seen_via", []) or []
        cur = run.note(b, vias[0] if vias else "earlier", fresh=False)
        for v in vias:
            if v not in cur["seen_via"]:
                cur["seen_via"].append(v)
    run.performers.update(doc.get("performers") or {})
    run.detail([(bid, "") for bid in sel["need_detail"]], "detail")
    chosen = set(sel["selected"])
    keep = {}
    for bid, b in run.books.items():
        if bid in chosen:
            if "cyan_list" not in b["seen_via"]:
                b["seen_via"].append("cyan_list")
            keep[bid] = b
        elif b.get("known_title_id"):
            keep[bid] = b
    out = dict(doc)
    out["books"] = keep
    out["performers"] = run.performers
    out["errors"] = list(doc.get("errors") or []) + run.errors
    out["delisted"] = list(doc.get("delisted") or []) + run.delisted
    out["selection"] = {"made": datetime.date.today().isoformat(), "chosen": len(chosen),
                        "kept": len(keep), "note": "Cyan's 14 Oct list; see this script's docstring"}
    json.dump(out, io.open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    missing = chosen - set(keep)
    print("kept %d books (%d chosen, %d held); chosen but unread: %d"
          % (len(keep), len(chosen & set(keep)), len(keep) - len(chosen & set(keep)), len(missing)))


if __name__ == "__main__":
    main(*sys.argv[1:4])
