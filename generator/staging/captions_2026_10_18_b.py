# -*- coding: utf-8 -*-
"""New titles from the 18 Oct 2026 ReelShort scrape, second half (19 titles).

Every caption is written from the ReelShort book the title page LINKS to
(data/availability.csv direct_link, matched on the 24 hex book id, not the
slug). Sources: generator/staging/reelshort_2026-10-18.json, and
reelshort_2026-10-11.json for eight-years-gone-down-the-drain,
fire-ice-return-of-the-alpha-queen-s-sister and too-late-to-be-your-only-one.

Skipped: none. All 19 books publish a synopsis with a story in it.
Thin source, written short rather than padded: her-baby-daddy-is-the-last-
dragon-knight (three sentences, no character names, so none are used).
"""

BATCH_TAG = "New 18 Oct"

CAPTIONS = {

    # FACTS: Clara, a young widow, shares one night with a stranger in the castle rose garden—not knowing he’s
    # FACTS: Crown Prince Gabriel. Pregnant, she leaves her baby and a golden ring on the castle steps to save
    # FACTS: him from a tyrant. She becomes a wet nurse at the castle, nursing the little prince who refuses all
    # FACTS: others—without knowing he’s her son, and the cold prince is her one-night stranger. When the truth
    # FACTS: surfaces, Gabriel crowns her queen.
    # FACTS: https://www.reelshort.com/movie/claimed-by-the-prince-the-forbidden-wet-nurse-6aa221dcce316629590e2bed
    'claimed-by-the-prince-the-forbidden-wet-nurse':
        "She gave up her baby to save him. Now she's his wet nurse.\nClara is a young widow, and in the castle's rose garden she spends one night with a man she doesn't know. She has no idea he's Crown Prince Gabriel. When she finds out she's pregnant, she leaves her baby on the castle steps with a golden ring, to keep him safe from a tyrant. Later Clara takes work at the castle as a wet nurse, and the little prince, who has refused everyone else, will feed from her. What she doesn't know is that the baby in her arms is her own son, and that the stranger from the garden was the cold prince all along. When the truth finally comes out, Gabriel makes her his queen.",

    # FACTS: Eve helped Noah build Black Tech from nothing, only to discover he has married the intern Mia and
    # FACTS: plans to hand her Eve's biggest project. At the Grant signing ceremony, Eve reveals her true
    # FACTS: identity as the Grant Group heiress and exposes Mia's leak, Noah's entitlement, and the cost of
    # FACTS: eight wasted years. Walking away from his collapse, she signs back the life that always belonged to
    # FACTS: her.
    # FACTS: https://www.reelshort.com/movie/eight-years-gone-down-the-drain-6a5724f41fd2b06f5e0142b5
    'eight-years-gone-down-the-drain':
        "Eight years building his company. He married the intern.\nEve spent eight years helping Noah turn Black Tech into something out of nothing. Then she learns he's gone and married Mia, the intern, and that he's planning to give Mia the biggest project Eve has. What Noah doesn't know is who Eve really is. At the Grant signing ceremony she reveals that she's the Grant Group heiress, and in front of everyone she lays it all bare: the leak Mia was behind, everything Noah thinks he's owed, and what those eight wasted years cost her. Noah's world comes crashing down, and Eve walks away from the wreckage to sign herself back into the life that was always hers.",

    # FACTS: Vanessa built an empire, paid off her husband’s debts, and funded his family’s lavish lifestyle.
    # FACTS: She's ready to enjoy the family vacation - until she finds out her husband gave away her first-class
    # FACTS: ticket to his ex-girlfriend! Finally, she realizes she's been nothing but a walking ATM to him. Now,
    # FACTS: she's done letting him bleed her dry, and she's going to take back everything she ever gave him!
    # FACTS: https://www.reelshort.com/movie/out-of-your-league-the-billionaire-wife-s-revenge-6ab48e78dc6fd7ef4a06596e
    'out-of-your-league-the-billionaire-wife-s-revenge':
        "She pays for everything. He gave her ticket to his ex.\nVanessa built an empire of her own. She cleared her husband's debts, and she's the one paying for the expensive way his whole family likes to live. Now they're all going on vacation and she's finally ready to relax, until she discovers that her husband has given her seat in first class to his ex girlfriend. That's when it hits her. To him she's never been anything but a walking ATM. Vanessa is done letting him drain her, and she's taking back every single thing she ever gave him.",

    # FACTS: Elena, Luna of the Winters Pack, loves Alpha Roman for ten years, his wife for five, yet he never
    # FACTS: sees her. Jealous stepsister Sienna causes her miscarriage and steals credit for saving Roman,
    # FACTS: leaving Elena blamed. Drained by a life debt that saved Roman, then rejected, Elena severs their
    # FACTS: bond and leaps from a cliff. Only in death does Roman learn every sacrifice was hers. He exposes
    # FACTS: Sienna, confesses too late, and seeks forbidden resurrection, but the ring he needs lies sunk in
    # FACTS: frozen falls.
    # FACTS: https://www.reelshort.com/movie/the-alpha-s-late-regret-6ac72f090816cc72b703a6e9
    'the-alpha-s-late-regret':
        "She saved his life. He only found out after she was gone.\nElena is Luna of the Winters Pack. She has loved Alpha Roman for ten years and been his wife for five, and in all that time he has never really looked at her. Sienna, her jealous stepsister, makes her miscarry, then claims she was the one who saved Roman's life, and somehow Elena ends up with the blame. The truth is that a life debt Elena took on to save Roman has left her drained. When he rejects her, she cuts their bond and throws herself off a cliff. Only once she's dead does Roman learn that every sacrifice had been hers. He exposes Sienna and confesses, far too late. Now he's chasing a forbidden way to bring her back, but the ring he needs is lost beneath a frozen waterfall.",

    # FACTS: 7-year-old Wolf Princess, Ruby Zephyr is cursed, and slowly freezing the heart of her sister, Talia.
    # FACTS: Talia would rather die than leave Ruby, so Ruby runs away, giving up her wolf, and all memory of who
    # FACTS: she is to save her sister. 11 years later, Alpha Queen Talia is determined to reunite with her long
    # FACTS: lost sister. She travels to Crystal Valley High, and finds a brilliant and kind student with her
    # FACTS: sister's violet eyes. As her suspicions grow, Talia sees Ruby mistreated by her peers and must
    # FACTS: intervene, jogging Ruby's memory and unlocking her Ice Wolf. When Ruby's bullies finally realize
    # FACTS: they've been abusing the Alpha Queen and her sister, the lost Ice Wolf Queen, they'll FREEZE with
    # FACTS: regret.
    # FACTS: https://www.reelshort.com/movie/fire-ice-return-of-the-alpha-queen-s-sister-6ab60ad679098aca75062427
    'fire-ice-return-of-the-alpha-queen-s-sister':
        "Her curse was freezing her sister's heart. So she ran.\nRuby Zephyr is a seven year old Wolf Princess, and the curse on her is slowly turning her sister Talia's heart to ice. Talia would sooner die than let her go, so Ruby is the one who leaves. She runs away and gives up her wolf and every memory of who she is, all to keep Talia alive. Eleven years later Talia is the Alpha Queen, and she's determined to find her lost sister. At Crystal Valley High she finds a student who is bright and kind and has her sister's violet eyes. The more Talia sees, the more certain she gets, and when she watches the other students treat Ruby badly, she steps in. That shakes Ruby's memory loose and wakes up her Ice Wolf. Her bullies are about to learn exactly who they've been picking on: the Alpha Queen's long lost sister, the Ice Wolf Queen herself. They're going to regret every minute of it.",

    # FACTS: Serena Vale died with Adrian's silver knife in her chest after her sister Lila screamed, "Serena
    # FACTS: stole my Luna mark." Reborn at the Moon Den, Serena refuses to bleed for Lila again. The mark
    # FACTS: chooses her in front of the pack, and when her former betrothed steps forward, she makes the choice
    # FACTS: that shatters Blackwood: "I choose Rowan Blackwood." Rowan is Adrian's cursed uncle, poisoned into a
    # FACTS: living corpse, but his wolf still answers her. When he wakes and asks who dared touch his Luna,
    # FACTS: Serena's second life turns from survival into war.
    # FACTS: https://www.reelshort.com/movie/reborn-as-the-cursed-alpha-s-luna-6a963bbc7308ebfe9309c899
    'reborn-as-the-cursed-alpha-s-luna':
        "She died on Adrian's silver knife. Reborn, she chose his uncle.\nWhen her sister Lila accused her of stealing her Luna mark, Serena Vale paid for it with her life, killed by Adrian's silver knife. Then she's reborn, back at the Moon Den, and this time she's not bleeding for Lila ever again. In front of the whole pack, the Luna mark picks Serena. When the man she was once promised to steps forward, she names someone else instead: Rowan Blackwood. It's the choice that tears Blackwood apart. Rowan is Adrian's uncle, cursed and poisoned until he's no more than a living corpse. Even so, his wolf answers to her. And when Rowan wakes and demands to know who laid a hand on his Luna, Serena isn't just trying to survive anymore. Now it's war.",

    # FACTS: Silvermoon pureblood Wren waits three years for her fated mate Silas, who rejects her for her
    # FACTS: half-sister Cora on the full moon. Framed and exiled by her family, Wren flees north and accepts
    # FACTS: Bloodmoon Alpha Ridge. When Silas learns Cora lied, it is too late. As Wren bonds with Ridge, Cora
    # FACTS: and Vera are banished, Elias falls comatose, and grief-stricken Silas ends his life in an icy lake.
    # FACTS: https://www.reelshort.com/movie/i-burned-my-wedding-dress-before-he-ever-marked-me-6aba0531e585c7314a06155c
    'i-burned-my-wedding-dress-before-he-ever-marked-me':
        'She waited three years for her mate. He chose her sister.\nWren is a Silvermoon pureblood, and for three years she waits for Silas, her fated mate. Then, under the full moon, he rejects her and picks her half sister Cora instead. Her own family frames her and throws her out, so Wren runs north, where she accepts Ridge, the Bloodmoon Alpha. By the time Silas finds out Cora was lying, Wren is already gone. As her bond with Ridge grows, everything she left behind falls apart. Cora and Vera are both banished, Elias ends up in a coma, and Silas, broken by grief, takes his own life in a frozen lake.',

    # FACTS: Ava loves Ethan for ten years, but he ties her to a flagpole as a cruel "Hanged Man" prank for his
    # FACTS: new crush Chloe, humiliating her before the whole school. Ava finally breaks free, transfers to
    # FACTS: Westbridge High, and cuts Ethan off. At her new school, she meets kind friends and Noah, who
    # FACTS: protects her. Ethan slowly realizes Chloe manipulated him and that Ava truly fears him. He comes to
    # FACTS: apologize, but Ava refuses him. The district punishes Ethan and Chloe. Ava finally smiles, no longer
    # FACTS: looking back.
    # FACTS: https://www.reelshort.com/movie/the-hanged-girl-on-the-flagpole-6ac7076da6819fff2c0e4e43
    'the-hanged-girl-on-the-flagpole':
        "Ten years of loving him, and he tied her to the flagpole.\nAva has loved Ethan for ten years. Then, for the sake of Chloe, his new crush, he ties Ava to the school flagpole as a Hanged Man prank and humiliates her in front of everyone. When Ava finally gets loose, she's done. She switches to Westbridge High and wants nothing more to do with Ethan. At her new school she makes friends who are actually kind to her, and she meets Noah, who looks out for her. Slowly Ethan works out that Chloe was playing him all along, and that Ava is genuinely afraid of him. He turns up to say sorry, and Ava turns him down. The school district comes down on Ethan and Chloe both, and Ava smiles at last, done looking back.",

    # FACTS: Verona spent her whole life as Talia’s little shadow—second pick for parents, leftovers for love.
    # FACTS: Even her fiancé Bastian saved the best for her twin: the diamond, the perfume, the front seat, the
    # FACTS: master bedroom. On her wedding day, she finally ran. In a quiet town by the kiln, she learned she
    # FACTS: was never “hard to love”—just never chosen first. His regret came late. Her happiness didn’t wait.
    # FACTS: https://www.reelshort.com/movie/too-late-to-be-your-only-one-6abbbefd47eb9b78d30825b9
    'too-late-to-be-your-only-one':
        "Second choice her whole life. On her wedding day, she ran.\nVerona has always been the shadow behind her twin sister Talia. Her parents picked Talia first, and Verona got whatever love was left over. Even Bastian, the man she's engaged to, keeps the best of everything for Talia. The diamond went to her sister. So did the perfume, the front seat and the master bedroom. On the day of her wedding, Verona finally walks out. She starts over in a small town where life is quiet, and there, beside the kiln, she learns that loving her was never the hard part. She just never got chosen first. Bastian's regret does come, but it comes too late, because Verona isn't waiting around for him to be happy.",

    # FACTS: Six years ago, the Empire's War Goddess crossed paths with the last Dragon Knight, a man who
    # FACTS: commands time itself. She raised their daughter alone and searched for him for six years. Now, side
    # FACTS: by side, they stand against a rotting throne and the Abyss that means to end the world.
    # FACTS: https://www.reelshort.com/movie/her-baby-daddy-is-the-last-dragon-knight-6ac9ab991eb02e828b0ef0bd
    'her-baby-daddy-is-the-last-dragon-knight':
        "The War Goddess. The last Dragon Knight. One daughter.\nThe War Goddess of the Empire met the last Dragon Knight six years ago. He's a man who can bend time itself. Since then she's raised their daughter on her own and spent every one of those years searching for him. Now they're finally together, and they're fighting as one against a throne that's rotting and the Abyss, which is set on ending the world.",

    # FACTS: A struggling romance novelist who has never been in love and is terrible at writing romantic scenes
    # FACTS: publicly tears into a billionaire in a hotel lobby, even stealing his lighter before walking away.
    # FACTS: Three days later, the billionaire offers him a ten-million-dollar contract to become his kept lover.
    # FACTS: Coincidentally, that is exactly the amount he needs for his mother’s life-saving surgery. Desperate
    # FACTS: to save his mother, he agrees to spend just one night with the billionaire. But what was supposed to
    # FACTS: be a one-night arrangement soon turns into a complicated, irresistible entanglement neither of them
    # FACTS: can escape.
    # FACTS: https://www.reelshort.com/movie/i-m-straight-mr-voss-6ac744229f77a474f603a52b
    'i-m-straight-mr-voss':
        "He insulted a billionaire. Three days later, the billionaire made him an offer.\nHe writes romance novels for a living, he's struggling, he's never once been in love, and he's hopeless at writing love scenes. One day in a hotel lobby he tears into a billionaire in front of everyone, steals the man's lighter, and walks off. Three days later that same billionaire offers him a contract worth ten million dollars to be his kept lover. Ten million is exactly what his mother's surgery will cost, and without it she won't survive. So he agrees, to one night and only one. But one night doesn't stay one night, and the deal turns into something tangled and irresistible that neither man can walk away from.",

    # FACTS: Luke Peterson is a seventeen-year-old outcast surviving a violent home and relentless school
    # FACTS: bullying in Chicago's South Side. When a mysterious representative of the Peterson Group — a global
    # FACTS: financial empire — reveals Luke is the founder's only legitimate heir, Luke receives the family's
    # FACTS: ancient signet ring, unlocking five abilities: invisibility, magnetic force, time suspension, X-ray
    # FACTS: vision, and spirit summoning. What follows is a methodical, deeply satisfying reversal. Every
    # FACTS: humiliation Luke has endured becomes the setup for a public reckoning — engineered with precision,
    # FACTS: executed with style.
    # FACTS: https://www.reelshort.com/movie/revenge-of-the-superpowered-nerd-6ab60a5d383eb0da93077d05
    'revenge-of-the-superpowered-nerd':
        "The kid everyone bullies is the only heir to a global empire.\nLuke Peterson is seventeen and an outcast on Chicago's South Side, with violence waiting for him at home and bullies waiting for him at school. Then someone shows up from the Peterson Group, a financial empire that reaches around the world, and tells Luke he's the one and only legitimate heir of its founder. He's handed the ancient family signet ring, and with it come five powers: he can turn invisible, control magnetic force, stop time, see through things with X ray vision, and summon spirits. Luke doesn't lash out. He plans. Every humiliation they ever put him through is about to be paid back, carefully and in public, where everybody can see.",

    # FACTS: Six years ago, Nadia, a circus clown, had a one-night stand with Aris, president of Sterling Group,
    # FACTS: and unexpectedly fell pregnant. She raised their daughter Elora alone. Five years later, when Elora
    # FACTS: was hospitalized with a high fever, the Teng Serpent totem on her collarbone revealed her direct
    # FACTS: bloodline to the Sterling family. After Nadia took a job at Starlight Amusement Park under the
    # FACTS: group, she was repeatedly framed by Severin, the operations director. While protecting the mother
    # FACTS: and daughter, Aris gradually realized Nadia was the woman from six years prior. In the end, the
    # FACTS: conspiracy was exposed, Severin was expelled from the family. Aris proposed publicly. Nadia gave
    # FACTS: birth to triplet daughters, and the whole family of seven lived happily together.
    # FACTS: https://www.reelshort.com/movie/the-sterling-s-hidden-heir-6ab9fd393587575fb4076e37
    'the-sterling-s-hidden-heir':
        "A circus clown, a one night stand, and the Sterling heir she raised alone.\nNadia works as a circus clown. Six years ago she spent one night with Aris, president of the Sterling Group, and it left her pregnant. She's raised their daughter Elora by herself ever since. Then Elora is taken to the hospital with a high fever, and the Teng Serpent totem she carries on her collarbone proves she's a Sterling by blood. Nadia goes to work at Starlight Amusement Park, which belongs to the Sterling Group, and Severin, the operations director, sets her up again and again. Aris keeps stepping in to protect Nadia and Elora, and bit by bit he works out that Nadia is the woman from that night. When the conspiracy comes out, Severin is thrown out of the family and Aris proposes in front of everyone. And there's more to come: Nadia gives birth to triplet girls.",

    # FACTS: Low-born Vera spent a year despised and hurt by Julian, her leopard beastman — to him, her purchase
    # FACTS: was shame. Heartbroken, she asked the Guild for a new contract and came home with the dragon nobody
    # FACTS: wanted, Cedric, unbowed by three years of taming. But he chose her. He shielded her, guarded her,
    # FACTS: and gave his life against every hunter. She understood at last. This contract is not taming, but two
    # FACTS: souls leaning on each other. When a plot aims at her unborn child, this dragon will tear down the
    # FACTS: city.
    # FACTS: https://www.reelshort.com/movie/ditched-my-jerk-beastman-bound-a-dragon-6acc7b9923005054b50d1dbb
    'ditched-my-jerk-beastman-bound-a-dragon':
        "Her leopard beastman was ashamed of her. The dragon chose her.\nVera is low born, and for a whole year Julian, her leopard beastman, looks down on her and hurts her, because to him being bought by her is a disgrace. Heartbroken, she goes back to the Guild to sign a new contract, and she comes home with the dragon nobody else would take. Cedric has spent three years refusing to be tamed. But he picks Vera. He shields her, stands guard over her, and puts his life on the line against every hunter that comes for her. That's when she finally understands that this contract was never about taming anybody. It's two souls holding each other up. And when someone plots against her unborn child, this dragon is ready to tear the whole city down.",

    # FACTS: Elowen, the eldest daughter of the Winfield family, was framed by her aunt Valera for treason and
    # FACTS: imprisoned in a high tower. While in captivity, she gave birth to a daughter, Mia; using her final
    # FACTS: reserves of strength, she sent the child—along with a dragon-crested ring and a red obsidian
    # FACTS: necklace—onto the back of the dragon Valensa, entrusting the beast to take her to her biological
    # FACTS: father, Prince Orion of Aetheron. Five-year-old Mia ventured alone into a royal banquet, only to be
    # FACTS: driven away as an impostor because her father was unaware of the truth. She worked as a cleaner at
    # FACTS: the Dragon-Taming Academy to earn the coins needed to visit her mother, all while silently guarding
    # FACTS: the secret her mother had left in her care. As Valera closed in, desperate to seize the secret arts
    # FACTS: of dragon-taming, Mia’s true identity was finally confirmed by the dragons. Orion, consumed by
    # FACTS: remorse, rescued Elowen from the execution grounds just as a greater conspiracy loomed; the
    # FACTS: vengeance of the Mondragon family and an undead army fueled by dark magic would soon sweep the
    # FACTS: family of three into an ultimate battle determining the fate of the empire.
    # FACTS: https://www.reelshort.com/movie/the-lost-little-princess-of-the-dragon-clan-6abb7747561ddb0d1f054df5
    'the-lost-little-princess-of-the-dragon-clan':
        "Born in a prison tower, sent to her father on a dragon's back.\nElowen is the Winfield family's eldest daughter, and her aunt Valera frames her for treason and has her locked away in a high tower. There she gives birth to a daughter, Mia. With the last of her strength she puts the baby on the dragon Valensa, along with a red obsidian necklace and a ring bearing a dragon crest, and trusts the dragon to carry her to her father, Prince Orion of Aetheron. At five, Mia walks into a royal banquet all by herself, and because Orion has no idea she exists, she's chased out as a fake. So she takes a cleaning job at the Dragon Taming Academy, saving up coins so she can visit her mother, and keeps quiet about the secret Elowen trusted her with. Valera is closing in, desperate to get her hands on the secrets of dragon taming, when the dragons themselves confirm who Mia really is. Orion, sick with regret, saves Elowen from the execution grounds. But the Mondragon family wants revenge, an undead army raised by dark magic is coming, and this family of three is about to fight for the fate of the whole empire.",

    # FACTS: After years of abuse, Evelyn leaves her marriage with nothing. Fate makes her the stepmother of
    # FACTS: mafia Don Matteo Vicari's daughter. Their contract marriage pulls her into a dangerous world where
    # FACTS: she heals traumatized little Bella and slowly captures Matteo's guarded heart. Standing up to her
    # FACTS: ex-husband, she breaks free from her past—and finds family, true love, and a new life.
    # FACTS: https://www.reelshort.com/movie/after-marrying-the-mafia-don-i-found-a-new-life-6ad02d11e200fce7fe0ec8f9
    'after-marrying-the-mafia-don-i-found-a-new-life':
        "She walked out of her marriage with nothing. Then she married a mafia Don.\nEvelyn puts up with years of abuse before she finally leaves her marriage, and she walks out with nothing at all. Then fate puts her in a contract marriage with Matteo Vicari, a mafia Don, which makes her stepmother to his little daughter Bella. It's a dangerous world to be dropped into. Bella has been through something terrible, and Evelyn is the one who helps her heal, while little by little she gets past the guard Matteo keeps around his heart. She stands up to her ex husband and leaves her past behind for good. What she finds is a family, real love, and a life that's finally her own.",

    # FACTS: Kai, an orphan turned soldier, led Valerano's fleet to defeat the Kyte Empire. Recognized as King
    # FACTS: Eddy's long-lost second prince, he returned to find his wife Sara and daughter Diana enslaved by his
    # FACTS: in-laws. He crowned Diana a Countess, crushed a Kyte invasion with his Underwater Fleet, and exposed
    # FACTS: the traitors. After Eddy's death, Kai faced his brother Jake's treachery, summoned the Airship Fleet
    # FACTS: to obliterate the Kyte army, and was crowned king. Sara became queen, Diana princess.
    # FACTS: https://www.reelshort.com/movie/crowned-the-son-in-law-s-return-6a714984282e82f7430d5aa3
    'crowned-the-son-in-law-s-return':
        "He won the war and came home a prince. His wife and daughter were slaves.\nKai grew up an orphan, became a soldier, and led Valerano's fleet to victory over the Kyte Empire. Then it turns out he's the long lost second son of King Eddy. But when he comes home, he finds his wife's family has turned his wife Sara and their daughter Diana into slaves. Kai makes Diana a Countess, sends his Underwater Fleet to smash a Kyte invasion, and drags the traitors into the light. When Eddy dies, Kai's own brother Jake turns on him, so he calls in the Airship Fleet and destroys the Kyte army completely. Kai is crowned king, Sara becomes his queen, and the daughter who was treated as a slave is now a princess.",

    # FACTS: Set in a medieval city‑state, Princess Liora, the second princess, is deeply in love with Ron, her
    # FACTS: personal knight whom she has promoted. Yet Ron is head‑over‑heels for Seraphina, the arrogant and
    # FACTS: jealous elder princess. After all her devotion goes unrequited, Liora sees through the hollow love
    # FACTS: and family affection in the royal palace. She volunteers to take her elder sister’s place and become
    # FACTS: the sacrificial bride bound by contract to the evil dragon. Her selfish father, the king, is
    # FACTS: secretly delighted and sends her off to this fate. Liora terminates her knight‑bond with Ron and
    # FACTS: gives him to Seraphina, cutting off all her old feelings. When the sacrificial bugles blare, Ron is
    # FACTS: horrified to find that it is Liora heading for the dragon’s lair, consumed by regret. The
    # FACTS: ferocious‑legendary dragon Kaelion is actually the Sun God cursed by a dark witch, and he falls for
    # FACTS: Liora at first sight. Leaving the cold‑hearted city‑state behind, Liora embarks on a brand‑new life
    # FACTS: with the cursed dragon. Those who once hurt her will eventually taste the pain of loss.
    # FACTS: https://www.reelshort.com/movie/abandoned-i-turned-and-married-the-evil-dragon-6ad0abde65dc2d829002d407
    'abandoned-i-turned-and-married-the-evil-dragon':
        "She volunteered to be the dragon's bride. The dragon fell for her.\nLiora is the second princess, and she's deeply in love with Ron, the knight she promoted to serve her personally. Ron only has eyes for her older sister Seraphina, who is arrogant and jealous. After giving everything and getting nothing back, Liora finally sees how empty the love and family feeling in that palace really are. So she offers to take Seraphina's place as the sacrificial bride, the one a contract has promised to the evil dragon, and the king, her selfish father, is quietly thrilled to send her. Before she goes, Liora cuts the knight bond between her and Ron and hands him to Seraphina, done with him for good. When the bugles sound for the sacrifice, Ron realizes with horror that it's Liora on her way to the dragon's lair, and the regret eats him alive. But the dragon Kaelion is really the Sun God under a dark witch's curse, and he falls for Liora the moment he sees her. She leaves that cold city behind for a whole new life with him, and the people who hurt her are about to learn what losing her costs.",

    # FACTS: Best friends, Ella and Leah, marry into the HARPER family at the same time – Ella to the firefighter
    # FACTS: older brother, Charles, and Leah to the doctor younger brother, Noah. On the three-year anniversary
    # FACTS: of their marriage, Ella is locked inside a blazing room by Charles's first love, Megan. Ella calls
    # FACTS: Charles and begs for help, but he brushes her off, saying he's busy helping Megan find her cat. At
    # FACTS: the most crucial moment, Leah rushes in to save Ella. Leah calls Noah, begging him to come and save
    # FACTS: Ella and her baby. But she's met with mockery and criticism. Heartbroken and betrayed, the best
    # FACTS: friends, who have endured years of their horrible marriages, decide to file for divorce with the
    # FACTS: HARPER brothers together.
    # FACTS: https://www.reelshort.com/movie/homegirls-before-husbands-6aac6e6d5230d8d6ca013277
    'homegirls-before-husbands':
        "Her firefighter husband was too busy finding his first love's cat.\nElla and Leah are best friends who marry two Harper brothers at once. Ella's husband is Charles, the older brother, a firefighter. Leah's is Noah, the younger one, a doctor. Three years in, on their anniversary, Charles's first love Megan locks Ella in a room that's on fire. Ella calls her husband and begs him to come. He waves her off because he's busy helping Megan look for her cat. It's Leah who runs in and gets Ella out. When Leah calls Noah and begs him to help save Ella and her baby, all she gets back is ridicule and blame. After years of miserable marriages, the best friends are done. They file for divorce from the Harper brothers, and they do it together.",
}

