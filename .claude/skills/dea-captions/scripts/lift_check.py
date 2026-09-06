#!/usr/bin/env python3
"""Phrase-lift detector: the gap the copy-ratio misses.

    python3 .claude/skills/dea-captions/scripts/lift_check.py <batch.py> [--n 5]

The existing copy detector compares whole bodies with difflib and fails a
caption at 0.6. A caption can score 0.13 against its source and still contain
"three Masters beyond Sacred Rank" lifted word for word, because one borrowed
phrase barely moves a whole-body ratio. That is the exact failure Cyan caught
on 6 Sep 2026, and it is the failure that matters: a distinctive phrase taken
off the platform page is the thing Google reads as duplicated content, and the
thing she reads as "you just changed some words".

So this checks the other axis. It reports every run of N+ consecutive words
that appears in both the caption body and the source, ignoring case and
punctuation.

Not every hit is a fault. Names, genre terms and unavoidable plain phrasing
("she finds out he is her") will show up, and the house rules REQUIRE keeping
the audience's vocabulary. Judgement lives with the writer. What the report is
for is making the decision conscious: read each hit and keep it because it is a
name or a term the audience browses by, or rewrite it because it is the
platform's phrasing doing your work for you.
"""
import io, json, os, re, sys

STOPWORDS_ONLY = re.compile(r"^(?:the|a|an|and|or|but|of|to|in|is|it|he|she|"
                            r"they|her|his|him|for|with|on|at|as|that|this|"
                            r"was|were|be|been|by|from|not|no|so|then|when|"
                            r"who|what|all|one|out|up|into|about|over)$")


def words(s):
    return re.sub(r"[^a-z0-9 ]", " ", (s or "").lower()).split()


def runs(cap_words, src_words, n):
    src_grams = {}
    for i in range(len(src_words) - n + 1):
        src_grams.setdefault(tuple(src_words[i:i + n]), i)
    hits, i = [], 0
    while i <= len(cap_words) - n:
        g = tuple(cap_words[i:i + n])
        if g in src_grams:
            # Grow the match as far as it goes, so a long lift reports once.
            j, k = i + n, src_grams[g] + n
            while (j < len(cap_words) and k < len(src_words)
                   and cap_words[j] == src_words[k]):
                j += 1; k += 1
            hits.append(" ".join(cap_words[i:j]))
            i = j
        else:
            i += 1
    # A run of nothing but function words is grammar, not lifting.
    return [h for h in hits if not all(STOPWORDS_ONLY.match(w) for w in h.split())]


def load_facts(path):
    """FACTS comments in the batch file are the source of record."""
    src = io.open(path, encoding="utf-8").read()
    out = {}
    for block, key in re.findall(r"((?:\s*# FACTS: [^\n]*\n)+)\s*'([a-z0-9\-]+)':", src):
        out[key] = " ".join(re.sub(r"\s*# FACTS: ", " ", block).split())
    return out


def main(path, n):
    ns = {}
    exec(compile(io.open(path, encoding="utf-8").read(), path, "exec"), ns)
    caps = ns.get("CAPTIONS", {})
    facts = load_facts(path)
    flagged = 0
    for tid in sorted(caps):
        cap = caps[tid]
        if not cap.strip() or tid not in facts:
            continue
        body = cap.split("\n", 1)[1] if "\n" in cap else cap
        hits = runs(words(body), words(facts[tid]), n)
        if hits:
            flagged += 1
            print("  %s" % tid)
            for h in sorted(hits, key=lambda x: -len(x.split())):
                print("      %2d words  %s" % (len(h.split()), h))
    print("\n%d of %d captions carry a %d+ word run from their source."
          % (flagged, len(caps), n))
    print("Read each one. Keep names and genre terms; rewrite the rest.")
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(2)
    n = int(sys.argv[sys.argv.index("--n") + 1]) if "--n" in sys.argv else 5
    sys.exit(main(sys.argv[1], n))
