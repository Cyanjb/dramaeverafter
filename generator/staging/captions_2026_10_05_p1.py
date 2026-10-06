# -*- coding: utf-8 -*-
"""Sunday caption batch 5 Oct 2026, part 1, new titles from the weekly scrape.
STAGED FOR CYAN'S REVIEW via PR, not approved.

12 written of 14 assigned. Every caption is written from the ReelShort book the
title's page LINKS to (availability.csv direct_link); the live page was fetched
on 5 Oct 2026 and its __NEXT_DATA__ description matched the queue facts word for
word, so FACTS below is that page text.

SKIPPED, needs Cyan or a better source (no caption written, nothing invented):
  fighting-the-fire: ReelShort publishes one sentence and nothing else (a
    firefighter of 15 years facing 'the fire burning inside'). No plot, no
    other characters, no events. A stub, not a story.
  on-the-day-of-the-broken-engagement-i-married-a-half-blood-dragon: the page
    text is a production pitch (palette, visual tone, theme), not a synopsis.
    It names only Luke and an unnamed female lead, and says nothing about the
    broken engagement or the marriage the title promises.

THIN BUT USABLE, flagged so she knows the caption is as long as the source allows:
  prep-school-pop-star (two sentences, no fuller text on the page),
  secrets-and-soulmates (an ensemble premise with no named characters),
  dirty-games and the-ceo-s-genius-baby (premise only).
"""

