#!/usr/bin/env python3
"""Apply Cyan's "same show" rulings from the duplicate rulings page.

The page (https://claude.ai/artifact/GgB8EP94pCy1LND2omFm2Y) lists every
pending match_queue pair, built from staging/rulings_pairs_2026-10-06.json;
her taps are saved in its db as rulings/<key> {v: same|different|unsure}.
Export them to a JSON file {key: verdict} and run this.

For a SAME pair whose other listing is a DramaBox book in the 28 Sep scrape
record, the page we hold gets that book linked (fill-blank: episodes, poster,
year; views and a snapshot; a dub becomes a second english-dub row), and
DramaBox's cast is credited where a name matches exactly one person we hold.
Unknown cast names are created needs_check; close names are only reported.
The match_queue row is marked confirmed_same. Anything else (titles from
other platforms, DIFFERENT, actor pairs) is listed for hand handling.
Re-running is safe: a book already linked is skipped.

Usage: python3 generator/apply_same_rulings.py <verdicts.json> [--apply]
"""
import difflib, hashlib, json, os, re, sys, unicodedata
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from merge_scrape import load, save

TODAY = "2026-10-06"
PAIRS = json.load(open(os.path.join(HERE, "staging", "rulings_pairs_2026-10-06.json"), encoding="utf-8"))
DB = json.load(open(os.path.join(HERE, "staging", "dramabox_2026-09-28.json"), encoding="utf-8"))
BOOKS = {str(b["book_id"]): b for b in (DB["books"].values() if isinstance(DB["books"], dict) else DB["books"])}
JUNK = re.compile(r"^(?:Biography\s+)?(?:IMDbPro\s+)?", re.I)


def norm(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]", "", s.lower())


def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", s)).strip("-")


def main(path, apply):
    verdicts = json.load(open(path, encoding="utf-8"))
    T, tf = load("titles.csv"); A, af = load("availability.csv"); S, sf = load("snapshots.csv")
    C, cf = load("credits.csv"); P, pf = load("people.csv"); Q, qf = load("match_queue.csv")
    by = {t["title_id"]: t for t in T}
    names = {}
    for p in P:
        for n in [p["name"]] + re.split(r"[|;]", p.get("aka_names") or ""):
            if n.strip():
                names.setdefault(norm(n), set()).add(p["person_id"])
    pids = {p["person_id"] for p in P}
    held = {(c["title_id"], c["person_id"]) for c in C}
    qkey = {hashlib.sha1((r["candidate_a"] + "|" + r["candidate_b"]).encode()).hexdigest()[:12]: r for r in Q}
    done, other = [], []
    for pair in PAIRS:
        v = verdicts.get(pair["key"])
        if v != "same":
            continue
        row = qkey.get(pair["key"])
        m = re.search(r"dramaboxdb\.com/movie/(\d+)", pair["evidence"])
        tid = pair["a"]["id"]
        if pair["type"] == "person" or not m or m.group(1) not in BOOKS or tid not in by:
            other.append((pair["key"], pair["a"]["name"], pair["b"]["name"])); continue
        bid = m.group(1); b = BOOKS[bid]
        if any(bid in (r["direct_link"] or "") for r in A):
            if row is not None and row["status"] == "pending":
                row["status"] = "confirmed_same (Cyan, %s, rulings page)" % TODAY
            continue
        A.append({k: "" for k in af} | {"title_id": tid, "platform_id": "dramabox", "title_as_listed_on_platform": b.get("title"),
                  "direct_link": b.get("url") or "https://www.dramaboxdb.com/movie/%s" % bid,
                  "view_count": b.get("views") or "", "view_count_date": "2026-09-28" if b.get("views") else "",
                  "last_checked": TODAY, "version": "english-dub" if b.get("dubbed") else ""})
        if b.get("views"):
            S.append({k: "" for k in sf} | {"title_id": tid, "platform_id": "dramabox", "view_count": b["views"], "date": "2026-09-28"})
        t = by[tid]
        if not b.get("dubbed"):
            for col, val in (("episode_count", b.get("episodes")), ("poster_ref", b.get("poster")), ("year", b.get("year"))):
                if val and not t.get(col):
                    t[col] = str(val)
        for c in b.get("cast") or []:
            name = JUNK.sub("", c["name"]).strip(); ids = names.get(norm(name), set())
            if len(ids) == 1:
                pid = next(iter(ids))
            elif ids:
                continue
            elif difflib.get_close_matches(norm(name), list(names), n=1, cutoff=0.9):
                print("  close name, not credited:", name, "on", tid); continue
            else:
                pid = slug(name)
                if pid in pids:
                    continue
                P.append({k: "" for k in pf} | {"person_id": pid, "slug": pid, "name": name, "role_type": "actor",
                                                 "data_confidence": "needs_check", "source": "dramabox_cast_%s" % TODAY})
                pids.add(pid); names[norm(name)] = {pid}
            if (tid, pid) not in held:
                C.append({k: "" for k in cf} | {"title_id": tid, "person_id": pid, "role": "actor"}); held.add((tid, pid))
        if row is not None:
            row["status"] = "confirmed_same (Cyan, %s, rulings page)" % TODAY
        done.append("%s <- DramaBox %s%s" % (tid, bid, " (dub)" if b.get("dubbed") else ""))
    print("linked %d:" % len(done)); [print("  " + d) for d in done]
    if other:
        print("needs hand handling %d:" % len(other)); [print("  ", *o) for o in other]
    if apply:
        for n, f, r in (("titles.csv", tf, T), ("availability.csv", af, A), ("snapshots.csv", sf, S),
                        ("credits.csv", cf, C), ("people.csv", pf, P), ("match_queue.csv", qf, Q)):
            save(n, f, r)
        print("applied")


if __name__ == "__main__":
    main(sys.argv[1], "--apply" in sys.argv)
