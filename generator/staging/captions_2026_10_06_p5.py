# -*- coding: utf-8 -*-
"""Caption batch 6 Oct 2026, part 5, titles imported 6 Oct (DramaBox 28 Sep data). STAGED FOR CYAN'S REVIEW, not approved.

31 titles, 31 written, none skipped. Every caption is written from the DramaBox
book the title page links to (availability.csv direct_link). DramaBox refuses
direct fetches, so each FACTS entry is the platform synopsis banked from the
28 Sep scrape, whitespace collapsed.

Thin sources (a premise of one or two sentences, written short rather than
padded, worth her eye): how-to-snatch-a-billionaire, when-he-finally-looked-back,
divorced-then-find-my-mr-right, billionaire-playboy-s-replacement-bride.

the-complete-transformation-of-a-girl: the source says "BDSM training
contract"; four capitals is a hard ban, so the caption says "a training
contract for dominance and submission". weapons-women-wild-west: the source
misspells "Civi War", so the name gate cannot match "Civil War"; the caption
says "with America at war with itself".
"""

CAPTIONS = {
    # 158.2M  My Poor Husband is A Billionaire
    'my-poor-husband-is-a-billionaire':
        "Her husband is a secret CEO. She thinks he's the man who ruined her life.\nThree years ago Stella spent one night with a man she didn't know, and she's sure he's the one behind the prostitution scandal that wrecked everything for her. She has the wrong idea about him, but she doesn't know that. Now she's in a flash marriage with Ethan, and before long they really do fall for each other. The longer she lives with him, though, the more Ethan reminds her of that stranger. And there's worse. He's been hiding the fact that he's a CEO from her the whole time. Stella can't live with what she's found out, so she divorces the husband she loves.",
    # 120.5M  Your Loser Husband Is A Big Shot
    'your-loser-husband-is-a-big-shot':
        "He gave up a fortune for love. Then three years of his life to save his family.\nNathan turned his back on his family's empire because he was in love. Then kidnappers took his wife and daughter. He sacrificed himself to save them and paid for it with three years of torture. He finally gets home and finds his wife tangled up with an old flame, and his own daughter keeping him at arm's length. With his heart broken, Nathan stops being the loser husband they all took him for. He steps back into his place as heir to a billion dollar fortune, cuts off everything from his old life, and starts again. The wife he suffered for has lost him, and this time he isn't coming back.",
    # 91.4M  Tempest：The Last Mecha
    'tempest-the-last-mecha':
        "The janitor mopping the floors is the Mech King.\nColt Thorne was the Mech King until his parents died and it broke him. Freya saved him, and ever since he's been hiding out as a janitor nobody looks at twice, quietly in love with her and never saying so. Then Freya is betrayed and pushed into a mech duel that could kill her. To save her, Colt has to stop pretending. He reaches the legendary 100% Neural Sync, takes command of The Tempest and sets out to crush his enemies. Beyond them is an alien swarm big enough to wipe out every living thing, and the whole world is depending on him. The quiet life he hid inside is over.",
    # 81.3M  Love at the End of Lies
    'love-at-the-end-of-lies':
        "Her fiance spent her savings. Her new husband thinks she's after his money.\nAva gets engaged to Dylan, and that same day she learns he's been secretly dipping into her savings. He isn't sorry. He and his mother hurl insults at her instead, and Ava is so angry she ends the engagement on the spot. Her grandmother's house is about to be lost unless she finds the money, and in desperation she agrees to marry Noah, her elderly neighbor's grandson. What Ava doesn't know is that Noah is a billionaire. And he's already decided she's just another gold digger. She left one man for using her, and the next one thinks she's the one doing the using.",
    # 65.1M  After Divorce: I Become Heiress
    'after-divorce-i-become-heiress':
        "She hid that she's an heiress. Now nobody believes her.\nSally's billionaire father loves her so much it's suffocating, so she keeps quiet about being his heiress and pays her own way. Then Felix, her husband, is unfaithful. To get even, Sally flash marries Aiden, and she has no idea he's the CEO of the Taylor family. Once the divorce goes through, she finally tells everyone who she is, and Felix and the rest just laugh at her. Even Aiden doesn't believe a word of it. Neither of them knows who the other one really is. Wait until they find out.",
    # 59.0M  Boss, She Said No Again!
    'boss-she-said-no-again':
        "Engaged to one Kingsley brother. Saved the life of the other.\nRowena was left on her own for sixteen years, and now she's back in New York to claim the inheritance her mother left her. Her cover is a fake engagement to the younger Kingsley son, with a breakup already planned for when she's done. Then she saves his older brother, Damien Kingsley, when the mafia comes for him. Damien is intrigued, and he pushes his way into her life without asking. Her scheming family keeps setting traps for her, and the ruthless Mrs. Kingsley sets a few of her own. Rowena and Damien start out as enemies and end up on the same side, digging into a murder nobody has explained. She came to New York for her mother's money, not a Kingsley, but Damien isn't taking no for an answer.",
    # 51.0M  A Virgin Surrogate for the Billionaire
    'a-virgin-surrogate-for-the-billionaire':
        "She carries his baby to pay for her sister's surgery.\nHoney Myers has a sister who needs surgery and no way to pay for it, so she agrees to become a surrogate for Tristan Brown, an NFL star. What follows is far from simple. There's betrayal, there are problems at every turn, and there's a love neither of them expected. Tristan's ex fiancee Jennifer keeps threatening what they have. Honey gets through all of it, and the baby she agreed to carry for her sister's sake ends up giving her a family and a happy ending of her own.",
    # 47.0M  Scent of the CEO's Lost Love
    'scent-of-the-ceo-s-lost-love':
        "A blind perfumer, a cold CEO and a contract marriage.\nStella has lived through years of abuse by hiding who she really is. She's the Lynn family's last heir. She's blind, she makes perfume, and now she has no choice but a contract marriage with Conor, a cold CEO. The secret at the heart of it is that she's the girl who saved his life long ago. As danger gets closer, they both have to face the past they share and every lie between them. Neither one saw it coming, but they're falling for each other anyway.",
    # 43.3M  Serendipitous Love
    'serendipitous-love':
        "She married a stranger on her first day at work. Then he vanished.\nThe day Sylvia Cooper starts at Taylor Corp. is also the day she marries Brian Anders, a man she's never met. The ink is barely dry on the marriage papers when he disappears. Twelve months pass. Then Liam Taylor, CEO of Taylor Corp., comes home from France. As time goes on he realizes he has feelings for Sylvia unlike anything he's felt before. Liam also wants a divorce. He shows up at the courthouse to get one, and the woman waiting for him at the door is Sylvia. So who exactly did she marry?",
    # 38.8M  Love, not Lost to Memory
    'love-not-lost-to-memory':
        "They drained her blood to save the heir. Seven years later she remembers none of it.\nVera Bell has twins for the Todds, a powerful family, and right there in the delivery room they drain her blood to save Finn Todd, the heir they've picked. They leave her for dead, still holding a lucky charm covered in her own blood. Seven years on, Vera is alive. She can't speak and she can't remember who she is, and she gets by scavenging while she raises her daughter, Grace Bell. The Todds got the heir they wanted, and Vera lost everything, even the memory of what they took from her.",
    # 36.5M  How to Snatch a Billionaire
    'how-to-snatch-a-billionaire':
        "Sick of blind dates, she kisses a stranger. He isn't letting it go.\nHarley has had enough of boring blind dates. So on a whim she grabs a good looking man as he walks by and kisses him. She doesn't know him at all. But the stranger isn't about to forget it, and that one impulsive kiss turns into a romance neither of them saw coming.",
    # 35.6M  Seducing Mr. Sterling: The Ice-cold Heir
    'seducing-mr-sterling-the-ice-cold-heir':
        "Seduce the CEO and ruin him. Her sister's life depends on it.\nEmma's sister is dying, and to save her Emma agrees to seduce Ethan Sterling, a ruthless CEO, and wreck his reputation. Once she's inside his world, with all its power and all its secrets, she starts to fall for the very man she's supposed to bring down. Now love and betrayal are pulling her in opposite directions, and she has to pick one. She can save her sister, or she can save the man who might be the one to save her.",
    # 31.5M  All My Love, All for You
    'all-my-love-all-for-you':
        "Her family wants to sell her to an older man for half a million dollars.\nMona Leed takes a courier job to cover her tuition, and that's how she meets Jim Judd. She ends up pregnant by him, which she never expected. Her family has plans of their own for her. An older man has offered them $500,000, and they intend to hand her over to him as his wife. Mona is determined to get out from under their control, so she makes up her mind to have the baby and says no to the marriage. Once Jim hears what she's going through and sees how innocent she really is, he steps in, takes her home and looks after her. Her family wanted half a million dollars for her. Jim just wants to take care of her.",
    # 29.3M  Pampered by Him
    'pampered-by-him':
        "She kissed a stranger to ruin her blind date. He was waiting for his contract bride.\nLia's stepmother sets her up on a blind date, and Lia decides the man needs to be taught a lesson. So she grabs a handsome stranger named Jeremy and kisses him right in front of her date. Her date storms off in a rage, but Lia's troubles are only beginning. The stranger is Jeremy Smith, the well known President of the Smith Group. He was sitting in that cafe waiting for his contract bride, and she never came. Lia took his first kiss instead, and now she's in far deeper than the date she was trying to get rid of.",
    # 26.9M  Billionaire Alpha Won’t Let Me Go
    'billionaire-alpha-wont-let-me-go':
        "She came back to New York with her son and ran into the werewolf she used to love.\nZoe Lopez moves back to New York with her little boy, and there she runs into Alexander Blackwood. He's a man she once loved, and he's also a werewolf. The old feelings come rushing back. So do secrets that were buried for a reason, about power, about family and about a supernatural bloodline, and those secrets put both their lives at risk. With danger getting closer, the romance between them catches fire all over again, and they're pushed toward a fate neither of them gets to control.",
    # 24.7M  Divorced, Then Find My Mr. Right
    'divorced-then-find-my-mr-right':
        "She lost her marriage, her child and her dignity.\nHazel is betrayed in the cruelest way, and when it's over her marriage is gone, her child is gone and so is her pride. For a while there's nothing but despair. Then she finds Evan again, a powerful man, and with his help she starts to climb back up. She wins back her career, she learns what she's worth, and for the first time Hazel is the one deciding where her life goes.",
    # 21.6M  Three Chances, I'm Gone Forever
    'three-chances-i-m-gone-forever':
        "She gave him a kidney. He gave her place to someone else.\nKama gave everything she had for Erwin, the boy she loved growing up. Her fortune, her health, even one of her kidneys. Then he betrays her and lets the manipulative Circe take her place. Kama makes herself a promise. Erwin gets three chances and not one more. She picks herself up after the heartbreak and takes back her power, her wealth and her dignity, with the billionaire Landon standing beside her. Once he's thrown away the third one, Kama has no mercy left for him.",
    # 20.0M  Hurt Me,Love Me
    'hurt-me-love-me':
        "Her husband never let go of Riley. She's the one who paid for it.\nKatherine married Eric, but Eric never really ended things with Riley, and Katherine has suffered for it ever since. She puts up with the pain because she loves him deeply and because she carries guilt of her own. Then, when she least expects it, she's pregnant again. Eric goes right on ignoring her and hurting her anyway. For the sake of the child they lost, Katherine finally decides to divorce him. Will Eric understand what he's thrown away before it's too late?",
    # 18.1M  A Woman Scorned
    'a-woman-scorned':
        "Her stepsister stole her fiance. Her family blamed her for it.\nCarynn Hughes has always been the black sheep. Her father doesn't like her, her stepmother is cruel to her, and her stepsister seduces her fiance, Archiebald Murray. That same day she happens to run into Jayden Lewis, a powerful man, and his sick grandfather, and it hands her a way to start her life over. Her parents still blame her for Archiebald cheating with her stepsister. So when the engagement comes around, Carynn makes sure they become a joke the whole town is laughing at.",
    # 16.4M  The Professor I'm Dating is A Billionaire
    'the-professor-i-m-dating-is-a-billionaire':
        "The professor who cost her the internship is secretly the CEO.\nReese is a gifted student, and she's just been humiliated twice. Her boyfriend cheats on her, and then she loses her internship at WG Group because of Sanger, the strictest professor she has. What Reese doesn't know is that Sanger is the CEO of WG, and behind the scenes he's been setting things up so she can come back. A robot competition with everything riding on it is her chance to show what she can do. She proves herself, she falls in love, and she finds out who Sanger really is. The professor who cost her the internship was the one quietly clearing her way back.",
    # 14.7M  A Dangerous Engagement: The Bride He Mustn't Touch
    'a-dangerous-engagement-the-bride-he-mustn-t-touch':
        "Her stepbrother is choosing her husband. She wants it to be him.\nShe ran away from the mob when she was eighteen, and neither her father, the mafia king, nor Angelo could track her down. Angelo is her stepbrother, her father's legally adopted son, and they never grew up together. When her father dies out of nowhere, Angelo finds her and brings her back. To him she's an innocent girl he has to protect. He decides she has to marry, to keep her safe and to keep the empire steady, and he puts himself in charge of choosing the groom. The trouble is that the only man she wants to marry is Angelo.",
    # 12.9M  Rescued by the Rugged Mountain Man
    'rescued-by-the-rugged-mountain-man':
        "Beaten, left in the snow, then attacked by a wolf.\nMia is a city girl who's already been hurt by her ex. Then she's beaten and sent away to a remote mountain buried under ice and snow. She's starving and freezing, and on top of all that a wild wolf comes after her. That's when a powerful man steps in and saves her. They can't stand each other at first, but little by little that turns into something real. Mia finds out who he really is, and she makes her cruel ex pay for what he did to her. In the end she gets her happy ever after with the man who pulled her out of the snow.",
    # 10.4M  Billionaire Playboy's Replacement Bride
    'billionaire-playboy-s-replacement-bride':
        "She spent one night with a stranger. He turned out to be the groom.\nAlicia's stepmother leans on her until she agrees to take her sister's place and marry a man she's never met. Miserable about it, she looks for comfort and spends one night with Lucius. Then the wedding day comes, and Alicia finds out the groom is Lucius. The replacement bride and the billionaire playboy are already in deeper than either of them meant to be, and a stand in wedding becomes a love neither of them planned on.",
    # 8.8M  I Don't Want Any of You Three
    'i-don-t-want-any-of-you-three':
        "Three childhood friends. All three were faking it.\nSerena Sterling is a wealthy heiress who always assumed one of the three boys she grew up with would be her husband one day. Then she finds out none of them ever meant it. Her father has been paying their way, and that money is the only reason any of them pretended to care about her. The girl all three of them really want is Bella, the daughter of the family driver. Serena is done with them. She doesn't want a single one of them.",
    # 8.3M  Oops! The CEO's Birthday is Ruined
    'oops-the-ceo-s-birthday-is-ruined':
        "She never once told her son no.\nTiffany spoiled Billy from the day he was born and never gave him a single rule. He grows up reckless and entitled, and she keeps looking the other way. He wrecks the party thrown by his father's boss, humiliates the guests, smashes up a million dollar car and then sets it on fire. Every time, she lets it slide. But loving him that blindly has a price. Billy throws away his own future and his father loses his career because of him, and in the end he's the reason Tiffany goes to prison. Sitting in a cell, she at last understands what that kind of love cost.",
    # 7.3M  Tempted by My Brother's Mafia Rival
    'tempted-by-my-brother-s-mafia-rival':
        "Her brother has one rule. Stay away from Dante DiMarco.\nMia Franco has lived a sheltered life and she's still a virgin. She's starting at Santa Lucia Academy, and before she does her brother lays down one rule. Nothing romantic with Dante DiMarco, the heir to the rival family. Mia falls for Dante anyway and keeps it a secret. The desire between them keeps building, and so does her defiance of her own family. Before long her brother and the man she loves are locked in a feud, and Mia is caught right between them.",
    # 6.5M  Weapons! Women! Wild West!
    'weapons-women-wild-west':
        "Reborn as a broke cowboy. His quest is to become the King of the Wild Frontier.\nJoey is a loser in the modern world, and then he's suddenly pulled inside a Wild West game set in the age of westward expansion, with America at war with itself. He's reborn there as a cowboy without a cent to his name. The game hands him a main quest he can't turn down, Become the King of the Wild Frontier, along with three women taken as prisoners of war. He's tied to a game system that runs on affection. The more those three women like him, the more modern weapons and skills Joey unlocks. Winning their hearts is how a loser like Joey gets armed.",
    # 5.5M  Nanny to the Mafia Single Daddy
    'nanny-to-the-mafia-single-daddy':
        "A widowed mafia godfather. His daughter's new nanny.\nVictor is a mafia godfather who shut love out of his life when his wife died without warning. Then Jennifer comes to work as his daughter's nanny, and he starts losing the control he's always kept, letting himself feel things he thought were behind him. What follows is a heated back and forth between them. There are misunderstandings to get past and more than one close call with death before they finally find their way to each other. For a man who closed his heart when his wife died, opening it again is the biggest risk of all.",
    # 3.7M  When He Finally Looked Back
    'when-he-finally-looked-back':
        "She walked into the fire on his wedding day.\nFor three years Lena has put up with his fury as her atonement. She's also dying. On his wedding day she walks into a fire to finally put an end to her suffering. Instead she's reborn. And by the time he finally looks back, she may not be there waiting.",
    # 2.5M  The Scheming Maid
    'the-scheming-maid':
        "A tutor tore her family apart. Twenty years later, she wants payback.\nTwenty years ago Emma Harrison had the kind of life people envied, the pampered daughter of a rich family. Then a private tutor named Therese Parish came into their lives, and her meddling brought everything down. Emma's father got caught up in an affair, her little brother died, and her mother had a severe breakdown. The happy family was gone. Emma swore that one day Therese would pay for every bit of the suffering she caused.",
    # 1.1M  The complete transformation of a girl
    'the-complete-transformation-of-a-girl':
        'She came for a paycheck. They thought she was the tester.\nGrace Miller is a rookie lingerie designer whose sister is seriously ill and needs surgery. To earn the money she slips into the company Chris Sullivan runs, and someone there mistakes her for an erotic experience tester. One mix up leads to another, and she ends up signing a BDSM training contract. All Grace has ever wanted is for people to respect her as a designer. Instead her work keeps getting written off as having no desire in it at all.',
}

