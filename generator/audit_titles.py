#!/usr/bin/env python3
"""Find title rows that are the same show twice, and tell them from sequels.

    python3 generator/audit_titles.py [--min 0.90]

Born 13 Sep 2026: Cyan spotted "FoulPlay For My Brother's Best Friend" and
"Foul Play with My Brother's Best Friend" both on Evan Adams' page, one
carrying the cast and the other the year and tropes. Two sources spelling a
title differently is how that happens, so it will keep happening.

THE HARD PART IS NOT FINDING PAIRS, IT IS NOT MERGING SEQUELS. A vertical
drama catalogue is full of "X" and "X 2", which are near-identical strings
and different shows. Those are excluded by name before anything else.

Verdicts, most confident first:
  TYPO     the two titles normalise to the same letters, or differ only by an
           accent or a doubled letter, AND they share a platform or a cast
           member. One show, two spellings.
  STUB     one row has no cast, no synopsis, no poster and no link, and the
           other has some. Nothing is lost by folding the empty one in.
  REVIEW   similar names, but the evidence does not settle it. Same name on
           two platforms can be a genuine relisting or two different shows,
           and only a human can say.

Nothing is written. Merge with generator/merge_title.py, passing --evidence.
"""
import argparse, collections, csv, difflib, os, re, sys, unicodedata

DATA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
SEQ = re.compile(r"\s*(?:part\s*)?(?:[0-9]{1,2}|i{1,3}v?|vi{0,3}|ix|xi{0,2})$", re.I)


def load(n):
    return list(csv.DictReader(open(os.path.join(DATA, n), newline="", encoding="utf-8")))


def fold(s):
    """Letters only, accents stripped, curly quotes flattened."""
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]", "", s.lower())


def stem(s):
    """The title with a trailing part/sequel marker removed."""
    s = re.sub(r"[‘’]", "'", s or "").strip()
    prev = None
    while prev != s:
        prev, s = s, SEQ.sub("", s).strip(" :-")
    return s


def main(min_ratio):
    titles = load("titles.csv")
    cred, avail = collections.defaultdict(set), collections.defaultdict(set)
    for c in load("credits.csv"):
        cred[c["title_id"]].add(c["person_id"])
    for a in load("availability.csv"):
        avail[a["title_id"]].add(a["platform_id"])

    def empty(r):
        return not any((r.get(f) or "").strip() for f in ("synopsis_short", "poster_ref")) \
            and not cred[r["title_id"]] \
            and not any((a.get("direct_link") or "").strip() for a in [{}])

    # A pair already ruled DIFFERENT is not asked again (24 Sep 2026: eleven
    # REVIEW pairs were distinct shows by episode count, cast or story, and
    # would otherwise come back every run). The ruling row names both ids.
    ruled = {frozenset((q["candidate_a"].split()[0], q["candidate_b"].split()[0]))
             for q in load("match_queue.csv")
             if (q.get("status") or "").startswith("ruled_different")
             and q.get("candidate_a") and q.get("candidate_b")}

    by_len = collections.defaultdict(list)
    keyed =[(fold(r["primary_title"]), r) for r in titles if r["primary_title"].strip()]
    for k, r in keyed:
        by_len[len(k)].append((k, r))

    out, seen = [], set()
    for L in sorted(by_len):
        cand = [x for M in range(L - 3, L + 4) for x in by_len.get(M, [])]
        for k, r in by_len[L]:
            for k2, r2 in cand:
                if r2["title_id"] <= r["title_id"]:
                    continue
                if abs(len(k) - len(k2)) > 3:
                    continue
                if k[:6] != k2[:6] and k[-6:] != k2[-6:]:
                    continue
                if difflib.SequenceMatcher(None, k, k2).ratio() < min_ratio:
                    continue
                # SEQUELS ARE NOT DUPLICATES. Different stems after stripping a
                # trailing number means one is a sequel of the other.
                if stem(r["primary_title"]) != r["primary_title"] or stem(r2["primary_title"]) != r2["primary_title"]:
                    if fold(stem(r["primary_title"])) != fold(stem(r2["primary_title"])) or \
                       fold(r["primary_title"]) != fold(r2["primary_title"]):
                        continue
                key = (r["title_id"], r2["title_id"])
                if key in seen or frozenset(key) in ruled:
                    continue
                seen.add(key)
                shared_cast = cred[r["title_id"]] & cred[r2["title_id"]]
                shared_app = avail[r["title_id"]] & avail[r2["title_id"]]
                same_letters = k == k2
                thin = [x for x in (r, r2) if not cred[x["title_id"]]
                        and not (x.get("synopsis_short") or "").strip()
                        and not (x.get("poster_ref") or "").strip()]
                if (same_letters or difflib.SequenceMatcher(None, k, k2).ratio() >= 0.97) and (shared_cast or shared_app):
                    v = "TYPO"
                elif len(thin) == 1:
                    v = "STUB"
                else:
                    v = "REVIEW"
                out.append((v, r, r2, shared_cast, shared_app))

    order = {"TYPO": 0, "STUB": 1, "REVIEW": 2}
    out.sort(key=lambda x: (order[x[0]], x[1]["primary_title"]))
    for v in ("TYPO", "STUB", "REVIEW"):
        rows = [x for x in out if x[0] == v]
        print(f"\n== {v}: {len(rows)}")
        for _, r, r2, sc, sa in rows:
            print(f"  {r['title_id']}\n    vs {r2['title_id']}")
            print(f"    {r['primary_title']!r} [{','.join(sorted(avail[r['title_id']])) or 'no app'}, "
                  f"{len(cred[r['title_id']])} cast] vs {r2['primary_title']!r} "
                  f"[{','.join(sorted(avail[r2['title_id']])) or 'no app'}, {len(cred[r2['title_id']])} cast]"
                  + (f"  shared cast {len(sc)}" if sc else "") + (f"  shared app {','.join(sorted(sa))}" if sa else ""))
    print(f"\n{len(out)} pairs. Sequels excluded by name. Merge with merge_title.py --evidence.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--min", type=float, default=0.90)
    main(ap.parse_args().min)
