#!/usr/bin/env python3
"""Credits and titles confirmed on DramaBox's own actor pages, 28 Sep 2026.

Cyan asked for the missing credit and the "ramoree" title fixed. Evidence:
dramaboxdb.com/name/11014 (Nicole Mattox: Almost Lover, Christmas With a
Country Bad Boy, Escape With Boss's Baby) and /name/12177 (Noah Fearnley,
including The Hockey Star's Remorse), plus each title's /movie/{bookId} page
for views, episode count, synopsis and cast. Banked in
staging/dramabox_actor_pages_2026-09-28.json.

- the-hockey-star-s-ramoree: primary_title corrected to "The Hockey Star's
  Remorse" (the slug stays: published URLs are permanent), episode_count
  filled, DramaBox link added.
- christmas-with-a-country-bad-boy, escape-with-boss-s-baby: DramaBox link
  added (Escape is the same production as our PineDrama row: Fearnley is
  already credited there and DramaBox lists him on it).
- almost-lover, food-love-robots: created, needs_check.
- Cast credited where a name matches exactly one person; a new name becomes
  a new person (Cyan approved creating people named on a platform page).
- the-great-and-powerful-genie: ai=yes. ReelShort's own page: "an
  AI-generated animated ReelShort original production". It has no human cast.
"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from merge_scrape import load, save
from import_trending_2026_09_28 import norm, slugify, aka_split
TODAY = "2026-09-28"; SRC = "dramabox_actor_pages_2026-09-28"
books = json.load(open(os.path.join(HERE, "staging", SRC + ".json"), encoding="utf-8"))
MAP = {"42000000808": "christmas-with-a-country-bad-boy", "41000110515": "escape-with-boss-s-baby",
       "41000116783": "the-hockey-star-s-ramoree", "42000001967": None, "41000112807": None}
titles, tf = load("titles.csv"); avail, af = load("availability.csv"); credits, cf = load("credits.csv")
people, pf = load("people.csv"); snaps, sf = load("snapshots.csv")
T = {t["title_id"]: t for t in titles}
pby = {}
for p in people:
    for nm in [p["name"]] + aka_split(p.get("aka_names")):
        pby.setdefault(norm(nm), set()).add(p["person_id"])
held = {(c["title_id"], c["person_id"]) for c in credits}
facts_path = os.path.join(HERE, "staging", "facts_trending_2026-09-28.json")
facts = json.load(open(facts_path, encoding="utf-8"))
for bid, b in books.items():
    tid = MAP[bid]
    url = "https://www.dramaboxdb.com/movie/%s/%s" % (bid, b["slug"])
    if tid is None:
        tid = slugify(b["title"]); assert tid not in T, tid
        row = {k: "" for k in tf} | {"title_id": tid, "slug": tid, "primary_title": b["title"],
            "episode_count": str(b["eps"]), "source_urls": url, "last_verified": TODAY,
            "data_confidence": "needs_check", "source": SRC, "origin": "english"}
        titles.append(row); T[tid] = row
    t = T[tid]
    if tid == "the-hockey-star-s-ramoree":
        t["primary_title"] = b["title"]
    if not t.get("episode_count"): t["episode_count"] = str(b["eps"])
    if not any(a["title_id"] == tid and a["platform_id"] == "dramabox" for a in avail):
        disp = "%.1fM" % (b["views"] / 1e6)
        avail.append({k: "" for k in af} | {"title_id": tid, "platform_id": "dramabox",
            "title_as_listed_on_platform": b["title"], "direct_link": url, "view_count": disp,
            "view_count_date": TODAY, "last_checked": TODAY})
        snaps.append({k: "" for k in sf} | {"title_id": tid, "platform_id": "dramabox", "view_count": disp, "date": TODAY})
    for name in b["cast"]:
        ids = pby.get(norm(name), set())
        if len(ids) > 1: continue
        if ids: pid = next(iter(ids))
        else:
            pid = slugify(name)
            people.append({k: "" for k in pf} | {"person_id": pid, "slug": pid, "name": name, "role_type": "actor",
                                                 "data_confidence": "needs_check", "source": SRC})
            pby[norm(name)] = {pid}; print("new person", pid)
        if (tid, pid) not in held:
            credits.append({k: "" for k in cf} | {"title_id": tid, "person_id": pid, "role": "actor"})
            held.add((tid, pid)); print("credit", tid, pid)
    if b.get("syn") and not (t.get("synopsis_short") or "").strip():
        facts.setdefault(tid, {"copied_text": b["syn"], "kind": "platform", "url": url, "from": SRC})
T["the-great-and-powerful-genie"]["ai"] = "yes"
for n, f, r in (("titles.csv", tf, titles), ("availability.csv", af, avail), ("credits.csv", cf, credits),
                ("people.csv", pf, people), ("snapshots.csv", sf, snaps)):
    save(n, f, r)
json.dump(facts, open(facts_path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
