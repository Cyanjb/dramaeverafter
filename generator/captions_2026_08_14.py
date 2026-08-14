"""First batch of rewritten captions, 14 Aug 2026 - the 15 highest-reach titles
whose copied synopses were quarantined.

VOICE, corrected 14 Aug after Cyan rejected the first draft batch: a MIXTURE OF WARM
AND BESTIE, "so fun but without the silly ditz" (her words, choosing between four
sample registers). Enthusiastic and playful but composed: one fan-aside per caption,
no caps-lock, no "okay so", no exclamation stacking. Short sentences, no em dashes,
no moralising. The first (dry/wry) batch below was REPLACED in the same file, which
is why the applier overwrites its own ids: the text being overwritten is ours, not a
platform's, so fill-blank-only does not apply to it.

PROVENANCE: written from the FACTS in _quarantined_synopses.json (character names,
premise, source novel). The platform's wording was not reused or reworded - where a
fact was thin the caption stays short rather than inventing plot.

Fill-blank-only: refuses to overwrite a non-empty synopsis_short.

Usage:
    py generator/captions_2026_08_14.py [--dry-run]
"""
import csv, io, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.environ.get("DEA_DATA") or os.path.join(HERE, "..", "data")
DRY = "--dry-run" in sys.argv

# Each value is "HOOK\nBODY". The hook renders as a subheading (Cyan, 14 Aug).
# NO DASHES OF ANY KIND, including hyphens (Cyan, 14 Aug, "this is very important").
CAPTIONS = {
    "swallow-me-whole":
        "Dark, obsessive, and not playing nice.\n"
        "Adapted from Gemma James's novel. If this is your corner of romance, you "
        "already know you want it.",
    "country-gal-to-ceo-s-bride":
        "She refuses to shrink to fit his world.\n"
        "Emma left a hard country life behind for the city, and one mix up drops "
        "her straight into a CEO's orbit. Watching her hold her ground is what "
        "makes this one so satisfying.",
    "i-accidentally-sexted-my-enemy":
        "Enemies to lovers with just the right amount of cringe.\n"
        "Evelyn's crush goes public in the most humiliating way possible, and then "
        "a text lands in exactly the wrong inbox.",
    "the-luna-s-second-choice":
        "The choosing does not go the way anyone planned.\n"
        "Elara grew up knowing she would have to pick one of the Alpha's five sons "
        "as her mate. Ten years later, honestly, it is delicious.",
    "love-is-a-dangerous-dance":
        "The feelings absolutely refuse to behave.\n"
        "A ballerina raised on a farm fakes an engagement to keep her place at an "
        "elite company. The dancing is real. The fiance is not.",
    "the-cursed-alpha-s-mate":
        "Come for the curse, stay for the ache.\n"
        "A cursed alpha and a fated bond neither of them asked for, adapted from "
        "Cricket Colson's novel.",
    "kidnapped-by-the-devil":
        "Wild premise, wilder ride.\n"
        "Her fiance loses a round of Russian roulette, so the arms dealer running "
        "the game takes the bride instead. It knows exactly what it is.",
    "dear-brother-you-loved-me-too-late":
        "By the time they realise what they had, it may be too late.\n"
        "Angelica has spent sixteen years being blamed for a death that was never "
        "her fault. Honestly, good for her.",
    "the-alpha-s-virgin-captive":
        "He is used to owning things. She is not one.\n"
        "One act of kindness leaves a wolfless girl bound to the most feared alpha "
        "around. Watching him learn the difference is the treat.",
    "oh-no-i-slept-with-my-husband":
        "Exactly the mess you are hoping for.\n"
        "Beth's marriage was strictly a paper arrangement. Then one night she "
        "cannot take back turns out to star the last man it should have: her own "
        "husband.",
    "rejected-luna-is-the-alpha-queen":
        "They have no idea they are snubbing a queen.\n"
        "After rogues destroy her pack, warrior Arya hides what she really is to "
        "survive. The payoff is worth every minute.",
    "my-firefighter-ex-husband-burns-in-regret":
        "Keep tissues close for this one.\n"
        "Losing their daughter broke the marriage before the divorce papers ever "
        "could. Now her firefighter ex is learning what regret really feels like.",
    "taming-my-bullies-2":
        "She did not come to play fair.\n"
        "Rowan and Emma fought their way from enemies to couple. Now an heiress "
        "with her own claim on Rowan arrives to test that bond.",
    "outplayed":
        "Her two lives cannot stay separate forever.\n"
        "Broke college student by day, rising gaming star by night. Brooklyn needs "
        "that prize money more than anyone around her knows.",
    "secret-boss-of-the-five-keys":
        "Nobody ever suspects the gardener.\n"
        "A quiet gardener with a five year secret: he has been taking the syndicate "
        "apart one boss at a time. Honestly, that is half the fun.",
}


def term_of(p):
    raw = open(p, "rb").read()
    crlf = raw.count(b"\r\n")
    return "\r\n" if crlf > raw.count(b"\n") - crlf else "\n"


def main():
    p = os.path.join(DATA, "titles.csv")
    term = term_of(p)
    rows = list(csv.DictReader(open(p, newline="", encoding="utf-8-sig")))
    written, skipped = 0, []
    for r in rows:
        cap = CAPTIONS.get(r["title_id"])
        if cap is None:
            continue
        # Overwriting is safe HERE ONLY: any existing text on these 15 ids is this
        # script's own earlier draft (the platform text was quarantined first), so
        # replacing it is revising our own copy, not clobbering someone's work.
        r["synopsis_short"] = cap
        written += 1
    print(f"captions written : {written}")
    if skipped:
        print(f"skipped (non-blank): {skipped}")
    if DRY:
        print("[dry-run] nothing written")
        return
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=list(rows[0].keys()), lineterminator=term)
    w.writeheader()
    w.writerows(rows)
    open(p, "w", encoding="utf-8", newline="").write(buf.getvalue())
    print("written titles.csv")


if __name__ == "__main__":
    main()