CAPTIONS = {
    # 17.9M  Secrets and Soulmates
    'secrets-and-soulmates':
        "Everyone in the house has a soulmate. Nobody knows who.\nA handful of good looking singles agree to share one house, and they're all there for the same reason. Somewhere under that roof, each of them has a match they haven't spotted yet, and the whole point is to work out who it is. That's harder than it sounds when everybody is keeping something back, temptation is waiting at every turn and the challenges are as sexy as they come. Will they recognize the person fate picked for them, or give their heart to the wrong one?",
    # 11.1M  Dirty Games
    'dirty-games':
        "The audience picks the challenges. The winners take home cash.\nLucy can't believe her luck when she's picked for a game show that streams online and plays out like reality TV. The rules are simple. Viewers send in the challenges, the contestants carry them out, and the ones who do can win serious money. At first it's all fun. Then the requests coming in from the audience start getting darker and more twisted, and Lucy is right in the middle of it. How far is she willing to go for the money?",
    # 7.7M  The Boss Forces My Heart.
    'the-boss-forces-my-heart':
        "She hired a man for the night. He turned out to be the mafia boss.\nSeren Voss walks in on her fiance with her stepsister, and in a fury she marches into an exclusive club and pays a stranger to spend the night with her. She has no idea she's just hired Kael Rizzo, the mafia boss everyone in the city is afraid of. Kael likes her nerve and isn't ready to let her go, so he binds her to him with a debt deal that runs for three months. It starts out as a risky flirtation and quickly turns into something neither of them can fight. But family betrayal, rival gangs, an abduction and a jealous ex are all closing in. Seren has become Kael's one weak spot, the only woman who has ever reached his heart, and if they want a future together they'll have to get through every enemy set on pulling them apart.",
    # 5.5M  Mated to My Sworn Enemy
    'mated-to-my-sworn-enemy':
        "She watched her family die. Now fate has paired her with the Alpha she blames.\nSamara Brenner is nine years old when she sees her family slaughtered, and she's the last heir of the White Wolf bloodline. She gets away, and for the next nine years she lives under a name that isn't hers, passing herself off as a weak Omega while she quietly gets ready for revenge. Then she finds out who she's meant to be with. Roman Hartwell, her fated mate, is the Alpha she has always believed had a hand in the massacre. Her hatred slowly gives way to a trust she doesn't want to feel, and then the truth hits her hard. Roman has been looking for her for years, and all that time he's been tracking down whoever was really behind the betrayal. Together they set out to expose a conspiracy that runs deep into both their families and take back her pack. But after nine years of living for vengeance, can Samara let love win?",
    # 3.9M  CLAIMED BY MY ALPHA STEPBROTHER
    'claimed-by-my-alpha-stepbrother':
        "One week to find her wolf, or she's out of the pack.\nEvery wolf in Tess's pack has shifted except her, and if she can't make it happen by next week she'll be thrown out for good. The only one who can help her is Jaxon. He's her Alpha's son, he's her stepbrother and he's her enemy. But whenever he gets near, her wolf wakes up like never before, and the hatred she's held onto for so long starts to feel like a story she's been telling herself. There's one problem. Under pack law, the next Alpha is never allowed a wolfless mate, and that's exactly what Tess is.",
    # 2.3M  Prep School Pop Star!
    'prep-school-pop-star':
        "Her best friend got famous on her voice. Then she took her boyfriend too.\nAriana is a secret heiress, and she's also the real singer who made her best friend famous. The beautiful voice people hear is Ariana's, but her friend is the one who gets the credit. Then that same friend steals Ariana's boyfriend as well. That's when her childhood friend comes back, and he's now the school heartthrob and the MVP. Her best friend has taken her voice and her boyfriend, and nobody knows who Ariana really is.",
    # 2.0M  The Godfather's Hidden Wife
    'the-godfather-s-hidden-wife':
        "She was carrying the Godfather's only heir. Nobody was supposed to know.\nEvelyn is secretly married to Damian Moretti, the Godfather, and the baby she's expecting is his only heir. He keeps her out of sight to protect her. But because nobody knows she's his wife, Bianca takes her for a mistress Damian has cast aside. Bianca humiliates her cruelly, and Evelyn loses her unborn child at Bianca's hands. Once Damian learns what really happened, he leaves it to Evelyn to decide how every last person involved is punished. A month later the gentle wife is gone. In her place is the true Lady Moretti, and every person who hurt her is about to pay.",
    # 1.3M  The Swap Game: Claimed by His Uncle
    'the-swap-game-claimed-by-his-uncle':
        "Her fiance tricked her into a swinger party. She ended up in his uncle's suite.\nChloe's fiance lies to get her to a swinger party, and she walks into the wrong suite by mistake. It belongs to his uncle Victor. After one night of giving in, her fiance dumps her and humiliates her, and Victor takes her by force and keeps her locked up, treating her like something he owns and uses. When she gets pregnant she pays for it. She's sold off, and the only way out is to fake her own death in a fire and run. Three years later Chloe comes back looking stunning, with her daughter beside her. Now Victor is the one doing the chasing, desperate to win back the woman he wronged. There are misunderstandings to clear up first, and after everything he put her through, Victor has a lot to make up for.",
    # 1.1M  Forced to Bear the Dragon's Heir
    'forced-to-bear-the-dragon-s-heir':
        "The substitute bride was only meant to give him an heir.\nA thousand years ago the dragons rescued the elves from the orcs, and ever since, each new Dragon King has been owed a princess who's a virgin. Lora is the elven king's daughter, born outside his marriage, and her stepmother blackmails her into going as the dragon's bride instead of Princess Bella. But Prince Draven is nothing like the tyrant in the old stories. He makes her an offer. If she gives him an heir, her mother goes free and so does she. Day after day Draven falls harder for her kindness, and Lora lets him in and chooses to carry his child. Then the orcs come back and Draven is badly hurt. Bella turns up claiming to be the real princess and turns Draven against Lora. Hurt and misunderstood, Lora leaves, and the orcs grab her to use against him. Draven puts everything on the line to get her back, drives the orcs off and shows everyone what Bella has been doing. By the end, the bastard bride sent in someone else's place becomes the Dragon King's true queen.",
    # 1.0M  The CEO's Genius Baby
    'the-ceo-s-genius-baby':
        "She stood in for her sister for one night with a CEO.\nFive years ago she spent one night with a powerful CEO in her sister's place, and afterwards she was made to leave the country. Now she's back, and she hasn't come home alone. Her child is a little genius. Then she finds out that the man who holds all that power is her baby's father. The night she spent as someone else has caught up with her, and this time there's a child in the middle of it.",
    # 828.5K  The Don's Fatal Tenderness
    'the-don-s-fatal-tenderness':
        "Humiliated at City Hall by her fiance. Five years later she's the Don's wife.\nLainey's fiance Leo shames her at City Hall by marrying Rosalie instead, because Rosalie is pregnant and the match gets him power. Lainey runs to New York and marries Don Falcone Marcus, who adores her, and she becomes the mother of his son. Five years on she's back in Chicago, and Leo and Rosalie mock her, snatch her bracelet and hit her across the face. They come after her a second time, this time at Marcus's gala, until her little boy Gable calls out for his mommy and everyone learns who Lainey really is. Marcus arrives in a rage. Rosalie stabs Lainey and then dies, and Leo is caught. Then Lainey finds out Marcus has loved her in secret for years, and they finally find their way back to each other.",
    # 477.3K  God of Wrath
    'god-of-wrath':
        "She saved the mafia heir. He won't stop until she's his.\nAdapted from Rina Kent's novel. Cecily Knight is a good girl at university who has quietly wanted popular golden boy Landon King for years. All of that changes the moment she acts on impulse and saves Jeremy Volkov. He's a brutal mafia heir, Landon's most dangerous rival, and a man who'll do whatever it takes to make Cecily belong to him. As the truth about how Landon has been manipulating her slowly comes out, Jeremy keeps coming for her, and his pursuit wakes up a dark side of Cecily she never knew she had. Now she has to choose between the boy she always thought she wanted and the man whose danger she can't resist.",
}

