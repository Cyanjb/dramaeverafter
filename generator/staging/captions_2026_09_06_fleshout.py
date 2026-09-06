# -*- coding: utf-8 -*-
"""Flesh-out batch, 6 Sep 2026. The thin pages Cyan's carve-outs keep
visible to Google (FLESHOUT-QUEUE.md): popular, new, or a lead actor, and
still carrying no synopsis. Every one is BELOW top-300 reach, so her 16 Aug
ruling applies and these are written without her manual review. Facts
fetched live from each platform page, 6 Sep, banked in
facts_fleshout_2026-09-06.json. Gated by check + readback + copy detector.

Two titles from the fetch are deliberately NOT here:
  dirty-work        its platform text is a marketing blurb with no story
                    in it, and inventing one is the thing the rules forbid.
"""

CAPTIONS = {
    # FACTS: To save her daughter, Harper Reed marries Klaus Wolfe—New York's most feared mafia godfather—in 
    # FACTS: her stepsister's place. On the wedding day, he sees right through her and calls her a gold digge
    # FACTS: r. He gives her one choice: jump into a shark pool, or watch her whole family die. Then she jump
    # FACTS: s without hesitation. That shatters his frozen heart. But she finds out that—this marriage is wa
    # FACTS: y worse than death. Lydia deeply hates her. Uncle Richard wants the Don's chair. And "Black Fox"
    # FACTS:  is dragging everyone to hell...
    '100-day-contract-mafia-s-dangerous-desire':
        "Jump in the shark pool, or watch your family die.\nHarper Reed marries Klaus Wolfe in her stepsister's place to save her daughter, and New York's most feared godfather sees straight through her on the wedding day and calls her a gold digger. Then he gives her the choice. She jumps without pausing, and something frozen in him gives way. What she learns after that is that this marriage is worse than the pool. Lydia hates her, Uncle Richard wants the Don's chair, and Black Fox is pulling everyone down together.",

    # FACTS: A destitute orphan Layla accidentally stumbles into the Wolf King Kai's suite, and one night sou
    # FACTS: l-binds them. He throws a check at her. She rips it up and slaps him. A month later, Layla disco
    # FACTS: vers she's pregnant with sextuplets. Her greedy stepfamily sells her for $100,000. Kai transform
    # FACTS: s into a silver wolf, rescues her, and declares her his destined mate. Layla joins K-Group on he
    # FACTS: r own merit. Kai secretly courts her. But Kai's rumored fiancée Chloe humiliates Layla—until Kai
    # FACTS:  breaks the engagement publicly. Chloe colludes with a dark warlock to sell Layla, revealing she
    # FACTS: 's a sacred vessel to break the wolf clan's curse. Kai rescues her and exposes Chloe as an ident
    'a-cinderella-for-wolf-king':
        "She ripped up his check and slapped him.\nLayla is a destitute orphan who stumbles into the Wolf King Kai's suite, and one night soul binds them. He offers money. She tears it up. A month later she is pregnant with sextuplets and her greedy stepfamily sells her for a hundred thousand dollars, so Kai turns silver wolf, takes her back and names her his destined mate. She joins K Group on merit while he courts her quietly. His rumoured fiancee Chloe humiliates her until he ends the engagement in public, then sells her to a dark warlock, because Layla is a sacred vessel who can break the wolf clan's curse. She is also the true Grey heiress, swapped at birth.",

    # FACTS: In A Farm Girl's Reckoning movie, bound by her late father's dying wish, ex-special forces soldi
    # FACTS: er Hanna Carter buried her past and settled into quiet farm life, marrying Jake and raising thei
    # FACTS: r five kids together. For years his family lived off her sacrifice. Then Jake turned on her, sho
    # FACTS: wing up with his mistress to demand a divorce while his family schemed to steal the farm and thr
    # FACTS: ow Hanna and her children out. Cornered at last, Hanna stops holding back — and Jake's family re
    # FACTS: alizes too late she was never just a farm girl.
    'a-farm-girl-s-reckoning':
        "Her father's dying wish bought them years of her silence.\nHanna Carter was special forces before she buried it, married Jake and raised five children on a quiet farm, and his family lived off that sacrifice without ever asking what she gave up. Then Jake arrives with his mistress to demand a divorce while his relatives move to take the farm and put her and the children off it. Cornered, Hanna stops holding back, and by the time they understand she was never just a farm girl it is much too late.",

    # FACTS: A witch cursed Prince Alexander to sleep for a century. Only a Jones daughter's kiss can break i
    # FACTS: t. Catherine, once bound to Prince Arthur who chose her half-sister, enters Vandros Castle and a
    # FACTS: wakens Alexander through a three-night ritual. His soul had escaped as a bat, guarding her since
    # FACTS:  childhood. They fall in love. Arthur storms their wedding, but Catherine rejects him. Two princ
    # FACTS: es duel on a cliff. She chooses Alexander. Arthur falls to a fiery end. They wed, sealed by bloo
    # FACTS: d and heart.
    'a-hundred-years-of-you':
        'A century of sleep, and only a Jones kiss ends it.\nA witch cursed Prince Alexander to sleep for a hundred years. Catherine, once promised to Prince Arthur before he chose her half sister, walks into Vandros Castle and wakes him through a three night ritual. His soul had slipped out as a bat and has been guarding her since she was a child. They fall in love, Arthur storms the wedding and she turns him down flat, and the two princes take it to a cliff edge where she makes her choice plain.',

    # FACTS: In my past life, my husband's niece drowned my newborn. To protect their precious heiress, the m
    # FACTS: afia family told me to let it go. When I refused, my own husband murdered me. Now, I’ve been reb
    # FACTS: orn on the morning it all happened. This time, I secretly send my son to my father, the most pow
    # FACTS: erful Mafia Godfather in the city. But when I return to the party, another baby still ends up in
    # FACTS:  the pool. Predictably, my husband and his family rush to destroy the body to cover it up. Now t
    # FACTS: here's just one question: whose child did their golden girl really kill?
    'a-mother-s-vengeance':
        'Her husband killed her for refusing to let it go.\nIn her last life the niece drowned her newborn, and the mafia family told her to swallow it to protect their precious heiress. She would not, so her husband murdered her. Now she is awake on the morning it all happened, and this time she gets her son quietly to her father, the most powerful Godfather in the city. Then she goes back to the party, and another baby still ends up in the pool. The family rushes to destroy the body as expected, which leaves one very interesting question about whose child their golden girl actually killed.',

    # FACTS: Evelyn, an ordinary high school student, is publicly humiliated after her crush on a popular hoc
    # FACTS: key player is exposed. Devastated, she musters up the courage to send him nudes anonymously in h
    # FACTS: opes of catching his eye. But she accidentally sends the pics to Colton instead, the captain of 
    # FACTS: the hockey team who always teases her. What will happen between them?
    'a-spicy-text-to-my-nemesis':
        'She sent the photos to the wrong hockey player.\nEvelyn is an ordinary high school student until her crush on a popular player is exposed and the whole school enjoys it. She gathers herself and sends him something anonymous to get his attention, and it goes to Colton instead, the team captain who has never stopped teasing her.',

    # FACTS: After a painful rebirth, Eleanor, once a devoted wife and mother, finds her family's affection r
    # FACTS: eserved for Lydia, her husband William's true love. Betrayed by William's bigamy and her childre
    # FACTS: n's cruelty, she abandons them, secretly applying to Harvard. As she builds a new life in scienc
    # FACTS: e, William and the children, now suffering under Lydia's abuse, realize their loss. They beg for
    # FACTS:  forgiveness, but Eleanor, hardened by their betrayal, coldly rejects them. Choosing her own pat
    # FACTS: h, she leaves them behind to embrace a future of independence and self-worth.
    'after-i-took-back-my-love':
        "Reborn, and the family still loves Lydia best.\nEleanor was a devoted wife and mother, and this time she can see exactly where William's affection goes and always went. Between his bigamy and her children's cruelty there is nothing worth staying for, so she leaves and quietly applies to Harvard. She builds a life in science while the four of them live with Lydia, and by the time they understand what they threw away and come asking, Eleanor is not interested in taking any of it back.",

    # FACTS: Nia is a 300-pound Omega mocked by the entire pack as a disgusting fat wolf. When Alpha Zayne ch
    # FACTS: ooses her as his Luna, she believes she has finally been loved. She poisons herself, bleeds for 
    # FACTS: him, tears her own fur to keep him warm, and carries his child. Then she overhears the truth: Za
    # FACTS: yne only used her as a womb and plans to kill her after the baby is born. Betrayed, abused, and 
    # FACTS: forced through unbearable trials, Nia awakens as a legendary White Wolf. Now she returns under a
    # FACTS:  new name, not for love, but to save the child Zayne killed. The Alpha finally falls in love wit
    # FACTS: h her beauty, but the woman who once loved him has already died.
    'after-the-330-pound-fat-wolf-left-the-alpha-went-crazy-with-regret':
        'He only ever wanted the womb.\nNia is an Omega the whole pack mocks, and when Alpha Zayne picks her as his Luna she believes she is finally loved. She poisons herself for him, bleeds for him, tears out her own fur to keep him warm, and carries his child. Then she overhears what the plan actually is, which ends with her dead once the baby arrives. Betrayed and put through trials nobody should survive, she wakes as a legendary White Wolf and returns under a new name, not for love, but for the child he killed.',

    # FACTS: When the Blaires turn Elena, the black sheep of the family, into a scapegoat to cover for their 
    # FACTS: adoptive daughter's crimes, she is sent to a reform school to be tortured. Three years later, on
    # FACTS:  the eve of her release, Elena just wants a fresh start—but her evil family has other plans.
    'after-the-reformatory-my-family-begs-me-home':
        "Three years in a reform school for her sister's crimes.\nThe Blaires need someone to carry the blame for their adoptive daughter, and Elena is the black sheep, so Elena is who they hand over. Reform school tortures her for three years. On the eve of her release all she wants is a clean start somewhere else, which is exactly when her family decides they want her back.",

    # FACTS: A gifted contract mage, Layla, spent her past life collecting ninety-nine sacred cores to help h
    # FACTS: er contracted beast, the Sacred Whale Neil, take human form—only to have Neil pierce her heart a
    # FACTS: nd push her into the Bloodtide Trench the moment he transformed. Reborn on the day of the contra
    # FACTS: ct ceremony, Layla abandons the Sacred Whale and chooses a dying little spirit snake instead. Ne
    # FACTS: il, now in human form, teams up with her sister Evelyn to humiliate her, but the little snake tu
    # FACTS: rns out to be Poseidon, the Sea Emperor. As past betrayals and old wounds resurface, Neil kneels
    # FACTS:  in regret—too late. Only Poseidon stands by her side. This time, Layla will never waste herself
    'after-the-sacred-whale-betrayed-me-i-contracted-poseidon':
        'Ninety nine sacred cores, and he put one through her heart.\nLayla spent a whole life collecting them so her contracted beast, the Sacred Whale Neil, could take human form, and the moment he had it he pierced her heart and pushed her into the Bloodtide Trench. Reborn on the day of the contract ceremony, she leaves him standing and picks a dying little spirit snake instead. Neil teams up with her sister Evelyn to make her look ridiculous for it, and then the snake turns out to be Poseidon, the Sea Emperor.',

    # FACTS: Her parents were cruelly killed by werewolves, yet she has now become the Fated Luna of the were
    # FACTS: wolf Alpha. However, their love defies werewolf traditions, sparking conflict as they face rogue
    # FACTS:  wolves and ancient prophecies. With hidden powers and fierce rivalries at play, love, destiny, 
    # FACTS: and power clash in this thrilling tale of passion and survival.
    'alpha-revenge-wolf-king-and-his-human-luna':
        'Werewolves killed her parents. One of them is her mate.\nShe is the Fated Luna of the werewolf Alpha now, which is a difficult thing to hold alongside what happened to her family. Their love breaks with werewolf tradition and the pack feels it, rogue wolves circle, and ancient prophecies start coming due. Hidden powers and old rivalries do the rest.',

    # FACTS: In Alpha's Regret After His Pregnant Luna's Death movie, Alpha Declan is tricked by his brother'
    # FACTS: s treacherous widow, Olivia, into locking his pregnant Luna, Evelyn, in a Silver Cage for three 
    # FACTS: days. He thought he was teaching her a lesson, but it was all part of Olivia's schemes to take E
    # FACTS: velyn's place as Luna! Declan refuses to believe Evelyn, even as she begs him to save her, convi
    # FACTS: nced it's all an act. He only realizes he's condemned his own Luna and their pup to death when h
    # FACTS: e sees their dead bodies with his very own eyes.
    'alpha-s-regret-after-his-pregnant-luna-s-death':
        "He locked his pregnant Luna in a Silver Cage.\nAlpha Declan is played by Olivia, his brother's treacherous widow, into caging Evelyn for three days. He tells himself it is a lesson. It is Olivia's plan to take the Luna's place. Evelyn begs him to save her and he refuses to believe a word of it, sure she is performing. He gets his proof when he sees the bodies of his Luna and their pup with his own eyes.",

    # FACTS: A mural artist and an architectural engineer are instantly drawn to each other, but their buddin
    # FACTS: g romance comes to a halt when the past comes back to haunt them.
    'art-of-falling-in-love':
        'They fell fast. The past caught up faster.\nShe paints murals and he engineers buildings, and neither of them needs long to work out where this is heading. What stops it is not a doubt or a rival or bad timing. It is the thing behind them, arriving on its own schedule, asking both of them to answer for it.',

    # FACTS: GT endurance driver Kai Mercer is pushed into a reserve role after refusing his sponsor’s sexual
    # FACTS:  advances, while struggling with his father’s debts and his mother’s illness. Through an anonymo
    # FACTS: us platform, Kai develops an intimate relationship with a mysterious man named Nox, unaware that
    # FACTS:  Nox is actually Adrian Cross, his new team owner and a four-time World Endurance Champion. As K
    # FACTS: ai falls for both identities, Adrian’s secret creates a dangerous conflict of trust and power. W
    # FACTS: hen the truth is exposed, Kai walks away. After kidnappings, threats, professional investigation
    # FACTS: s, and an ethics hearing, the two eventually rebuild their relationship, while Kai earns his pla
    'below-the-red-line':
        "He said no to his sponsor and lost his seat.\nKai Mercer is a GT endurance driver pushed into a reserve role after refusing his sponsor, carrying his father's debts and his mother's illness at the same time. Through an anonymous platform he gets close to a man called Nox, without knowing Nox is Adrian Cross, his new team owner and a four time World Endurance Champion. Kai falls for both versions of him, which turns into a serious problem about trust and power the moment the truth is out, and he walks.",

    # FACTS: At her engagement ceremony, Evadne is slapped, shamed, and rejected by Valerius, the Black Drago
    # FACTS: n prince, after her scheming twin sister steals the sacred power meant to protect her future. Br
    # FACTS: anded impure before the entire realm, Evadne makes one impossible choice: she marries Aurelius, 
    # FACTS: the cursed god-king everyone fears. But her sister’s stolen power hides a cruel secret—every sha
    # FACTS: meful child she conceives can be forced into Evadne’s body. What they don’t know is Evadne’s own
    # FACTS:  gift can purify any bloodline and awaken extinct Titans. The more they try to ruin her, the mor
    # FACTS: e divine monsters she gives birth to.
    'betrayed-then-birthed-titans':
        "Her sister stole her power. Her gift makes Titans.\nEvadne is slapped, shamed and rejected at her own engagement by Valerius, the Black Dragon prince, after her twin takes the sacred power meant to protect her. Branded impure in front of the realm, she marries Aurelius, the cursed god king everyone fears. The stolen power carries a cruel catch, because every shameful child her sister conceives can be forced into Evadne's body. Nobody has worked out that Evadne can purify any bloodline and wake extinct Titans, so the harder they push, the more divine monsters she delivers.",

    # FACTS: Sunny star quarterback Seth hides a love-starved heart behind his perfect facade. When violent e
    # FACTS: x-linebacker "Mad Dog" Matthew transfers into his team and becomes his forced roommate, their ex
    # FACTS: plosive fights bleed into charged, unbearable tension. Seth falls hard, until he spots his rival
    # FACTS:  Ethan's birthday carved into Matthew’s necklace, convinced he's just a stand-in...
    'blitzed-by-my-rival-s-obsession':
        "He fell for his rival. The necklace says otherwise.\nSeth is the sunny star quarterback with a love starved heart behind the perfect face. Matthew is the violent ex linebacker they call Mad Dog, transferred onto his team and installed as his forced roommate. Their fights turn into something neither of them can hold still, and Seth falls hard. Then he sees his rival Ethan's birthday carved into Matthew's necklace, and decides he knows exactly what he is.",

    # FACTS: Desperate to pay for her sick mother’s treatment, restaurant waitress Anna is betrayed by her bi
    # FACTS: ological father, Richard, and sent into a deadly trap controlled by an East Side crime boss. Usi
    # FACTS: ng her combat skills and intelligence, she survives, defeats Victor, and escapes with crucial ev
    # FACTS: idence. With the help of Leo, an undercover operative and Thomas’s son, Anna rises through Los A
    # FACTS: ngeles’ criminal underworld, taking control of casinos and territory. But she soon discovers tha
    # FACTS: t her entire rise has been part of Thomas’s larger power game. Together, Anna and Leo expose the
    # FACTS:  money-laundering operation and bring down Thomas and Richard.
    'blood-rose-crushing-the-cartel':
        "Her own father sold her into the trap.\nAnna waits tables and needs money for her sick mother's treatment, and Richard hands her to an East Side crime boss expecting that to be the end of it. She fights her way out with the evidence, and with Leo, an undercover operative and Thomas's son, she climbs through the Los Angeles underworld taking casinos and territory. Then she works out that her whole rise has been a move in Thomas's bigger game.",

    # FACTS: Aria, a human teenage girl, suddenly finds herself homeless after her family goes bankrupt. She'
    # FACTS: s forced to live in her car, a shameful secret she needs to hide from the vicious bullies at her
    # FACTS:  elite private high school. One day, she discovers that she's the mate of both Damon, the werewo
    # FACTS: lf heir, and Levi, the vampire prince. These two supernaturally handsome boys have opposite pers
    # FACTS: onalities. One as passionate as fire, and the latter as cold as ice. Which one is her true love?
    # FACTS:  Aria later discovers that there's more to her real identity than she thought. It's a secret tha
    # FACTS: t could destroy everything.
    'bound-by-crimson-and-silver':
        "She lives in her car and hides it from the whole school.\nAria's family goes bankrupt and she keeps the shame of it quiet from the vicious bullies at her elite private high school. Then she finds out she is the mate of both Damon, the werewolf heir, and Levi, the vampire prince, one of them all fire and the other all ice. Working out which is real is the smaller problem, because there is more to who she is than she knows, and it is the kind of secret that could bring the whole thing down.",

    # FACTS: Beast King Elden bears a lethal lightning curse—any living thing he touches burns to cinders. Hu
    # FACTS: man girl Vera is the only one who can endure his touch. To break the curse, he forces her into m
    # FACTS: arriage by holding her mother hostage. Vera resents him, but glimpses his sincere heart: he heal
    # FACTS: s her, shields her, and crumbles when she prays for him barefoot through brambles. The curse can
    # FACTS:  be broken by consummation—but Vera would die from the backlash. Elden makes an antidote, but th
    # FACTS: e villainess Lia swaps it for poison. On their wedding night, the curse lifts—but Vera collapses
    # FACTS: , never to wake. Elden mourns her for six years at her grave. But Vera is alive, raising twin ch
    'bound-to-the-ruthless-beast':
        'Everything he touches burns. She does not.\nBeast King Elden carries a lethal lightning curse, and Vera is the only living thing that can take his touch, so he holds her mother hostage and forces the marriage. She resents him and still catches the truth of him, healing her, shielding her, going to pieces when she prays for him barefoot through brambles. The curse breaks with consummation and the backlash would kill her, so he makes an antidote, and the villainess Lia swaps it for poison. Six years he mourns at her grave, and six years she is alive in the slums with twins.',

    # FACTS: Leo, the legendary surfing champion, loses his title to a mysterious newcomer named Ruslan. But 
    # FACTS: the biggest shock comes when he discovers that Ruslan is the man from his unforgettable night. F
    # FACTS: orced into an uneasy partnership, the two rivals find themselves drawn to each other as secrets,
    # FACTS:  danger, and betrayal close in. Behind their battle for glory lies a hidden truth about Ruslan—a
    # FACTS: nd their forbidden desire has only just begun...
    'caught-in-his-current':
        'The newcomer who took his title is the man from that night.\nLeo is the legendary surfing champion until Ruslan turns up out of nowhere and beats him. Then he recognises him. Forced into an uneasy partnership, the two rivals keep being pulled toward each other while secrets and danger and betrayal close in, and there is a truth about Ruslan still waiting.',

    # FACTS: Betrayed by her boyfriend. Hunted down by her father. Forced to mate with a ruthless Alpha King.
    # FACTS:  Cora thought her life was over until she escaped and accidentally marked a dangerous, magnetic 
    # FACTS: stranger. Left with no choice, she accepted a fake mating proposal from that stranger, totally u
    # FACTS: naware that her "contract mate" is the very Alpha King she’s desperately trying to escape...
    'caught-the-ruthless-alpha-s-runaway-luna':
        'She escaped the Alpha King and marked a stranger.\nBetrayed by her boyfriend, hunted by her own father and forced toward a mating she never agreed to, Cora runs, and in the middle of it accidentally marks a dangerous, magnetic stranger. With nothing else left she accepts his offer of a fake mating, which is a fine plan except for one detail she has not worked out yet about who he is.',

    # FACTS: Tammy is a single mom who needs money to look for her son. Desperate for work, Tammy takes a a w
    # FACTS: et nurse job in a powerful manor, never guessing the cold, intimidating master is the father of 
    # FACTS: her son. Nor that her touch alone breaks his years-long trauma with women. What he doesn't know 
    # FACTS: is that he's about to hire her.
    'ceo-s-irresistible-wet-nurse':
        'She took the job to fund the search for her son.\nTammy is a single mother out of options when she is hired as a wet nurse in a powerful manor, with no idea the cold and intimidating master of the house is the father of the boy she is looking for. Her touch also happens to be the only thing that gets past his years of trauma around women, which is not something either of them saw coming.',

    # FACTS: My billionaire CEO is my contract-married husband! My grandmother fell seriously ill, so I flash
    # FACTS: -married a stranger for her surgery fees. We entered a one-year contract marriage. I bumped into
    # FACTS:  a handsome man, who I later found out was the CEO of the company I wanted to join! But little d
    # FACTS: id I know, he was the man I married... As the contract period nears its end, we are supposed to 
    # FACTS: divorce. However, both of us lost our marriage certificates. Now what do we do? Does this mean w
    # FACTS: e can't get divorced after all?
    'ceo-that-intern-is-actually-your-wife':
        'They flash married for surgery fees. Now they cannot divorce.\nHer grandmother needed an operation, so she agreed to a one year contract marriage with a stranger and got on with her life. Then she bumps into a handsome man who turns out to be the CEO of the company she is trying to join, and also the husband she signed for. The contract is nearly up and they are meant to split. Both of them have lost the marriage certificate.',

    # FACTS: Elena, the daughter of the Lord of Yalkreon, ventures out in search of sacred tree sap to save h
    # FACTS: er mother from a deadly ice curse. Along the way, she unexpectedly rescues Hades, King of the Un
    # FACTS: derworld, who immediately decides to make her his queen. But Elena is betrayed by her fiancé, th
    # FACTS: en forcibly sold as a sacrifice to the Lord of the Frostlands by her cruel stepmother and greedy
    # FACTS:  father. Just as all hope is lost during the sacrificial ceremony, Hades descends in overwhelmin
    # FACTS: g force, punishes everyone who has wronged her, and takes her back to the Underworld under his p
    # FACTS: rotection.
    'chained-by-hades-the-underworld-king':
        'She went for tree sap. She came back with Hades.\nElena, daughter of the Lord of Yalkreon, sets out for sacred tree sap to lift a deadly ice curse from her mother, and on the way she rescues Hades, King of the Underworld, who decides then and there she will be his queen. Her fiance betrays her, and her stepmother and greedy father sell her as a sacrifice to the Lord of the Frostlands. The ceremony is already under way when Hades comes down on the lot of them.',

    # FACTS: Eva, a cold-blooded assassin, accidentally triggers a deadly curse after killing the man chosen 
    # FACTS: as her soulmate. Her only chance of survival is Leo—a clumsy Cupid apprentice who has failed his
    # FACTS:  divine exam for ten thousand years. Bound by an invisible life thread, they must stay within th
    # FACTS: ree meters of each other or die. With only seven days left, the mismatched pair is forced to run
    # FACTS:  from a powerful assassin organization while uncovering a conspiracy that has been manipulating 
    # FACTS: love itself. Eva has never trusted anyone. But when Leo repeatedly risks his life to save hers, 
    # FACTS: she must decide whether love is her greatest weakness—or her only way out.
    'clumsy-cupid':
        'Three metres apart or they both die.\nEva is a cold blooded assassin who kills the man chosen as her soulmate and triggers a deadly curse doing it, and her only way out is Leo, a clumsy Cupid apprentice who has been failing his divine exam for ten thousand years. An invisible life thread ties them together with a hard limit on distance and seven days on the clock. They run from a powerful assassin organisation while uncovering a conspiracy that has been manipulating love itself, and Eva has never trusted anyone in her life.',

    # FACTS: Exiled half-beast prince Cassian storms back from the dead, slaughters his father, and seizes th
    # FACTS: e throne in a bloodbath. His first prey, Vera, the ice-cold former queen. The woman who crushed 
    # FACTS: their love for a crown, married his father, and cast him into the beast pit to rot. Consumed by 
    # FACTS: rage, the ruthless new king forces his stepmother into his bed as his personal captive and swear
    # FACTS: s to kill Lucian, Vera's royal son with the dead king. Then a bombshell drops. His so-called hal
    # FACTS: f-brother shares his rare, exclusive beast blood. Vera has hidden the truth of Lucian's identity
    # FACTS: .
    'crowned-in-his-claws':
        'He came back from the dead and took the throne in blood.\nExiled half beast prince Cassian returns, kills his father and seizes the crown, and his first target is Vera, the ice cold former queen who crushed what they had for a crown, married his father and threw him into the beast pit. He installs his stepmother in his bed as his captive and swears to kill Lucian, her son by the dead king. Then the ground moves. His so called half brother carries the same rare beast blood he does, which means Vera has been hiding what Lucian actually is.',

    # FACTS: After a devastating betrayal that decimates two powerful wolf packs, young Nora Reed is forced i
    # FACTS: nto a mating bond with Alpha Drake, her enemy, her savior, and the man who believes she's respon
    # FACTS: sible for his family's death. For three years, Drake torments her, determined never to love her.
    # FACTS:  But when he finally claims her body and then shoves her aside, Nora shatters. She cuts their ma
    # FACTS: gical soul-bond and disappears. Years later, she returns not as Nora Reed, but as Nadia Moon, he
    # FACTS: iress to a royal European pack, cloaked in wealth, power. Her mission is clear, protect her chil
    # FACTS: dren, reclaim her power, and avoid Drake at all costs.
    'crowned-in-silver-blood':
        'He tormented her for three years, then let her go.\nA betrayal guts two powerful wolf packs, and young Nora Reed is forced into a mating bond with Alpha Drake, who is her enemy and her savior and the man convinced she killed his family. He spends three years making sure she knows he will never love her. Then he claims her body and shoves her aside, and that is what breaks her. Nora cuts their soul bond and vanishes. She comes back as Nadia Moon, heiress to a royal European pack, with wealth and power and a clear mission. Protect her children, take back what is hers, and stay away from Drake.',

    # FACTS: He's the strongest Alpha alive—cursed so that anyone who touches him burns to ash. She's a wolfl
    # FACTS: ess mage apprentice who fell from the sky straight into his arms… and didn't burn. Desperate to 
    # FACTS: find her fated mate, Aria takes a job as Kael's personal maid, unaware the cold, dangerous Alpha
    # FACTS:  is already falling for her. But a dark prophecy looms: their child will carry a curse far deadl
    # FACTS: ier than his—and bearing it could cost Aria her life. When rivals attack and Aria's life hangs b
    # FACTS: y a thread, Kael will face the deadliest mountain in the world to save her. Because some fates a
    # FACTS: ren't written—they're fought for.
    'cursed-alpha-s-fated-luna':
        'Anyone who touches him turns to ash. She fell into his arms.\nKael is the strongest Alpha alive, and the curse came with the title. Aria is a wolfless mage apprentice who lands on him out of the sky and does not burn. Hunting for her own fated mate, she takes work as his personal maid without noticing the cold and dangerous Alpha is already gone on her. A dark prophecy is sitting over both of them, because their child would carry something far worse than his curse, and carrying it could kill her.',

    # FACTS: For ten years, janitor Maya scrimps and saves while raising her daughter Lily almost entirely on
    # FACTS:  her own—only to discover that her husband, Adrian, is actually a multimillionaire who has lavis
    # FACTS: hed all his love and affection on his first love and her son. Completely heartbroken, Maya leave
    # FACTS: s with Lily. She is later revealed to be the daughter of a fallen war hero, and after reclaiming
    # FACTS:  her true identity, she becomes the long-lost beloved heiress of the powerful Harrington family.
    # FACTS:  When Adrian loses his business, his family, and the wife and daughter he took for granted, he f
    # FACTS: alls to his knees and begs for forgiveness. Lily gives him only one final answer: “Daddy, we’re 
    'daddy-we-re-done':
        'Ten years of scrimping, and he was a multimillionaire.\nMaya cleans for a living and raises Lily almost entirely alone, going without so they can get by. Then she finds out Adrian has money, and has been spending all of it, and all of his affection, on his first love and her son. Maya leaves with her daughter. What surfaces afterward is that she is the daughter of a fallen war hero and the long lost heiress of the powerful Harrington family. By the time Adrian has lost the business, the family and them, he is on his knees, and Lily has one line left for him.',

    # FACTS: Evelyn was once the beloved human daughter of four mighty Norse god-kings. But when the false sa
    # FACTS: intess Freya framed her, the fathers who raised her chose to believe a liar. They stripped her b
    # FACTS: lessing, tortured her soul, stole her blood, and forced her to beg for death. Only after Evelyn 
    # FACTS: truly dies do they discover the truth: Freya was the monster all along, and Evelyn's real mother
    # FACTS:  has been trapped beneath the World Tree. Now the gods want their daughter back. But the little 
    # FACTS: girl they destroyed no longer wants to return.
    'daughter-of-the-four-norse-god-kings':
        "Four god kings raised her, then believed a liar.\nEvelyn was the beloved human daughter of four Norse god kings until the false saintess Freya framed her, and the fathers who brought her up chose Freya. They stripped her blessing, tortured her soul, took her blood and left her begging to die. Only after she is actually dead do they learn Freya was the monster and that Evelyn's real mother has been trapped beneath the World Tree the whole time. Now the gods want her back, and the girl they destroyed is not interested.",

    # FACTS: In Divorced and Desired! My Trio of Elite Suitors movie, Ivory, a secret billionaire heiress, ha
    # FACTS: s invested her time and money in growing her husband. After three years of marriage, her husband
    # FACTS: , Nelson...
    'divorced-and-desired-my-trio-of-elite-suitors':
        'Three years funding his rise, and he wants out.\nIvory is a secret billionaire heiress who has spent her time and her money growing her husband Nelson into somebody. Three years of marriage buys her exactly what that kind of investment usually buys.',

    # FACTS: Sarah Loren is a widow with a teenage son, Ethan Cole is a big shot CEO who wants to acquire her
    # FACTS:  company. He is arrogant, brilliant, and unnecessarily good looking, and he'll stop at nothing t
    # FACTS: o get what he wants, and what he wants… is Sarah's heart.
    'do-me-over':
        'He came to buy her company. He stayed for her.\nSarah Loren is a widow raising a teenage son when Ethan Cole moves to acquire her business. He is a big shot CEO, arrogant and brilliant and unnecessarily good looking, and he does not lose. He also stops caring about the company somewhere along the way, because what he actually wants is her heart.',

    # FACTS: Ava Lin’s Manhattan wedding turns into a nightmare when a voice from three years in the future w
    # FACTS: arns her not to marry Ryan Hall. Her groom has secretly registered a marriage with her best frie
    # FACTS: nd, Mia Chen, who is already pregnant with his child. In the original timeline, Ava was framed a
    # FACTS: s unstable, stripped of her career and trust, and forced into psychiatric evaluation. This time,
    # FACTS:  she refuses to break down for their cameras. Guided by her future self, Ava gathers marriage re
    # FACTS: cords, recordings, legal proof, and the hidden safeguards left by her parents. As Ryan, Mia, and
    # FACTS:  the powerful Hall family try to silence her and seize control of her inheritance, Ava turns the
    'don-t-say-i-do':
        "A voice from three years ahead says do not marry him.\nAva Lin's Manhattan wedding goes strange fast when her future self warns her about Ryan Hall, who has quietly registered a marriage to her best friend Mia Chen, already pregnant with his child. In the timeline she is being warned about, Ava was painted as unstable, stripped of her career and pushed into psychiatric evaluation. This time she does not fall apart for their cameras. Guided from the future, she gathers records, recordings, legal proof and the safeguards her parents left her, and turns the fake wedding into a public reckoning.",

    # FACTS: Lucas returns to LA as the mysterious CEO of Apex Group, ready to marry his beloved girlfriend, 
    # FACTS: Evelyn. But Evelyn mistakes him for a nobody and leaves him for a "richer man." Little does she 
    # FACTS: know, she just dumped the most powerful billionaire in LA. Then, a stunning female CEO enters Lu
    # FACTS: cas’s life and she gets down on one knee and proposes to Lucas. CEO meets CEO. Together, they be
    # FACTS: come the most powerful couple in the world and make every idiot who underestimated them regret i
    # FACTS: t!
    'fake-husband-hidden-king':
        'She dumped him for a richer man. He owns the city.\nLucas comes back to LA as the mysterious head of Apex Group, intending to marry Evelyn, who takes one look, decides he is a nobody and leaves. She has just walked out on the most powerful billionaire in town. Then another chief executive turns up in his life, goes down on one knee and proposes to him, and together they make everyone who underestimated either of them regret it.',

    # FACTS: She faked her death. Three years later, Sierra comes back to her own funeral with a new identity
    # FACTS: . She takes down her unfaithful ex and her best friend who betrayed her. She vows to take her th
    # FACTS: ree-year-old son back. For revenge, she teams up with Julian, the heir to the most powerful fami
    # FACTS: ly. In a game of power, they go from sworn enemies to each other's only hope. Finally the truth 
    # FACTS: comes out. They take everything back and find their way back to each other.
    'faked-my-death-destroyed-the-billionaire':
        'She turned up at her own funeral with a new name.\nSierra faked it and stayed gone for three years, and she comes back to take down the unfaithful ex and the best friend who helped him, and to get her three year old son back. For the revenge she teams up with Julian, heir to the most powerful family in play, and they go from sworn enemies to the only ally the other has. When the truth finally lands they take back everything and find their way to each other.',

    # FACTS: Medieval times. Dragons rule the continent. Lydia is forced by her family to marry the "savage" 
    # FACTS: Dragon King, Lucian, in her sister's place. She flees into the night — and in a blizzard-buried 
    # FACTS: cabin, she encounters a dragon-shifter whose power is spiraling out of control. To save him, she
    # FACTS:  gives him her virginity... The next day, she is captured. Her secret dragon pregnancy is expose
    # FACTS: d, and she is branded an unclean sinner, dragged onto the trial platform. Meanwhile, Lucian sear
    # FACTS: ches for her frantically, tearing a scale from his own heart to cast a tracking spell. When the 
    # FACTS: crystal ball reveals the truth — that Lydia is the woman who saved him, unintentionally carrying
    'fate-of-the-dragon-s-bride':
        "Married off in her sister's place, and she ran.\nDragons rule the continent, and Lydia's family hands her to the savage Dragon King Lucian instead of her sister. She flees into the night and shelters in a cabin buried by a blizzard, where she finds a dragon shifter whose power is tearing loose. Saving him costs her something she does not get back. The next day she is captured, her dragon pregnancy exposed, and she is branded unclean and dragged onto the trial platform, while Lucian tears a scale from his own heart to cast a tracking spell and find her.",

    # FACTS: Luca Conri is the wolf-less runt of the Nightreign Pack, whose bark is bigger than his bite. Tor
    # FACTS: mented by his own pack and hunted by rivals, Luca is reluctantly put under the protection of his
    # FACTS:  dominant Alpha, and older brother's best friend, Dalton. However, everything changes when the t
    # FACTS: wo become fated mates, a bond that violates the natural order of the pack. As enemies close in a
    # FACTS: nd traditions try to tear them apart, Luca and Dalton must decide if they want to give into thei
    # FACTS: r lustful temptations in a forbidden romance that threatens their own lives.
    'fated-to-his-brother-s-alpha':
        "The runt of the pack is mated to his brother's best friend.\nLuca Conri has no wolf and a bark much bigger than his bite, tormented by his own pack and hunted by rivals, so he ends up under the reluctant protection of Dalton, the dominant Alpha who is also his older brother's best friend. Then they turn out to be fated mates, which violates the natural order the pack is built on. With enemies closing in and tradition working to pull them apart, they have to decide whether this is worth what it will cost them.",

    # FACTS: A firefighter sets his own home ablaze for his mistress’s drill, trapping his three-year-old dau
    # FACTS: ghter inside. The mother watches via security cam, but he dismisses her pleas, calls the child i
    # FACTS: llegitimate, and prioritizes the assessment. As flames consume the nursery, the daughter’s ghost
    # FACTS:  emerges—still apologizing for being “bad.” Only when charred remains, a melted necklace, and fi
    # FACTS: nal recordings surface does he break down. But forgiveness never comes. The daughter’s last word
    # FACTS: s: “Daddy didn’t love me.” He is arrested; she fades into ash, finally free.
    'firefighter-husband-burned-his-daughter-driven-to-desperate-regret':
        "He set the fire himself, with his daughter inside.\nA firefighter stages a blaze at his own home for his mistress's drill, trapping his three year old. The mother watches it on the security camera and he waves off everything she says, calls the child illegitimate and puts the assessment first. As the nursery goes up, the daughter appears still apologising for being bad. He only breaks when the charred remains, the melted necklace and the final recordings surface, and forgiveness is not on offer.",

    # FACTS: At a superpower‑fueled academy where strength reigns supreme, ordinary girl Sophie unexpectedly 
    # FACTS: awakens the extremely rare ability of Future Sight. Yet the very first vision she sees of the fu
    # FACTS: ture shows her locked in a passionate kiss with Damien, the campus’s cold‑hearted, sharp‑tongued
    # FACTS:  student council president! Convinced this could never happen, Sophie is determined to keep her 
    # FACTS: distance from him. But fate plays a cruel joke on her: that very same night, her mother remarrie
    # FACTS: s‑‑and Damien suddenly becomes her stepbrother. As the embrace and shared bed from her prophecy 
    # FACTS: start coming true one after another, misunderstandings and romantic tension between them keep bu
    'fleeing-the-future-i-saw-with-him':
        'Her first vision is kissing the boy she cannot stand.\nAt an academy where strength decides everything, ordinary Sophie wakes the rare gift of Future Sight, and what it shows her is Damien, the cold and sharp tongued student council president, with his mouth on hers. She decides it will never happen and sets about avoiding him. That night her mother remarries and Damien becomes her stepbrother, and the scenes from the prophecy start arriving one after another.',

    # FACTS: For years, demigod Elena endured the arrogance and cruelty of Alec, Sovereign of Olympus—only to
    # FACTS:  have him reject her on her eighteenth birthday. But fate gives her a second chance when she mee
    # FACTS: ts Stefano, the powerful King of the Titans. His choice is immediate and public, "I want her. No
    # FACTS:  one else." Just as Elena finally finds her true match, Alec and his lover set out to destroy th
    # FACTS: em. Can Elena escape their trap, and will Stefano save her in time?
    'forbidden-bonds-fated-to-the-ocean-god':
        'Rejected on her eighteenth birthday, chosen the same week.\nElena has spent years absorbing the arrogance and cruelty of Alec, Sovereign of Olympus, and he rejects her the moment she turns eighteen. Fate offers her a second chance when she meets Stefano, the powerful King of the Titans, who makes his choice publicly and immediately, saying he wants her and nobody else. Alec and his lover set out to destroy them both, and the trap is already being built.',

    # FACTS: When the Duke dies suddenly, his greedy brother Richard steals the title and fortune. Overnight,
    # FACTS:  Cordelia—the Duke’s only daughter—is stripped of her nobility and secretly blinded in a vicious
    # FACTS:  plot. To protect her commoner lover, Luke, she brutally breaks his heart and drives him away. B
    # FACTS: elieving she abandoned him for status, Luke leaves for the frontier, fueled by hatred. Years lat
    # FACTS: er, Luke returns as Luciano Thorne, the Empire's most powerful war hero and new Duke. Meanwhile,
    # FACTS:  Cordelia is trapped at home, desperately guarding what's left of her inheritance. When her uncl
    # FACTS: e forces the blind Cordelia to marry a 70-year-old merchant, Luciano arrives with an immense dow
    'forced-to-marry-my-ruined-ex-the-duke-s-revenge':
        "She broke his heart to keep him alive.\nWhen the Duke dies, his greedy brother Richard takes the title and the money, and Cordelia is stripped of her nobility and secretly blinded in the process. To keep her commoner lover Luke out of it she is deliberately cruel to him, and he leaves for the frontier believing she traded him for status. Years later he is back as Luciano Thorne, the Empire's most powerful war hero and the new Duke, while Cordelia is trapped at home guarding what is left. Her uncle is marrying her off to a seventy year old merchant when Luciano arrives with a dowry to claim her himself.",

    # FACTS: Ever since my Omega sister saved me from wolfsbane poisoning, she used that life debt to control
    # FACTS:  every detail of my existence—including my wedding. She picked the flowers, designed the theme, 
    # FACTS: and even tried on wedding dresses with my groom while he smiled in delight. Every time I voiced 
    # FACTS: my outrage, they weaponized the past to silence me: "She saved your life! Why are you always act
    # FACTS: ing like the villain?" If they want the wedding so badly, they can keep each other. I discarded 
    # FACTS: my ring and returned to my royal pack, took my throne as Alpha Queen.
    'from-puppet-bride-to-alpha-queen':
        'Her sister tried on wedding dresses with the groom.\nEver since she saved her from wolfsbane poisoning, her Omega sister has used that life debt to run every part of her life, and the wedding is where it peaks. She picks the flowers, sets the theme, and stands there with the groom smiling at her in the mirror. Any objection gets met with the same line about who saved whose life and why she is always the villain. Fine. They can keep each other. She leaves the ring behind, goes back to her royal pack and takes the throne.',

    # FACTS: In 2006, Marcel "The Sniper" Wallace wins THE LEAGUE title, then loses his wife to rival Tyler M
    # FACTS: urray's hitman. He vanishes into a fast-food job for twenty years. Lured back as coach, he reuni
    # FACTS: tes with his resentful son Mars, a LEAGUE star. Marcel proves himself through impossible shots w
    # FACTS: hile Murray escalates to kidnapping and blackmail. At the Hall of Fame, Marcel reveals his ident
    # FACTS: ity and Murray confesses to murder. Victory comes when Mars accepts twenty unsent birthday lette
    # FACTS: rs and they embrace.
    'full-court-legend':
        'He won the title, lost his wife, and disappeared for twenty years.\nMarcel Wallace, the Sniper, takes the league in 2006 and then loses his wife to a hitman sent by his rival Tyler Murray. He spends the next twenty years working fast food. Lured back as a coach, he walks into his resentful son Mars, now a league star. Marcel proves what he still is with shots that should not go in, while Murray escalates to kidnapping and blackmail. At the Hall of Fame the truth comes out and Murray confesses to murder, and the win is Mars finally opening twenty unsent birthday letters.',

    # FACTS: Mira is the long-lost biological daughter of the Hale family of Ashen City. Yet after returning 
    # FACTS: home, she repeatedly gives way to their adopted daughter, Lia—surrendering her room, her place a
    # FACTS: s a dragon rider, and even half of her mother’s inheritance. Before the wedding, Draegoth—the bo
    # FACTS: nded dragon Garrick personally tamed and the only keepsake Mira has left from her mother—is trai
    # FACTS: ned to obey Lia alone and nearly kills Mira. Realizing that Garrick, her fiancé of eight years, 
    # FACTS: has always seen her as nothing more than a gullible woman, Mira walks barefoot across burning co
    # FACTS: als, breaks off their engagement, and turns to marry Theron, the Lord of the North, who has wait
    'goodbye-my-ex-i-m-marrying-the-dragon-prince-final':
        "They trained her mother's dragon to obey her sister.\nMira is the long lost daughter of the Hale family and keeps giving way to their adopted daughter Lia, handing over her room, her place as a dragon rider, even half her mother's inheritance. Before the wedding, Draegoth, the last keepsake she has from her mother, is turned on her and nearly kills her. Realising Garrick has spent eight years seeing her as gullible, Mira walks barefoot over burning coals, ends the engagement, and turns to Theron, Lord of the North, who has waited the same eight years.",

    # FACTS: Born with the sealed bloodline of Hades, Lia Thorne is raised as the lost daughter of the wealth
    # FACTS: y Lancaster family. But when her return exposes their crimes and shatters their "lucky" adopted 
    # FACTS: daughter Ava's perfect life, Lia is branded a curse. On her twelfth birthday, her parents drug h
    # FACTS: er and leave her at Black Rose Manor, the most feared mafia estate in Black Bay. They expect her
    # FACTS:  to die. Instead, mafia queen Veronica Knight and executioner Damian Wolf protect her as their l
    # FACTS: ittle princess. As enemies close in, Lia's hidden power awakens, turning every betrayal into dea
    # FACTS: dly karma.
    'hades-mafia-princess':
        'Her parents drugged her and left her at Black Rose Manor.\nLia Thorne carries the sealed bloodline of Hades and is raised as the lost daughter of the wealthy Lancasters. Her return exposes their crimes and ruins the perfect life of Ava, their lucky adopted daughter, so they brand her a curse and dispose of her on her twelfth birthday at the most feared mafia estate in Black Bay, expecting her to die there. Instead the mafia queen Veronica Knight and the executioner Damian Wolf take her in as their little princess.',

    # FACTS: Olivia saved Adam, the silent serpent shapeshifter no one wanted, and spent years nursing him ba
    # FACTS: ck to health. Yet when fire trapped her and her sister Chloe, Adam chose Chloe and left Olivia t
    # FACTS: o die. Reborn on the day the twin serpent guards are chosen, Olivia gives both brothers to Chloe
    # FACTS:  and fights her way into the family business. When Chloe arranges Olivia's kidnapping, Adam once
    # FACTS:  again sacrifices her safety for Chloe's birthday. But this time, Olivia has planned her escape.
    # FACTS:  Declared dead, she becomes the secret ally of Jason Astor, the ruthless Serpent King and her fa
    # FACTS: mily's greatest enemy. As Olivia destroys the family that treated her as disposable, Adam return
    'he-chose-my-sister-so-i-chose-the-serpent-king':
        'She nursed him for years. He let her burn.\nOlivia saved Adam, the silent serpent shapeshifter nobody wanted, and spent years getting him well again. When fire trapped her and her sister Chloe, he chose Chloe. Reborn on the day the twin serpent guards are chosen, Olivia hands both brothers to Chloe and fights her way into the family business instead. Chloe arranges her kidnapping and Adam trades her safety for a birthday party, but this time Olivia has already planned the exit. Declared dead, she becomes the secret ally of Jason Astor, the ruthless Serpent King her family fears most.',

    # FACTS: Klare is an overlooked nurse at Venus Hospital, struggling with severe anxiety after a family tr
    # FACTS: agedy. Her only comfort is submitting online to a mysterious “Master,” whose commands make her f
    # FACTS: eel safe. But in real life, her new boss, Dance Gordon, is arrogant, sharp-tongued, and always t
    # FACTS: argeting her. By day, they clash at the hospital. By night, he is the perfect Master behind the 
    # FACTS: screen, giving all his patience and tenderness to his one and only — “Cake.” Enemies in real lif
    # FACTS: e. Addicted online.
    'he-paid-for-one-night-then-wanted-forever':
        'By day he targets her. By night he is her Master.\nKlare is an overlooked nurse at Venus Hospital carrying severe anxiety after a family tragedy, and her one comfort is submitting online to a stranger whose commands make her feel safe. Her new boss Dance Gordon is arrogant and sharp tongued and never off her case. The two men are the same man, and behind the screen he gives all his patience and tenderness to the one person he calls Cake. Enemies in the daylight, addicted to each other in the dark.',

    # FACTS: "I'm Jason Hayes, and today, I am reborn. In my past life, I was weak. In this one, I choose to 
    # FACTS: be the villain." From a humble waiter to the king of the underworld, Jason fights back against e
    # FACTS: very bully and outmaneuvers the most powerful figures, including the father-in-law of a crime lo
    # FACTS: rd. His ironclad rule: touch what's mine, and you won't survive. Only when he stops stepping asi
    # FACTS: de does Jason learn a brutal truth: the world makes way for those who refuse to move.
    'he-s-done-being-nice':
        "In his last life he was weak. This time he picks villain.\nJason Hayes comes back knowing exactly what being nice cost him, and he is finished being nice. He goes from waiter to king of the underworld, working through every bully in his way and outplaying the most powerful people in the city, including a crime lord's father in law. His rule is simple, which is that touching what belongs to him ends badly. The brutal part he learns on the way up is that the world only makes room for people who refuse to move.",

    # FACTS: Bankrupt heiress Isolde signs a three-year mistress contract with Savien Thorne, heir to the Tho
    # FACTS: rn Group, just to cover her mother’s life-saving medical bills. The second the contract ends, sh
    # FACTS: e’s ready to walk away for good. Until she finds out she’s pregnant. His arranged fiancée learns
    # FACTS:  the secret, and torments her at every turn. Worse — she’s never been anything but a double for 
    # FACTS: the other woman. She moves out and cuts all ties. But he’s not letting her get away.
    'his-caged-love':
        "A three year contract, and then the test was positive.\nBankrupt heiress Isolde signs on as Savien Thorne's mistress to cover her mother's medical bills, and plans to walk the second the term ends. The pregnancy changes the arithmetic. His arranged fiancee finds out and makes a project of tormenting her, and then Isolde learns the worst part, which is that she has only ever been a double for the other woman. She moves out and cuts every tie. He has no intention of letting that stand.",

    # FACTS: Ava Russell on the eve of her arranged marriage, is drugged by her fiancé Nico Moretti and has h
    # FACTS: er hair brutally shaved off by his comrade Scarlett. Refusing to swallow this humiliation, Ava s
    # FACTS: ecretly contacts Damian Costello, the powerful heir of the Costello family who has secretly love
    # FACTS: d her for twelve years. On the wedding day, when Nico tries to sneak Ava into his family through
    # FACTS:  a shabby, hidden ceremony and Scarlett publicly strips off her wig to mock her, Damian arrives 
    # FACTS: with a magnificent fleet to marry Ava in style. With the help of Damian and the Commission, Nico
    # FACTS:  and Scarlett are stripped of their power and arrested for violating family laws, while Ava fina
    'his-partner-her-revenge':
        'They shaved her head the night before the wedding.\nAva Russell is drugged by her fiance Nico Moretti and his comrade Scarlett takes her hair, and Ava decides not to swallow it. She quietly contacts Damian Costello, heir to the Costello family, who has loved her in silence for twelve years. On the day, Nico tries to slip her into his family through a shabby hidden ceremony and Scarlett pulls off her wig in front of everyone, which is when Damian arrives with a fleet to marry her properly. With the Commission behind them, Nico and Scarlett lose their power and their freedom.',

    # FACTS: Erin Vance’s 18th wedding anniversary turns into a nightmare when she discovers her husband Dere
    # FACTS: k cheating with her best friend Sofia. Betrayed and abandoned, Erin is forced to start over with
    # FACTS:  nothing. With help from Gavin Bower, she enters the “Miss Intercontinental” contest and rises f
    # FACTS: rom a housewife to a champion through her talent and determination. Defeating Sofia and exposing
    # FACTS:  her scandals, Erin rebuilds her life. Gavin, secretly the president of K Group, supports her wh
    # FACTS: ile letting her prove herself. After overcoming betrayal and danger, Erin regains her dignity an
    # FACTS: d begins a new chapter with Gavin.
    'i-became-the-ceo-s-most-beloved':
        'Her anniversary, her husband, her best friend.\nErin Vance finds Derek with Sofia on their eighteenth wedding anniversary and is left with nothing to start over from. Gavin Bower helps her into the Miss Intercontinental contest, where a housewife turns into a champion on talent and sheer stubbornness. She beats Sofia, drags her scandals into the light, and rebuilds. Gavin is quietly the president of K Group the whole time, and he lets her prove it herself.',

    # FACTS: I’m Seraphina, ocean princess. In my last life, I loved shark lord Kael, yet he held me down whi
    # FACTS: le his lover Lira stabbed my heart with venom crystal. Reborn on my mate-picking day, I shocked 
    # FACTS: everyone by choosing Rhys, the playful dragon eel playboy. Kael seethed, ignored me when assassi
    # FACTS: ns poisoned me, and knelt begging me to ditch Rhys later. But Lira’s fake fragility hides deadly
    # FACTS:  malice—she just pushed me into deadly undertow. Can Rhys reach me before I drown?
    'i-chose-the-playboy-eel-to-abandon-my-shark-lover':
        "Her shark lord held her down while his lover killed her.\nSeraphina is an ocean princess who loved Kael, and in her last life he pinned her while Lira drove a venom crystal into her heart. Reborn on her mate picking day, she stuns the court by choosing Rhys, the playful dragon eel playboy nobody takes seriously. Kael seethes, ignores her when assassins poison her, then kneels begging her to drop Rhys. Lira's fragility is a costume over something lethal, and she has just pushed Seraphina into a deadly undertow.",

    # FACTS: Three years after leaving Onyx Stormfire, Serafina meets him again at the Grand Clan Gathering h
    # FACTS: osted by the Ravenwing clan—only to find another woman at his side. No one knows that Serafina o
    # FACTS: nce gave up half of her own dragonfire to save Onyx from death, then pretended she had fallen fo
    # FACTS: r his younger brother, Corin, so Onyx would hate her and stop searching for the truth. The divid
    # FACTS: ed flame has left her unable to shift, and the last of her dragonfire is fading. She has returne
    # FACTS: d only to see him one final time. When Corin reveals the truth, Onyx risks everything to reach h
    # FACTS: er. Their twin dragonfires finally reunite, saving them both. Locke is exposed as the poisoner b
    'i-gave-my-flame-up':
        'She gave him half her dragonfire and made him hate her.\nSerafina meets Onyx Stormfire again three years on at the Grand Clan Gathering, with another woman beside him. Nobody knows she once gave up half her own fire to keep him alive, then pretended to fall for his younger brother Corin so he would stop looking for the truth. The divided flame has left her unable to shift and the rest of it is going out. She has come back to see him once. Then Corin tells him, and Onyx risks everything to reach her.',

    # FACTS: After three years on the battlefield, the wife returns victorious, but unexpectedly pregnant! Th
    # FACTS: e former Grand Marshal of the empire's army had retired due to his parents' last wishes and marr
    # FACTS: ied a woman known for her bravery and ambition. She aspired to achieve greatness on the battlefi
    # FACTS: eld, and before she left, he gifted her a legendary spear forged from thousand-year-old cold iro
    # FACTS: n. Three years later, she returns clad in silver armor, pregnant, and holding another man's hand
    # FACTS: . She presents a letter of divorce, declaring, "My husband must be a heroic figure who stands ta
    # FACTS: ll, not a weak scholar with no strength." Unbeknownst to her, the seemingly powerless man she ha
    'i-gave-my-wife-a-red-tasseled-spear':
        "She came home from war pregnant, holding another man's hand.\nThe empire's former Grand Marshal retired on his parents' last wishes and married a woman known for her bravery and ambition. She wanted greatness on the battlefield, so he gave her a legendary spear forged from thousand year old cold iron and let her go. Three years later she returns in silver armour with a letter of divorce, telling him a husband must be a heroic figure who stands tall, not a weak scholar with no strength. She has no idea the powerless man she married is the empire's guardian deity, and she is about to watch him put the armour back on.",

    # FACTS: In I’m Pregnant It’s Not Yours movie, husband prefers secretary, who looks like his white moonli
    # FACTS: ght, over his wife Iris. Calmly, Iris asks for a divorce, revealing that the baby she's carrying
    # FACTS:  isn't his. Five years later, she returns powerfully with her new flame, while Husband is left d
    # FACTS: rowning in regret.
    'i-m-pregnant-it-s-not-yours':
        'She asked for a divorce very calmly, and then explained why.\nIris watches her husband choose his secretary, who conveniently resembles his white moonlight, and does not make a scene about it. She asks to end the marriage, and mentions on the way out that the baby she is carrying was never his. Five years later she comes back with money, standing and a new man, and he is still drowning in it.',

    # FACTS: Wealthy heiress Vivian Sterling publicly breaks her engagement after catching fiancé Bryce with 
    # FACTS: her stepsister. Having secretly recovered from paralysis months ago, she stands from her wheelch
    # FACTS: air to reclaim her power. That night, she meets Adrian, a dangerous, motorcycle-riding mechanic 
    # FACTS: who saves her from harassment. After a one-night stand, she proposes a contract marriage to esca
    # FACTS: pe Bryce's stalking. Vivian believes Adrian is merely a handsome working-class man, unaware he i
    # FACTS: s the true heir to the Hale dynasty—and Bryce's most feared uncle. A decade earlier, Adrian was 
    # FACTS: the one who pulled her from a fatal car crash and bore the scars; Bryce stole the credit and her
    'i-married-my-cheating-ex-s-uncle':
        'She stood up out of the wheelchair and ended it.\nVivian Sterling catches her fiance Bryce with her stepsister and breaks the engagement in public, rising from the chair she secretly stopped needing months ago. That night a motorcycle riding mechanic named Adrian gets her out of a bad situation, and after one night she proposes a contract marriage to keep Bryce off her. She thinks Adrian is working class and handsome. He is the true heir to the Hale dynasty and the uncle Bryce fears most, and a decade ago he pulled her from a crash and wore the scars while Bryce took the credit.',

    # FACTS: On her wedding day, Jagger Hamilton abandons Avery for his adopted sister Tatum. Jagger's uncle 
    # FACTS: Beckett, Manhattan's feared "Ice Blade," marries her instead. Three years later, Avery carries B
    # FACTS: eckett's long-awaited child, but Jagger and Tatum return and brutally kill the baby. Beckett exa
    # FACTS: cts brutal revenge, crippling and disowning them. Years later, Avery and Beckett welcome a healt
    # FACTS: hy son, while a ruined, disabled Jagger—rejected by the family—takes his own life.
    'i-married-the-groom-s-uncle':
        "Abandoned at the altar, married by his uncle instead.\nJagger Hamilton leaves Avery on their wedding day for his adopted sister Tatum, and his uncle Beckett, the man Manhattan calls the Ice Blade, marries her in his place. Three years on Avery is carrying Beckett's long awaited child when Jagger and Tatum come back and brutally take the baby from them. Beckett's revenge cripples and disowns them both. Years later Avery and Beckett have a healthy son, and a ruined Jagger, cast out by his own family, ends it himself.",

    # FACTS: Lord Julian Thornfield burns Adeline’s village, turns her into a vampire, and forces her to beco
    # FACTS: me his dead wife’s replacement. Even his daughter, Eve, calls her “Mama.” When Adeline tries to 
    # FACTS: die, Eve’s strange power hurls them a hundred years into the past. There, Julian is not a cruel 
    # FACTS: lord yet. He is a scarred human slave in a circus cage, whipped as a monster. Adeline only wants
    # FACTS:  to hand Eve back and escape, but the child’s broken heart ties her to them both. Then the caged
    # FACTS:  man asks who she is, and Adeline answers, “I’m your future wife.”
    'i-was-my-vampire-husband-s-dead-wife':
        "He burned her village and made her his dead wife.\nLord Julian Thornfield turns Adeline and installs her as a replacement, and even his daughter Eve calls her Mama. When Adeline tries to end it, Eve's strange power throws all three of them a hundred years into the past, where Julian is not a cruel lord yet. He is a scarred human slave in a circus cage, whipped as a monster. Adeline means to hand the child back and go, and the girl's broken heart holds her there. Then the caged man asks who she is.",

    # FACTS: Tessa is pushed off a building by her adopted sister Chloe. She wakes up at fifteen, reliving he
    # FACTS: r life. This time, she refuses to fight for her family's love. Chloe manipulates everyone, frami
    # FACTS: ng Tessa for cheating. Tessa calmly proves Chloe's guilt using surveillance footage. Chloe is ex
    # FACTS: pelled. Tessa earns straight A's and a Yale scholarship. Her family apologizes, but she remains 
    # FACTS: distant. She leaves for Yale alone, determined to live for herself.
    'i-watched-them-love-her':
        "Pushed off a building, she woke up at fifteen.\nChloe put her there, and this time Tessa does not spend her life competing for her family's affection. Chloe works everyone as usual and frames her for cheating, and Tessa produces the surveillance footage and lets it speak. Chloe is expelled. Tessa takes straight results and a Yale scholarship, and when the family apologise she stays exactly as distant as she means to, then leaves for Yale on her own.",

    # FACTS: In 1849, the American West, poor dockworker William is betrayed by his lover and his boss, losin
    # FACTS: g everything and becoming a slave laborer in a gold mine. On the brink of death, he awakens a my
    # FACTS: sterious "Golden Eye" that allows him to see through anything and uncover hidden treasures. From
    # FACTS:  a powerless nobody to a legendary mining tycoon, William uses his extraordinary vision and inte
    # FACTS: lligence to defeat the elites who once crushed him!
    'king-of-gold':
        'Betrayed into a gold mine, he woke up seeing through stone.\nIt is 1849 in the American West, and William is a poor dockworker sold out by his lover and his boss until he is working the mines as a slave. Close to death, he awakens the Golden Eye, which lets him see through anything and find what is hidden. From a nobody with nothing, he builds himself into a legendary mining tycoon and goes back for every elite who put him down there.',

    # FACTS: Shivon has spent her life dreaming of escaping her cruel family and earning a place at the Royal
    # FACTS:  Academy. But after one reckless night with the mysterious Duke Alaric Blackmoor, she discovers 
    # FACTS: she’s carrying the one thing everyone believed impossible—his child. Alaric was thought incapabl
    # FACTS: e of producing an heir, because a wolf can only conceive with his fated mate. Now, as Shivon’s f
    # FACTS: amily tries to sell her to the ruthless Lord Greyfang, Alaric will stop at nothing to find the w
    # FACTS: oman who may be his one true mate—and protect the impossible heir growing inside her.
    'knocked-up-by-the-wolf-duke':
        'A wolf can only conceive with his fated mate.\nShivon has spent her life planning her way out of a cruel family and into the Royal Academy, and one reckless night with Duke Alaric Blackmoor leaves her carrying the child everyone was certain he could never have. That fact tells its own story about who she is to him. Her family moves to sell her to the ruthless Lord Greyfang, and Alaric will do anything to find the woman and protect the heir.',

    # FACTS: The tycoon, in order to be with his lover, asked his handsome and strong driver to seduce his wi
    # FACTS: fe, thereby causing her to have an affair, with the aim of having her leave the house with nothi
    # FACTS: ng. In the end, the boss’s plan was exposed, and both he and his lover faced punishment. The dri
    # FACTS: ver also realized the importance of being down-to-earth and returned to the countryside.
    'late-bloomer':
        'He told his driver to seduce his own wife.\nThe tycoon wants his lover and wants his wife gone with nothing, so he sets his handsome, strong driver on her to manufacture an affair. The plan comes out, and he and his lover both pay for it. The driver comes out of it with a clear view of what matters and goes back to the countryside.',

    # FACTS: The story follows Leilani, whose adoptive father has been framed by her ex-boyfriend. Desperate 
    # FACTS: for help, she turns to the one man she trusts the least—Diego Marlowe, a ruthless, undefeated at
    # FACTS: torney who also happens to be her enemy’s future brother-in-law. What begins as a dangerous deal
    # FACTS:  and a fake relationship soon spirals into a high-stakes game of power, secrets, and irresistibl
    # FACTS: e attraction. As they use each other to navigate the battles surrounding them, one question ling
    # FACTS: ers: Is Diego truly just her lawyer—or something far more dangerous to her heart?
    'legally-bound-to-love':
        "Her father is framed. The only help is her enemy.\nLeilani's ex boyfriend has set her adoptive father up, and the one man who can undo it is Diego Marlowe, a ruthless undefeated attorney who happens to be her enemy's future brother in law. He is also the man she trusts least in the world. A dangerous deal and a fake relationship turn into a game of power and secrets neither of them fully controls, and the question that will not go away is whether Diego is only her lawyer.",

    # FACTS: When James loses his daughter Amy and his legs on the same day, he stops believing in magic. Lit
    # FACTS: tle does he know, Amy is now Mia, a fortune-telling prodigy come to save James from his fatal ba
    # FACTS: d karma.
    'little-miss-fortune':
        'He lost his daughter and his legs the same day.\nJames stops believing in anything after that, magic included, which is fair enough. What he does not know is that Amy is back as Mia, a fortune telling prodigy, and she has come for the fatal bad karma that is still coming for her father.',

    # FACTS: My cold, ruthless Mafia godfather guardian tore off his mask the night of my twenty-first birthd
    # FACTS: ay. He doesn't want me to call him uncle anymore. He wants me as his caged bird.
    'locked-by-the-mafia-boss':
        'On her twenty first birthday he stopped being her uncle.\nHer guardian is a cold and ruthless Mafia godfather, and the night she comes of age he takes the mask off. He does not want to hear uncle again. What he wants is her, kept.',

    # FACTS: Five years after breaking up with his college sweetheart Nora, successful ad man Ben unexpectedl
    # FACTS: y reunites with her as his new partner at work. But whenever Ben reveals his true feelings, his 
    # FACTS: consciousness is thrown back five years into his younger self. Determined to fix the mistakes th
    # FACTS: at ended their relationship, Ben begins rewriting the past—only to discover that every change ca
    # FACTS: n reshape the present. To win Nora back, he must finally face the one thing he has always avoide
    # FACTS: d: telling her the truth.
    'love-has-a-deadline':
        'Every time he tells her the truth, he wakes up in the past.\nFive years after the breakup, Ben is a successful ad man who finds Nora assigned as his new partner at work. The moment he says what he actually feels, his consciousness lands back in his younger self. He starts rewriting the mistakes that ended them, and finds that every change he makes reshapes the present in ways he did not intend, until the only move left is the one he has always dodged.',

    # FACTS: Yeonju joins Perfect Match, a survival dating show where several men compete for one woman’s hea
    # FACTS: rt. Moving into the “Match House,” she begins a seven-day experiment in love — a whirlwind of un
    # FACTS: expected chemistry and temptation. From poolside challenges and secret touches to one-night date
    # FACTS: s, each day brings new excitement, new connections… and new betrayals. As emotions blur between 
    # FACTS: sincerity and strategy, passion and hesitation, Yeonju finds herself sinking deeper into a storm
    # FACTS:  of desire and confusion. With every elimination and every choice she makes, her heart grows hea
    # FACTS: vier — until the final day, when her decision will shape one of five completely different ending
    'love-in-my-hands':
        'Seven days, several men, one heart on the line.\nYeonju joins Perfect Match, a survival dating show where a house full of men compete for one woman, and moves into the Match House for a week long experiment in falling for someone. Poolside challenges, secret touches and one night dates keep the chemistry moving, and so do the betrayals. Sincerity and strategy get harder to tell apart with every elimination, and the choice she makes on the final day decides which of five endings she gets.',

    # FACTS: Elena is drugged by her stepfather and, at a masked ball, has a night with Vincent—a powerful he
    # FACTS: ir who can't touch any woman due to childhood trauma. She gives birth to Leo, but Frank sends th
    # FACTS: e baby to an orphanage. Vincent recognizes his tie at the scene, adopts Leo, and brings him home
    # FACTS: . Desperate to reclaim her child, Elena applies as a wet nurse at Cunningham Manor, reuniting wi
    # FACTS: th Vincent—neither recognizes the other. Leo only drinks Elena's milk. Vincent discovers Elena i
    # FACTS: s the only woman he can touch without repulsion, and gradually falls for her. Frank's schemes an
    # FACTS: d Lina's sabotage are repeatedly thwarted by Vincent. Elena learns her child has been "adopted" 
    'mafia-s-desire-for-the-wet-nurse':
        'She took the job to get her baby back.\nDrugged by her stepfather, Elena has a night at a masked ball with Vincent, a powerful heir who cannot bear to touch a woman because of what happened to him as a child. She gives birth to Leo and Frank sends the baby to an orphanage. Vincent recognises his own tie at the scene, adopts the boy and takes him home. Desperate, Elena applies as wet nurse at Cunningham Manor, and neither of them recognises the other. Leo will drink from nobody else, and Vincent discovers she is the only woman he can touch.',

    # FACTS: Catherine, pregnant and controller of FG Group, catches her husband Jesse cheating on video with
    # FACTS:  mistress Mia. She brings his disabled father Walter to the billiard parlor, where Mia shatters 
    # FACTS: Catherine's family crest necklace, smokes illegally, and brutally assaults both the pregnant Cat
    # FACTS: herine and elderly Walter—almost killing the unborn child. When Jesse arrives, he takes Mia's si
    # FACTS: de—until he learns Walter is his biological father and Mia has committed grievous bodily harm. B
    # FACTS: usiness tycoon John Morgan, who had cut ties with Jesse, watches Catherine's abuse live. He arri
    # FACTS: ves, reveals his true identity, and shatters Jesse's business hopes. Jesse and Mia slander Cathe
    'make-my-cheating-husband-pay-the-price':
        "She brought his disabled father to the billiard parlour.\nCatherine is pregnant and runs FG Group, and she has video of her husband Jesse with his mistress Mia. Mia smashes the family crest necklace, smokes where she should not, and beats both the pregnant Catherine and the elderly Walter badly enough to nearly cost the baby. Jesse arrives and takes Mia's side, right up until he learns Walter is his biological father. The tycoon John Morgan, who cut Jesse off long ago, watches the whole thing live and comes to say who he really is.",

    # FACTS: On mating night, Charlie is claimed by the Alpha and his Beta. By morning, she's publicly declar
    # FACTS: ed "unsatisfactory" and replaced. But when she discovers she can hear their private mind-link—an
    # FACTS: d their chosen mate can't—the question becomes: if she was never meant for them, why is she the 
    # FACTS: only one who feels the bond?
    'mated-to-the-alpha-and-his-beta':
        'Declared unsatisfactory by morning, still bonded by night.\nCharlie is claimed by the Alpha and his Beta on mating night, then publicly declared unsatisfactory and replaced before the day is out. What nobody knows is that she can hear their private mind link, and the mate they chose instead cannot. So if Charlie was never meant for them, she is left with one question worth answering. Why is she the only one who feels the bond.',

    # FACTS: Five years ago, Elena Hartwell broke up with her college boyfriend Killian Thorne to protect him
    # FACTS:  from her ruthless uncle Victor—making him believe she was a gold-digger. Heartbroken, Killian r
    # FACTS: eturned to his family's trillion-dollar empire, while Elena was framed by Victor and imprisoned,
    # FACTS:  where she gave birth to their daughter Luna. Now, brave 4-year-old Luna tracks down Killian at 
    # FACTS: his corporate headquarters, shocking everyone by calling him "Daddy." After a DNA test confirms 
    # FACTS: the truth, Killian learns of Elena's wrongful conviction and the sacrifices she made. With his p
    # FACTS: ower and resources, he sets out to free Elena, protect Luna from Victor's schemes, and win back 
    'mommy-s-little-savior':
        "A four year old walked into his headquarters and called him Daddy.\nElena Hartwell ended things with Killian Thorne five years ago to keep her ruthless uncle Victor away from him, letting him believe she was a gold digger. He went back to his family's trillion dollar empire and she was framed by Victor and imprisoned, where she gave birth to Luna. Now Luna has tracked him down herself. A test confirms it, and Killian learns what the conviction really was and what Elena gave up, and starts using everything he has to get her out.",

    # FACTS: Klare is an overlooked nurse at Venus Hospital, struggling with severe anxiety after a family tr
    # FACTS: agedy. Her only comfort is submitting online to a mysterious “Master,” whose commands make her f
    # FACTS: eel safe. But in real life, her new boss, Dance Gordon, is arrogant, sharp-tongued, and always t
    # FACTS: argeting her. By day, they clash at the hospital. By night, he is the perfect Master behind the 
    # FACTS: screen, giving all his patience and tenderness to his one and only — “Cake.” Enemies in real lif
    # FACTS: e. Addicted online.
    'my-boss-is-my-secret-online-dom':
        'The man who torments her at work is the voice she trusts.\nKlare is overlooked at Venus Hospital and living with severe anxiety after a family tragedy, and the only place she feels steady is online, following the commands of someone she has never met. At the hospital her new boss Dance Gordon is arrogant, sharp tongued and always aiming at her. Behind the screen the same man is endlessly patient with the one person he calls Cake, and neither of them knows they are already the closest thing the other has.',

    # FACTS: Wealthy heiress Emily is hunted down by her relatives over her massive inheritance. She flees to
    # FACTS:  her family’s rural farm for shelter, only to accidentally discover that their fireplace connect
    # FACTS: s to a dragon‑ruled otherworld. She keeps sending modern supplies to this realm, aiding Kael, th
    # FACTS: e metal dragon lord, in protecting his people and homeland. To the dragons, she becomes the "Dra
    # FACTS: gon God". From firewood and medicine to modern weaponry, she reshapes the dragon‑race war step b
    # FACTS: y step — and rewrites her own destiny.
    'my-fireplace-ships-to-dragon-realm':
        "The farmhouse fireplace opens onto a dragon war.\nEmily is a wealthy heiress being hunted by relatives who want her inheritance, so she runs to the family's rural farm and finds, by accident, that the fireplace connects to an otherworld ruled by dragons. She starts sending supplies through it to Kael, the metal dragon lord, helping him protect his people. Firewood and medicine turn into modern weaponry, the dragons start calling her the Dragon God, and the shape of their war changes step by step, along with her own future.",

    # FACTS: Once a straight A freshman, Emma Lucas lost everything when Adrian Cole filmed her in bed and le
    # FACTS: t her nudes spread across campus. He said her brother owed his sister a life, then made Emma pay
    # FACTS:  for it. Three years later, Emma strips to keep Ryan alive, only to find Adrian in the VIP booth
    # FACTS: , paying men to humiliate her. “How did you get this cheap?” But when her family shatters and th
    # FACTS: e truth about Lily resurfaces, Adrian’s revenge starts looking like the cruelest mistake of his 
    # FACTS: life.
    'my-first-love-pays-to-watch-me-strip':
        'He filmed her, ruined her, then bought a seat.\nEmma Lucas was a straight A freshman before Adrian Cole spread her nudes across campus, telling her that her brother owed his sister a life and she would be the one paying. Three years later she strips to keep Ryan alive, and finds Adrian in the private booth, paying men to humiliate her and asking how she got this cheap. Then her family comes apart and the truth about Lily surfaces, and his revenge starts to look like the worst decision he ever made.',

    # FACTS: I called 911 because I accidentally handcuffed myself to my bed. I expected a locksmith. Instead
    # FACTS: , my ex-boyfriend kicked down my door—with three firefighters behind him. He thinks another man 
    # FACTS: tied me up and abandoned me. Then I blurt out, "No, I didn't use protection." Now he's furious, 
    # FACTS: jealous, and refusing to believe the truth. My biggest embarrassment just became his biggest mis
    # FACTS: understanding... and neither of us is ready for what comes next.
    'my-hot-firefighter-ex':
        'She called for a locksmith. Her ex kicked the door in.\nShe handcuffed herself to her own bed by accident and rang for help, and what arrives is her ex boyfriend with three firefighters behind him. He takes one look and decides another man tied her up and left her there. Then she blurts out that she did not use protection, which does nothing to help, and now he is furious and jealous and refusing to hear the actual explanation.',

    # FACTS: Gamble King Harold hid his identity, protecting the Daltons and taking care of Grace for three y
    # FACTS: ears as his master Victor Dalton begged him before he passed away. However, his silent protectio
    # FACTS: n was only repaid with contempt and ridicule. Harold endured it all until only three days remain
    # FACTS: ed. But Grace was tricked by her friend, and it seemed that the Dalton family would suffer heavy
    # FACTS:  losses. Harold used his gambling skills to defeat the evil rivals. After that, Harold left. Whe
    # FACTS: n Grace knew Harold's departure, she panicked and searched everywhere for his whereabouts.
    'my-househusband-is-gamble-king':
        'Three years of contempt from the family he protects.\nVictor Dalton begged Harold to look after Grace before he died, so the Gamble King buried his name and did it, quietly, for three years. What he got back was ridicule. He takes it right up until three days are left, and Grace is tricked by a friend into a position that will cost the Daltons dearly. Harold sits down and wins it back with the skill he never told them about, then leaves. Grace works out what she had only once he is gone, and starts looking everywhere.',

    # FACTS: In My Immortal Love movie, after being fired and betrayed on her birthday, Lana’s life takes a s
    # FACTS: upernatural turn when she becomes the first person in 2,000 years to see Augustus—a cursed, invi
    # FACTS: sible Roman immortal. Believing Lana is his destined "miracle," Augustus begs her to help break 
    # FACTS: his eternal curse. There's just one deadly catch: to set him free, she must kill him. As they gr
    # FACTS: ow closer and undeniable sparks fly, Lana is torn between her deepening love and the cruel fate 
    # FACTS: demanding his sacrifice. Can they defeat the ancient gods and break the curse without losing eac
    # FACTS: h other, or is their romance doomed?
    'my-immortal-love':
        'To free him from the curse, she has to kill him.\nFired and betrayed on her birthday, Lana becomes the first person in two thousand years to see Augustus, a cursed and invisible Roman immortal. He is certain she is the miracle he has waited for and begs her to break what holds him, and the method is the problem. As they get closer and the pull between them turns into something neither can talk away, Lana is caught between loving him and the fate that demands she end him.',

    # FACTS: When Naomi accidentally summons Thanatos, the God of Death, a desperate kiss awakens his heart a
    # FACTS: fter ten thousand years. Revealed as his destined Bride of Death, Naomi is the only one who can 
    # FACTS: break his curse, while the immortal reaper discovers that even a god can fall in love.
    'my-marriage-with-the-god-of-death':
        'She summoned Death by accident and kissed him.\nNaomi does not mean to call up Thanatos, and the desperate kiss that follows wakes a heart that has been still for ten thousand years. She turns out to be his destined Bride of Death, the only person who can break what holds him, and the immortal reaper learns that even a god is not safe from falling in love.',

    # FACTS: Serena Hale was a devoted wife. But her husband hadn't touched her in months. So when a stranger
    # FACTS:  pulled her from a bar one night, she surrendered to him - because in her drugged haze, she thou
    # FACTS: ght he was her husband. One mistake. That stranger is Evan Knight - the billionaire underworld k
    # FACTS: ing now funding her husband's company. He knows she's married. He doesn't care. He's been waitin
    # FACTS: g for her for sixteen years - since the rainy night she saved a beaten boy in an alley and didn'
    # FACTS: t even remember his face. But he remembered everything. Her piano. Her voice. The way the rain c
    # FACTS: lung to her white dress. Now he sits across from her at every dinner, watches her husband fake d
    'my-protective-mafia-lover':
        "He has been waiting sixteen years for her to look up.\nSerena Hale was a devoted wife to a husband who had not touched her in months, so when a stranger pulled her from a bar she went with him, believing through the haze that he was her husband. That stranger is Evan Knight, the billionaire underworld king now funding her husband's company. He knows she is married and it changes nothing. Sixteen years ago she saved a beaten boy in an alley and never remembered his face, and he remembered all of it, down to the rain on her white dress.",

    # FACTS: Head over heels for Preston, the Principal's son, Mia has always put him first. But when she fin
    # FACTS: ds out he's been cheating on her with the rich heiress Vivian Walden, Mia hatches a grand escape
    # FACTS:  plan with Preston's opportunistic mother. Will Preston capture her heart back before it leaves 
    # FACTS: permanently for London, or will Sebastian, the mysterious royal boy from London get Mia's love?
    'my-royal-rebound':
        "She put him first for years. He picked the heiress.\nMia has always arranged her life around Preston, the principal's son, so finding out he has been cheating with the rich heiress Vivian Walden takes the ground out from under her. She builds an escape plan with Preston's own opportunistic mother, aimed at London. Preston has until she boards to win her back, and Sebastian, the mysterious royal boy from London, is not making that easier.",

    # FACTS: Caleb Shaw calls BDSM a cure for his dead marriage, then chains his wife Mara to a tree for his 
    # FACTS: mistress. When Mara says the safe word, he leaves with the key. By sunrise, Nina’s hired men fin
    # FACTS: d her. But Caleb never knew what Mara buried for this marriage. She was not just his wife. She w
    # FACTS: as the woman who once owned the West Side docks. Now the collar, the blood, and the betrayal wil
    # FACTS: l drag every Shaw secret into the light.
    'my-safe-word-was-revenge':
        "She said the safe word. He left with the key.\nCaleb Shaw sells the whole arrangement to Mara as a cure for a dead marriage, then chains her to a tree for his mistress and walks off. Nina's hired men find her by sunrise. What Caleb never bothered to learn is what his wife buried to marry him, because before she was anybody's wife she owned the West Side docks. The collar, the blood and the betrayal are about to drag every Shaw secret into daylight.",

    # FACTS: Reese Calder orders a custom companion android, 006, with the face of Nolan Vance, her spoiled, 
    # FACTS: maddening lifelong rival. By day, 006 cooks, cleans, and kneels when she says, "Down." By night,
    # FACTS:  he breaks every command and makes her forget he is supposed to be a machine. Then Kindred Care 
    # FACTS: texts: "Your companion hasn't shipped yet." Nolan calls it a prank. Miles calls it suicide: "If 
    # FACTS: Reese finds the truth, you're done." But Reese finds the truth anyway, and now the liar is still
    # FACTS:  kneeling.
    'my-sex-robot-has-my-enemy-s-face':
        "The android has her rival's face. It is not an android.\nReese Calder orders a custom companion with the face of Nolan Vance, the spoiled lifelong rival who has been maddening her for years. By day 006 cooks and cleans and kneels when she tells him to. By night he breaks every command she gives and makes her forget what he is meant to be. Then the company texts to say her companion has not shipped yet. Nolan calls it a prank, Miles calls it suicide, and Reese finds out anyway, which leaves the liar still on his knees.",

    # FACTS: At my own Mate Claim Ceremony, Cassian rejected me and took my sister Maris’s hand, claiming he 
    # FACTS: only wanted to save her from the Council. Then he tried to rip my dead mother’s moonstone neckla
    # FACTS: ce from my neck so Maris could wear it as his chosen Luna. The chain broke. So did the last reas
    # FACTS: on I had to wait for him. In three days, the Council would send me to Rowan Vale, the Lycan king
    # FACTS: ’s dying heir. Everyone pitied me. But Rowan was the first man to ask if I chose him freely.
    'my-sister-stole-my-mate-so-i-married-a-king':
        "He tore her dead mother's necklace off for her sister.\nCassian rejects her at her own Mate Claim Ceremony and takes Maris by the hand, saying he only means to save her from the Council. Then he reaches for the moonstone necklace so Maris can wear it as his chosen Luna, and the chain breaks, along with the last reason to wait for him. In three days the Council sends her to Rowan Vale, the Lycan king's dying heir, and everyone pities her for it. Rowan is the first man who asks whether she is choosing him freely.",

    # FACTS: Eli got busted watching gay porn, and now the whole campus knows he's into guys. One of them is 
    # FACTS: the guy he likes—but he's not the only one watching. The other roommate claims he hates him, yet
    # FACTS:  he keeps falling deeper, step by step. Now both roommates are going feral over him—one with swe
    # FACTS: et traps, the other with raw possession. Eli's move? He keeps them both in his grip. The rule is
    # FACTS:  simple: he picks no one. Want to stay? Play by his rules.
    'my-two-dangerous-roommates-crave-me':
        'The whole campus knows now. Both roommates were watching.\nEli gets caught, and one of the people who finds out is the boy he likes. The other roommate says he hates him and keeps falling anyway, step by step. Now they are both going feral over him, one laying sweet traps and the other going straight for possession. Eli has decided how this works. He picks nobody, they both stay, and they play by his rules or they do not stay at all.',

    # FACTS: On the day Beatrice catches her husband of eight years cheating, she quietly hands him divorce p
    # FACTS: apers he signs without realizing — starting a thirty-day countdown to freedom. As she dismantles
    # FACTS:  the Belmont family's schemes one by one, she is pulled into the orbit of Damian Crowley, her ex
    # FACTS: -husband's most feared cousin and the mysterious head of the NobleQuest Group. Revenge, a slow-b
    # FACTS: urning romance, and a long-buried secret about a fire and her own origins begin to surface.
    'obsessed-by-my-ex-s-boss':
        "He signed the divorce papers without reading them.\nThe day Beatrice catches her husband of eight years cheating, she hands him the paperwork and he signs, which starts a thirty day countdown he does not know about. As she takes the Belmont family's schemes apart one at a time, she is pulled toward Damian Crowley, her ex husband's most feared cousin and the mysterious head of the NobleQuest Group. Revenge and a slow romance run alongside a long buried secret about a fire and where she actually came from.",

    # FACTS: Xanthea Plath, an illegitimate child of the Alpha of Virgo pack, was an omega and omegas weren't
    # FACTS:  allowed to dream, yet she never stopped dreaming. She wanted to be a doctor just like her mothe
    # FACTS: r but the luna of the pack, her stepmother would break her physically and mentally and stop at n
    # FACTS: othing to crush all her dreams. Xanthea had still found a way though all the abuse her steps put
    # FACTS:  her through. But one day her world came crashing down right before her entrance in a medical co
    # FACTS: llege when she found out that she was being offered as a bride to the ruthless triplet alphas al
    # FACTS: so known as the demon lords of the Infernal pack of the underworld. Xanthea had heard the horrif
    'offered-to-the-triplet-alpha':
        "An omega is not allowed to dream. She dreamed anyway.\nXanthea Plath is the illegitimate daughter of the Virgo pack's Alpha, and her stepmother the luna has spent years breaking her down to make sure she never becomes the doctor her own mother was. She finds a way through it regardless, right up to the doors of medical college. That is when she learns she has been offered as a bride to the ruthless triplet alphas, the demon lords of the Infernal pack, and she already knows how every suitor before her ended.",

    # FACTS: At Waverly University, the ice rink is split in two: on one side, the hockey team trains with br
    # FACTS: utal intensity; on the other, the figure skating team glides through elegant routines. Abby Will
    # FACTS: iams is the golden girl of the ballet-on-ice program — obedient, disciplined, and desperate to l
    # FACTS: and the lead role of the Black Swan in the Winter Showcase. There's just one problem: she has no
    # FACTS:  idea how to be "bad." Enter Tristan Beaumont, the university's most notorious playboy and capta
    # FACTS: in of the hockey team — reckless, magnetic, and hiding a devastating secret behind his bad-boy r
    # FACTS: eputation. When Abby asks him to teach her how to unleash her dark side, neither of them expects
    'offside-with-the-hockey-star':
        "She needs to learn how to be bad. He teaches that.\nThe rink at Waverly University is split down the middle, hockey brutality on one side and figure skating elegance on the other. Abby Williams is the golden girl of the ballet on ice programme, obedient and disciplined and desperate for the Black Swan lead in the Winter Showcase, with one problem she cannot train her way out of. Tristan Beaumont is the captain of the hockey team, the university's most notorious playboy, and hiding something behind it. Standing between them is his younger brother Taylor, her skating partner and best friend.",

    # FACTS: After surviving a month of kidnapping and torture, Claire returns home with severe PTSD, only to
    # FACTS:  be misunderstood and humiliated by her brother Maxwell and her family. As her trauma becomes im
    # FACTS: possible to ignore, Maxwell begins to doubt his judgment — but when Claire gives up on ten years
    # FACTS:  of love and walks away, he finally realizes the truth was never what he believed.
    'once-love-is-lost-it-never-returns':
        'A month of captivity, and her family called it acting.\nClaire comes home from a month of captivity carrying trauma she cannot hide, and her brother Maxwell leads the humiliation, certain she is exaggerating. The trauma gets harder to explain away by the week, and Maxwell starts to doubt his own judgement. He works it out far too late. Claire gives up on ten years of loving these people and walks, and only then does he understand that the truth was never what he decided it was.',

    # FACTS: Forced to spy on heir Lucien to pay her father’s debts, Elara finds herself trapped in a web of 
    # FACTS: betrayal, lost love, and tragic loss. After the truth of her noble lineage surfaces, she must fa
    # FACTS: ce a vindictive rival and a complicated past. Amidst power struggles and life-threatening danger
    # FACTS: , can Lucien’s ultimate sacrifice heal their broken bond?
    'our-love-built-on-lies':
        "She was sent to spy on him to clear her father's debts.\nElara has no choice about it, and getting close to the heir Lucien pulls her into betrayal, love she did not plan for and loss she cannot undo. Then the truth about her own noble lineage comes out and she has a vindictive rival and a complicated past to answer for at once. With power struggles closing in and real danger on the table, what Lucien is willing to give up may be the only thing that mends this.",

    # FACTS: I dated Lucien secretly for three years, but he denied me at graduation after a heartbeat test p
    # FACTS: aired him with his rival Seraphina. He even stole my umbrella and altered my overseas academy ad
    # FACTS: mission. I cut all contact and flew to Arcadia to rebuild myself. Years later, he traveled thous
    # FACTS: ands of miles to beg for a second chance. Yet I met Nathan, a sincere mage who treats me as an e
    # FACTS: qual. Will I ever forgive the boy who broke me completely?
    'outgrowing-my-old-magic-love':
        'Three secret years, denied at graduation.\nA heartbeat test pairs Lucien with his rival Seraphina, and he drops her in front of everyone. He also takes her umbrella and quietly alters her overseas academy admission. She cuts contact and flies to Arcadia to rebuild from nothing. Years later he travels thousands of miles to beg for a second chance, and by then she has met Nathan, a sincere mage who treats her as an equal.',

    # FACTS: For five years of marriage, I gave up my career and left everything behind to follow my brigadie
    # FACTS: r general husband—only to end up living as an illegal resident on the base. He gave my military 
    # FACTS: dependent slot to the girl we sponsored, and even had the lock on our home changed for her. Hear
    # FACTS: tbroken, I left in the dead of night and started over in a new city. Seven years later, at a mil
    # FACTS: itary arts festival, we crossed paths again. He was full of regret, but I was already standing n
    # FACTS: ext to another man. This time, I didn't look back.
    'paper-marriage':
        'Five years following him, and she was living there illegally.\nShe gave up her career to go where her brigadier general husband went, and ended up on the base with no standing at all. He handed her military dependent slot to the girl they sponsored, then changed the lock on their home for her. She left in the middle of the night and started again in a new city. Seven years later they cross paths at a military arts festival, and he is full of regret, and she is already standing beside someone else.',

    # FACTS: Senior year was supposed to be the best year ever. Then two pink lines changed everything. Now K
    # FACTS: elsey has to tell the campus heartthrob he's going to be a dad — and hide it all from the Dean w
    # FACTS: ho also happens to be her grandmother.
    'positively-pregnant':
        'Two pink lines, and the Dean is her grandmother.\nSenior year was supposed to be the best one, and now Kelsey has to tell the campus heartthrob he is going to be a father. Keeping it from everyone would be hard enough without the woman running the place being family.',

    # FACTS: Sloane was a fake mate assigned to heir Royce. For three years, he never marked her, spiked her 
    # FACTS: drinks with suppressants, and humiliated her in public. His brother Kael, whose Thorne blood Slo
    # FACTS: ane recognized at a ceremony, returned and proposed a deal: “Three months, he never pleased you 
    # FACTS: once. I need one night.” One true bite shattered the fake bond. Sloane carried Kael's pup. Royce
    # FACTS:  killed Magnus for the seat, kidnapped seven-months-pregnant Sloane, and confessed to everything
    # FACTS: —recorded live by the ring she wore. Royce was caged for life. Kael knelt before the pack and as
    # FACTS: ked Sloane to be his Luna.
    'pregnant-by-his-alpha-brother':
        "Three years a fake mate, drugged and never marked.\nSloane was assigned to the heir Royce, who spiked her drinks with suppressants, never marked her and humiliated her in public whenever it suited him. His brother Kael comes back, the one whose Thorne blood she recognised at a ceremony, with an offer of one night. One true bite breaks the fake bond. She carries Kael's pup, and Royce kills Magnus for the seat and takes her at seven months pregnant, confessing the lot of it to a ring that is recording live.",

    # FACTS: Laila, a destitute widow, is forced off a cliff by the tyrannical Governor Barrow—only to fall i
    # FACTS: nto the sacred dragon realm. There, she spends one fateful night with King Kael, a dragon sovere
    # FACTS: ign bound by a deadly curse that burns any woman he touches. Ten months later, she gives birth t
    # FACTS: o a royal dragon egg. Hunted by Barrow, she desperately entrusts the egg to the dragon clan. Whe
    # FACTS: n the temple issues a decree seeking one who can hatch the egg, Laila tears down the royal notic
    # FACTS: e and steps forward. Despite scorn and humiliation from the nobles, she reunites with Kael. In t
    # FACTS: he end, it is her unconditional mother's love that awakens the dying egg—and a penniless commone
    'pregnant-with-the-dragon-lord-s-last-heir':
        "Pushed off a cliff, she landed in the dragon realm.\nLaila is a destitute widow when the tyrannical Governor Barrow forces her over the edge, and the fall drops her somewhere nobody expected. She spends one night with King Kael, a dragon sovereign under a curse that burns any woman he touches. Ten months later she gives birth to a royal dragon egg, and with Barrow hunting her she hands it to the dragon clan. When the temple asks for someone who can hatch it, Laila tears the notice off the wall and steps up, and the nobles laugh until a mother's love wakes the dying egg.",

    # FACTS: After years of being dismissed by her husband, Eric, as uptight, boring, and hopelessly inexperi
    # FACTS: enced, Chloe finally decides she’s had enough. Desperate to save her dying marriage—and prove sh
    # FACTS: e can be the woman he wants—she ventures into an exclusive underground club for a private lesson
    # FACTS:  in pleasure. But Chloe walks into the wrong room. What she mistakes for an elite adults-only tr
    # FACTS: aining session is actually a secret gathering where vampires select their human blood thralls. A
    # FACTS: nd the man she approaches for guidance is no ordinary instructor. Victor is a ruthless billionai
    # FACTS: re, a predator hiding at the very top of human society—and a powerful vampire Dom accustomed to 
    'private-lessons-with-my-vampire-boss':
        'She walked into the wrong room at the club.\nAfter years of Eric calling her uptight and boring and hopelessly inexperienced, Chloe decides to fix it and books a private lesson at an exclusive underground club, hoping to save the marriage. What she has actually walked into is a secret gathering where vampires choose their human blood thralls, and the man she asks for guidance is no instructor. Victor is a ruthless billionaire, a predator at the very top of human society, and used to complete obedience.',

    # FACTS: Olivia, an art student harboring a secret crush on a star hockey player, accidentally stumbles u
    # FACTS: pon the shocking truth: Liam, the campus playboy, is secretly an anonymous adult content creator
    # FACTS: . To keep his secret safe, the two enter into a dangerous "fake dating" pact. As they navigate e
    # FACTS: ndless teasing, power struggles, and joint battles against campus bullying and malicious schemes
    # FACTS: , their pretend romance begins to blur into real passion. However, just as they finally face the
    # FACTS: ir true feelings for each other, a deadly blackmail scheme threatens to destroy everything Liam 
    # FACTS: holds dear...
    'puck-perfect-my-sex-education-tutor':
        "She found out what the campus playboy does after dark.\nOlivia is an art student with a quiet crush on a star hockey player when she stumbles onto Liam's secret, which is that he anonymously makes adult content. Keeping it quiet costs her a fake dating pact with him. Between the teasing, the power struggles and the campus bullies they end up fighting together, the pretending starts running out of road. Then a blackmail scheme arrives aimed at everything Liam cannot afford to lose.",

    # FACTS: Briar gave everything to her elite dragon flight and her fiancé, Silas. Her reward? Betrayal. Th
    # FACTS: ey mocked her unawakened dragon as a useless runt, stripped her of her rank, and left her to die
    # FACTS: . But death didn't take. Reborn back to a few days ago, Briar turns her back on her toxic ex. Wh
    # FACTS: ile they laugh at her "weak" dragon, Briar is ready to unleash a mythical power unseen for centu
    # FACTS: ries. When the skies clash, Silas will realize too late: they didn't just discard a useless team
    # FACTS: mate—they threw away the goddess of victory.
    'reborn-to-rule-the-sky-with-my-dragon':
        'They mocked her dragon as a runt and left her to die.\nBriar gave her elite dragon flight everything, and her fiance Silas most of all, and was repaid with betrayal, stripped rank and a slow death. Death does not take. She wakes a few days earlier and turns her back on the lot of them. They are still laughing at her unawakened dragon, which is convenient, because Briar is about to unleash a mythical power nobody has seen in centuries. When the skies clash, Silas will realise they did not throw away a useless teammate. They threw away the goddess of victory.',

    # FACTS: Ruby only meant to take a temporary nanny job for quick money, but she accidentally walks into t
    # FACTS: he frozen world of billionaire Ethan Cole and his impossible twins. The children have already dr
    # FACTS: iven away sixteen nannies, Ethan runs his home like a boardroom, and every corner of the estate 
    # FACTS: is ruled by cold order instead of warmth. What begins as a one-week trial quickly turns into som
    # FACTS: ething much larger. As Ruby challenges the household’s rigid rules, the twins slowly begin to tr
    # FACTS: ust again, Ethan is forced to confront the way he confuses control with parenting, and an extern
    # FACTS: al power struggle over custody, inheritance, and corporate leadership starts closing in. Caught 
    'rent-a-mom-for-the-billionaire-twins':
        'Sixteen nannies have already walked out of that house.\nRuby takes a temporary job for quick money and lands in the frozen world of billionaire Ethan Cole and his impossible twins. He runs his home like a boardroom and the whole estate operates on cold order. A one week trial turns into something much bigger as she starts breaking the rules of the place, the twins begin to trust again, and Ethan has to look at how long he has confused control with parenting. Meanwhile a fight over custody, inheritance and the company is closing in around all of them.',

    # FACTS: In a small village divided by strict rules, a young man from the lower village fell in love with
    # FACTS:  his childhood friend from the upper village. Unfortunately, their romance was discovered, leadi
    # FACTS: ng to a ...
    'return-to-reckon-with-his-hateful-village':
        'The village split them once. He came back for it.\nThe rules of this village keep the lower half and the upper half apart, and a young man from the lower village falls for his childhood friend from the upper one anyway. They are found out, and what follows is the reason he leaves. The reckoning is what brings him home.',

    # FACTS: Wendy, a naturally gifted ballet prodigy, had her identity maliciously swapped at birth by Helen
    # FACTS: a, a former dancer consumed by jealousy. For eighteen years, she endured abuse and suppression, 
    # FACTS: yet quietly clung to her dream of dancing. To cover her grandfather’s medicalsurgery expenses, s
    # FACTS: he took a job at a theatre and signed up for a competition. However, Angela, the impostor heires
    # FACTS: s, repeatedly framed her. Worse still, her birth mother Sophia wrongfully accused her of plagiar
    # FACTS: ism, getting her blacklisted across the industry.In her darkest hour, Alexander, a corporate CEO
    # FACTS: , recognized her talent and resilience. He funded her grandfather’s surgery and supported her as
    'revenge-of-the-black-swan':
        "Swapped at birth by a jealous dancer.\nHelena could not stand what Wendy was going to be, so she switched them, and eighteen years of abuse and suppression follow without ever quite killing the dream. To pay for her grandfather's surgery Wendy takes a job at a theatre and enters a competition, where Angela, the impostor heiress, frames her again and again. Then her birth mother Sophia accuses her of plagiarism and gets her blacklisted across the industry. Alexander sees what she is at the worst possible moment, pays for the surgery and backs her into the International Dance Invitational.",

    # FACTS: Leo has always been one rank behind Jaxon, the star quarterback who takes everything Leo wants, 
    # FACTS: including his crush, the hottest girl on campus. What Leo doesn't know is that Jaxon is secretly
    # FACTS:  in love with him. So Jaxon tanks an exam on purpose, then makes Leo an offer — Tutor me to keep
    # FACTS:  my captaincy, and I'll teach you how to win your dream girl. Studying calculus by day, dating l
    # FACTS: essons by night — and one plan Leo never accounted for, falling for his romance coach, his bigge
    # FACTS: st rival.
    'romance-lessons-with-my-quarterback':
        'He tanked an exam to get the tutoring.\nLeo has spent his life one rank behind Jaxon, the star quarterback who takes everything he wants, including his crush. What Leo has not worked out is that Jaxon is in love with him. So Jaxon fails on purpose and makes an offer, which is tutoring to keep his captaincy in exchange for lessons in winning the girl. Calculus by day and dating drills by night, and one outcome Leo never allowed for, which is falling for his romance coach.',

    # FACTS: Based on the novel by Sierra Simone. Ex-soldier Tristan becomes bodyguard to his uncle-in-law, a
    # FACTS:  magnetic billionaire who runs an exclusive sex club. Despite his best efforts to stay professio
    # FACTS: nal, Tristan's drawn to his boss’s dominance, breaking down his defenses until he finally submit
    # FACTS: s. Under Mark’s seduction, Tristan is pulled into a world of pain and pleasure he never imagined
    # FACTS: . But his lust for Mark unravels when he’s sent to retrieve Mark’s fiancée… and falls for her to
    # FACTS: o.
    'salt-kiss':
        "He is guarding the man he cannot stop wanting.\nEx soldier Tristan takes work as bodyguard to his uncle in law, a magnetic billionaire running an exclusive club, and does his best to keep it professional. Mark's dominance wears him down until he submits, and what follows is a world of pain and pleasure he had not imagined for himself. Then he is sent to collect Mark's fiancee, and falls for her too.",

    # FACTS: Samantha Hughes waited a whole year for AURA’s final farewell concert, only to find her childhoo
    # FACTS: d sweetheart Logan kissing Sierra outside the venue after giving away Sam’s VIP ticket. When Log
    # FACTS: an keeps choosing Sierra, exposes Sam’s family trauma, and later abandons her during a fire, Sam
    # FACTS:  finally sees the boy she loved is gone. She withdraws from Berkeley, moves to New York, rebuild
    # FACTS: s her life with her mother, and refuses every attempt Logan makes to drag her back. Even when Si
    # FACTS: erra tries to ruin her reputation and Logan begs for another chance, Sam chooses peace, dignity,
    # FACTS:  and a new love who actually stays.
    'scorched-heart':
        "He gave away her ticket and kissed someone else outside.\nSamantha Hughes waited a year for the band's farewell concert, and Logan hands her seat to Sierra and does not think twice. He keeps choosing Sierra, drags out Sam's family trauma in public, and then leaves her behind during a fire. That is where the boy she loved stops existing. She withdraws from Berkeley, moves to New York, rebuilds with her mother and turns down every attempt to pull her back, including the begging.",

    # FACTS: Six years ago, heiress Milo left penniless Asher to save her failing family, keeping her pregnan
    # FACTS: cy a secret. Now a ruthless tech billionaire still bitter about the past, Asher reunites with Mi
    # FACTS: lo at a gala — she’s now a desperate single mom, scrambling to pay for their son Leo’s life-savi
    # FACTS: ng heart surgery. As the truth of her sacrifice unfolds, a guilt-stricken Asher sets out to win 
    # FACTS: her back, secures top care for their son, brings the real culprit to justice, and earns his seco
    # FACTS: nd chance at love...
    'second-chance-the-tech-billionaire-s-secret-family':
        "She left him penniless and kept the pregnancy quiet.\nSix years ago Milo walked away from Asher to save her failing family, and never told him why or about the baby. Now he is a ruthless tech billionaire still bitter about it, and they meet again at a gala where she is a single mother scrambling to pay for their son Leo's heart surgery. As what she actually did comes out, Asher sets about getting the boy proper care, putting the real culprit in front of a court, and earning the second chance.",

    # FACTS: On the continent of Vester, Iso—Supreme Ruler of the Hidden Dragon Dominion—goes into hiding und
    # FACTS: er a humble identity to investigate his mother Saintess Esara's murder. Disguised as an ordinary
    # FACTS:  man, he takes residence in Silvermoon Castle and, honoring an old betrothal, becomes the fiancé
    # FACTS:  of Sera, heiress to the saintess lineage. Sera, however, is obsessed with the legendary Dragon 
    # FACTS: Lord—a mythical figure she has worshipped from afar—and feels only disappointment toward her unr
    # FACTS: emarkable-looking betrothed. She frequently mocks and belittles him, unaware of his true identit
    # FACTS: y. Cardinal Taren of the Orthodox Church, coveting the saintess's power, secretly hires eight re
    'secret-dragon':
        'She worships the Dragon Lord and mocks her own fiance.\nIso rules the Hidden Dragon Dominion and goes into hiding as an ordinary man to find out who murdered his mother, the Saintess Esara. Living in Silvermoon Castle, he honours an old betrothal and becomes engaged to Sera, heiress to the saintess line, who has spent years adoring a mythical figure from a distance and finds her unremarkable betrothed a disappointment. She belittles him regularly. Meanwhile Cardinal Taren wants the saintess power and has quietly hired eight renowned Dragon Slayers.',

    # FACTS: Six years ago, college student Isabel was framed, leading to an unexpected encounter with billio
    # FACTS: naire heir Ethan, after which she became pregnant and dropped out of school. Six years later, Is
    # FACTS: abel works tirelessly to raise her child, who suffers from severe allergies. By a twist of fate,
    # FACTS:  she joins Ethan's company and becomes his personal assistant. Faced with relentless bullying an
    # FACTS: d even life-threatening schemes against her child by the vicious heiress Rachel, Isabel refuses 
    # FACTS: to back down and bravely fights back. As they spend time together day and night, Ethan not only 
    # FACTS: repeatedly steps in to save her but also falls deeply in love with her. As the plot unfolds, the
    'secretly-pregnant-with-the-billionaire-s-daughter':
        "Six years raising his child, and now she is his assistant.\nIsabel was framed as a college student, and the encounter with billionaire heir Ethan that followed left her pregnant and out of school. Six years on she works herself into the ground for a daughter with severe allergies, and a twist of luck puts her in Ethan's company as his personal assistant. The vicious heiress Rachel bullies her and then starts going after the child, and Isabel refuses to fold. Ethan keeps stepping in, keeps falling for her, and the girl's real bloodline is about to reach his great grandmother.",

    # FACTS: Isabella gave up her secret life as the leader of the legendary Shadow Circle to be with her bel
    # FACTS: oved mate, whom she works hard as an herbalist to support. But when he's promoted to Alpha's Gen
    # FACTS: eral, instead of thanking her, he breaks their mate bond and replaces her with a scheming Comman
    # FACTS: der's Daughter. He's not expecting the Alpha himself to show up and reveal Isabella is the lost 
    # FACTS: wolf princess — destined to be Alpha Queen — and he'll regret letting her go.
    'she-bows-for-no-one':
        "She gave up the Shadow Circle for a man who dropped her.\nIsabella walked away from leading a legendary order to be with her mate, and worked as a herbalist to keep them both. The day he makes Alpha's General he breaks their mate bond and replaces her with a scheming Commander's daughter. What he does not plan for is the Alpha turning up in person to say out loud what Isabella is, which is the lost wolf princess and the next Alpha Queen.",

    # FACTS: At their mate-selection ceremony, Grant rejects Mara in front of both tribes and gives her place
    # FACTS:  to her crying younger sister. He swears it is only temporary. He has forgotten one thing: Mara 
    # FACTS: turns twenty-two in three days. Under tribal law, an unmated woman loses her right to choose, an
    # FACTS: d Mara has already been assigned to the dying Dragon King. Grant expects her father to stop it. 
    # FACTS: Mara accepts the decree. Three days later, as Grant comes to bond with Brenna, one hundred drago
    # FACTS: n guards arrive at the Hale gates to escort Mara away as their future queen.
    'sister-stole-my-mate-i-got-the-dragon-king':
        'He gave her place to her sister and forgot the calendar.\nGrant rejects Mara in front of both tribes at the mate selection ceremony, hands her position to her crying younger sister and promises it is only temporary. What he has not counted is the three days until Mara turns twenty two, after which tribal law takes her right to choose and she goes where she is assigned, which is to the dying Dragon King. Grant assumes her father will stop it. Mara accepts. Three days later, as he arrives to bond with Brenna, a hundred dragon guards reach the Hale gates for their future queen.',

    # FACTS: In Slimming Revolution Movie, Declan, the Harrison family's heir, marries Claire, the daughter o
    # FACTS: f a wealthy tycoon, due to a family arrangement. However, on their wedding day, Declan is shocke
    # FACTS: d to see that Claire, whom he's meeting for the first time, is a plus-size woman, nearly 300 pou
    # FACTS: nds. The wedding guests quickly turn Declan into the laughingstock of the event. Reluctantly, De
    # FACTS: clan starts married life with this stranger, and Claire's intense love for him only adds to his 
    # FACTS: stress. When Claire's efforts to protect their love inadvertently anger Declan, he, obsessed wit
    # FACTS: h appearances, cruelly takes out his frustrations on her, even criticizing her weight. Feeling d
    'slimming-revolution':
        "He married her sight unseen and made her the joke.\nDeclan is the Harrison heir, married off to Claire, a tycoon's daughter he meets for the first time at their own wedding. She is nearly three hundred pounds, and the guests turn him into the laughingstock of the day. He never forgives her for it. Claire loves him hard anyway, and every time she tries to protect what they have he punishes her for it, down to her weight. So she stops trying to be loved by him and starts a transformation aimed squarely at making him regret every word.",

    # FACTS: After being mistreated by his wife’s family for years, Leo discovers that he is the heir to a va
    # FACTS: st fortune. Now it’s time — for revenge!
    'son-in-law-s-revenge':
        "Years of being the family's punching bag, then the will.\nLeo has taken everything his wife's family has thrown at him for years without much choice about it. Then he finds out he is the heir to a vast fortune, and the arrangement changes rather quickly.",

    # FACTS: To the world, Nate Ryder is a failure whose Awakening ended in disgrace. But Nate knows the trut
    # FACTS: h: he awakened the SSS-rank Thunder God—the rarest power on Earth. His father sold his health fo
    # FACTS: r a vial of Awakening serum. His mother has been paralyzed for ten years, yet she's the reason h
    # FACTS: e never gives up. At school, the elite bully Tyler—an A-rank prodigy—crushes that serum and work
    # FACTS: s with corrupt administrators to bar Nate from the national tournament. Facing relentless humili
    # FACTS: ation, Nate hides his power and bides his time. Every insult, every injustice becomes fuel for h
    # FACTS: is training. Then the Federal Awakened Selection Tournament begins. Tyler, determined to defeat 
    'sss-rank-the-slum-born-thunder-god':
        'The world calls his Awakening a disgrace. He knows better.\nNate Ryder awakened the Thunder God, the rarest power on Earth, and told nobody. His father sold his health for the vial of serum that made it possible, and his mother has been paralysed for ten years and is the reason he keeps going. At school the elite bully Tyler crushes that serum and works with corrupt administrators to keep Nate out of the national tournament. So Nate hides what he is and turns every insult into training, and waits for the Federal Awakened Selection Tournament and the one fight Tyler is certain he cannot lose.',

    # FACTS: Straight-A bookworm Georgia Pruitt accidentally shoves rockstar Riot Cross off his stage, so her
    # FACTS:  strict father ships her to Silver Pines reform camp, where Riot's label sends him too. Bound as
    # FACTS:  accountability buddies, the enemies fall in love through bullying storms, lakeside rescues, a s
    # FACTS: tolen kiss, and a rewritten love song. When leaked photos force a breakup, Riot leaps from his d
    # FACTS: eparting car to sing with her onstage, and they choose each other and music school over Harvard 
    # FACTS: and the tour.
    'summer-with-a-superstar':
        "She shoved a rockstar off his own stage.\nGeorgia Pruitt is a straight A bookworm right up until she knocks Riot Cross into the crowd, and her strict father ships her off to Silver Pines reform camp. Riot's label sends him to the same place. Bound together as accountability buddies, they get through bullying, a lakeside rescue, a stolen kiss and a rewritten love song, and fall for each other doing it. When leaked photos force them apart, Riot jumps out of a departing car to sing with her, and they pick each other and music school over Harvard and the tour.",

    # FACTS: Ryder and Enzo, F1 rivals for fourteen years, one from the slums, one a billionaire heir. Enzo w
    # FACTS: hispers "I love you" during CPR; Ryder wakes convinced it was sabotage. Handcuffs, saunas, and b
    # FACTS: lindfold drills force them close as Ryder battles desire. Enzo risks his life against a violent 
    # FACTS: rival and quietly pays Ryder's mother's surgery. They confess at the track where it began. In th
    # FACTS: e final race, Enzo pushes Ryder to victory with his own car and crashes. In the wreckage, Ryder 
    # FACTS: says "I love you."
    't-boning-my-f1-rival':
        "He said it during CPR. Ryder decided it was sabotage.\nFourteen years of rivalry sit between them, Ryder out of the slums and Enzo a billionaire heir. Enzo whispers that he loves him while bringing him back, and Ryder wakes convinced it was a tactic. Handcuffs, saunas and blindfold drills keep forcing them together while Ryder fights what he feels. Enzo risks his life against a violent rival and quietly pays for Ryder's mother's surgery without telling him. They say it at the track where it started, and in the final race Enzo pushes Ryder to the win and crashes doing it.",

    # FACTS: Olivia has secretly loved her stepbrother Jacob for years — but ever since their parents' weddin
    # FACTS: g, he's treated her like a stranger. He races motorcycles and lives on the edge; she's the golde
    # FACTS: n girl who never breaks a rule. When one reckless night forces them together, buried feelings st
    # FACTS: art clawing their way to the surface. Some lines were never meant to be crossed.
    'tempted-by-my-bad-boy-stepbrother':
        'Since their parents married he treats her like a stranger.\nOlivia has quietly loved Jacob for years, and the wedding that made them family is the moment he stopped looking at her. He races motorcycles and lives close to the edge. She is the golden girl who has never broken a rule in her life. Then one reckless night puts them in the same room with nowhere to hide, and what they have both been burying starts clawing its way up.',

    # FACTS: After his mother’s death, billionaire heir Vincent became reckless, cold, and impossible to cont
    # FACTS: rol. But everything snaps when his father Arthur brings home a mysterious woman who looks exactl
    # FACTS: y like Vincent’s late mother — and even gives her his mother’s priceless jewels. Convinced Evely
    # FACTS: n is a manipulative gold digger, Vincent sets out to expose her. But inside an abandoned greenho
    # FACTS: use wrapped in vines, he uncovers her darkest secret… and a dangerous attraction neither of them
    # FACTS:  can resist.
    'tempted-by-my-step-son':
        "His father brought home a woman with his mother's face.\nVincent has been reckless and cold and impossible to handle since his mother died, and Arthur walking in with Evelyn, who looks exactly like her, is more than he can take. Then his father gives her his mother's priceless jewels. Certain she is a manipulative gold digger, Vincent sets out to expose her, and what he finds in an abandoned greenhouse wrapped in vines is her darkest secret and an attraction neither of them can talk their way out of.",

    # FACTS: I’ve been dreading my eighteenth birthday for as long as I can remember. My mating day was even 
    # FACTS: worse than I could have imagined. Not only was I mated to the Alpha and the Beta, they don’t wan
    # FACTS: t me. Publicly cast aside for another woman, I fled into the wilderness, entirely unaware that I
    # FACTS:  was actually a forbidden wolf-vampire hybrid. To protect me from a corrupt Council, my family w
    # FACTS: iped my memories, leaving me stranded in a rogue town as "Katie"—heavily pregnant and completely
    # FACTS:  lost. But my past violently caught up when my mates and their secret Alpha brother, Mason, trac
    # FACTS: ked me down. With a dark conspiracy now targeting my newborn daughter to breed a lethal hybrid a
    'the-alpha-and-beta-s-shared-mate':
        'Mated to the Alpha and the Beta. Neither wants her.\nShe dreaded her eighteenth birthday for years and the day itself is worse than anything she imagined, cast aside in public for another woman. She runs into the wilderness with no idea she is a forbidden wolf vampire hybrid. To keep her from a corrupt Council her family wipes her memory, leaving her stranded in a rogue town as Katie, heavily pregnant and completely lost. Then her mates and their secret Alpha brother Mason track her down, and a conspiracy aimed at her newborn daughter starts closing in.',

    # FACTS: Five years ago, Tiffany was betrayed by her fiancé and best friend, poisoned, and left for dead 
    # FACTS: while pregnant. She survived, but her newborn daughter vanished without a trace. Desperate to fi
    # FACTS: nd her, Tiffany takes a job as a nanny at the Silvermoon Pack, never realizing the little prince
    # FACTS: ss in her care is her own missing daughter. The girl's father is Asher Sterling—the ruthless, un
    # FACTS: touchable Alpha who has spent five years searching for the mysterious woman from his one unforge
    # FACTS: ttable night. As Tiffany and Asher are drawn together, old enemies resurface, deadly secrets unr
    # FACTS: avel...
    'the-alpha-and-his-nanny-luna':
        "She is the nanny. The little princess is hers.\nFive years ago Tiffany was betrayed by her fiance and her best friend, poisoned and left for dead while pregnant. She lived. Her newborn daughter vanished. Desperate to find her, she takes a nanny job at the Silvermoon Pack without ever realising the child in her care is the one she lost. The girl's father is Asher Sterling, the ruthless and untouchable Alpha who has spent five years hunting for the woman from one unforgettable night. Old enemies surface as they are pulled together, and the secrets start coming undone.",

    # FACTS: “It’s just a formality.” Reynolds threw those words in Eliot’s face on their wedding day, leavin
    # FACTS: g him behind to greet his comrade. Four years of lies, another Alpha’s scent on Reynolds’ skin.E
    # FACTS: liot didn’t cry. He ripped off his ring, threw it at Reynolds’ feet, and walked into the hall ac
    # FACTS: ross.Vaughn had been waiting there for four years. White roses. Starlight lamps. A ring he’d kep
    # FACTS: t since they were kids. He spent four years climbing four ranks just to rewrite the law that loc
    # FACTS: ked Omegas out of the mech bay. He never told Eliot. He just pried the door open and waited.
    'the-alpha-commander-s-long-awaited-omega':
        "It is just a formality, he said, on their wedding day.\nReynolds says it to Eliot and leaves to greet his comrade, four years of lies and another Alpha's scent still on him. Eliot does not cry. He pulls the ring off, drops it at his feet and walks into the hall across the way. Vaughn has been waiting in there for four years with white roses, starlight lamps and a ring he has kept since they were children. He climbed four ranks in that time purely to rewrite the law shutting Omegas out of the mech bay, and never said a word about it.",

    # FACTS: "I'd rather you had let me bleed out." Those were my Alpha's last words after I spent a lifetime
    # FACTS:  loving the man whose life I saved. Reborn, I ask for only one thing—freedom. Instead, he forces
    # FACTS:  me to mate his younger brother. What he doesn't know is that his brother has spent three years 
    # FACTS: searching for the mysterious girl who once saved him... and she's me. When the truth finally com
    # FACTS: es out, which brother will regret losing me first?
    'the-alpha-heir-gave-me-to-his-brother':
        "I would rather you had let me bleed out.\nThose are her Alpha's last words to her, after a lifetime spent loving the man whose life she saved. Reborn, she asks for one thing, which is freedom, and he forces her to mate his younger brother instead. What he does not know is that the brother has spent three years looking for the mysterious girl who once saved him, and she is standing right there. When it finally comes out, one of them regrets it first.",

    # FACTS: Annie, a human, fell in love with Fenrir, the wolf king, and bore twin half-blood children. Yet 
    # FACTS: they were brutally exiled due to blood prejudice and Mara’s malicious schemes. Five years later,
    # FACTS:  the twins’ werewolf blood awakens unexpectedly, dragging the whole family back into power strug
    # FACTS: gles and deadly hunts. Following the clues, Fenrir uncovers the truth of the past. While protect
    # FACTS: ing his wife and daughters, he exacts revenge on the real mastermind behind all the crimes.
    'the-alpha-king-s-half-blood-twins':
        "Exiled for the blood in her children's veins.\nAnnie is human, and loving Fenrir the wolf king and bearing his twin half blood daughters gets all of them driven out, on prejudice and on Mara's scheming. Five years later the twins' werewolf blood wakes up without warning and drags the whole family back into power struggles and hunts. Following it back, Fenrir finds out what really happened, and while he keeps his wife and daughters standing he goes after the one who arranged all of it.",

    # FACTS: Sold to a drug lord by her foster father, Aurora leaps from a tower and is reborn. She exposes t
    # FACTS: he Harrisons' abuse, then her sealed wolf awakens, revealing her as Alpha King Vincent's long-lo
    # FACTS: st daughter. Vincent brings Aurora home to a noble academy where she crushes every challenger. T
    # FACTS: hree adopted brothers discover they are all her destined mates. At her coronation, Aurora expose
    # FACTS: s the Harrisons' crimes and Vincent banishes them. All three brothers declare love, leaving her 
    # FACTS: choice open.
    'the-alpha-king-s-true-heiress':
        "Sold to a drug lord, she jumped. Then she woke up.\nAurora's foster father sells her, so she leaps from a tower and is reborn with everything she needs. She exposes the Harrisons for what they did to her, and then her sealed wolf wakes and names her the long lost daughter of Alpha King Vincent. He takes her home to a noble academy where she goes through every challenger put in front of her. Three adopted brothers each discover they are her destined mate. At her coronation the Harrisons' crimes come out and Vincent banishes them, and all three brothers declare themselves.",

    # FACTS: Sold at auction and cast aside by the Alpha who bought her, Omega Elena is handed off to his van
    # FACTS: ished uncle—the Lycan King and War God, Finn—only to discover that her five children were his al
    # FACTS: l along, and that the man she thought had betrayed her has loved and protected her from the very
    # FACTS:  start.
    'the-alpha-king-sold-me-to-the-war-god':
        'Sold at auction, then handed on like a parcel.\nThe Alpha who bought Omega Elena discards her and passes her to his vanished uncle, Finn, the Lycan King they call the War God. What she finds out there changes the shape of everything behind her. Her five children were his all along, and the man she was sure had betrayed her has been loving and protecting her from the very start.',

    # FACTS: When Olivia signs up for a life-saving surgery that will erase every memory - including the man 
    # FACTS: who broke her heart - she's finally ready to walk away from her painful marriage. But with 14 da
    # FACTS: ys left on the clock, her cold, distant husband realizes too late what he's about to lose.
    'the-art-of-letting-go':
        'Fourteen days until she forgets him on purpose.\nOlivia signs up for a life saving surgery that will wipe every memory she has, including the man who broke her heart, and she is ready. The marriage has been painful for long enough. Her cold, distant husband has two weeks on the clock to work out what he is about to lose, and he is only starting to understand it now.',

    # FACTS: In The Atlantic Bride movie, in 1911, amid New York’s Gilded Age, Evelyn Hart, a rural English s
    # FACTS: choolteacher, voyages across the ocean for love, only to suffer betrayal at the hands of her fia
    # FACTS: ncé Thomas. On the ocean liner, she comes to the rescue of Julian Kane, a mysterious wounded man
    # FACTS: , and agrees to a marriage of convenience with him when left with nowhere to turn. Little does s
    # FACTS: he know he is the heir to the Kane family empire, commanding railways, shipping and steel. What 
    # FACTS: begins as a reclusive tycoon hiding his true identity blossoms into a tender romance. As workpla
    # FACTS: ce clashes and taunts from her old rival mount, affection grows between them, while the truth of
    'the-atlantic-bride':
        "She crossed an ocean for a man who betrayed her.\nIt is 1911, and Evelyn Hart, a rural English schoolteacher, crosses the ocean to New York's Gilded Age to marry Thomas, who has other plans for her. On the liner she saves a wounded stranger named Julian Kane, and with nowhere else to go she agrees to marry him for convenience. She has no idea he is heir to an empire of railways, shipping and steel. What starts as a reclusive tycoon keeping his name to himself turns into something tender, while her old rival keeps sniping and the truth of who he is works its way to the surface.",

    # FACTS: Kaelen Ashfell bought me at the Mate Auction for a fortune. Three years later, after I gave him 
    # FACTS: three hatchlings, his first love came back, and he crossed my name out of his Bond Ledger like I
    # FACTS:  was property to return. He handed me and our babies to his brother Roran, then let his first lo
    # FACTS: ve tear apart my den, my garden, and even hurt our child. Kael thought regret could bring me bac
    # FACTS: k. But the mate he discarded was about to learn what it felt like to be protected by someone els
    # FACTS: e.
    'the-auctioned-mate':
        'He crossed her name out of his Bond Ledger.\nKaelen Ashfell bought her at the Mate Auction for a fortune, and three years and three hatchlings later his first love came back, so he struck her out like property being returned. He handed her and the babies to his brother Roran, then stood by while his first love tore apart her den and her garden and hurt their child. Kael thinks regret is enough to bring her home. The mate he discarded is about to show him what being protected by someone else looks like.',

    # FACTS: Yvonne is murdered by her jealous sister right as she's giving birth. She wakes up one year in t
    # FACTS: he past, the day they picked their husbands! Fiona remembers the "future" and chooses Oliver, wh
    # FACTS: o was Yvonne's husband. Yvonne picks Fiona's past/future wheelchair-bound husband, Ethan. What n
    # FACTS: o one knows, is that Ethan is secretly the richest man in the world!
    'the-billionaire-groom-exchange':
        "Murdered in the delivery room, awake a year earlier.\nYvonne is killed by her jealous sister as she gives birth, and wakes on the day the sisters picked their husbands. Fiona remembers the future too, and takes Oliver, who was Yvonne's. So Yvonne takes the wheelchair bound husband Fiona was stuck with, Ethan. Neither knows Ethan is secretly the richest man in the world.",

    # FACTS: To discover who truly loves them, wealthy couple Hannah and her husband fake bankruptcy, with hi
    # FACTS: m pretending to be paralyzed after a stroke. Their test exposes the truth: their biological son 
    # FACTS: Thomas and his wife refuse to help and turn them away, while adopted son Theo and his wife give 
    # FACTS: up everything to save him. After learning the truth, Hannah and her husband leave their $50 mill
    # FACTS: ion fortune to Theo. Thomas loses everything and finally realizes that true family is built on l
    # FACTS: ove, not blood.
    'the-billionaire-parents-final-test':
        'They faked bankruptcy to find out who actually loved them.\nHannah and her husband stage the collapse, with him pretending to be paralysed after a stroke, and the results are unambiguous. Their biological son Thomas and his wife refuse to help and turn them out. Their adopted son Theo and his wife give up everything they have to save him. So the fifty million dollar fortune goes to Theo, Thomas loses the lot, and the lesson about what family is built on arrives far too late.',

    # FACTS: Iris’s mother, who had immigrated to the United States from Thailand as part of a blended family
    # FACTS: , died in a car accident along with her American husband while they were on their way to get mar
    # FACTS: ried. Unwilling to see Iris deported, her stepfather’s son, Leon, dropped out of school to work 
    # FACTS: on a construction site and shoulder the financial burden; as they relied on each other, the two 
    # FACTS: grew close. After graduating from high school, Iris was accepted into a New York law school, jus
    # FACTS: t as she had hoped. Leon promised to join her, but on the very last day, he was involved in an a
    # FACTS: ccident at the construction site, and the two lost contact. Five years later, Iris joined a top-
    'the-boy-raised-me-is-mine':
        "He left school for a construction site to keep her here.\nIris loses her mother and her American stepfather in a crash on the way to their wedding, and rather than watch her be deported, Leon, her stepfather's son, drops out and takes on the whole financial weight himself. Leaning on each other turns into something else. She gets into a New York law school as planned and he promises to follow, and on the last day there is an accident on the site and they lose contact. Five years later she is at a top firm, and Leon walks in.",

    # FACTS: After Dante Conti let his mistress Selena Russo torment their six-year-old daughter Sofia, Isabe
    # FACTS: lla Moretti fought back and was locked inside Ashford Sanitarium. Years later, Dante forced her 
    # FACTS: to sign away her rights with Sofia’s urn as a threat, believing he had broken her forever. But S
    # FACTS: icily turned the abandoned wife into Don Moretti. Backed by Luca Ricci, the Don of Palermo, and 
    # FACTS: the hidden power of her father Vittorio, Isabella returns to New York’s Five Families banquet to
    # FACTS:  expose Selena’s lies, reclaim her empire, and make Dante watch the Conti throne collapse for ev
    # FACTS: ery drop of blood he spilled.
    'the-don-s-bloody-bride':
        "He locked her away and used their daughter's urn as leverage.\nDante Conti let his mistress Selena Russo torment six year old Sofia, and when Isabella Moretti fought back she was put inside Ashford Sanitarium. Years later he forced her to sign her rights away with the urn in front of her, sure she was finished. Sicily had other ideas, and the abandoned wife came out of it as Don Moretti. Backed by Luca Ricci and the hidden weight of her father Vittorio, she walks into the Five Families banquet in New York to take her empire back.",

    # FACTS: On the Dragon Continent, bloodline is everything. Pure dragon blood grants shifting forms and ma
    # FACTS: gic resistance. Those who can't shift are called Exiles — treated as slaves. Kaelen, firstborn o
    # FACTS: f the Red Dragon House, was born unable to shift. On the eve of his coming-of-age, his three bro
    # FACTS: thers cut his tendons, stripped his inheritance, and took his fiancée. His father branded him a 
    # FACTS: slave and exiled him to the Silent Deadfire Volcano. In the volcano's depths, disaster became bl
    # FACTS: essing. The dragon blood within him awakened the ancient Progenitor Dragon God's inheritance. Ov
    # FACTS: er ten years, his severed bones regenerated, and he mastered world-destroying Dragon Tongue magi
    'the-dragon-s-return-reclaiming-my-throne':
        "His brothers cut his tendons the night before he came of age.\nOn the Dragon Continent, blood decides everything, and those who cannot shift are Exiles who live as slaves. Kaelen was firstborn of the Red Dragon House and born unable to shift, so his three brothers took his tendons, his inheritance and his fiancee, and his father branded him a slave and threw him into the Silent Deadfire Volcano. Down there the disaster turned. His blood woke the ancient Progenitor Dragon God's inheritance, and ten years later he has whole bones and Dragon Tongue magic that can end worlds.",

    # FACTS: Born a commoner, Eleanor has spent years quietly protecting her husband, Duke Adrian, and his ki
    # FACTS: ngdom. Yet he has always mistaken her loyalty for ambition, believing she married him only for s
    # FACTS: tatus and power. After being publicly humiliated and heartlessly cast aside by the man she loves
    # FACTS: , Eleanor finally gives up on their marriage and walks away. Only after she leaves does Adrian d
    # FACTS: iscover that the mysterious masked warrior who repeatedly saved his life was Eleanor all along. 
    # FACTS: What he still does not know is that she is also the long-lost heir to a powerful empire. When El
    # FACTS: eanor reclaims her identity and the power that rightfully belongs to her, Adrian finally realize
    'the-duchess-they-cast-away':
        'The masked warrior who kept saving him was his wife.\nEleanor was born a commoner and has spent years quietly protecting Duke Adrian and his kingdom, while he decided her loyalty was ambition and that she married him for the title. He humiliates her in public and casts her off, and she finally stops trying. Only once she is gone does he find out who the mysterious warrior was. He still does not know she is the long lost heir to a powerful empire, which she is about to reclaim.',

    # FACTS: Ethan Cole, a top-tier aviation legend in his previous life, dies as a national aviation legend.
    # FACTS:  He is reborn as an 8-year-old boy on the same flight where he once flew with his father. Only t
    # FACTS: his time, he knows the truth: Flight 8236 is going to crash, and everyone on board will die. At 
    # FACTS: 9,000 meters above sea level, fire begins to burn along the wings. The fuselage cracks open into
    # FACTS:  freezing air. As panic spreads across the cabin, Ethan realizes he is the only one who understa
    # FACTS: nds what is coming. Trapped in a child’s body, he must stop the disaster and save his father—the
    # FACTS:  man he loves most—before it is too late.
    'the-eight-year-old-captain':
        'He knows the flight goes down. He is eight years old.\nEthan Cole died a national aviation legend and woke up as a child on the same flight he once took with his father. Flight 8236 is going to crash and everyone aboard will die, and he is the only person who knows it. Nine thousand metres up the wings catch, the fuselage splits open into freezing air, and panic goes through the cabin. Trapped in a small body, he has to stop it and get to his father before it is too late.',

    # FACTS: To protect her beloved boyfriend Noah, Amelia accidentally causes her father’s “death.” In order
    # FACTS:  to safeguard their shared dream of a musical future, she hides her pregnancy, pretends to cheat
    # FACTS: , breaks up with Noah, and turns herself in—serving seven years in prison. Upon release, Amelia 
    # FACTS: discovers their daughter Lisa has leukemia, and only umbilical cord blood can save her. With no 
    # FACTS: other choice, she approaches Noah-now a global music star, and reconnects with him physically, h
    # FACTS: iding the truth behind her return. Noah has never stopped loving her, but the heartbreak of Amel
    # FACTS: ia‘s sudden betrayal still lingers. As they’re drawn back into each other’s orbit, love and pain
    'the-encore-of-us':
        "She confessed to a death, hid a pregnancy, and served seven years.\nProtecting Noah costs Amelia everything, starting with her father's apparent death. To keep their shared musical future intact she hides the baby, fakes an affair, ends it with him and turns herself in. She comes out to find their daughter Lisa has leukaemia and only cord blood will save her, so she goes to Noah, now a global star, and gets close again without telling him why. He never stopped loving her and the way she left still sits there. Then her dead father surfaces.",

    # FACTS: Roger, chairman of the trillion-dollar group WestDream, wantsto do something special for his sin
    # FACTS: gle mother and introduce his fiancée Vivian to her, so he brings his mother Susan, who works at 
    # FACTS: a small-town restaurant, to the city to celebrate her birthday. However, Vivian’s cousin Lisa, u
    # FACTS: naware of Susan’s true identity, mistakes Susan for a thief and humiliates her. Later, Susan is 
    # FACTS: again targeted by her future daughter-in-law Vivian, who treats Susan as a fraud and humiliates 
    # FACTS: her. Susan tries again and again to defend herself, but no one listens.After suffering repeated 
    # FACTS: humiliation, she is finally rescued by Roger. Only then does everyone realize that the humble Su
    'the-extraordinary-mother-of-a-billionaire':
        "They called his mother a thief. He owns a trillion dollar group.\nRoger runs WestDream and wants to do something special for the single mother who raised him, so he brings Susan up from her small town restaurant job to celebrate her birthday and meet his fiancee Vivian. Vivian's cousin Lisa takes one look and accuses her of stealing. Then Vivian joins in, treating her as a fraud. Susan defends herself again and again and nobody listens, right up until Roger walks in and the room understands who she is. By then regret is not much use to anyone.",

    # FACTS: One drunken night, one humiliating ex, fake-date her worst enemy Blake or watch the Greenharts l
    # FACTS: ose every point because of her. Hannah signs the contract expecting torture. Instead, she finds 
    # FACTS: the cold, untouchable rival everyone fears has a side no one's ever seen, fiercely protective, q
    # FACTS: uietly devoted, and hiding a secret of his own. When the pretending stops feeling like pretendin
    # FACTS: g, is it still an act? Then her ex Tristan discovers the truth—Hannah is Miss H, the anonymous g
    # FACTS: enius the whole school idolizes. Now he's on his knees, begging for a second chance. Two boys, o
    # FACTS: ne choice.
    'the-fake-dating-spell':
        'Fake date your worst enemy or sink the whole house.\nOne drunken night and one humiliating ex leave Hannah with a contract and no leverage, so she signs, expecting to be tortured by Blake for the duration. The cold untouchable rival everyone fears turns out to have a side nobody has ever seen, fiercely protective and quietly devoted, with a secret of his own. Then the pretending stops feeling like pretending. Her ex Tristan works out that Hannah is Miss H, the anonymous genius the school worships, and drops to his knees begging for a second chance. Two boys, one choice.',

    # FACTS: Framed by her pack, Leila was thrown into the Howling Chasm and lost her arm. Two years later, h
    # FACTS: er cruel family forces her to marry the North’s rumored “mad wolf,” Darian. But Darian is not ma
    # FACTS: d—he is her fiercest protector. When her grandmother reveals that Leila is the true Alpha’s daug
    # FACTS: hter, the impostor’s schemes collapse. Awakening her dormant wolf powers, Leila rejects her unwo
    # FACTS: rthy family and walks away with Darian into a new life under the blood moon.
    'the-furless-one':
        "Thrown into the Howling Chasm, she came out missing an arm.\nLeila was framed by her own pack, and two years later her cruel family marries her off to the mad wolf of the North, Darian. He is not mad, and he turns out to be the fiercest protection she has ever had. Then her grandmother says out loud that Leila is the true Alpha's daughter, the impostor's schemes fall apart, and the wolf that was sleeping in her wakes up.",

    # FACTS: On the night before her engagement, Celeste Yarrow is locked inside a rooftop glass greenhouse b
    # FACTS: y Ingrid Sloane, drenched in freezing water while the guests film and laugh. Damien Thorne, the 
    # FACTS: man she spent three years saving, refuses to protect her and even exposes her deepest trauma for
    # FACTS:  Ingrid’s amusement. Everyone thinks Celeste is just a small-town woman clinging to power, but s
    # FACTS: he is the real force behind Yarrow Capital and the projects that made Thorne rise. After shatter
    # FACTS: ing the glass cage herself, Celeste cancels the engagement, pulls her investment, releases the e
    # FACTS: vidence, and makes every betrayer pay.
    'the-glass-cage':
        'Locked in a glass greenhouse while the guests filmed it.\nThe night before her engagement, Ingrid Sloane shuts Celeste Yarrow into a rooftop greenhouse and drenches her in freezing water while everyone laughs. Damien Thorne, the man she spent three years building up, will not step in, and then hands Ingrid her deepest trauma for entertainment. They all think Celeste is a small town woman clinging to power. She is the actual force behind Yarrow Capital and the projects that made Thorne. She breaks the glass herself, cancels the engagement, pulls her money and releases the evidence.',

    # FACTS: Rejected by his royal family and cast into the ocean as a child, Kai secretly becomes the legend
    # FACTS: ary God of Tides. Years later, he returns home in disguise to find the pirate kingdom under sieg
    # FACTS: e. Now, Kai must save his family, all the while dealing with a father who thinks that he's worth
    # FACTS: less.
    'the-god-of-tides':
        'His family threw him in the ocean. It made him a god.\nCast out as a child by his royal family, Kai quietly becomes the legendary God of Tides. Years later he comes home in disguise and finds the pirate kingdom under siege. Saving his family means working around a father who still believes he is worthless.',

    # FACTS: On a snowy Thanksgiving, young healer Rita lives with her ungrateful uncle William and his cruel
    # FACTS:  family. They exploit her powers, sabotage her feast, and secretly hire a thug to drive her away
    # FACTS: . Hunted and alone, she is rescued by mafia godfather Richard Genovese and his wife. Discovering
    # FACTS:  their kindness and lack of an heir, they adopt her. On the journey, Rita's powers save them fro
    # FACTS: m crises, alarming Richard's rival. At the manor, she heals Richard's dying father, Arthur, and 
    # FACTS: finds a lost heirloom. Her courage and abilities win the family's trust. Rita becomes a true Gen
    # FACTS: ovese, protecting her new family with everything she has.
    'the-godfather-s-guardian-angel':
        "They hired a thug to run the healer out of the house.\nRita spends a snowy Thanksgiving with her ungrateful uncle William and his cruel family, who use her powers, wreck her feast and then arrange for her to be driven off for good. Hunted and alone, she is found by the mafia godfather Richard Genovese and his wife, who have no heir and know kindness when they see it, and they adopt her. Her powers pull them through crisis after crisis on the road, which does not go unnoticed by Richard's rival, and at the manor she heals his dying father Arthur.",

    # FACTS: Ever since their parents married, Becca has hated her stepbrother, Samir. For two years, she's b
    # FACTS: lamed him for stealing her family, her home, and the life she lost. But when a brutal heatwave k
    # FACTS: nocks out the AC, they’re trapped alone in a house that’s far too hot—and far too small. As Sami
    # FACTS: r struggles to fix the broken air conditioner, lingering resentment gives way to lingering touch
    # FACTS: es. The line between hate and desire begins to disappear, and Becca must face the one truth. She
    # FACTS: 's spent years denying that the man she's forbidden to want may be the only one she can't resist
    # FACTS: .
    'the-heat-after-the-ac-died':
        'The air conditioning dies. The house gets very small.\nBecca has spent two years blaming her stepbrother Samir for taking her family, her home and the life she had before their parents married. Then a brutal heatwave knocks the cooling out and they are shut in together with nowhere to go. He works on the broken unit, the resentment starts landing as something else entirely, and the line she has been holding gets harder to find. She has been denying it for years, and the man she is forbidden to want may be the only one she cannot resist.',

    # FACTS: Everyone accuses Faye of being a gold-digging prostitute because of her hobo clothes. Little do 
    # FACTS: they realize that she's the ONLY ONE who can cure the hottest and richest man in the nation - wa
    # FACTS: r hero, Adam Stone! (And win his heart too)
    'the-hobo-goddess-and-her-billion-dollar-contract':
        'They call her a gold digger. She is his only cure.\nFaye dresses like a hobo, so everyone in the room has decided what she is and says it out loud. Not one of them has worked out that she is the only person alive who can cure the hottest and richest man in the nation, war hero Adam Stone. Winning his heart is a bonus.',

    # FACTS: Four years ago, healer Seraphina saved cursed Infernal Legion commander Drake and gave birth to 
    # FACTS: twins. Unaware of his identity, she was exiled by her family and raised the children alone. Year
    # FACTS: s later, the wounded Drake is found by the kids and brought home. He falls for Seraphina at firs
    # FACTS: t sight and proposes firmly. Amid stepmother's persecution, brother's power grab and dark magic 
    # FACTS: crisis, they uncover the truth of their past. Finally Drake inherits the Lord of the North, and 
    # FACTS: the family of four lives happily together.
    'the-inferno-warlord-s-secret-healer-bride':
        "The twins found a wounded man and brought him home.\nFour years ago the healer Seraphina saved Drake, commander of the cursed Infernal Legion, and had his children without ever knowing who he was. Her family exiled her for it and she raised them alone. Now the children have dragged him back to her door, he falls for her on sight and proposes without hesitating, and they work out the truth of the past through a stepmother's persecution, a brother's grab for power and a dark magic crisis.",

    # FACTS: After Matilda's only daughter, Elodie, is rescued from her kidnapper by local police - she is tu
    # FACTS: rned over to foster care and never to be seen again. Matilda and her son, Carson, never stopped 
    # FACTS: searching for her - spending every last penny on posters and PI invesitgations till they starved
    # FACTS: . Then, after twenty long years of desperate attempts to get Elodie back, she returns. Except, n
    # FACTS: ow she's Billionaire CEO Miss Atkins and her company is going to destroy the very home she grew 
    # FACTS: up in - and the only remaining clue that could bring the family back together again.
    'the-lady-boss-ceo-is-my-daughter':
        'Twenty years of searching, and the billionaire is her.\nElodie is rescued from her kidnapper and then handed to foster care, and Matilda never sees her again. She and her son Carson spend two decades and every last penny on posters and private investigators, starving for it. Then Elodie comes back as Billionaire CEO Miss Atkins, and her company is set to demolish the home she grew up in, the one remaining clue that could put this family back together.',

    # FACTS: twenty‑year‑ago, top gambler Alexander was framed by Calvin, losing everything and turned into a
    # FACTS:  puppet. His daughter Ivy, abandoned back then, grows up with extraordinary gambling gifts. She 
    # FACTS: heads to Las Vegas, gambles at the enemy’s casino, reunites with her birth mother and half‑broth
    # FACTS: er. After deadly showdowns including a face‑off against her controlled father, Ivy kills the vil
    # FACTS: lain, settles old scores and rises as the new gambling god.
    'the-last-ace':
        "Her father was framed and turned into a puppet.\nTwenty years ago Calvin took everything from the top gambler Alexander, and the daughter he abandoned grew up with a gift of her own. Ivy goes to Las Vegas and sits down at the enemy's tables, finds her birth mother and half brother along the way, and works through a run of deadly showdowns that ends with her facing the father who is still being controlled.",

    # FACTS: Elena signed the divorce papers, penniless, wandering through the rain with her suitcase. A "Wan
    # FACTS: ted: Stepmother" flyer on a deli bulletin board caught her attention. She followed the address, 
    # FACTS: only to find that her employer turned out to be the Marchetti family, the most powerful mafia dy
    # FACTS: nasty on the East Coast.
    'the-mafia-boss-s-contract-bride':
        'Wanted, a stepmother. She answered the flyer.\nElena signs the divorce papers with nothing to her name and walks through the rain with a suitcase, and a notice on a deli board catches her eye. She follows the address to find that her new employer is the Marchetti family, the most powerful mafia dynasty on the East Coast.',

    # FACTS: Sabrina wakes from a crash to find her husband cheating with her best friend. To steal her $5 bi
    # FACTS: llion trust, he "gives" her to his Mafia uncle, Silas. She fakes amnesia and uses Silas's power 
    # FACTS: to destroy them both—exposing fake pregnancy, stealing deals, sending her husband to prison. Whe
    # FACTS: n she tries to leave, Silas corners her: "You took ten years to reach me. Now you want to run?" 
    # FACTS: He waited in the shadows for a decade—and finally turns her from a bargaining chip into his brid
    # FACTS: e.
    'the-mafia-s-stolen-bride':
        "He gave his wife to his mafia uncle for her trust fund.\nSabrina wakes from a crash to find her husband with her best friend, and his plan for her five billion dollar trust is to hand her to his uncle Silas. She fakes amnesia and uses Silas's reach to take both of them apart, exposing the fake pregnancy, stealing the deals, putting her husband in prison. Then she tries to leave, and Silas corners her to point out that she took ten years to reach him. He waited in the shadows the whole decade, and he is not treating her as a bargaining chip.",

    # FACTS: Serlanty, East Sea mermaid princess, was drained of golden scales by her family and lover. The b
    # FACTS: astard Winsil stole her credit. She traded the Heart of the Ocean for human form, defeated evil 
    # FACTS: with the Land King and found true love.
    'the-mermaid-queen-s-revenge':
        'Her family and her lover drained her golden scales.\nSerlanty is the East Sea mermaid princess, and the people closest to her take what makes her royal while the bastard Winsil claims the credit for her work. She trades the Heart of the Ocean for human form, beats what is coming with the Land King beside her, and finds the real thing on the way.',

    # FACTS: Clara is trapped in a year‑long sexless marriage. She develops hypersexuality and seeks medical 
    # FACTS: help—only to meet Dr. Killian, a domineering CEO‑physician who humiliates her during a full exam
    # FACTS: . That night, her husband Julian rejects her advance, and she discovers he gratifies himself to 
    # FACTS: photos of her half‑sister Vivian—exposing the fraud of her marriage. The next day, Killian is re
    # FACTS: vealed as her company's new CEO. He promotes her to his personal assistant, exploiting her condi
    # FACTS: tion with constant verbal and physical pressure. During a phone call from her own home, with Jul
    # FACTS: ian just outside the door, Killian pushes her into a hysterical orgasm, escalating their forbidd
    'the-new-ceo-turns-out-to-be-my-gynecologist':
        "The doctor who humiliated her is her new CEO.\nClara is a year into a sexless marriage when hypersexuality sends her looking for medical help, and she gets Dr Killian, a domineering CEO physician who humiliates her through a full exam. That night Julian rejects her and she finds him gratifying himself to photos of her half sister Vivian, which is the whole marriage explained. The next morning Killian is announced as her company's new CEO. He makes her his personal assistant and applies pressure everywhere he can find it, and his possessiveness only sharpens when a friend of his shows interest in her.",

    # FACTS: High school star student Eleanor Vance has been best friends with Leo Carter for 16 years, until
    # FACTS:  he knocks her out and ties her to a goalpost as a “prank” to impress the popular girl Savannah.
    # FACTS:  Humiliated in front of the whole school, Ellie transfers to California without a word. There, s
    # FACTS: he finds real friends, academic success, and a caring new boyfriend. Meanwhile, Leo loses his mi
    # FACTS: nd with regret, but Ellie has learned that some betrayals can never be forgiven.
    'the-prank-that-broke-us':
        'Sixteen years of friendship, and he tied her to a goalpost.\nEleanor Vance and Leo Carter grew up together, right up to the day he knocks her out and strings her up as a prank to impress Savannah. Humiliated in front of the entire school, Ellie transfers to California without saying goodbye. There she finds real friends, does well, and meets someone who treats her properly. Leo loses his mind with regret back home, which is his to carry, because Ellie has worked out that some betrayals do not get forgiven.',

    # FACTS: At Asgard Academy, underdog Elena is relentlessly bullied for her pathetically weak magic. Ice-c
    # FACTS: old, stoic Professor Cassius notices her for one thing. Her scent feels hauntingly familiar, and
    # FACTS:  it inexplicably awakens his long-sealed curse mark. He offers her private tutoring as cover, he
    # FACTS: lping her rein in her wildly unstable magic. Until he makes the shocking discovery...
    'the-professor-s-forbidden-dragon-prey':
        'Her scent woke a curse mark he had sealed for years.\nElena is bullied without mercy at Asgard Academy for magic everyone agrees is pathetic. The ice cold Professor Cassius notices her for one reason only, which is that she smells hauntingly familiar and something long buried in him responds to it. He offers private tutoring as a cover story and helps her get her wildly unstable magic under control, and then he finds out what she actually is.',

    # FACTS: Asher secretly dated QB Chase for six months. Chase never went public—instead he played the perf
    # FACTS: ect couple with Asher's sister Daisy. A naked photo of Asher leaked across campus. Daisy stole i
    # FACTS: t from Chase's phone. Chase told Asher to stay quiet and kept using him. Hockey captain Finn ope
    # FACTS: ned Instagram in front of everyone: “Want to date? Follow me first.” Next day, he held Asher's h
    # FACTS: and in the hallway—fingers laced, for everyone to see. Daisy faked a nut allergy attack to frame
    # FACTS:  Asher. Asher shoved her head into a fountain. Chase lost his game and screamed at Daisy on the 
    # FACTS: sideline—his golden image shattered. Finn won, looked at the camera, and said: “Our goalie held 
    'the-quarterback-s-secret-darling':
        "Six months in secret while he played the perfect couple with her sister.\nChase never went public with Asher, and Daisy took the naked photo off his phone and let it run across campus. Chase told Asher to keep quiet and carried on using him. Then the hockey captain Finn opened Instagram in front of everyone and said follow me first, and the next day held Asher's hand down the hallway with their fingers laced where nobody could miss it. Daisy fakes an allergy attack to frame him, Asher puts her head in a fountain, and Chase loses his game and his golden image on the sideline.",

    # FACTS: I‘m Elowen, the only rabbit shifter with purifying blood, destined to be Alpha King Kael’s Luna.
    # FACTS:  But on our bonding altar, he brought his pregnant snake mistress, ordering me to raise their ch
    # FACTS: ild as their servant. I revoked our bond and offered myself to any shifter willing to claim me. 
    # FACTS: Everyone feared Kael—until cursed, discarded Prince Rowan stepped forward. I chose him, my pure 
    # FACTS: blood suppressing his deadly curse. The old prophecy shifted to us. Kael lost all power and begg
    # FACTS: ed me back, while his serpent lover sank into dark corruption. Can Rowan and I stop the feral be
    # FACTS: ast tide sweeping the realm?
    'the-rabbit-bride-who-rejected-her-alpha-king':
        "He brought his pregnant mistress to their bonding altar.\nElowen is the only rabbit shifter with purifying blood and she is meant to be Alpha King Kael's Luna, right up until he arrives with his snake mistress and instructs her to raise their child as a servant. She revokes the bond and offers herself to any shifter willing to take her. They all fear Kael, until the cursed and discarded Prince Rowan steps forward. Her blood suppresses his curse, the old prophecy moves to them, and Kael loses everything and comes back begging.",

    # FACTS: “Did you get rejected?!” My sister Jade laughs at me. “I knew it! I told you that you would. No 
    # FACTS: one would ever want you. A wolfless. But I’m more surprised that you, of all people, found a fat
    # FACTS: ed mate. Kind of unfair if you ask me.” It stings to hear this. It’s exactly what happened. She 
    # FACTS: was right. “Well, let’s not let this bring us down.” Mother smiles and claps. “It’s been decided
    # FACTS:  that Jade is to be mated to the fourth wolf prince. ” Jade smirks. “One of the bastard illegiti
    # FACTS: mate princes, but I’m not complaining.” She smiles with pride. “He’s still a prince.” The crowd 
    # FACTS: suddenly grow noisy. The princes arrive. “Alpha Prince Dorian, the fourth prince, Antonio the fi
    'the-raven-wolf-king-wolfless':
        'Rejected, and her sister will not let it go.\nJade laughs at her for it, says she always knew, says nobody would want a wolfless, and admits she is surprised someone like her found a fated mate at all. It stings because it happened exactly that way. Then Mother claps and announces Jade will be mated to the fourth wolf prince, one of the illegitimate ones, which Jade decides she can live with because a prince is a prince. The crowd goes up as the princes arrive, Dorian and Antonio and Emmet, all three of them illegitimate.',

    # FACTS: Elena, the biological daughter of the wealthy Delaney family, was framed by her adopted sister S
    # FACTS: arah in a car accident. Wrongfully accused of drunk driving, she was sentenced to ten years in p
    # FACTS: rison. Nobody believed her. Famous sculptor Leo helped her take a new identity. Flora grew into 
    # FACTS: a renowned sculptor. When she returned, Sarah accused her of being an ex-con and plagiarizing ar
    # FACTS: tworks. Flora fought back, exposing Sarah's lies. Sarah was the bastard daughter of Elena's dad.
    # FACTS:  Sarah got punished. Flora cut ties with the cold family and started a new life with her lover M
    # FACTS: arc.
    'the-real-heiress-reclaims-her-place':
        'Ten years in prison for a crash she did not cause.\nElena is the biological daughter of the wealthy Delaney family, and her adopted sister Sarah frames her for a drunk driving accident that costs her ten years. Nobody believes her. The sculptor Leo gives her a new identity, and Flora comes out of it a renowned artist in her own right. Sarah greets her return by calling her an ex con and a plagiarist, which is the last mistake she gets to make. Flora takes her lies apart in public, the truth about Sarah being the bastard daughter comes out, and Flora walks away from the cold family for good with Marc.',

    # FACTS: This is a female-oriented revenge short drama with a rebirth & counterattack theme. With her pas
    # FACTS: t-life memories, the heroine Chloe is reborn. She avoids the marriage-robbing trap set by her si
    # FACTS: ster Lily, gives up the false shortcut of becoming a mafia godmother, and chooses to accept the 
    # FACTS: upright wealthy businessman Jayce who is in financial crisis. Relying on her experience in manag
    # FACTS: ing underground industries from her previous life, she helps Jayce turn the tables and reach the
    # FACTS:  top. In the end, the evildoers get what they deserve, and Chloe becomes the ultimate ruler of b
    # FACTS: oth the legal and underworld worlds on the East Coast.
    'the-road-not-taken':
        "She has done this life before, and the shortcut was a trap.\nChloe is reborn holding everything she learned the first time, which means she sees her sister Lily's marriage robbing scheme coming and steps around it. She turns down the false shortcut of becoming a mafia godmother and backs Jayce instead, an upright wealthy businessman in real financial trouble. Everything she learned running underground industries in the last life goes into pulling him back to the top, and by the end the people who wronged her have what is coming and she rules both sides of the East Coast.",

    # FACTS: In The Rockstar's Secret movie, Juniper is hopelessly, recklessly in love with Tristan—the dark,
    # FACTS:  intoxicating rockstar who rules their campus. The catch? He’s her protective older brother Cart
    # FACTS: er’s best friend, and as far as Tristan is concerned, Juniper is nothing more than an invisible 
    # FACTS: little sister. Until the night the lights go out. Trapped in the pitch-black darkness, a wild, u
    # FACTS: ninhibited flame ignites between them—a night of unforgettable passion with a mysterious girl wh
    # FACTS: ose face Tristan never saw. All he has to trace his secret lover is a delicate butterfly bracele
    # FACTS: t left behind, and the vivid memory of a butterfly birthmark. He is obsessively hunting for the 
    'the-rockstar-s-secret':
        "One night in the dark, and a butterfly bracelet.\nJuniper is recklessly in love with Tristan, the rockstar who rules their campus, who happens to be her protective older brother Carter's best friend and who has never seen her as anything but an invisible little sister. Then the lights go out, and what happens between them in the pitch black is not something either can take back. All Tristan has afterward is a delicate butterfly bracelet and the memory of a butterfly birthmark, and he is hunting obsessively for a stranger who sits across his kitchen table every day.",

    # FACTS: When the British heir dies suddenly, a modern royal family spirals into chaos. Party-loving twin
    # FACTS: s Prince Liam and Princess Eleanor are forced to grow up fast—Liam is thrust toward the crown wh
    # FACTS: ile falling for Ophelia, the palace security chief’s American daughter, and Eleanor hits rock bo
    # FACTS: ttom after a dangerous betrayal. As King Simon grieves and the monarchy teeters, ruthless Queen 
    # FACTS: Helena joins forces with scheming Prince Cyrus to keep control at any cost. A dynasty built on g
    # FACTS: lamour is about to face its darkest reckoning. Buy full season: https://www.lionsgate.com/shows/
    # FACTS: the-royals/the-royals-season-1
    'the-royals':
        'The heir dies, and the party is over for everyone.\nA modern British royal family comes apart when the heir suddenly dies. The party loving twins have to grow up in a hurry, Prince Liam pushed toward the crown while falling for Ophelia, the American daughter of the palace security chief, and Princess Eleanor hitting bottom after a dangerous betrayal. King Simon is grieving and the monarchy is wobbling, which suits the ruthless Queen Helena, who joins forces with the scheming Prince Cyrus to hold control at any price. A dynasty built on glamour is heading for its darkest reckoning.',

    # FACTS: Raised on her Grandma's one unbreakable rule, stay away from serpents, she never expects to save
    # FACTS:  a heavily wounded man in the forest. Little does she know, the man she's saved is the feared Si
    # FACTS: lver Serpent King, Silvan. He's made up his mind and has marked her as his. On Bella's wedding d
    # FACTS: ay, he crashes the ceremony and declares her his in front of everyone. Desperate to escape this 
    # FACTS: possessive monster, Bella decides to run away with her childhood sweetheart. But to her shock, t
    # FACTS: he man she trusts most betrays her and offers her up as a sacrifice. Betrayed, hunted, and on th
    # FACTS: e edge of death, the man she once feared most becomes the only one left protecting her.
    'the-silver-serpent-s-bride':
        'Grandma had one rule. Stay away from serpents.\nBella breaks it by saving a badly wounded man in the forest, without knowing he is Silvan, the feared Silver Serpent King, who decides on the spot that she is his. He crashes her wedding to claim her in front of everyone. Desperate to get away from him she runs with her childhood sweetheart, the person she trusts most, who hands her over as a sacrifice. Betrayed and hunted and close to dying, she finds the monster she was running from is the only one still standing between her and the end.',

    # FACTS: Sawyer is a quarterback prodigy, but his mom Marnie always ignores him in favor of his adopted b
    # FACTS: rother, Ben, even when Ben frames Sawyer, steals his MVP title, and ruins his future. Heartbroke
    # FACTS: n, Sawyer vows to make his mom realize just how much she hurt him and how much she's lost.
    'the-son-rises-alone':
        'His mother chose the brother who framed him.\nSawyer is a quarterback prodigy, and Marnie has never once looked at him the way she looks at his adopted brother Ben. Ben frames him, takes his most valuable player title and ruins what was coming next, and she still does not see it. Heartbroken, Sawyer sets out to make his mother understand exactly what she did and exactly what she has lost.',

    # FACTS: The human girl Lena is sacrificed to Draven, a Vampire King afflicted by a petrification curse, 
    # FACTS: and the two unexpectedly forge a life-binding blood pact. To save Draven—who is left dying and d
    # FACTS: rained of his royal blood after the curse is broken—Lena endures seven years of perilous hardshi
    # FACTS: ps to locate the source of the Blood Spring and rescue her true love. Ultimately, they ascend th
    # FACTS: e throne side by side, ruling over a kingdom where humans and vampires coexist. Yet, just as pea
    # FACTS: ce dawns, the sigil of an ancient witch quietly begins to glow red deep within the Blood Spring.
    # FACTS: ..
    'the-stone-cursed-king-s-blood-bride':
        "Sacrificed to a vampire king turning slowly to stone.\nLena is handed over to Draven, who is under a petrification curse, and instead of the ending everyone expected they forge a life binding blood pact. Breaking the curse leaves him dying and drained of royal blood, so Lena spends seven hard years hunting the source of the Blood Spring to bring him back. They take the throne together over a kingdom where humans and vampires live side by side, and then an ancient witch's sigil starts glowing red down in the Blood Spring.",

    # FACTS: Tessa’s crush throws her cinnamon roll in the trash and calls her a fat pig in front of the whol
    # FACTS: e class. When she finally stops begging to be chosen, she starts glowing up and catches everyone
    # FACTS: ’s eye, including the boy who destroyed her. But Tessa has already chosen Adrian, the masked out
    # FACTS: cast everyone calls scarred and pathetic. By the time Chase wants her back, Adrian’s secret is o
    # FACTS: ut: he was never weak. He was the richest, most dangerous boy in the room.
    'the-ugly-girl-turned-pretty':
        "He binned her cinnamon roll and called her a fat pig.\nTessa's crush does it in front of the whole class, and the day she stops begging to be chosen is the day everything turns. She glows up, the room notices, and so does the boy who wrecked her. Too late. Tessa has already chosen Adrian, the masked outcast everybody writes off as scarred and pathetic. By the time Chase wants her back, Adrian's secret is out, and he was never the weak one. He was the richest and most dangerous boy in the room.",

    # FACTS: Princess Valerie marries the ruthless Dragon King Therak to save her kingdom. But their wedding 
    # FACTS: night hides a deadly game. Beneath her pillow lies the dagger meant for his heart. In his veins 
    # FACTS: flows a curse: devour her before the Blood Moon, or die. Yet when danger strikes, Therak risks h
    # FACTS: is life to protect her. Enemies by fate, lovers by choice. The Blood Moon rises. One must die.
    'the-virgin-sacrifice-the-dragon-king-claims':
        'There is a dagger under her wedding pillow.\nPrincess Valerie marries the ruthless Dragon King Therak to save her kingdom, and neither of them comes to the wedding night honestly. She has a blade meant for his heart. He carries a curse that says devour her before the Blood Moon or die himself. Then danger arrives and Therak puts his life between her and it. Enemies by fate, lovers by choice, and the Blood Moon is rising on both of them.',

    # FACTS: Cassia, the Wingless Goddess, was born a scapegoat for fake‑princess Celine. Mis‑prophesied as a
    # FACTS:  doomsday omen at birth, she was abandoned by her birth father. Raised under the protection of h
    # FACTS: er adoptive father, she awakens the legendary divine wings. She exposes that fake‑princess Celin
    # FACTS: e is the real destroyer behind everything. Finally, she overthrows the corrupt Wing‑Caste system
    # FACTS:  and ascends the throne as the new queen.
    'the-wingless-god':
        'Born wingless and blamed for the end of the world.\nCassia was mis prophesied as a doomsday omen at birth and handed the role of scapegoat for the fake princess Celine, then abandoned by her own father. Her adoptive father keeps her alive long enough for the legendary divine wings to wake in her. She proves Celine is the real destroyer behind all of it, brings down the corrupt Wing Caste system and takes the throne herself.',

    # FACTS: Thirteen years ago, a traitorous scheme tore the Bloodwolf Clan apart. The true-born princess, s
    # FACTS: till just a child, was cast out in the wild, losing all memory of who she really was. At ninetee
    # FACTS: n, she awakens the overpowering Progenitor's Power. Returning home, she finds her Mother torture
    # FACTS: d, her father paralyzed, and the traitors colluding with the enemy to destroy the clan from the 
    # FACTS: inside. Will the true-born princess be able to reclaim her throne and save her people?
    'the-wolfless-alpha-queen':
        "Cast out as a child, she woke up with the Progenitor's Power.\nA traitorous scheme tore the Bloodwolf Clan apart thirteen years ago, and the true born princess was left in the wild with no memory of who she was. At nineteen the power comes up in her and she goes home, to a mother being tortured, a father paralysed, and traitors working with the enemy to hollow the clan out from the inside.",

    # FACTS: Freya, a female rabbit beastkin, was adopted by Lady Hughes, her mother’s best friend, after her
    # FACTS:  parents passed away. She grew up and attended school alongside Landon and Marcel, the twin wolf
    # FACTS:  beastkin brothers of the Hughes household. The twins were popular celebrities at the beastkin a
    # FACTS: cademy. Leveraging her rabbit-type healing powers, Freya tirelessly helped them resolve all kind
    # FACTS: s of troubles, fully believing she would marry one of the two brothers someday. Everything fell 
    # FACTS: apart the moment Charlotte, a fox beastkin, appeared. Charlotte schemed relentlessly to frame Fr
    # FACTS: eya and drive her away. She successfully manipulated the wolf twins into misunderstanding Freya,
    'the-wolves-regret-for-their-rabbit':
        'She healed them for years, then the fox arrived.\nFreya is a rabbit beastkin taken in by Lady Hughes after her parents died, and she grows up alongside the twin wolf brothers Landon and Marcel, who are celebrities at the beastkin academy. Her healing powers get them out of everything, and she assumes she will marry one of them. Charlotte the fox beastkin arrives and works patiently at framing her, turning the twins against her one misunderstanding at a time, until Freya has nowhere in that house left to stand.',

    # FACTS: No mate, no wolf, and raising a pup alone, Ella never expected one act of kindness to tie her fa
    # FACTS: te to Alpha Torin, who is cursed to never touch a woman. When she becomes the wet nurse to his n
    # FACTS: ewborn heir, Ella is pulled into a deadly game of jealousy and betrayal inside the Alpha's keep.
    'thirsty-for-the-wet-nurse':
        "No mate, no wolf, and a pup to raise alone.\nElla has nothing and expects nothing, so one act of kindness tying her fate to Alpha Torin is not a thing she saw coming. He is cursed never to touch a woman. When she becomes wet nurse to his newborn heir, she walks straight into a deadly game of jealousy and betrayal being played inside the Alpha's keep.",

    # FACTS: Cole was the undisputed Supreme Sorcerer — until he died in a cataclysmic magical war. His soul 
    # FACTS: reincarnated into the body of a young boy named Leo — a boy afflicted with a Death Curse, with l
    # FACTS: ittle time left to live. The only hope: the Starlight Potion, guarded by the arrogant Westwood f
    # FACTS: amily. Leo’s mother, Clara, a powerless ordinary woman, humbled herself before the Westwoods, be
    # FACTS: gging for the potion to save her son.They ridiculed her. Humiliated her. But Clara never backed 
    # FACTS: down. Until Leo could take it no more.Something inside Leo shattered. A pressure so immense it c
    # FACTS: racked the marble floor exploded from his tiny frame. The entire Westwood mansion trembled. Ever
    'this-child-is-a-legendary-sorcerer':
        "The Supreme Sorcerer died. He woke up as a dying boy.\nCole is killed in a cataclysmic magical war and reincarnates into Leo, a child carrying a Death Curse with little time left. The only hope is the Starlight Potion, held by the arrogant Westwood family. Leo's mother Clara is an ordinary powerless woman, and she humbles herself in front of them and begs. They ridicule her. She refuses to back down, and then something in Leo gives way. The marble floor cracks, the mansion shakes, and every sorcerer in the room is on their knees unable to breathe. What none of them know is that Clara carries the Death Curse too.",

    # FACTS: She discovers her mob boss husband's affair and loses one of her twin babies due to his adopted 
    # FACTS: sister's schemes. She reports him to the authorities and flees while still pregnant. Seven years
    # FACTS:  later, she runs into him on the street. She thinks her murderous husband is going to kill her, 
    # FACTS: but when he drags her back home against her will, she realizes the truth. Seven years ago, it wa
    # FACTS: s all a misunderstanding. The ruthless mafia boss only wants one thing—to win her love back.
    'torn-between-the-mafia-twins':
        "She reported her mob boss husband and ran, pregnant.\nHis adopted sister's schemes cost her one of her twin babies, and his affair costs him everything else. She turns him in to the authorities and disappears while still carrying the other child. Seven years later they meet on the street and she is certain her murderous husband has come to kill her. He drags her home instead, and the truth finally lands. Seven years ago was a misunderstanding, and the ruthless mafia boss wants one thing, which is her love back.",

    # FACTS: Cora took in three wounded wolves and raised them. The moment her sister Vivian appeared, the wo
    # FACTS: lves couldn't look away—they turned cold and rough, trying to break Cora. She overheard them moc
    # FACTS: king her. So she offered a trade: three wolves for Vivian's snake. Silas the snake was ice-cold,
    # FACTS:  yet he stayed—doing chores, guarding her. When her family forced an arranged marriage, Cora fak
    # FACTS: ed agreement, then fled through a window on her wedding day. Silas tracked her to the airport, i
    # FACTS: njuring two wolves who tried to stop him. “You'll never get rid of me,” he said. Cora took over 
    # FACTS: the family business and bonded with Silas. The cold snake was truer than any wolf.
    'traded-my-wolves-for-a-snake':
        'Three wolves for one snake, and she never looked back.\nCora took in three wounded wolves and raised them, and the moment her sister Vivian walked in they could not look away, turning cold and rough and working on breaking her. She overhears them laughing at her, so she offers the trade. Silas the snake is ice cold and stays anyway, doing chores, standing guard. When her family forces an arranged marriage she plays along and goes out a window on the wedding day, and Silas tracks her to the airport, putting down two wolves who try to stop him.',

    # FACTS: I ran from my arranged wedding after catching my fiancé in bed with another woman. That same nig
    # FACTS: ht, I lost my virginity to a stranger—only to discover he was my fiancé all along. When I became
    # FACTS:  pregnant, he looked me in the eye and said, “Get rid of the baby.” I walked away for good... un
    # FACTS: til his powerful rival offered me a new life. Now two mafia heirs are fighting for me, but only 
    # FACTS: one deserves my heart. The problem? The man who broke me refuses to let me go.
    'two-mafia-bosses-begging-me-for-love':
        'She ran from the wedding and slept with a stranger.\nShe caught her fiance in bed with someone else and left, and the stranger she went home with that night turns out to be the fiance himself. When she falls pregnant he looks straight at her and tells her to get rid of it, so she goes for good. His most powerful rival offers her a different life. Now two mafia heirs are competing for her, only one of them has earned anything, and the man who broke her refuses to let go.',

    # FACTS: Ava once saved Ethan after he was drugged, only to be forced into a marriage that made him hate 
    # FACTS: her until her death. Reborn on the same night, she refuses to be his antidote, cuts him out of h
    # FACTS: er life, protects her grandfather, and exposes Chloe's lies. This life is not about making Ethan
    # FACTS:  regret her; it is about walking toward someone who truly catches her.
    'uncle-i-don-t-want-you-anymore':
        "She saved him once and he hated her until she died.\nAva helped Ethan when he was drugged, and it bought her a forced marriage and years of his contempt. Reborn on the same night, she refuses to be his antidote. She cuts him out entirely, gets her grandfather protected, and takes Chloe's lies apart in the open. This time is not about making Ethan sorry. It is about walking toward someone who actually catches her.",

    # FACTS: After his father dies saving the world, he is branded a traitor and his entire clan is destroyed
    # FACTS: . Ryan vanishes into exile, training in secret for fourteen years. Now Ryan returns to expose th
    # FACTS: e dark mage's conspiracy, clear his father's name.
    'vindication-blood-of-the-archmage':
        "His father saved the world and was called a traitor for it.\nThe clan was destroyed for it too. Ryan disappeared into exile and spent fourteen years training where nobody could see him, and he is back now to pull the dark mage's conspiracy into the open and put his father's name right.",

    # FACTS: Six years ago, top lawyer Madeline met wealthy heir Nicholas at a masquerade ball and later gave
    # FACTS:  birth to a clever daughter Isla. Her half-sister Vivienne stole keepsakes to pretend to be Nich
    # FACTS: olas's lover, coveting wealth and status. Later, Madeline worked at Nicholas's group and reunite
    # FACTS: d with him. Romance bloomed between them amid constant workplace schemes and threats. Clues incl
    # FACTS: uding a rare hereditary disease and identical birthmarks revealed the truth. Eventually, Vivienn
    # FACTS: e's fraud was exposed. All misunderstandings were cleared up. Madeline and Nicholas chose each o
    # FACTS: ther, and the three lived a happy life together.
    'wrong-heir-right-her':
        "A masquerade, a daughter, and a sister with the keepsakes.\nSix years ago the lawyer Madeline met the heir Nicholas at a masked ball, and afterwards raised a clever daughter called Isla. Her half sister Vivienne stole the mementoes and used them to pass herself off as his lover, chasing the money and the standing. Then Madeline takes a job at Nicholas's group and they are in the same rooms again, with romance building through constant scheming and threats, until a rare hereditary disease and matching birthmarks say plainly what happened.",

    # FACTS: After his girlfriend dumps him, Michael, a luxury brand CEO with X-ray vision, uses his powers a
    # FACTS: nd confidence to bring down arrogant global influencer bullies, all while winning the heart of h
    # FACTS: is high school's most popular girl.
    'you-can-t-stop-my-super-x-ray-vision':
        'Dumped, and then he stopped being polite about the vision.\nMichael runs a luxury brand and sees through anything he looks at, and after his girlfriend leaves he puts both to work on the arrogant global influencers throwing their weight around. Somewhere in the middle of taking them apart, he wins over the most popular girl from his old school.',

}
