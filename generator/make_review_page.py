#!/usr/bin/env python3
"""Cyan's one-page caption review, generated from a batch file.

This is the review format that worked (HANDOVER, 24 Aug): the whole batch on one
page, ranked by reach, each caption shown as it will render, the source one tap
away, an edit box prefilled and saved in the browser, a read tick, and one
"Collect my edits" button that emits paste-ready blocks. Earlier generators
lived in session scratchpads and had to be rebuilt every time; this one lives in
the repo. The page is a VIEW; the staging file stays the record.

Her rules encoded here: read means done (a ticked, unedited caption is
approved); collect emits only captions whose text actually changed, compared
with whitespace collapsed, so mechanical differences are never resent.

Usage:
    python3 generator/make_review_page.py generator/staging/captions_2026_09_02_b4.py out.html [--title "Batch four"]
"""
import io, json, sys, html, os

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import caption_pipeline as cp  # noqa: E402

CSS = """
:root{--paper:#FBF7F2;--surface:#FFFFFF;--ink:#2A2226;--plum:#2B1B2E;--wine:#7A2B4A;--gold:#C9962E;--gold-deep:#A87B1F;--line:#E4D8CE;--muted:#5A4A50;--tert:#7D6C64;--warm:#F8F1EA;--ok:#2F5F3E;--okbg:#DFEAE1}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--paper:#1C1419;--surface:#26191F;--ink:#EFE6E0;--plum:#F3E8EE;--wine:#D2778F;--gold:#D9A94A;--gold-deep:#E2B85F;--line:#3F2D36;--muted:#C4B3B9;--tert:#A8979D;--warm:#231A1F;--ok:#A9D8B6;--okbg:#1F3A29}}
:root[data-theme="dark"]{--paper:#1C1419;--surface:#26191F;--ink:#EFE6E0;--plum:#F3E8EE;--wine:#D2778F;--gold:#D9A94A;--gold-deep:#E2B85F;--line:#3F2D36;--muted:#C4B3B9;--tert:#A8979D;--warm:#231A1F;--ok:#A9D8B6;--okbg:#1F3A29}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font-family:'Atkinson Hyperlegible',system-ui,sans-serif;font-size:17px;line-height:1.55}
h1,h2,h3{font-family:'Fraunces',Georgia,serif;font-weight:600;color:var(--plum);margin:0;line-height:1.15}
.wrap{max-width:720px;margin:0 auto;padding:0 18px 80px}
.top{position:sticky;top:0;background:var(--paper);border-bottom:1px solid var(--line);padding:12px 0;display:flex;gap:12px;align-items:center;flex-wrap:wrap;z-index:2}
.top h1{font-size:22px}.top .count{margin-left:auto;font-size:14px;color:var(--tert);font-variant-numeric:tabular-nums}
.btn{font:inherit;font-size:15px;padding:9px 14px;border:1px solid var(--wine);background:var(--wine);color:#fff;border-radius:2px;cursor:pointer}
.btn.ghost{background:transparent;color:var(--wine)}
.cap{border-top:1px solid var(--line);padding:22px 0;display:flex;flex-direction:column;gap:10px}
.cap.done{background:linear-gradient(90deg,var(--okbg) 0,transparent 6px)}
.meta{display:flex;gap:10px;align-items:baseline;flex-wrap:wrap;font-size:13px;color:var(--tert);letter-spacing:.06em;text-transform:uppercase}
.meta b{font-family:'Fraunces',Georgia,serif;font-size:16px;color:var(--plum);text-transform:none;letter-spacing:0}
.hook{font-family:'Fraunces',Georgia,serif;font-size:21px;color:var(--plum);line-height:1.25}
.body{color:var(--ink)}
details{font-size:15px;color:var(--muted)}summary{cursor:pointer;color:var(--wine)}
details p{margin:8px 0 0;background:var(--warm);padding:10px 12px;border-left:3px solid var(--gold)}
textarea{width:100%;min-height:150px;font:inherit;font-size:16px;line-height:1.5;padding:10px;border:1px solid var(--line);background:var(--surface);color:var(--ink);border-radius:2px;resize:vertical}
textarea.changed{border-color:var(--gold-deep)}
.row{display:flex;gap:14px;align-items:center;flex-wrap:wrap;font-size:15px}
.row label{display:flex;gap:8px;align-items:center;cursor:pointer}
input[type=checkbox]{width:22px;height:22px;accent-color:var(--wine)}
.out{margin-top:20px}.out textarea{min-height:220px;font-family:ui-monospace,Menlo,monospace;font-size:14px}
.note{font-size:14px;color:var(--tert)}
"""

