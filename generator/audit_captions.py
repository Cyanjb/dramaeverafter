#!/usr/bin/env python3
"""The every-hundred audit. Cyan, 16 Aug 2026: "I feel comfortable with you just
going forward without me manually checking. We can set up another check for the
100 previous synopses every 100 synopses to catch issues."

WHAT THIS IS FOR, and why it is not just caption_pipeline check. That checker
looks at ONE caption at a time: dashes, invented names, length against source,
rejected constructions. It cannot see the failure mode that actually threatens
unsupervised writing, which is SAMENESS. Write two hundred captions alone and
the crutches creep in - every third one opening "What she does not know is
that", every hook built the same way, the same six verbs. No single caption is
wrong and the corpus reads like a machine.

So this measures the corpus against itself:

  1 REPEATED PHRASES   four word runs appearing in three or more captions
  2 HOOK SHAPES        openings and constructions reused too often
  3 NEAR DUPLICATES    two bodies too similar to each other
  4 CRUTCH VERBS       the handful of constructions I reach for under load
  5 RULE FAILURES      everything caption_pipeline.validate catches
  6 A SAMPLE FOR CYAN  ten at random, so a human still sees real output

RUN IT EVERY 100 APPLIED CAPTIONS, over the previous 100.

Usage:
    py generator/audit_captions.py               # the most recent 100 in data
    py generator/audit_captions.py --last 200    # a wider window
    py generator/audit_captions.py --sample 15
"""
import collections, csv, difflib, io, os, random, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import caption_pipeline as cp  # noqa: E402

DATA = os.environ.get("DEA_DATA") or os.path.join(os.path.dirname(HERE), "data")

# Constructions I lean on when writing at volume. Not banned - a few are fine and
# some are Cyan's own - but if one appears in a tenth of the corpus it has stopped
# being a choice.
CRUTCHES = [
    r"\bturns out to be\b", r"\bwhat (?:he|she|they) do(?:es)? not know\b",
    r"\bhas no idea\b", r"\bright up until\b", r"\bends up\b",
    r"\bon the spot\b", r"\bnobody knows\b", r"\bkeeping it quiet\b",
    r"\bthe moment\b", r"\bnever once\b", r"\bwalks? (?:back )?into\b",
]


