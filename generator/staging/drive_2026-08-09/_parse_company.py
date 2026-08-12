"""Parse an IMDb company-page dump into distinct (rank, title, tt) rows.

Company pages number every entry, and a SERIES contributes one row per EPISODE,
all sharing the series tt. Deduping by tt and keeping the lowest rank recovers
the series title, because IMDb ranks a series above its own episodes. Verified
on GoodShort: 540 numbered rows -> 190 distinct titles, 0 episode rows surviving.

The saved dump escapes the ordinal as a literal backslash-dot, e.g. "1\\. Title".
That backslash is REAL text in the file, not an escape - writing this parser
through a shell heredoc silently ate it and produced zero matches.

Usage:  py _parse_company.py <saved-tool-result.txt> <platform_id> <out.json>
"""
import json
import re
import sys

src, platform, out = sys.argv[1], sys.argv[2], sys.argv[3]
text = json.load(open(src, encoding="utf-8"))["fileContent"]

mc = re.search(r"\b(co\d{6,})\b", text)
company = mc.group(1) if mc else "?"
mr = re.search(r"(\d[\d,]*)\s*[-–]\s*(\d[\d,]*)\s+of\s+(\d[\d,]*)", text)
header = mr.group(0) if mr else "no range header"

# ordinal is "<n>" then an optional literal backslash then "."
ORD = re.compile(r"(?m)^(\d+)\\?\.[ \t]*(.+?)[ \t]*$")
titles = {int(n): t.strip() for n, t in ORD.findall(text)}
tts = {int(n): tt for tt, n in re.findall(r"/title/(tt\d+)/\?ref_=sr_t_(\d+)", text)}
ranks = sorted(set(titles) & set(tts))

seen, ded = set(), []
for r in ranks:
    if tts[r] in seen:
        continue
    seen.add(tts[r])
    ded.append({"rank": r, "title": titles[r], "imdb_id": tts[r]})

print(f"{platform}: company={company}  header='{header}'")
print(f"  numbered rows={len(titles)}  tt links={len(tts)}  paired={len(ranks)}")
print(f"  duplicate/episode rows collapsed={len(ranks) - len(ded)}  DISTINCT={len(ded)}")
left = [r for r in ded if re.search(r"Episode|S\d+\.E\d+", r["title"])]
print(f"  episode-shaped surviving (want 0): {len(left)}")
missing = sorted(set(tts) - set(titles))
if missing:
    print(f"  tt links with no title text: {len(missing)} (ranks {missing[:6]})")

json.dump({"company": company, "platform": platform, "header": header,
           "distinct": len(ded), "titles": ded},
          open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"  -> {out}")
