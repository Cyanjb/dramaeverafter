# -*- coding: utf-8 -*-
"""Reddit-research flesh-out, 20 Sep 2026.

The Reddit dataset Cyan supplied (generator/staging/reddit_research_2026-09-20.json)
surfaced six in-database titles carrying no synopsis. The Reddit notes themselves
are NOT the fact source here and must never be: they are viewer commentary
("really good acting", "great chemistry", "rewatched it"), not plot, and writing
a caption from them would be inventing a story. Every caption below is written
from the platform's own page, fetched live 20 Sep and banked in
facts_reddit6_2026-09-20.json.

All six rank 2771-3427 by reach, well below top 300, so Cyan's 16 Aug 2026
ruling applies: written and applied without her manual review.

Two of the six are deliberately NOT here, for want of a source:
  kiss-of-the-pirate-king          the My Drama link on its availability row
                                   404s and no search route resolves it
  i-kissed-a-ceo-and-he-liked-it   no direct_link, and DramaBox search returns
                                   no match for the title
Both need a working platform link before anyone writes them. The Reddit doc
offers "pirate romance" and "the title is essentially the premise", which is
exactly the thin material the rules forbid building on.
"""

CAPTIONS = {
    # FACTS: Scholarship girl Julie has one reckless, electric night with the irresistibly hot new hoc
    # FACTS: key captain-only to discover he's Liam, the childhood enemy she can't stand. To kill rumo
    # FACTS: rs and keep their exes away, they fake-date. But the chemistry feels anything but fake, a
    # FACTS: nd the tension between them is getting dangerously hard to resist.
    'faking-it-with-the-hockey-captain':
        "One night with the new hockey captain. Then she finds out who he is.\nJulie is at school on a scholarship and the last thing she needs is a night she cannot take back with the boy who has just taken over as hockey captain. He turns out to be Liam, the childhood enemy she has spent years being unable to stand. People start talking, and both of them have an ex who will not take the hint, so they agree to be seen together and let everyone draw the obvious conclusion. Fake dating is supposed to be the easy part. It is turning out to be the only part neither of them is any good at pretending.",

    # FACTS: A shy teen gamer has secretly posed as a boy online for years, forming a deep bond with h
    # FACTS: er teammate Jupiter, who turns out to be TJ, the popular jock she secretly likes at schoo
    # FACTS: l. When their esports team earns a shot at a live tournament, her hidden identity unravel
    # FACTS: s, putting her friendships, her team, and her first love at risk. Now she must choose bet
    # FACTS: ween the safety of the persona that protected her and the truth that could cost her every
    # FACTS: thing.
    'life-is-not-a-game':
        "Online she has been a boy for years. The tournament is in person.\nShe is quiet at school and somebody else entirely once she is online, where she has played as a boy for so long that nobody on her team knows any different. The teammate she is closest to goes by Jupiter, and what they have built over the years is the realest thing she has. Then she works out that Jupiter is TJ, the popular boy at school she has quietly had a crush on. Their esports team qualifies for a live tournament, and the person she invented cannot go with her. Telling the truth costs her the team, her friends and him. Saying nothing costs her the only place she has ever been herself.",

    # FACTS: Cheer Up Baby follows Jane, a high school mascot who hits rock bottom when a tornado dest
    # FACTS: roys her home and school bullies push her to the limit. Forced into an unexpected living
    # FACTS: arrangement, she reunites with her childhood nemesis, a boy she once teased as "Tubby." H
    # FACTS: owever, the boy she remembered is gone, replaced by the tall, handsome captain of the bas
    # FACTS: ketball team.
    'cheer-up-baby':
        "The tornado takes her house. The boy she used to bully takes her in.\nJane is the school mascot and her year is already going badly before a tornado flattens her home and leaves her with nowhere to sleep. The bullies at school have been working on her for a while, and losing the house is the part that nearly finishes her. The living arrangement she ends up in puts her back under the same roof as her childhood nemesis, the boy she used to call Tubby to his face. He is not that boy any more. He is tall, he is captain of the basketball team, and Jane has to share a roof with him. Wait until he reminds her what she used to call him.",

    # FACTS: When wealthy Queen Bee Kenzie makes a deal with high school bad boy Clay to be her fake b
    # FACTS: oyfriend and bodyguard, she unknowingly steps into his dangerous world of illegal undergr
    # FACTS: ound fighting. What begins as a transactional arrangement quickly ignites into an undenia
    # FACTS: ble attraction, blurring the lines between protector and lover. But when Clay's brutal fi
    # FACTS: ght ring catches the attention of Kenzie's District Attorney father, their worlds collide
    # FACTS: , forcing Clay to decide if he's willing to risk his freedom for the girl he's sworn to p
    # FACTS: rotect.
    'fight-dirty':
        "She hires the school bad boy. She never asks what he does at night.\nKenzie has the money and the run of her school, and the deal she puts to Clay is a simple one. He plays her fake boyfriend, he keeps her safe, and she pays for both. What nobody tells her is that Clay spends his nights in an illegal underground fight ring, and the arrangement walks her straight into it. It stops being a transaction fairly quickly for both of them. Then her father, who is the District Attorney, starts taking an interest in exactly where Clay has been fighting, and Clay has to decide whether the girl he promised to protect is worth going to prison for.",
}


# The platform text each caption was written from, fetched live 20 Sep 2026.
# Banked with its URL in facts_reddit6_2026-09-20.json.
FACTS = {
    'faking-it-with-the-hockey-captain':
        "Scholarship girl Julie has one reckless, electric night with the irresistibly hot new hockey captain-only to discover he's Liam, the childhood enemy she can't stand. To kill rumors and keep their exes away, they fake-date. But the chemistry feels anything but fake, and the tension between them is getting dangerously hard to resist.",
    'life-is-not-a-game':
        'A shy teen gamer has secretly posed as a boy online for years, forming a deep bond with her teammate Jupiter, who turns out to be TJ, the popular jock she secretly likes at school. When their esports team earns a shot at a live tournament, her hidden identity unravels, putting her friendships, her team, and her first love at risk. Now she must choose between the safety of the persona that protected her and the truth that could cost her everything.',
    'cheer-up-baby':
        'Cheer Up Baby follows Jane, a high school mascot who hits rock bottom when a tornado destroys her home and school bullies push her to the limit. Forced into an unexpected living arrangement, she reunites with her childhood nemesis, a boy she once teased as "Tubby." However, the boy she remembered is gone, replaced by the tall, handsome captain of the basketball team.',
    'fight-dirty':
        "When wealthy Queen Bee Kenzie makes a deal with high school bad boy Clay to be her fake boyfriend and bodyguard, she unknowingly steps into his dangerous world of illegal underground fighting. What begins as a transactional arrangement quickly ignites into an undeniable attraction, blurring the lines between protector and lover. But when Clay's brutal fight ring catches the attention of Kenzie's District Attorney father, their worlds collide, forcing Clay to decide if he's willing to risk his freedom for the girl he's sworn to protect.",
}

# kind -> where. All four are the title's own page on the platform that carries it.
SOURCES = {
    'faking-it-with-the-hockey-captain': ('platform', 'https://www.dramaboxdb.com/movie/42000010167/faking-it-with-the-hockey-captain'),
    'life-is-not-a-game': ('platform', 'https://candyjar.com/en/series/life-is-not-a-game-589'),
    'cheer-up-baby': ('platform', 'https://pinedrama.com/dramas/cheer-up-baby'),
    'fight-dirty': ('platform', 'https://candyjar.com/en/series/fight-dirty-634'),
}
