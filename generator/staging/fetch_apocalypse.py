#!/usr/bin/env python3
"""One-off fetch: platform synopses for the apocalypse cluster, 5 Sep 2026.

Cyan's ask: apocalypse romances are trending; the cluster's pages must look
good. Fetches each title's own platform page (GoodShort JSON-LD, ReelShort
og/meta), banks facts to facts_apocalypse_2026-09-05.json in the staging
shape the caption pipeline reads (text, route, url, episodes, views).
Polite: one request per second, desktop UA, direct links from availability.
"""
import csv, json, re, time, urllib.request, html as htmllib
from collections import defaultdict

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"}
KEY = re.compile(r'apocalyp|zombie|doomsday|end.of.the.world|wasteland', re.I)

titles = list(csv.DictReader(open('data/titles.csv')))
avail = list(csv.DictReader(open('data/availability.csv')))
av = defaultdict(list)
for a in avail: av[a['title_id']].append(a)

cluster = [t for t in titles if KEY.search(t['primary_title'] + ' ' + t.get('alt_titles','') + ' ' + t.get('tropes',''))]

def fetch(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.read().decode('utf-8', 'replace')

out = {}
misses = []
for t in cluster:
    tid = t['title_id']
    rows = [a for a in av.get(tid, []) if (a.get('direct_link') or '').strip()]
    if not rows:
        misses.append((tid, 'no direct link'))
        continue
    a = rows[0]
    url = a['direct_link'].strip()
    try:
        page = fetch(url)
    except Exception as e:
        misses.append((tid, f'fetch failed: {e}'))
        time.sleep(1)
        continue
    text = ''
    episodes = ''
    views = ''
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', page, re.S):
        try:
            ld = json.loads(m.group(1))
        except Exception:
            continue
        items = ld if isinstance(ld, list) else [ld]
        for it in items:
            if isinstance(it, dict) and it.get('@type') in ('TVSeries', 'Movie', 'CreativeWork'):
                text = (it.get('description') or '').strip() or text
                episodes = str(it.get('numberOfEpisodes') or '') or episodes
    if not text:
        m = re.search(r'<meta (?:property="og:description"|name="description") content="([^"]+)"', page)
        if m: text = m.group(1).strip()
    m = re.search(r'Views</p><p[^>]*>([\d.]+[KMB]?)</p>', page)
    if m: views = m.group(1)
    text = htmllib.unescape(text)
    if text:
        out[tid] = {"text": text, "route": "platform", "url": url,
                    "episodes": episodes, "views": views,
                    "platform": a['platform_id']}
        print(f"OK  {tid[:50]:50} {len(text):4} chars ep={episodes:>3} views={views}")
    else:
        misses.append((tid, 'no synopsis on page'))
        print(f"MISS {tid[:50]}")
    time.sleep(1.0)

json.dump(out, open('generator/staging/facts_apocalypse_2026-09-05.json', 'w', encoding='utf-8'),
          indent=1, ensure_ascii=False)
print(f"\nbanked {len(out)} of {len(cluster)}; misses: {len(misses)}")
for tid, why in misses: print(f"  MISS {tid}: {why}")