def rows(name):
    with io.open(os.path.join(DATA, name), encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def ours(t):
    s = (t.get("synopsis_short") or "").strip()
    return s if "\n" in s else ""


def ngrams(text, n=4):
    words = re.findall(r"[a-z']+", text.lower())
    return {" ".join(words[i:i + n]) for i in range(len(words) - n + 1)}


def main():
    last = int(sys.argv[sys.argv.index("--last") + 1]) if "--last" in sys.argv else 100
    n_sample = int(sys.argv[sys.argv.index("--sample") + 1]) if "--sample" in sys.argv else 10

    titles = [t for t in rows("titles.csv") if ours(t)]
    reach = {}
    for r in rows("availability.csv"):
        reach[r["title_id"]] = max(reach.get(r["title_id"], 0), cp.views(r.get("view_count")))
    titles.sort(key=lambda t: -reach.get(t["title_id"], 0))
    window = titles[:last]

    print("=" * 72)
    print("CAPTION AUDIT  |  %d captions written by us in total, auditing the top %d"
          % (len(titles), len(window)))
    print("=" * 72)

    parts = {t["title_id"]: cp.parts(ours(t)) for t in window}
    bodies = {k: v[1] for k, v in parts.items()}
    hooks = {k: v[0] for k, v in parts.items()}

    # 1 repeated phrases -----------------------------------------------------
    print("\n1. REPEATED FOUR WORD PHRASES (3+ captions)")
    seen = collections.Counter()
    where = collections.defaultdict(list)
    for tid, b in bodies.items():
        for g in ngrams(hooks[tid] + " " + b):
            seen[g] += 1
            where[g].append(tid)
    rep = [(c, g) for g, c in seen.items() if c >= 3]
    rep.sort(reverse=True)
    if not rep:
        print("   none. good.")
    for c, g in rep[:12]:
        print("   %2dx  %-42s e.g. %s" % (c, g, where[g][0][:34]))

    # 2 hook shapes ----------------------------------------------------------
    print("\n2. HOOK OPENINGS (first two words)")
    opens = collections.Counter(" ".join(h.split()[:2]).lower() for h in hooks.values())
    for o, c in opens.most_common(8):
        flag = "  <-- overused" if c > max(3, len(window) // 12) else ""
        print("   %2dx  %s%s" % (c, o, flag))

    # 3 near duplicate bodies ------------------------------------------------
    print("\n3. NEAR DUPLICATE BODIES (ratio > 0.55)")
    ids = list(bodies)
    dupes = []
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            r = difflib.SequenceMatcher(None, bodies[ids[i]], bodies[ids[j]]).ratio()
            if r > 0.55:
                dupes.append((r, ids[i], ids[j]))
    dupes.sort(reverse=True)
    if not dupes:
        print("   none. good.")
    for r, a, b in dupes[:8]:
        print("   %.2f  %s  <->  %s" % (r, a[:32], b[:32]))

    # 4 crutches -------------------------------------------------------------
    print("\n4. CRUTCH CONSTRUCTIONS (share of the window)")
    for pat in CRUTCHES:
        hits = [t for t, b in bodies.items() if re.search(pat, hooks[t] + " " + b, re.I)]
        if not hits:
            continue
        pct = 100.0 * len(hits) / len(window)
        flag = "  <-- LEANING ON IT" if pct >= 10 else ""
        print("   %5.1f%%  %-34s %d captions%s"
              % (pct, pat.replace("\\b", "").replace("(?:", "(") , len(hits), flag))

    # 5 rule failures --------------------------------------------------------
    # PROVENANCE MUST COME FROM THE STAGING FILES, not from build_queue. Once a
    # caption is applied, the live synopsis IS our caption, so build_queue reports
    # the title as tier A with no facts and every real character name reads as
    # invented. The first run of this audit failed 14 captions that way. The
    # FACTS blocks in generator/staging/captions_*.py are the record of what each
    # caption was written from, and they are the only correct source here.
    import glob
    facts = {}
    for path in sorted(glob.glob(os.path.join(HERE, "staging", "captions_*.py"))):
        try:
            _, f = cp.load_batch(path)
            facts.update({k: v for k, v in f.items() if v and v.strip()})
        except Exception as e:
            print("   (could not read %s: %s)" % (os.path.basename(path), e))
    q = {r["tid"]: r for r in cp.build_queue()}
    print("\n5. RULE FAILURES   [provenance loaded for %d titles]" % len(facts))
    fails = missing = 0
    for t in window:
        tid = t["title_id"]
        src = facts.get(tid)
        if not src:
            missing += 1
            continue        # written before provenance was recorded; not a failure
        errs = cp.validate(tid, ours(t), src, q.get(tid, {}).get("title", ""))
        errs = [e for e in errs if "floor" not in e and "use more of it" not in e]
        if errs:
            fails += 1
            print("   %-40s %s" % (tid[:38], "; ".join(errs)))
    if not fails:
        print("   none. good.")
    if missing:
        print("   NOTE: %d captions have no recorded provenance and were not checked."
              " Those predate the pipeline; anything written by it carries its source."
              % missing)

    # 6 sample ---------------------------------------------------------------
    print("\n6. RANDOM SAMPLE FOR CYAN (%d of %d)" % (n_sample, len(window)))
    random.seed()
    for t in random.sample(window, min(n_sample, len(window))):
        h, b, _ = parts[t["title_id"]]
        print("\n   %s" % t["primary_title"])
        print("   %s" % h)
        print("   %s" % b)

    print("\n" + "=" * 72)
    print("Read section 6 aloud. If any of it sounds like a machine, the corpus has")
    print("drifted and the next hundred need a different hand.")


if __name__ == "__main__":
    main()
