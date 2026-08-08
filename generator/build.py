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

# Cards rendered into a static listing page before we hand off to Browse. Without a
# cap, /tropes/revenge.html emitted 1,849 poster cards and weighed 1.1 MB, which is
# indefensible for a phone-first audience. Browse already does progressive reveal over
# the whole index client-side, so the overflow link points there pre-filtered.
GRID_CAP = 60
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

# Platforms ranked by verified availability rows. Computed once up front because the
# site header/footer need it on every page, not just the homepage.
_plat_counts = defaultdict(int)
for a in availability:
    if a["platform_id"] in platforms: _plat_counts[a["platform_id"]] += 1
TOP_PLATFORMS = sorted(_plat_counts.items(), key=lambda kv: -kv[1])
APPS_WITH_DATA = [platforms[pid] for pid, n in TOP_PLATFORMS if n > 0]
# Only these get an /apps/ page, so only these may be linked from a card caption.
APP_PAGE_NAMES = {p["name"] for p in APPS_WITH_DATA}

def _raw_tropes(t):
    return [x.strip() for x in t["tropes"].split(";") if x.strip()]

# Trope canonicalisation. The data holds 266 distinct trope STRINGS that collapse to
# only 226 slugs: "CEO"/"ceo", "age gap"/"age-gap" and 38 other pairs. Because the
# page filename comes from the slug, each pair wrote the same .html twice and the
# second write won, so a trope page listed only ONE variant's titles. That hid 1,945
# titles across 40 pages (/tropes/ceo.html showed 103 of 1,830).
#
# Fixing it at the source rather than per page: the most-frequent spelling becomes
# the canonical name for its slug, and tropes_of() returns canonical names deduped
# by slug. Everything downstream -- pages, chips, counts, the A-Z index, trope x
# platform pages -- then agrees by construction.
_trope_freq = defaultdict(int)
for _t in titles:
    for _x in _raw_tropes(_t): _trope_freq[_x] += 1
TROPE_CANON = {}
for _name, _n in sorted(_trope_freq.items(), key=lambda kv: (-kv[1], kv[0])):
    TROPE_CANON.setdefault(slug(_name), _name)

_tropes_cache = {}
def tropes_of(t):
    # Memoised per title. Canonicalising runs a regex per trope, and the trope x
    # platform loop calls this ~54 million times (226 tropes x 70 platforms x 3,407
    # titles); without the cache that step alone dominated the whole build.
    key = t["title_id"]
    hit = _tropes_cache.get(key)
    if hit is not None:
        return hit
    seen, out = set(), []
    for x in _raw_tropes(t):
        s = slug(x)
        if s and s not in seen:
            seen.add(s)
            out.append(TROPE_CANON.get(s, x))
    _tropes_cache[key] = out
    return out

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

# Social / profile links. The socials column holds one or more URLs separated by
# semicolons, commas or whitespace; the domain decides the label, so filling in an
# Instagram or TikTok handle later needs no template change. Unknown domains render
# under their bare hostname rather than being dropped.
SOCIAL_LABELS = [
    ("imdb.com", "IMDb"), ("instagram.com", "Instagram"), ("tiktok.com", "TikTok"),
    ("youtube.com", "YouTube"), ("youtu.be", "YouTube"), ("twitter.com", "X"),
    ("x.com", "X"), ("facebook.com", "Facebook"), ("threads.net", "Threads"),
    ("threads.com", "Threads"), ("linkedin.com", "LinkedIn"), ("backstage.com", "Backstage"),
    ("spotlight.com", "Spotlight"), ("actorsaccess.com", "Actors Access"),
]

def social_links(p):
    raw = (p.get("socials") or "").strip()
    if not raw: return ""
    out, seen = [], set()
    for u in re.split(r"[;,\s]+", raw):
        u = u.strip()
        if not u.startswith("http"): continue
        m = re.search(r"https?://(?:www\.)?([^/]+)", u)
        if not m: continue
        host = m.group(1).lower()
        label = next((lbl for dom, lbl in SOCIAL_LABELS if host.endswith(dom)), host)
        if label in seen: continue
        seen.add(label)
        out.append('<a class="chip" href="%s" rel="nofollow noopener" target="_blank">%s</a>' % (esc_attr(u), label))
    return '<div class="chips socials">%s</div>' % "".join(out) if out else ""

# --------- shared partials -----------------------------------------------
# The no-poster plate and the initials ring are designed objects, not fallbacks:
# ~25% of titles and ~94% of actors have no image, so these render on nearly
# every page and must be byte-for-byte identical wherever they appear.

def is_ai(t):
    """AI-generated titles are flagged by hand in titles.csv `ai`.

    Deliberately NOT inferred. Two signals narrow the candidates -- ReelShort stamps
    an 'Ai GENERATE' badge on the poster, and an AI title tends to have no cast on a
    platform that normally lists one -- but neither is conclusive: of the first three
    no-cast ReelShort titles checked, two carried the badge and one was plainly
    live-action. Calling a real production AI-generated is a false accusation against
    the people in it, so nothing lands here without a human confirming the poster.

    The column is tri-state, because "checked, not AI" has to be recordable:
        (blank)  never checked
        yes      confirmed AI-generated from the poster badge
        no       confirmed NOT AI by a human, do not re-queue
    Only `yes` is truthy here, so `no` renders exactly like blank. It exists so
    make_worklists.py can keep a settled title out of AI-CHECK.md; without it a
    ruling was lost and the same title came back to the top of the queue."""
    return (t.get("ai") or "").strip().lower() in ("yes", "y", "true", "1")

def is_upcoming(t):
    """Announced but not yet released. status=upcoming is the only truthy value.

    Every title in the database was a released one until Aug 2026, so every page
    could safely imply "watchable now". An upcoming title breaks that assumption,
    which is why it carries a badge and is hidden from Browse by default: someone
    searching wants something they can watch tonight. It still gets a page, so the
    title is indexable BEFORE release rather than after everyone else has covered
    it, which is the whole point of carrying one."""
    return (t.get("status") or "").strip().lower() == "upcoming"

def book_of(t):
    """Book adaptation. Returns the author name, or 'yes' when we know it is an
    adaptation but not by whom, or '' when it is not one.

    Populated two ways, neither of them a guess: 11 titles state it outright in the
    synopsis ("Based on the novel by Sarah Brianne"), and Cyan supplied the rest by
    hand. NOT inferred from platform -- CandyJar is Inkitt/Galatea and its catalogue
    is largely novel adaptations, but 'largely' is not 'all', and claiming a book
    behind a title that has none would be as wrong as the AI label."""
    return (t.get("book") or "").strip()

def poster_box(t, app_name=""):
    """Cover art, or a typographic edition when there is none. Image layers over
    the plate; if the hotlink dies, onerror removes the <img> and the plate
    (title + app name) shows through instead of a broken image."""
    img = (t.get("poster_ref") or "").strip()
    name = t["primary_title"]
    plate = (f'<span class="poster--empty"><span class="label">No poster</span>'
             f'<span class="ttl">{name}</span>'
             f'<span class="app">{app_name}</span></span>')
    img_html = (f'<img src="{esc_attr(img)}" alt="{esc_attr(name)}" loading="lazy" onerror="this.remove()">'
                if img else "")
    ai = '<span class="ai-badge" title="AI-generated">AI</span>' if is_ai(t) else ""
    # Sits left so it never collides with the AI badge; a title can be both.
    soon = '<span class="soon-badge" title="Not released yet">SOON</span>' if is_upcoming(t) else ""
    return f'<span class="poster">{plate}{img_html}{ai}{soon}</span>'

def actor_ring(name, img, size="md", on_warm=False):
    cls = "ring ring--%s%s" % (size, " on-warm" if on_warm else "")
    initials = "".join(w[0].upper() for w in name.split()[:2]) or "?"
    img = (img or "").strip()
    img_html = f'<img src="{esc_attr(img)}" alt="" loading="lazy" onerror="this.remove()">' if img else ""
    return f'<span class="{cls}"><span>{initials}</span>{img_html}</span>'

def title_app(t):
    avails = avail_by_title.get(t["title_id"], [])
    return platforms.get(avails[0]["platform_id"], {}).get("name", "") if avails else ""

def poster_card(t, pre="", rail_item=False, size_sm=False, show_app=True, note=""):
    """The one poster card used on every rail and every grid: home, browse,
    title-detail similar rail, actor credits, trope grid, app grid.
    `note` carries page-specific context (the role/character on an actor page).
    It never repeats the title, per the caption rule."""
    app_name = title_app(t)
    v = views_label(title_views(t))
    tr = tropes_of(t)
    bits = [x for x in [v, tr[0] if tr else ""] if x]
    meta = " &middot; ".join(bits)
    cls = "poster-card"
    if rail_item: cls += " rail-item" + (" sm" if size_sm else "")
    # The card is a wrapper, not one big anchor: the poster links to the title and the
    # app name links to that app's page. Anchors cannot nest, which is why the caption
    # sits outside the poster link rather than inside it.
    app_html = ""
    if show_app and app_name:
        app_html = (f'<a class="app-name" href="{pre}apps/{slug(app_name)}.html">{app_name}</a>'
                    if app_name in APP_PAGE_NAMES else f'<span class="app-name">{app_name}</span>')
    if note: app_html = f'<span class="card-note">{note}</span>' + app_html
    href = f'{pre}titles/{tslug(t)}.html'
    star = (f'<button class="fav-btn" type="button" data-fav="{tslug(t)}" '
            f'aria-label="Save {esc_attr(t["primary_title"])} to my list" aria-pressed="false">'
            f'<span aria-hidden="true">&#9733;</span></button>')
    return (f'<div class="{cls}" '
            f'data-v="{title_views(t)}" data-n="{esc_attr(t["primary_title"].lower())}" '
            f'data-y="{esc_attr(t.get("year") or "")}" data-app="{slug(app_name) if app_name else ""}" '
            f'data-ai="{"1" if is_ai(t) else ""}" data-book="{"1" if book_of(t) else ""}"'
            # Emitted ONLY when true. data-ai and data-book are always emitted, and
            # copying that here rewrote 5,074 pages to add an empty attribute -- which
            # is exactly the noise the deterministic build exists to prevent, since it
            # buries the one page that actually changed.
            f'{" data-upcoming=1" if is_upcoming(t) else ""}>'
            f'<a class="poster-link" href="{href}">{poster_box(t, app_name)}</a>{star}'
            f'{app_html}<a class="meta" href="{href}">{meta}</a></div>')

# Reusable client-side re-sort for a static grid (Actor detail, Trope page). Cards
# already carry data-v/data-n/data-y from poster_card, so no extra JSON payload
# is needed just to change display order.
SORT_JS = """
<script>
document.querySelectorAll('[data-sort-for]').forEach(function(sel){
  var grid = document.getElementById(sel.dataset.sortFor);
  if(!grid) return;
  sel.addEventListener('change', function(){
    var cards = Array.prototype.slice.call(grid.children);
    var mode = sel.value;
    cards.sort(function(a,b){
      if(mode==='az') return a.dataset.n.localeCompare(b.dataset.n);
      if(mode==='year') return (b.dataset.y||'').localeCompare(a.dataset.y||'');
      return (parseInt(b.dataset.v,10)||0) - (parseInt(a.dataset.v,10)||0);
    });
    cards.forEach(function(c){ grid.appendChild(c); });
  });
});
document.querySelectorAll('[data-app-filter-for]').forEach(function(sel){
  var grid = document.getElementById(sel.dataset.appFilterFor);
  if(!grid) return;
  sel.addEventListener('change', function(){
    var v = sel.value;
    Array.prototype.forEach.call(grid.children, function(c){
      c.style.display = (!v || c.dataset.app === v) ? '' : 'none';
    });
  });
});
</script>
"""

def sort_select(target_id, label="Sort"):
    return (f'<label class="sort-label">{label}<select class="sort-select" data-sort-for="{target_id}" aria-label="{label}">'
            f'<option value="views">Most watched</option><option value="year">Newest</option><option value="az">A&ndash;Z</option>'
            f'</select></label>')

def actor_tile(p, pre="", ring_size="rail", on_warm=False):
    n = len(credits_by_person.get(p["person_id"], []))
    return (f'<a class="actor-tile" href="{pre}actors/{pslug(p)}.html">'
            f'{actor_ring(p["name"], (p.get("photo_ref") or "").strip(), ring_size, on_warm)}'
            f'<span class="stack"><span class="name">{p["name"]}</span><span class="sub">{n} titles</span></span></a>')

def person_row(name, sub, img, href, size="sm"):
    return (f'<a class="person-row {"sm" if size == "sm" else ""}" href="{href}">'
            f'{actor_ring(name, img, size)}<span class="stack"><span class="name">{name}</span><span class="sub">{sub}</span></span></a>')

def rail(cards, extra_cls=""):
    return f'<div class="rail {extra_cls}">%s</div>' % "".join(cards)

def chip_link(href, name, count=None):
    c = f'<span class="c">{count:,}</span>' if count is not None else ""
    return f'<a class="chip" href="{href}">{name}{c}</a>'

# Trope names are stored lowercase, which reads fine mid-sentence ("billionaire
# stories") but wrong for genuine acronyms. Only well-established ones are listed;
# ambiguous short tags like "sm" are left alone rather than guessed at.
TROPE_ACRONYMS = {"ceo": "CEO", "bl": "BL", "gl": "GL", "dilf": "DILF", "milf": "MILF",
                  "fbi": "FBI", "cia": "CIA", "mma": "MMA", "nyc": "NYC", "vip": "VIP",
                  "ai": "AI", "cfo": "CFO", "pi": "PI"}

def trope_text(name):
    """Trope as it should read inside a sentence or a chip."""
    return " ".join(TROPE_ACRONYMS.get(w.lower(), w) for w in name.split())

def trope_heading(name):
    """Trope as a page heading: title-case, but acronyms stay uppercase."""
    return " ".join(TROPE_ACRONYMS.get(w.lower(), w.title()) for w in name.split())

def trope_chip(tr, pre, count=None):
    """Link only if a trope page exists; otherwise render inert so we never emit a 404."""
    label = trope_text(tr)
    if tr in all_tropes_set:
        return chip_link(f'{pre}tropes/{slug(tr)}.html', label, count)
    c = f'<span class="c">{count:,}</span>' if count is not None else ""
    return f'<span class="chip">{label}{c}</span>'

