#!/usr/bin/env python3
"""Parse a saved IMDb TITLE page PDF into the staged cast JSON shape.

A title page is HARDER than a person page and the traps list says so: a person page
gives one row per credit, a title page is a GRID and the pairing has to be
reconstructed. The reconstruction here is the one established on 13 Aug.

THE GRID. extract_text(extraction_mode='layout') renders the cast as a two-column
table, one row at a time:

    Kirby Ellwood                                    David Edwin Williams
       Erin White                                        Dr. Victor K. Lore
       1 ep - 2026                                            1 ep - 2026

THE INDENT IS THE DATA. Which character belongs to which actor is carried ONLY by
horizontal position, so this pairs by COLUMN OFFSET - the start column of each
segment - and never by order-within-line. Stripping whitespace first took one title
from 18 pairs down to 3, which is why the traps list shouts about it.

THE nm IDS COME FROM THE LINK ANNOTATIONS, not the text. Each cast link carries
'?ref_=tt_cst_t_N' where N is the billing slot, so the ids and their ORDER are exact
even where the text pairing is uncertain. They are used to (a) know how many cast
IMDb rendered and (b) attach an id to each name positionally, which is safe because
both sequences are billing order.

THE PLATFORM IS IN THE PRODUCTION-COMPANY FIELD, which is the whole reason a title
page is worth reading: IMDb never says which app a title streams on anywhere else,
and platform is the one attribute that cannot be inferred. sec 23.

Usage:
    py parse_imdb_title_pdf.py "<pdf path>" [--out DIR]
"""
import os, re, sys, json, argparse
from pypdf import PdfReader

# Known platform names as they appear in IMDb's production-company field.
PLATFORMS = {
    "reelshort": "reelshort", "dramabox": "dramabox", "drama box": "dramabox",
    "goodshort": "goodshort", "my drama": "my-drama", "mydrama": "my-drama",
    "candyjar": "candyjar", "candy jar": "candyjar", "shortmax": "shortmax",
    "short max": "shortmax", "dramapops": "dramapops", "drama pops": "dramapops",
    "dramawave": "dramawave", "drama wave": "dramawave", "netshort": "netshort",
    "vigloo": "vigloo", "shortical": "shortical", "playlet": "playlet",
    "kalostv": "kalostv", "kalos tv": "kalostv", "dreameshort": "dreameshort",
    "dreame short": "dreameshort", "pinedrama": "pinedrama", "shorts": "shorts",
}
NOISE_RE = re.compile(r"^(1 ep|\d+ eps?|\d+ episodes?)\b|^[\d\s•\-–]+$", re.I)

# Section headings and type strings that sit in the same column as a cast name.
NOT_A_NAME = {
    "tv mini series", "tv series", "tv movie", "short", "video", "cast", "top cast",
    "series cast", "storyline", "episodes", "photos", "videos", "more like this",
    "user reviews", "details", "trailer", "official trailer", "watchlist",
    "add to watchlist", "see all", "edit", "back to top", "director", "writers",
    "writer", "stars", "star", "all cast crew", "production box office",
    "technical specs", "did you know", "contribute to this page", "more to explore",
}


def looks_like_person(s):
    """A cast cell is a personal name. This has to be STRICT: anything else accepted
    here does not merely add junk, it SHIFTS every nm id after it, because ids are
    attached by position. Letting the title and the storyline through moved Kirby
    Ellwood from billing slot 1 to slot 3 and silently gave him another actor's id."""
    if not s or len(s) > 34 or s.lower() in NOT_A_NAME:
        return False
    if re.search(r"\d", s) or NOISE_RE.match(s):
        return False
    words = s.split()
    if not (1 < len(words) <= 5):
        return False
    for w in words:
        if w.lower() in ("de", "van", "von", "der", "da", "di", "del", "la", "jr.", "jr",
                         "ii", "iii"):
            continue
        if not re.match(r"^[A-ZÀ-Ý][\w'\-\.]*$", w):
            return False
    return True


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


def billing(uris):
    """[(slot, nm)] in billing order, from ?ref_=tt_cst_t_N."""
    seen = {}
    for u in uris:
        m = re.search(r"/name/(nm\d+)/\?ref_=tt_cst_[a-z]+_(\d+)", u)
        if m:
            seen.setdefault(int(m.group(2)), m.group(1))
    return [(k, seen[k]) for k in sorted(seen)]


