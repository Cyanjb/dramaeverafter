#!/usr/bin/env python3
"""Print every caption beside the source it was written from, for a final check.

Cyan, 16 Aug 2026: "The last thing you do before you move on from a caption is to
read your result then read its caption source of the title to make sure the
information is accurate. You need to be clear on what the original source is as
well, whether it's from a 3rd party website or the PDFs I gave you."

This is the LAST STEP of writing a batch, after check passes and before apply.
The automated guard only compares proper nouns; it cannot tell whether a claim is
true. Only reading the two side by side does that, so this puts them side by side
and names the source kind on every one.

Usage:
    py generator/readback.py generator/staging/captions_<batch>.py
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import caption_pipeline as cp  # noqa: E402


def main():
    path = sys.argv[1]
    caps, facts = cp.load_batch(path)
    sources = cp.load_sources(path)
    q = {r["tid"]: r for r in cp.build_queue()}
    filled = [(t, c) for t, c in caps.items() if c.strip()]
    filled.sort(key=lambda x: -q.get(x[0], {}).get("reach", 0))

    print("READ BACK  |  %s  |  %d captions" % (os.path.basename(path), len(filled)))
    print("Read the caption, then read the source. Every claim in the caption must")
    print("be traceable to the source or to the title itself.\n")

    for i, (tid, cap) in enumerate(filled, 1):
        hook, body, aside = cp.parts(cap)
        kind, where = sources.get(tid, ("UNRECORDED", "?"))
        src = facts.get(tid) or q.get(tid, {}).get("facts", "") or "(none on file)"
        warn = ""
        if kind == "fansite":
            warn = "   <<< FAN SITE, not authoritative"
        elif kind == "UNRECORDED":
            warn = "   <<< SOURCE KIND NOT RECORDED"
        print("=" * 74)
        print("%2d. %s" % (i, q.get(tid, {}).get("title", tid)))
        print("    SOURCE KIND : %s (%s)%s" % (kind, where, warn))
        print("\n    CAPTION")
        print("      %s" % hook)
        print("      %s" % body)
        if aside:
            print("      %s" % aside)
        print("\n    SOURCE")
        for k in range(0, len(src), 88):
            print("      %s" % src[k:k + 88])
        print()


if __name__ == "__main__":
    main()