CSS = """
:root{
--paper:#FBF7F2;--ink:#2A2226;--plum:#2B1B2E;--wine:#7A2B4A;--gold:#C9962E;--gold-deep:#A87B1F;--blush:#EFD9DE;--line:#E4D8CE;
--muted:#5A4A50;--sec:#6B5A60;--tert:#8A7A70;--ph:#9B8C90;--chip-off-fg:#C2B4AC;--chip-off-bg:#F4EDE6;--chip-off-bd:#EBE0D6;
--warm:#F8F1EA;--hero-a:#FDF9F5;--hero-b:#F8F1EA;--blush-bd:#DFBFC8;--input-bd:#D8C7BA;--chip-bd:#E0CFC2;--wine-hover:#5C1E37;
}
*{box-sizing:border-box}
html,body{margin:0;padding:0}
body{background:var(--paper);color:var(--ink);font-family:'Atkinson Hyperlegible',system-ui,sans-serif;font-size:16px;line-height:1.6}
h1,h2,h3{font-family:'Fraunces',Georgia,serif;font-weight:600;line-height:1.14;color:var(--plum);margin:0}
p{margin:0}
a{color:var(--wine);text-decoration:none}
a:hover{color:var(--wine-hover)}
:focus-visible{outline:2px solid var(--wine);outline-offset:2px}
input,select,button,textarea{font-family:'Atkinson Hyperlegible',system-ui,sans-serif}
input::placeholder,textarea::placeholder{color:var(--ph)}
img{max-width:100%}

/* ---------- layout shells ---------- */
.wrap{max-width:760px;margin:0 auto;padding:0 22px}
.wrap-wide{max-width:1320px;margin:0 auto}
.pad{padding:0 22px}

/* ---------- header ---------- */
.site-header{border-bottom:1px solid var(--line);background:var(--paper);padding:16px 22px;display:flex;flex-wrap:wrap;align-items:center;gap:14px 22px}
.wordmark{display:flex;align-items:baseline;gap:2px;flex:0 0 auto;font-family:'Fraunces',Georgia,serif;font-weight:600;font-size:23px;color:var(--plum)}
.wordmark em{font-style:italic;font-weight:400;color:var(--wine)}
.site-nav{display:flex;gap:20px;flex:0 0 auto;font-size:15px;flex-wrap:wrap}
.site-nav a{color:var(--ink);border-bottom:2px solid transparent;padding-bottom:2px}
.site-nav a:hover{color:var(--wine);border-bottom-color:var(--gold)}
.site-search{flex:1 1 210px;max-width:340px;min-width:0;display:flex;align-items:center;gap:8px;border:1px solid var(--line);background:#fff;border-radius:2px;padding:0 12px;margin-left:auto}
.site-search:focus-within{border-color:var(--wine)}
.site-search .glyph{color:var(--wine);font-size:15px;flex:0 0 auto}
.site-search input{flex:1;min-width:0;font-size:16px;line-height:1.2;padding:11px 0;border:0;outline:none;background:transparent;color:var(--ink)}

/* ---------- hero ---------- */
.hero{padding:52px 22px 44px;background:linear-gradient(var(--hero-a),var(--hero-b));border-bottom:1px solid var(--line)}
.hero .inner{max-width:760px}
.eyebrow{margin:0 0 14px;font-size:13px;letter-spacing:.16em;text-transform:uppercase;color:var(--gold-deep)}
h1{font-size:clamp(30px,3.6vw,44px);line-height:1.08;letter-spacing:-.015em;text-wrap:balance}
.hero h1{font-size:clamp(32px,4.4vw,52px);line-height:1.06;letter-spacing:-.02em}
.lede{margin:0 0 26px;font-size:17px;line-height:1.6;color:var(--muted);max-width:56ch;text-wrap:pretty}
.hero-search-form{display:flex;flex-wrap:wrap;gap:10px;max-width:560px}
.hero-search-form input{flex:1 1 240px;min-width:0;font-size:16px;padding:15px 16px;border:1px solid var(--input-bd);background:#fff;border-radius:2px;outline:none;color:var(--ink)}
.hero-search-form input:focus{border-color:var(--wine)}
.stat-line{display:flex;flex-wrap:wrap;gap:8px 22px;margin-top:22px;font-size:14px;color:var(--sec)}
.stat-line b{font-family:'Fraunces',Georgia,serif;font-size:17px;color:var(--plum)}
.stat-line .dot{color:#D9C6B8}

/* ---------- buttons ---------- */
.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;font-size:16px;font-weight:700;padding:15px 26px;border-radius:2px;cursor:pointer;text-decoration:none;min-height:44px;border:0}
.btn-gold{background:var(--gold);color:#241A12}
.btn-gold:hover{background:var(--gold-deep);color:#fff}
.btn-wine{background:var(--paper);color:var(--wine);border:1px solid var(--wine)}
.btn-wine:hover{background:var(--wine);color:#fff}

/* ---------- section headings ---------- */
.section-head{display:flex;align-items:baseline;justify-content:space-between;gap:16px;margin-bottom:18px}
.section-head h2{font-size:26px}
.section-head .all{font-size:14px;white-space:nowrap;border-bottom:1px solid var(--line)}
.section-warm{background:var(--warm);border-top:1px solid var(--line);border-bottom:1px solid var(--line)}

/* ---------- rails ---------- */
.rail{display:flex;gap:18px;overflow-x:auto;padding:0 22px 22px;scroll-snap-type:x mandatory;-webkit-overflow-scrolling:touch;scrollbar-width:thin}
.rail::-webkit-scrollbar{height:8px}
.rail::-webkit-scrollbar-track{background:#EFE7DE;border-radius:4px}
.rail::-webkit-scrollbar-thumb{background:#D9C6B8;border-radius:4px}
.rail-item{flex:0 0 174px;min-width:0;scroll-snap-align:start}
.rail-item.sm{flex-basis:158px}
.rail-item.actor{flex-basis:auto;text-align:center}

/* ---------- grids ---------- */
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(158px,1fr));gap:22px 18px}
.grid.cast{grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:14px}
.grid.apps{grid-template-columns:repeat(auto-fill,minmax(168px,1fr));gap:14px}
.grid.circles{grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:18px}
.grid.trope-idx{grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:8px 14px}
.grid.az{grid-template-columns:repeat(auto-fill,minmax(238px,1fr));gap:12px}

/* ---------- poster card (grid/rail) ---------- */
.poster-card{display:flex;flex-direction:column;gap:6px;min-width:0;color:inherit;position:relative}
.fav-btn{position:absolute;top:7px;left:7px;z-index:4;width:32px;height:32px;padding:0;border:0;cursor:pointer;
border-radius:50%;background:rgba(43,27,46,.55);color:rgba(255,255,255,.85);font-size:16px;line-height:1;
display:flex;align-items:center;justify-content:center;transition:background .15s,color .15s}
.fav-btn:hover{background:rgba(43,27,46,.8);color:#fff}
.fav-btn[aria-pressed="true"]{background:var(--gold);color:#241A12}
.fav-btn:focus-visible{outline:2px solid var(--gold);outline-offset:2px}
.title-actions{display:flex;flex-wrap:wrap;gap:10px;margin:18px 0 0}
.act-btn{display:inline-flex;align-items:center;gap:8px;font-size:15px;padding:11px 18px;border-radius:2px;
border:1px solid var(--wine);background:var(--paper);color:var(--wine);cursor:pointer;min-height:44px;font-family:inherit}
.act-btn:hover{background:var(--wine);color:#fff}
.act-btn[aria-pressed="true"]{background:var(--gold);border-color:var(--gold);color:#241A12}
.act-btn[aria-pressed="true"]:hover{background:var(--gold-deep);color:#fff}
.mylist-actions{display:flex;flex-wrap:wrap;gap:10px}
.mylist-empty{border:1.5px dashed var(--line);border-radius:3px;padding:40px 24px;text-align:center;background:#fff}
.mylist-empty h3{font-family:'Fraunces',Georgia,serif;color:var(--plum);margin-bottom:6px;font-size:19px}
.poster-card .poster-link{display:block;margin-bottom:4px}
.poster-card .meta{display:block;text-decoration:none}
.poster-card .app-name:hover{color:var(--wine-hover);text-decoration:underline}
/* display:block is load-bearing. .poster is a <span>, and it used to be a flex ITEM of
   an <a class="poster-card">, which blockified it for free. Splitting the card so the app
   name could be its own link left it as a plain inline box, and an absolutely-positioned
   image inside an inline containing block resolves to ZERO width -- every poster on the
   site silently vanished while the HTML still looked perfect. Do not remove. */
.poster{display:block;position:relative;aspect-ratio:2/3;background:#F1E6E9;border:1px solid var(--line);border-radius:3px;overflow:hidden}
.poster--empty{display:flex}
.ai-badge{position:absolute;top:6px;right:6px;z-index:3;background:rgba(43,27,46,.86);color:#F6EEE6;
font-size:10.5px;font-weight:700;letter-spacing:.1em;padding:3px 7px;border-radius:2px;line-height:1}
/* Left, so a title that is both AI and unreleased shows both badges side by side. */
.soon-badge{position:absolute;top:6px;left:6px;z-index:3;background:var(--wine);color:#F6EEE6;
font-size:10.5px;font-weight:700;letter-spacing:.1em;padding:3px 7px;border-radius:2px;line-height:1}
.book-note{margin:0 0 16px;font-size:14.5px;color:var(--wine)}
.ai-toggle{display:flex;align-items:center;gap:9px;font-size:14px;color:var(--ink);cursor:pointer;
padding:11px 12px;border:1px solid var(--chip-bd);background:#fff;border-radius:2px;margin:26px 0 0}
.ai-toggle input{width:17px;height:17px;accent-color:var(--wine);cursor:pointer}
.poster img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block}
.poster--empty{height:100%;background:var(--blush);padding:15px 13px;display:flex;flex-direction:column;justify-content:space-between;gap:10px}
.poster--empty .label{font-size:10.5px;letter-spacing:.15em;text-transform:uppercase;color:#A0687D}
.poster--empty .ttl{font-family:'Fraunces',Georgia,serif;font-weight:600;font-size:16px;line-height:1.22;color:var(--plum);text-wrap:pretty;min-width:0}
.poster--empty .app{border-top:1px solid var(--blush-bd);padding-top:9px;font-size:11.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--wine)}
.rail-item .poster--empty .ttl{font-size:17px}
.rail-item.sm .poster--empty .ttl{font-size:15px}
.actor-tile .stack,.person-row .stack{display:block}
.bio{max-width:62ch}
.bio h2{font-size:20px;margin-bottom:8px}
.bio p{font-size:16px;line-height:1.65;color:#3E3238;text-wrap:pretty}
.poster-card .app-name{font-size:13px;font-weight:700;color:var(--wine)}
.poster-card .card-note{display:block;font-size:13px;color:var(--ink);line-height:1.35;text-wrap:pretty}
.poster-card .meta{font-size:13px;color:var(--sec);line-height:1.45;text-wrap:pretty;min-width:0}
.poster-card:hover .poster{border-color:var(--wine)}

/* ---------- actor identity: monogram ring ---------- */
.ring{position:relative;border-radius:50%;background:var(--blush);overflow:hidden;flex:0 0 auto;display:flex;align-items:center;justify-content:center;font-family:'Fraunces',Georgia,serif;font-weight:600;color:var(--wine);letter-spacing:.02em}
.ring img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.ring--sm{width:46px;height:46px;font-size:16px;box-shadow:inset 0 0 0 2px #fff,0 0 0 1px var(--blush-bd)}
.ring--md{width:50px;height:50px;font-size:17px;box-shadow:inset 0 0 0 2px #fff,0 0 0 1px var(--blush-bd)}
.ring--rail{width:78px;height:78px;font-size:24px;box-shadow:inset 0 0 0 3px var(--paper),0 0 0 1px var(--blush-bd)}
.ring--rail.on-warm{box-shadow:inset 0 0 0 3px var(--warm),0 0 0 1px var(--blush-bd)}
.ring--hero{width:132px;height:132px;font-size:44px;box-shadow:inset 0 0 0 5px var(--paper),0 0 0 1px var(--blush-bd)}

.actor-tile{display:flex;flex-direction:column;align-items:center;gap:10px;text-align:center;text-decoration:none;color:inherit}
.actor-tile .name{font-size:15px;color:var(--ink);line-height:1.3}
.actor-tile .sub{font-size:13px;color:var(--tert)}

.person-row{display:flex;align-items:center;gap:14px;border:1px solid var(--line);background:#fff;padding:13px 15px;min-width:0;text-decoration:none;color:inherit}
.person-row:hover{border-color:var(--wine)}
.person-row.sm{padding:12px 14px;gap:13px}
.person-row .name{font-size:15.5px;color:var(--ink);line-height:1.3}
.person-row .sub{font-size:13px;color:var(--tert)}

/* ---------- chips (feed the existing filter JS: data-g / data-v) ---------- */
.chip{display:inline-flex;align-items:baseline;gap:7px;padding:8px 14px;border:1px solid var(--chip-bd);background:var(--paper);border-radius:999px;font-size:15px;font-family:inherit;color:var(--ink);text-decoration:none;cursor:pointer}
.chip .c{font-size:12.5px;color:var(--ph)}
.chip:hover:not(.off){border-color:var(--wine);background:#fff}
.chip.on{background:var(--wine);border-color:var(--wine);color:#FFF8F2}
.chip.on .c{color:rgba(255,248,242,.75)}
.chip.off{border-color:var(--chip-off-bd);background:var(--chip-off-bg);color:var(--chip-off-fg);cursor:not-allowed}
.chip.off .c{color:var(--chip-off-fg)}
.chips{display:flex;flex-wrap:wrap;gap:10px}
.chips.tight{gap:8px}
.chips.collapsed .extra{display:none}
.chip-all{display:inline-flex;align-items:center;padding:9px 16px;border:1px solid var(--wine);border-radius:999px;font-size:15px;font-weight:700;color:var(--wine)}
.chip-all:hover{background:var(--wine);color:#fff}
.chip-dashed{margin-top:12px;font-size:14px;padding:9px 15px;background:transparent;border:1px dashed #C0A99A;color:var(--wine);border-radius:999px;cursor:pointer;font-family:inherit}
.chip-dashed:hover{border-style:solid;border-color:var(--wine)}

/* ---------- app tiles ---------- */
.app-tile{border:1px solid var(--line);background:#fff;padding:18px 16px;display:flex;flex-direction:column;gap:5px;text-decoration:none;color:inherit}
.app-tile:hover{border-color:var(--gold)}
.app-tile .n{font-family:'Fraunces',Georgia,serif;font-weight:600;font-size:19px;color:var(--plum)}
.app-tile .c{font-size:13.5px;color:var(--sec)}

/* ---------- form fields ---------- */
.field{display:flex;flex-direction:column;gap:7px}
.field label{font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--tert)}
.field input,.field select,.field textarea{width:100%;font-size:16px;padding:13px 14px;border:1px solid var(--input-bd);background:#fff;border-radius:2px;outline:none;color:var(--ink)}
.field input:focus,.field select:focus,.field textarea:focus{border-color:var(--wine)}
.field textarea{font-family:inherit;line-height:1.55;resize:vertical}
.field .hint{font-size:13px;color:var(--ph)}
.sort-label{display:flex;align-items:center;gap:8px;font-size:14px;color:var(--sec)}
.sort-label select{font-size:16px;padding:9px 11px;border:1px solid var(--input-bd);background:#fff;color:var(--ink);border-radius:2px}

/* ---------- breadcrumb ---------- */
.crumb{padding:14px 22px;font-size:13.5px;color:var(--tert);border-bottom:1px solid var(--line);display:flex;gap:8px;flex-wrap:wrap}
.crumb a{color:var(--tert)}
.crumb a:hover{color:var(--wine)}
.crumb .current{color:var(--sec)}

/* ---------- where-to-watch card ---------- */
.watch-card{background:#fff;border:1px solid var(--line);padding:20px;max-width:440px}
.watch-card .label{margin:0 0 14px;font-size:13px;letter-spacing:.12em;text-transform:uppercase;color:var(--tert)}
.watch-btn{display:flex;align-items:center;justify-content:space-between;gap:14px;background:var(--gold);color:#241A12;padding:17px 22px;font-size:18px;font-weight:700;border-radius:2px;text-decoration:none}
.watch-btn:hover{background:var(--gold-deep);color:#fff}
.watch-more{display:block;margin-top:12px;font-size:14px;color:var(--wine)}
.watch-disclosure{margin:12px 0 0;font-size:12.5px;color:var(--ph);line-height:1.5}
.watch-pending{display:inline-block;padding:13px 20px;border:1.5px dashed var(--line);border-radius:999px;color:var(--tert);font-size:14px}

/* ---------- title / actor / app hero (two-column, gradient) ---------- */
.split-hero{display:flex;flex-wrap:wrap;gap:34px;padding:34px 22px 40px;background:linear-gradient(var(--hero-a),var(--hero-b));border-bottom:1px solid var(--line)}
.split-hero.tight{gap:28px;padding:36px 22px 34px;align-items:flex-start}
.split-hero .poster-col{flex:0 1 300px;min-width:0}
.split-hero .poster-col img{width:100%;aspect-ratio:2/3;object-fit:cover;display:block;border:1px solid var(--line);border-radius:3px}
.split-hero .info-col{flex:1 1 400px;min-width:0}
.views-line{margin:0 0 22px;font-size:15.5px;color:var(--sec)}
.story{margin-top:28px;max-width:60ch}
.story h2{margin:0 0 8px;font-size:20px}
.story p{margin:0;font-size:16px;line-height:1.65;color:#3E3238;text-wrap:pretty}

.stat-figures{display:flex;flex-wrap:wrap;gap:10px 26px;margin-top:20px}
.stat-figures .stat{display:block}
.stat-figures .n{display:block;font-family:'Fraunces',Georgia,serif;font-size:26px;color:var(--plum);line-height:1.1}
.stat-figures .l{display:block;font-size:13px;color:var(--tert);letter-spacing:.04em}
.stat-figures .divider{width:1px;align-self:stretch;background:var(--line)}
.usual{display:flex;flex-wrap:wrap;gap:8px;margin-top:22px;align-items:center}
.usual .label{font-size:13px;color:var(--tert)}

.app-cta{flex:0 1 320px;min-width:0;background:#fff;border:1px solid var(--line);padding:20px}
.app-cta .label{margin:0 0 14px;font-size:13px;letter-spacing:.12em;text-transform:uppercase;color:var(--tert)}

/* ---------- browse ---------- */
.browse-layout{display:flex;flex-wrap:wrap;align-items:flex-start}
.browse-aside{flex:1 1 288px;min-width:0;border-right:1px solid var(--line);background:var(--warm);padding:26px 20px 40px;align-self:stretch}
.browse-aside h1{font-size:27px;margin:0 0 18px}
.aside-search{display:flex;align-items:center;gap:8px;border:1px solid var(--input-bd);background:#fff;padding:0 12px;margin-bottom:22px}
.aside-search:focus-within{border-color:var(--wine)}
.aside-search input{flex:1;min-width:0;font-size:16px;padding:12px 0;border:0;outline:none;background:transparent}
.active-filters{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:10px 12px;background:var(--blush);border:1px solid var(--blush-bd);margin-bottom:24px}
.active-filters .txt{font-size:13.5px;color:var(--wine-hover);line-height:1.4}
.reset-pill{flex:0 0 auto;font-size:13px;padding:6px 11px;background:transparent;border:1px solid #B98A9B;color:var(--wine);border-radius:999px;cursor:pointer;font-family:inherit}
.reset-pill:hover{background:var(--wine);color:#fff;border-color:var(--wine)}
.filter-group{margin-bottom:26px}
.filter-group h2{margin:0 0 4px;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--tert);font-family:'Atkinson Hyperlegible',sans-serif;font-weight:700}
.filter-group .hint{margin:0 0 11px;font-size:13px;color:var(--ph)}
.results-panel{flex:3 1 560px;min-width:0;padding:26px 22px 46px}
.results-head{display:flex;flex-wrap:wrap;align-items:baseline;justify-content:space-between;gap:12px;padding-bottom:14px;border-bottom:1px solid var(--line);margin-bottom:22px}
.results-head .count{margin:0;font-size:16px;color:var(--ink)}
.results-head .count b{font-family:'Fraunces',Georgia,serif;font-size:22px;color:var(--plum)}
.show-more{display:flex;justify-content:center;margin-top:34px}
.no-results{font-size:15px;color:var(--sec)}

/* ---------- actors A-Z ---------- */
.az-bar{padding:20px 22px 10px;border-bottom:1px solid var(--line);position:sticky;top:0;background:rgba(251,247,242,.96);backdrop-filter:blur(6px);z-index:5}
.az-letters{display:flex;flex-wrap:wrap;gap:6px}
.az-letter{min-width:34px;min-height:34px;padding:0 8px;display:inline-flex;align-items:center;justify-content:center;border:1px solid var(--chip-bd);background:var(--paper);color:var(--wine);border-radius:2px;font-size:14.5px;font-weight:700;text-decoration:none}
.az-letter:hover{border-color:var(--wine)}
.az-letter.empty{border-color:#EDE4DB;background:#F5EFE8;color:var(--chip-off-fg);pointer-events:none}
.idx-letter{grid-column:1/-1;margin:22px 0 4px;font-size:22px;color:var(--wine);border-bottom:1px solid var(--line);padding-bottom:8px}
.trope-idx .idx-letter{margin:20px 0 2px;font-size:21px;padding-bottom:7px}
.pagination{display:flex;align-items:center;justify-content:center;gap:10px;margin-top:36px;flex-wrap:wrap}
.pagination a{padding:12px 18px;border:1px solid var(--chip-bd);background:#fff;font-size:15px;text-decoration:none;color:var(--ink)}
.pagination a.next{border-color:var(--wine);font-weight:700;color:var(--wine)}
.pagination a.next:hover{background:var(--wine);color:#fff}
.pagination .status{font-size:14px;color:var(--tert)}

/* ---------- all-tropes index ---------- */
.trope-idx-row{display:flex;align-items:baseline;justify-content:space-between;gap:10px;padding:11px 13px;border-bottom:1px solid #EFE5DC;font-size:15.5px;color:var(--ink);min-width:0;text-decoration:none}
.trope-idx-row:hover{background:var(--warm);color:var(--wine)}
.trope-idx-row .n{min-width:0;text-wrap:pretty}
.trope-idx-row .c{flex:0 0 auto;font-size:13px;color:var(--ph)}

/* ---------- blog ---------- */
.blog-featured{display:flex;flex-wrap:wrap;gap:26px;align-items:stretch;border:1px solid var(--line);background:#fff;overflow:hidden;text-decoration:none;color:inherit}
.blog-featured:hover{border-color:var(--wine)}
.blog-featured .copy{flex:1 1 300px;min-width:0;order:2;padding:26px 26px 28px;display:flex;flex-direction:column;gap:12px;justify-content:center}
.blog-featured .art{flex:0 1 340px;min-width:0;order:1;align-self:stretch}
.blog-featured .art img{width:100%;height:100%;min-height:230px;object-fit:cover;display:block}
.blog-kicker{font-size:11.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--gold-deep)}
.blog-featured h2{font-size:clamp(24px,2.6vw,32px);line-height:1.14;letter-spacing:-.01em;text-wrap:pretty}
.blog-sub{font-size:13.5px;color:var(--tert)}
.blog-row{display:flex;flex-wrap:wrap;gap:18px;align-items:flex-start;padding:22px 4px;border-bottom:1px solid #EFE5DC;min-width:0;text-decoration:none;color:inherit}
.blog-row:hover{background:#FBF5EF}
.blog-row .thumb{flex:0 0 auto;width:96px;aspect-ratio:2/3;background:var(--blush);border:1px solid var(--line);border-radius:3px;overflow:hidden}
.blog-row .thumb img{width:100%;height:100%;object-fit:cover;display:block}
.blog-row .body{flex:1 1 240px;min-width:0}
.blog-row h3{font-size:20px;line-height:1.2;text-wrap:pretty}
.blog-row .excerpt{font-size:15px;line-height:1.6;color:var(--muted);max-width:56ch;text-wrap:pretty}
.newsletter-block{border:1px solid var(--blush-bd);background:var(--blush);padding:20px}
.newsletter-block p{font-size:14.5px;line-height:1.55;color:#5C4048}
.newsletter-block input{width:100%;font-size:16px;padding:13px 14px;border:1px solid #C8A3AF;background:#fff;border-radius:2px;outline:none;color:var(--ink);margin-bottom:10px}
.topics-block{border:1px solid var(--line);background:#fff;padding:20px}
.blog-empty{border:1.5px dashed var(--line);border-radius:3px;padding:44px 24px;text-align:center;color:var(--sec);background:#fff}
.blog-empty h3{font-family:'Fraunces',Georgia,serif;color:var(--plum);margin-bottom:6px;font-size:19px}

/* ---------- contact ---------- */
.reason-pill{padding:9px 15px;border:1px solid var(--chip-bd);background:var(--paper);color:var(--ink);border-radius:999px;font-size:15px;cursor:pointer;font-family:inherit}
.reason-pill.on{border-color:var(--wine);background:var(--wine);color:#FFF8F2}
.contact-row{display:flex;flex-wrap:wrap;gap:16px}
.contact-row .field{flex:1 1 200px;min-width:0}
.contact-side{flex:1 1 260px;min-width:0;display:flex;flex-direction:column;gap:16px}
.side-card{border:1px solid var(--line);background:#fff;padding:20px}
.side-card h2{font-size:19px;margin-bottom:12px}
.side-card.warn{border-color:var(--blush-bd);background:var(--blush)}
.side-card.warn ul{margin:0;padding-left:20px;display:flex;flex-direction:column;gap:9px;font-size:14.5px;line-height:1.55;color:#5C4048}
.side-card .kv{margin-bottom:14px}
.side-card .kv:last-child{margin-bottom:0}
.side-card .kv .k{font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--tert);margin-bottom:4px}
.reassure{font-size:13.5px;color:var(--tert);max-width:34ch;line-height:1.5}

/* ---------- misc ---------- */
.empty-state{border:1.5px dashed var(--line);border-radius:3px;padding:32px 26px;text-align:center;background:#fff}
.empty-state h3{font-family:'Fraunces',Georgia,serif;color:var(--plum);margin-bottom:4px;font-size:18px}
.empty-state p{color:var(--sec);font-size:14px;max-width:38ch;margin:0 auto;line-height:1.55}
table{border-collapse:collapse;width:100%;font-size:.9rem}
th{background:var(--plum);color:#fff;text-align:left;padding:8px 10px}
td{border:1px solid var(--line);padding:8px 10px;vertical-align:top}
tr:nth-child(even) td{background:#F7F0EA}

/* ---------- socials + faq (pre-existing SEO content, restyled) ---------- */
.chips.socials{margin:14px 0 2px}
.chips.socials .chip{font-size:13px}
.faq{background:var(--plum);color:#EFE4EA;padding:34px 22px 40px}
.faq h2{color:#fff;font-size:22px;margin-bottom:10px}
.faq details{border-bottom:1px solid #4a3450;padding:13px 0}
.faq summary{cursor:pointer;font-weight:700;font-size:15px}
.faq p{margin-top:8px;font-size:14px;line-height:1.55;color:#D9C8D4}
.faq .note{font-size:13px;color:#9b86a0;margin-top:20px}

/* ---------- footer ---------- */
footer.site-footer{border-top:1px solid var(--line);background:var(--plum);color:#E8DCD4;padding:34px 22px 30px;display:flex;flex-wrap:wrap;gap:24px 40px;justify-content:space-between}
.footer-brand{max-width:38ch}
.footer-brand .wordmark{font-family:'Fraunces',Georgia,serif;font-size:20px;margin-bottom:8px}
.footer-brand .wordmark em{font-style:italic;color:var(--gold)}
.footer-brand .wordmark span{color:#F6EEE6}
.footer-brand p{margin:0;font-size:13.5px;line-height:1.6;color:#BCA9AF}
.footer-cols{display:flex;gap:40px;flex-wrap:wrap;font-size:14px}
.footer-col{display:flex;flex-direction:column;gap:8px}
.footer-col .h{font-size:11.5px;letter-spacing:.14em;text-transform:uppercase;color:#8A7480}
.footer-col a{color:#E8DCD4}
.footer-col a:hover{color:#fff}
"""

