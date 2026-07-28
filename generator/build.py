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

# Origin routing. ROOT_ORIGIN is the established section and stays at the root paths
# (/titles/, /where-to-watch/) so no existing URL ever moves. Any other origin gets
# its own namespace one level deeper (e.g. /chinese/titles/). See adapters.md sec 11.
# Renamed western -> english 2026-07-28 at Cyan's call. This is a display/routing
# value only, never a slug, so the rename moves zero URLs.
ROOT_ORIGIN = "english"
def origin_of(t): return (t.get("origin") or ROOT_ORIGIN).strip().lower() or ROOT_ORIGIN
def tdir(t):
    o = origin_of(t)
    return "" if o == ROOT_ORIGIN else o + "/"
def tdepth(t): return 1 if origin_of(t) == ROOT_ORIGIN else 2

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

# Root sections (home, tropes, platforms, trope+platform pages) cover ROOT_ORIGIN only.
# Other origins are browsed from their own section index.
titles_root = [t for t in titles if origin_of(t) == ROOT_ORIGIN]
titles_other = [t for t in titles if origin_of(t) != ROOT_ORIGIN]
origins_other = sorted({origin_of(t) for t in titles_other})

all_tropes = sorted({tr for t in titles_root for tr in tropes_of(t)})
all_tropes_set = set(all_tropes)
# --- Popularity + artwork helpers -------------------------------------------
# Artwork is ~5% populated. Every card falls back to a lettered placeholder so a
# missing image reads as a design choice, not a broken page. Swap in licensed art
# later by filling poster_ref / photo_ref; no template change needed.
def view_num(s):
    s = (s or "").strip().upper().replace(",", "")
    if not s: return 0
    mult = 1
    if s.endswith("B"): mult, s = 1000000000, s[:-1]
    elif s.endswith("M"): mult, s = 1000000, s[:-1]
    elif s.endswith("K"): mult, s = 1000, s[:-1]
    try: return int(float(s) * mult)
    except ValueError: return 0

def title_views(t):
    return max((view_num(a.get("view_count")) for a in avail_by_title.get(t["title_id"], [])), default=0)

def views_label(n):
    if n >= 1000000000: return "%.1fB views" % (n / 1000000000.0)
    if n >= 1000000: return "%.0fM views" % (n / 1000000.0)
    if n >= 1000: return "%.0fK views" % (n / 1000.0)
    return ""

def esc_attr(s):
    return (s or "").replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")

def art_block(img, letter, badge=""):
    if img:
        inner = '<img src="%s" alt="" loading="lazy">' % esc_attr(img)
    else:
        inner = '<span class="ph">%s</span>' % (letter or "?")
    b = '<span class="badge">%s</span>' % badge if badge else ""
    return '<span class="art">%s%s</span>' % (inner, b)

def title_card_art(t, pre=""):
    name = t["primary_title"]
    return ('<a class="card" href="%s%stitles/%s.html">%s<span class="t">%s</span><span class="s">%s</span></a>'
            % (pre, tdir(t), tslug(t), art_block((t.get("poster_ref") or "").strip(),
               name[:1].upper(), views_label(title_views(t))), name, t.get("year", "") or ""))

def person_card_art(p, pre=""):
    n = len(credits_by_person.get(p["person_id"], []))
    return ('<a class="card person" href="%sactors/%s.html">%s<span class="t">%s</span><span class="s">%s titles</span></a>'
            % (pre, pslug(p), art_block((p.get("photo_ref") or "").strip(), p["name"][:1].upper()), p["name"], n))

def rail(cards):
    return '<div class="rail">%s</div>' % "".join(cards)


