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

Nothing here writes anything. The Coverage export lags 2-3 days and
counts URLs, not pages; read it as Google's memory, not the site's size.
"""
import csv, glob, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECTIONS = ("titles", "where-to-watch", "actors", "tropes", "apps")

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


def main(folder):
    chart = read_chart(folder)
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
