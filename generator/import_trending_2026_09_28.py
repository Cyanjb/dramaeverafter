#!/usr/bin/env python3
"""Import the platform-chart titles from the 28 Sep 2026 trending research.

Cyan, 28 Sep 2026, on the trending gap report (TRENDING-GAPS-2026-09-28.md):
import all titles that have a platform page, AI titles included and labelled,
as needs_check. Source: generator/staging/trending_research_2026-09-28.json,
key platforms.platforms.<platform_id>.titles, each read off the platform's own
chart and title page.

The database rules are merge_scrape.py's, applied to a one-off source:
  NEW TITLE: data_confidence=needs_check, origin english unless the platform
    marks it a dub (then chinese, adapters.md sec 11), ai=yes where the
    platform badges it AI, slug in house style (apostrophes become hyphens),
    never colliding with an existing slug.
  DUBS (CONVENTIONS.md, 24 Sep): "(DUBBED)" and kin are stripped for the title.
    A dub of a show we hold becomes a second availability row on that show with
    version=english-dub; a dub with no original on file keeps its own page,
    marked english-dub.
  SAME NAME ALREADY HELD, NOT A DUB: match_queue.csv, never created, never
    merged. Same-name productions across platforms are usually different shows.
  NEAR NAME (hyphenless or close spelling): match_queue.csv as well.
  SAME TITLE ON TWO PLATFORMS IN THIS IMPORT: one page, the listing with the
    larger view count; the other listing goes to match_queue.csv.
  SYNOPSES are never written to synopsis_short. They go to
    staging/facts_trending_2026-09-28.json, which caption_pipeline.load_facts()
    reads, so the caption pipeline has them as the fact source.
  CREDITS: a cast name matching exactly one person (name or aka, | or ;)
    is credited. Cyan approved creating new people named on a platform page
    (28 Sep); a name that is only CLOSE to an existing person is held, never
    created, and listed in the report.
  VIEWS: view_count and view_count_date on availability, plus a snapshots row.

Usage:
    python3 generator/import_trending_2026_09_28.py            # dry run, report only
    python3 generator/import_trending_2026_09_28.py --apply
"""
import difflib, json, os, re, sys, unicodedata
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from merge_scrape import load, save, views_num, EXCLUDE_RE  # noqa: E402

TODAY = "2026-09-28"
SOURCE = "trending_research_2026-09-28"
RESEARCH = os.path.join(HERE, "staging", "trending_research_2026-09-28.json")
FACTS_OUT = os.path.join(HERE, "staging", "facts_trending_2026-09-28.json")
# Cast strings the platform ran together, split by hand (checked 28 Sep 2026).
CAST_FIX = {"Mitchel BufaliniBrittany Marsicek": ["Mitchel Bufalini", "Brittany Marsicek"]}
# DramaBox's performerList on a dubbed Chinese show is the ON-SCREEN cast, not
# the English voice cast, so every credit here is role=actor (not dub_voice).
DUB_RE = re.compile(r"\s*[\(\[]\s*(eng(lish)?\s*)?dub(bed)?(\s*version)?\s*[\)\]]\s*", re.I)


def norm(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]", "", s.lower())