def page(title, desc, body, canonical, jsonld=None, depth=1, nav_search_val=""):
    pre = "../" * depth
    ld = f'<script type="application/ld+json">{json.dumps(jsonld)}</script>' if jsonld else ""
    app_links = "".join(
        f'<a href="{pre}apps/{slug(pl["name"])}.html">{pl["name"]}</a>'
        for pl in APPS_WITH_DATA[:3])
    q = esc_attr(nav_search_val)
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
{ld}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,600;0,9..144,700;1,9..144,400&family=Atkinson+Hyperlegible:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{pre}style.css">
</head><body>
<header class="site-header">
<a class="wordmark" href="{pre}index.html"><span>Drama</span><em>EverAfter</em></a>
<nav class="site-nav">
<a href="{pre}browse.html">Browse</a>
<a href="{pre}actors/index.html">Actors</a>
<a href="{pre}platforms.html">Apps</a>
<a href="{pre}tropes/index.html">Tropes</a>
<a href="{pre}blog.html">Blog</a>
<a href="{pre}my-list.html">My List</a>
</nav>
<form class="site-search" action="{pre}browse.html" method="get">
<span class="glyph">&#8981;</span>
<input type="search" name="q" placeholder="Search a title or actor" aria-label="Search a title or actor" value="{q}">
</form>
</header>
{body}
<footer class="site-footer">
<div class="footer-brand">
<div class="wordmark"><span>Drama</span><em>EverAfter</em></div>
<p>A reader-made index of vertical dramas &mdash; which app, which cast, what next. Some links earn a commission.</p>
</div>
<div class="footer-cols">
<div class="footer-col"><span class="h">Browse</span>
<a href="{pre}browse.html">All titles</a><a href="{pre}actors/index.html">Actors</a><a href="{pre}tropes/index.html">Tropes</a></div>
<div class="footer-col"><span class="h">Apps</span>
{app_links}<a href="{pre}platforms.html">All apps</a></div>
<div class="footer-col"><span class="h">Site</span>
<a href="{pre}index.html">Home</a><a href="{pre}my-list.html">My List</a><a href="{pre}blog.html">Blog</a><a href="{pre}contact.html">Contact</a></div>
</div>
</footer>
</body></html>"""

def watch_buttons(title_id, pre=""):
    avails = avail_by_title.get(title_id, [])
    if not avails:
        # An unreleased title has no availability for a reason, so saying "platform
        # being verified" would be wrong twice: it implies we are mid-check, and it
        # implies the show is watchable somewhere. Say what is actually true.
        t = t_by_id.get(title_id)
        if t is not None and is_upcoming(t):
            return '<span class="watch-pending">Not released yet</span>'
        return '<span class="watch-pending">Platform being verified</span>'
    a = avails[0]
    name = platforms.get(a["platform_id"], {}).get("name", "?")
    link = a["direct_link"] or "#AFFILIATE-LINK-PENDING"
    # An upcoming title normally DOES have a known platform -- that is the whole point
    # of announcing it -- so it reaches here with an availability row and would other-
    # wise render "Watch on ReelShort" for something nobody can watch. Say "Coming to"
    # and do not link out, because the destination has nothing to play yet.
    t_up = t_by_id.get(title_id)
    if t_up is not None and is_upcoming(t_up):
        return f'<span class="watch-pending">Coming to {name}</span>'
    out = f'<a class="watch-btn" href="{link}"><span>Watch on {name}</span><span class="arrow">&rarr;</span></a>'
    if len(avails) > 1:
        others = ", ".join(platforms.get(r["platform_id"], {}).get("name", "?") for r in avails[1:])
        out += f'<span class="watch-more">Also on {others}</span>'
    return out

# Favourites live ONLY in the visitor's own browser (localStorage). Nothing is sent
# anywhere, there is no account and no backend, so there is nothing to secure and
# nothing to breach. The UI says "saved on this device" so nobody expects it to sync.
FAV_JS = """
<script>
(function(){
  var KEY='dea_favs';
  function read(){ try{ return JSON.parse(localStorage.getItem(KEY)||'[]'); }catch(e){ return []; } }
  function write(v){ try{ localStorage.setItem(KEY, JSON.stringify(v)); }catch(e){} }
  function has(s){ return read().indexOf(s)!==-1; }
  function toggle(s){
    var v=read(), i=v.indexOf(s);
    if(i===-1) v.push(s); else v.splice(i,1);
    write(v); return i===-1;
  }
  window.deaFavs={read:read,has:has,toggle:toggle,KEY:KEY};

  function paint(btn){
    var on=has(btn.dataset.fav);
    btn.setAttribute('aria-pressed', on?'true':'false');
    if(btn.classList.contains('act-btn')){
      var lbl=btn.querySelector('.act-label');
      if(lbl) lbl.textContent = on ? 'Saved to my list' : 'Save to my list';
    }
  }
  function wire(root){
    (root||document).querySelectorAll('[data-fav]').forEach(function(b){
      if(b.dataset.favWired) return;
      b.dataset.favWired='1';
      paint(b);
      b.addEventListener('click', function(e){
        e.preventDefault(); e.stopPropagation();
        toggle(b.dataset.fav);
        document.querySelectorAll('[data-fav="'+b.dataset.fav+'"]').forEach(paint);
        if(window.deaOnFavChange) window.deaOnFavChange();
      });
    });
  }
  window.deaWireFavs=wire;
  if(document.readyState!=='loading') wire(); else document.addEventListener('DOMContentLoaded',function(){wire();});
})();
</script>
"""

# Share uses the phone's own share sheet where available and falls back to copying the
# link. No third-party buttons, so no tracking scripts loaded onto the page.
SHARE_JS = """
<script>
document.addEventListener('click', function(e){
  var b=e.target.closest('[data-share]');
  if(!b) return;
  e.preventDefault();
  var url=b.dataset.share, title=b.dataset.shareTitle||document.title;
  if(navigator.share){ navigator.share({title:title,url:url}).catch(function(){}); return; }
  var done=function(){
    var l=b.querySelector('.act-label'); if(!l) return;
    var old=l.textContent; l.textContent='Link copied';
    setTimeout(function(){ l.textContent=old; }, 1800);
  };
  if(navigator.clipboard && navigator.clipboard.writeText){
    navigator.clipboard.writeText(url).then(done).catch(function(){ window.prompt('Copy this link:', url); });
  } else { window.prompt('Copy this link:', url); }
});
</script>
"""


def watch_card(title_id, pre=""):
    return (f'<div class="watch-card"><p class="label">Where to watch</p>{watch_buttons(title_id, pre)}'
            f'<p class="watch-disclosure">We may earn a commission, which is what keeps this database free.</p></div>')

# --------- derived actor summary -------------------------------------------
# Computed at build time from credits/availability/titles, never stored in
# people.csv. Two reasons: it would duplicate data that is already there and go
# stale the moment a credit is added, and bio_short holds REAL sourced biography
# for 703 people -- mixing generated text into that column would make it
# impossible to tell the two apart later.
#
# Hard rule: every clause below must be traceable to a row in the CSVs. No claim
# about a real person that the database cannot support.

def _plural(n, word):
    return f"{n} {word}" + ("" if n == 1 else "s")

# --------- sourced biography cleanup ---------------------------------------
# bio_short was harvested from the ReelShort fandom blog and a lot of it arrived
# with article furniture attached: "Sarah Moliski as Haley Actress, host and...",
# "Part 1: Who's in ...", or circular junk like "X is the actor playing Y".
# The character-name prefix is strippable EXACTLY, because we already hold the
# real character names in credits.csv -- no guessing at where the name ends.
_chars_by_person = defaultdict(set)
for _c in credits:
    _ch = (_c.get("character_name") or "").strip()
    if _ch: _chars_by_person[_c["person_id"]].add(_ch)

_BIO_JUNK = [
    re.compile(r"\bis the (actor|actress) (playing|behind)\b", re.I),
    re.compile(r"\bfans have praised\b", re.I),
    re.compile(r"Meet the .{0,24}(Cast|Lineup)", re.I),
    re.compile(r"^\S+\s+as\s+[A-Z]"),          # still a role fragment after cleaning
]

def clean_bio(p):
    """Return a presentable sourced biography, or '' if what we harvested is junk."""
    b = re.sub(r"\s+", " ", (p.get("bio_short") or "").strip())
    if not b:
        return ""
    name = p["name"]
    for ch in sorted(_chars_by_person.get(p["person_id"], ()), key=len, reverse=True):
        b = re.sub(r"^" + re.escape(name) + r"\s+as\s+" + re.escape(ch) + r"\s*[,.:;-]?\s*",
                   "", b, flags=re.I)
    b = re.sub(r"^Part\s*\d+\s*[:.-]?\s*", "", b).strip()
    # 40, not 60: "ReelShort actor known for dark mafia romance leads." is a perfectly
    # good short bio, and the junk patterns above already catch the genuinely useless
    # short ones ("X is the actor playing Y", headline questions).
    if len(b) < 40 or b.endswith("?") or any(r.search(b) for r in _BIO_JUNK):
        return ""
    return b

def actor_summary(p, pairs):
    """pairs: list of (credit_row, title_row) for this person."""
    if not pairs:
        return "No verified credits in the database yet. This page fills in as titles are confirmed."
    titles = [t for _c, t in pairs]
    n = len(titles)

    plat = defaultdict(int)
    for t in titles:
        for a in avail_by_title.get(t["title_id"], []):
            if a["platform_id"] in platforms:
                plat[platforms[a["platform_id"]]["name"]] += 1
    top_plat = sorted(plat.items(), key=lambda kv: -kv[1])

    trope_n = defaultdict(int)
    for t in titles:
        for tr in tropes_of(t): trope_n[tr] += 1
    top_tr = [tr for tr, _ in sorted(trope_n.items(), key=lambda kv: -kv[1])[:2]]

    # Co-stars: people sharing a title with this person, most frequent first.
    co = defaultdict(int)
    for t in titles:
        for c in credits_by_title.get(t["title_id"], []):
            if c["person_id"] != p["person_id"] and c["person_id"] in p_by_id:
                co[c["person_id"]] += 1
    top_co = sorted(co.items(), key=lambda kv: -kv[1])
    best = max(titles, key=lambda t: title_views(t))

    # Sentence 1: volume and where. "all of them" only makes sense for more than one.
    if len(top_plat) == 1:
        where = f"on {top_plat[0][0]}" if n == 1 else f"all of them on {top_plat[0][0]}"
        s1 = f"Appears in {_plural(n, 'title')} in the database, {where}."
    elif len(top_plat) > 1:
        s1 = (f"Appears in {_plural(n, 'title')} in the database, most of them on "
              f"{top_plat[0][0]}, and also turns up on {top_plat[1][0]}.")
    else:
        s1 = f"Appears in {_plural(n, 'title')} in the database."

    out = [s1]
    # Sentence 2: what kind of stories, only when a trope actually repeats.
    if top_tr and trope_n[top_tr[0]] > 1:
        named = [trope_text(x) for x in top_tr]
        kinds = " and ".join(named) if len(named) > 1 and trope_n[top_tr[1]] > 1 else named[0]
        out.append(f"Those credits lean toward {kinds} stories.")
    # Sentence 3: a recurring co-star, only if they have genuinely repeated.
    if top_co and top_co[0][1] > 1:
        out.append(f"Has shared {_plural(top_co[0][1], 'title')} with "
                   f"{p_by_id[top_co[0][0]]['name']}, more than with anyone else.")
    # Sentence 4: the most-watched credit, only when we have a real view count.
    if title_views(best):
        out.append(f"The most-watched credit here is {best['primary_title']}, "
                   f"at {views_label(title_views(best)).replace(' views', ' views')}.")
    return " ".join(out)

# --------- build ---------
# Selective clean: remove ONLY generated artifacts, never data/ or generator/
for d in ["actors", "titles", "tropes", "where-to-watch", "apps"] + origins_other:
    p = os.path.join(DIST, d)
    if os.path.exists(p): shutil.rmtree(p)
for f in ["index.html", "platforms.html", "browse.html", "blog.html", "contact.html", "my-list.html", "robots.txt", "sitemap.xml", "style.css"]:
    p = os.path.join(DIST, f)
    if os.path.exists(p): os.remove(p)
for d in ["", "actors", "titles", "tropes", "apps"]:
    os.makedirs(os.path.join(DIST, d), exist_ok=True)
open(os.path.join(DIST, "style.css"), "w").write(CSS)
urls = []

# Actor pages
for p in people:
    sl = pslug(p)
    my_credits = credits_by_person.get(p["person_id"], [])
    my_pairs = [(c, t_by_id[c["title_id"]]) for c in my_credits if c["title_id"] in t_by_id]
    my_titles = [t for _c, t in my_pairs]
    # Character name is the single most useful fact on an actor's own page, so it
    # rides along on the card caption. 1,509 of 3,585 credits have one.
    note_for = {}
    for c, t in my_pairs:
        role = (c.get("role") or "").replace("+", " &middot; ").title() or "Cast"
        ch = (c.get("character_name") or "").strip()
        note_for[t["title_id"]] = f"{role} &middot; {ch}" if ch else role
    verified_n = len(my_titles)
    plat_counts = defaultdict(int)
    for t in my_titles:
        for a in avail_by_title.get(t["title_id"], []):
            if a["platform_id"] in platforms: plat_counts[platforms[a["platform_id"]]["name"]] += 1
    top_plats = sorted(plat_counts.items(), key=lambda kv: -kv[1])
    trope_counts_p = defaultdict(int)
    for t in my_titles:
        for tr in tropes_of(t): trope_counts_p[tr] += 1
    top_tropes_p = sorted(trope_counts_p.items(), key=lambda kv: -kv[1])
    years = sorted({t["year"] for t in my_titles if t.get("year")})
    active = f"{years[0]}–{years[-1]}" if len(years) > 1 else (years[0] if years else "—")
    # ONE biography per actor, never two. A cleaned sourced bio is better writing
    # than anything derived, so it leads when we have one; otherwise the derived
    # factual summary stands alone. The stat figures and trope chips below already
    # carry the numbers, so nothing is lost by not printing both.
    real_bio = clean_bio(p)
    oneliner = real_bio or actor_summary(p, my_pairs)
    usual_html = "".join(trope_chip(tr, "../", cnt) for tr, cnt in top_tropes_p[:8])
    cards = "".join(poster_card(t, "../", note=note_for.get(t["title_id"], ""))
                    for t in sorted(my_titles, key=lambda x: -title_views(x)))
    plat_line = ", ".join(n for n, _ in top_plats) if top_plats else "platform verification in progress"
    ld = {"@context": "https://schema.org", "@type": "Person", "name": p["name"], "jobTitle": "Actor",
          "description": (real_bio or oneliner)[:160],
          "performerIn": [{"@type": "TVSeries", "name": t["primary_title"]} for t in my_titles]}
    body = f"""
