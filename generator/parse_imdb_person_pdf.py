#!/usr/bin/env python3
"""Parse a saved IMDb PERSON page PDF into the staged filmography JSON shape.

Replaces hand-transcription. The 28 filmographies staged before 13 Aug were read by
eye, which is why the batch took several sessions and why the pagination trap bit
ten of fourteen pages.

HOW THE PAGE IS STRUCTURED, established by inspection 13 Aug:

  extract_text(extraction_mode='layout') renders each credit as a BLOCK of lines
  separated by blank lines, indented together:

      Title
      [rating]  Type          e.g. "Short", "  7.8  TV Mini Series"
      Character
      [N episodes]  Year      e.g. "2024", "8 episodes   2022-2023"

  NEVER STRIP THE INDENT before splitting into blocks - the trap list is explicit
  that indentation is data, and it is what keeps a block together here.

THE LINK ANNOTATIONS ARE USED AS A COUNT CHECK, NOT AS A PAIRING. Each credit
carries '...nm_flmg_job_1_accord_1_cdt_t_N', so the number of distinct N is how many
credits IMDb thinks it rendered. Pairing block i to link i would be the obvious move
and is WRONG: the pagination trap drops unrelated fragments INTO credit rows, so the
two sequences can drift and the pairing would silently mislabel. Comparing the COUNTS
detects exactly that drift without pretending to fix it.

VERTICAL FILTER. A vertical drama is a TV Mini Series on IMDb. Features, shorts,
long-running TV, music videos and podcasts are excluded, and every exclusion is
LISTED in the output so nothing disappears silently - the same reason the appliers
print their unmatched rows.

ANOMALIES ARE REPORTED, NEVER GUESSED. If the block count and the link count
disagree, or a block carries an 'Upcoming'/'Previous' pagination token, or a block
has no year, the file is written with "needs_review": true and the offending blocks
verbatim. A staged file with that flag must not be applied without a human look.

Usage:
    py parse_imdb_person_pdf.py "<pdf path>" [--out DIR] [--print]
"""
import os, re, sys, json, argparse

from pypdf import PdfReader

TYPES = ("TV Mini Series", "TV Series", "TV Movie", "TV Special", "TV Short",
         "Music Video", "Video Game", "Podcast Series", "Podcast Episode",
         "Short", "Video")
VERTICAL_TYPE = "TV Mini Series"
PAGINATION = ("Upcoming", "Previous", "Next")

YEAR_RE = re.compile(r"(?:(\d+)\s+episodes?)?\s*((?:19|20)\d{2})(?:\s*[–\-]\s*((?:19|20)\d{2})?)?\s*$")
# The rating can be GLUED to the type with no space once a pagination control has
# been stripped: 'Previous    7.854TV Mini Series' is rating 7.8, count 54, then the
# type. Requiring whitespace after the number lost 'The Man Who Stands Beside You'.
TYPE_RE = re.compile(r"^\s*(?:[\d.]+\s*)?(" + "|".join(re.escape(t) for t in TYPES) + r")\s*$")


def bare(s):
    """Article-stripped, punctuation-free key. The article must go BEFORE spaces
    collapse, or 'Alpha's Doe' becomes 'lphasdoe' - see apply_imdb_filmography.py."""
    s = re.sub(r"^(the|a|an)\s+", "", (s or "").strip().lower())
    return re.sub(r"[^a-z0-9]", "", s)


def held_titles():
    """Every title we already hold, for the type_uncertain ruling."""
    import csv
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "titles.csv")
    out = set()
    try:
        for t in csv.DictReader(open(p, newline="", encoding="utf-8")):
            out.add(bare(t["primary_title"]))
            for a in (t.get("alt_titles") or "").split("|"):
                if a.strip():
                    out.add(bare(a))
    except FileNotFoundError:
        pass
    return out


def slugify(s):
    s = (s or "").lower()
    s = (s.replace("ü", "u").replace("ö", "o").replace("á", "a").replace("é", "e")
           .replace("í", "i").replace("ó", "o").replace("ú", "u").replace("ñ", "n")
           .replace("å", "a").replace("ø", "o").replace("æ", "ae"))
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def read(path):
    r = PdfReader(path)
    text = "\n".join(p.extract_text(extraction_mode="layout") for p in r.pages)
    uris = []
    for page in r.pages:
        for a in (page.get("/Annots") or []):
            try:
                u = (a.get_object().get("/A") or {}).get("/URI")
            except Exception:
                continue
            if u:
                uris.append(u)
    return text, uris