SOURCES = {  # kind -> caption_pipeline.SOURCE_KINDS
    'claimed-by-the-prince-the-forbidden-wet-nurse': ('platform', 'https://www.reelshort.com/movie/claimed-by-the-prince-the-forbidden-wet-nurse-6aa221dcce316629590e2bed'),
    'eight-years-gone-down-the-drain': ('platform', 'https://www.reelshort.com/movie/eight-years-gone-down-the-drain-6a5724f41fd2b06f5e0142b5'),
    'out-of-your-league-the-billionaire-wife-s-revenge': ('platform', 'https://www.reelshort.com/movie/out-of-your-league-the-billionaire-wife-s-revenge-6ab48e78dc6fd7ef4a06596e'),
    'the-alpha-s-late-regret': ('platform', 'https://www.reelshort.com/movie/the-alpha-s-late-regret-6ac72f090816cc72b703a6e9'),
    'fire-ice-return-of-the-alpha-queen-s-sister': ('platform', 'https://www.reelshort.com/movie/fire-ice-return-of-the-alpha-queen-s-sister-6ab60ad679098aca75062427'),
    'reborn-as-the-cursed-alpha-s-luna': ('platform', 'https://www.reelshort.com/movie/reborn-as-the-cursed-alpha-s-luna-6a963bbc7308ebfe9309c899'),
    'i-burned-my-wedding-dress-before-he-ever-marked-me': ('platform', 'https://www.reelshort.com/movie/i-burned-my-wedding-dress-before-he-ever-marked-me-6aba0531e585c7314a06155c'),
    'the-hanged-girl-on-the-flagpole': ('platform', 'https://www.reelshort.com/movie/the-hanged-girl-on-the-flagpole-6ac7076da6819fff2c0e4e43'),
    'too-late-to-be-your-only-one': ('platform', 'https://www.reelshort.com/movie/too-late-to-be-your-only-one-6abbbefd47eb9b78d30825b9'),
    'her-baby-daddy-is-the-last-dragon-knight': ('platform', 'https://www.reelshort.com/movie/her-baby-daddy-is-the-last-dragon-knight-6ac9ab991eb02e828b0ef0bd'),
    'i-m-straight-mr-voss': ('platform', 'https://www.reelshort.com/movie/i-m-straight-mr-voss-6ac744229f77a474f603a52b'),
    'revenge-of-the-superpowered-nerd': ('platform', 'https://www.reelshort.com/movie/revenge-of-the-superpowered-nerd-6ab60a5d383eb0da93077d05'),
    'the-sterling-s-hidden-heir': ('platform', 'https://www.reelshort.com/movie/the-sterling-s-hidden-heir-6ab9fd393587575fb4076e37'),
    'ditched-my-jerk-beastman-bound-a-dragon': ('platform', 'https://www.reelshort.com/movie/ditched-my-jerk-beastman-bound-a-dragon-6acc7b9923005054b50d1dbb'),
    'the-lost-little-princess-of-the-dragon-clan': ('platform', 'https://www.reelshort.com/movie/the-lost-little-princess-of-the-dragon-clan-6abb7747561ddb0d1f054df5'),
    'after-marrying-the-mafia-don-i-found-a-new-life': ('platform', 'https://www.reelshort.com/movie/after-marrying-the-mafia-don-i-found-a-new-life-6ad02d11e200fce7fe0ec8f9'),
    'crowned-the-son-in-law-s-return': ('platform', 'https://www.reelshort.com/movie/crowned-the-son-in-law-s-return-6a714984282e82f7430d5aa3'),
    'abandoned-i-turned-and-married-the-evil-dragon': ('platform', 'https://www.reelshort.com/movie/abandoned-i-turned-and-married-the-evil-dragon-6ad0abde65dc2d829002d407'),
    'homegirls-before-husbands': ('platform', 'https://www.reelshort.com/movie/homegirls-before-husbands-6aac6e6d5230d8d6ca013277'),
}

