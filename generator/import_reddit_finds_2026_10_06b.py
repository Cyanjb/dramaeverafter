#!/usr/bin/env python3
"""Add the five Reddit finds that have no readable platform page.

Cyan, 6 Oct 2026, after the first pass left them out for having no web page:
"I am still missing" these five. They go in on the best source there is,
marked needs_check, with the Reddit thread that identified each one in
source_urls. No platform text is copied and none is invented:
  - The Elf Prince Is My Baby Daddy, The Warlord's Captured Virgin Bride,
    The Drunk Wolf: DramaWave (app-only, so no direct link; the site falls back
    to the DramaWave app page, as for 41 other DramaWave titles).
  - Love in Cyberpunk 2077: ShortsWave (app-only; new platform row).
  - Every Version of You: one full-movie upload on YouTube by Ever After
    Productions, tagged #aifilm by the uploader (new platform row; ai=yes).
Episode counts only where a platform shows them. Research with URLs:
scratchpad missing8.json (6 Oct).

Usage: python3 generator/import_reddit_finds_2026_10_06b.py [--apply]
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from merge_scrape import load, save

TODAY = "2026-10-06"
SOURCE = "reddit_finds_2026-10-06"
PLATFORMS = [
    {"platform_id": "shortswave", "name": "ShortsWave", "web_url": "", "pricing_model": "coins + IAP", "affiliate_program": "tbc"},
    {"platform_id": "youtube", "name": "YouTube", "web_url": "https://www.youtube.com/", "pricing_model": "free", "affiliate_program": "no"},
]
FINDS = [
    {"tid": "the-elf-prince-is-my-baby-daddy", "title": "The Elf Prince Is My Baby Daddy",
     "alt": "The Wood Elf Princess|Pregnant with the Elf Prince Triplets", "platform": "dramawave", "url": "",
     "eps": "", "ai": "", "src": "https://www.reddit.com/r/Vertical_Dramas/search/?q=%22Elf+Prince+Is+My+Baby+Daddy%22"},
    {"tid": "the-warlord-s-captured-virgin-bride", "title": "The Warlord's Captured Virgin Bride",
     "alt": "", "platform": "dramawave", "url": "", "eps": "", "ai": "",
     "src": "https://www.reddit.com/r/Askshortdramas/comments/1u4lvrv/the_warlords_captured_virgin_bride/"},
    {"tid": "the-drunk-wolf", "title": "The Drunk Wolf", "alt": "", "platform": "dramawave", "url": "",
     "eps": "", "ai": "",
     "src": "https://www.reddit.com/r/Vertical_Dramas/comments/1vlalo0/does_anyone_have_a_link_for_the_drunk_wolf_short/"},
    {"tid": "love-in-cyberpunk-2077", "title": "Love in Cyberpunk 2077", "alt": "", "platform": "shortswave",
     "url": "", "eps": "", "ai": "",
     "src": "https://www.reddit.com/r/Vertical_Dramas/comments/1uwo64z/love_in_cyberpunk_2077/"},
    {"tid": "every-version-of-you", "title": "Every Version of You", "alt": "", "platform": "youtube",
     "url": "https://www.youtube.com/watch?v=jbT2jJjh_VM", "eps": "", "ai": "yes",
     "src": "https://www.youtube.com/watch?v=jbT2jJjh_VM"},
]


def main(apply):
    plats, pf = load("platforms.csv"); titles, tf = load("titles.csv"); avail, af = load("availability.csv")
    have_p = {p["platform_id"] for p in plats}
    for p in PLATFORMS:
        if p["platform_id"] not in have_p:
            plats.append({k: "" for k in pf} | p); print("platform", p["platform_id"])
    held = {t["title_id"] for t in titles}
    for f in FINDS:
        if f["tid"] in held:
            print("already held:", f["tid"]); continue
        titles.append({k: "" for k in tf} | {"title_id": f["tid"], "slug": f["tid"], "primary_title": f["title"],
            "alt_titles": f["alt"], "year": "2026", "episode_count": f["eps"], "source_urls": f["src"],
            "last_verified": TODAY, "data_confidence": "needs_check", "source": SOURCE, "origin": "english",
            "ai": f["ai"]})
        avail.append({k: "" for k in af} | {"title_id": f["tid"], "platform_id": f["platform"],
            "title_as_listed_on_platform": f["title"], "direct_link": f["url"], "last_checked": TODAY})
        print("add", f["tid"])
    if apply:
        save("platforms.csv", pf, plats); save("titles.csv", tf, titles); save("availability.csv", af, avail)
        print("applied")


if __name__ == "__main__":
    main("--apply" in sys.argv)