JS = """
const KEY='dea-review-'+document.body.dataset.batch;
const state=JSON.parse(localStorage.getItem(KEY)||'{}');
const norm=s=>s.replace(/\\s+/g,' ').trim();
function save(){localStorage.setItem(KEY,JSON.stringify(state));count();}
function count(){const n=document.querySelectorAll('.cap').length;let read=0,edited=0;
 document.querySelectorAll('.cap').forEach(c=>{const id=c.dataset.id;const ta=c.querySelector('textarea');
  const ed=norm(ta.value)!==norm(ta.dataset.orig);ta.classList.toggle('changed',ed);
  const done=(state[id]&&state[id].read)||ed;c.classList.toggle('done',done);if(done)read++;if(ed)edited++;});
 document.getElementById('count').textContent=read+' of '+n+' read · '+edited+' edited';}
document.querySelectorAll('.cap').forEach(c=>{const id=c.dataset.id;const ta=c.querySelector('textarea');const cb=c.querySelector('input');
 if(state[id]){if(state[id].text!=null)ta.value=state[id].text;cb.checked=!!state[id].read;}
 ta.addEventListener('input',()=>{state[id]=Object.assign(state[id]||{},{text:ta.value});save();});
 cb.addEventListener('change',()=>{state[id]=Object.assign(state[id]||{},{read:cb.checked});save();});});
document.getElementById('collect').addEventListener('click',()=>{const parts=[];
 document.querySelectorAll('.cap').forEach(c=>{const ta=c.querySelector('textarea');if(norm(ta.value)!==norm(ta.dataset.orig))parts.push('['+c.dataset.id+']\\n'+ta.value.trim());});
 const read=[...document.querySelectorAll('.cap')].filter(c=>c.querySelector('input').checked).map(c=>c.dataset.id);
 document.getElementById('outbox').value=(parts.length?parts.join('\\n\\n'):'(no edits)')+'\\n\\nREAD: '+read.length+' ticked';
 document.getElementById('outbox').focus();document.getElementById('outbox').select();});
document.getElementById('markall').addEventListener('click',()=>{document.querySelectorAll('.cap').forEach(c=>{const id=c.dataset.id;c.querySelector('input').checked=true;state[id]=Object.assign(state[id]||{},{read:true});});save();});
count();
"""


def main():
    src, dst = sys.argv[1], sys.argv[2]
    title = sys.argv[sys.argv.index("--title") + 1] if "--title" in sys.argv else os.path.basename(src)
    caps, facts = cp.load_batch(src)
    sources = cp.load_sources(src)
    q = {r["tid"]: r for r in cp.build_queue()}
    entries = [(tid, c) for tid, c in caps.items() if c.strip()]
    entries.sort(key=lambda kv: -(q.get(kv[0], {}).get("reach") or 0))
    rows = []
    for i, (tid, cap) in enumerate(entries, 1):
        hook, body = (cap.strip().split("\n", 1) + [""])[:2]
        r = q.get(tid, {})
        src_txt = facts.get(tid) or r.get("facts", "")
        url = (sources.get(tid) or ("", ""))[1]
        link = f' · <a href="{html.escape(url)}" target="_blank" rel="noopener">platform page</a>' if url else ""
        rows.append(f"""
<section class="cap" data-id="{html.escape(tid)}">
<div class="meta"><span>{i}</span><b>{html.escape(r.get('title', tid))}</b><span>{cp.views_label(r.get('reach') or 0)}</span></div>
<p class="hook">{html.escape(hook)}</p>
<p class="body">{html.escape(body.strip())}</p>
<details><summary>What the platform says{link}</summary><p>{html.escape(" ".join(src_txt.split()))}</p></details>
<textarea data-orig="{html.escape(cap.strip())}">{html.escape(cap.strip())}</textarea>
<div class="row"><label><input type="checkbox"> Read</label><span class="note">Edit the box only if you would change it. Read means done.</span></div>
</section>""")
    page = f"""<title>{html.escape(title)}</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600&family=Atkinson+Hyperlegible:wght@400;700&display=swap">
<style>{CSS}</style>
<body data-batch="{html.escape(os.path.basename(src))}">
<div class="wrap">
<div class="top"><h1>{html.escape(title)}</h1><span class="count" id="count"></span><button class="btn ghost" id="markall" type="button">Mark all read</button><button class="btn" id="collect" type="button">Collect my edits</button></div>
<p class="note" style="margin:14px 0 0">{len(entries)} captions, ranked by reach. Each shows exactly as it will render on the site. Your edits and ticks are saved in this browser; "Collect my edits" outputs only the captions you changed, as paste-ready blocks.</p>
{''.join(rows)}
<div class="out"><h2>Paste this back to Claude</h2><textarea id="outbox" readonly placeholder="Press Collect my edits"></textarea></div>
</div>
<script>{JS}</script>
</body>"""
    io.open(dst, "w", encoding="utf-8", newline="\n").write(page)
    print("wrote %s: %d captions" % (dst, len(entries)))


if __name__ == "__main__":
    main()
