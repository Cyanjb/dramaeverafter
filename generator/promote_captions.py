#!/usr/bin/env python3
"""Move Cyan-approved captions out of a draft batch into the approved file.

Only captions_approved_*.py is ever applied to data/. Anything she has not ruled
on stays in the draft. This script does that promotion explicitly, naming which
ranks are held back and why, rather than promoting a whole batch on trust.

THE TRAP THIS SCRIPT CREATES, and it has already bitten once. Promotion rebuilds
the approved file FROM THE DRAFT. So an edit made ONLY in the approved file is
discarded the next time this runs. On 15 Aug Cyan changed "doesn't stay that
simple" to "doesn't stay that way" in the approved file; a later promotion put
the draft's older wording back, and the correction reached the live site only
after she noticed it missing. APPLY HER WORDING TO THE DRAFT AS WELL, always.

(This lived in a scratchpad until 16 Aug, when a session checking the handover
against disk found the file did not exist in the repo at all. It is here now so
the documented trap refers to something real.)

Usage:
    py generator/promote_captions.py <draft-file> <approved-file> [--hold 3,7,12]
"""
import io, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import caption_pipeline as cp  # noqa: E402


def wrap(text, indent="        ", width=64):
    esc = text.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
    chunks, line = [], ""
    for tok in esc.split(" "):
        if line and len(line) + len(tok) + 1 > width:
            chunks.append(line)
            line = tok
        else:
            line = (line + " " + tok).strip()
    if line:
        chunks.append(line)
    return ['%s"%s"%s' % (indent, c if k == len(chunks) - 1 else c + " ",
                          "," if k == len(chunks) - 1 else "")
            for k, c in enumerate(chunks)]


def main():
    draft, approved = sys.argv[1], sys.argv[2]
    hold = set()
    if "--hold" in sys.argv:
        hold = {int(x) for x in sys.argv[sys.argv.index("--hold") + 1].split(",") if x}

    caps, facts = cp.load_batch(draft)
    sources = cp.load_sources(draft)
    q = {r["tid"]: r for r in cp.build_queue()}
    order = sorted([t for t, c in caps.items() if c.strip()],
                   key=lambda t: -q.get(t, {}).get("reach", 0))

    take = [t for i, t in enumerate(order, 1) if i not in hold]
    held = [(i, t) for i, t in enumerate(order, 1) if i in hold]

    out = ['# -*- coding: utf-8 -*-',
           '"""APPROVED captions only. Cyan has signed off on every line in this file.',
           "",
           "Only this file is ever applied. The draft batch is a workspace.",
           "",
           "WARNING: this file is REGENERATED from the draft by promote_captions.py, so an",
           "edit made only here is lost on the next promotion. Edit the draft too.",
           '"""', "", "CAPTIONS = {"]
    for t in take:
        out.append("")
        out.append("    # %-8s %s" % (cp.views_label(q.get(t, {}).get("reach", 0)),
                                      q.get(t, {}).get("title", t)))
        out.append("    %r:" % t)
        out.extend(wrap(caps[t]))
    out += ["}", "", "SOURCES = {  # kind -> caption_pipeline.SOURCE_KINDS"]
    for t in take:
        if t in sources:
            out.append("    %r: %r," % (t, sources[t]))
    out += ["}", "", "FACTS = {  # the published synopsis each caption was written from"]
    for t in take:
        f = facts.get(t) or q.get(t, {}).get("facts", "")
        if f and f.strip():
            out.append("    %r:" % t)
            out.extend(wrap(f.replace("\n", " ")))
    out.append("}")
    io.open(approved, "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")

    print("promoted %d captions -> %s" % (len(take), os.path.basename(approved)))
    missing = [t for t in take if t not in sources]
    if missing:
        print("WARNING: %d promoted captions have NO source kind recorded" % len(missing))
    for i, t in held:
        print("   held back: %2d  %s" % (i, q.get(t, {}).get("title", t)))


if __name__ == "__main__":
    main()