def segments(line):
    """[(start_col, text)] for a padded layout line. Split on 3+ spaces, keep the
    column so the character below can be matched to the actor above."""
    out = []
    for m in re.finditer(r"\S(?:.*?\S)?(?=\s{3,}|\s*$)", line):
        s = m.group(0).strip()
        if s:
            out.append((m.start(), s))
    return out


def platform_of(text):
    m = re.search(r"Production compan(?:y|ies)(.{0,220})", text, re.S)
    if not m:
        return None, ""
    blob = m.group(1)
    names = [s for _, s in segments(blob.split("\n")[0])] or []
    for extra in blob.split("\n")[1:3]:
        names += [s for _, s in segments(extra)]
    for n in names:
        k = n.strip().lower()
        if k in PLATFORMS:
            return PLATFORMS[k], ", ".join(names[:4])
    return None, ", ".join(names[:4])


def parse_cast(text, n_expected):
    """Pair actor -> character by COLUMN, walking the grid row by row."""
    lines = text.split("\n")
    i = next((k for k, l in enumerate(lines) if re.match(r"\s*Cast\s+\d+\s*$", l)), None)
    if i is None:
        i = next((k for k, l in enumerate(lines) if "Top cast" in l), 0)
    pairs, k, seen = [], i, set()
    # STOP at n_expected. IMDb tells us exactly how many cast it rendered via the
    # link annotations, so collecting more than that is proof of contamination
    # rather than a bonus.
    while k < len(lines) - 1 and len(pairs) < n_expected:
        segs = [(c, s) for c, s in segments(lines[k]) if looks_like_person(s)]
        if segs and len(segs) <= 2:
            nxt = segments(lines[k + 1]) if k + 1 < len(lines) else []
            # The CHARACTER cell must not be a type or heading either. The title's
            # own header row ("Fever Cage" over "TV Mini Series") passes the name
            # test on the actor side and would otherwise be accepted as cast -
            # one junk row is enough to shift every nm id by a slot.
            nxt = [(c, s) for c, s in nxt
                   if not NOISE_RE.match(s) and len(s) <= 44
                   and s.lower() not in NOT_A_NAME]
            if nxt:
                for col, actor in segs:
                    if actor in seen:
                        continue
                    seen.add(actor)
                    best, bd = "", 10 ** 9
                    for c2, ch in nxt:
                        d = abs(c2 - col)
                        if d < bd:
                            bd, best = d, ch
                    # A character in the OTHER column is far away; 24 cols is about
                    # half the gutter and comfortably separates the two columns.
                    # Key is "name", not "actor": _to_cast_batch.py reads c["name"]
                    # and "order" is the billing slot the existing staged files use.
                    pairs.append({"order": len(pairs) + 1, "name": actor,
                                  "character": best if bd <= 24 else ""})
                k += 2
                continue
        k += 1
    return pairs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    text, uris = read(args.pdf)
    bill = billing(uris)
    base = os.path.basename(args.pdf)
    title = re.split(r"\s*\((TV|Video|\d{4})", base)[0].strip()
    plat, companies = platform_of(text)

    cast = parse_cast(text, len(bill))
    # Attach nm ids positionally: both sequences are billing order.
    for i, c in enumerate(cast):
        if i < len(bill):
            c["nm"] = bill[i][1]

    out = {
        "title": title,
        "platform": plat,
        "platform_source": "IMDb production-company field: %s" % companies,
        "production_companies": companies,
        "source_pdf": base,
        "read_by": "parse_imdb_title_pdf.py (pypdf layout mode, column pairing)",
        "counts": {"imdb_cast_links": len(bill), "pairs_parsed": len(cast),
                   "with_character": sum(1 for c in cast if c["character"])},
        "cast": cast,
        "caption_rule": "CAST ONLY. No IMDb storyline is copied or reworded.",
    }
    if not plat:
        out["needs_review"] = True
        out["review_reason"] = ("no known platform in the production-company field (%s)"
                                % companies)
    if args.out:
        os.makedirs(args.out, exist_ok=True)
        slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
        p = os.path.join(args.out, "title__%s.json" % slug)
        json.dump(out, open(p, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        print("wrote", p)
    print("%-42s platform=%-11s cast_links=%-3d paired=%-3d with_char=%d"
          % (title[:41], plat or "?", len(bill), len(cast),
             out["counts"]["with_character"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