<nav class="crumb"><a href="../actors/index.html">Actors</a><span>/</span><span class="current">{p['name']}</span></nav>
<section class="split-hero tight">
{actor_ring(p['name'], (p.get('photo_ref') or '').strip(), "hero")}
<div class="info-col">
<p class="eyebrow">Actor</p><h1>{p['name']}</h1>
<p class="lede">{oneliner}</p>
{social_links(p)}
<div class="stat-figures">
<div class="stat"><span class="n">{verified_n}</span><span class="l">titles</span></div>
<div class="divider"></div>
<div class="stat"><span class="n">{len(plat_counts) or '?'}</span><span class="l">apps</span></div>
<div class="divider"></div>
<div class="stat"><span class="n">{active}</span><span class="l">active</span></div>
</div>
{f'<div class="usual"><span class="label">Usual tropes</span>{usual_html}</div>' if usual_html else ''}
</div>
</section>
<section class="pad" style="padding:26px 22px 46px">
<div class="results-head"><h2 style="font-size:24px">Credits</h2>{sort_select('credits-grid')}</div>
<div class="grid" id="credits-grid">{cards}</div>
</section>
{SORT_JS}{FAV_JS}
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

# Actors A-Z (NEW): a real single-page directory rather than the prototype's fake
# pagination -- with 1,850 rows, a jump-to-letter anchor bar serves the same intent
# (find a letter fast) better than paging through ~74 screens.
def surname(name): return name.split()[-1] if name.split() else name
photo_n = sum(1 for p in people if (p.get("photo_ref") or "").strip())
directory = sorted(people, key=lambda p: surname(p["name"]).lower())
present_letters = {surname(p["name"])[0].upper() for p in people if surname(p["name"])}
az_bar = "".join(
    f'<a class="az-letter" href="#letter-{L}">{L}</a>' if L in present_letters
    else f'<span class="az-letter empty" aria-disabled="true">{L}</span>'
    for L in "ABCDEFGHIJKLMNOPQRSTUVWXYZ")