def trope_chip(tr, pre):
    """Link only if a trope page exists; otherwise render inert so we never emit a 404."""
    if tr in all_tropes_set:
        return f'<a class="trope" href="{pre}tropes/{slug(tr)}.html">{tr}</a>'
    return f'<span class="trope">{tr}</span>'

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
.searchbar{display:flex;flex-wrap:wrap;gap:10px;margin:18px 0}
.searchbar input[type=text]{flex:1 1 240px;padding:11px 14px;border:1.5px solid var(--line);border-radius:10px;font-size:1rem;font-family:inherit;background:#fff;color:var(--ink)}
.searchbar select{padding:11px 12px;border:1.5px solid var(--line);border-radius:10px;font-size:1rem;font-family:inherit;background:#fff;color:var(--ink)}
.result-count{font-size:.82rem;color:#7d6e64;margin:4px 0 14px}
.hero-search{display:flex;flex-wrap:wrap;gap:8px;margin-top:20px;background:#fff;padding:8px;border-radius:12px;box-shadow:0 6px 18px rgba(43,27,46,.12)}
.hero-search input[type=text]{flex:1 1 260px;padding:13px 16px;border:none;border-radius:8px;font-size:1.05rem;font-family:inherit}
.hero-search button{background:var(--gold);color:#241a05;border:none;font-weight:700;border-radius:8px;padding:0 20px;cursor:pointer;font-size:.95rem}
.seeall{font-size:.85rem;margin-top:10px;display:inline-block}
.wrap-wide{max-width:1180px;margin:0 auto;padding:0 20px}
.hero-art{height:190px;border-radius:16px;margin-bottom:22px;border:1px solid var(--line);background:linear-gradient(120deg,var(--blush) 0%,#fff 45%,var(--gold) 140%);display:flex;align-items:center;justify-content:center;position:relative;overflow:hidden}
.hero-art .wordmark{font-family:'Fraunces',Georgia,serif;font-size:2.1rem;font-weight:700;color:var(--plum);opacity:.5;letter-spacing:.02em}
.row-head{display:flex;justify-content:space-between;align-items:baseline;gap:12px;flex-wrap:wrap;margin-bottom:2px}
.row-head a{font-size:.8rem;text-decoration:none;white-space:nowrap}
.rail{display:flex;gap:14px;overflow-x:auto;scroll-snap-type:x proximity;padding:10px 0 14px;scrollbar-width:thin}
.rail::-webkit-scrollbar{height:8px}
.rail::-webkit-scrollbar-thumb{background:var(--line);border-radius:4px}
.card{flex:0 0 146px;scroll-snap-align:start;text-decoration:none;color:var(--ink);display:block}
.card .art{aspect-ratio:2/3;border-radius:12px;overflow:hidden;border:1px solid var(--line);background:linear-gradient(155deg,var(--blush),#fff 55%,var(--line));display:flex;align-items:center;justify-content:center;position:relative}
.card .art img{width:100%;height:100%;object-fit:cover;display:block}
.card .art .ph{font-family:'Fraunces',Georgia,serif;font-size:2.7rem;font-weight:700;color:var(--wine);opacity:.32}
.card .art .badge{position:absolute;left:6px;bottom:6px;background:rgba(43,27,46,.84);color:#fff;font-size:.66rem;padding:2px 8px;border-radius:20px}
.card .t{display:block;font-family:'Fraunces',Georgia,serif;font-size:.85rem;font-weight:700;color:var(--plum);margin-top:8px;line-height:1.25}
.card .s{display:block;font-size:.73rem;color:#7d6e64;margin-top:2px}
.card:hover .art{border-color:var(--wine)}
.card.person{flex:0 0 118px}
.card.person .art{aspect-ratio:1/1;border-radius:50%}
.card.person .t,.card.person .s{text-align:center}
.stub{border:1.5px dashed var(--line);border-radius:14px;padding:26px 20px;text-align:center;color:#7d6e64;font-size:.9rem;background:#fff}
.stub strong{display:block;font-family:'Fraunces',Georgia,serif;color:var(--plum);font-size:1.05rem;margin-bottom:4px}
.facetbar{margin:14px 0 4px}
.facetgroup{margin-bottom:10px}
.facetgroup h3{font-size:.74rem;letter-spacing:.09em;text-transform:uppercase;color:#7d6e64;font-family:'Atkinson Hyperlegible',Georgia,serif;font-weight:700;margin-bottom:7px}
.facets{display:flex;flex-wrap:wrap;gap:7px}
.facet{background:#fff;border:1.5px solid var(--line);border-radius:20px;padding:6px 12px;font-size:.82rem;font-family:inherit;color:var(--ink);cursor:pointer;display:inline-flex;align-items:center;gap:6px;line-height:1.2}
.facet .c{font-size:.68rem;color:#9b8b80;font-variant-numeric:tabular-nums}
.facet:hover:not(.off){border-color:var(--wine);color:var(--wine)}
.facet.on{background:var(--wine);border-color:var(--wine);color:#fff}
.facet.on .c{color:rgba(255,255,255,.75)}
.facet.off{opacity:.32;cursor:default}
.facet-reset{background:none;border:none;color:var(--wine);font-family:inherit;font-size:.8rem;cursor:pointer;text-decoration:underline;padding:6px 2px}
.facet-more{background:none;border:none;color:var(--wine);font-family:inherit;font-size:.78rem;cursor:pointer;text-decoration:underline;padding:6px 2px}
.facets.collapsed .extra{display:none}
.resultgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(132px,1fr));gap:16px}
.resultgrid .card{flex:none;width:auto}
.hero-banner{position:relative;margin:-1px 0 10px}
.hero-media{position:relative;min-height:460px;display:flex;align-items:center;justify-content:center;overflow:hidden;background:linear-gradient(135deg,#2B1B2E 0%,#7A2B4A 58%,#C9962E 145%)}
.hero-media img.hero-img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.hero-ph{position:relative;z-index:1;color:rgba(255,255,255,.5);font-family:'Fraunces',Georgia,serif;font-size:.82rem;letter-spacing:.2em;text-transform:uppercase;border:1.5px dashed rgba(255,255,255,.34);padding:13px 24px;border-radius:10px}
.hero-scrim{position:absolute;inset:0;z-index:2;background:linear-gradient(90deg,rgba(18,10,20,.9) 0%,rgba(18,10,20,.66) 48%,rgba(18,10,20,.15) 100%)}
.hero-copy{position:absolute;inset:0;z-index:3;display:flex;flex-direction:column;justify-content:center}
.hero-copy .inner{max-width:1180px;width:100%;margin:0 auto;padding:0 24px}
.hero-copy .eyebrow{color:var(--gold);margin-bottom:6px}
.hero-copy h1{color:#fff;font-size:clamp(2rem,5.2vw,3.5rem);max-width:15ch;margin-bottom:10px}
.hero-copy .lede{color:rgba(255,255,255,.88);max-width:46ch;font-size:1rem;margin-bottom:16px}
.hero-copy .hero-search{max-width:560px;margin-top:0;box-shadow:0 10px 30px rgba(0,0,0,.34)}
.hero-stats{display:flex;gap:26px;margin-top:18px;flex-wrap:wrap}
.hero-stats .n{display:block;font-family:'Fraunces',Georgia,serif;font-size:1.5rem;font-weight:700;color:#fff;line-height:1}
.hero-stats .l{display:block;font-size:.72rem;letter-spacing:.11em;text-transform:uppercase;color:rgba(255,255,255,.66);margin-top:3px}
@media(max-width:640px){.hero-media{min-height:400px}.hero-scrim{background:linear-gradient(180deg,rgba(18,10,20,.55) 0%,rgba(18,10,20,.9) 62%)}.hero-copy{justify-content:flex-end;padding-bottom:26px}}
.rail-stub{flex:0 0 100%;border:1.5px dashed var(--line);border-radius:14px;padding:26px 20px;text-align:center;color:#7d6e64;font-size:.88rem;background:#fff}
.rail-stub strong{display:block;font-family:'Fraunces',Georgia,serif;color:var(--plum);font-size:1rem;margin-bottom:4px}
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

def title_card(t, role_html="", depth=1, title_pre=None):
    pre = "../" * depth
    tp = pre if title_pre is None else title_pre
    trope_html = "".join(trope_chip(tr, pre) for tr in tropes_of(t))
    yr = f'{t["year"]} · ' if t["year"] else ""
    return f"""<article class="card">
<div class="poster"><span>poster 9:16</span></div>
<div>{role_html}
<h3><a href="{tp}titles/{tslug(t)}.html">{t['primary_title']}</a></h3>
<p class="meta">{yr}{t['genres'].replace(';', ',').title()}</p>
<div class="tropes">{trope_html}</div>
{watch_buttons(t['title_id'])}
</div></article>"""

# --------- build ---------
# Selective clean: remove ONLY generated artifacts, never data/ or generator/
for d in ["actors", "titles", "tropes", "where-to-watch"] + origins_other:
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
    d, pre = tdir(t), "../" * tdepth(t)
    cast = ""
    for c in credits_by_title.get(t["title_id"], []):
        pr = p_by_id.get(c["person_id"])
        if pr:
            cast += f'<li><a href="{pre}actors/{pslug(pr)}.html">{pr["name"]}</a> ({c["role"]})</li>'
    trope_html = "".join(trope_chip(tr, pre) for tr in tropes_of(t))
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
<section><div class="wrap"><p class="crumb"><a href="{pre}index.html">Home</a> / {'' if not d else f'<a href="../index.html">{origin_of(t).title()}</a> / '}Titles / {t['primary_title']}</p>
{f"<p class=\"updated\">Also known as: {t['alt_titles'].replace(';', ', ')}</p>" if t.get('alt_titles') else ''}
<p>{t['synopsis_short']}</p>
<h2 style="margin-top:20px">Where to watch</h2>
<p class="updated">Checked {UPDATED}</p>
{watch_buttons(t['title_id'])}
{'<h2 style="margin-top:20px">Cast</h2><ul style="padding-left:20px">' + cast + '</ul>' if cast else ''}
</div></section>"""
    html = page(f"Where to Watch {t['primary_title']} (2026) | DramaEverAfter",
                f"{t['primary_title']}: where to watch, cast and tropes. Updated {UPDATED}.",
                body, f"{DOMAIN}/{d}titles/{sl}.html", ld, depth=tdepth(t))
    os.makedirs(os.path.join(DIST, d, "titles"), exist_ok=True)
    open(os.path.join(DIST, d, "titles", f"{sl}.html"), "w").write(html)
    urls.append(f"/{d}titles/{sl}.html")

# Trope pages
for tr in all_tropes:
    sl = slug(tr)
    matching = [t for t in titles_root if tr in tropes_of(t)]
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
    d, pre = tdir(t), "../" * tdepth(t)
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
<section><div class="wrap"><p class="crumb"><a href="{pre}index.html">Home</a> / {'' if not d else f'<a href="../index.html">{origin_of(t).title()}</a> / '}Where to Watch / {t['primary_title']}</p>
<p>{answer}</p>{free_line}
{watch_buttons(t['title_id'])}
<p style="margin-top:16px"><a href="../titles/{sl}.html">Full {t['primary_title']} page: cast, tropes and details &rarr;</a></p>
</div></section>
<section class="faq"><div class="wrap"><h2>Quick answers</h2>{faq_items}
<p class="note">Spotted it on another app? Report it and help the database grow.</p></div></section>"""
    html = page(f"Where to Watch {t['primary_title']}: All Platforms (2026) | DramaEverAfter",
                f"Where to watch {t['primary_title']}: every platform it streams on, checked {UPDATED}.",
                body, f"{DOMAIN}/{d}where-to-watch/{sl}.html", depth=tdepth(t))
    os.makedirs(os.path.join(DIST, d, "where-to-watch"), exist_ok=True)
    open(os.path.join(DIST, d, "where-to-watch", f"{sl}.html"), "w").write(html)
    urls.append(f"/{d}where-to-watch/{sl}.html")

# Trope x platform combination pages (publish only at 5+ verified titles, per architecture doc)
for tr in all_tropes:
    for pid, pl in platforms.items():
        matching = [t for t in titles_root
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

# Search index + browse page (client-side search/filter, no backend needed).
# Facets are stored as slugs so the chip value and the title tag always match, and
# so both spellings of a trope (e.g. "Age Gap" / "Age-Gap") collapse to one chip.
search_actors = [{"n": p["name"], "s": pslug(p),
                  "c": len(credits_by_person.get(p["person_id"], [])),
                  "i": (p.get("photo_ref") or "").strip()} for p in people]

trope_counts = defaultdict(int)
platform_counts = defaultdict(int)
trope_label = {}
platform_label = {}

search_titles = []
for t in titles_root:
    tr_slugs = sorted({slug(x) for x in tropes_of(t) if slug(x)})
    for x in tropes_of(t):
        if slug(x): trope_label.setdefault(slug(x), x.title())
    pl_slugs = sorted({slug(platforms[a["platform_id"]]["name"])
                       for a in avail_by_title.get(t["title_id"], []) if a["platform_id"] in platforms})
    for a in avail_by_title.get(t["title_id"], []):
        if a["platform_id"] in platforms:
            platform_label.setdefault(slug(platforms[a["platform_id"]]["name"]), platforms[a["platform_id"]]["name"])
    for s in tr_slugs: trope_counts[s] += 1
    for s in pl_slugs: platform_counts[s] += 1
    entry = {"n": t["primary_title"], "s": tslug(t)}
    if t.get("year"): entry["y"] = t["year"]
    if tr_slugs: entry["tr"] = tr_slugs
    if pl_slugs: entry["pl"] = pl_slugs
    entry["o"] = [origin_of(t)]
    v = title_views(t)
    if v: entry["v"] = v
    img = (t.get("poster_ref") or "").strip()
    if img: entry["i"] = img
    search_titles.append(entry)

open(os.path.join(DIST, "search-index.json"), "w").write(
    json.dumps({"actors": search_actors, "titles": search_titles}, separators=(",", ":")))

VISIBLE = 40  # chips shown before "show all"

def facet_chips(group, counts, labels):
    out = []
    ordered = sorted(counts.items(), key=lambda kv: (-kv[1], labels.get(kv[0], kv[0])))
    for i, (s, _n) in enumerate(ordered):
        extra = " extra" if i >= VISIBLE else ""
        out.append('<button class="facet%s" data-g="%s" data-v="%s" type="button">%s<span class="c"></span></button>'
                   % (extra, group, s, labels.get(s, s)))
    return "".join(out), len(ordered)

# Origin facet. Buckets Cyan wants exposed are declared up front, not derived from the
# data, so the filter shows the full shape of the taxonomy even while a bucket is empty.
# An empty bucket renders greyed out and disabled, same as any other zero-match chip.
ORIGIN_BUCKETS = [("english", "English"), ("chinese", "Chinese"), ("dubbed", "Dubbed")]
origin_counts = defaultdict(int)
for t in titles_root: origin_counts[origin_of(t)] += 1
origin_facets = "".join(
    '<button class="facet" data-g="origin" data-v="%s" type="button">%s<span class="c"></span></button>' % (v, lbl)
    for v, lbl in ORIGIN_BUCKETS)

trope_facets, n_tropes = facet_chips("trope", trope_counts, trope_label)
platform_facets, n_platforms = facet_chips("platform", platform_counts, platform_label)
trope_more = ('<button class="facet-more" data-target="f-trope" type="button">Show all %d tropes</button>' % n_tropes) if n_tropes > VISIBLE else ""
platform_more = ('<button class="facet-more" data-target="f-platform" type="button">Show all %d apps</button>' % n_platforms) if n_platforms > VISIBLE else ""

BROWSE_JS = """
<script>
(function(){
  var D=null, CAP=60;
  var FIELD={trope:'tr', platform:'pl', origin:'o'};
  var active={};
  var qEl=document.getElementById('q'), sortEl=document.getElementById('f-sort');
  var titlesOut=document.getElementById('results-titles'), actorsOut=document.getElementById('results-actors');
  var countEl=document.getElementById('result-count'), resetEl=document.getElementById('f-reset');
  var chips=[].slice.call(document.querySelectorAll('.facet'));
  chips.forEach(function(c){ if(!active[c.dataset.g]) active[c.dataset.g]=new Set(); });

  function esc(s){return String(s==null?'':s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/"/g,'&quot;');}
  function has(arr,v){return arr && arr.indexOf(v)!==-1;}
  function vlabel(n){
    if(!n) return '';
    if(n>=1e9) return (n/1e9).toFixed(1)+'B views';
    if(n>=1e6) return Math.round(n/1e6)+'M views';
    if(n>=1e3) return Math.round(n/1e3)+'K views';
    return '';
  }
  function art(img,letter,badge){
    var inner = img ? '<img src="'+esc(img)+'" alt="" loading="lazy">' : '<span class="ph">'+esc(letter||'?')+'</span>';
    return '<span class="art">'+inner+(badge?'<span class="badge">'+esc(badge)+'</span>':'')+'</span>';
  }

  function matches(t,q){
    if(q && t.n.toLowerCase().indexOf(q)===-1) return false;
    for(var g in active){
      var f=t[FIELD[g]], it=active[g].values(), x;
      while(!(x=it.next()).done){ if(!has(f,x.value)) return false; }
    }
    return true;
  }

  function run(){
    if(!D) return;
    var q=qEl.value.trim().toLowerCase();
    var titles=D.titles.filter(function(t){return matches(t,q);});

    // Single pass over the current result set tallies every facet at once, so each
    // chip's number is "results you'd get if you also picked this".
    var tally={}; for(var g in active) tally[g]={};
    for(var i=0;i<titles.length;i++){
      var t=titles[i];
      for(var g2 in active){
        var f=t[FIELD[g2]]; if(!f) continue;
        for(var j=0;j<f.length;j++) tally[g2][f[j]]=(tally[g2][f[j]]||0)+1;
      }
    }
    for(var c=0;c<chips.length;c++){
      var el=chips[c], g=el.dataset.g, v=el.dataset.v, n=tally[g][v]||0, on=active[g].has(v);
      el.querySelector('.c').textContent=n;
      el.className=(el.className.indexOf('extra')!==-1?'facet extra':'facet')+(on?' on':(n?'':' off'));
      el.disabled=(!n && !on);
    }

    var sort=sortEl.value;
    if(sort==='views') titles.sort(function(a,b){return (b.v||0)-(a.v||0);});
    else if(sort==='az') titles.sort(function(a,b){return a.n.localeCompare(b.n);});
    else if(sort==='year') titles.sort(function(a,b){return String(b.y||'').localeCompare(String(a.y||''));});

    var actors=D.actors.filter(function(a){return !q || a.n.toLowerCase().indexOf(q)!==-1;});
    actors.sort(function(a,b){return b.c-a.c;});

    var nf=0; for(var g3 in active) nf+=active[g3].size;
    resetEl.style.display=(nf||q)?'inline-block':'none';
    countEl.textContent=titles.length.toLocaleString()+' titles'+(q?', '+actors.length.toLocaleString()+' actors':'')+(nf?' · '+nf+' filter'+(nf>1?'s':'')+' on':'');

    titlesOut.innerHTML=titles.slice(0,CAP).map(function(t){
      return '<a class="card" href="titles/'+esc(t.s)+'.html">'+art(t.i,t.n.charAt(0).toUpperCase(),vlabel(t.v))
        +'<span class="t">'+esc(t.n)+'</span><span class="s">'+esc(t.y||'')+'</span></a>';
    }).join('') || '<p class="updated">No titles match. Try removing a filter.</p>';
    if(titles.length>CAP) titlesOut.innerHTML+='<p class="updated">+ '+(titles.length-CAP).toLocaleString()+' more. Narrow with a filter or search.</p>';

    if(q){
      actorsOut.innerHTML=actors.slice(0,24).map(function(a){
        return '<a class="card person" href="actors/'+esc(a.s)+'.html">'+art(a.i,a.n.charAt(0).toUpperCase(),'')
          +'<span class="t">'+esc(a.n)+'</span><span class="s">'+a.c+' titles</span></a>';
      }).join('') || '<p class="updated">No actors match.</p>';
      actorsOut.parentNode.style.display='';
    } else {
      actorsOut.parentNode.style.display='none';
    }
  }

  chips.forEach(function(el){
    el.addEventListener('click',function(){
      if(el.disabled) return;
      var g=el.dataset.g,v=el.dataset.v;
      if(active[g].has(v)) active[g].delete(v); else active[g].add(v);
      run();
    });
  });
  [].slice.call(document.querySelectorAll('.facet-more')).forEach(function(b){
    b.addEventListener('click',function(){
      var box=document.getElementById(b.dataset.target);
      var collapsed=box.classList.toggle('collapsed');
      b.textContent=collapsed?b.dataset.moreLabel:'Show fewer';
    });
  });

  var timer=null;
  qEl.addEventListener('input',function(){clearTimeout(timer);timer=setTimeout(run,120);});
  sortEl.addEventListener('change',run);
  resetEl.addEventListener('click',function(){
    for(var g in active) active[g].clear(); qEl.value=''; run();
  });

  fetch('search-index.json').then(function(r){return r.json();}).then(function(d){
    D=d;
    var p=new URLSearchParams(window.location.search);
    if(p.get('q')) qEl.value=p.get('q');
    ['trope','platform','origin'].forEach(function(g){
      if(p.get(g) && active[g]) active[g].add(p.get(g));
    });
    run();
  }).catch(function(){ countEl.textContent='Could not load the index. Please refresh.'; });
})();
</script>
"""

browse_body = f"""
<section class="hero"><div class="wrap-wide">
<p class="eyebrow">Search &amp; Browse</p><h1>Find any actor or drama</h1>
<p class="lede">{len(titles_root)} titles and {len(people)} actors. Search by name, or stack filters. Greyed-out chips have no matches left.</p>
<div class="searchbar">
<input type="text" id="q" placeholder="Search titles or actors&hellip;" autocomplete="off" aria-label="Search titles or actors">
<select id="f-sort" aria-label="Sort titles">
<option value="views">Most watched</option>
<option value="az">A&ndash;Z</option>
<option value="year">Newest first</option>
</select>
</div>
<div class="facetbar">
<div class="facetgroup"><h3>Country of origin</h3><div class="facets" id="f-origin">{origin_facets}</div></div>
<div class="facetgroup"><h3>Trope</h3><div class="facets collapsed" id="f-trope">{trope_facets}</div>{trope_more}</div>
<div class="facetgroup"><h3>App</h3><div class="facets" id="f-platform">{platform_facets}</div>{platform_more}</div>
</div>
<p class="result-count" id="result-count">Loading&hellip;</p>
<button class="facet-reset" id="f-reset" type="button" style="display:none">Reset all filters</button>
</div></section>
<section><div class="wrap-wide" style="display:none"><h2>Actors</h2><div class="resultgrid" id="results-actors"></div></div></section>
<section><div class="wrap-wide"><h2>Titles</h2><div class="resultgrid" id="results-titles"></div></div></section>
{BROWSE_JS}"""
html = page("Search DramaEverAfter: Every Actor and Title (2026) | DramaEverAfter",
            f"Search and filter {len(people)} vertical drama actors and {len(titles_root)} titles by trope and platform.",
            browse_body, f"{DOMAIN}/browse.html", depth=0)
open(os.path.join(DIST, "browse.html"), "w").write(html)
urls.append("/browse.html")

# Per-origin section indexes (e.g. /chinese/index.html). Western has no section index —
# it IS the root site. Only emitted for origins that actually have titles.
ORIGIN_BLURB = {
    "chinese": ("Chinese Short Drama (Duanju)",
                "Native Chinese-language vertical dramas from Douyin, Kuaishou and the "
                "Chinese short-drama studios. Separate from the Western vertical catalogue."),
}
for o in origins_other:
    o_titles = [t for t in titles_other if origin_of(t) == o]
    heading, blurb = ORIGIN_BLURB.get(o, (o.title() + " Short Drama", ""))
    cards = "".join(title_card(t, depth=1, title_pre="") for t in o_titles)
    body = f"""
<section class="hero"><div class="wrap">
<p class="eyebrow">Section</p><h1>{heading}</h1>
<p class="lede">{blurb}</p>
<div class="stat-row"><div class="stat"><span class="n">{len(o_titles)}</span><span class="l">Titles</span></div></div>
</div></section>
<section><div class="wrap"><p class="crumb"><a href="../index.html">Home</a> / {heading}</p>
<div class="grid">{cards}</div></div></section>"""
    html = page(f"{heading} | DramaEverAfter",
                f"{heading}: titles, cast and where to watch. Updated {UPDATED}.",
                body, f"{DOMAIN}/{o}/index.html", depth=1)
    os.makedirs(os.path.join(DIST, o), exist_ok=True)
    open(os.path.join(DIST, o, "index.html"), "w").write(html)
    urls.append(f"/{o}/index.html")

# Homepage
# Row order follows how the fan community actually browses (actors, tropes, apps,
# what's new) rather than by origin. Origin rows sit below as their own sections.
top_actors = sorted(people, key=lambda p: -len(credits_by_person.get(p["person_id"], [])))[:18]
featured = sorted(titles_root, key=lambda t: -title_views(t))[:18]
just_added = sorted(titles_root, key=lambda t: (t.get("last_verified") or ""), reverse=True)[:18]

_plat_counts = defaultdict(int)
for a in availability:
    if a["platform_id"] in platforms: _plat_counts[a["platform_id"]] += 1
top_platforms = sorted(_plat_counts.items(), key=lambda kv: -kv[1])[:16]
platform_chips = "".join(
    '<a class="chip" href="browse.html?platform=%s">%s</a>' % (slug(platforms[pid]["name"]), platforms[pid]["name"])
    for pid, _ in top_platforms)

_seen_chips = set()
trope_chips = ""
for tr in all_tropes:
    _s = slug(tr)
    if _s in _seen_chips: continue
    _seen_chips.add(_s)
    trope_chips += '<a class="chip" href="tropes/%s.html">%s</a>' % (_s, tr.title())

section_links = "".join(
    '<section><div class="wrap"><h2>%s</h2><p><a href="%s/index.html">Browse the %s catalogue &rarr;</a></p></div></section>'
    % (ORIGIN_BLURB.get(o, (o.title() + " Short Drama", ""))[0], o, o)
    for o in origins_other)

# Origin sections we have committed to but have no rows for yet render as an honest
# stub rather than an empty rail.
STUB_ORIGINS = []
stub_sections = "".join(
    '<section><div class="wrap"><h2>%s</h2><div class="stub"><strong>Coming soon</strong>%s</div></div></section>' % (h, b)
    for h, b in STUB_ORIGINS if h.split()[0].lower() not in origins_other)

body = f"""
<section class="hero-banner">
<div class="hero-media">
<!-- Swap the placeholder for real art by dropping <img class="hero-img" src="..." alt=""> in here. -->
<span class="hero-ph">Hero image placeholder</span>
<div class="hero-scrim"></div>
<div class="hero-copy"><div class="inner">
<p class="eyebrow">The vertical drama database</p>
<h1>Find your next ever after.</h1>
<p class="lede">Every vertical drama, every actor, every platform, one place. Cross-referenced across ReelShort, DramaBox, ShortMax, My Drama and more.</p>
<form class="hero-search" action="browse.html" method="get">
<input type="text" name="q" placeholder="Search {len(people)} actors or {len(titles_root)} titles&hellip;" aria-label="Search actors or titles">
<button type="submit">Search</button>
</form>
<div class="hero-stats">
<div><span class="n">{len(titles_root)}</span><span class="l">Titles</span></div>
<div><span class="n">{len(people)}</span><span class="l">Actors</span></div>
<div><span class="n">{len(platforms)}</span><span class="l">Platforms</span></div>
</div>
</div></div>
</div></section>

<section><div class="wrap-wide">
<div class="row-head"><h2>Most watched</h2><a href="browse.html">Browse all &rarr;</a></div>
{rail([title_card_art(t) for t in featured])}
</div></section>

<section><div class="wrap-wide">
<div class="row-head"><h2>Popular actors</h2><a href="browse.html">All {len(people)} actors &rarr;</a></div>
{rail([person_card_art(p) for p in top_actors])}
</div></section>

<section><div class="wrap-wide">
<div class="row-head"><h2>Popular Chinese actors</h2></div>
<div class="rail"><div class="rail-stub"><strong>Coming soon</strong>No Chinese-origin titles are in the database yet, so there are no actors to rank. This strip fills itself the moment the first ones land.</div></div>
</div></section>

<section><div class="wrap"><h2>Browse by trope</h2><div class="chipsrow">{trope_chips}</div></div></section>

<section><div class="wrap"><h2>Browse by app</h2><div class="chipsrow">{platform_chips}</div>
<p><a class="seeall" href="platforms.html">Every platform compared: pricing and where to start &rarr;</a></p></div></section>

<section><div class="wrap-wide">
<div class="row-head"><h2>Just added</h2><p class="updated">Updated {UPDATED}</p></div>
{rail([title_card_art(t) for t in just_added])}
</div></section>
{section_links}{stub_sections}"""
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
