"""Merge the 73 '<slug>-pinedrama' duplicate titles into their twins and delete them.

CYAN'S RULING, 14 Aug 2026: delete the duplicates. Evidence recorded in adapters
and the session: all 73 are the SAME productions as their twins (byte-identical or
same-artwork posters on all 73 pairs, same characters in the one disputed synopsis),
and pinedrama.com is a fan/affiliate directory, not a platform.

MERGE BEFORE DELETE - the duplicates carry real data:
  credits    moved to the twin unless the (twin, person) pair already exists;
             where it exists, a blank character_name on the twin is filled from
             the duplicate. Nothing is overwritten.
  tropes     merged into the twin by slug (same story, same tropes).
  availability  rows on the duplicates were already re-pointed to official
             platforms on 14 Aug, so each row is kept ONLY if the twin does not
             already have that platform; otherwise it is a duplicate and dropped.
  match_queue   rows pairing a duplicate with its twin get
             status=confirmed_same (Cyan, 2026-08-14) rather than deletion,
             because rulings are history.

THE SLUGS WERE PUBLISHED URLS. 73 pages will 404 until Google recrawls, the same
accepted cost as the 43 withdrawn trope pages. The built HTML files are removed
here as well so the repo does not keep serving them.

Usage:
    py generator/merge_pinedrama_twins.py [--dry-run]
"""
import csv, io, os, re, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.environ.get("DEA_DATA") or os.path.join(HERE, "..", "data")
ROOT = os.path.abspath(os.path.join(HERE, ".."))
SUF = "-pinedrama"
DRY = "--dry-run" in sys.argv


def slugify(s):
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", (s or "").lower())).strip("-")


def term_of(p):
    raw = open(p, "rb").read()
    crlf = raw.count(b"\r\n")
    return "\r\n" if crlf > raw.count(b"\n") - crlf else "\n"


def load(n):
    p = os.path.join(DATA, n)
    return list(csv.DictReader(open(p, newline="", encoding="utf-8-sig"))), term_of(p)


def save(n, rows, term):
    p = os.path.join(DATA, n)
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=list(rows[0].keys()), lineterminator=term)
    w.writeheader()
    w.writerows(rows)
    open(p, "w", encoding="utf-8", newline="").write(buf.getvalue())


def main():
    titles, t_term = load("titles.csv")
    av, a_term = load("availability.csv")
    credits, c_term = load("credits.csv")
    queue, q_term = load("match_queue.csv")

    by_id = {t["title_id"]: t for t in titles}
    pine = [t for t in titles if t["title_id"].endswith(SUF)]
    twins = {t["title_id"]: t["title_id"][:-len(SUF)] for t in pine}
    missing_twin = [p for p, tw in twins.items() if tw not in by_id]
    if missing_twin:
        sys.exit(f"ABORT: {len(missing_twin)} duplicates have no twin: {missing_twin[:5]}")

    # ---- tropes: merge into twin by slug ----
    tropes_merged = 0
    for p, tw in twins.items():
        src, dst = by_id[p], by_id[tw]
        have = {slugify(x) for x in (dst["tropes"] or "").split(";") if x.strip()}
        cur = [x for x in (dst["tropes"] or "").split(";") if x.strip()]
        for x in (src["tropes"] or "").split(";"):
            x = x.strip()
            if x and slugify(x) not in have:
                cur.append(x)
                have.add(slugify(x))
                tropes_merged += 1
        dst["tropes"] = ";".join(cur)

    # ---- credits: move or fill ----
    existing = {(c["title_id"], c["person_id"]): c for c in credits}
    moved, filled, dropped_dup = 0, 0, 0
    for c in list(credits):
        tid = c["title_id"]
        if tid not in twins:
            continue
        tw = twins[tid]
        key = (tw, c["person_id"])
        if key in existing:
            ex = existing[key]
            if (c["character_name"] or "").strip() and not (ex["character_name"] or "").strip():
                ex["character_name"] = c["character_name"]
                filled += 1
            credits.remove(c)
            dropped_dup += 1
        else:
            c["title_id"] = tw
            existing[key] = c
            moved += 1

    # ---- availability: keep only platforms the twin lacks ----
    twin_plats = {}
    for r in av:
        twin_plats.setdefault(r["title_id"], set()).add(r["platform_id"])
    av_moved, av_dropped = 0, 0
    for r in list(av):
        tid = r["title_id"]
        if tid not in twins:
            continue
        tw = twins[tid]
        if r["platform_id"] in twin_plats.get(tw, set()):
            av.remove(r)
            av_dropped += 1
        else:
            r["title_id"] = tw
            twin_plats.setdefault(tw, set()).add(r["platform_id"])
            av_moved += 1

    # ---- match_queue: record the ruling ----
    ruled = 0
    for r in queue:
        joined = " ".join(v or "" for v in r.values())
        if SUF in joined and not (r["status"] or "").startswith("confirmed"):
            r["status"] = "confirmed_same (Cyan, 2026-08-14: pinedrama twins merged)"
            ruled += 1

    # ---- delete the title rows and the built pages ----
    titles = [t for t in titles if t["title_id"] not in twins]
    pages = [os.path.join(ROOT, "titles", f"{p}.html") for p in twins]
    pages = [p for p in pages if os.path.exists(p)]

    print(f"duplicates to delete   : {len(twins)}")
    print(f"tropes merged to twins : {tropes_merged}")
    print(f"credits moved          : {moved}")
    print(f"credits filled (char)  : {filled}")
    print(f"credit dupes dropped   : {dropped_dup}")
    print(f"availability moved     : {av_moved}")
    print(f"availability dupes out : {av_dropped}")
    print(f"match_queue rows ruled : {ruled}")
    print(f"built pages to remove  : {len(pages)}")

    if DRY:
        print("\n[dry-run] nothing written")
        return
    save("titles.csv", titles, t_term)
    save("availability.csv", av, a_term)
    save("credits.csv", credits, c_term)
    save("match_queue.csv", queue, q_term)
    for p in pages:
        os.remove(p)
    print("\nwritten all four CSVs, removed built pages")


if __name__ == "__main__":
    main()