FACTS = {
    'secrets-and-soulmates':
        "A group of sexy singles move in together with one unforgettable goal: uncover their secret soulmate. Each person has a hidden match living alongside them, but finding true love isn't easy when secrets, temptations, and sexy challenges are around every corner. Will our singles recognize true, fated love—or choose the wrong heart?",
    'dirty-games':
        'Lucy is excited to be chosen for a reality TV style game show, being streamed online, where contestants complete challenges sent in by the audience, to win big cash prizes. The fun soon turns sinister, as the viewer requests become more perverse.',
    'the-boss-forces-my-heart':
        'After catching her fiancé with her stepsister, Seren Voss storms into an exclusive club and impulsively hires a man for the night—unaware that he is Kael Rizzo, the city’s most feared mafia boss. Amused by her audacity and determined to keep her close, Kael binds her to a three-month debt agreement. What begins as a dangerous game of attraction soon becomes something neither can resist. But as family betrayal, rival gangs, abduction, and a jealous former partner close in, Seren becomes Kael’s greatest weakness—and the only woman capable of capturing his heart. To claim their future, they must survive the enemies determined to tear them apart.',
    'mated-to-my-sworn-enemy':
        "When nine-year-old Samara Brenner, the last heir of the legendary White Wolf bloodline, witnesses her family slaughtered, she escapes and spends the next nine years hiding under a false identity, pretending to be a weak Omega while preparing for revenge. Her plan unravels when she discovers her fated mate is Roman Hartwell, the Alpha she has believed was complicit in her family's massacre. As hatred turns into reluctant trust, Samara uncovers a devastating truth: Roman has spent years searching for her and hunting the real mastermind behind the betrayal. Together, they must expose a conspiracy that reaches deep into their own families, reclaim her pack, and decide whether love is stronger than vengeance.",
    'claimed-by-my-alpha-stepbrother':
        "Tess is the only wolf in her pack who hasn't shifted — and if she doesn't figure it out by next week, she's out for good. Her only hope is Jaxon: her Alpha's son, her step-brother, her enemy. But the moment he's close, everything changes — her wolf stirs closer than ever, and the hatred she's clung to starts feeling like a lie. There's just one problem: pack law says a future Alpha can never take a wolfless mate.",
    'prep-school-pop-star':
        "Secret heiress Ariana is the angelic voice behind her best friend's fame. When that bestie steals her boyfriend too, Ariana's childhood friend—the school heartthrob and MVP —comes back.",
    'the-godfather-s-hidden-wife':
        'Evelyn is the Godfather Damian Moretti’s secret wife, carrying his only heir. Hidden away for her safety, she is mistaken for a discarded mistress by Bianca, who brutally humiliates her and kills her unborn child. When Damian discovers the truth, he gives Evelyn the power to punish everyone involved. One month later, the gentle wife returns as the true Lady Moretti, and no one who wronged her will escape.',
    'the-swap-game-claimed-by-his-uncle':
        'Chloe was tricked by her fiancé into attending a swinger party and accidentally entered the suite of his uncle Victor. After a night of indulgence, she was abandoned and humiliated by her fiancé, then forcibly possessed and imprisoned by Victor, reduced to a mere tool. After becoming pregnant, she suffered retaliation, was sold off, faked her death in a fire, and escaped. Three years later, she makes a glamorous return with her daughter. Victor embarks on a “wife-chasing crematorium,” and eventually the misunderstandings are cleared, culminating in a grand wedding and a happy ending for the family of three.',
    'forced-to-bear-the-dragon-s-heir':
        'A thousand years ago, dragons saved the elves from orcs—but demanded a virgin princess for every new Dragon King. Lora, the elven king’s illegitimate daughter, is blackmailed by her stepmother into taking Princess Bella’s place as the dragon bride. But Prince Draven isn’t the tyrant of legend. He offers a deal: give him an heir, and he’ll free her mother and grant her freedom. Day by day, Draven falls for Lora’s gentle heart. She opens to him and willingly carries his child. Then the orcs return, and Draven is gravely wounded. Bella arrives, playing the “true princess,” poisoning Draven’s trust in Lora. Heartsick and misunderstood, Lora walks away—only to be kidnapped by orcs as leverage. Draven risks everything to save her, drives back the orcs, and exposes Bella’s schemes. In the end, the bastard bride becomes the Dragon King’s one true queen.',
    'the-ceo-s-genius-baby':
        "Five years ago, she took her sister's place in a one-night entanglement with a powerful CEO and was forced to leave the country. Five years later, she returns with a genius baby, only to discover that the all-powerful man is the child's father.",
    'the-don-s-fatal-tenderness':
        'Lainey is humiliated by her fiancé Leo at City Hall, who marries pregnant Rosalie for power. She flees to New York, marries Don Falcone Marcus, and becomes his cherished wife and mother of their son. Five years later, back in Chicago, Leo and Rosalie mock her, steal her bracelet, and slap her. At Marcus’s gala, they attack her again. Their son Gable cries out for Mommy—exposing Lainey’s identity. Marcus arrives, enraged. Rosalie stabs Lainey, then dies. Leo is captured. Lainey discovers Marcus secretly loved her for years. They reconcile deeply.',
    'god-of-wrath':
        "Based on the novel by Rina Kent. Good-girl university student Cecily Knight has spent years pining after popular golden boy Landon King. But everything changes when she impulsively saves Jeremy Volkov: Brutal mafia heir, Landon's deadliest rival, and the one man who will stop at nothing to make Cecily his. As Landon's manipulation is slowly exposed and Jeremy's relentless pursuit awakens something dark in Cecily she never knew existed, she must choose between the boy she thought she wanted and the dangerous man she can't stop craving.",
}

