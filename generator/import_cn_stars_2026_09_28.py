#!/usr/bin/env python3
"""Import Chinese short-drama stars and their platform-confirmed titles.

Cyan, 28 Sep 2026: add the Chinese live-action stars (Chen Si, Zhao Xixi, Yao
Guanyu and others) and their headline titles, titles only where a platform
page confirms them. Source: generator/staging/cn_stars_research_2026-09-28.json,
each title read off its iQIYI International, DramaBox or WeTV page.

Rules, as import_trending_2026_09_28.py:
  - one page per drama. Where the same drama carries a different English title
    on another platform (verified: same cast, episode count and plot), the
    other title goes in alt_titles.
  - origin=chinese, data_confidence=needs_check. Hidden Love (WeTV, 24 eps) is
    skipped: that is a horizontal series, not a short drama.
  - a title already held under the same name goes to match_queue.csv, never
    merged.
  - the 14 stars get people rows (Han Yutong already exists), with the Chinese
    name and every credited variant ("Si Chen", "Ben", "Austin") in aka_names so
    later platform credits match. A title credits the target stars in its cast
    plus any co-star who matches exactly one existing person. Other co-stars
    are not created here.
  - synopses go to staging/facts_trending_2026-09-28.json for the caption
    pipeline, never to synopsis_short.

Usage: python3 generator/import_cn_stars_2026_09_28.py [--apply]
"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from merge_scrape import load, save, views_num
from import_trending_2026_09_28 import norm, slugify, aka_split

TODAY = "2026-09-28"
SOURCE = "cn_stars_research_2026-09-28"
RESEARCH = os.path.join(HERE, "staging", SOURCE + ".json")
FACTS = os.path.join(HERE, "staging", "facts_trending_2026-09-28.json")
PLATFORM = {"iqiyi": "iqiyi", "dramabox": "dramabox", "wetv": "wetv"}
ALT = {"Bright Moon of Spring Night": "Love in the Time of Shadows",
       "Phoenix Lord": "Their Legend, Written in Love",
       "Inescapable Scorching Love": "Your Love Is My Chains",
       "Starlight Redemption": "Falling Under the Stars",
       "When Fish Swim to Land": "Where the Fish Swim Ashore",
       "Depth of Love": "Secret Color Criticality"}
SKIP = {"Hidden Love"}


def plat(s):
    s = s.lower()
    return "iqiyi" if "iqiyi" in s or "iq.com" in s else "dramabox" if "dramabox" in s else "wetv" if "wetv" in s else None


def main(apply):
    d = json.load(open(RESEARCH, encoding="utf-8"))
    titles, tf = load("titles.csv"); avail, af = load("availability.csv"); credits, cf = load("credits.csv")
    people, pf = load("people.csv"); snaps, sf = load("snapshots.csv"); mq, mf = load("match_queue.csv")
    by_norm = {}
    for t in titles:
        for nm in [t["primary_title"]] + aka_split(t.get("alt_titles")):
            by_norm.setdefault(norm(nm), t["title_id"])
    slugs = {t["title_id"] for t in titles}
    pby = {}
    for p in people:
        for nm in [p["name"]] + aka_split(p.get("aka_names")):
            pby.setdefault(norm(nm), set()).add(p["person_id"])
    held = {(c["title_id"], c["person_id"]) for c in credits}
    facts = json.load(open(FACTS, encoding="utf-8"))

    # People first: the 14 stars.
    star_ids = {}
    for a in d["actors"]:
        akas = [a["chinese"]] if a.get("chinese") else []
        akas += [re.sub(r"\s*\(.*?\)\s*", "", x).strip() for x in a.get("aka") or []]
        parts = a["name"].split()
        if len(parts) == 2:
            akas.append(parts[1] + " " + parts[0])          # DramaBox writes given name first
        akas = [x for x in dict.fromkeys(akas) if x and norm(x) != norm(a["name"])]
        ids = pby.get(norm(a["name"]), set())
        if len(ids) == 1:
            pid = next(iter(ids))
            p = next(p for p in people if p["person_id"] == pid)
            have = aka_split(p.get("aka_names"))
            add = [x for x in akas if norm(x) not in {norm(h) for h in have}]
            if add:
                p["aka_names"] = "|".join(have + add)
        else:
            pid = slugify(a["name"])
            people.append({k: "" for k in pf} | {"person_id": pid, "slug": pid, "name": a["name"],
                "aka_names": "|".join(akas), "role_type": "actor", "data_confidence": "needs_check",
                "source": SOURCE})
        for nm in [a["name"]] + akas:
            pby[norm(nm)] = {pid}
        star_ids[norm(a["name"])] = pid
        for x in akas:
            star_ids[norm(x)] = pid

    created, queued, seen = [], [], set()
    for a in d["actors"]:
        for t in a["titles"]:
            if t["url"] in seen or t["title"] in SKIP:
                continue
            seen.add(t["url"])
            pid_ = plat(t["platform"])
            key = norm(t["title"])
            alt = ALT.get(t["title"], "")
            existing = by_norm.get(key) or (by_norm.get(norm(alt)) if alt else None)
            if existing:
                mq.append({"candidate_a": "%s (existing title)" % existing,
                           "candidate_b": "%s on %s (Chinese stars research %s)" % (t["title"], pid_, TODAY),
                           "evidence": "same title text; %s at %s" % (pid_, t["url"]), "status": "pending"})
                queued.append(t["title"]); continue
            slug = slugify(t["title"])
            if slug in slugs:
                queued.append(t["title"]); continue
            slugs.add(slug); by_norm[key] = slug
            titles.append({k: "" for k in tf} | {"title_id": slug, "slug": slug, "primary_title": t["title"],
                "alt_titles": alt, "year": str(t.get("year") or ""), "episode_count": str(t.get("episodes") or ""),
                "source_urls": t["url"], "last_verified": TODAY, "data_confidence": "needs_check",
                "source": SOURCE, "origin": "chinese"})
            v = views_num(str(t.get("views") or ""))
            disp = ("%.1fM" % (v / 1e6)) if v else ""
            avail.append({k: "" for k in af} | {"title_id": slug, "platform_id": pid_,
                "title_as_listed_on_platform": t["title"], "direct_link": t["url"], "view_count": disp,
                "view_count_date": TODAY if v else "", "last_checked": TODAY})
            if v:
                snaps.append({k: "" for k in sf} | {"title_id": slug, "platform_id": pid_, "view_count": disp, "date": TODAY})
            for name in t.get("cast") or []:
                ids = pby.get(norm(name), set())
                pid = star_ids.get(norm(name)) or (next(iter(ids)) if len(ids) == 1 else None)
                if pid and (slug, pid) not in held:
                    credits.append({k: "" for k in cf} | {"title_id": slug, "person_id": pid, "role": "actor"})
                    held.add((slug, pid))
            if t.get("synopsis"):
                facts.setdefault(slug, {"copied_text": t["synopsis"], "kind": "platform", "url": t["url"], "from": SOURCE})
            created.append(slug)
    stars = sorted(set(star_ids.values()))
    print("titles created %d, queued %d %s" % (len(created), len(queued), queued))
    print("stars %d, credits now: %s" % (len(stars), {s: sum(1 for c in credits if c["person_id"] == s) for s in stars}))
    if apply:
        for n, f, r in (("titles.csv", tf, titles), ("availability.csv", af, avail), ("credits.csv", cf, credits),
                        ("people.csv", pf, people), ("snapshots.csv", sf, snaps), ("match_queue.csv", mf, mq)):
            save(n, f, r)
        json.dump(facts, open(FACTS, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        print("applied")


if __name__ == "__main__":
    main("--apply" in sys.argv)
