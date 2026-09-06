# -*- coding: utf-8 -*-
"""Widget batch, 6 Sep 2026. UNAPPROVED DRAFT.

Cyan, 6 Sep: a fresh widget with the ones she has done removed, plus the
new ones from the AI titles and the front page that still need writing.
These are all ABOVE the top-300 reach floor or on the homepage, so her
16 Aug ruling says they get her eye. Do NOT apply without her review.

Three from the list are not here and need her or a better source:
  first-daughter-forbidden-duty      no platform link on the row at all
  when-the-wolf-fell-in-love         platform text is truncated boilerplate
  the-mafias-stolen-bride-twin-switch  platform text is a marketing blurb
"""

CAPTIONS = {
    # FACTS: In Abandoned Pawn Unrivaled Dragon King movie, Owen — discarded heir of the Hull family, the one
    # FACTS:  and only disciple of the master of the Dragon Knight Sanctum. He awakens the Ten Dragon God Mar
    # FACTS: ks and forges a soul-deep bond with Akura, bearer of the ancient Golden Dragon bloodline. Betray
    # FACTS: ed by his own family, stripped of his name, and tormented by the very Sanctum that should have b
    # FACTS: een his home — when the buried truth finally breaks free, the outcast of old rises in the full w
    # FACTS: rath of a Dragon God and grinds every last humiliation to dust. From that moment on, the young d
    # FACTS: ragonlord sets forth across the land with his dragon at his side, and the entire continent shudd
    'abandoned-pawn-unrivaled-dragon-king':
        'Stripped of his name by his own family.\nOwen is the discarded heir of the Hull family and the only disciple of the master of the Dragon Knight Sanctum. He awakens the Ten Dragon God Marks and bonds soul deep with Akura, who carries the ancient Golden Dragon bloodline. His family betray him, take his name, and the Sanctum that should have been home torments him instead. Then the buried truth gets out, the outcast rises in the full wrath of a Dragon God, and the continent starts to feel it.',

    # FACTS: Trapped in an arranged marriage to the cold and dangerously seductive heir of the New York mafia
    # FACTS: , LUCA, 18yo sheltered mafia princess from Chicago, ARIA must decide if surrendering her body—an
    # FACTS: d maybe her heart—to a man born of violence is her greatest betrayal or her only chance at survi
    # FACTS: val.
    'bound-by-honor':
        'Married off at eighteen to the man Chicago fears.\nAria is a sheltered mafia princess from Chicago, handed into an arranged marriage with Luca, the cold and dangerously seductive heir of the New York mafia. What she has to work out is whether giving her body, and possibly her heart, to a man born of violence is the worst betrayal she could commit or the only thing that keeps her alive.',

    # FACTS: Best friends Ella and Leah married the Harper brothers, firefighter Charles and doctor Noah. On 
    # FACTS: their third anniversary, Charles’s first love locks Ella inside a burning room. When Ella begs C
    # FACTS: harles for help, he brushes her off to find his ex's cat. Leah rushes in to rescue Ella and call
    # FACTS: s Noah to save Ella and her baby, but is met with mockery. Heartbroken and betrayed after years 
    # FACTS: of miserable marriages, the best friends decide to file for divorce from the Harper brothers tog
    # FACTS: ether.
    'brides-in-smoke':
        "He went to find his ex's cat while his wife burned.\nElla and Leah are best friends married to the Harper brothers, firefighter Charles and doctor Noah. On their third anniversary, Charles's first love locks Ella in a burning room, and when Ella begs him for help he brushes her off to go and find the cat. Leah runs in after her and calls Noah to save Ella and her baby, and gets mocked for it. After years of miserable marriage, they file for divorce from the Harper brothers together.",

    # FACTS: Fay Thompson thought she understood the mafia world -- but the arrival of a scheming rival, a sh
    # FACTS: ocking pregnancy, and her lover's arrest will force her to become the Mafia Queen she was always
    # FACTS:  meant to be, or lose Kent Lippert forever.
    'falling-for-my-ex-s-mafia-dad-2':
        'She thought she understood this world. Then he was arrested.\nFay Thompson has learned the mafia well enough to think she has it, and then a scheming rival arrives, a pregnancy lands, and her lover is taken into custody. She becomes the Mafia Queen she was always going to be, or she loses Kent Lippert for good.',

    # FACTS: In Honey-Trapped My Fiancé's Billionaire Rival movie, after ten years of loving Ryan, Jade Gray 
    # FACTS: is asked to seduce his billionaire rival, Asher Blackwood, to help save Ryan’s first love, Elean
    # FACTS: or. But Asher secretly has feelings for Jade, turning Ryan’s carefully planned scheme into a dan
    # FACTS: gerous love triangle. As Jade grows closer to Asher, she begins to question who truly deserves h
    # FACTS: er love.
    'honey-trapped-my-fiance-s-billionaire-rival':
        "He asked her to seduce his rival. For another woman.\nJade Gray has loved Ryan for ten years, and what he wants from her now is to honey trap his billionaire rival Asher Blackwood so that Ryan's first love Eleanor can be saved. What none of them planned for is that Asher already has feelings for Jade, which turns a careful scheme into a dangerous love triangle. The closer she gets to Asher, the harder it is to keep believing Ryan deserves her.",

    # FACTS: In In Bed with My Brother-in-Law movie, Bella's arranged marriage becomes a nightmare when she c
    # FACTS: atches her fiancé cheating. Seeking revenge, she sleeps with a stranger, unwittingly bedding her
    # FACTS:  fiancé's powerful mafia boss brother, Damian Gotti. Forced back into the Gotti family, Bella fa
    # FACTS: ces dangerous secrets and forbidden desires. Damian relentlessly pursues her under his brother's
    # FACTS:  nose. Eventually, Damian exposes his brother's crimes, saves Bella, and they unite to defend th
    # FACTS: eir mafia throne.
    'in-bed-with-my-brother-in-law':
        "Revenge sex with a stranger, who turns out to be his brother.\nBella's arranged marriage goes wrong the moment she catches her fiance cheating, so she sleeps with a stranger to even the score and beds Damian Gotti, her fiance's powerful mafia boss brother. Forced back into the Gotti family, she is surrounded by dangerous secrets and things she is not supposed to want, and Damian pursues her relentlessly right under his brother's nose. In the end he exposes his brother's crimes and they hold the mafia throne together.",

    # FACTS: In My Billionaire Boss Won't Let Me Quit movie, seeking a fresh start after years of managing cr
    # FACTS: ises, Grace takes on a new job, only to be swept into a fake marriage by her enigmatic boss, Mas
    # FACTS: on. As their pretend arrangement blurs into undeniable passion, Grace falls deeper into his spel
    # FACTS: l. But Mason is playing a far more dangerous game—and he has no intention of ever letting her go
    # FACTS: .
    'my-billionaire-boss-won-t-let-me-quit':
        "She wanted a fresh start. He wanted a wife.\nGrace has spent years managing other people's crises and takes a new job to get away from it, and her enigmatic boss Mason sweeps her into a fake marriage almost immediately. The pretending stops being pretending faster than she expects and she falls hard. What she has not seen is that Mason is playing a much more dangerous game, and letting her go was never in it.",

    # FACTS: After claiming her fifth World Culinary Championship, the legendary Chef Sage goes undercover as
    # FACTS:  a homeless beggar to find a partner with genuine character. Ignored by the masses and ruthlessl
    # FACTS: y mocked by her ex, she encounters Jasper, a kind-hearted man who offers her his food. Desperate
    # FACTS:  to save his family's failing restaurant from a vicious corporate takeover, Jasper hires Sage to
    # FACTS:  play his wealthy fake fiancée. As rival factions push the Vance family to the brink with a high
    # FACTS: -stakes "Culinary Death Match," all hope seems lost. But when cornered, the beggar bride sheds h
    # FACTS: er disguise. With a flash of her blade and her signature blue flame, she turns the tables agains
    'my-homeless-bride-is-a-culinary-legend':
        "Five world titles, and she is begging on the street on purpose.\nChef Sage goes undercover as a homeless beggar to find a partner with real character, and gets ignored by everyone and mocked by her ex. Jasper offers her his food. He is also desperate to save his family's failing restaurant from a vicious takeover, so he hires her to play his wealthy fake fiancee. When rival factions push the Vance family into a high stakes Culinary Death Match and it all looks lost, the beggar bride drops the disguise, and her blade and her blue flame do the rest.",

    # FACTS: In Shattered Vows movie, princess Venessa lived a sheltered life—until her sister was murdered. 
    # FACTS: Stripped of her innocence in a single night, she must confront a devastating betrayal: her husba
    # FACTS: nd and best friend just helped the killer escape justice. The pampered princess is gone. Now she
    # FACTS: 's coming for every last one of them, to take back the justice they owe her sister.
    'shattered-vows':
        "Her husband helped her sister's killer walk free.\nPrincess Venessa lived a sheltered life until her sister was murdered, and one night takes all of that away from her. The betrayal she has to look at is the worst kind: the two people closest to her, her husband and her best friend, helped the killer escape justice. The pampered princess is finished. What comes next is her collecting, from every one of them, what they owe her sister.",

    # FACTS: In Sold to the Warlord Born for the Sky movie, a sheltered northern princess who was sold into m
    # FACTS: arriage to the dragon-riding warlord of the brutal Blackclaw horde must decide whether surrender
    # FACTS: ing to the man who bought her is her greatest betrayal or the only thing that can save her dying
    # FACTS:  people.
    'sold-to-the-warlord-born-for-the-sky':
        'Sold north to south, to a man who rides dragons.\nA sheltered northern princess is sold into marriage with the dragon riding warlord of the brutal Blackclaw horde, and the question in front of her does not get easier the longer she looks at it. Surrendering to the man who bought her is either the worst thing she could do, or the only thing that saves her dying people.',

    # FACTS: Pampered real alpha princess Evie is framed and sent to the ruthless Werewolf Military Academy b
    # FACTS: y her own family. They believe she is living comfortably, completely unaware that under the fake
    # FACTS:  alpha princess's orders, Evie suffers brutal abuse. Three years later, she returns, broken insi
    # FACTS: de, yet her family still views her as a spoiled brat. It is only when her father strikes her and
    # FACTS:  her prosthetic limb falls off that they finally realize the horrifying truth...
    'the-alpha-princess-is-gone-for-good':
        "Her family thought she was living comfortably.\nEvie is the real alpha princess, framed by her own family and sent to the ruthless Werewolf Military Academy, and they have no idea that under the fake alpha princess's orders she is being brutally abused there. Three years later she comes home broken inside and they still see a spoiled brat. It takes her father striking her, and her prosthetic limb coming off in front of them, before any of them understand what they did.",

    # FACTS: Elijah Baran is a genie in a magic lamp who can grant three wishes. After thousands of years, a 
    # FACTS: billionaire uses his last wish to grant Elijah freedom, but on one condition: Elijah must marry 
    # FACTS: his granddaughter, Christine, for five years! To fulfill the wish, Elijah transforms into a huma
    # FACTS: n, marries Christine, and secretly helps her become a successful CEO. However, Christine ignores
    # FACTS:  and constantly belittles him during their marriage. When the five years are almost up, Elijah s
    # FACTS: tarts to realize that Christine might never truly love him. He decides to divorce her.
    'the-great-and-powerful-genie':
        "Three wishes, and the last one bought him a wife.\nElijah Baran has spent thousands of years in a magic lamp granting wishes when a billionaire spends his final one on setting Elijah free, with a condition attached. He has to marry the man's granddaughter Christine and stay married for five years. So the genie turns human, takes the vows, and quietly builds her into a successful CEO while she ignores and belittles him. With the five years nearly up, Elijah works out that she may never love him, and decides on a divorce.",

    # FACTS: Wren is labeled wolfless and abandoned by her childhood lover Tristan at his coronation, who pub
    # FACTS: licly rejects their mate bond and lets his lover cut her hair. Heartbroken, she leaves the Dark 
    # FACTS: Moon pack and enters the elite Apex Academy. There, she awakens the rare powerful White Wolf blo
    # FACTS: odline hidden inside her. With the quiet Frost heir Killian's support, Wren defeats rivals, unco
    # FACTS: vers Vaelen's evil plot that preys on wolfkin's blood power, and rescues her dad. She stands sid
    # FACTS: e by side with Killian to build a new order where no one is forced to kneel for power.
    'the-lycan-s-savage-luna':
        "Rejected at his coronation, and they cut her hair.\nWren is written off as wolfless and abandoned by her childhood love Tristan, who rejects their mate bond publicly and stands there while his lover takes a blade to her hair. She leaves the Dark Moon pack for the elite Apex Academy, where the rare White Wolf bloodline hidden in her wakes up. With the quiet Frost heir Killian behind her she beats every rival, exposes Vaelen's plot to feed on wolfkin blood power and gets her father out, and together they start building an order where nobody kneels for power.",

    # FACTS: In The Valkyrie Divorces the God of War movie, to protect his wife, God King Kairos sealed his d
    # FACTS: ivine powers and feigned being a worthless mortal. Instead of gratitude, Cassia returned bearing
    # FACTS:  her lover's child, demanding the family relic while humiliating him publicly. Driven past his l
    # FACTS: imit, Kairos shattered his shackles, awakening his supreme godhood. He exposed her lover as an a
    # FACTS: byssal spy, leading to the traitor's execution. Begging for mercy, Cassia fled in exile, as the 
    # FACTS: God King reclaimed his absolute throne.
    'the-valkyrie-divorces-the-god-of-war':
        "He sealed his godhood for her. She came back pregnant.\nGod King Kairos gave up his divine powers and played a worthless mortal to keep his wife safe, and Cassia returned carrying her lover's child, demanding the family relic and humiliating him in public. Pushed past what he can hold, Kairos breaks the shackles and his supreme godhood comes back. He exposes her lover as an abyssal spy, the traitor is executed, and Cassia is begging by the time she flees into exile.",

    # FACTS: In Zero to Alpha Return of the Wolf King movie, exiled for failing to awaken his wolf form, Nory
    # FACTS:  trained twenty years under three Masters beyond Sacred Rank. Returning to see his mother, he en
    # FACTS: ters the Clan Tournament, shatters the test stone, crushes every foe, and is revealed as the sav
    # FACTS: ior three Gold Leaders sought. When vampires invade, he slams the Legendary First Sire through s
    # FACTS: even walls. Learning his mother was injured saving him, he gathers three sacred relics to heal h
    # FACTS: er. But crimson eyes in distant mist hint a greater threat.
    'zero-to-alpha-return-of-the-wolf-king':
        'Exiled for having no wolf, back with twenty years of training.\nNory could not awaken his wolf form, so they threw him out, and he spent two decades under three Masters beyond Sacred Rank. He comes home to see his mother, enters the Clan Tournament, shatters the test stone and goes through every opponent, which is when three Gold Leaders realise he is the savior they were looking for. When vampires invade he puts the Legendary First Sire through seven walls. Then he learns his mother was hurt saving him, and goes after three sacred relics to heal her.',

}
