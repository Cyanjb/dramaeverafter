#!/usr/bin/env python3
"""What Google already sends us that we are not serving.

    python3 generator/gsc_opportunities.py <folder with a GSC Queries.csv> [...]

Born 6 Sep 2026 from one question: why did
/titles/eng-dub-apocalypse-romance-system.html earn 76 clicks, five times
the site's average CTR, while pages with more data earned none? The answer
was in the query export: it ranked for "romance system made me the king of
the apocalypse", a GoodShort listing we did not hold at all. Google had
demand, we had the nearest page, and the click landed by accident.

So this reads a Search Console query export and prints the accidents worth
turning into intent:

  UNSERVED   queries we rank for whose subject is in no title or actor row.
             Each is a title we could add or an alt name we could record.
  BLIND SPOT high impressions, zero clicks, decent position. Google offers
             us the traffic every day and nobody takes it, which usually
             means the page cannot answer the question (an actor's age, a
             cast list we do not hold).
  INTENT     clicks and CTR grouped by what the searcher wanted. The 6 Sep
             read: watch intent converts near 15%, cast and age intent near
             1%. Chase the first, fix the data behind the second.

Nothing here writes to the database. It prints a list for a human to rule
on, because every fix is a judgement call about what is really the same show.
"""
import csv, os, re, sys, unicodedata
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def norm(s):
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower().replace("’", "").replace("'", "").replace("`", "")
    return " ".join(re.sub(r"[^a-z0-9]+", " ", s).split())


# Words that describe what the searcher wants, not which show they want. The
# subject of a query is what is left once these are gone.
MODIFIERS = {"cast", "full", "free", "episode", "episodes", "watch", "drama",
             "dramas", "actor", "actress", "dub", "dubbed", "list", "app",
             "where", "season", "online", "movie", "movies", "series", "short",
             "verticals", "vertical", "reelshort", "goodshort", "dramabox",
             "shortmax", "the", "a", "an", "of", "to", "in", "is", "my", "age",
             "edad", "wiki", "trailer", "review", "recap", "ending"}

INTENTS = [
    ("watch it now", r"\b(where to watch|watch|free|full movie|full episode|full|online|streaming|app)\b"),
    ("who is in it", r"\b(cast|actor|actress|who plays|starring)\b"),
    ("about the actor", r"\b(age|edad|born|birthday|real name|instagram|wife|husband|dating|married|height)\b"),
    ("their other work", r"\b(drama list|dramas|verticals|movies|filmography|shows)\b"),
    ("browsing a type", r"\b(vertical drama|short drama|micro drama|best|top|like|similar)\b"),
]


def subject(q):
    """What the searcher is asking ABOUT, once the asking words are gone.
    Both sides of every comparison go through this, or a query loses "my"
    while the title keeps it and a match we hold looks like a gap."""
    return " ".join(w for w in norm(q).split() if w not in MODIFIERS)


def load_known():
    def rows(n):
        with open(os.path.join(ROOT, "data", n), encoding="utf-8") as f:
            return list(csv.DictReader(f))
    known = set()
    for t in rows("titles.csv"):
        for name in [t["primary_title"]] + (t.get("alt_titles") or "").split(";"):
            if subject(name):
                known.add(subject(name))
    for p in rows("people.csv"):
        for name in [p["name"]] + (p.get("aka_names") or "").split(";"):
            if subject(name):
                known.add(subject(name))
    return known


def main(dirs):
    known = load_known()
    seen, rows = set(), []
    for d in dirs:
        f = d if d.endswith(".csv") else os.path.join(d, "Queries.csv")
        if not os.path.exists(f):
            print(f"  (no Queries.csv in {d})")
            continue
        for r in csv.DictReader(open(f, encoding="utf-8-sig")):
            q = r.get("Top queries") or r.get("Query") or ""
            if not q or q in seen:
                continue
            seen.add(q)
            rows.append((q, int(r["Clicks"]), int(r["Impressions"]), float(r["Position"])))
    if not rows:
        print("No query rows found. Export Performance > Queries from Search Console.")
        return 1

    clicks = sum(r[1] for r in rows)
    print(f"{len(rows)} queries, {clicks} clicks, {sum(r[2] for r in rows)} impressions\n")

    unserved = []
    for q, c, i, pos in rows:
        s = subject(q)
        if len(s) < 8:            # too short to be a title; a generic phrase
            continue
        if s in known:
            continue
        # A subject wholly inside something we hold is a partial match, not a gap.
        if any(s in k for k in known if len(k) > 12):
            continue
        unserved.append((c, i, pos, q, s))

    print("== UNSERVED: we rank for it, we do not hold it ==")
    print("   (add the title, or record it as an alt name on the show it really is)")
    for c, i, pos, q, s in sorted(unserved, reverse=True)[:30]:
        print(f"   {c:3} clicks {i:5} impr  pos {pos:5.1f}  {q}")
    print(f"   ... {len(unserved)} in all, {sum(u[0] for u in unserved)} clicks,"
          f" {sum(u[1] for u in unserved)} impressions\n")

    print("== BLIND SPOTS: Google offers, nobody takes ==")
    print("   (top-10 position, 15+ impressions, zero clicks: the page cannot answer it)")
    blind = [r for r in rows if r[1] == 0 and r[2] >= 15 and r[3] <= 10.5]
    for q, c, i, pos in sorted(blind, key=lambda r: -r[2])[:25]:
        print(f"   {i:5} impr  pos {pos:5.1f}  {q}")
    print(f"   ... {len(blind)} in all, {sum(b[2] for b in blind)} impressions going nowhere\n")

    print("== INTENT: what converts ==")
    tally = defaultdict(lambda: [0, 0, 0])
    for q, c, i, pos in rows:
        ql = q.lower()
        for name, pat in INTENTS:
            if re.search(pat, ql):
                t = tally[name]
                t[0] += 1; t[1] += c; t[2] += i
    print(f"   {'wants':18} {'queries':>8} {'clicks':>7} {'impr':>7} {'CTR':>7}")
    for name, _ in INTENTS:
        n, c, i = tally[name]
        print(f"   {name:18} {n:8} {c:7} {i:7} {100 * c / i if i else 0:6.2f}%")
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1:]))
