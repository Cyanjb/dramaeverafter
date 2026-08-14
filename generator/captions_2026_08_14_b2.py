"""Caption batch 2, 14 Aug 2026 - the next 45 by reach.

VOICE: warm + bestie, fun without the silly ditz (Cyan's ruling, recorded in the
READ FIRST standing rules). One playful fan-aside per caption, no caps-lock, no
exclamation stacking, no em dashes. Written fresh from the quarantined facts; the
platform's wording is never reused or reworded. Where facts were thin the caption
stays short rather than inventing plot.

Fill-blank-only: these 45 had no live synopsis when written.

Usage:
    py generator/captions_2026_08_14_b2.py [--dry-run]
"""
import csv, io, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.environ.get("DEA_DATA") or os.path.join(HERE, "..", "data")
DRY = "--dry-run" in sys.argv

# Each value is "HOOK\nBODY". The hook renders as a subheading (Cyan, 14 Aug).
# NO DASHES OF ANY KIND, including hyphens (Cyan, 14 Aug, "this is very important").
CAPTIONS = {
    "runaway-princess-bride":
        "The runaway bride trope done properly.\n"
        "Riley fled a forced marriage the moment her groom showed his true colours, "
        "and ran straight into Xander Thorne.",
    "duke-with-benefits":
        "Her biggest mistake became her best decision.\n"
        "Taylor's music dreams and her real life pulled two different ways. The "
        "duke of the title is where it gets fun.",
    "my-three-ungrateful-brothers-come-crawling-back":
        "Watching her make them earn it is deeply satisfying.\n"
        "Oriana lost her mum at six and got dumped at a trailer park by her "
        "stepmother. Now the family that threw her away wants back in.",
    "my-brothers-begged-but-i-m-the-dragon-s-queen":
        "Fantasy with a grudge, in the best way.\n"
        "The Frostmark Empire is locked in endless winter, and only a royal bride "
        "can wake the Abyss Dragon and bring the warmth back. Guess who her "
        "brothers suddenly need.",
    "bound-by-vendetta-sleeping-with-the-enemy":
        "The truth may be closer than she can afford.\n"
        "Daiana's father was killed on her birthday, and she has been hunting his "
        "killer ever since. The title tells you where that search puts her.",
    "baby-you-had-it-coming":
        "The title is a promise, and this one keeps it.\n"
        "Ivy married the man of her dreams and got a nightmare on a loop instead.",
    "darling-please-come-home":
        "This one does not let you look away.\n"
        "Stella was kidnapped while her brother could only watch, and everything "
        "changes for her after.",
    "in-bed-with-your-lies":
        "The lies go deeper than she thinks.\n"
        "Sara is reduced to a maid in the house her late mother built from nothing. "
        "The injustice is only the setup.",
    "succession-beauty-and-the-billionaire":
        "Rock bottom, meet billionaire.\n"
        "Grace loses her mother, her home and her boyfriend in one brutal reveal: "
        "she was never the real daughter. You know where this is going and it is "
        "still a treat.",
    "love-ages-like-fine-wine":
        "Second chances rarely simmer this well.\n"
        "Austin was the love of Grace's life right up until he stood her up at the "
        "altar. Years later the story is not finished with either of them.",
    "blood-and-bones-of-the-disowned-daughter":
        "She does not come back gently.\n"
        "Natalie was the cherished daughter until Monica arrived as the true "
        "heiress and played her out of the family.",
    "freed-by-the-sexy-farmer":
        "The farm is not the prison she expected.\n"
        "Her family ruined, heiress Lily is sold to a man with a fearsome "
        "reputation. The title hints at how that actually goes.",
    "reborn-to-see-the-football-stars-ruin-themselves":
        "Rebirth plus cheer squad politics is a wild combination.\n"
        "The night before the state final, the team parties when they should not, "
        "and Katlyn gets to watch the fallout with knowledge she should not have.",
    "out-of-my-way-the-reborn-mafia-queen-is-here":
        "The title is not exaggerating about the attitude.\n"
        "Her identity stolen, her life ended, and then a second chance. Arya comes "
        "back knowing exactly who did what.",
    "the-seduction-game":
        "The game backfires exactly the way you hope it will.\n"
        "A scholarship lands a broke, brilliant girl in an elite prep school, "
        "where the queen bee sets her bad boy pawn on her.",
    "private-school-playboys":
        "The doormat era ends on the spot.\n"
        "Maddie has always put Lowell Academy's golden boy first. Then she catches "
        "him cheating, and watching her flip the script is the fun of it.",
    "a-mistaken-surrogate-for-the-ruthless-billionaire":
        "One clinic error, one much more interesting man.\n"
        "Luciana was about to tell her husband she was finally pregnant when she "
        "caught him cheating. The surrogacy mix up that follows changes everything.",
    "poolboy":
        "Class war in swim trunks.\n"
        "Swim captain Aidan loses his job thanks to his rich bully, then lands "
        "poolside in the last place he should be working. It knows exactly how "
        "fun that is.",
    "deadly-affair-with-my-brother-in-law":
        "The title says deadly and it means it.\n"
        "Aurora is engaged to Patrick but it is his brother Noah she falls for, "
        "and Patrick does not take betrayal quietly.",
    "my-dear-daughter-love-me-once-more":
        "Have the tissues ready.\n"
        "He only ever had eyes for his first love, and his little girl Aria paid "
        "the price. A father and daughter tearjerker first, a romance second.",
    "reborn-i-gifted-her-my-hell":
        "Deliciously petty rebirth revenge.\n"
        "Orphan sisters get a do over back to the day of their adoption, and Poppy "
        "remembers every awful thing. This time she picks differently, on purpose.",
    "my-husband-killed-me-then-i-won-the-mega-ball":
        "Revenge with a lottery jackpot behind it.\n"
        "Adoria's husband murders her, and she wakes up back in time holding "
        "tomorrow's winning numbers. Exactly as satisfying as it sounds.",
    "end-of-the-world-start-of-my-empire":
        "The end of the world is his opening move.\n"
        "After World War III, Arthur is scraping by on scavenged goods. Apocalypse "
        "hustle stories do not get better setups than this.",
    "lady-boss-takes-on-vegas-bullies":
        "The bullies have no idea who is holding the mop.\n"
        "Jane goes undercover as a janitor to investigate abuse claims in her own "
        "operation. The reveal is worth the wait.",
    "accelerating-love":
        "Honestly, good for her.\n"
        "Lillian catches her boyfriend with her best friend at her own wedding. "
        "The rebound that follows moves considerably faster than the title suggests.",
    "my-step-brother-is-my-ex":
        "The awkward is the point, and it is glorious.\n"
        "Four years after a misunderstanding wrecked them, Hannah's ex walks back "
        "into her life as her new stepbrother.",
    "pregnant-by-the-golden-billionaire-bachelor":
        "A grown up heroine for once.\n"
        "A maid of 45, one night with an infertile billionaire silver fox, and "
        "twins on the way. The show knows what a gift that setup is.",
    "my-gorgeous-wife-is-an-ex-convict":
        "The reckoning is lovely to watch.\n"
        "Brielle went to prison for a death she did not cause, sent there by the "
        "fiance who would not believe her. Three years later she is out.",
    "curse-of-the-dragon-king":
        "Forbidden, impossible, and completely committed to the fantasy.\n"
        "A human, Marked as a dragon's mate. Not just any dragon either, but the "
        "king.",
    "don-t-challenge-the-lady-billionaire":
        "The mask comes off, and the title is fair warning.\n"
        "Juliet runs a financial empire and hid it for seven years for love, only "
        "to be discarded.",
    "the-boy-i-hate":
        "Forced proximity at highway speed.\n"
        "Her boyfriend bails on the road trip from LA to NYC for her best friend's "
        "wedding, so Samantha ends up sharing the drive with the last person she "
        "would choose.",
    "submitting-to-my-best-friend-s-dad":
        "The one man who should be completely off limits.\n"
        "After a rough year at Yale and a breakup, Becca just wanted a summer off. "
        "Age gap forbidden done with real heat.",
    "a-blind-date-with-my-mr-meant-to-be":
        "Fate does the heavy lifting here, beautifully.\n"
        "Jessica lost her daughter to child services and never stopped grieving. "
        "Years later she unknowingly marries a billionaire, and the threads of her "
        "old life start pulling.",
    "ms-detective-and-mr-thief":
        "The thief she is hunting is closer than she thinks.\n"
        "Fifteen years later, Isabel and Ari reunite and the sparks are immediate. "
        "Small problem: she is a detective building her career on catching exactly "
        "his kind.",
    "crossing-the-line-to-love":
        "What she does next crosses every sensible line.\n"
        "Three days before her wedding, Nichole finds her fiance in bed with her "
        "bridesmaid. That is exactly why it is worth watching.",
    "seduction-cove":
        "Your guilty pleasure, sorted.\n"
        "A reality show built to break couples: hot singles, cash prizes, insane "
        "challenges. Loyalty does not stand a chance.",
    "hold-me-in-the-dark":
        "Who he becomes in the dark is a different question entirely.\n"
        "Intern Isla knows the cold CEO who torments her on the tennis court by "
        "day. Double identity romance with real tension.",
    "kidnapped-by-the-mafia":
        "The heart of gold is the inconvenient part.\n"
        "Sold by her own boyfriend to mafia king Vincenzo as a contract bride, "
        "Violet plans her escape from day one. His heart is what makes it sing.",
    "falling-for-my-nemesis-stepbrother":
        "Enemies under one roof, always a good time.\n"
        "Nicole is the good girl. Kane, her new stepbrother, is very much not. She "
        "gets to find out what is underneath the reputation.",
    "rock-on-band-beauty-in-disguise":
        "A girl in disguise in a boy band is a classic for a reason.\n"
        "When her twin brother loses his voice before the rehearsal that matters, "
        "Astra steps into his place. This one has fun with it.",
    "park-avenue-girls-don-t-play-nice":
        "The title is the thesis, and she proves it.\n"
        "Cheated out of the Paris art scholarship that was her way out, Anna "
        "reinvents herself among the Park Avenue set.",
    "the-warlord-returns":
        "The room has no idea what just arrived.\n"
        "War hero Harrison comes home to learn his sister died at her fiance's "
        "hand. He walks into the man's banquet in his worn army coat. Chills.",
    "mother-warrior-unleashed":
        "Mum on a warpath, at full throttle.\n"
        "Traffickers grab the wrong teenager: her mother is a legendary Navy SEAL "
        "living quietly under the radar.",
    "mistaken-for-a-gold-digger":
        "One sudden marriage, one giant misread.\n"
        "Lila needs money to save an orphanage. William is a billionaire allergic "
        "to gold diggers. The fun writes itself.",
    "gossip-godmother":
        "Part mystery, part teen drama, entirely moreish.\n"
        "Scholarship student Zoey starts receiving gossip posts that predict her "
        "future, and they keep being right.",
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
        # Overwriting is safe HERE ONLY: any existing text on these ids is this
        # script's own earlier draft (the platform text was quarantined first).
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