SOURCES = {
    'secrets-and-soulmates': ('platform', 'https://www.reelshort.com/movie/secrets-and-soulmates-697b24657630003c87070a55'),
    'dirty-games': ('platform', 'https://www.reelshort.com/movie/dirty-games-68244b101a86d1ee5f03bfd9'),
    'the-boss-forces-my-heart': ('platform', 'https://www.reelshort.com/movie/the-boss-forces-my-heart-6ab9c2a17e569c9b2506f8e7'),
    'mated-to-my-sworn-enemy': ('platform', 'https://www.reelshort.com/movie/mated-to-my-sworn-enemy-6a9e210d6851b4c2d303c2cb'),
    'claimed-by-my-alpha-stepbrother': ('platform', 'https://www.reelshort.com/movie/claimed-by-my-alpha-stepbrother-6ab090e57087873df908c6d9'),
    'prep-school-pop-star': ('platform', 'https://www.reelshort.com/movie/prep-school-pop-star-6aabe2c2ddeda4f8620cf697'),
    'the-godfather-s-hidden-wife': ('platform', 'https://www.reelshort.com/movie/the-godfather-s-hidden-wife-6a9e1564668ea4a80b077b17'),
    'the-swap-game-claimed-by-his-uncle': ('platform', 'https://www.reelshort.com/movie/the-swap-game-claimed-by-his-uncle-6ab0f32835b6b75a6d031850'),
    'forced-to-bear-the-dragon-s-heir': ('platform', 'https://www.reelshort.com/movie/forced-to-bear-the-dragon-s-heir-6ab49d3661f3258f2d05a8db'),
    'the-ceo-s-genius-baby': ('platform', 'https://www.reelshort.com/movie/the-ceo-s-genius-baby-6ab4caad55d7dfdf17051310'),
    'the-don-s-fatal-tenderness': ('platform', 'https://www.reelshort.com/movie/the-don-s-fatal-tenderness-6aaa11db6f352adbdf0772d6'),
    'god-of-wrath': ('platform', 'https://www.reelshort.com/movie/god-of-wrath-6aac82d6cb3883b74605b9b8'),
}
