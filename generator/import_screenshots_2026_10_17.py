#!/usr/bin/env python3
"""Add the GoodShort and DramaWave shows from Cyan's app screenshots (17 Oct 2026).

Cyan put screenshots of the GoodShort, DramaWave and DramaBox apps in Drive and
said "do 1 and 2": add what is missing, ranked shows first. DramaBox's went in
through merge_dramabox.py (staging/dramabox_2026-10-17.json). This adds:

  - 29 GoodShort shows: every ranked or top-searched title in her screenshots
    plus 2 search suggestions, each read on its own goodshort.com page. They
    were found by walking GoodShort's own listing pages (/channel/..,
    /dramas/playlets, the genre listings); the site search is disallowed by
    robots.txt and was not used. view_count is the website's figure, which is
    lower than the app's (the app's chart counts are kept in the record).
  - 1 DramaWave show, Broken Vows: The Goddess Casts You Down, the only one of
    the 41 charted DramaWave shows on DramaWave's public web catalogue. Its
    link is the public share page, mydramawave.com/share/series/<id>.

Platform synopses are banked in staging/facts_trending_2026-10-17.json for the
caption pipeline and are never written to synopsis_short. The records with
everything the pages said are staging/screenshots_2026-10-17.json.

Usage: python3 generator/import_screenshots_2026_10_17.py [--apply]
"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from merge_scrape import load, save

TODAY = "2026-10-17"
REC = os.path.join(HERE, "staging", "screenshots_2026-10-17.json")
FACTS = os.path.join(HERE, "staging", "facts_trending_2026-10-17.json")
ALIAS = {"hiddenidentity": "secret identity", "familystory": "family bonds"}


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", (s or "").lower().replace("’", "'")).strip("-")


def norm(s):
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def main(apply):
    rec = json.load(open(REC, encoding="utf-8"))
    titles, tf = load("titles.csv"); avail, af = load("availability.csv"); vocab_rows, _ = load("tropes.csv")
    vocab = {}
    for v in vocab_rows:
        for k in (v.get("name"), v.get("slug")):
            if k: vocab.setdefault(norm(k), v["name"])
    held_ids = {t["title_id"] for t in titles}
    held_names = {norm(n): t["title_id"] for t in titles
                  for n in [t["primary_title"]] + (t.get("alt_titles") or "").split("|") if n.strip()}
    facts = {}
    for r in rec:
        name = r["title"].replace("’", "'")
        tid = slug(name)
        if tid in held_ids or norm(name) in held_names:
            print("held already, skipped:", name); continue
        tropes = []
        for tag in r.get("tags") or []:
            v = ALIAS.get(norm(tag)) or vocab.get(norm(tag))
            if v and v not in tropes: tropes.append(v)
        alt = r["query"] if norm(r["query"]) != norm(name) and not r["query"].endswith("...") else ""
        titles.append({k: "" for k in tf} | {
            "title_id": tid, "slug": tid, "primary_title": name, "alt_titles": alt, "year": "2026",
            "episode_count": str(r.get("episodes") or ""), "genres": "romance" if "Romance" in (r.get("genres") or []) else "",
            "tropes": ";".join(tropes), "poster_ref": r.get("poster") or "", "source_urls": r["url"],
            "last_verified": TODAY, "data_confidence": "needs_check", "source": "cyan_screenshots_2026-10-17",
            "origin": "english"})
        avail.append({k: "" for k in af} | {
            "title_id": tid, "platform_id": r["platform"], "title_as_listed_on_platform": name,
            "direct_link": r["url"], "view_count": r.get("views") or "", "view_count_date": TODAY if r.get("views") else "",
            "last_checked": TODAY})
        held_ids.add(tid); held_names[norm(name)] = tid
        facts[tid] = {"copied_text": r["synopsis"], "kind": "platform", "url": r["url"], "fetched": TODAY}
        print("add", r["platform"], tid, "|", r.get("seen_in_app", ""))
    if apply:
        save("titles.csv", tf, titles); save("availability.csv", af, avail)
        json.dump(facts, open(FACTS, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("applied", len(facts))


if __name__ == "__main__":
    main("--apply" in sys.argv)