rows_html, cur = [], ""
for p in directory:
    L = surname(p["name"])[0].upper() if surname(p["name"]) else "#"
    if L != cur:
        cur = L
        rows_html.append(f'<h2 class="idx-letter" id="letter-{L}">{L}</h2>')
    n = len(credits_by_person.get(p["person_id"], []))
    app = title_app(t_by_id[credits_by_person[p["person_id"]][0]["title_id"]]) if credits_by_person.get(p["person_id"]) and credits_by_person[p["person_id"]][0]["title_id"] in t_by_id else ""
    sub = f"{n} title{'s' if n != 1 else ''}" + (f" &middot; {app}" if app else "")
    rows_html.append(
        f'<a class="person-row sm" href="{pslug(p)}.html" data-n="{esc_attr(p["name"].lower())}">'
        f'{actor_ring(p["name"], (p.get("photo_ref") or "").strip(), "sm")}'
        f'<span class="stack"><span class="name">{p["name"]}</span><span class="sub">{sub}</span></span></a>')
AZ_JS = """
<script>
(function(){
  var input=document.getElementById('actor-search');
  var rows=[].slice.call(document.querySelectorAll('#az-index [data-n]'));
  var headers=[].slice.call(document.querySelectorAll('#az-index .idx-letter'));
  input.addEventListener('input', function(){
    var q=input.value.trim().toLowerCase();
    rows.forEach(function(r){ r.style.display = (!q || r.dataset.n.indexOf(q)!==-1) ? '' : 'none'; });
    headers.forEach(function(h){
      var next=h.nextElementSibling, show=false;
      while(next && !next.classList.contains('idx-letter')){ if(next.style.display!=='none') show=true; next=next.nextElementSibling; }
      h.style.display = show ? '' : 'none';
    });
  });
})();
</script>
"""
body = f"""
<section class="hero"><div class="inner">
<p class="eyebrow">Directory</p><h1>Actors</h1>
<p class="lede">{len(people):,} people, listed by surname. Only {photo_n} have a photo anywhere we can link to, so most are initials &mdash; the credit list is the useful part anyway.</p>
<form class="aside-search" style="max-width:420px" onsubmit="return false">
<span class="glyph" style="color:var(--wine)">&#8981;</span>
<input type="text" id="actor-search" placeholder="Search actors" autocomplete="off" aria-label="Search actors">
</form>
</div></section>
<section class="az-bar"><div class="az-letters">{az_bar}</div></section>
<section class="pad" style="padding:28px 22px 46px">
<div class="grid az" id="az-index">{"".join(rows_html)}</div>
</section>
{AZ_JS}"""
html = page("Every Vertical Drama Actor, A-Z | DramaEverAfter",
            f"An A-Z directory of {len(people):,} vertical drama actors, with credits and where to watch.",
            body, f"{DOMAIN}/actors/index.html", depth=1)
open(os.path.join(DIST, "actors", "index.html"), "w").write(html)
urls.append("/actors/index.html")

ORIGIN_LABEL = {"english": "English original", "chinese": "Chinese original", "dubbed": "Dubbed release"}

# Title pages
for t in titles:
    sl = tslug(t)
    d, pre = tdir(t), "../" * tdepth(t)
    cast_html = ""
    for c in credits_by_title.get(t["title_id"], []):
        pr = p_by_id.get(c["person_id"])
        if not pr: continue
        role = (c["role"] or "").replace("+", " · ").title() or "Cast"
        n_titles = len(credits_by_person.get(c["person_id"], []))
        cast_html += person_row(pr["name"], f"{role} · {n_titles} titles",
                                 (pr.get("photo_ref") or "").strip(), f"{pre}actors/{pslug(pr)}.html", "md")
    # Set is for the overlap test below only. Anything rendered reads from tropes_of()
    # directly: set order follows Python's per-process string hash, so displaying from
    # it rewrote the "If you liked this" hint on 2,267 pages every rebuild.
    my_tropes = set(tropes_of(t))
    origin_pool = titles_root if origin_of(t) == ROOT_ORIGIN else [x for x in titles_other if origin_of(x) == origin_of(t)]
    similar = sorted([x for x in origin_pool if x["title_id"] != t["title_id"] and my_tropes & set(tropes_of(x))],
                      key=lambda x: -title_views(x))[:10]
    similar_html = "".join(poster_card(x, pre, rail_item=True, size_sm=True) for x in similar)
    trope_html = "".join(trope_chip(tr, pre) for tr in tropes_of(t))
    lang_label = ORIGIN_LABEL.get(origin_of(t), origin_of(t).title())
    v = views_label(title_views(t))
    # Genres are distinct from tropes and are set on 2,306 titles; the source data
    # mixes "romance"/"Romance" so normalise case. Status renders only when it is a
    # real viewer-facing state -- the old page printed the internal "Needs_Check"
    # flag straight into the copy.
    genres = ", ".join(sorted({g.strip().title() for g in (t.get("genres") or "").split(";") if g.strip()}))
    status = (t.get("status") or "").strip().lower()
    status_label = status.title() if status in ("complete", "ongoing") else ""
    views_bits = [x for x in [v, genres, lang_label] if x]
    ep = f"{t['episode_count']} episodes" if t.get("episode_count") else ""
    eyebrow_bits = [x for x in ["Vertical drama", t.get("year"), ep, status_label] if x]
    if t.get("data_confidence") == "needs_check": eyebrow_bits.append("community reported")
    ld = {"@context": "https://schema.org", "@type": "TVSeries", "name": t["primary_title"],
          "description": t["synopsis_short"][:160]}
    body = f"""
<nav class="crumb"><a href="{pre}index.html">Home</a><span>/</span>{f'<a href="{pre}index.html">{origin_of(t).title()}</a><span>/</span>' if d else ''}<span class="current">{t['primary_title']}</span></nav>
<section class="split-hero">
<div class="poster-col">{poster_box(t, title_app(t))}</div>
<div class="info-col">
<p class="eyebrow">{" &middot; ".join(str(x) for x in eyebrow_bits)}</p>
<h1>{t['primary_title']}</h1>
<p class="views-line">{" &middot; ".join(views_bits)}</p>
{f'<p class="book-note"><span aria-hidden="true">&#128214;</span> Based on the novel{" by " + book_of(t) if book_of(t) != "yes" else ""}</p>' if book_of(t) else ''}
<div class="chips" style="margin-bottom:26px">{trope_html}</div>
<div class="watch-card"><p class="label">Where to watch</p>{watch_buttons(t['title_id'], pre)}
<p class="watch-disclosure">Opens the app. We may earn a commission, which is what keeps this database free.</p></div>
<div class="title-actions">
<button class="act-btn" type="button" data-fav="{tslug(t)}" aria-pressed="false">
<span aria-hidden="true">&#9733;</span><span class="act-label">Save to my list</span></button>
<button class="act-btn" type="button" data-share="{DOMAIN}/{d}titles/{tslug(t)}.html" data-share-title="{esc_attr(t['primary_title'])}">
<span aria-hidden="true">&#8599;</span><span class="act-label">Share</span></button>
</div>
{f'<p class="hint" style="margin-top:14px">Also known as: {t["alt_titles"].replace(";", ", ")}</p>' if t.get('alt_titles') else ''}
<div class="story"><h2>The story</h2><p>{t['synopsis_short']}</p></div>
</div>
</section>
{f'<section class="pad" style="padding:34px 22px 36px"><h2 style="font-size:24px;margin-bottom:20px">Cast</h2><div class="grid cast">{cast_html}</div></section>' if cast_html else ''}
{f'''<section class="section-warm" style="padding:30px 0 44px">
<div class="section-head pad"><h2>If you liked this</h2><span class="hint" style="font-size:13.5px;color:var(--tert)">{" &middot; ".join(tropes_of(t)[:2])}</span></div>
<div class="rail">{similar_html}</div>
</section>''' if similar_html else ''}
{FAV_JS}{SHARE_JS}"""
    html = page(f"Where to Watch {t['primary_title']} (2026) | DramaEverAfter",
                f"{t['primary_title']}: where to watch, cast and tropes. Updated {UPDATED}.",
                body, f"{DOMAIN}/{d}titles/{sl}.html", ld, depth=tdepth(t))
    os.makedirs(os.path.join(DIST, d, "titles"), exist_ok=True)
    open(os.path.join(DIST, d, "titles", f"{sl}.html"), "w").write(html)
    urls.append(f"/{d}titles/{sl}.html")

# Trope pages
for tr in all_tropes:
    sl = slug(tr)
    matching = sorted([t for t in titles_root if tr in tropes_of(t)], key=lambda x: -title_views(x))
    pair_counts = defaultdict(int)
    for t in matching:
        for other in tropes_of(t):
            if other != tr: pair_counts[other] += 1
    pair_html = "".join(trope_chip(o, "../", c) for o, c in sorted(pair_counts.items(), key=lambda kv: -kv[1])[:6])
    apps_here = sorted({title_app(t) for t in matching if title_app(t)})
    app_opts = "".join(f'<option value="{slug(a)}">{a}</option>' for a in apps_here)
    shown = matching[:GRID_CAP]
    cards = "".join(poster_card(t, "../") for t in shown)
    more = len(matching) - len(shown)
    count_line = (f'Showing <b>{len(shown)}</b> of {len(matching):,} titles'
                  if more else f'<b>{len(matching):,}</b> titles')
    more_html = (f'<div class="show-more"><a class="btn btn-wine" href="../browse.html?trope={sl}">'
                 f'See all {len(matching):,} on Browse &rarr;</a></div>') if more else ""
    body = f"""
<nav class="crumb"><a href="../tropes/index.html">Tropes</a><span>/</span><span class="current">{trope_heading(tr)}</span></nav>
<section class="hero"><div class="inner">
<p class="eyebrow">Trope</p><h1>{trope_heading(tr)}</h1>
<p class="lede">{len(matching):,} titles carry this trope. Updated {UPDATED}.</p>
{f'<div class="chips" style="align-items:center"><span class="hint" style="font-size:13px;color:var(--tert);margin-right:4px">Often paired with</span>{pair_html}</div>' if pair_html else ''}
</div></section>
<section class="pad" style="padding:24px 22px 46px">
<div class="results-head">
<p class="count">{count_line}</p>
<div style="display:flex;gap:10px;flex-wrap:wrap;align-items:center">
{f'<label class="sort-label">App<select id="trope-app-{sl}" data-app-filter-for="trope-grid" aria-label="Filter by app"><option value="">Any app</option>{app_opts}</select></label>' if app_opts else ''}
{sort_select('trope-grid')}
</div>
</div>
<div class="grid" id="trope-grid">{cards}</div>
{more_html}
</section>
{SORT_JS}{FAV_JS}"""
    html = page(f"Best {trope_heading(tr)} Vertical Dramas (2026) | DramaEverAfter",
                f"Every verified {tr} vertical drama across ReelShort, DramaBox and more. Updated {UPDATED}.",
                body, f"{DOMAIN}/tropes/{sl}.html")
    open(os.path.join(DIST, "tropes", f"{sl}.html"), "w").write(html)
    urls.append(f"/tropes/{sl}.html")

# All-tropes index (NEW): a counted A-Z list, not a chip cloud -- 226 chips is a wall.
trope_total = defaultdict(int)
for t in titles_root:
    for tr in tropes_of(t): trope_total[tr] += 1
tropes_sorted = sorted(all_tropes, key=lambda x: x.lower())
idx_rows, cur_letter = [], ""
for tr in tropes_sorted:
    letter = tr[0].upper()
    if letter != cur_letter:
        cur_letter = letter
        idx_rows.append(f'<h2 class="idx-letter">{letter}</h2>')
    idx_rows.append(f'<a class="trope-idx-row" href="{slug(tr)}.html"><span class="n">{trope_heading(tr)}</span><span class="c">{trope_total[tr]:,}</span></a>')
body = f"""
<section class="hero"><div class="inner">
<p class="eyebrow">Index</p><h1>All {len(all_tropes)} tropes</h1>
<p class="lede">Every tag in the database with a count next to it. If you know what you're in the mood for, start here.</p>
</div></section>
<section class="pad" style="padding:26px 22px 46px">
<div class="grid trope-idx trope-idx">{"".join(idx_rows)}</div>
</section>"""
html = page(f"All {len(all_tropes)} Vertical Drama Tropes | DramaEverAfter",
            f"Every trope in the database, counted. Browse {len(all_tropes)} tropes A to Z.",
            body, f"{DOMAIN}/tropes/index.html")
open(os.path.join(DIST, "tropes", "index.html"), "w").write(html)
urls.append("/tropes/index.html")


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
<nav class="crumb"><a href="{pre}index.html">Home</a><span>/</span><span class="current">Where to Watch {t['primary_title']}</span></nav>
<section class="hero"><div class="inner">
<p class="eyebrow">Where to Watch</p><h1>{t['primary_title']}</h1>
<p class="lede">Checked {UPDATED}</p></div></section>
<section class="pad" style="padding:26px 22px 40px">
<p style="font-size:16px;line-height:1.6;max-width:60ch">{answer}</p>{free_line}
<div class="watch-card" style="margin-top:16px"><p class="label">Where to watch</p>{watch_buttons(t['title_id'], pre)}
<p class="watch-disclosure">We may earn a commission, which is what keeps this database free.</p></div>
<p style="margin-top:16px"><a href="{pre}titles/{sl}.html">Full {t['primary_title']} page: cast, tropes and details &rarr;</a></p>
</section>
<section class="faq"><div class="wrap"><h2>Quick answers</h2>{faq_items}
<p class="note">Spotted it on another app? Report it and help the database grow.</p></div></section>"""
    html = page(f"Where to Watch {t['primary_title']}: All Platforms (2026) | DramaEverAfter",
                f"Where to watch {t['primary_title']}: every platform it streams on, checked {UPDATED}.",
                body, f"{DOMAIN}/{d}where-to-watch/{sl}.html", depth=tdepth(t))
    os.makedirs(os.path.join(DIST, d, "where-to-watch"), exist_ok=True)
    open(os.path.join(DIST, d, "where-to-watch", f"{sl}.html"), "w").write(html)
    urls.append(f"/{d}where-to-watch/{sl}.html")

# Trope x platform combination pages (publish only at 5+ verified titles, per architecture doc)
#
# This used to be a nested scan: for every trope, for every platform, walk all 3,407
# titles. That is 226 x 70 x 3,407 = ~54 million iterations and it dominated the build.
# Indexing titles by trope once, then bucketing that much smaller pool by platform,
# produces exactly the same pages in a fraction of the time.
_verified_root = [t for t in titles_root if t.get("data_confidence", "verified") == "verified"]
titles_by_trope = defaultdict(list)
for _t in _verified_root:
    for _tr in tropes_of(_t):
        titles_by_trope[_tr].append(_t)

for tr in all_tropes:
    pool = titles_by_trope.get(tr, [])
    if len(pool) < 5:
        continue
    by_plat = defaultdict(list)
    for _t in pool:
        # A title can carry several availability rows for one platform; count it once.
        for _pid in {a["platform_id"] for a in avail_by_title.get(_t["title_id"], [])}:
            by_plat[_pid].append(_t)
    for pid, matching in by_plat.items():
        pl = platforms.get(pid)
        if pl is None or len(matching) < 5:
            continue
        trs, pls = slug(tr), slug(pl["name"])
        os.makedirs(os.path.join(DIST, "tropes", trs), exist_ok=True)
        ranked_m = sorted(matching, key=lambda x: -title_views(x))[:GRID_CAP]
        cards = "".join(poster_card(t, "../../", show_app=False) for t in ranked_m)
        body = f"""