def slugify(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode()
    s = s.lower().replace("&", " and ")
    s = re.sub(r"[’']", "-", s)
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return re.sub(r"-{2,}", "-", s).strip("-")


def aka_split(s):
    return [x.strip() for x in re.split(r"[|;]", s or "") if x.strip()]


def main(apply):
    research = json.load(open(RESEARCH, encoding="utf-8"))["platforms"]["platforms"]
    titles, tf = load("titles.csv")
    avail, af = load("availability.csv")
    credits, cf = load("credits.csv")
    people, pf = load("people.csv")
    snaps, sf = load("snapshots.csv")
    mq, mf = load("match_queue.csv")
    plat_ids = {r["platform_id"] for r in load("platforms.csv")[0]}

    by_norm, by_slug_nohyph = {}, {}
    for t in titles:
        for nm in [t["primary_title"]] + aka_split(t.get("alt_titles")):
            by_norm.setdefault(norm(nm), t["title_id"])
        by_slug_nohyph.setdefault(t["title_id"].replace("-", ""), t["title_id"])
    slugs = {t["title_id"] for t in titles}
    held_links = {r["direct_link"].rstrip("/") for r in avail if r.get("direct_link")}
    mq_text = "\n".join(",".join(r.values()) for r in mq)

    person_by_name = {}
    for p in people:
        for nm in [p["name"]] + aka_split(p.get("aka_names")):
            person_by_name.setdefault(norm(nm), set()).add(p["person_id"])
    person_ids = {p["person_id"] for p in people}
    held_pairs = {(c["title_id"], c["person_id"]) for c in credits}

    # Collect chart listings with a page.
    listings = []
    for pid, pl in research.items():
        for x in pl["titles"]:
            url = (x.get("url") or "").strip()
            name = (x.get("title") or "").strip()
            if not url or not name or EXCLUDE_RE.search(name):
                continue
            dub = bool(DUB_RE.search(name))
            base = DUB_RE.sub(" ", name).strip()
            listings.append(dict(pid=pid, url=url, listed=name, base=base, dub=dub,
                                 views=views_num(str(x.get("views") or "")),
                                 views_disp=str(x.get("views") or "").strip(),
                                 episodes=x.get("episodes"), synopsis=x.get("synopsis"),
                                 cast=[n for c in (x.get("cast") or []) if c and c.strip()
                                       for n in CAST_FIX.get(c.strip(), [c.strip()])],
                                 ai=bool(x.get("ai_badge"))))

    report = Counter()
    queued, created, dub_rows, held_people, new_people = [], [], [], [], []
    facts = {}

    def queue(a, b, evidence):
        if b in mq_text:
            report["already_queued"] += 1
            return
        mq.append({"candidate_a": a, "candidate_b": b, "evidence": evidence, "status": "pending"})
        queued.append((a, b))

    # One page per base title in this import: biggest listing wins.
    groups = {}
    for L in listings:
        groups.setdefault(norm(L["base"]), []).append(L)

    for key, group in groups.items():
        group.sort(key=lambda L: -L["views"])
        lead = group[0]
        if lead["pid"] not in plat_ids:
            report["platform_not_in_platforms_csv"] += 1
            continue
        if lead["url"].rstrip("/") in held_links:
            report["link_already_held"] += 1
            continue
        existing = by_norm.get(key) or by_slug_nohyph.get(slugify(lead["base"]).replace("-", ""))
        if existing:
            if lead["dub"] and not any(r["title_id"] == existing and r["platform_id"] == lead["pid"] for r in avail):
                dub_rows.append((existing, lead))
            else:
                queue("%s (existing title)" % existing,
                      "%s on %s (trending research %s)" % (lead["listed"], lead["pid"], TODAY),
                      "same title text; %s lists '%s' at %s. Same-name shows across platforms are usually different productions." % (lead["pid"], lead["listed"], lead["url"]))
            continue
        close = difflib.get_close_matches(key, list(by_norm), n=1, cutoff=0.92)
        if close:
            queue("%s (existing title)" % by_norm[close[0]],
                  "%s on %s (trending research %s)" % (lead["listed"], lead["pid"], TODAY),
                  "near-identical title; %s lists '%s' at %s" % (lead["pid"], lead["listed"], lead["url"]))
            continue
        slug = slugify(lead["base"])
        if not slug or slug in slugs:
            queue("%s (existing slug)" % slug, "%s on %s" % (lead["listed"], lead["pid"]), "slug collision; %s" % lead["url"])
            continue
        created.append((slug, lead))
        slugs.add(slug)
        by_norm[key] = slug
        for other in group[1:]:
            queue("%s (created %s from %s)" % (slug, TODAY, lead["pid"]),
                  "%s on %s (trending research %s)" % (other["listed"], other["pid"], TODAY),
                  "same title on two platforms in one import; %s at %s" % (other["pid"], other["url"]))

    def add_avail(tid, L):
        avail.append({k: "" for k in af} | {
            "title_id": tid, "platform_id": L["pid"], "title_as_listed_on_platform": L["listed"],
            "direct_link": L["url"], "view_count": L["views_disp"] if L["views"] else "",
            "view_count_date": TODAY if L["views"] else "", "last_checked": TODAY,
            "version": "english-dub" if L["dub"] else ""})
        if L["views"]:
            snaps.append({k: "" for k in sf} | {"title_id": tid, "platform_id": L["pid"],
                                                 "view_count": L["views_disp"], "date": TODAY})

    def add_cast(tid, L):
        for name in L["cast"]:
            ids = person_by_name.get(norm(name), set())
            if len(ids) == 1:
                pid = next(iter(ids))
            elif len(ids) > 1:
                report["cast_ambiguous"] += 1
                continue
            else:
                close = difflib.get_close_matches(norm(name), list(person_by_name), n=1, cutoff=0.9)
                if close:
                    held_people.append((name, sorted(person_by_name[close[0]]), tid))
                    continue
                pid = slugify(name)
                if not pid or pid in person_ids:
                    report["person_slug_collision"] += 1
                    continue
                people.append({k: "" for k in pf} | {"person_id": pid, "slug": pid, "name": name.strip(),
                                                     "role_type": "actor", "data_confidence": "needs_check",
                                                     "source": "%s (%s cast list)" % (SOURCE, L["pid"])})
                person_ids.add(pid)
                person_by_name[norm(name)] = {pid}
                new_people.append((name, tid))
            if (tid, pid) not in held_pairs:
                credits.append({k: "" for k in cf} | {"title_id": tid, "person_id": pid,
                                                      "role": "actor"})
                held_pairs.add((tid, pid))
                report["credits_added"] += 1

    for slug, L in created:
        titles.append({k: "" for k in tf} | {
            "title_id": slug, "slug": slug, "primary_title": L["base"],
            "episode_count": str(L["episodes"] or ""), "source_urls": L["url"],
            "last_verified": TODAY, "data_confidence": "needs_check", "source": SOURCE,
            "origin": "chinese" if L["dub"] else "english", "ai": "yes" if L["ai"] else ""})
        add_avail(slug, L)
        add_cast(slug, L)
        if L["synopsis"]:
            facts[slug] = {"copied_text": L["synopsis"], "kind": "platform", "url": L["url"], "from": SOURCE}
    for tid, L in dub_rows:
        add_avail(tid, L)

    print("listings with a page: %d, distinct titles: %d" % (len(listings), len(groups)))
    print("create: %d  (dub pages %d, AI-badged %d, with synopsis %d, platforms %s)" % (
        len(created), sum(L["dub"] for _, L in created), sum(L["ai"] for _, L in created),
        len(facts), dict(Counter(L["pid"] for _, L in created))))
    print("dub rows added to titles we hold: %d %s" % (len(dub_rows), [t for t, _ in dub_rows]))
    print("to match_queue: %d" % len(queued))
    print("new people: %d, close names held: %d, %s" % (len(new_people), len(held_people), dict(report)))
    for h in held_people:
        print("  HELD person", h)
    if apply:
        save("titles.csv", tf, titles)
        save("availability.csv", af, avail)
        save("credits.csv", cf, credits)
        save("people.csv", pf, people)
        save("snapshots.csv", sf, snaps)
        save("match_queue.csv", mf, mq)
        json.dump(facts, open(FACTS_OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        print("applied")
    return created, queued, held_people, new_people


if __name__ == "__main__":
    main("--apply" in sys.argv)
