#!/usr/bin/env python3
"""Find credits filed on the wrong show, with ReelShort's own evidence.

    python3 generator/audit_credits.py <reelshort staging json> [--apply]

Born 10 Sep 2026 from Falling for My Ex's Mafia Dad, which carried the
Hargroves from Love Is a Dangerous Dance: the reelshort_fandom_cast
source sometimes files one show's cast on another. The tell is an actor
credited as the SAME character on two shows that are not sequels.

Evidence: the weekly scrape reads every actor's ReelShort tag page, and
a book's "actors" list in the staging record is exactly the actors whose
tag pages list it. So for a suspicious pair the record says, per show,
whether ReelShort itself puts the actor in it.

Verdicts, per (actor, character) credited on two unrelated shows:
  REMOVE   the actor's tag page was read (lists at least one book), it
           lists the other show, and it does not list this one. Both
           signals together; either alone is not enough (tag pages miss
           ~10% of real credits, so absence alone never removes).
  KEEP     both shows on the tag page: the actor is in both; a repeated
           character may be a spin-off. Cyan's eye, not a rule.
  UNKNOWN  no tag page, or the show is not in the record.

--apply removes the REMOVE credits and writes the log next to the
staging file. Sequels are excluded by name (shared leading words, or
one title containing the other). Nothing here invents a character.
"""
import csv, io, json, os, re, sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
MOVIE = re.compile(r"/movie/[^/]*?-([0-9a-f]{24})")


def load(n):
    return list(csv.DictReader(open(os.path.join(DATA, n), newline="", encoding="utf-8")))


def save(n, recs):
    p = os.path.join(DATA, n)
    raw = open(p, "rb").read()
    term = "\r\n" if raw.count(b"\r\n") > raw.count(b"\n") - raw.count(b"\r\n") else "\n"
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=list(recs[0].keys()), lineterminator=term)
    w.writeheader(); w.writerows(recs)
    open(p, "w", newline="", encoding="utf-8").write(buf.getvalue())


def words(s):
    return re.sub(r"[^a-z0-9 ]", " ", s.lower()).split()


def sequels(a, b):
    wa, wb = words(a), words(b)
    if not wa or not wb: return False
    if " ".join(wa) in " ".join(wb) or " ".join(wb) in " ".join(wa): return True
    return wa[:2] == wb[:2]


def main(staging, apply):
    books = json.load(open(staging, encoding="utf-8")).get("books") or {}
    titles = {t["title_id"]: t for t in load("titles.csv")}
    people = {p["person_id"]: p for p in load("people.csv")}
    bid_of = {}
    for r in load("availability.csv"):
        m = MOVIE.search(r.get("direct_link") or "")
        if m and r["platform_id"] == "reelshort": bid_of.setdefault(r["title_id"], m.group(1))
    on_tag = defaultdict(set)   # actor name (lower) -> book ids the tag page lists
    for bid, b in books.items():
        for a in b.get("actors") or []: on_tag[a.strip().lower()].add(bid)

    credits = load("credits.csv")
    pairs = defaultdict(list)
    for c in credits:
        ch = (c.get("character_name") or "").strip()
        if ch: pairs[(c["person_id"], ch)].append(c)

    remove, keep, unknown = [], [], []
    for (pid, ch), cs in sorted(pairs.items()):
        tids = sorted({c["title_id"] for c in cs})
        if len(tids) < 2: continue
        names = [titles.get(t, {}).get("primary_title", t) for t in tids]
        if all(sequels(names[0], n) for n in names[1:]): continue
        name = people.get(pid, {}).get("name", pid).strip().lower()
        tag = on_tag.get(name, set())
        listed = {t: (bid_of[t] in tag) if t in bid_of and tag else None for t in tids}
        if not tag or None in listed.values():
            unknown.append((pid, ch, listed)); continue
        yes = [t for t, v in listed.items() if v]
        no = [t for t, v in listed.items() if v is False]
        if yes and no:
            for t in no: remove.append((pid, ch, t, yes))
        else:
            keep.append((pid, ch, listed))

    print(f"REMOVE {len(remove)} (tag page lists the other show, not this one):")
    for pid, ch, t, yes in remove: print(f"  {pid:22} {ch:24} off {t}   (on {', '.join(yes)})")
    print(f"KEEP {len(keep)} (actor on both shows per ReelShort; the repeated character is Cyan's call):")
    for pid, ch, l in keep: print(f"  {pid:22} {ch:24} {', '.join(l)}")
    print(f"UNKNOWN {len(unknown)} (no tag page read, or a show not in the record):")
    for pid, ch, l in unknown: print(f"  {pid:22} {ch:24} " + "  ".join(f"{t}={'?' if v is None else v}" for t, v in l.items()))

    if not apply or not remove:
        return
    gone = {(pid, t) for pid, ch, t, _ in remove}
    before = len(credits)
    credits = [c for c in credits if (c["person_id"], c["title_id"]) not in gone]
    save("credits.csv", credits)
    log = os.path.join(os.path.dirname(staging), "credits_removed_%s.json" % os.path.basename(staging)[10:20])
    json.dump([{"person_id": pid, "character": ch, "title_id": t, "tag_page_lists": yes} for pid, ch, t, yes in remove],
              open(log, "w", encoding="utf-8"), indent=1)
    print(f"\nremoved {before - len(credits)} credits; log: {log}")


if __name__ == "__main__":
    if len(sys.argv) < 2: sys.exit(__doc__)
    main(sys.argv[1], "--apply" in sys.argv)
