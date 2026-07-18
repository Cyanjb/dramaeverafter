#!/usr/bin/env python3
"""DramaEverAfter static site generator. Reads data/*.csv, writes dist/."""
import csv, os, re, json, shutil
from collections import defaultdict

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA, DIST = os.path.join(os.path.dirname(ROOT), "data"), os.path.dirname(ROOT)
DOMAIN = "https://dramaeverafter.com"
UPDATED = "July 2026"

def rows(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as f:
        return list(csv.DictReader(f))

def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

def tslug(t): return t.get("slug") or slug(t["primary_title"])
def pslug(p): return p.get("slug") or slug(p["name"])

people = rows("people.csv")
titles = rows("titles.csv")
# Skip malformed rows that would render as ".html" (empty slug AND empty title).
titles = [t for t in titles if (t.get("slug") or "").strip() or (t.get("primary_title") or "").strip()]
platforms = {p["platform_id"]: p for p in rows("platforms.csv")}
availability = rows("availability.csv")
credits = rows("credits.csv")

t_by_id = {t["title_id"]: t for t in titles}
p_by_id = {p["person_id"]: p for p in people}
avail_by_title = defaultdict(list)
for a in availability: avail_by_title[a["title_id"]].append(a)
credits_by_person = defaultdict(list)
credits_by_title = defaultdict(list)
for c in credits:
    credits_by_person[c["person_id"]].append(c)
    credits_by_title[c["title_id"]].append(c)

def tropes_of(t):
    return [x.strip() for x in t["tropes"].split(";") if x.strip()]

all_tropes = sorted({tr for t in titles for tr in tropes_of(t)})

CSS = """
:root{--paper:#FBF7F2;--ink:#2A2226;--plum:#2B1B2E;--wine:#7A2B4A;--gold:#C9962E;--gold-deep:#A87B1F;--blush:#EFD9DE;--line:#E4D8CE}
*{margin:0;padding:0;box-sizing:border-box}
body{background:var(--paper);color:var(--ink);font-family:'Atkinson Hyperlegible',Georgia,serif;font-size:18px;line-height:1.6}
h1,h2,h3{font-family:'Fraunces','Playfair Display',Georgia,serif;font-weight:600;line-height:1.15;color:var(--plum)}
a{color:var(--wine)}
.wrap{max-width:760px;margin:0 auto;padding:0 20px}
.site-head{border-bottom:1px solid var(--line);padding:14px 0}
.site-head .wrap{display:flex;justify-content:space-between;align-items:baseline;flex-wrap:wrap;gap:6px}
.logo{font-family:'Fraunces',Georgia,serif;font-size:1.15rem;font-weight:700;color:var(--plum);text-decoration:none}
.logo em{font-style:normal;color:var(--gold-deep)}
.tag{font-size:.78rem;color:#8a7a70}
.hero{padding:40px 0 32px;background:linear-gradient(180deg,var(--paper) 0%,var(--blush) 140%)}
.hero-grid{display:grid;grid-template-columns:150px 1fr;gap:26px;align-items:start}
.frame{aspect-ratio:9/16;background:var(--plum);border-radius:14px;position:relative;overflow:hidden;box-shadow:0 10px 28px rgba(43,27,46,.28)}
.frame::after{content:"EP 01";position:absolute;top:10px;left:10px;font-size:.6rem;letter-spacing:.14em;color:var(--gold);border:1px solid var(--gold);border-radius:4px;padding:2px 6px}
.frame .ph{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;color:#b9a0b3;font-size:.7rem;text-align:center;padding:0 12px}
.eyebrow{font-size:.74rem;letter-spacing:.16em;text-transform:uppercase;color:var(--gold-deep);margin-bottom:8px}
h1{font-size:clamp(1.9rem,6.5vw,2.7rem)}
.lede{margin-top:10px;font-size:1.02rem}
.lede strong{color:var(--wine)}
.stat-row{display:flex;gap:22px;margin-top:18px;flex-wrap:wrap}
.stat .n{font-family:'Fraunces',Georgia,serif;font-size:1.5rem;font-weight:700;color:var(--plum);display:block;line-height:1}
.stat .l{font-size:.72rem;letter-spacing:.1em;text-transform:uppercase;color:#8a7a70}
section{padding:26px 0}
h2{font-size:1.45rem;margin-bottom:6px}
.updated{font-size:.8rem;color:#8a7a70;margin-bottom:16px}
.card{display:grid;grid-template-columns:84px 1fr;gap:18px;padding:18px 0;border-top:1px solid var(--line)}
.card:last-of-type{border-bottom:1px solid var(--line)}
.poster{aspect-ratio:9/16;background:var(--plum);border-radius:9px;position:relative}
.poster span{position:absolute;inset:0;display:flex;align-items:flex-end;justify-content:center;padding-bottom:8px;color:#b9a0b3;font-size:.58rem}
.card h3{font-size:1.15rem}
.card h3 a{color:var(--plum);text-decoration:none}
.card h3 a:hover{color:var(--wine)}
.meta{font-size:.82rem;color:#7d6e64;margin:3px 0 8px}
.tropes{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:12px}
.trope{font-size:.72rem;background:var(--blush);color:var(--wine);border-radius:5px;padding:3px 8px;text-decoration:none}
.watch{display:inline-block;background:var(--gold);color:#241a05;text-decoration:none;font-weight:700;font-size:.85rem;border-radius:8px;padding:8px 14px;box-shadow:0 2px 0 var(--gold-deep);margin:0 6px 6px 0}
.watch:hover{background:#d8a93e}
.watch.pending{background:#efe7dc;color:#8a7a70;box-shadow:none}
.role-tag{font-size:.7rem;letter-spacing:.1em;text-transform:uppercase;color:var(--gold-deep);font-weight:700}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:16px}
.tile{background:#fff;border:1px solid var(--line);border-radius:12px;padding:14px;text-decoration:none;color:var(--ink)}
.tile:hover{border-color:var(--wine)}
.tile .nm{font-family:'Fraunces',Georgia,serif;font-weight:700;color:var(--plum);font-size:1.02rem}
.tile .kf{font-size:.78rem;color:#7d6e64;margin-top:4px}
.chipsrow{display:flex;gap:8px;flex-wrap:wrap}
.chip{font-size:.82rem;border:1.5px solid var(--line);background:#fff;border-radius:999px;padding:6px 14px;text-decoration:none;color:var(--ink)}
.chip:hover{border-color:var(--wine);color:var(--wine)}
.faq{background:var(--plum);color:#EFE4EA;padding:38px 0 46px}
.faq h2{color:#fff}
.faq details{border-bottom:1px solid #4a3450;padding:13px 0}
.faq summary{cursor:pointer;font-weight:700}
.faq p{margin-top:8px;font-size:.94rem;color:#D9C8D4}
.faq .note{font-size:.78rem;color:#9b86a0;margin-top:20px}
table{border-collapse:collapse;width:100%;font-size:.9rem}
th{background:var(--plum);color:#fff;text-align:left;padding:8px 10px}
td{border:1px solid var(--line);padding:8px 10px;vertical-align:top}
tr:nth-child(even) td{background:#F7F0EA}
footer{padding:26px 0;font-size:.8rem;color:#8a7a70;border-top:1px solid var(--line);margin-top:30px}
.crumb{font-size:.75rem;letter-spacing:.06em;text-transform:uppercase;color:#8a7a70;margin-bottom:10px}
.crumb a{color:#8a7a70}
@media(max-width:540px){.hero-grid{grid-template-columns:104px 1fr;gap:16px}.card{grid-template-columns:66px 1fr;gap:13px}body{font-size:17px}}
"""

def page(title, desc, body, canonical, jsonld=None, depth=1):
    pre = "../" * depth
    ld = f'<script type="application/ld+json">{json.dumps(jsonld)}</script>' if jsonld else ""
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
{ld}
<link rel="stylesheet" href="{pre}style.css">
</head><body>
<header class="site-head"><div class="wrap">
<a class="logo" href="{pre}index.html">Drama<em>EverAfter</em></a>
<span class="tag">Find your next ever after.</span>
</div></header>
{body}
<footer><div class="wrap">DramaEverAfter · Find your next ever after. · Some links are referral links; they cost you nothing and keep this database free.</div></footer>
</body></html>"""

def watch_buttons(title_id, pre=""):
    out = []
    for a in avail_by_title.get(title_id, []):
        pl = platforms.get(a["platform_id"], {})
        link = a["direct_link"] or "#AFFILIATE-LINK-PENDING"
        out.append(f'<a class="watch" href="{link}">Watch on {pl.get("name","?")}</a>')
    if not out:
        out.append('<span class="watch pending">Platform being verified</span>')
    return "".join(out)

def title_card(t, role_html="", depth=1):
    pre = "../" * depth
    trope_html = "".join(f'<a class="trope" href="{pre}tropes/{slug(tr)}.html">{tr}</a>' for tr in tropes_of(t))
    yr = f'{t["year"]} · ' if t["year"] else ""
    return f"""<article class="card">
<div class="poster"><span>poster 9:16</span></div>
<div>{role_html}
<h3><a href="{pre}titles/{tslug(t)}.html">{t['primary_title']}</a></h3>
<p class="meta">{yr}{t['genres'].replace(';', ',').title()}</p>
<div class="tropes">{trope_html}</div>
{watch_buttons(t['title_id'])}
</div></article>"""

# --------- build ---------
# Selective clean: remove ONLY generated artifacts, never data/ or generator/
for d in ["actors", "titles", "tropes", "where-to-watch"]:
    p = os.path.join(DIST, d)
    if os.path.exists(p): shutil.rmtree(p)
for f in ["index.html", "platforms.html", "robots.txt", "sitemap.xml", "style.css"]:
    p = os.path.join(DIST, f)
    if os.path.exists(p): os.remove(p)
for d in ["", "actors", "titles", "tropes"]:
    os.makedirs(os.path.join(DIST, d), exist_ok=True)
open(os.path.join(DIST, "style.css"), "w").write(CSS)
urls = []

# Actor pages
for p in people:
    sl = pslug(p)
    my_credits = credits_by_person.get(p["person_id"], [])
    my_titles = [(c, t_by_id[c["title_id"]]) for c in my_credits if c["title_id"] in t_by_id]
    verified_n = len(my_titles)
    cards = ""
    for c, t in my_titles:
        role = c["role"].replace("+", "·").title()
        chr_ = f" · {c['character_name']}" if c["character_name"] else ""
        cards += title_card(t, f'<span class="role-tag">{role}{chr_}</span>')
    plats = sorted({platforms[a["platform_id"]]["name"] for c, t in my_titles for a in avail_by_title.get(t["title_id"], [])})
    plat_line = ", ".join(plats) if plats else "platform verification in progress"
    known = my_titles[0][1]["primary_title"] if my_titles else "vertical dramas"
    ld = {"@context": "https://schema.org", "@type": "Person", "name": p["name"], "jobTitle": "Actor",
          "description": p["bio_short"][:160],
          "performerIn": [{"@type": "TVSeries", "name": t["primary_title"]} for _, t in my_titles]}
    body = f"""
<section class="hero"><div class="wrap hero-grid">
<div class="frame">{f'<img src="{p["photo_ref"]}" alt="{p["name"]}" loading="lazy" style="width:100%;height:100%;object-fit:cover;border-radius:inherit">' if p.get('photo_ref','').startswith('http') else '<div class="ph">portrait 9:16</div>'}</div>
<div><p class="eyebrow">Vertical Drama Actor</p><h1>{p['name']}</h1>
<p class="lede">Known for <strong>{known}</strong>.{f' <a href="{p["socials"]}" rel="nofollow noopener" target="_blank">IMDb profile</a>' if p.get('socials','').startswith('https://www.imdb.com') else ''}</p>
<div class="stat-row"><div class="stat"><span class="n">{verified_n}</span><span class="l">Titles verified</span></div>
<div class="stat"><span class="n">{len(plats) or '?'}</span><span class="l">Platforms</span></div></div>
</div></div></section>
<section><div class="wrap"><p class="crumb"><a href="../index.html">Home</a> / Actors / {p['name']}</p>
<p>{p['bio_short']}</p></div></section>
<section><div class="wrap"><h2>Every {p['name']} vertical drama</h2>
<p class="updated">Updated {UPDATED} · {verified_n} titles verified so far, more added weekly</p>
{cards}</div></section>
<section class="faq"><div class="wrap"><h2>{p['name']}: quick answers</h2>
<details><summary>What is {p['name']} best known for?</summary><p>{p['bio_short'].split('.')[0]}.</p></details>
<details><summary>What apps are {p['name']} dramas on?</summary><p>Verified so far: {plat_line}. Each title above links to where it streams.</p></details>
<p class="note">Spot a missing title? This database grows weekly from fan reports.</p>
</div></section>"""
    html = page(f"{p['name']} Vertical Dramas: Complete List & Where to Watch (2026) | DramaEverAfter",
                f"Every vertical drama {p['name']} has starred in, with platforms and where to watch. Updated {UPDATED}.",
                body, f"{DOMAIN}/actors/{sl}.html", ld)
    open(os.path.join(DIST, "actors", f"{sl}.html"), "w").write(html)
    urls.append(f"/actors/{sl}.html")

# Title pages
for t in titles:
    sl = tslug(t)
    cast = ""
    for c in credits_by_title.get(t["title_id"], []):
        pr = p_by_id.get(c["person_id"])
        if pr:
            cast += f'<li><a href="../actors/{pslug(pr)}.html">{pr["name"]}</a> ({c["role"]})</li>'
    trope_html = "".join(f'<a class="trope" href="../tropes/{slug(tr)}.html">{tr}</a>' for tr in tropes_of(t))
    ld = {"@context": "https://schema.org", "@type": "TVSeries", "name": t["primary_title"],
          "description": t["synopsis_short"][:160]}
    yr = f'{t["year"]} · ' if t["year"] else ""
    body = f"""
<section class="hero"><div class="wrap hero-grid">
<div class="frame"><div class="ph">poster 9:16</div></div>
<div><p class="eyebrow">Vertical Drama{' · community reported, verification pending' if t.get('data_confidence')=='needs_check' else ''}</p><h1>{t['primary_title']}</h1>
<p class="lede">{yr}{t['genres'].replace(';', ',').title()} · {t['status'].title()}</p>
<div class="tropes" style="margin-top:12px">{trope_html}</div>
</div></div></section>
<section><div class="wrap"><p class="crumb"><a href="../index.html">Home</a> / Titles / {t['primary_title']}</p>
{f"<p class=\"updated\">Also known as: {t['alt_titles'].replace(';', ', ')}</p>" if t.get('alt_titles') else ''}
<p>{t['synopsis_short']}</p>
<h2 style="margin-top:20px">Where to watch</h2>
<p class="updated">Checked {UPDATED}</p>
{watch_buttons(t['title_id'])}
{'<h2 style="margin-top:20px">Cast</h2><ul style="padding-left:20px">' + cast + '</ul>' if cast else ''}
</div></section>"""
    html = page(f"Where to Watch {t['primary_title']} (2026) | DramaEverAfter",
                f"{t['primary_title']}: where to watch, cast and tropes. Updated {UPDATED}.",
                body, f"{DOMAIN}/titles/{sl}.html", ld)
    open(os.path.join(DIST, "titles", f"{sl}.html"), "w").write(html)
    urls.append(f"/titles/{sl}.html")

# Trope pages
for tr in all_tropes:
    sl = slug(tr)
    matching = [t for t in titles if tr in tropes_of(t)]
    cards = "".join(title_card(t) for t in matching)
    body = f"""
<section class="hero"><div class="wrap">
<p class="eyebrow">Trope</p><h1>Best {tr.title()} Vertical Dramas</h1>
<p class="lede">{len(matching)} verified titles and counting. Updated {UPDATED}.</p>
</div></section>
<section><div class="wrap"><p class="crumb"><a href="../index.html">Home</a> / Tropes / {tr.title()}</p>
{cards}</div></section>"""
    html = page(f"Best {tr.title()} Vertical Dramas (2026) | DramaEverAfter",
                f"Every verified {tr} vertical drama across ReelShort, DramaBox and more. Updated {UPDATED}.",
                body, f"{DOMAIN}/tropes/{sl}.html")
    open(os.path.join(DIST, "tropes", f"{sl}.html"), "w").write(html)
    urls.append(f"/tropes/{sl}.html")


# Where-to-watch pages (money keywords: "where to watch X", "is X on reelshort or dramabox")
os.makedirs(os.path.join(DIST, "where-to-watch"), exist_ok=True)
for t in titles:
    sl = tslug(t)
    avails = avail_by_title.get(t["title_id"], [])
    plat_names = [platforms[a["platform_id"]]["name"] for a in avails if a["platform_id"] in platforms]
    answer = (f"{t['primary_title']} streams on {', '.join(plat_names)}." if plat_names
              else f"{t['primary_title']} is in our database and platform verification is in progress.")
    free_line = ""
    for a in avails:
        if a.get("free_episode_count"):
            free_line += f"<p>{platforms[a['platform_id']]['name']}: first {a['free_episode_count']} episodes free.</p>"
    faq_items = f"""<details open><summary>Where can I watch {t['primary_title']}?</summary><p>{answer}</p></details>
<details><summary>Is {t['primary_title']} free?</summary><p>{'See free episode counts above. ' if free_line else ''}Most vertical drama apps unlock early episodes free, then charge coins or a subscription for the rest.</p></details>"""
    body = f"""
<section class="hero"><div class="wrap">
<p class="eyebrow">Where to Watch</p><h1>Where to Watch {t['primary_title']}</h1>
<p class="lede">Checked {UPDATED}</p></div></section>
<section><div class="wrap"><p class="crumb"><a href="../index.html">Home</a> / Where to Watch / {t['primary_title']}</p>
<p>{answer}</p>{free_line}
{watch_buttons(t['title_id'])}
<p style="margin-top:16px"><a href="../titles/{sl}.html">Full {t['primary_title']} page: cast, tropes and details &rarr;</a></p>
</div></section>
<section class="faq"><div class="wrap"><h2>Quick answers</h2>{faq_items}
<p class="note">Spotted it on another app? Report it and help the database grow.</p></div></section>"""
    html = page(f"Where to Watch {t['primary_title']}: All Platforms (2026) | DramaEverAfter",
                f"Where to watch {t['primary_title']}: every platform it streams on, checked {UPDATED}.",
                body, f"{DOMAIN}/where-to-watch/{sl}.html")
    open(os.path.join(DIST, "where-to-watch", f"{sl}.html"), "w").write(html)
    urls.append(f"/where-to-watch/{sl}.html")

# Trope x platform combination pages (publish only at 5+ verified titles, per architecture doc)
for tr in all_tropes:
    for pid, pl in platforms.items():
        matching = [t for t in titles
                    if tr in tropes_of(t)
                    and any(a["platform_id"] == pid for a in avail_by_title.get(t["title_id"], []))
                    and t.get("data_confidence", "verified") == "verified"]
        if len(matching) < 5:
            continue
        trs, pls = slug(tr), slug(pl["name"])
        os.makedirs(os.path.join(DIST, "tropes", trs), exist_ok=True)
        cards = "".join(title_card(t, depth=2) for t in matching)
        body = f"""
<section class="hero"><div class="wrap">
<p class="eyebrow">Trope x Platform</p><h1>Best {tr.title()} Dramas on {pl['name']}</h1>
<p class="lede">{len(matching)} verified titles. Updated {UPDATED}.</p></div></section>
<section><div class="wrap"><p class="crumb"><a href="../../index.html">Home</a> / <a href="../{trs}.html">{tr.title()}</a> / {pl['name']}</p>
{cards}</div></section>"""
        html = page(f"Best {tr.title()} Vertical Dramas on {pl['name']} (2026) | DramaEverAfter",
                    f"Every verified {tr} vertical drama on {pl['name']}. Updated {UPDATED}.",
                    body, f"{DOMAIN}/tropes/{trs}/{pls}.html", depth=2)
        open(os.path.join(DIST, "tropes", trs, f"{pls}.html"), "w").write(html)
        urls.append(f"/tropes/{trs}/{pls}.html")

# Platforms page
prows = ""
for p in platforms.values():
    aff = "Yes" if p["affiliate_program"].upper().startswith("YES") else "TBC"
    prows += f"<tr><td><b>{p['name']}</b></td><td>{p['pricing_model']}</td><td>{aff}</td></tr>"
body = f"""
<section class="hero"><div class="wrap"><p class="eyebrow">Guide</p><h1>Every Vertical Drama App</h1>
<p class="lede">The platforms, compared. Updated {UPDATED}.</p></div></section>
<section><div class="wrap"><p class="crumb"><a href="index.html">Home</a> / Platforms</p>
<table><tr><th>Platform</th><th>Pricing</th><th>Referral links</th></tr>{prows}</table>
</div></section>"""
html = page("Vertical Drama Apps Compared (2026) | DramaEverAfter",
            f"ReelShort, DramaBox, ShortMax and more compared: pricing and where to start. Updated {UPDATED}.",
            body, f"{DOMAIN}/platforms.html", depth=0)
open(os.path.join(DIST, "platforms.html"), "w").write(html)
urls.append("/platforms.html")

# Homepage
actor_tiles = "".join(
    f'<a class="tile" href="actors/{pslug(p)}.html"><div class="nm">{p["name"]}</div>'
    f'<div class="kf">{len(credits_by_person.get(p["person_id"],[]))} titles verified</div></a>'
    for p in people)
trope_chips = "".join(f'<a class="chip" href="tropes/{slug(tr)}.html">{tr.title()}</a>' for tr in all_tropes)
body = f"""
<section class="hero"><div class="wrap">
<p class="eyebrow">The vertical drama database</p>
<h1>Find your next ever after.</h1>
<p class="lede">Every vertical drama, every actor, every platform, one place. Cross-referenced across ReelShort, DramaBox, ShortMax, My Drama, NetShort and more.</p>
<div class="stat-row">
<div class="stat"><span class="n">{len(titles)}</span><span class="l">Titles</span></div>
<div class="stat"><span class="n">{len(people)}</span><span class="l">Actors</span></div>
<div class="stat"><span class="n">{len(platforms)}</span><span class="l">Platforms</span></div>
</div></div></section>
<section><div class="wrap"><h2>Browse by actor</h2><p class="updated">Updated {UPDATED}</p>
<div class="grid">{actor_tiles}</div></div></section>
<section><div class="wrap"><h2>Browse by trope</h2><div class="chipsrow">{trope_chips}</div></div></section>
<section><div class="wrap"><h2>The apps, compared</h2><p><a href="platforms.html">Every vertical drama platform: pricing and where to start &rarr;</a></p></div></section>"""
html = page("DramaEverAfter: Every Vertical Drama, Every Platform, One Place",
            "The searchable database of vertical dramas and micro dramas: actors, tropes, and where to watch across ReelShort, DramaBox, ShortMax and more.",
            body, f"{DOMAIN}/", depth=0)
open(os.path.join(DIST, "index.html"), "w").write(html)
urls.insert(0, "/")

# sitemap + robots
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
sm += "".join(f"<url><loc>{DOMAIN}{u}</loc></url>\n" for u in urls) + "</urlset>"
open(os.path.join(DIST, "sitemap.xml"), "w").write(sm)
open(os.path.join(DIST, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n")

print(f"Built {len(urls)} pages -> dist/")