FACTS = {
    'my-poor-husband-is-a-billionaire':
        'Stella had a one-night stand with a stranger and mistook the man as someone who had plunged her into a prostitution scandal and ruined her life. Three years later, Stella married a man named Ethan in a flash and the two soon fell in love. However, gradually Stella found Ethan similar to the man three years ago. Even worse, Ethan had been hiding his CEO identity from Stella. Unable to accept the truth, Stella divorced Ethan.',
    'your-loser-husband-is-a-big-shot':
        'Nathan gave up his family empire for love. When his wife and daughter were kidnapped, he chose self-sacrifice and endured three years of torment. Returning home, he found his wife entangled with her former flame and his daughter distant. Heartbroken, he reclaimed his position as heir to the billion-dollar fortune. He severed ties with the past and embarked on a new life.',
    'tempest-the-last-mecha':
        "Broken by his parents' deaths, Colt Thorne, the Mech King, hides as a lowly janitor after being saved by Freya. But when Freya, the woman he secretly loves, is betrayed and forced into a lethal mech duel, Colt must unleash his hidden identity. Unlocking his legendary 100% Neural Sync, he commands The Tempest to crush his enemies and save the world from an extinction-level alien swarm!",
    'love-at-the-end-of-lies':
        "On her engagement day, Ava discovers that her fiancé́ Dylan has secretly misused her savings. Instead of feeling guilty, Dylan and his mother insulted her, prompting her to call off the engagement in anger. In a desperate attempt to raise funds to save her grandmother's house, Ava agrees to marry Noah, the grandson of her elderly neighbor. Unknown to Ava, Noah is a billionaire who mistakenly believes Ava is a gold digger.",
    'after-divorce-i-become-heiress':
        'In order to get rid of her billionaire father’s overwhelming love, Sally hid her real identity as the wealthy heiress and chose to make her own living. Her husband Felix cheats on her. In retaliation, Sally married Aiden in a flash. Unknown to her, Aiden is CEO of Taylor family. After the divorce, Sally chose to reveal her identity but was jeered by Felix and others. Aiden didn’t believe her either. But when would Sally and Aiden know their real identities?',
    'boss-she-said-no-again':
        "Abandoned for sixteen years, Rowena returns to New York to reclaim her mother's inheritance. Posing as the Kingsley second son's fiancée, she plans a breakup as cover. But she saves Damien Kingsley, the Kingsley's elder son, from a mafia attack. Intrigued, Damien forces into her life. As Rowena navigates traps from her scheming family and ruthless Mrs. Kingsley, her bond with Damien shifts from enemies to allies as they uncover the truth behind a mysterious murder.",
    'a-virgin-surrogate-for-the-billionaire':
        "Honey Myers becomes a surrogate for NFL star Tristan Brown to pay for her sister's surgery, navigating through challenges, betrayal, and unexpected love, ultimately finding happiness and family together despite numerous obstacles and threats from Tristan's ex-fiancée, Jennifer.",
    'scent-of-the-ceo-s-lost-love':
        'After surviving years of abuse and hiding her identity as the last heir of the Lynn family, blind perfumer Stella is forced into a contract marriage with cold CEO Conor, unaware that she is the girl who once saved his life. As danger closes in, both must confront their shared past, the lies between them, and the growing bond neither expected.',
    'serendipitous-love':
        'The day Sylvia Cooper joined Taylor Corp. marked the day she was wedded to a total stranger named Brian Anders, who promptly disappeared right after they signed the marriage papers.A year later, Liam Taylor, the CEO of Taylor Corp., returned from France.Over time, Liam found himself harboring unique emotions for Sylvia. Liam was also pursuing a divorce. When he arrived at the Courthouse, standing patiently waiting at the entrance was none other than Sylvia…',
    'love-not-lost-to-memory':
        'After giving birth to twins for the powerful Todd family, Vera Bell is drained of her blood in the delivery room to save their chosen heir, Finn Todd—leaving her lifeless, clutching a blood-stained lucky charm. Seven years later, mute and stripped of her memory, Vera survives by scavenging while raising her daughter, Grace Bell.',
    'how-to-snatch-a-billionaire':
        "Tired of dull blind dates, Harley impulsively kisses a handsome stranger passing by. But he won't let go easily, sparking an unexpected romantic encounter.",
    'seducing-mr-sterling-the-ice-cold-heir':
        "To save her dying sister, Emma agrees to seduce ruthless CEO Ethan Sterling and ruin his reputation. But as she enters his world of power and secrets, she finds herself falling for the man she was meant to destroy. Torn between love and betrayal, Emma must choose: her sister's life—or the man who just might save her own.",
    'all-my-love-all-for-you':
        'To raise money for her tuition, Mona Leed works as a courier, where she meets Jim Judd and unexpectedly becomes pregnant. Her family, however, plans to marry her off to an older man in exchange for 500 thousand dollars. Determined to escape her family’s control, Mona decides to keep the baby and refuses the arranged marriage. Learning of her situation and recognizing Mona’s innocence, Jim steps in, bringing her home and caring for her.',
    'pampered-by-him':
        'Lia was arranged a blind date by her stepmother. To teach the guy a lesson, Lia caught a handsome guy, Jeremy, and kissed him in front of the man. Although the man left her angrily, she found herself trapped in bigger trouble. That man was the famous President of the Smith Group, Jeremy Smith, at the cafe to meet his contract bride. However, she did not show up, and Lia snatched his first kiss instead.',
    'billionaire-alpha-wont-let-me-go':
        'Zoe Lopez returns to New York with her young son and crosses paths with Alexander Blackwood, a past lover—and a werewolf. As old feelings resurface, buried secrets of power, family, and supernatural heritage threaten their lives. With danger looming, their intense romance reignites, forcing them to face a fate beyond their control.',
    'divorced-then-find-my-mr-right':
        'After a brutal betrayal, Hazel loses her marriage, child, and dignity. Rising from despair, she reunites with Evan, a powerful man who helps her reclaim her career, self-worth, and take control of her fate.',
    'three-chances-i-m-gone-forever':
        "After sacrificing everything—her fortune, her health, even a kidney—for her childhood love Erwin, Kama is betrayed and replaced by the manipulative Circe. Vowing to give Erwin just three chances, she rises from heartbreak to reclaim her power, wealth, and dignity—with billionaire Landon by her side. When the final chance is gone, so is Kama's mercy.",
    'hurt-me-love-me':
        'Even though Katherine and Eric got married, Eric was still entangled with Riley, which caused Katherine great suffering. Despite her pain, Katherine endured it out of guilt and deep love. Unexpectedly, she became pregnant again, but Eric continued to neglect and hurt her. For the sake of their lost child, Katherine decided to divorce.',
    'a-woman-scorned':
        'Carynn Hughes was always the black sheep of her family. Her father did not like her, her stepmother was cruel, and her stepsister seduced her fiancee, Archiebald Murray. After a chance encounter with the powerful Jayden Lewis and his ill grandfather on the same day, she was given the opportunity to start a new life. Although her parents blamed her for Archiebald’s affair with her stepsister, Carynn manages to turn them into the town’s laughingstock during their engagement.',
    'the-professor-i-m-dating-is-a-billionaire':
        "Reese, a talented student, is humiliated after being cheated on by her boyfriend and losing her internship at WG Group due to the strict professor, Sanger. Unbeknownst to her, Sanger is actually WG's CEO, secretly paving the way for her comeback. Through a high-stakes robot competition, Reese proves herself, wins love, and discovers Sanger's true identity.",
    'a-dangerous-engagement-the-bride-he-mustn-t-touch':
        "I ran from the mob at 18. My dad, the mafia king, couldn't find me. And neither could Angelo, my stepbrother, my father's legally adopted son. When my father suddenly died, Angelo found me and brought me back. Though we were never raised together, Angelo saw me as his innocent responsibility. He insisted I marry for my safety and the empire's stability, and took charge of selecting my future husband. But I wanted Angelo to marry me.",
    'rescued-by-the-rugged-mountain-man':
        "Mia, a city girl who was hurt by her ex, was beaten and banished to a deep mountain covered in ice and snow. In the midst of hunger and cold, she was even attacked by a wild wolf. At this moment, a powerful man saved her. The two started off disliking each other but gradually developed feelings for one another. Mia also discovered the man's true identity and punished her evil ex. Eventually, they lived happily together.",
    'billionaire-playboy-s-replacement-bride':
        "Under her stepmother's pressure, Alicia substitutes her sister to marry a stranger. Disheartened, she finds solace in Lucius's company for a night. Later, at the wedding, she discovers Lucius is the groom, sparking an unexpected love story.",
    'i-don-t-want-any-of-you-three':
        "The wealthy heiress Serena Sterling once thought she would marry one of her three childhood friends when she grew up. However, she unexpectedly discovered that all three of them had only been feigning affection for her due to her father's financial support for them, and that their true feelings were actually for the driver's daughter, Bella.",
    'oops-the-ceo-s-birthday-is-ruined':
        "Tiffany spoiled her son Billy from birth, never setting limits. He grows into a reckless, entitled brat—wrecking his father's boss's party, humiliating guests, destroying a million-dollar car, and setting it on fire, while she looks the other way. But her blind love comes at a cost: Billy destroys his own future, ruins his father's career, and ultimately sends Tiffany to prison. Only behind bars does she finally understand the price of her love.",
    'tempted-by-my-brother-s-mafia-rival':
        'When sheltered virgin Mia Franco transfers to Santa Lucia Academy, her brother forbids her from getting romantically involved with rival heir Dante DiMarco, but she secretly falls for him, leading to escalating desire, defiance of her family, and a feud between her brother and her lover, Dante.',
    'weapons-women-wild-west':
        'Joey, a modern-day underdog loser, is suddenly transported into a Wild West game world set during the era of westward expansion and the American Civi War—only to find himself reborn as a penniless cowboy. Forced to accept a main quest titled "Become the King of the Wild Frontier,” he is assigned three female war captives and bound to an affection-based game system.By increasing their favorability, Joey can unlock modern weapons and skills.',
    'nanny-to-the-mafia-single-daddy':
        "Mafia godfather Victor closes his heart off to love after the unexpected death of his wife. But when Jennifer, his daughter's nanny, enters his life, he finds himself losing control and giving in to feelings he never expected. As their passionate push-and-pull romance unfolds, the two must overcome misunderstandings and survive brushes with death before finally finding their way to each other.",
    'when-he-finally-looked-back':
        'After three years of enduring his wrath as atonement, the terminally ill Lena walks into a fire on his wedding day to end her torment, only to be unexpectedly reborn.',
    'the-scheming-maid':
        "20 years ago, Emma Harrison, the privileged daughter of a wealthy family, enjoyed a life that many envied. However, their world crumbled due to the meddling of a private tutor, Therese Parish. Emma's father became entangled in an affair, her younger brother tragically passed away, and her mother suffered a severe breakdown, shattering their once-happy family.Emma swore to herself that she would definitely make Therese pay back for all the suffering she inflicted on her.",
    'the-complete-transformation-of-a-girl':
        'Rookie lingerie designer Grace Miller sneaks into Chris Sullivan\'s company to earn money for her seriously ill sister\'s surgery, but is mistaken for an erotic experience tester. After a series of mix‑ups, she ends up signing a BDSM training contract. All she ever wanted was to be taken seriously as a designer, yet her creations are mocked as "devoid of desire.',
}

