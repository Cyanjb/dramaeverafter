#!/usr/bin/env python3
"""Repair people whose name was stored through a broken encoding, and the slug
that was derived from the broken name.

Slugs are permanent by standing rule, because changing one breaks every link and
every indexed URL. That rule assumes the slug is CORRECT. A slug derived from
mojibake is not a URL worth keeping: 'hristine-oswald' has lost the C from
Christine. Cyan ruled on 8 Aug 2026 that a misspelled URL is worse than a changed
one, so these are corrected and the old paths are 301'd in _redirects. The rule
still holds for every slug that was right in the first place.

Only rows whose corruption round-trips cleanly are touched:

    name.encode('latin-1').decode('utf-8')

That is the exact inverse of the fault (utf-8 bytes read as latin-1), so a clean
result is proof of what the original was rather than a guess about it. Anything
that fails to round-trip is REPORTED, never repaired, because the alternative is
inventing a real person's name -- which the standing rule forbids for the same
reason a wrong AI tag is forbidden.

A rename that collides with an existing person is also refused. That is a MERGE,
and merges need a human ruling; renaming into an occupied id would silently fuse
two people's filmographies.

Usage:
    python3 fix_mojibake_slugs.py [--apply]
"""
import csv, io, os, re, sys, argparse

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


# Cyrillic letters that are visually identical to Latin ones. A name that is
# otherwise plain Latin but carries one of these is a homoglyph typo, not a
# foreign spelling: 'сHristine' is Christine with a Cyrillic es standing in for
# the C, which is why it slugged to 'hristine-oswald' with the C simply gone.
# Only substituted when the REST of the name is ASCII, so a genuinely Cyrillic
# or Ukrainian name is never quietly Latinised.
HOMOGLYPH = {"а": "a", "е": "e", "о": "o", "р": "p",
             "с": "c", "у": "y", "х": "x", "А": "A",
             "Е": "E", "О": "O", "Р": "P", "С": "C",
             "У": "Y", "Х": "X", "І": "I", "і": "i"}


def corrupted(s):
    return (any(0x80 <= ord(c) <= 0x9F for c in s) or "Å" in s or "Ã" in s
            or any(c in HOMOGLYPH for c in s))


def dehomoglyph(s):
    """Latin-ise look-alike Cyrillic ONLY when every other letter is ASCII."""
    if not any(c in HOMOGLYPH for c in s):
        return s
    rest = [c for c in s if c not in HOMOGLYPH]
    if any(ord(c) > 0x7F for c in rest):
        return s          # genuinely non-Latin name, leave it alone
    return "".join(HOMOGLYPH.get(c, c) for c in s)


def repair(s):
    """Return the true string, or None when the corruption does not round-trip."""
    fixed = s
    if any(0x80 <= ord(c) <= 0x9F for c in s) or "Å" in s or "Ã" in s:
        try:
            fixed = s.encode("latin-1").decode("utf-8")
        except (UnicodeEncodeError, UnicodeDecodeError):
            return None
    fixed = dehomoglyph(fixed)
    if corrupted(fixed):
        return None
    # 'cHristine' -> 'Christine'. Only when the mis-cased pair sits at a word start,
    # which is the signature of a homoglyph swallowing the real capital.
    fixed = re.sub(r"\b([a-z])([A-Z])", lambda m: m.group(1).upper() + m.group(2).lower(), fixed)
    return fixed


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    people, credits = load("people.csv"), load("credits.csv")
    ids = {p["person_id"] for p in people}

    renames, refused = [], []
    for p in people:
        if not corrupted(p["name"]):
            continue
        fixed = repair(p["name"])
        if fixed is None:
            refused.append((p["person_id"], p["name"], "does not round-trip - cannot know the real name"))
            continue
        new_id = slugify(fixed)
        if new_id == p["person_id"]:
            renames.append((p["person_id"], p["person_id"], p["name"], fixed))
            continue
        if new_id in ids:
            refused.append((p["person_id"], p["name"],
                            f"'{new_id}' already exists - this is a MERGE, needs a ruling"))
            continue
        renames.append((p["person_id"], new_id, p["name"], fixed))

    print(f"repairable: {len(renames)}")
    for old, new, was, now in renames:
        print(f"    {old:<24} -> {new:<24} {was!r} -> {now!r}")
    print(f"refused:    {len(refused)}")
    for pid, nm, why in refused:
        print(f"    {pid:<24} {nm!r}\n        {why}")

    if not args.apply:
        print("\n[dry run] nothing written. Re-run with --apply")
        return
    if not renames:
        print("\nnothing to apply")
        return

    remap = {old: new for old, new, _, _ in renames}
    fix_name = {old: now for old, _, _, now in renames}
    for p in people:
        if p["person_id"] in remap:
            p["name"] = fix_name[p["person_id"]]
            p["slug"] = remap[p["person_id"]]
            p["person_id"] = remap[p["person_id"]]
    moved = 0
    for c in credits:
        if c["person_id"] in remap:
            c["person_id"] = remap[c["person_id"]]
            moved += 1
    save("people.csv", people)
    save("credits.csv", credits)

    # The old URL is already published and may be indexed, so it must not 404.
    lines = []
    path = os.path.join(REPO, "_redirects")
    if os.path.exists(path):
        lines = [l.rstrip("\n") for l in open(path, encoding="utf-8")]
    # ONLY when the slug actually moved. Fixing a NAME usually leaves the slug
    # alone, because slugify() strips non-ASCII anyway -- 'Oliwia Drozdzyk' and
    # 'Oliwia Drożdżyk' both slug to oliwia-dro-d-yk. Writing a rule regardless
    # emitted "/actors/x.html -> /actors/x.html 301", which is a redirect loop
    # that would take the page down rather than move it.
    changed = [(o, n) for o, n, _, _ in renames if o != n]
    for old, new in changed:
        rule = f"/actors/{old}.html  /actors/{new}.html  301"
        if rule not in lines:
            lines.append(rule)
    if lines:
        open(path, "w", encoding="utf-8").write("\n".join(lines).rstrip() + "\n")

    for old, new in changed:
        stale = os.path.join(REPO, "actors", f"{old}.html")
        if os.path.exists(stale):
            os.remove(stale)

    print(f"\nfixed {len(renames)} names, moved {moved} credits, "
          f"{len(changed)} slugs actually moved (and were redirected)")


if __name__ == "__main__":
    main()
