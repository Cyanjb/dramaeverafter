#!/usr/bin/env python3
"""Add Cyan's AI pick of the week, which the database does not hold yet.

Cyan, 14 Oct 2026: "For the pick of the week ... My Nonstop Chatter Unlocked
My Autistic Stepbrother's World. It's AI on DramaBox." DramaBox shelved it on
12 Oct 2026, after the last DramaBox scrape (and the GitHub runner gets 403s
from DramaBox anyway), so it goes in by hand from its own detail page:
https://www.dramaboxdb.com/movie/42000030222 (bookInfo read 14 Oct: 30
episodes, 209,712 plays). ai=yes is Cyan's call; DramaBox's English title
carries no AI flag. The caption lives in staging/captions_2026_10_14_pick.py.

Usage: python3 generator/import_pick_2026_10_14.py [--apply]
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from merge_scrape import load, save

TODAY = "2026-10-14"
TID = "my-nonstop-chatter-unlocked-autistic-stepbrother-s-world"
TITLE = "My Nonstop Chatter Unlocked Autistic Stepbrother's World"
URL = "https://www.dramaboxdb.com/movie/42000030222/my-nonstop-chatter-unlocked-autistic-stepbrother-s-world"
POSTER = "https://thwztchapter.dramaboxdb.com/data/cppartner/4x2/42x0/420x0/42000030222/42000030222.jpg"


def main(apply):
    titles, tf = load("titles.csv"); avail, af = load("availability.csv")
    if TID in {t["title_id"] for t in titles}:
        print("already held:", TID); return
    titles.append({k: "" for k in tf} | {"title_id": TID, "slug": TID, "primary_title": TITLE,
        "year": "2026", "episode_count": "30", "genres": "drama",
        "tropes": "cute kids;step-siblings;family bonds;family drama;healing;redemption",
        "poster_ref": POSTER, "source_urls": URL, "last_verified": TODAY,
        "data_confidence": "verified", "source": "cyan_pick_2026-10-14", "origin": "english", "ai": "yes"})
    avail.append({k: "" for k in af} | {"title_id": TID, "platform_id": "dramabox",
        "title_as_listed_on_platform": TITLE, "direct_link": URL, "view_count": "209.7K",
        "view_count_date": TODAY, "last_checked": TODAY})
    print("add", TID)
    if apply:
        save("titles.csv", tf, titles); save("availability.csv", af, avail); print("applied")


if __name__ == "__main__":
    main("--apply" in sys.argv)