<nav class="crumb"><a href="../../index.html">Home</a><span>/</span><a href="../{trs}.html">{trope_heading(tr)}</a><span>/</span><span class="current">{pl['name']}</span></nav>
<section class="hero"><div class="inner">
<p class="eyebrow">Trope &times; Platform</p><h1>Best {trope_heading(tr)} Dramas on {pl['name']}</h1>
<p class="lede">{len(matching)} verified titles. Updated {UPDATED}.</p></div></section>
<section class="pad" style="padding:24px 22px 46px"><div class="grid">{cards}</div></section>"""
        html = page(f"Best {trope_heading(tr)} Vertical Dramas on {pl['name']} (2026) | DramaEverAfter",
                    f"Every verified {tr} vertical drama on {pl['name']}. Updated {UPDATED}.",
                    body, f"{DOMAIN}/tropes/{trs}/{pls}.html", depth=2)
        open(os.path.join(DIST, "tropes", trs, f"{pls}.html"), "w").write(html)
        urls.append(f"/tropes/{trs}/{pls}.html")

# Apps: one NEW per-platform page for every app with real availability data
# (design screen 8), plus platforms.html restyled as the "all apps" index. The
# old pricing/affiliate comparison table is kept as supplementary content below
# the grid rather than deleted -- it isn't part of the ten designed screens, but
# it's real data other pages link to and searches may already rank for.
os.makedirs(os.path.join(DIST, "apps"), exist_ok=True)
for pid, n in TOP_PLATFORMS:
    if n == 0: continue
    pl = platforms[pid]
    pls = slug(pl["name"])
    app_titles = sorted([t for t in titles_root if any(a["platform_id"] == pid for a in avail_by_title.get(t["title_id"], []))],
                         key=lambda x: -title_views(x))
    with_posters = sum(1 for t in app_titles if (t.get("poster_ref") or "").strip())
    origin_tally = defaultdict(int)
    for t in app_titles: origin_tally[origin_of(t)] += 1
    dom_origin = max(origin_tally.items(), key=lambda kv: kv[1])[0] if origin_tally else "english"
    lang_word = {"english": "English", "chinese": "Chinese", "dubbed": "Dubbed"}.get(dom_origin, dom_origin.title())
    actor_tally = defaultdict(int)
    for t in app_titles:
        for c in credits_by_title.get(t["title_id"], []): actor_tally[c["person_id"]] += 1
    regulars = sorted(actor_tally.items(), key=lambda kv: -kv[1])[:8]
    regulars_html = "".join(actor_tile(p_by_id[pid_], "../", "app", on_warm=True) for pid_, _ in regulars if pid_ in p_by_id)
    grid_html = "".join(poster_card(t, "../", show_app=False) for t in app_titles[:10])
    # A button with href="#" looks live and does nothing, which is worse than no
    # button: every app page shipped one of these because web_url was empty for all
    # 15 platforms. Render the CTA only when there is somewhere real to send people.
    web_url = (pl.get("web_url") or "").strip()
    body = f"""
