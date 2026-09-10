#!/usr/bin/env python3
"""Merge one title record into another, after a human ruling.

The sibling of merge_person.py, born 10 Sep 2026 when Cyan ruled that
"The Billionaire Heiress's Double Life" (a 2026 ReelShort relisting,
996K views) is "The Double Life of a Billionaire Heiress" (2024, 178.6M).
ReelShort publishes the same show under a new listing and a new name;
this is what carries the ruling out. NEVER run it on a guess.

What it does, in order:
  credits       re-point every credit from the loser to the keeper, dropping
                any that would duplicate a credit the keeper already has, and
                carrying a character name across where the keeper's was blank.
  tropes        the loser's join the keeper's tropes column, deduplicated;
  pinned        re-pointed, deduplicated.
  availability  the loser's platform rows are dropped when the keeper already
                has that platform (two Watch buttons for one app is a lie), and
                re-pointed otherwise. The dropped link is kept in the keeper's
                source_urls so the relisting's book id is on record.
  snapshots     the loser's are dropped: a relisting counts from zero and
                would wreck the keeper's trend.
  alt_titles    the loser's name (and its alts) join the keeper's, so the
                weekly scrape matches the relisting by name and holds it for
                a ruling instead of creating it again.
  titles        the loser row is removed.
  _redirects    the loser's page 301s to the keeper (the URL may be indexed).
  match_queue   the ruling is recorded so the pair never returns unanswered.

Usage:
    python3 generator/merge_title.py --keep <title_id> --lose <title_id> [--apply]
"""
import argparse, csv, datetime, io, os

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


def uniq(xs):
    seen, out = set(), []
    for x in xs:
        x = (x or "").strip()
        if x and x not in seen:
            seen.add(x); out.append(x)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--keep", required=True)
    ap.add_argument("--lose", required=True)
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()

    titles = load("titles.csv")
    keep = next((t for t in titles if t["title_id"] == a.keep), None)
    lose = next((t for t in titles if t["title_id"] == a.lose), None)
    if not keep or not lose:
        raise SystemExit(f"not found: keep={bool(keep)} lose={bool(lose)}")
    print(f"keep : {a.keep}  {keep['primary_title']!r}")
    print(f"lose : {a.lose}  {lose['primary_title']!r}")

    credits = load("credits.csv")
    have = {c["person_id"] for c in credits if c["title_id"] == a.keep}
    moved, dropped, filled = [], [], []
    for c in credits:
        if c["title_id"] != a.lose:
            continue
        (dropped if c["person_id"] in have else moved).append(c)
    for c in moved:
        c["title_id"] = a.keep
    for d in dropped:
        tgt = next(c for c in credits if c["title_id"] == a.keep and c["person_id"] == d["person_id"])
        if not (tgt.get("character_name") or "").strip() and (d.get("character_name") or "").strip():
            tgt["character_name"] = d["character_name"]; filled.append(d["person_id"])
    credits = [c for c in credits if c["title_id"] != a.lose]
    print(f"credits moved {len(moved)}, duplicates dropped {len(dropped)}, characters carried {len(filled)}")

    def repoint(name, keyfield):
        rows = load(name)
        has = {r[keyfield] for r in rows if r["title_id"] == a.keep}
        out, n_moved, n_dropped = [], 0, 0
        for r in rows:
            if r["title_id"] == a.lose:
                if r[keyfield] in has:
                    n_dropped += 1; continue
                r["title_id"] = a.keep; n_moved += 1
            out.append(r)
        print(f"{name}: moved {n_moved}, dropped {n_dropped}")
        return out
    # tropes.csv is the vocabulary (name, count), not a title link table: a
    # title's tropes live in its own tropes column, so the loser's join the
    # keeper's there. build.py recounts the vocabulary on every run.
    keep["tropes"] = ";".join(uniq((keep.get("tropes") or "").split(";") + (lose.get("tropes") or "").split(";")))
    pinned = repoint("pinned.csv", "rail") if os.path.exists(os.path.join(DATA, "pinned.csv")) else None

    avail = load("availability.csv")
    keep_plats = {r["platform_id"] for r in avail if r["title_id"] == a.keep}
    extra_urls, out = [], []
    for r in avail:
        if r["title_id"] == a.lose:
            if r["platform_id"] in keep_plats:
                if (r.get("direct_link") or "").strip():
                    extra_urls.append(r["direct_link"].strip())
                continue
            r["title_id"] = a.keep
        out.append(r)
    avail = out
    print(f"availability: relisting links banked in source_urls: {extra_urls}")

    snaps = [s for s in load("snapshots.csv") if s["title_id"] != a.lose]

    alts = uniq((keep.get("alt_titles") or "").split(";") + [lose["primary_title"]]
                + (lose.get("alt_titles") or "").split(";"))
    alts = [x for x in alts if x != keep["primary_title"]]
    keep["alt_titles"] = ";".join(alts)
    keep["source_urls"] = ";".join(uniq((keep.get("source_urls") or "").split(";")
                                        + (lose.get("source_urls") or "").split(";") + extra_urls))
    for f in ("poster_ref", "year", "episode_count", "book", "imdb_id"):
        if not (keep.get(f) or "").strip() and (lose.get(f) or "").strip():
            keep[f] = lose[f]
    print(f"alt_titles now: {keep['alt_titles']!r}")

    if not a.apply:
        print("\n[dry run] nothing written")
        return

    save("titles.csv", [t for t in titles if t["title_id"] != a.lose])
    save("credits.csv", credits)
    if pinned: save("pinned.csv", pinned)
    save("availability.csv", avail)
    save("snapshots.csv", snaps)

    queue = load("match_queue.csv")
    today = datetime.date.today().isoformat()
    queue.append({"candidate_a": f"{a.keep} (existing title)",
                  "candidate_b": f"{a.lose} (ReelShort relisting, {lose['primary_title']})",
                  "evidence": "Same cast (Marc Herrmann, Kelsey C Lynn, Michael Ursu), same episode count, same tropes; a later ReelShort listing under a new name.",
                  "status": f"confirmed_same (Cyan, {today})"})
    save("match_queue.csv", queue)

    path = os.path.join(REPO, "_redirects")
    lines = [l.rstrip("\n") for l in open(path, encoding="utf-8")]
    rule = f"/titles/{a.lose}.html  /titles/{a.keep}.html  301"
    if rule not in lines:
        # BEFORE the generic /:slug rules, never appended after them: :slug
        # matches "name.html" as one segment, so a specific rule placed later
        # never fires and the old URL 301s to name.html.html forever
        # (found live 10 Sep 2026). check_site guards the order.
        first = next((i for i, l in enumerate(lines) if ":slug" in l), len(lines))
        while first > 0 and lines[first - 1].startswith("#"):
            first -= 1
        lines.insert(first, rule)
    open(path, "w", encoding="utf-8").write("\n".join(lines).rstrip() + "\n")
    for stale in (os.path.join(REPO, "titles", f"{a.lose}.html"),):
        if os.path.exists(stale): os.remove(stale)
    print("\nmerged. queue row recorded, redirect written, stale page removed")


if __name__ == "__main__":
    main()
