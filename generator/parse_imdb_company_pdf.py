"""Parse a saved IMDb COMPANY SEARCH pdf (imdb.com/search/title/?companies=coNNN)
into a clean list of SERIES, with the episode results removed.

WHY THIS EXISTS: THE POSTER LINK IS THE ONLY RELIABLE ID (Cyan spotted the cause,
13 Aug). An IMDb company search lists EPISODES as numbered results in their own
right, alongside the series. On the DramaBox page 196 of 614 results - 32% - were
episodes. Importing that list blind creates junk titles, because pdf text extraction
fuses the episode label onto the series name:

    Episode #1.1Forget Me Not: Omega's Return

THREE WAYS TO GET THIS WRONG, ALL TRIED FIRST:
  1. Take every /title/tt link annotation. Gives 616 ids for 614 results - it mixes
     in episode links nested under a series result.
  2. Take the text and match tt from it. extract_text() yields ZERO tt on this file;
     the ids live only in the link annotations.
  3. Treat a slot with more than one tt as contaminated. Flags 198 slots, but most
     are simply the poster and the title text both linking to the SAME series, so
     it discards good rows and still keeps bad ones.

WHAT ACTUALLY WORKS: every result carries a POSTER link whose ref_ is sr_i_<slot>,
exactly one per result, always pointing at that result's own tt. Pair it with the
printed "<slot>. <name>" line and drop any name matching ^Episode #\\d+\\.\\d+.
Verified on DramaBox: 614 slots -> 614 distinct poster ids, zero collisions, and
the 413-title staged parse from 9 Aug proved to be 413 of the 418 real series with
ZERO episodes wrongly kept.

DOES NOT GIVE WATCH LINKS. IMDb never names the app or the URL. This yields
title + tt + platform-from-filename only; direct_link comes from the platform.

Usage:
    py generator/parse_imdb_company_pdf.py "<file.pdf>" [--platform <id>] [--json out.json]
"""
import csv, json, os, re, sys

try:
    from pypdf import PdfReader
except ImportError:
    sys.exit("pypdf missing:  py -m pip install pypdf")

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.environ.get("DEA_DATA") or os.path.join(HERE, "..", "data")
EPISODE = re.compile(r"^Episode\s*#\d+\.\d+", re.I)


def parse(path):
    r = PdfReader(path)
    slot_tt = {}
    for p in r.pages:
        for a in (p.get("/Annots") or []):
            try:
                u = (a.get_object().get("/A") or {}).get("/URI") or ""
                m = re.search(r"/title/(tt\d+)", u)
                ref = re.search(r"ref_=sr_i_(\d+)", u)
                if m and ref:
                    slot_tt[int(ref.group(1))] = m.group(1)
            except Exception:
                pass

    text = "\n".join((p.extract_text() or "") for p in r.pages)
    slot_name = {}
    for line in text.splitlines():
        m = re.match(r"^\s*(\d+)\.\s*(.+)$", line)
        if m:
            slot_name.setdefault(int(m.group(1)), m.group(2).strip())

    header = re.search(r"1-(\d+)\s+of\s+([\d,]+)", text)
    series, episodes, unnamed = [], [], []
    for slot in sorted(slot_tt):
        tt, name = slot_tt[slot], slot_name.get(slot)
        if not name:
            unnamed.append({"slot": slot, "imdb_id": tt})
        elif EPISODE.match(name):
            episodes.append({"slot": slot, "imdb_id": tt, "name": name})
        else:
            series.append({"slot": slot, "imdb_id": tt, "title": name})
    return {"header": header.group(0) if header else None,
            "slots": len(slot_tt), "series": series,
            "episodes_dropped": episodes, "slots_without_a_name": unnamed}


def measure(series, platform):
    titles = list(csv.DictReader(open(os.path.join(DATA, "titles.csv"), newline="", encoding="utf-8")))
    av = list(csv.DictReader(open(os.path.join(DATA, "availability.csv"), newline="", encoding="utf-8")))
    by_tt = {t["imdb_id"].strip(): t for t in titles if t.get("imdb_id", "").strip()}
    on_plat = {r["title_id"] for r in av if r["platform_id"] == platform} if platform else set()
    has_av = {r["title_id"] for r in av}

    held, gain, noplat, absent = [], [], [], []
    for s in series:
        t = by_tt.get(s["imdb_id"])
        if not t:
            absent.append(s)
            continue
        held.append(t)
        if t["title_id"] not in on_plat:
            gain.append({"title_id": t["title_id"], "primary_title": t["primary_title"],
                         "imdb_id": s["imdb_id"]})
            if t["title_id"] not in has_av:
                noplat.append(t["title_id"])
    return held, gain, noplat, absent


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit(__doc__)
    path = args[0]
    platform = None
    if "--platform" in sys.argv:
        platform = sys.argv[sys.argv.index("--platform") + 1]

    out = parse(path)
    name = os.path.basename(path)
    print(f"\n=== {name} ===")
    print(f"  header on page      : {out['header']}")
    print(f"  numbered results    : {out['slots']}")
    print(f"  EPISODES dropped    : {len(out['episodes_dropped'])}"
          f"  ({100 * len(out['episodes_dropped']) // max(out['slots'], 1)}%)")
    print(f"  slots with no name  : {len(out['slots_without_a_name'])}")
    print(f"  CLEAN SERIES        : {len(out['series'])}")

    if platform:
        held, gain, noplat, absent = measure(out["series"], platform)
        print(f"  -- against our data (tt match, platform_id={platform}) --")
        print(f"  we hold             : {len(held)}")
        print(f"  would GAIN a row    : {len(gain)}")
        print(f"  ...no platform today: {len(noplat)}")
        print(f"  not held (import q) : {len(absent)}")
        out["would_gain_platform_row"] = gain
        out["not_held_import_queue"] = absent

    if "--json" in sys.argv:
        p = sys.argv[sys.argv.index("--json") + 1]
        json.dump(out, open(p, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        print(f"  wrote {p}")


if __name__ == "__main__":
    main()
