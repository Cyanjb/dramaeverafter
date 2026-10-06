#!/usr/bin/env python3
"""Add the Reddit-sourced titles that have an official platform page.

Cyan, 6 Oct 2026: she found nine titles on Reddit that the site did not hold,
and asked for them to be checked on Reddit and the platforms' own sites. The
research (scratchpad missing8.json, every fact tied to a URL) found official
pages for two not added elsewhere:
  - The God Level Blacksmith, DramaBox 42000018757 (43 eps, 6.7M plays)
  - No Escape from the Vampire, AnyReel 5708 (60 eps), also listed by fans as
    Taming the Thorny Rose and Bound to the Vampire
Deny Me, Dragon King came in with the 28 Sep DramaBox import and One Night
Stand with the Empire's General through merge_scrape.py. Left out, because no
platform page could be read (Cyan's rule, 28 Sep: titles with a platform page
only): The Warlord's Captured Virgin Bride, The Drunk Wolf and The Elf Prince
Is My Baby Daddy (DramaWave, app-only), Love in Cyberpunk 2077 (ShortsWave, no
web catalogue), Every Version of You (a single YouTube upload, no app).

Rules as import_trending_2026_09_28.py: needs_check, origin english, ai blank
(neither page states it), synopses go to the facts file for the caption
pipeline, never to synopsis_short. Tropes only from the platform's own tags or
the title itself, vocabulary only.

Usage: python3 generator/import_reddit_finds_2026_10_06.py [--apply]
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from merge_scrape import load, save

TODAY = "2026-10-06"
SOURCE = "reddit_finds_2026-10-06"
FACTS = os.path.join(HERE, "staging", "facts_trending_2026-10-06.json")
FINDS = [
    {"tid": "the-god-level-blacksmith", "title": "The God Level Blacksmith", "alt": "",
     "platform": "dramabox", "url": "https://www.dramaboxdb.com/movie/42000018757",
     "eps": "43", "views": "6.7M", "year": "2026", "tropes": "secret identity",
     "synopsis": "In the shadows of a war-torn kingdom, Ronan Vire, the hidden Iron Wraith, fights for the top of the Hero's List in order to obtain the best medical resources to cure his little sister. However, he is then caught up in the battle between the kingdom and the demons. To save the realm from collapse, Ronan wields his shape-shifting hammer with God-level power and stands up against the demons with Princess Seraphina and allies from the Noble Houses."},
    {"tid": "no-escape-from-the-vampire", "title": "No Escape from the Vampire",
     "alt": "Taming the Thorny Rose|Bound to the Vampire",
     "platform": "anyreel", "url": "https://www.anyreel.app/movie/no-escape-from-the-vampire-5708",
     "eps": "60", "views": "", "year": "2026", "tropes": "vampire;possessive love",
     "synopsis": None},  # read from missing8.json below, verbatim
]


def main(apply):
    research = {x["title"]: x for x in json.load(open(sys.argv[sys.argv.index("--research") + 1], encoding="utf-8"))} \
        if "--research" in sys.argv else {}
    titles, tf = load("titles.csv"); avail, af = load("availability.csv"); snaps, sf = load("snapshots.csv")
    held = {t["title_id"] for t in titles}
    facts = json.load(open(FACTS, encoding="utf-8")) if os.path.exists(FACTS) else {}
    for f in FINDS:
        if f["tid"] in held:
            print("already held:", f["tid"]); continue
        syn = f["synopsis"] or research.get(f["title"], {}).get("synopsis")
        titles.append({k: "" for k in tf} | {"title_id": f["tid"], "slug": f["tid"], "primary_title": f["title"],
            "alt_titles": f["alt"], "year": f["year"], "episode_count": f["eps"], "tropes": f["tropes"],
            "source_urls": f["url"], "last_verified": TODAY, "data_confidence": "needs_check",
            "source": SOURCE, "origin": "english"})
        avail.append({k: "" for k in af} | {"title_id": f["tid"], "platform_id": f["platform"],
            "title_as_listed_on_platform": f["title"], "direct_link": f["url"], "view_count": f["views"],
            "view_count_date": TODAY if f["views"] else "", "last_checked": TODAY})
        if f["views"]:
            snaps.append({k: "" for k in sf} | {"title_id": f["tid"], "platform_id": f["platform"],
                                                 "view_count": f["views"], "date": TODAY})
        if syn:
            facts[f["tid"]] = {"copied_text": " ".join(syn.split()), "kind": "platform", "url": f["url"], "from": SOURCE}
        print("add", f["tid"], "facts" if syn else "NO FACTS")
    if apply:
        save("titles.csv", tf, titles); save("availability.csv", af, avail); save("snapshots.csv", sf, snaps)
        json.dump(facts, open(FACTS, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        print("applied")


if __name__ == "__main__":
    main("--apply" in sys.argv)