SOURCES = {
    'my-poor-husband-is-a-billionaire': ('platform', 'https://www.dramaboxdb.com/movie/41000107888/my-poor-husband-is-a-billionaire'),
    'your-loser-husband-is-a-big-shot': ('platform', 'https://www.dramaboxdb.com/movie/42000007948/your-loser-husband-is-a-big-shot'),
    'tempest-the-last-mecha': ('platform', 'https://www.dramaboxdb.com/movie/42000018529/tempest-the-last-mecha'),
    'love-at-the-end-of-lies': ('platform', 'https://www.dramaboxdb.com/movie/41000112267/love-at-the-end-of-lies'),
    'after-divorce-i-become-heiress': ('platform', 'https://www.dramaboxdb.com/movie/41000105193/after-divorce-i-become-heiress'),
    'boss-she-said-no-again': ('platform', 'https://www.dramaboxdb.com/movie/42000004139/boss-she-said-no-again'),
    'a-virgin-surrogate-for-the-billionaire': ('platform', 'https://www.dramaboxdb.com/movie/41000115756/a-virgin-surrogate-for-the-billionaire'),
    'scent-of-the-ceo-s-lost-love': ('platform', 'https://www.dramaboxdb.com/movie/42000007731/scent-of-the-ceo-s-lost-love'),
    'serendipitous-love': ('platform', 'https://www.dramaboxdb.com/movie/41000100811/serendipitous-love-dubbed'),
    'love-not-lost-to-memory': ('platform', 'https://www.dramaboxdb.com/movie/41000122380/love-not-lost-to-memory-dubbed'),
    'how-to-snatch-a-billionaire': ('platform', 'https://www.dramaboxdb.com/movie/41000103082/how-to-snatch-a-billionaire'),
    'seducing-mr-sterling-the-ice-cold-heir': ('platform', 'https://www.dramaboxdb.com/movie/41000115012/seducing-mr-sterling-the-ice-cold-heir'),
    'all-my-love-all-for-you': ('platform', 'https://www.dramaboxdb.com/movie/41000107530/all-my-love-all-for-you'),
    'pampered-by-him': ('platform', 'https://www.dramaboxdb.com/movie/41000100822/pampered-by-him'),
    'billionaire-alpha-wont-let-me-go': ('platform', 'https://www.dramaboxdb.com/movie/41000113458/billionaire-alpha-won-t-let-me-go'),
    'divorced-then-find-my-mr-right': ('platform', 'https://www.dramaboxdb.com/movie/42000002416/divorced-then-find-my-mr-right'),
    'three-chances-i-m-gone-forever': ('platform', 'https://www.dramaboxdb.com/movie/41000118844/three-chances-i-m-gone-forever'),
    'hurt-me-love-me': ('platform', 'https://www.dramaboxdb.com/movie/41000109091/hurt-me-love-me'),
    'a-woman-scorned': ('platform', 'https://www.dramaboxdb.com/movie/41000100870/a-woman-scorned'),
    'the-professor-i-m-dating-is-a-billionaire': ('platform', 'https://www.dramaboxdb.com/movie/41000118236/the-professor-i-m-dating-is-a-billionaire'),
    'a-dangerous-engagement-the-bride-he-mustn-t-touch': ('platform', 'https://www.dramaboxdb.com/movie/42000003947/a-dangerous-engagement-the-bride-he-mustn-t-touch'),
    'rescued-by-the-rugged-mountain-man': ('platform', 'https://www.dramaboxdb.com/movie/42000004809/rescued-by-the-rugged-mountain-man'),
    'billionaire-playboy-s-replacement-bride': ('platform', 'https://www.dramaboxdb.com/movie/41000122434/billionaire-playboy-s-replacement-bride'),
    'i-don-t-want-any-of-you-three': ('platform', 'https://www.dramaboxdb.com/movie/42000009982/i-don-t-want-any-of-you-three'),
    'oops-the-ceo-s-birthday-is-ruined': ('platform', 'https://www.dramaboxdb.com/movie/42000009374/oops-the-ceo-s-birthday-is-ruined'),
    'tempted-by-my-brother-s-mafia-rival': ('platform', 'https://www.dramaboxdb.com/movie/42000021675/tempted-by-my-brother-s-mafia-rival'),
    'weapons-women-wild-west': ('platform', 'https://www.dramaboxdb.com/movie/42000008417/weapons-women-wild-west'),
    'nanny-to-the-mafia-single-daddy': ('platform', 'https://www.dramaboxdb.com/movie/42000023486/nanny-to-the-mafia-single-daddy'),
    'when-he-finally-looked-back': ('platform', 'https://www.dramaboxdb.com/movie/42000011262/when-he-finally-looked-back'),
    'the-scheming-maid': ('platform', 'https://www.dramaboxdb.com/movie/41000100888/the-scheming-maid'),
    'the-complete-transformation-of-a-girl': ('platform', 'https://www.dramaboxdb.com/movie/42000017312/the-complete-transformation-of-a-girl'),
}
