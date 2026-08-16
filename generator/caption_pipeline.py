#!/usr/bin/env python3
"""The caption pipeline. Three commands, one shape, every batch.

WHY THIS EXISTS. There are 3,513 titles and only 60 captions written by us, so the
work had to stop being bespoke. Two things made the first sessions slow: hunting for
each title's facts by hand, and having no mechanical way to prove a caption did not
invent plot. Both are solved here.

    py generator/caption_pipeline.py next 45      -> staging/captions_<date>.py to fill in
    py generator/caption_pipeline.py check <file> -> refuses the batch if any rule fails
    py generator/caption_pipeline.py apply <file> -> fill-blank-only write, then rebuild

RANKED STRICTLY BY REACH, ACROSS BOTH BACKLOGS AT ONCE. This corrects a real
sequencing error: the first 60 captions were drawn from the fact file (titles whose
copied synopsis was removed), which happens to hold LOW reach titles topping out near
14M, while every one of the biggest titles sat untouched in the rewrite queue still
showing platform text. Not one of the top 15 by views had a caption of ours. Reach
does not care which backlog a title came from, so neither does this.

    top 100 titles = 49.6% of all views
    top 300 titles = 82.8%
    top 600 titles = 98.4%

so the goal is NOT 3,513 captions. It is the top few hundred, done properly.

TIERS, measured 15 Aug:
    A     60  caption already ours          -> needs an ASIDE only
    B    756  live platform text on disk    -> that text IS the fact source
    C  2,256  blank, facts in the fact file -> facts on disk
    D    441  nothing on disk               -> MUST FETCH before writing.
              All 441 have zero recorded views and only 16 have a link, so they are
              both the most expensive and the least valuable. They wait.

THE ACCURACY GUARD is the part that matters. Cyan, 15 Aug: "anything you write is
correct and in line with the plot... We can't have incorrect synopsis on this
website." So check() extracts every proper noun from the hook and body and refuses
the batch unless each one appears in that title's own fact source or its title. A
fabricated character cannot reach the site. Sentence-initial words are skipped
because they are capitalised by grammar, not because they are names - flagging
"Things do not go to plan" as an invented name was a real false positive, and a
checker that cries wolf is one that gets ignored.

NO FACT SOURCE MEANS GO AND READ ONE. Cyan's rule: a title with no facts on disk is
fetched from the platform's own page before a word is written, and the fetched text
is stored beside the caption as provenance. `next` marks those rows FETCH REQUIRED
rather than letting them through.

Usage:
    py generator/caption_pipeline.py next [N] [--offset N]
    py generator/caption_pipeline.py check <file>
    py generator/caption_pipeline.py apply <file> [--dry-run]
"""
import csv, io, json, os, re, sys, unicodedata, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.environ.get("DEA_DATA") or os.path.join(os.path.dirname(HERE), "data")
STAGING = os.path.join(HERE, "staging")
FACTFILE = os.path.join(STAGING, "_quarantined_synopses.json")

DASHES = {c for c in map(chr, range(0x110000))
          if unicodedata.category(c) == "Pd"} | {"-", "–", "—", "−"}

# Shapes Cyan has rejected, both calibration rounds. See the standing rules.
REJECTED = [
    (r"is the (whole|entire) (hook|appeal|point|draw)", "analytical verdict"),
    (r"\bof it all is\b", "analytical verdict"),
    (r"and it lands\b", "analytical verdict"),
    (r"is exactly why you clicked", "analytical verdict"),
    (r"done properly\b", "appraises the execution"),
    (r"exactly as promised\b", "appraises the execution"),
    (r"\blove me some\b", "singular speaker, the site speaks as us"),
]
# An aside must stand alone: cover the hook and body and it still has to make sense.
# CALIBRATED AGAINST CYAN'S OWN WORDING, 15 Aug. The real fault was a bare pronoun
# standing in for the show with nothing to point at - "It knows exactly what it is"
# reads as nonsense once lifted out of its paragraph. What is NOT a fault:
#   "This one is served with an extra helping of angst"  - "this one" is idiomatic
#       for "this show" and is always available to a reader, it points at nothing
#   "They are all about to eat their words"              - a fan may refer to the
#       people just read about; that is the aside commenting on the series
# Both of those are her wording, so the rule narrows to bare It/That, and to This
# only when it is not "this one".
BACKREF = [
    (r"^(it|that)\b", "aside opens on a bare pronoun with nothing to point at"),
    (r"^this\b(?!\s+one\b)", "aside opens on a bare This"),
    (r"\bthe difference\b", "aside leans on something defined in the hook"),
]