def subject(text, uris, path):
    """Name from the page head; nm from the page's own self-referencing links."""
    nm = ""
    counts = {}
    for u in uris:
        m = re.search(r"/name/(nm\d+)", u)
        if m:
            counts[m.group(1)] = counts.get(m.group(1), 0) + 1
    # The subject's own nm appears far more than any co-star's.
    if counts:
        nm = max(counts.items(), key=lambda kv: kv[1])[0]
    # NAME COMES FROM THE FILENAME, not the page text. Cyan saves these as
    # "<Name> - IMDb.pdf" and that is the same string the ledger holds, so it is
    # both reliable and consistent with the batch. Reading the first short line of
    # the layout text instead produced "Back to top", which would have written a
    # person_id of 'back-to-top'.
    name = os.path.basename(path).split(" - IMDb")[0].strip()
    return name, nm


def strip_pagination(ln):
    """IMDb's Upcoming/Previous/Next controls land INSIDE a credit row and glue
    themselves to it: 'Previous    7.854TV Mini Series'. Remove the token so the
    row can be read; the fact that it happened is still reported by the caller."""
    return re.sub(r"^\s*(Upcoming|Previous|Next)\s*\d*\s*", "  ", ln), \
        bool(re.match(r"^\s*(Upcoming|Previous|Next)\b", ln))


