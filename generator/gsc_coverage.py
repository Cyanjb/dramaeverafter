#!/usr/bin/env python3
"""Read a Search Console Coverage export against what the repo actually publishes.

    python3 generator/gsc_coverage.py <folder with Chart.csv and "Critical issues.csv">

Born 10 Sep 2026 from Cyan's question: "why is it saying I have 10K pages?
I don't have that many, do I?" She does. Every title makes two pages
(/titles and /where-to-watch), every actor one, every trope one, and
Netlify's Pretty URLs answer the extensionless twin of each, so Google
knows roughly one URL per page plus one duplicate per page it has tried
without .html. This prints the two sides next to each other so the number
stops being a surprise:

  KNOWN      what Google says it knows (indexed + not indexed, last day)
  PUBLISHED  html files in the repo, how many carry noindex, sitemap size
  REASONS    each "not indexed" reason with what it means for this site
  DRILLDOWN  if the folder is a reason's drilldown export (Table.csv of
             URLs), each URL classified against the repo: a page we have
             noindexed ourselves, an indexable page Google declined, an
             extensionless twin, or a file that no longer exists. The
             first two are the whole question: the 10 Sep drilldown
             showed the 29 Aug jump was Google's own verdict, crawled
             before our noindex shipped, not Google filing our noindex.

Nothing here writes anything. The Coverage export lags 2-3 days and
counts URLs, not pages; read it as Google's memory, not the site's size.
"""
import csv, glob, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECTIONS = ("titles", "actors", "tropes", "apps")

MEANING = {
    "Alternative page with proper canonical tag":
        "duplicate URL variants (extensionless twins served by Netlify Pretty "
        "URLs, plus http/www). Harmless: Google honours the canonical. Drops "
        "only when Pretty URLs is off and the _redirects rules fire.",
    "Page with redirect":
        "URLs answered by _redirects (trope folds, slug fixes). Expected.",
    "Discovered - currently not indexed":
        "Google found the URL (sitemap or link) and chose not to crawl it "
        "yet. On this site that is mostly the thin pages: noindexed since "
        "5 Sep and out of the sitemap, so they will fade slowly, not fast.",
    "Crawled - currently not indexed":
        "Google crawled the page and left it out. Quality verdict, page by "
        "page. The top earner landed here on 29 Aug; this bucket shrinks "
        "as captions and cast replace platform text.",
    "Server error (5xx)": "hosting fault. Should stay at zero.",
}


def norm(s):
    return s.replace("–", "-").replace("—", "-").strip()


def read_chart(folder):
    rows = list(csv.DictReader(open(os.path.join(folder, "Chart.csv"), encoding="utf-8-sig")))
    days = [r for r in rows if r.get("Indexed")]
    if not days:
        return None
    peak = max(days, key=lambda r: int(r["Indexed"]))
    last = days[-1]
    drop = None
    for a, b in zip(days, days[1:]):
        if int(b["Indexed"]) < int(a["Indexed"]) * 0.7:
            drop = (a, b)
    return rows, days, peak, last, drop


def published():
    total = noidx = 0
    for sec in SECTIONS:
        for p in glob.glob(os.path.join(ROOT, sec, "**", "*.html"), recursive=True):
            total += 1
            if 'content="noindex"' in open(p, encoding="utf-8").read():
                noidx += 1
    for p in glob.glob(os.path.join(ROOT, "*.html")):
        if not p.endswith("404.html"):
            total += 1
    sitemap = open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read().count("<loc>")
    return total, noidx, sitemap


def classify(url):
    u = url.replace("https://dramaeverafter.com/", "").replace("https://dramaeverafter.com", "")
    sec = u.split("/")[0] if "/" in u else "root"
    twin = not (u.endswith(".html") or u.endswith("/") or u == "")
    p = (u + ".html") if twin else (u + "index.html" if u.endswith("/") or u == "" else u)
    full = os.path.join(ROOT, p)
    if not os.path.exists(full):
        state = "file gone"
    elif 'content="noindex"' in open(full, encoding="utf-8").read():
        state = "noindexed by us"
    else:
        state = "INDEXABLE, Google declined"
    return sec, state, ("extensionless twin" if twin else "html"), p


def drilldown(folder):
    path = os.path.join(folder, "Table.csv")
    if not os.path.exists(path):
        return
    rows = list(csv.DictReader(open(path, encoding="utf-8-sig")))
    if not rows or "URL" not in rows[0]:
        return
    meta = os.path.join(folder, "Metadata.csv")
    issue = ""
    if os.path.exists(meta):
        for r in csv.DictReader(open(meta, encoding="utf-8-sig")):
            if r.get("Property") == "Issue":
                issue = norm(r["Value"])
    print(f"DRILLDOWN  {len(rows):,} URLs{' for ' + issue if issue else ''} (GSC caps the export at 1,000)")
    crawled = sorted(set(r.get("Last crawled", "") for r in rows))
    if crawled and crawled[0]:
        print(f"           last crawled between {crawled[0]} and {crawled[-1]}")
    counts, pages = {}, {}
    for r in rows:
        sec, state, kind, p = classify(r["URL"])
        counts[(state, sec)] = counts.get((state, sec), 0) + 1
        pages.setdefault(state, set()).add(p)
    for state in ("INDEXABLE, Google declined", "noindexed by us", "file gone"):
        n = sum(v for (s, _), v in counts.items() if s == state)
        if not n:
            continue
        secs = ", ".join(f"{sec} {v}" for (s, sec), v in sorted(counts.items(), key=lambda x: -x[1]) if s == state)
        print(f"  {n:>6,}  {state}  ({len(pages[state]):,} distinct pages: {secs})")


def main(folder):
    chart = read_chart(folder)
    if not os.path.exists(os.path.join(folder, "Chart.csv")) or "Indexed" not in open(os.path.join(folder, "Chart.csv"), encoding="utf-8-sig").readline():
        drilldown(folder)
        return
    total, noidx, sitemap = published()
    print(f"PUBLISHED  {total:,} html pages, {noidx:,} carry noindex, "
          f"{total - noidx:,} indexable, sitemap lists {sitemap:,}")
    if chart:
        rows, days, peak, last, drop = chart
        known = int(last["Indexed"]) + int(last["Not indexed"])
        print(f"KNOWN      Google, {last['Date']}: {int(last['Indexed']):,} indexed + "
              f"{int(last['Not indexed']):,} not indexed = {known:,} URLs")
        print(f"           peak indexed {int(peak['Indexed']):,} on {peak['Date']}")
        if drop:
            a, b = drop
            print(f"           index EJECTION {a['Date']} -> {b['Date']}: "
                  f"{int(a['Indexed']):,} -> {int(b['Indexed']):,}")
        extra = known - total
        print(f"           {extra:,} more URLs than pages: extensionless twins, "
              f"redirected old URLs, and pages since deleted")
        imp = [(r["Date"], int(r["Impressions"])) for r in rows if r.get("Impressions")]
        top = max(imp, key=lambda x: x[1])
        print(f"IMPRESSIONS peak {top[1]:,} on {top[0]}; last 5 days: "
              + ", ".join(f"{d[5:]}={n}" for d, n in imp[-5:]))
    path = os.path.join(folder, "Critical issues.csv")
    if os.path.exists(path):
        print("REASONS")
        for r in csv.DictReader(open(path, encoding="utf-8-sig")):
            reason = norm(r["Reason"])
            print(f"  {int(r['Pages']):>6,}  {reason}")
            print(f"          {MEANING.get(reason, 'not seen before; read it on the GSC page')}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1])