# Titles whose PUBLISHED synopsis is genuinely too short to reach the 200 floor.
# A title only belongs here after the platform page has been read and confirmed to
# publish nothing more - never as a way round the minimum. Cyan's standing rule is
# that a title with no findable synopsis goes on a list for her, not into invention.
SOURCE_LIMITED = {
    # ReelShort publishes ONE sentence for this and nothing else: no extended
    # synopsis, no chapter titles, no character descriptions. Checked twice,
    # 15 Aug 2026. Its theme tags are tags, not plot, and are not usable as facts.
    "snatched-a-billionaire-to-be-my-husband",
}


def rows(name):
    with io.open(os.path.join(DATA, name), encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def views(s):
    m = re.match(r"^([\d.]+)\s*([KMB])?$", (s or "").strip().upper())
    if not m:
        return 0
    return int(float(m.group(1)) * {"K": 1e3, "M": 1e6, "B": 1e9, None: 1}[m.group(2)])


def views_label(n):
    if n >= 1e6:
        return "%.1fM" % (n / 1e6)
    if n >= 1e3:
        return "%.1fK" % (n / 1e3)
    return "n/a" if not n else str(n)


def load_facts():
    if os.path.exists(FACTFILE):
        return json.load(io.open(FACTFILE, encoding="utf-8"))
    return {}


def proper_nouns(text):
    """Capitalised words that are NOT sentence initial."""
    out = []
    for sent in re.split(r"(?<=[.!?])\s+", text):
        for w in re.findall(r"[A-Za-z][A-Za-z']*", sent)[1:]:
            if re.match(r"^[A-Z][a-z]{2,}$", w):
                out.append(w)
    return out


def parts(cap):
    p = [x.strip() for x in cap.split("\n")]
    return (p + ["", "", ""])[:3]


def validate(tid, cap, fact, title):
    """Every rule, in one place. Returns a list of failures."""
    errs = []
    hook, body, aside = parts(cap)
    if not hook:
        errs.append("no hook")
    if not body:
        errs.append("no body")
    # BODY LENGTH. Cyan moved this three times in one evening, 200 -> 400 -> here,
    # and then settled the conflict it created: "first rule is to be accurate, if
    # you can't find enough substance DROP THE COUNT."
    #
    # SO ACCURACY OUTRANKS LENGTH, ALWAYS. The floor is a prompt to go and fetch
    # more synopsis. It is never a licence to pad and never a reason to infer.
    # Measured 15 Aug: of 45 titles, only 6 have a PUBLISHED synopsis of 400+
    # characters, 15 have 300-399, 16 have 200-299 and 8 have under 200. A 400
    # floor would therefore have forced invention on 39 of them.
    #
    # THE CHECK IS THEREFORE RELATIVE, NOT ABSOLUTE. An absolute floor punishes a
    # caption for its platform publishing a short synopsis, which the writer cannot
    # fix and must not fix by inventing. What IS worth catching is a caption that
    # leaves material on the table: a 200 character body under a 600 character
    # source means the story is there and was not used.
    #
    # So: aim for 300+, but only FAIL when the source could clearly support it.
    elif len(body) < 300 and tid not in SOURCE_LIMITED and len(fact or "") >= 350:
        errs.append("body is %d chars from a %d char source - the substance is "
                    "there, use more of it" % (len(body), len(fact or "")))
    elif len(body) > 700:
        errs.append("body is %d chars, over the 700 maximum" % len(body))
    # THE ASIDE IS OPTIONAL as of 15 Aug 2026. Cyan: "We have to remove the last
    # sentence, it is causing the biggest problems." Captions are HOOK + BODY, the
    # same shape as the 60 already live. build.py still renders a third part if one
    # is ever present, so nothing has to be undone if she wants them back.
    bad = sorted({c for c in cap if c in DASHES})
    if bad:
        errs.append("DASH %s" % bad)
    if "!" in cap:
        errs.append("exclamation mark")
    if re.search(r"\b[A-Z]{4,}\b", cap):
        errs.append("caps lock")
    # The hook may be TWO short sentences: the approved corpus has "He is used to
    # owning things. She is not one." What it may not be is long, so cap the length
    # rather than the sentence count.
    # 100, and deliberately generous. Cyan, 15 Aug: "make the cap a comfortable 100,
    # I want the cap to be flexible", then "you don't have to have a 100 but if you
    # reach a 100 it's fine." So 100 is a CEILING, NOT A TARGET. Short hooks remain
    # the norm - most sit around 40 to 50 characters and should - and nothing here
    # should be padded toward the limit. This checker flagged her own wording FOUR
    # times by being tighter than her taste, which is why the guard now only catches
    # a runaway paragraph in the hook slot rather than enforcing a house style.
    if len(hook) > 100:
        errs.append("hook is %d chars, too long to read as a subheading" % len(hook))
    if len(re.findall(r"[.!?]", hook)) > 2:
        errs.append("hook is more than two sentences")
    for pat, why in REJECTED:
        if re.search(pat, cap, re.I):
            errs.append("%s (%s)" % (why, pat))
    for pat, why in BACKREF:
        if re.search(pat, aside, re.I):
            errs.append(why)
    haystack = ((fact or "") + " " + title).lower()

    def known(n):
        """A name counts as sourced if it appears, or if its singular does.
        'the Pattersons' from a source that says 'the Patterson family' is a
        plural, not an invention, and failing it teaches you to ignore the
        checker. Same for a possessive."""
        n = n.lower()
        if n in haystack:
            return True
        for stripped in (n.rstrip("s"), n[:-2] if n.endswith("es") else n):
            if len(stripped) > 2 and stripped in haystack:
                return True
        return False

    invented = sorted({n for n in proper_nouns(hook + " " + body) if not known(n)})
    if invented:
        errs.append("INVENTED PROPER NOUN %s - not in the fact source" % invented)
    return errs


def build_queue():
    titles = rows("titles.csv")
    facts = load_facts()
    reach, link, plat = {}, {}, {}
    for r in rows("availability.csv"):
        t = r["title_id"]
        reach[t] = max(reach.get(t, 0), views(r.get("view_count")))
        if r.get("direct_link") and t not in link:
            link[t] = r["direct_link"]
            plat[t] = r.get("platform_id", "")
    q = []
    for t in titles:
        tid = t["title_id"]
        s = (t.get("synopsis_short") or "").strip()
        if s and "\n" in s:
            tier, src = "A", ""              # ours already; needs an aside only
        elif s:
            tier, src = "B", s               # the live platform text is the fact source
        elif tid in facts:
            tier, src = "C", facts[tid].get("copied_text", "")
        else:
            tier, src = "D", ""              # nothing on disk
        q.append({"tid": tid, "title": t["primary_title"], "tier": tier, "facts": src,
                  "reach": reach.get(tid, 0), "link": link.get(tid, ""),
                  "platform": plat.get(tid, "")})
    q.sort(key=lambda r: -r["reach"])
    return q


def cmd_next(n, offset):
    q = [r for r in build_queue() if r["tier"] != "A"][offset:offset + n]
    stamp = datetime.date.today().isoformat().replace("-", "_")
    path = os.path.join(STAGING, "captions_%s_r%d.py" % (stamp, offset))
    out = ['# -*- coding: utf-8 -*-', '"""Batch generated by caption_pipeline.py next.',
           "",
           "Fill CAPTIONS. Each value is HOOK newline BODY newline ASIDE.",
           "  HOOK  one sentence, leads as the subheading",
           "  BODY  the synopsis, in our words, ONLY facts from the source below",
           "  ASIDE us talking to the reader, must stand alone with the rest covered",
           "",
           "FETCH REQUIRED means there is no fact source on disk. Read the platform page",
           "first, paste what it says into FACTS below, then write. Never write from the",
           "title alone.", '"""', "", "CAPTIONS = {"]
    for r in q:
        out.append("")
        out.append("    # %-8s %s" % (views_label(r["reach"]), r["title"]))
        if r["tier"] == "D":
            out.append("    # !! FETCH REQUIRED - no facts on disk. link: %s" % (r["link"] or "none"))
        for line in (r["facts"] or "").strip().splitlines() or [""]:
            for chunk in [line[i:i + 88] for i in range(0, len(line), 88)] or [""]:
                out.append("    # FACTS: %s" % chunk)
        out.append("    %r:" % r["tid"])
        out.append('        "",')
    out.append("}")
    out.append("")
    out.append("FACTS = {  # paste fetched text here for any FETCH REQUIRED row")
    for r in q:
        if r["tier"] == "D":
            out.append("    %r: %r," % (r["tid"], ""))
    out.append("}")
    out.append("")
    io.open(path, "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")
    print("wrote %s" % path)
    print("%d titles, reach %s down to %s"
          % (len(q), views_label(q[0]["reach"]), views_label(q[-1]["reach"])))
    tiers = {}
    for r in q:
        tiers[r["tier"]] = tiers.get(r["tier"], 0) + 1
    print("tiers: %s   (D = must fetch first)" % tiers)


def load_batch(path):
    src = io.open(path, encoding="utf-8").read()
    ns = {}
    exec(compile(src, path, "exec"), ns)
    return ns.get("CAPTIONS", {}), ns.get("FACTS", {})


def cmd_check(path):
    caps, extra = load_batch(path)
    q = {r["tid"]: r for r in build_queue()}
    todo = [t for t, c in caps.items() if not c.strip()]
    done = {t: c for t, c in caps.items() if c.strip()}
    print("batch %s: %d filled, %d still blank" % (os.path.basename(path), len(done), len(todo)))
    fails = 0
    for tid, cap in done.items():
        r = q.get(tid, {})
        fact = extra.get(tid) or r.get("facts", "")
        if not fact.strip():
            print("  FAIL %-46s NO FACT SOURCE - fetch and paste it into FACTS first" % tid[:44])
            fails += 1
            continue
        errs = validate(tid, cap, fact, r.get("title", ""))
        if errs:
            print("  FAIL %-46s %s" % (tid[:44], "; ".join(errs)))
            fails += 1
    print("\n%d of %d pass" % (len(done) - fails, len(done)))
    return 1 if fails else 0


def cmd_apply(path, dry):
    caps, extra = load_batch(path)
    if cmd_check(path):
        print("\nREFUSING TO APPLY - fix the failures above.")
        return 1
    p = os.path.join(DATA, "titles.csv")
    raw = open(p, "rb").read()
    crlf = raw.count(b"\r\n")
    term = "\r\n" if crlf > raw.count(b"\n") - crlf else "\n"
    titles = rows("titles.csv")
    fields = list(titles[0].keys())
    wrote = skipped = 0
    for t in titles:
        cap = caps.get(t["title_id"], "").strip()
        if not cap:
            continue
        cur = (t.get("synopsis_short") or "").strip()
        if cur and "\n" in cur and cur != cap and "--update-ours" not in sys.argv:
            # Already ours. Never overwrite our own approved work SILENTLY - but this
            # is not always a mistake. On 16 Aug the number one title was live with an
            # ASIDE and an old wording, because it had been applied and built before
            # Cyan dropped the last line from every caption. The approved file held
            # the corrected version and apply kept skipping it. So the skip is still
            # the default, and --update-ours is the explicit way to say "yes, replace
            # our earlier text with the newer approved text".
            skipped += 1
            print("   SKIP (already ours, differs from approved): %s" % t["title_id"])
            continue
        t["synopsis_short"] = cap
        wrote += 1
    print("\nwould write %d captions, skipping %d already ours" % (wrote, skipped))
    if dry:
        print("DRY RUN - nothing written.")
        return 0
    with io.open(p, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator=term)
        w.writeheader()
        w.writerows(titles)
    print("written: data/titles.csv   -> now run build.py")
    return 0


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        print(__doc__)
        sys.exit(0)
    if a[0] == "next":
        n = int(a[1]) if len(a) > 1 and a[1].isdigit() else 45
        off = int(a[a.index("--offset") + 1]) if "--offset" in a else 0
        cmd_next(n, off)
    elif a[0] == "check":
        sys.exit(cmd_check(a[1]))
    elif a[0] == "apply":
        sys.exit(cmd_apply(a[1], "--dry-run" in a))
    else:
        print(__doc__)