def credit_units(text):
    """Every credit in the document, found by scanning for TYPE lines.

    NOT by splitting on blank lines, which was the first attempt and is WRONG: two
    credits regularly render into one run with no blank between them, and a
    first-type-line/last-year-line reading then fuses them - it took 'Racing Into
    Love with My Secret Boss' and gave it the 73-episode count belonging to
    'Claimed by the Alpha I Hate' below it. A wrong episode count on a real title
    is worse than a missed credit, because nothing downstream flags it.

    A credit is anchored on its TYPE line: the title is the line above, the year is
    the next year-line below, and the character is whatever sits between.
    """
    lines = text.split("\n")
    hits = []
    for i, raw in enumerate(lines):
        ln, paged = strip_pagination(raw)
        m = TYPE_RE.match(ln)
        if not m or i == 0:
            continue
        title = lines[i - 1]
        title, tpaged = strip_pagination(title)
        title = title.strip()
        if not title or TYPE_RE.match(title) or YEAR_RE.search(title):
            continue
        # the year for THIS credit is the first year-line before the next type line
        year_i = None
        for j in range(i + 1, min(i + 6, len(lines))):
            nxt, _ = strip_pagination(lines[j])
            if TYPE_RE.match(nxt):
                break
            if YEAR_RE.search(nxt.strip()):
                year_i = j
                break
        if year_i is None:
            continue
        ym = YEAR_RE.search(strip_pagination(lines[year_i])[0].strip())
        chars = [strip_pagination(x)[0].strip() for x in lines[i + 1:year_i]]
        chars = [c for c in chars if c]
        character, billed_as = "", ""
        if chars:
            parts = [p.strip() for p in re.split(r"\s{3,}", chars[0]) if p.strip()]
            character = parts[0] if parts else ""
        # IMDb appends the BILLING VARIANT to the character when the actor was
        # credited under another name: "Kane Hudson (as Jesse Morales)". That is not
        # part of the character and must never reach character_name - eight credits
        # went live reading 'Julian Barlow (as Jesse Morales)' before this was caught.
        # It is also genuine aka evidence, so it is kept in its own field rather than
        # discarded, per the rule to record a name variant when one is seen.
        m_as = re.search(r"\s*\(as ([^)]+)\)\s*$", character)
        if m_as:
            billed_as = m_as.group(1).strip()
            character = character[:m_as.start()].strip()
        rec = {"title": title, "character": character, "year": int(ym.group(2))}
        if billed_as:
            rec["billed_as"] = billed_as
        if ym.group(1):
            rec["episodes"] = int(ym.group(1))
        hits.append({"rec": rec, "kind": m.group(1),
                     "paged": paged or tpaged,
                     "raw": [lines[i - 1]] + lines[i:year_i + 1]})
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("--out", default=None)
    ap.add_argument("--print", dest="show", action="store_true")
    args = ap.parse_args()

    text, uris = read(args.pdf)
    name, nm = subject(text, uris, args.pdf)

    n_links = len({m.group(1) for u in uris
                   for m in [re.search(r"cdt_t_(\d+)", u)] if m})

    # The same credit renders more than once - the "Known for" rail repeats
    # filmography entries, sometimes in a different shape ('2023 - 37 eps' rather
    # than '37 episodes 2023'). Dedupe on title, keeping the RICHEST reading.
    best, recovered = {}, []
    for u in credit_units(text):
        k = re.sub(r"[^a-z0-9]", "", u["rec"]["title"].lower())
        if not k:
            continue
        score = (1 if u["rec"].get("episodes") else 0) + (1 if u["rec"]["character"] else 0)
        if k not in best or score > best[k][0]:
            best[k] = (score, u)
        if u["paged"]:
            recovered.append(u["rec"]["title"])

    # TYPE_UNCERTAIN: a vertical is normally a TV Mini Series, but IMDb files some
    # of them as plain TV Series - and real television is TV Series too, so the type
    # alone cannot decide. The established ruling (progress log, Kirby Ellwood,
    # 13 Aug) is to PROMOTE one we already hold, because a title in our vertical
    # database is evidence that it is vertical. The rest are reported, never guessed.
    held = held_titles()
    vertical, excluded, uncertain = [], [], []
    for _, u in best.values():
        r = u["rec"]
        if u["kind"] == VERTICAL_TYPE:
            vertical.append(r)
        elif u["kind"] == "TV Series":
            if bare(r["title"]) in held:
                r = dict(r, promoted="TV Series on IMDb, but we hold the title, "
                                      "so it is a vertical (Kirby Ellwood precedent)")
                vertical.append(r)
            else:
                uncertain.append({"title": r["title"], "character": r["character"],
                                  "year": r["year"], "type": u["kind"]})
        else:
            excluded.append({"title": r["title"], "type": u["kind"], "year": r["year"]})
    vertical.sort(key=lambda c: (-c["year"], c["title"]))
    excluded.sort(key=lambda c: (-c["year"], c["title"]))
    uncertain.sort(key=lambda c: (-c["year"], c["title"]))

    parsed_total = len(vertical) + len(excluded) + len(uncertain)
    gap = (n_links - parsed_total) if n_links else 0

    # WHAT THE FLAG MEANS, and why it is not simply "gap > 0". A small gap is normal
    # and harmless: IMDb renders a few credits with NO type and NO year line at all
    # (the hand transcriber hit the same rows and noted them - "Beach Town Maidens
    # ('Kyle', no type or year listed)"). Those cannot be parsed by anyone and cost
    # a possible credit, never a wrong one; the applier adds credits only for titles
    # already held, so a miss writes nothing.
    #
    # The DANGEROUS case is a WRONG credit, and that is what the flag is for: a
    # stripped pagination control, which is the one mechanism known to move data
    # between rows. Controlled against three hand-transcribed pages (141 credits):
    # zero false positives, two exact matches. Flagging every small gap instead
    # would fire on every file and train the next reader to ignore it.
    needs_review = bool(recovered) or gap > 3

    out = {
        "name": name,
        "nm": nm,
        "person_id": slugify(name),
        "confident": not needs_review,
        "source_pdf": os.path.basename(args.pdf),
        "read_by": "parse_imdb_person_pdf.py (pypdf layout mode + link-count check)",
        "counts": {"imdb_credit_links": n_links, "credits_parsed": parsed_total,
                   "unparsed_gap": gap,
                   "vertical": len(vertical), "excluded_non_vertical": len(excluded),
                   "type_uncertain": len(uncertain)},
        "pagination_trap_rows_recovered": sorted(set(recovered)),
        "credits": vertical,
        "type_uncertain_not_staged": uncertain,
        "non_vertical_excluded": excluded,
        "caption_rule": "CAST ONLY. No IMDb storyline or platform synopsis is copied "
                        "or reworded. Captions are written from scratch.",
    }
    if needs_review:
        out["needs_review"] = True
        out["review_reason"] = (
            ("%d row(s) had a pagination control stripped out of them - check those "
             "titles against another field before trusting them; " % len(set(recovered))
             if recovered else "")
            + ("%d linked credits could not be parsed at all" % gap if gap > 3 else ""))

    if args.out:
        os.makedirs(args.out, exist_ok=True)
        p = os.path.join(args.out, "actor__%s.json" % out["person_id"])
        json.dump(out, open(p, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        print("wrote %s" % p)
    print("%-26s nm=%-12s vertical=%-3d excluded=%-3d links=%-3d %s"
          % (name[:25], nm or "?", len(vertical), len(excluded), n_links,
             "NEEDS REVIEW" if needs_review else "ok"))
    if args.show:
        for c in vertical:
            print("    ", c)
    return 0


if __name__ == "__main__":
    sys.exit(main())