<nav class="crumb"><a href="../platforms.html">Apps</a><span>/</span><span class="current">{pl['name']}</span></nav>
<section class="split-hero">
<div class="info-col">
<p class="eyebrow">App</p><h1>{pl['name']}</h1>
<p class="lede">{len(app_titles):,} titles in the database{f", mostly {lang_word.lower()}" if lang_word else ""}.</p>
<div class="stat-figures">
<div class="stat"><span class="n">{len(app_titles):,}</span><span class="l">titles</span></div>
<div class="divider"></div>
<div class="stat"><span class="n">{with_posters:,}</span><span class="l">with posters</span></div>
<div class="divider"></div>
<div class="stat"><span class="n">{lang_word}</span><span class="l">mostly original</span></div>
</div>
</div>
<div class="app-cta"><p class="label">Get the app</p>
{f'<a class="watch-btn" href="{esc_attr(web_url)}"><span>Open {pl["name"]}</span><span class="arrow">&rarr;</span></a>' if web_url else f'<p class="watch-pending">No public web link on file for {pl["name"]}</p>'}
<p class="watch-disclosure">Pricing: {pl.get('pricing_model') or 'varies by title'}.{' We may earn a commission &mdash; that&rsquo;s what pays for this database.' if web_url else ''}</p>
</div>
</section>
<section class="pad" style="padding:30px 22px 20px">
<div class="section-head"><h2>Most watched on {pl['name']}</h2><a class="all" href="../tropes/index.html">Browse by trope &rarr;</a></div>
<div class="grid">{grid_html}</div>
</section>
{f'''<section class="section-warm" style="padding:28px 0 44px;margin-top:26px">
<div class="pad"><h2 style="margin-bottom:20px">Regulars on this app</h2><div class="grid circles">{regulars_html}</div></div>
</section>''' if regulars_html else ''}"""
    html = page(f"{pl['name']}: Titles, Pricing and Where to Start (2026) | DramaEverAfter",
                f"{pl['name']} on DramaEverAfter: {len(app_titles):,} titles, regulars, and how to get started.",
                body, f"{DOMAIN}/apps/{pls}.html", depth=1)
    open(os.path.join(DIST, "apps", f"{pls}.html"), "w").write(html)
    urls.append(f"/apps/{pls}.html")

# Platforms page -> "all apps" index
app_tiles = "".join(
    f'<a class="app-tile" href="apps/{slug(platforms[pid]["name"])}.html"><span class="n">{platforms[pid]["name"]}</span><span class="c">{n:,} titles</span></a>'
    for pid, n in TOP_PLATFORMS if n > 0)
prows = ""
for p in platforms.values():
    aff = "Yes" if p["affiliate_program"].upper().startswith("YES") else "TBC"
    prows += f"<tr><td><b>{p['name']}</b></td><td>{p['pricing_model']}</td><td>{aff}</td></tr>"
body = f"""
<nav class="crumb"><a href="index.html">Home</a><span>/</span><span class="current">Apps</span></nav>
<section class="hero"><div class="inner"><p class="eyebrow">Guide</p><h1>Every vertical drama app</h1>
<p class="lede">{len(APPS_WITH_DATA)} apps with verified catalogues, {len(platforms)} tracked in all. Updated {UPDATED}.</p></div></section>
<section class="pad" style="padding:34px 22px 40px"><div class="grid apps">{app_tiles}</div></section>
<section class="section-warm pad" style="padding:34px 22px 44px">
<h2 style="margin-bottom:16px">Compare pricing</h2>
<table><tr><th>Platform</th><th>Pricing</th><th>Referral links</th></tr>{prows}</table>
</section>"""
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
        if slug(x): trope_label.setdefault(slug(x), trope_heading(x))
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
    if is_ai(t): entry["ai"] = 1
    if book_of(t): entry["bk"] = 1
    if is_upcoming(t): entry["up"] = 1
    v = title_views(t)
    if v: entry["v"] = v
    img = (t.get("poster_ref") or "").strip()
    if img: entry["i"] = img
    search_titles.append(entry)

open(os.path.join(DIST, "search-index.json"), "w").write(
    json.dumps({"actors": search_actors, "titles": search_titles}, separators=(",", ":")))

VISIBLE = 14  # chips shown before "show all N" disclosure, per design ("14 most common of 226")

def facet_chips(group, counts, labels):
    out = []
    ordered = sorted(counts.items(), key=lambda kv: (-kv[1], labels.get(kv[0], kv[0])))
    for i, (s, _n) in enumerate(ordered):
        extra = " extra" if i >= VISIBLE else ""
        out.append('<button class="chip%s" data-g="%s" data-v="%s" type="button" aria-pressed="false">%s<span class="c"></span></button>'
                   % (extra, group, s, labels.get(s, s)))
    return "".join(out), len(ordered)

# Origin facet. Buckets Cyan wants exposed are declared up front, not derived from the
# data, so the filter shows the full shape of the taxonomy even while a bucket is empty.
# An empty bucket renders greyed out and disabled, same as any other zero-match chip.
ORIGIN_BUCKETS = [("english", "English"), ("chinese", "Chinese"), ("dubbed", "Dubbed")]
origin_counts = defaultdict(int)
for t in titles_root: origin_counts[origin_of(t)] += 1
origin_facets = "".join(
    '<button class="chip" data-g="origin" data-v="%s" type="button" aria-pressed="false">%s<span class="c"></span></button>' % (v, lbl)
    for v, lbl in ORIGIN_BUCKETS)

trope_facets, n_tropes = facet_chips("trope", trope_counts, trope_label)
platform_facets, n_platforms = facet_chips("platform", platform_counts, platform_label)
trope_more = ('<button class="chip-dashed" data-target="f-trope" type="button">Show all %d tropes &#9662;</button>' % n_tropes) if n_tropes > VISIBLE else ""
platform_more = ('<button class="chip-dashed" data-target="f-platform" type="button">Show all %d apps &#9662;</button>' % n_platforms) if n_platforms > VISIBLE else ""

BROWSE_JS = f"""
<script>
(function(){{
  var D=null, STEP=24, visibleCount=STEP, lastTitles=[];
  var PLABEL={json.dumps(platform_label, separators=(',', ':'))};
  var APPPAGE={json.dumps({slug(p["name"]): 1 for p in APPS_WITH_DATA}, separators=(',', ':'))};
  var TLABEL={json.dumps(trope_label, separators=(',', ':'))};
  var FIELD={{trope:'tr', platform:'pl', origin:'o'}};
  var active={{}};
  var qEl=document.getElementById('q'), sortEl=document.getElementById('f-sort');
  var titlesOut=document.getElementById('results-titles'), actorsOut=document.getElementById('results-actors');
  var countEl=document.getElementById('result-count'), resetEl=document.getElementById('f-reset');
  var moreBtn=document.getElementById('f-more'), moreWrap=document.getElementById('f-more-wrap');
  var chips=[].slice.call(document.querySelectorAll('.chip[data-g]'));
  chips.forEach(function(c){{ if(!active[c.dataset.g]) active[c.dataset.g]=new Set(); }});

  function esc(s){{return String(s==null?'':s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/"/g,'&quot;');}}
  function has(arr,v){{return arr && arr.indexOf(v)!==-1;}}
  function vlabel(n){{
    if(!n) return '';
    if(n>=1e9) return (n/1e9).toFixed(1)+'B views';
    if(n>=1e6) return Math.round(n/1e6)+'M views';
    if(n>=1e3) return Math.round(n/1e3)+'K views';
    return '';
  }}
  function posterCard(t){{
    var appName=(t.pl && t.pl[0] && PLABEL[t.pl[0]]) || '';
    var plate='<span class="poster--empty"><span class="label">No poster</span><span class="ttl">'+esc(t.n)+'</span><span class="app">'+esc(appName)+'</span></span>';
    var img=t.i ? '<img src="'+esc(t.i)+'" alt="'+esc(t.n)+'" loading="lazy" onerror="this.remove()">' : '';
    var bits=[]; var vl=vlabel(t.v); if(vl) bits.push(vl); if(t.tr && t.tr[0]) bits.push(TLABEL[t.tr[0]]||t.tr[0]);
    // Mirrors poster_card() in build.py: wrapper div, poster and caption link to the
    // title, app name links to that app's page. Anchors cannot nest.
    var appHtml='';
    if(appName){{
      appHtml = APPPAGE[t.pl[0]]
        ? '<a class="app-name" href="apps/'+esc(t.pl[0])+'.html">'+esc(appName)+'</a>'
        : '<span class="app-name">'+esc(appName)+'</span>';
    }}
    var href='titles/'+esc(t.s)+'.html';
    // Badges must mirror poster_box() in build.py. They were missing here, so a title
    // shown by UNchecking "hide AI" (or "hide unreleased") rendered with no marking at
    // all: the filter hid it, and the moment you asked to see it the warning vanished.
    var badge=(t.ai?'<span class="ai-badge" title="AI-generated">AI</span>':'')+
              (t.up?'<span class="soon-badge" title="Not released yet">SOON</span>':'');
    return '<div class="poster-card"><a class="poster-link" href="'+href+'"><span class="poster">'+plate+img+badge+
      '</span></a><button class="fav-btn" type="button" data-fav="'+esc(t.s)+'" aria-pressed="false" '+
      'aria-label="Save to my list"><span aria-hidden="true">&#9733;</span></button>'+appHtml+
      '<a class="meta" href="'+href+'">'+esc(bits.join(' \\u00b7 '))+'</a></div>';
  }}
  function actorCard(a){{
    var initials=a.n.split(' ').map(function(w){{return w.charAt(0).toUpperCase();}}).slice(0,2).join('');
    var img=a.i ? '<img src="'+esc(a.i)+'" alt="" loading="lazy" onerror="this.remove()">' : '';
    return '<a class="actor-tile" href="actors/'+esc(a.s)+'.html"><span class="ring ring--rail"><span>'+esc(initials)+'</span>'+img+'</span>'+
      '<span class="stack"><span class="name">'+esc(a.n)+'</span><span class="sub">'+a.c+' titles</span></span></a>';
  }}

  var onlyBookEl=document.getElementById('only-book');
  var hideAiEl=document.getElementById('hide-ai');
  var hideSoonEl=document.getElementById('hide-upcoming');
  // Default is to HIDE AI titles; the choice is remembered between visits.
  try{{ var saved=localStorage.getItem('dea_hide_ai'); if(saved!==null) hideAiEl.checked=(saved==='1'); }}catch(e){{}}
  // Same for unreleased titles: a search here means "what can I watch", so they
  // are out by default and opting in is one click.
  try{{ var su=localStorage.getItem('dea_hide_upcoming'); if(su!==null) hideSoonEl.checked=(su==='1'); }}catch(e){{}}

  function matches(t,q){{
    if(hideAiEl.checked && t.ai) return false;
    if(hideSoonEl.checked && t.up) return false;
    if(onlyBookEl.checked && !t.bk) return false;
    if(q && t.n.toLowerCase().indexOf(q)===-1) return false;
    for(var g in active){{
      var f=t[FIELD[g]], it=active[g].values(), x;
      while(!(x=it.next()).done){{ if(!has(f,x.value)) return false; }}
    }}
    return true;
  }}

  function renderTitles(){{
    var slice=lastTitles.slice(0,visibleCount);
    titlesOut.innerHTML=slice.map(posterCard).join('') || '<p class="no-results">No titles match. Try removing a filter.</p>';
    moreWrap.style.display = lastTitles.length>visibleCount ? '' : 'none';
    if(window.deaWireFavs) window.deaWireFavs(titlesOut);
  }}

  function run(){{
    if(!D) return;
    visibleCount=STEP;
    var q=qEl.value.trim().toLowerCase();
    var titles=D.titles.filter(function(t){{return matches(t,q);}});

    // Single pass over the current result set tallies every chip at once, so each
    // chip's number is "results you'd get if you also picked this".
    var tally={{}}; for(var g in active) tally[g]={{}};
    for(var i=0;i<titles.length;i++){{
      var t=titles[i];
      for(var g2 in active){{
        var f=t[FIELD[g2]]; if(!f) continue;
        for(var j=0;j<f.length;j++) tally[g2][f[j]]=(tally[g2][f[j]]||0)+1;
      }}
    }}
    for(var c=0;c<chips.length;c++){{
      var el=chips[c], g=el.dataset.g, v=el.dataset.v, n=tally[g][v]||0, on=active[g].has(v);
      el.querySelector('.c').textContent=n.toLocaleString();
      el.className=(el.className.indexOf('extra')!==-1?'chip extra':'chip')+(on?' on':(n?'':' off'));
      el.disabled=(!n && !on);
      el.setAttribute('aria-pressed', on ? 'true' : 'false');
      el.setAttribute('aria-disabled', (!n && !on) ? 'true' : 'false');
    }}

    var sort=sortEl.value;
    if(sort==='views') titles.sort(function(a,b){{return (b.v||0)-(a.v||0);}});
    else if(sort==='az') titles.sort(function(a,b){{return a.n.localeCompare(b.n);}});
    else if(sort==='year') titles.sort(function(a,b){{return String(b.y||'').localeCompare(String(a.y||''));}});
    lastTitles=titles;

    var actors=D.actors.filter(function(a){{return !q || a.n.toLowerCase().indexOf(q)!==-1;}});
    actors.sort(function(a,b){{return b.c-a.c;}});

    var nf=0; for(var g3 in active) nf+=active[g3].size;
    resetEl.style.display=(nf||q)?'inline-block':'none';
    countEl.innerHTML='<b>'+titles.length.toLocaleString()+'</b> titles'+(q?', '+actors.length.toLocaleString()+' actors':'');
    document.getElementById('active-summary').textContent = (nf||q) ? ((nf?nf+' filter'+(nf>1?'s':'')+' on':'')+(nf&&q?', ':'')+(q?'searching \\"'+q+'\\"':'')) : 'No filters yet \\u2014 showing everything';

    renderTitles();
    if(window.deaWireFavs) window.deaWireFavs(titlesOut);

    if(q){{
      actorsOut.innerHTML=actors.slice(0,24).map(actorCard).join('') || '<p class="no-results">No actors match.</p>';
      actorsOut.parentNode.style.display='';
    }} else {{
      actorsOut.parentNode.style.display='none';
    }}
  }}

  chips.forEach(function(el){{
    el.addEventListener('click',function(){{
      if(el.disabled) return;
      var g=el.dataset.g,v=el.dataset.v;
      if(active[g].has(v)) active[g].delete(v); else active[g].add(v);
      run();
    }});
  }});
  [].slice.call(document.querySelectorAll('.chip-dashed')).forEach(function(b){{
    b.addEventListener('click',function(){{
      var box=document.getElementById(b.dataset.target);
      var collapsed=box.classList.toggle('collapsed');
      b.innerHTML=collapsed?b.dataset.moreLabel:'Show fewer &#9652;';
    }});
  }});
  moreBtn.addEventListener('click',function(){{ visibleCount+=STEP; renderTitles(); }});

  var timer=null;
  qEl.addEventListener('input',function(){{clearTimeout(timer);timer=setTimeout(run,120);}});
  sortEl.addEventListener('change',run);
  onlyBookEl.addEventListener('change', run);
  hideAiEl.addEventListener('change',function(){{
    try{{ localStorage.setItem('dea_hide_ai', hideAiEl.checked?'1':'0'); }}catch(e){{}}
    run();
  }});
  hideSoonEl.addEventListener('change',function(){{
    try{{ localStorage.setItem('dea_hide_upcoming', hideSoonEl.checked?'1':'0'); }}catch(e){{}}
    run();
  }});
  resetEl.addEventListener('click',function(){{
    for(var g in active) active[g].clear(); qEl.value=''; run();
  }});

  fetch('search-index.json').then(function(r){{return r.json();}}).then(function(d){{
    D=d;
    var p=new URLSearchParams(window.location.search);
    if(p.get('q')) qEl.value=p.get('q');
    ['trope','platform','origin'].forEach(function(g){{
      if(p.get(g) && active[g]) active[g].add(p.get(g));
    }});
    run();
  }}).catch(function(){{ countEl.textContent='Could not load the index. Please refresh.'; }});
}})();
</script>
"""

browse_body = f"""
<div class="browse-layout">
<aside class="browse-aside">
<h1>Browse titles</h1>
<form class="aside-search" onsubmit="return false">
<span class="glyph" style="color:var(--wine)">&#8981;</span>
<input type="text" id="q" placeholder="Search within results" autocomplete="off" aria-label="Search within results">
</form>
<div class="active-filters">
<span class="txt" id="active-summary">No filters yet &mdash; showing everything</span>
<button class="reset-pill" id="f-reset" type="button" style="display:none">Reset</button>
</div>
<div class="filter-group">
<h2>Country of origin</h2><p class="hint">Pick one</p>
<div class="chips tight" id="f-origin">{origin_facets}</div>
</div>
<div class="filter-group">
<h2>Trope</h2><p class="hint">{VISIBLE} most common of {n_tropes}</p>
<div class="chips tight collapsed" id="f-trope">{trope_facets}</div>{trope_more}
</div>
<div class="filter-group">
<h2>App</h2><p class="hint">{VISIBLE if n_platforms > VISIBLE else n_platforms} of {n_platforms} shown</p>
<div class="chips tight collapsed" id="f-platform">{platform_facets}</div>{platform_more}
<p class="hint" style="margin-top:14px">Greyed chips would return nothing with your current picks. They stay put so the panel never jumps.</p>
</div>
<label class="ai-toggle" for="only-book">
<input type="checkbox" id="only-book">
<span>Only titles based on a book</span>
</label>
<label class="ai-toggle" for="hide-ai">
<input type="checkbox" id="hide-ai" checked>
<span>Hide AI-generated titles</span>
</label>
<label class="ai-toggle" for="hide-upcoming">
<input type="checkbox" id="hide-upcoming" checked>
<span>Hide titles not out yet</span>
</label>
</aside>
<section class="results-panel">
<div class="results-head">
<p class="count" id="result-count">Loading&hellip;</p>
<label class="sort-label">Sort<select id="f-sort" aria-label="Sort titles">
<option value="views">Most watched</option>
<option value="az">A&ndash;Z</option>
<option value="year">Newest first</option>
</select></label>
</div>
<div class="grid" id="results-titles"></div>
<div class="show-more" id="f-more-wrap" style="display:none"><button class="btn btn-wine" id="f-more" type="button">Show 24 more</button></div>
</section>
</div>
<section class="section-warm pad" id="results-actors-section" style="display:none;padding:34px 22px 40px">
<h2 style="margin-bottom:18px">Actors</h2><div class="grid circles" id="results-actors"></div>
</section>
{FAV_JS}{BROWSE_JS}"""
html = page("Search DramaEverAfter: Every Actor and Title (2026) | DramaEverAfter",
            f"Search and filter {len(people)} vertical drama actors and {len(titles_root)} titles by trope and platform.",
            browse_body, f"{DOMAIN}/browse.html", depth=0)
open(os.path.join(DIST, "browse.html"), "w").write(html)
urls.append("/browse.html")

# My List. Renders entirely from localStorage + the existing search index, so the
# page itself is static and personal to whoever opens it. No account, no server.
MYLIST_JS = """
<script>
(function(){
  var out=document.getElementById('mylist-grid'), empty=document.getElementById('mylist-empty'),
      countEl=document.getElementById('mylist-count'), clearBtn=document.getElementById('mylist-clear'),
      copyBtn=document.getElementById('mylist-copy'), noteEl=document.getElementById('mylist-note');
  var lastPicked=[];
  var PLABEL=%(plabel)s, TLABEL=%(tlabel)s, APPPAGE=%(apppage)s, D=null;
  function esc(s){return String(s==null?'':s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/"/g,'&quot;');}
  function vlabel(n){ if(!n) return '';
    if(n>=1e9) return (n/1e9).toFixed(1)+'B views';
    if(n>=1e6) return Math.round(n/1e6)+'M views';
    if(n>=1e3) return Math.round(n/1e3)+'K views'; return ''; }
  function card(t){
    var app=(t.pl&&t.pl[0]&&PLABEL[t.pl[0]])||'';
    var plate='<span class="poster--empty"><span class="label">No poster</span><span class="ttl">'+esc(t.n)+
      '</span><span class="app">'+esc(app)+'</span></span>';
    var img=t.i?'<img src="'+esc(t.i)+'" alt="'+esc(t.n)+'" loading="lazy" onerror="this.remove()">':'';
    var bits=[]; var vl=vlabel(t.v); if(vl) bits.push(vl); if(t.tr&&t.tr[0]) bits.push(TLABEL[t.tr[0]]||t.tr[0]);
    var appHtml = app ? (APPPAGE[t.pl[0]]
      ? '<a class="app-name" href="apps/'+esc(t.pl[0])+'.html">'+esc(app)+'</a>'
      : '<span class="app-name">'+esc(app)+'</span>') : '';
    var href='titles/'+esc(t.s)+'.html';
    // Badges must mirror poster_box() in build.py. They were missing here, so a title
    // shown by UNchecking "hide AI" (or "hide unreleased") rendered with no marking at
    // all: the filter hid it, and the moment you asked to see it the warning vanished.
    var badge=(t.ai?'<span class="ai-badge" title="AI-generated">AI</span>':'')+
              (t.up?'<span class="soon-badge" title="Not released yet">SOON</span>':'');
    return '<div class="poster-card"><a class="poster-link" href="'+href+'"><span class="poster">'+plate+img+badge+
      '</span></a><button class="fav-btn" type="button" data-fav="'+esc(t.s)+'" aria-pressed="false" '+
      'aria-label="Remove from my list"><span aria-hidden="true">&#9733;</span></button>'+appHtml+
      '<a class="meta" href="'+href+'">'+esc(bits.join(' · '))+'</a></div>';
  }
  function render(){
    if(!D) return;
    var favs=window.deaFavs.read();
    var picked=D.titles.filter(function(t){ return favs.indexOf(t.s)!==-1; });
    countEl.textContent = picked.length ? picked.length+(picked.length===1?' drama':' dramas')+' saved' : '';
    clearBtn.style.display = picked.length ? 'inline-flex' : 'none';
    copyBtn.style.display = picked.length ? 'inline-flex' : 'none';
    noteEl.style.display = picked.length ? '' : 'none';
    lastPicked = picked;
    if(!picked.length){ out.innerHTML=''; empty.style.display=''; return; }
    empty.style.display='none';
    out.innerHTML = picked.map(card).join('');
    window.deaWireFavs(out);
  }
  window.deaOnFavChange = render;
  function asText(){
    var lines=['My DramaEverAfter list', ''];
    lastPicked.forEach(function(t,i){
      var app=(t.pl&&t.pl[0]&&PLABEL[t.pl[0]])||'';
      lines.push((i+1)+'. '+t.n+(app?'  ('+app+')':''));
      lines.push('   %(domain)s/titles/'+t.s+'.html');
      lines.push('');
    });
    lines.push('Saved from %(domain)s');
    // fromCharCode(10) rather than a backslash-n literal: this JS is generated from a
    // Python string, so an escape sequence here has to survive both layers intact. It
    // did not, and the literal newline it produced was a JS syntax error that killed
    // the whole script silently -- the page built fine and rendered nothing.
    return lines.join(String.fromCharCode(10));
  }
  copyBtn.addEventListener('click', function(){
    var txt=asText(), lbl=copyBtn.querySelector('.act-label');
    var ok=function(){ var o=lbl.textContent; lbl.textContent='Copied'; setTimeout(function(){ lbl.textContent=o; },1800); };
    if(navigator.clipboard && navigator.clipboard.writeText){
      navigator.clipboard.writeText(txt).then(ok).catch(function(){ window.prompt('Copy your list:', txt); });
    } else { window.prompt('Copy your list:', txt); }
  });
  clearBtn.addEventListener('click', function(){
    if(!window.confirm('Remove every drama from your list? This cannot be undone.')) return;
    try{ localStorage.setItem(window.deaFavs.KEY,'[]'); }catch(e){}
    render();
  });
  fetch('search-index.json').then(function(r){return r.json();}).then(function(d){ D=d; render(); })
    .catch(function(){ empty.style.display=''; });
})();
</script>
""" % {"domain": DOMAIN, "plabel": json.dumps(platform_label, separators=(",", ":")),
        "tlabel": json.dumps(trope_label, separators=(",", ":")),
        "apppage": json.dumps({slug(p["name"]): 1 for p in APPS_WITH_DATA}, separators=(",", ":"))}

mylist_body = f"""
<section class="hero"><div class="inner">
<p class="eyebrow">Your list</p><h1>Dramas you saved</h1>
<p class="lede">Star anything on the site and it lands here. No account, no sign-up,
and nothing is sent anywhere &mdash; your list stays in this browser.</p>
<p id="mylist-count" style="font-size:15px;color:var(--sec)"></p>
</div></section>
<section class="pad" style="padding:26px 22px 46px">
<div id="mylist-empty" class="mylist-empty" style="display:none">
<h3>Nothing saved yet</h3>
<p>Tap the star on any drama and it will show up here.</p>
<p style="margin-top:16px"><a class="btn btn-wine" href="browse.html">Browse dramas &rarr;</a></p>
</div>
<div class="mylist-actions">
<button class="act-btn" id="mylist-copy" type="button" style="display:none">
<span aria-hidden="true">&#128203;</span><span class="act-label">Copy my list</span></button>
<button class="act-btn" id="mylist-clear" type="button" style="display:none">Clear my list</button>
</div>
<p id="mylist-note" class="hint" style="display:none;margin:12px 0 26px;font-size:13px;color:var(--tert)">
Tip: copy your list to keep it if you switch devices.</p>
<div class="grid" id="mylist-grid"></div>
</section>
{FAV_JS}{MYLIST_JS}"""
html = page("My List | DramaEverAfter",
            "The dramas you have saved, kept in your own browser.",
            mylist_body, f"{DOMAIN}/my-list.html", depth=0)
open(os.path.join(DIST, "my-list.html"), "w").write(html)
urls.append("/my-list.html")


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
    cards = "".join(poster_card(t, "") for t in o_titles)
    body = f"""
<nav class="crumb"><a href="../index.html">Home</a><span>/</span><span class="current">{heading}</span></nav>
<section class="hero"><div class="inner">
<p class="eyebrow">Section</p><h1>{heading}</h1>
<p class="lede">{blurb}</p>
<div class="stat-line"><b>{len(o_titles):,}</b> titles</div>
</div></section>
<section class="pad" style="padding:26px 22px 46px"><div class="grid">{cards}</div></section>"""
    html = page(f"{heading} | DramaEverAfter",
                f"{heading}: titles, cast and where to watch. Updated {UPDATED}.",
                body, f"{DOMAIN}/{o}/index.html", depth=1)
    os.makedirs(os.path.join(DIST, o), exist_ok=True)
    open(os.path.join(DIST, o, "index.html"), "w").write(html)
    urls.append(f"/{o}/index.html")

# Homepage
top_actors = sorted(people, key=lambda p: -len(credits_by_person.get(p["person_id"], [])))[:18]

# Straight "most watched" returned 9 ReelShort cards out of 9, because ReelShort
# reports much larger view counts than anyone else. That misrepresents a catalogue
# that is actually 1,821 GoodShort to 573 ReelShort, and buries every other app.
# Take each platform's best titles in turn so the rail reads as a cross-section.
def spread_by_platform(pool, limit, per_platform=2, key=None):
    key = key or (lambda t: -title_views(t))
    buckets = defaultdict(list)
    for t in sorted(pool, key=key):
        buckets[title_app(t) or "?"].append(t)
    order = sorted(buckets, key=lambda k: -len(buckets[k]))
    out, round_i = [], 0
    while len(out) < limit and round_i < per_platform:
        added = False
        for name in order:
            if len(buckets[name]) > round_i:
                out.append(buckets[name][round_i]); added = True
                if len(out) >= limit: break
        if not added: break
        round_i += 1
    return out

# Only GoodShort and ReelShort report view counts at all, so a "most watched" rail can
# only ever honestly cover those two. Spread within them rather than letting ReelShort's
# larger numbers take every slot.
featured = spread_by_platform([t for t in titles_root if title_views(t)], 12, per_platform=6)

# The variety rail. Every app that has artwork gets representation here, ranked by views
# where we have them and by recency where we do not -- which is why it is NOT labelled
# "most watched": we have no view data for five of these seven apps.
_with_art = [t for t in titles_root if (t.get("poster_ref") or "").strip()]
across_apps = spread_by_platform(
    _with_art, 14, per_platform=2,
    key=lambda t: (-title_views(t), (t.get("last_verified") or "")))

# NEW RELEASES. This used to sort on last_verified, which is 2026-07 for all 3,407
# rows because the catalogue was scraped in one pass -- so the old "Just added" rail
# was effectively arbitrary. `year` is the only genuine release signal we hold (no
# release-date column exists), so this is titles from the current year, newest year
# first, ranked by views where we have them. Artwork is required so the rail is not a
# wall of blank plates.
_year_now = int(UPDATED.split()[-1]) if UPDATED.split()[-1].isdigit() else 2026
def _release_year(t):
    y = (t.get("year") or "").strip()
    return int(y) if y.isdigit() else 0
_with_art_dated = [t for t in titles_root
                   if (t.get("poster_ref") or "").strip() and _release_year(t) >= _year_now - 1]
new_releases = sorted(_with_art_dated,
                      key=lambda t: (-_release_year(t), -title_views(t)))[:12]

home_apps = "".join(
    f'<a class="app-tile" href="apps/{slug(platforms[pid]["name"])}.html"><span class="n">{platforms[pid]["name"]}</span><span class="c">{n:,} titles</span></a>'
    for pid, n in TOP_PLATFORMS[:6] if n > 0)

home_tropes = sorted(all_tropes, key=lambda x: -trope_total[x])[:14]
home_trope_chips = "".join(trope_chip(tr, "", trope_total[tr]) for tr in home_tropes)

section_links = "".join(
    f'<section class="pad" style="padding:10px 22px 28px"><h2 style="font-size:20px;margin-bottom:6px">{ORIGIN_BLURB.get(o, (o.title() + " Short Drama", ""))[0]}</h2>'
    f'<a href="{o}/index.html">Browse the catalogue &rarr;</a></section>'
    for o in origins_other)

body = f"""
<section class="hero"><div class="inner">
<p class="eyebrow">Looking for that app? that actor? that drama?</p>
<h1>All the Drama Ever After. Find it. Watch it. Love it.</h1>
<p class="lede">Every micro-drama we can find, the cast behind it, and the one app it actually streams on. No account, no algorithm, no autoplay.</p>
<form class="hero-search-form" action="browse.html" method="get">
<input type="search" name="q" placeholder="e.g. Silver Fox, or Sarah Moliski" aria-label="Search actors or titles">
<button class="btn btn-gold" type="submit">Search</button>
</form>
<div class="stat-line">
<span><b>{len(titles_root):,}</b> titles</span><span class="dot">&middot;</span>
<span><b>{len(people):,}</b> actors</span><span class="dot">&middot;</span>
<span><b>{len(APPS_WITH_DATA)}</b> apps</span>
</div>
</div></section>

<section style="padding:40px 0 8px">
<div class="section-head pad"><h2>Most watched right now</h2><a class="all" href="browse.html">All titles &rarr;</a></div>
<div class="rail">{"".join(poster_card(t, "", rail_item=True) for t in featured)}</div>
</section>

<section style="padding:8px 0 8px">
<div class="section-head pad"><h2>Across every app</h2><a class="all" href="platforms.html">All {len(APPS_WITH_DATA)} apps &rarr;</a></div>
<div class="rail">{"".join(poster_card(t, "", rail_item=True, size_sm=True) for t in across_apps)}</div>
</section>

<section class="section-warm pad" style="padding:34px 22px 40px">
<h2 style="margin-bottom:6px">Browse by trope</h2>
<p style="font-size:15px;color:var(--sec);margin-bottom:20px">The shortcut most people actually use. {len(all_tropes)} in all.</p>
<div class="chips">{home_trope_chips}<a class="chip-all" href="tropes/index.html">All {len(all_tropes)} tropes &rarr;</a></div>
</section>

<section class="pad" style="padding:38px 22px 40px">
<h2 style="margin-bottom:20px">Where these stream</h2>
<div class="grid apps">{home_apps}</div>
</section>

<section class="pad" style="padding:34px 22px 46px;border-top:1px solid var(--line)">
<div class="section-head"><h2>Faces you keep seeing</h2><a class="all" href="actors/index.html">All actors &rarr;</a></div>
<div class="grid circles">{"".join(actor_tile(p, "") for p in top_actors)}</div>
</section>

<section class="section-warm pad" style="padding:30px 22px 44px">
<div class="section-head"><h2>New releases</h2><a class="all" href="browse.html?sort=year">Browse by newest &rarr;</a></div>
<div class="rail" style="padding:0">{"".join(poster_card(t, "", rail_item=True, size_sm=True) for t in new_releases)}</div>
</section>
{section_links}
{FAV_JS}"""
html = page("DramaEverAfter: Every Vertical Drama, Every Platform, One Place",
            "The searchable database of vertical dramas and micro dramas: actors, tropes, and where to watch across ReelShort, DramaBox, ShortMax and more.",
            body, f"{DOMAIN}/", depth=0)
open(os.path.join(DIST, "index.html"), "w").write(html)
urls.insert(0, "/")

# Blog (NEW): template + layout only. No posts.csv exists yet, so this renders an
# honest empty state rather than fabricated content. Linked from nav/footer now so
# the URL is stable; drop real posts in later with no template change needed.
body = f"""
<section class="hero"><div class="inner">
<p class="eyebrow">Reading room</p>
<h1 style="max-width:24ch">What to watch next, and why it's everywhere</h1>
<p class="lede">Recaps, trope explainers and app comparisons. Nothing published yet &mdash; check back soon.</p>
</div></section>
<section class="pad" style="padding:34px 22px 46px;display:flex;flex-wrap:wrap;gap:34px;align-items:flex-start">
<div style="flex:3 1 480px;min-width:0">
<h2 style="margin-bottom:16px">Latest</h2>
<div class="blog-empty"><h3>No posts yet</h3><p>The first recap is being written. Check back soon, or follow along elsewhere.</p></div>
</div>
<aside class="contact-side" style="flex:1 1 250px">
<div class="newsletter-block">
<h2 style="font-size:20px;margin-bottom:8px">One email a week</h2>
<p>The new titles worth your evening, plus whatever I got sucked into. No sponsored fluff.</p>
<form onsubmit="return false">
<input type="email" placeholder="you@email.com" aria-label="Email address">
<button class="btn btn-gold" type="button" style="width:100%">Sign me up</button>
</form>
</div>
</aside>
</section>"""
html = page("The DramaEverAfter Blog: Recaps, Trope Explainers and App Comparisons",
            "Vertical drama recaps, trope explainers and app comparisons from DramaEverAfter.",
            body, f"{DOMAIN}/blog.html", depth=0)
open(os.path.join(DIST, "blog.html"), "w").write(html)
urls.append("/blog.html")

# Contact (NEW): reason-chooser form is fully interactive client-side (pure
# presentation, no network call) -- only the actual submission is left unwired,
# per the go-ahead to ship UI only for now.
CONTACT_JS = """
<script>
(function(){
  var REASONS = {
    correction: {label:'Which page is wrong?', hint:'A title, actor or app page. A link is even better.', ph:'What should it say instead?'},
    missing: {label:'Title and app', hint:'The exact name as it appears in the app, please \\u2014 spelling varies.', ph:'Anything else you know \\u2014 year, lead actors, episode count.'},
    photo: {label:'Which page is wrong?', hint:'A title, actor or app page. A link is even better.', ph:"Tell me which credits are yours and what you'd like the profile to say."},
    other: {label:'Which page is wrong?', hint:'A title, actor or app page. A link is even better.', ph:'Tell me what\\'s going on.'}
  };
  var pills=[].slice.call(document.querySelectorAll('.reason-pill'));
  var titleField=document.getElementById('title-field'), titleLabel=document.getElementById('title-field-label'),
      titleHint=document.getElementById('title-field-hint'), msg=document.getElementById('message-field');
  function select(id){
    pills.forEach(function(p){ var on=p.dataset.reason===id; p.classList.toggle('on', on); p.setAttribute('aria-pressed', on?'true':'false'); });
    var r=REASONS[id];
    titleField.style.display = (id==='correction' || id==='missing') ? '' : 'none';
    titleLabel.textContent = r.label; titleHint.textContent = r.hint; msg.placeholder = r.ph;
  }
  pills.forEach(function(p){ p.addEventListener('click', function(){ select(p.dataset.reason); }); });
  select('correction');
})();
</script>
"""
body = f"""
<section class="hero"><div class="inner">
<p class="eyebrow">Contact</p>
<h1 style="max-width:22ch">Found a mistake? Tell me.</h1>
<p class="lede">This database is assembled from app catalogues, so names get misspelled and posters go missing. Corrections are the single most useful thing you can send me.</p>
</div></section>
<section class="pad" style="padding:34px 22px 46px;display:flex;flex-wrap:wrap;gap:34px;align-items:flex-start">
<form style="flex:2 1 420px;min-width:0;display:flex;flex-direction:column;gap:20px" onsubmit="return false">
<div class="field">
<label>What's this about?</label>
<div class="chips tight" role="group" aria-label="Reason for contact">
<button type="button" class="reason-pill" data-reason="correction" aria-pressed="true">A correction</button>
<button type="button" class="reason-pill" data-reason="missing" aria-pressed="false">A missing title</button>
<button type="button" class="reason-pill" data-reason="photo" aria-pressed="false">I'm an actor</button>
<button type="button" class="reason-pill" data-reason="other" aria-pressed="false">Something else</button>
</div>
</div>
<div class="contact-row">
<div class="field"><label for="c-name">Your name</label><input id="c-name" type="text" placeholder="Optional"></div>
<div class="field"><label for="c-email">Email</label><input id="c-email" type="email" placeholder="Only if you want a reply"></div>
</div>
<div class="field" id="title-field">
<label id="title-field-label" for="c-page">Which page is wrong?</label>
<input id="c-page" type="text" placeholder="e.g. How to Tame a Silver Fox">
<span class="hint" id="title-field-hint">A title, actor or app page. A link is even better.</span>
</div>
<div class="field">
<label for="message-field">Message</label>
<textarea id="message-field" rows="7" placeholder="What should it say instead?"></textarea>
</div>
<div style="display:flex;flex-wrap:wrap;gap:14px;align-items:center">
<button class="btn btn-gold" type="button">Send it</button>
<span class="reassure">I read everything myself, usually within a couple of days.</span>
</div>
</form>
<aside class="contact-side">
<div class="side-card">
<h2>Faster than the form</h2>
<div class="kv"><div class="k">Email</div><a href="mailto:hello@dramaeverafter.com">hello@dramaeverafter.com</a></div>
<div class="kv"><div class="k">Corrections</div><a href="mailto:fix@dramaeverafter.com">fix@dramaeverafter.com</a></div>
</div>
<div class="side-card warn">
<h2>Before you write</h2>
<ul>
<li>I'm not affiliated with ReelShort, DramaBox or any other app &mdash; I can't fix your subscription or refund coins.</li>
<li>Actor photos are the apps' own promotional stills, which is why most profiles are still initials. If you're an actor and want yours changed or removed, tell me and it's done.</li>
<li>Missing title? Send the app and the exact name and it usually goes live the same week.</li>
</ul>
</div>
</aside>
</section>
{CONTACT_JS}"""
html = page("Contact DramaEverAfter: Report a Correction or Missing Title",
            "Report a correction, a missing title, or get in touch with DramaEverAfter.",
            body, f"{DOMAIN}/contact.html", depth=0)
open(os.path.join(DIST, "contact.html"), "w").write(html)
urls.append("/contact.html")

# sitemap + robots
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
sm += "".join(f"<url><loc>{DOMAIN}{u}</loc></url>\n" for u in urls) + "</urlset>"
open(os.path.join(DIST, "sitemap.xml"), "w").write(sm)
open(os.path.join(DIST, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n")

print(f"Built {len(urls)} pages -> dist/")