FACTS = {  # the published synopsis each caption was written from
    'claimed-by-the-prince-the-forbidden-wet-nurse':
        'Clara, a young widow, shares one night with a stranger in the castle rose garden—not knowing he’s Crown Prince Gabriel. Pregnant, she leaves her baby and a golden ring on the castle steps to save him from a tyrant. She becomes a wet nurse at the castle, nursing the little prince who refuses all others—without knowing he’s her son, and the cold prince is her one-night stranger. When the truth surfaces, Gabriel crowns her queen.',
    'eight-years-gone-down-the-drain':
        "Eve helped Noah build Black Tech from nothing, only to discover he has married the intern Mia and plans to hand her Eve's biggest project. At the Grant signing ceremony, Eve reveals her true identity as the Grant Group heiress and exposes Mia's leak, Noah's entitlement, and the cost of eight wasted years. Walking away from his collapse, she signs back the life that always belonged to her.",
    'out-of-your-league-the-billionaire-wife-s-revenge':
        "Vanessa built an empire, paid off her husband’s debts, and funded his family’s lavish lifestyle. She's ready to enjoy the family vacation - until she finds out her husband gave away her first-class ticket to his ex-girlfriend! Finally, she realizes she's been nothing but a walking ATM to him. Now, she's done letting him bleed her dry, and she's going to take back everything she ever gave him!",
    'the-alpha-s-late-regret':
        'Elena, Luna of the Winters Pack, loves Alpha Roman for ten years, his wife for five, yet he never sees her. Jealous stepsister Sienna causes her miscarriage and steals credit for saving Roman, leaving Elena blamed. Drained by a life debt that saved Roman, then rejected, Elena severs their bond and leaps from a cliff. Only in death does Roman learn every sacrifice was hers. He exposes Sienna, confesses too late, and seeks forbidden resurrection, but the ring he needs lies sunk in frozen falls.',
    'fire-ice-return-of-the-alpha-queen-s-sister':
        "7-year-old Wolf Princess, Ruby Zephyr is cursed, and slowly freezing the heart of her sister, Talia. Talia would rather die than leave Ruby, so Ruby runs away, giving up her wolf, and all memory of who she is to save her sister. 11 years later, Alpha Queen Talia is determined to reunite with her long lost sister. She travels to Crystal Valley High, and finds a brilliant and kind student with her sister's violet eyes. As her suspicions grow, Talia sees Ruby mistreated by her peers and must intervene, jogging Ruby's memory and unlocking her Ice Wolf. When Ruby's bullies finally realize they've been abusing the Alpha Queen and her sister, the lost Ice Wolf Queen, they'll FREEZE with regret.",
    'reborn-as-the-cursed-alpha-s-luna':
        'Serena Vale died with Adrian\'s silver knife in her chest after her sister Lila screamed, "Serena stole my Luna mark." Reborn at the Moon Den, Serena refuses to bleed for Lila again. The mark chooses her in front of the pack, and when her former betrothed steps forward, she makes the choice that shatters Blackwood: "I choose Rowan Blackwood." Rowan is Adrian\'s cursed uncle, poisoned into a living corpse, but his wolf still answers her. When he wakes and asks who dared touch his Luna, Serena\'s second life turns from survival into war.',
    'i-burned-my-wedding-dress-before-he-ever-marked-me':
        'Silvermoon pureblood Wren waits three years for her fated mate Silas, who rejects her for her half-sister Cora on the full moon. Framed and exiled by her family, Wren flees north and accepts Bloodmoon Alpha Ridge. When Silas learns Cora lied, it is too late. As Wren bonds with Ridge, Cora and Vera are banished, Elias falls comatose, and grief-stricken Silas ends his life in an icy lake.',
    'the-hanged-girl-on-the-flagpole':
        'Ava loves Ethan for ten years, but he ties her to a flagpole as a cruel "Hanged Man" prank for his new crush Chloe, humiliating her before the whole school. Ava finally breaks free, transfers to Westbridge High, and cuts Ethan off. At her new school, she meets kind friends and Noah, who protects her. Ethan slowly realizes Chloe manipulated him and that Ava truly fears him. He comes to apologize, but Ava refuses him. The district punishes Ethan and Chloe. Ava finally smiles, no longer looking back.',
    'too-late-to-be-your-only-one':
        'Verona spent her whole life as Talia’s little shadow—second pick for parents, leftovers for love. Even her fiancé Bastian saved the best for her twin: the diamond, the perfume, the front seat, the master bedroom. On her wedding day, she finally ran. In a quiet town by the kiln, she learned she was never “hard to love”—just never chosen first. His regret came late. Her happiness didn’t wait.',
    'her-baby-daddy-is-the-last-dragon-knight':
        "Six years ago, the Empire's War Goddess crossed paths with the last Dragon Knight, a man who commands time itself. She raised their daughter alone and searched for him for six years. Now, side by side, they stand against a rotting throne and the Abyss that means to end the world.",
    'i-m-straight-mr-voss':
        'A struggling romance novelist who has never been in love and is terrible at writing romantic scenes publicly tears into a billionaire in a hotel lobby, even stealing his lighter before walking away. Three days later, the billionaire offers him a ten-million-dollar contract to become his kept lover. Coincidentally, that is exactly the amount he needs for his mother’s life-saving surgery. Desperate to save his mother, he agrees to spend just one night with the billionaire. But what was supposed to be a one-night arrangement soon turns into a complicated, irresistible entanglement neither of them can escape.',
    'revenge-of-the-superpowered-nerd':
        "Luke Peterson is a seventeen-year-old outcast surviving a violent home and relentless school bullying in Chicago's South Side. When a mysterious representative of the Peterson Group — a global financial empire — reveals Luke is the founder's only legitimate heir, Luke receives the family's ancient signet ring, unlocking five abilities: invisibility, magnetic force, time suspension, X-ray vision, and spirit summoning. What follows is a methodical, deeply satisfying reversal. Every humiliation Luke has endured becomes the setup for a public reckoning — engineered with precision, executed with style.",
    'the-sterling-s-hidden-heir':
        'Six years ago, Nadia, a circus clown, had a one-night stand with Aris, president of Sterling Group, and unexpectedly fell pregnant. She raised their daughter Elora alone. Five years later, when Elora was hospitalized with a high fever, the Teng Serpent totem on her collarbone revealed her direct bloodline to the Sterling family. After Nadia took a job at Starlight Amusement Park under the group, she was repeatedly framed by Severin, the operations director. While protecting the mother and daughter, Aris gradually realized Nadia was the woman from six years prior. In the end, the conspiracy was exposed, Severin was expelled from the family. Aris proposed publicly. Nadia gave birth to triplet daughters, and the whole family of seven lived happily together.',
    'ditched-my-jerk-beastman-bound-a-dragon':
        'Low-born Vera spent a year despised and hurt by Julian, her leopard beastman — to him, her purchase was shame. Heartbroken, she asked the Guild for a new contract and came home with the dragon nobody wanted, Cedric, unbowed by three years of taming. But he chose her. He shielded her, guarded her, and gave his life against every hunter. She understood at last. This contract is not taming, but two souls leaning on each other. When a plot aims at her unborn child, this dragon will tear down the city.',
    'the-lost-little-princess-of-the-dragon-clan':
        'Elowen, the eldest daughter of the Winfield family, was framed by her aunt Valera for treason and imprisoned in a high tower. While in captivity, she gave birth to a daughter, Mia; using her final reserves of strength, she sent the child—along with a dragon-crested ring and a red obsidian necklace—onto the back of the dragon Valensa, entrusting the beast to take her to her biological father, Prince Orion of Aetheron. Five-year-old Mia ventured alone into a royal banquet, only to be driven away as an impostor because her father was unaware of the truth. She worked as a cleaner at the Dragon-Taming Academy to earn the coins needed to visit her mother, all while silently guarding the secret her mother had left in her care. As Valera closed in, desperate to seize the secret arts of dragon-taming, Mia’s true identity was finally confirmed by the dragons. Orion, consumed by remorse, rescued Elowen from the execution grounds just as a greater conspiracy loomed; the vengeance of the Mondragon family and an undead army fueled by dark magic would soon sweep the family of three into an ultimate battle determining the fate of the empire.',
    'after-marrying-the-mafia-don-i-found-a-new-life':
        "After years of abuse, Evelyn leaves her marriage with nothing. Fate makes her the stepmother of mafia Don Matteo Vicari's daughter. Their contract marriage pulls her into a dangerous world where she heals traumatized little Bella and slowly captures Matteo's guarded heart. Standing up to her ex-husband, she breaks free from her past—and finds family, true love, and a new life.",
    'crowned-the-son-in-law-s-return':
        "Kai, an orphan turned soldier, led Valerano's fleet to defeat the Kyte Empire. Recognized as King Eddy's long-lost second prince, he returned to find his wife Sara and daughter Diana enslaved by his in-laws. He crowned Diana a Countess, crushed a Kyte invasion with his Underwater Fleet, and exposed the traitors. After Eddy's death, Kai faced his brother Jake's treachery, summoned the Airship Fleet to obliterate the Kyte army, and was crowned king. Sara became queen, Diana princess.",
    'abandoned-i-turned-and-married-the-evil-dragon':
        'Set in a medieval city‑state, Princess Liora, the second princess, is deeply in love with Ron, her personal knight whom she has promoted. Yet Ron is head‑over‑heels for Seraphina, the arrogant and jealous elder princess. After all her devotion goes unrequited, Liora sees through the hollow love and family affection in the royal palace. She volunteers to take her elder sister’s place and become the sacrificial bride bound by contract to the evil dragon. Her selfish father, the king, is secretly delighted and sends her off to this fate. Liora terminates her knight‑bond with Ron and gives him to Seraphina, cutting off all her old feelings. When the sacrificial bugles blare, Ron is horrified to find that it is Liora heading for the dragon’s lair, consumed by regret. The ferocious‑legendary dragon Kaelion is actually the Sun God cursed by a dark witch, and he falls for Liora at first sight. Leaving the cold‑hearted city‑state behind, Liora embarks on a brand‑new life with the cursed dragon. Those who once hurt her will eventually taste the pain of loss.',
    'homegirls-before-husbands':
        "Best friends, Ella and Leah, marry into the HARPER family at the same time – Ella to the firefighter older brother, Charles, and Leah to the doctor younger brother, Noah. On the three-year anniversary of their marriage, Ella is locked inside a blazing room by Charles's first love, Megan. Ella calls Charles and begs for help, but he brushes her off, saying he's busy helping Megan find her cat. At the most crucial moment, Leah rushes in to save Ella. Leah calls Noah, begging him to come and save Ella and her baby. But she's met with mockery and criticism. Heartbroken and betrayed, the best friends, who have endured years of their horrible marriages, decide to file for divorce with the HARPER brothers together.",
}
