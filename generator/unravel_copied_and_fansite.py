"""Unravel two problems that are legal/positioning issues, not data-quality niceties.

PROBLEM 1 - COPIED SYNOPSES. 2,053 of 3,145 synopses are EXACTLY 300 characters or
300 bytes: the documented scraper-truncation shape. They are the platform's own
marketing prose, cut mid-sentence, published on our pages. That breaks the standing
caption rule on both grounds Cyan gave - copyright, and duplicate content against the
very platforms we are trying to outrank. completeness.py already refuses to count
them, so the metric does not change; only the exposure does.

    --quarantine   moves every copied synopsis OUT of titles.csv into a local,
                   GITIGNORED file. Nothing is lost: the file is the fact source for
                   rewriting later. Facts are not copyrightable; the PROSE is what
                   must never be reused, so a rewrite reads the premise and then
                   writes fresh, in DramaEverAfter's own fellow-fan voice.

PROBLEM 2 - WE LINK TO A FAN/AFFILIATE SITE, NOT A PLATFORM. pinedrama.com is not a
streaming service. Its own page payload carries "supplier":"reelshort", its watch
buttons are affiliate redirects (short.inbeidou.ai/link/reelshort/...), its page slugs
end "-reelshort", and its footer describes it as a guide with "links to official
platforms". It is the same category as shortdramadb and verticaldrama.tv, both of
which this project already refuses. We hold 137 rows calling it a platform, and on
133 titles it is the ONLY watch option we offer.

    --relink-twins  for the 73 duplicate '<slug>-pinedrama' titles, the non-suffixed
                    twin already carries an OFFICIAL link. Copy the twin's platform
                    and link onto the duplicate's row so it stops pointing at the fan
                    site. Deduplicating the two title rows is a SEPARATE, one-way
                    decision and is NOT done here.

The remaining 64 pinedrama rows sit on titles with no twin, so their official
platform has to be found per title; they are reported, never guessed.

Usage:
    py generator/unravel_copied_and_fansite.py [--quarantine] [--relink-twins] [--dry-run]
"""
import csv, io, json, os, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.environ.get("DEA_DATA") or os.path.join(HERE, "..", "data")
QUAR = os.path.join(HERE, "staging", "_quarantined_synopses.json")   # gitignored
REPORT = os.path.join(HERE, "staging", "pinedrama_unresolved_" + time.strftime("%Y-%m-%d") + ".json")
DRY = "--dry-run" in sys.argv


def term_of(p):
    raw = open(p, "rb").read()
    crlf = raw.count(b"\r\n")
    return "\r\n" if crlf > raw.count(b"\n") - crlf else "\n"


def load(n):
    p = os.path.join(DATA, n)
    return list(csv.DictReader(open(p, newline="", encoding="utf-8-sig"))), term_of(p)


def save(n, rows, term):
    p = os.path.join(DATA, n)
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=list(rows[0].keys()), lineterminator=term)
    w.writeheader()
    w.writerows(rows)
    open(p, "w", encoding="utf-8", newline="").write(buf.getvalue())


import re


def is_copied(s, source=""):
    """What can be PROVEN or KNOWN to be platform prose, not merely suspected.

    Cyan, 14 Aug: 'surely it doesn't have to be exactly 300' - correct. The 300
    shapes are the floor. Added here:
      - a synopsis with no terminal punctuation is a truncation whatever its length;
      - every mydrama_2026-07-17 synopsis is a KNOWN verbatim ld+json copy (the 9 Aug
        refill wrote the platform's own description field, byte-identical);
      - every pinedrama_2026-07-20 synopsis is the fan site's marketing copy.
    What this still cannot catch: an untruncated verbatim copy from other scrapes.
    Those are all source=<scrape> and data_confidence=needs_check, so they are
    REPORTED as suspect for the rewrite queue rather than silently trusted.
    """
    if not s:
        return False
    if len(s) == 300 or len(s.encode("utf-8")) == 300:
        return True
    if not re.search(r"[.!?…\"'”’)\]]\s*$", s.strip()):
        return True     # cut mid-sentence
    if source.startswith(("mydrama_", "pinedrama_")):
        return True     # known-verbatim sources
    return False


def main():
    titles, t_term = load("titles.csv")
    av, a_term = load("availability.csv")
    by_id = {t["title_id"]: t for t in titles}

    # ---------- problem 1 ----------
    quarantined = 0
    if "--quarantine" in sys.argv:
        store = json.load(open(QUAR, encoding="utf-8")) if os.path.exists(QUAR) else {}
        suspect = 0
        for t in titles:
            s = t["synopsis_short"] or ""
            if not s.strip():
                continue
            if is_copied(s, t.get("source", "")):
                store[t["title_id"]] = {"primary_title": t["primary_title"],
                                        "copied_text": s,
                                        "note": "PLATFORM PROSE. Fact source only - never reuse the wording."}
                t["synopsis_short"] = ""
                quarantined += 1
            elif t.get("data_confidence") != "verified":
                suspect += 1
        print(f"left in place but scrape-sourced (rewrite queue): {suspect}")
        if not DRY:
            os.makedirs(os.path.dirname(QUAR), exist_ok=True)
            json.dump(store, open(QUAR, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        print(f"copied synopses quarantined : {quarantined}")

    # ---------- problem 2 ----------
    relinked, unresolved = 0, []
    if "--relink-twins" in sys.argv:
        # official rows, by title: anything not pinedrama
        official = {}
        for r in av:
            if r["platform_id"] != "pinedrama" and r["direct_link"].strip():
                official.setdefault(r["title_id"], r)
        for r in av:
            if r["platform_id"] != "pinedrama":
                continue
            tid = r["title_id"]
            twin = tid[:-len("-pinedrama")] if tid.endswith("-pinedrama") else None
            src = official.get(twin) if twin else None
            if src is not None:
                r["platform_id"] = src["platform_id"]
                r["direct_link"] = src["direct_link"]
                r["title_as_listed_on_platform"] = src["title_as_listed_on_platform"]
                r["last_checked"] = time.strftime("%Y-%m-%d")
                relinked += 1
            else:
                t = by_id.get(tid)
                unresolved.append({"title_id": tid,
                                   "primary_title": t["primary_title"] if t else "",
                                   "episode_count": t["episode_count"] if t else "",
                                   "why": "no twin with an official link - platform must be found per title"})
        print(f"pinedrama rows re-pointed to an official platform : {relinked}")
        print(f"pinedrama rows still unresolved                   : {len(unresolved)}")
        if not DRY:
            json.dump({"note": "pinedrama.com is a fan/affiliate directory, not a platform. "
                               "These rows still point at it and need an official platform found.",
                       "rows": unresolved},
                      open(REPORT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)

    if DRY:
        print("\n[dry-run] nothing written")
        return
    if quarantined or relinked:
        save("titles.csv", titles, t_term)
        save("availability.csv", av, a_term)
        print("\nwritten titles.csv, availability.csv")


if __name__ == "__main__":
    main()
