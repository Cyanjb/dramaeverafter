# -*- coding: utf-8 -*-
"""Caption batch 18 Oct 2026, half A: 19 ReelShort titles from the 18 Oct
weekly scrape. STAGED FOR CYAN'S REVIEW, not approved. A second half is being
written in parallel as a separate file.

Every caption is written from the ReelShort book the title page links to
(availability.csv direct_link), matched on the 24 hex book id, not the slug.
Each FACTS entry is that book's synopsis as read by the 18 Oct scrape
(reelshort_2026-10-18.json), whitespace collapsed. w-king: same book id and the
same synopsis text in reelshort_2026-10-11.json; that source is short (names and
premise only), so the caption retells only what it gives.

NOT WRITTEN: none. All 19 sources carry names and a story.
"""

BATCH_TAG = "New 18 Oct"

CAPTIONS = {
    # 33.8M    Never Enjoyed Divorce Like This
    # FACTS: She is a wealthy heiress and a renowned fashion designer who gave up her career for her husband.
    # FACTS: However, his coldness and distrust broke her heart. After their divorce, she met a handsome,
    # FACTS: wealthy, and caring new man who helped her slowly forget the pain of her past. She thought she had
    # FACTS: found her true love, but little did she know that he was only after her money and power. When she
    # FACTS: discovered the deception and left him, he realized he had truly fallen for her. At the same time,
    # FACTS: her ex-husband wanted to reconcile. Who will she choose?
    # FACTS: https://www.reelshort.com/movie/never-enjoyed-divorce-like-this-66da5b2863f055aeb90e1bf9
    'never-enjoyed-divorce-like-this':
        "She gave up her career for him. He never even trusted her.\nShe's a wealthy heiress and a famous fashion designer, and she put her career aside for her husband. What she got back was a man who was cold to her and never trusted her, and in the end he broke her heart. After the divorce a new man comes along who's handsome, rich and kind, and slowly he helps her let go of the hurt. She's sure she's finally found real love. She hasn't. All he wanted was her money and her power, and when she finds out she walks away. Only then does he realize he's actually fallen for her. And at the very same moment, her ex husband decides he wants her back. Both men hurt her, and now both want her. Who will she choose?",
    # 11.7M    Divorced, I Married the Mafioso
    # FACTS: Humiliated, divorced and broke, orphan Nina applies to be the step-mom for hire of Mafia Don Leon
    # FACTS: Marconi, wins little Gio over with a Spider-Man doll, and signs a marriage contract. His tenderness
    # FACTS: eases her depression, and when he names her his wife at a gala, Easton's family collapses.
    # FACTS: Drug-addled Easton kidnaps Nina and Gio; Leon drives him off, they marry for real, and Gio proves to
    # FACTS: be his sister's son. Carmen's revenge fails as Nina gives birth to Dahlia, and Easton dies by his
    # FACTS: own bomb.
    # FACTS: https://www.reelshort.com/movie/divorced-i-married-the-mafioso-6ab6084357304459cf0cfcc5
    'divorced-i-married-the-mafioso':
        "Her divorce left her broke. A Mafia Don hired her as a stepmom.\nNina is an orphan, freshly divorced, humiliated and out of money. So she applies to be a paid stepmom for Leon Marconi, a Mafia Don, and wins over little Gio with a Spider Man doll. She signs a marriage contract. Leon is gentle with her, and bit by bit that tenderness pulls her out of her depression. When he introduces her at a gala as his wife, Easton's whole family comes crashing down. Easton, out of his mind on drugs, kidnaps Nina and Gio, and Leon runs him off. After that the contract isn't needed anymore, because they marry for real, and it turns out Gio is really the son of Leon's sister. Carmen tries for revenge and fails, Nina gives birth to a baby girl named Dahlia, and Easton is killed by his own bomb.",
    # 9.8M     Hearing the Little Alpha's Mind Saved My Life
    # FACTS: For Ava, Godfather Alexander’s Capone estate is the only safe place left in Hearing The Little
    # FACTS: Alpha’s Mind Saved My Life. At least, that’s what she believes as she desperately tries to stay
    # FACTS: inside. Beyond the estate, her husband has sent armed rogues after her, and every one of them is
    # FACTS: ready to tear her apart. When Ava first reaches the estate, wolf scratches cover her arms and legs,
    # FACTS: and she is bleeding badly. At first, Ava only hopes to find work as one of the maids. The job is far
    # FACTS: from easy. She is expected to tame Alexander’s cute but dangerous little pup, Leo. His raging
    # FACTS: bloodline can make him bite just about anyone—and anything—that gets too close. Something about Leo
    # FACTS: doesn’t make sense. Although he is dangerous around everyone else, he clings to Ava like a soft
    # FACTS: kitten. After she removes a nasty, sharp splinter from his mouth, she begins to discover what has
    # FACTS: really been happening to him. Through his thoughts, Leo tells Ava that his grandmother has been
    # FACTS: poisoning him. If Ava wants to earn her freedom, she must first find a way to cure the Young Master.
    # FACTS: Characters Ava Ava is the wolfless girl and main female character of Hearing The Little Alpha’s Mind
    # FACTS: Saved My Life. She possesses the unusual ability to hear Young Master Leo’s thoughts. Her connection
    # FACTS: with Leo catches Alexander’s attention and makes her the target of the Head Nanny’s jealousy. Alpha
    # FACTS: Alexander Alpha Alexander is the main male character and the feared King of the Black Werewolves.
    # FACTS: Other werewolves shiver at the sound of his name. He takes an interest in Ava after seeing how
    # FACTS: easily she can soothe Young Master Leo. Young Master Leo Young Master Leo is Alpha Alexander’s cute
    # FACTS: but dangerous little pup. His behavior is shaped by his raging bloodline and the mistreatment he
    # FACTS: suffers from his grandmother. Despite his aggression toward others, he quickly becomes attached to
    # FACTS: Ava. Head Nanny The Head Nanny is a minor villain in the series. She pretends to care for Young
    # FACTS: Master Leo while secretly conspiring with his grandmother. Ava’s growing connection with Leo also
    # FACTS: makes the Head Nanny jealous.
    # FACTS: https://www.reelshort.com/movie/hearing-the-little-alpha-s-mind-saved-my-life-6ab0966c2eac8bc8bb0d3e4d
    'hearing-the-little-alpha-s-mind-saved-my-life':
        "She can hear the Alpha's little pup thinking. He says his grandmother is poisoning him.\nAva's husband has sent armed rogues to hunt her down, and the only place she still feels safe is the Capone estate of Alpha Alexander, King of the Black Werewolves, whose name alone makes other wolves shiver. She gets there bleeding badly, her arms and legs covered in wolf scratches, and all she asks for is a job as a maid. The job she gets is taming Leo, Alexander's adorable and dangerous little pup, whose wild bloodline makes him bite anyone who comes near. Except Leo doesn't bite Ava. He sticks to her like a kitten. Ava has no wolf of her own, but she can hear what Leo is thinking, and once she pulls a sharp splinter out of his mouth he tells her the truth. Someone has been poisoning him, and it's his own grandmother. Ava can only earn her freedom by curing the Young Master. But the Head Nanny who pretends to look after Leo is secretly working with his grandmother, and she can't stand how close Ava is getting to him.",
    # 7.0M     Sexting My Pucking Nemesis
    # FACTS: In Sexting My Pucking Nemesis, Ethan Miller may be a nerd, but he’s also the hockey player his
    # FACTS: teammates would rather avoid. He has never been good at respecting boundaries. Then he does the one
    # FACTS: thing his captain hates most: he publicly asks out Captain Hunter Kennedy’s younger sister, Hayley.
    # FACTS: For Hunter, few things could be more infuriating than watching the man he secretly wants chase after
    # FACTS: his sister. When he realizes Hayley plans to answer Ethan’s message, Hunter confiscates her phone.
    # FACTS: Ethan, using the username “Bad Boy,” sends Hayley a sexy text in the hope of winning her heart. What
    # FACTS: Ethan doesn’t know is that Hunter is the one answering those messages. Pretending to be Hayley,
    # FACTS: Hunter plays along with Ethan’s provocative texts and soon gets carried away. What begins as a trick
    # FACTS: turns into a private sexting relationship with Ethan—except Ethan has no idea who is really on the
    # FACTS: other side. As more people become involved, keeping the secret becomes harder. Can Hunter, Ethan’s
    # FACTS: biggest bully and hockey captain, pull him away from Hayley? Or will Ethan keep chasing the girl he
    # FACTS: thinks he wants without ever discovering who has truly captured his attention? Characters Ethan
    # FACTS: Miller Ethan Miller is a hockey player who loves learning and serves as one of the main male
    # FACTS: characters. He believes he’s straight and has his eyes on Hayley. Without realizing it, however, he
    # FACTS: ends up sexting her older brother—who also happens to be his nemesis. Hunter Kennedy Hunter Kennedy
    # FACTS: is the good-looking hockey captain and the second main male character. He is Hayley’s protective
    # FACTS: older brother and Ethan’s biggest bully. Beneath their rivalry, Hunter has had his eye on Ethan for
    # FACTS: a long time. Hayley Kennedy Hayley Kennedy is a supporting character and Ethan’s original love
    # FACTS: interest. She has a reputation for acting out of reach and is often accompanied by two other
    # FACTS: cheerleaders. Her phone unknowingly becomes the starting point of Ethan and Hunter’s secret
    # FACTS: connection. Trent Trent is the villain who considers himself Hunter’s best friend. He reacts badly
    # FACTS: when rumors and scandals involving Hunter and Ethan begin to surface. Their growing connection
    # FACTS: threatens the place Trent believes he holds in Hunter’s life.
    # FACTS: https://www.reelshort.com/movie/sexting-my-pucking-nemesis-6ab3ba913eb244b17d031ed1
    'sexting-my-pucking-nemesis':
        "He's sexting the captain's sister. Except the captain is the one texting back.\nEthan Miller plays hockey, he's a total nerd who loves to learn, and he's the guy his teammates would rather steer clear of. He's never been great with boundaries, so he asks out Hayley, the younger sister of captain Hunter Kennedy, in front of everyone. Hunter is Ethan's biggest bully, and he's furious, and not only because she's his sister: he's secretly wanted Ethan for ages. When Hayley looks ready to reply, Hunter takes her phone. So when Ethan, going by Bad Boy, sends her a flirty, sexy message, it's Hunter who answers as Hayley. It starts as a trick, then Hunter gets carried away, and soon they're sexting in private while Ethan, who's sure he's straight, has no clue who he's really talking to. Then more people get pulled in, including Trent, who sees himself as Hunter's best friend and hates the rumors starting to spread. How long can Hunter keep his secret?",
    # 5.1M     Reborn to Claim My Alpha King
    # FACTS: Kael raised Selene like a rose for eighteen years and never once let a thorn touch her — never dared
    # FACTS: to mark her, because everything he treasures gets taken. On the night of her eighteenth birthday,
    # FACTS: she tore their mate bond apart in front of the entire pack so she could run to Damian. It nearly
    # FACTS: killed her. But in the end, Damian killed her. She was never his love, only the blade he planned to
    # FACTS: gut Kael with. And when she died, her soul didn't leave. She watched Kael go through her enemies
    # FACTS: like a slaughter, then walk to her grave and follow her into the dark. Now she's reborn. This time,
    # FACTS: she isn't running anywhere. She will love Kael and take revenge on Damian.
    # FACTS: https://www.reelshort.com/movie/reborn-to-claim-my-alpha-king-6ab9e49dc7142fa1b005d0d7
    'reborn-to-claim-my-alpha-king':
        "She broke their mate bond for another man. That man killed her.\nFor eighteen years Kael raised Selene and kept every hurt away from her, and he never marked her, because anything he loves ends up taken from him. Then on her eighteenth birthday, in front of the whole pack, she rips their mate bond apart to run off with Damian. Breaking it almost kills her. Damian finishes the job. He never loved her, she was only ever the weapon he meant to use on Kael. After she dies her soul stays behind, and she watches Kael tear through every enemy she had, then visit her graveside and follow her into death. Now Selene is reborn, and she's done running. She's going to love Kael, and she's going to make Damian pay.",
    # 4.5M     The Campus King's Hidden Obsession
    # FACTS: Ella's boyfriend Kyle kisses freshman Nina in a truth-or-dare game and tells her not to be a sore
    # FACTS: loser — so she quietly unfollows him. When the next dare lands on campus golden boy Owen Blackwood,
    # FACTS: he asks Ella to try him, and she takes his hand. What she thinks is one night of spite is the night
    # FACTS: Owen has waited three years for. Kyle tries everything to win her back and fails at every turn; when
    # FACTS: Nina attacks Ella online, Owen's prepared rebuttal destroys her. Owen takes Kyle's punch without
    # FACTS: dodging, and Ella tells Kyle the truth: Owen is better in every way that counts.
    # FACTS: https://www.reelshort.com/movie/the-campus-king-s-hidden-obsession-6abb71a6cfdea42e2f0f5b33
    'the-campus-king-s-hidden-obsession':
        "Her boyfriend kissed another girl on a dare. So she took the golden boy's hand.\nIn a game of truth or dare, Ella's boyfriend Kyle kisses Nina, a freshman, and then acts like Ella is a sore loser for minding. She doesn't make a scene. She just quietly unfollows him. Then the next dare goes to Owen Blackwood, the golden boy of the whole campus, and he asks Ella to give him a try. She puts her hand in his. To her it's one night to get back at Kyle. To Owen it's the night he's been waiting three years for. Kyle throws everything he has at getting her back, and none of it works. When Nina goes after Ella online, Owen already has his answer ready, and it finishes her. When Kyle swings at him, Owen doesn't even dodge the punch. And Ella spells it out for Kyle. Owen beats him in every way that matters.",
    # 4.0M     Seducing My Sister's Husband Behind Her Back
    # FACTS: As William and Fiona's relationship begins to crumble, Fiona's younger brother, Leon, sees his
    # FACTS: chance to make a move. He urges the ever-honorable William to get back at Fiona by cheating, and
    # FACTS: even offers to help him "practice." William still sees Leon as the boy he's looked after since
    # FACTS: childhood, unaware that Leon has spent years plotting to make him his. But as they cross one
    # FACTS: boundary after another, William is horrified to realize he's falling for Leon. Consumed by guilt, he
    # FACTS: tries to walk away, only for Leon to chase after him and finally confess the love he's kept buried
    # FACTS: for ten years.
    # FACTS: https://www.reelshort.com/movie/seducing-my-sister-s-husband-behind-her-back-6abd01b9dad9e551c60fad59
    'seducing-my-sister-s-husband-behind-her-back':
        "He's loved his sister's husband for ten years.\nWilliam and Fiona's marriage is coming apart, and Leon, Fiona's younger brother, sees his opening. William has always been the honorable one, so Leon pushes him to cheat on Fiona to get even with her, and says he will even help him practice first. William has looked after Leon since Leon was a little boy and still sees him that way. He has no idea Leon has been scheming for years to make William his. They cross one line, then another, and William is horrified to find he's falling for his wife's brother. Eaten up with guilt, he tries to break it off. Leon goes after him and finally says what he's kept hidden for a decade: he's in love with William.",
    # 3.3M     Daddy, We’re Secret Billionaires
    # FACTS: Seven-year-old genius Daisy concealed her identity as the heir to a top-tier wealthy family. While
    # FACTS: secretly manipulating the stock market and controlling a large conglomerate, she quietly supported
    # FACTS: her ordinary father, Richard. At bidding conferences, at school, and at class reunions, she
    # FACTS: repeatedly humiliated the rich kids who looked down on Richard, step by step helping her father get
    # FACTS: to know Lila, a woman of quality. In the end, she publicly revealed her hidden identity as the
    # FACTS: wealthiest person in the shadows, shaking up the entire Los Angeles business world.
    # FACTS: https://www.reelshort.com/movie/daddy-we-re-secret-billionaires-6ab4b9cdc4ba90cc8d07abda
    'daddy-we-re-secret-billionaires':
        "She's seven, she's a genius, and she secretly runs a conglomerate.\nDaisy is seven years old, and she's hiding who she really is: the heir to one of the very richest families there is. Behind the scenes she moves the stock market and runs a huge conglomerate, and the whole time she's quietly backing her ordinary dad, Richard. Every time the rich kids look down on him, at bidding conferences, at school, at class reunions, Daisy makes them regret it, one humiliation at a time. Along the way she gives Richard his chance with Lila, a woman who's truly worth his time. And when she finally stands up in public and reveals that she's the richest person nobody knew about, the whole Los Angeles business world is shaken.",
    # 2.6M     Found a True Love on My Bachelor Party
    # FACTS: The night before her wedding, Astrid's fiancé, Marco, makes a shocking proposal: they can both have
    # FACTS: one night with anyone they want. He thinks she'll never find someone better. Instead, Astrid walks
    # FACTS: straight to the man she loved seven years ago—Brennan, her fiancé's best friend and the only man she
    # FACTS: never forgot. What starts as one reckless night changes everything. By morning, Brennan begs her not
    # FACTS: to marry Marco. She says yes—and they go straight to the County Clerk's Office to get married. But
    # FACTS: Marco soon comes looking for his bride, only to discover that Astrid is already Brennan's wife. Then
    # FACTS: the truth about their seven-year separation comes out: Brennan's mother once offered Astrid ten
    # FACTS: million dollars to leave him forever.
    # FACTS: https://www.reelshort.com/movie/found-a-true-love-on-my-bachelor-party-6ac7ae4da506710b4d068a0b
    'found-a-true-love-on-my-bachelor-party':
        "Her fiance said they could each have one night with anyone. She picked his best friend.\nThe night before their wedding, Marco makes Astrid a shocking offer: they each get one night with whoever they want. He's sure she'll never find anyone better than him. Astrid goes straight to Brennan, Marco's best friend, the man she was in love with seven years ago and never managed to forget. One reckless night changes everything, and by morning Brennan is begging her to call off the wedding. She agrees, and they head straight for the County Clerk's Office and get married there. When Marco shows up to collect his bride, she's already married to Brennan. That's when the reason they spent seven years apart finally comes out. Back then, Brennan's mother put ten million dollars in front of Astrid to make her leave him for good.",
    # 2.5M     She Stole My EpiPen. My Family Made Her Pay
    # FACTS: Madison, my boyfriend's childhood sweetheart, learns I'm allergic to peanuts—then hides peanut
    # FACTS: extract in every party appetizer. When my airway clamps shut, I reach for my EpiPen and find it's
    # FACTS: been switched to a candy toy. My boyfriend calls me a drama queen. I stop explaining and press my
    # FACTS: watch's hidden SOS button, alerting my family's private security team.
    # FACTS: https://www.reelshort.com/movie/she-stole-my-epipen-my-family-made-her-pay-6ac7ae12978a8f90e207bf49
    'she-stole-my-epipen-my-family-made-her-pay':
        "Her boyfriend's childhood sweetheart swapped her EpiPen for a candy toy.\nMadison was her boyfriend's sweetheart growing up, and when she learns that his girlfriend is allergic to peanuts, she slips peanut extract into every appetizer at the party. Her throat starts to close, she reaches for her EpiPen, and it's gone. In its place is a toy made of candy. Her boyfriend just calls her a drama queen. So she stops trying to explain herself to him. She presses a hidden SOS button on her watch instead, and her family's private security team is on its way. Her family is coming, and they're going to make Madison pay.",
    # 2.3M     I Sexted the Hockey Captain
    # FACTS: Tilly, an ordinary high school student, is publicly humiliated after her crush on a popular hockey
    # FACTS: player is exposed. Devastated, she musters up the courage to send him nudes anonymously in hopes of
    # FACTS: catching his eye. But she accidentally sends the pics to Oliver instead, the captain of the hockey
    # FACTS: team who always teases her. What will happen between them?
    # FACTS: https://www.reelshort.com/movie/i-sexted-the-hockey-captain-6abc7af7147958ea14077eeb
    'i-sexted-the-hockey-captain':
        "She meant to send the photos to her crush. The hockey captain got them instead.\nTilly is an ordinary high school student, until her crush on one of the popular hockey players comes out and she's humiliated in front of everyone. Heartbroken, she works up the nerve to send him some private photos without her name on them, hoping he'll finally notice her. Except they don't go to him. They go to Oliver, the hockey team's captain and the one boy who never stops teasing her. So what happens between Tilly and Oliver now?",
    # 2.0M     The Beasts Kill for Me
    # FACTS: Dragged off to the Beast Wars, Ivar returns ten years later with no memory of his family's faces,
    # FACTS: but the ability to control the very beasts he was fighting. Disguised as a beggar, he uses the
    # FACTS: beasts to free his enslaved family and destroy the cruel nobles who tore them apart.
    # FACTS: https://www.reelshort.com/movie/the-beasts-kill-for-me-6abb68092027710dc506e960
    'the-beasts-kill-for-me':
        "He was sent to fight the beasts. He came back commanding them.\nIvar was taken away to fight in the Beast Wars, and it's ten years before he makes it home. By then he can't even remember his own family's faces. What he brings back instead is the power to command the same beasts he spent all those years fighting. His family has been enslaved, and cruel nobles are the ones who tore them apart. So Ivar dresses up as a beggar and lets the beasts do the work. First he sets his family free, and then he turns the beasts on the nobles who broke them.",
    # 1.8M     Maria the Little Lucky Star
    # FACTS: Maria, a lop-eared rabbit orphan, grew up in a boar-folk village. Because whatever she said always
    # FACTS: came true, the villagers saw her as a cursed child and drove her into a cowshed to live alone.
    # FACTS: Duchess Ethelyn stumbled upon Maria while lost, and Maria's blessing unexpectedly cured Ethelyn of a
    # FACTS: chronic illness she'd suffered for years. Ethelyn brought Maria back to Avalon Ducal Manor, and
    # FACTS: Maria's arrival filled the lifeless castle with laughter again. With her power, she healed the
    # FACTS: crippled legs of the third young master, Cyrus, and slowly thawed the frozen heart of Duke Regulus.
    # FACTS: Yet Maria foresaw a conspiracy against the manor—Regulus would be assassinated, Ethelyn would die a
    # FACTS: horrible death, Cyrus would be crushed, and the entire manor would be reduced to ashes. How will
    # FACTS: Maria rewrite it all?
    # FACTS: https://www.reelshort.com/movie/maria-the-little-lucky-star-6abcbeb1b68f8046430a740a
    'maria-the-little-lucky-star':
        "Whatever this little rabbit girl says comes true.\nMaria is an orphan, a little rabbit with floppy ears, growing up in a village of boar folk. Everything she says comes true, so the villagers decide she's a cursed child and make her live alone in a cowshed. Then Duchess Ethelyn gets lost and finds her there, and one blessing from Maria ends an illness Ethelyn has suffered with for years. Ethelyn takes her home to Avalon Ducal Manor, a cold, empty castle, and with Maria in it there's laughter in the halls again. She heals the legs of Cyrus, the third young master, who was crippled, and little by little she thaws out Duke Regulus, whose heart had turned to ice. But Maria can see what's coming. There's a plot against the manor. Regulus will be assassinated, Ethelyn will die a terrible death, Cyrus will be crushed, and the whole manor will burn to ashes. How can one little girl change all of it?",
    # 1.4M     I Slept With My Ex's Father
    # FACTS: Olivia, 21, gets dumped when Lucas claims his adoptive father disapproves of her. Drunk and
    # FACTS: desperate to win him back, she knocks on the wrong door—and spends the night with Dylan Hill, the
    # FACTS: 32-year-old CEO. Lucas moves on within days, but Dylan keeps appearing: at her internship, at her
    # FACTS: hospital bedside, between her and every bad date. He's cold, controlled, and impossible to
    # FACTS: read—until he isn't. From one wrong door to a ring in Florida, this is the love story her ex will
    # FACTS: never forgive.
    # FACTS: https://www.reelshort.com/movie/i-slept-with-my-ex-s-father-6ac73c314b4fca595707ba13
    'i-slept-with-my-ex-s-father':
        "She went to win back her ex. She ended up in bed with his father.\nOlivia is twenty one when Lucas dumps her, claiming his adoptive father doesn't approve of her. Drunk and set on getting him back, she turns up at the wrong door, and by morning she's spent the night with Dylan Hill, a thirty two year old CEO. And Dylan is Lucas's adoptive father. Lucas has moved on within days. Dylan, though, keeps turning up: at her internship, beside her hospital bed, and in the way of every bad date she goes on. He's cold, always in control and impossible to read, until suddenly he isn't. One wrong door leads all the way to a ring in Florida, and it's a love story Lucas will never forgive.",
    # 1.3M     My Sister Got the Party, I Got the Scholarship
    # FACTS: Twin sister Ollie Campbell spent eighteen years as the family green leaf while porcelain-pretty
    # FACTS: Willow took the dresses, the MacBook, and the praise. Beck forgot her mango allergy for Willow's
    # FACTS: iced drinks; Hayes spent months of pay on Willow and blamed Ollie. On application night, they
    # FACTS: steered Willow to Stanford and Ollie to community college—never asking about her 1580 SAT. Beck
    # FACTS: dropped MIT for Willow; Ollie quietly chose UT Austin, 2,400 km away. When Mom stole her savings for
    # FACTS: Willow's graduation party, Ollie left. A reporter exposed her National Merit scholarships too late.
    # FACTS: In Texas, she rebuilt herself—honors, papers, NSF work—and refused Dad's regret, Hayes's scolding,
    # FACTS: and Beck's rain-soaked plea. Years later, she turns away their money pleas and harassment. At
    # FACTS: graduation, she smiles for the camera and toasts, "To the future." Willow got the party. Ollie got
    # FACTS: the scholarship—and a life that is finally hers. Favoritism breeds no loyalty; silence never buys
    # FACTS: being seen. An underestimated life can still bloom.
    # FACTS: https://www.reelshort.com/movie/my-sister-got-the-party-i-got-the-scholarship-6ac9f405c750922fe70106b9
    'my-sister-got-the-party-i-got-the-scholarship':
        "Her mom stole her savings to pay for her twin's party. So she left.\nFor eighteen years Ollie Campbell was the twin nobody looked at, while pretty Willow got the dresses, the MacBook and every bit of the praise. Beck forgot all about Ollie's mango allergy when Willow wanted iced drinks, and Hayes spent months of wages on Willow and then put the blame on Ollie. When it was time to apply to college, the family pointed Willow toward Stanford and Ollie toward community college, and nobody asked about her 1580 on the SAT. Beck gave up MIT for Willow. Ollie quietly picked UT Austin, 2,400 kilometers away. Then Mom took Ollie's savings to pay for Willow's graduation party, and Ollie walked out. By the time a reporter revealed she'd won National Merit scholarships, it was too late to matter. In Texas she builds a whole new life with honors, academic papers and NSF work, and she says no to Dad's regret, to Hayes's lectures and to Beck begging her in the rain. Years later they come asking for money and won't leave her alone, and she still turns them away. At her graduation she smiles into the camera and raises a glass to what comes next. Her twin got the party. Ollie got a life that's finally her own.",
    # 934.9K   I Traded Three Beasts for One Wolf King
    # FACTS: Eldest princess Elsa keeps three fox beastmen—until they see her sister Luna. She trades all three
    # FACTS: for Luna's untouchable cold-faced werewolf. She wanted a servant; yet he bows only to her, and once
    # FACTS: he bites, won't let go. Forced to marry, she signs, schemes, and flees on her wedding day. Then the
    # FACTS: foxes kneel begging her back—but can't pass the gates. When the capital falls to chaos as Luna
    # FACTS: drains the treasury, Elsa returns with the mountain king. What she wants back was never just the
    # FACTS: throne.
    # FACTS: https://www.reelshort.com/movie/i-traded-three-beasts-for-one-wolf-king-6ad02c9a3d67475767005f2c
    'i-traded-three-beasts-for-one-wolf-king':
        "She traded three fox beastmen for one cold werewolf.\nElsa is the eldest princess, and she keeps three fox beastmen, right up until they lay eyes on her sister Luna. So she trades all three of them for Luna's werewolf, the cold faced one nobody can touch. Elsa only wanted a servant. Instead he bows to nobody but her, and once he bites, he doesn't let go. When she's forced into a marriage, she signs, makes her plans and runs off on the day of the wedding. After that the foxes come back on their knees begging her to take them again, but they can't even get through the gates. In the capital Luna drains the treasury dry and everything falls into chaos, and Elsa comes home with the mountain king. The throne was never the only thing she came back for.",
    # 900.1K   He Left Me for a Senator's Daughter
    # FACTS: Inez hid her four-star general father and loved Lachlan for five years—until she found his prenup
    # FACTS: with Senator's daughter Sutton and saw him shield Sutton first in a crash. She left, took an NSC
    # FACTS: post, and met Lucian Sinclair. When Sutton's smear campaign backfired, Inez exposed the truth and
    # FACTS: both families fell. Lachlan begged mercy; she refused and began again with Lucian.
    # FACTS: https://www.reelshort.com/movie/he-left-me-for-a-senator-s-daughter-6ac99c5d1eb02e828b0ef0b5
    'he-left-me-for-a-senator-s-daughter':
        "Five years together, and he had a prenup with someone else.\nInez loved Lachlan for five years and kept it to herself that her father is a four star general. Then she finds his prenup with Sutton, a Senator's daughter, and when there's a crash she watches him protect Sutton before her. So Inez leaves. She takes a post at the NSC and meets Lucian Sinclair. Sutton's smear campaign blows up in her own face, and Inez lays out the truth for everyone to see. Both families go down. Lachlan begs her for mercy. She doesn't give him any, and starts her life over with Lucian.",
    # 760.7K   W・KING
    # FACTS: Reborn with a chance at retribution, Sun vows revenge—but the threads of fate binding him to Liu Che
    # FACTS: refuse to sever. Amidst ruthless power struggles and shadowy conspiracies, they manipulate each
    # FACTS: other even as they burn with irresistible attraction. In a tempest of love and hatred, they rage
    # FACTS: against destiny’s grip, only to find themselves inexorably drawn back to the bond they cannot
    # FACTS: escape...
    # FACTS: https://www.reelshort.com/movie/w-king-67c672350da5ecbdcc0f90c0
    'w-king':
        "Reborn for revenge, and still bound to the one person he can't escape.\nSun has been reborn, and this time he's going to get his revenge. The trouble is that fate has tied him to Liu Che, and nothing he does will cut that tie. In the middle of brutal fights for power and plots hidden in the shadows, they use each other at every turn, and the whole time the pull between them keeps burning hotter. Caught between love and hate, they fight their destiny with everything they have, and every time it drags them back to each other. Can either of them ever really walk away?",
    # 653.9K   The Dragon King 's Bride
    # FACTS: Celestia, the goddess, was drugged and betrayed by her stepsister Mortis. She spent one fateful
    # FACTS: night with Dragon King Azriel and later gave birth to a pair of dragon-god twins. Coveting the
    # FACTS: Dragon Queen’s throne, Mortis stole their baby daughter Joey, raised her as her own, and plotted to
    # FACTS: execute Celestia. Fleeing to the barren wasteland, Celestia lived in anonymity for five years with
    # FACTS: her son Aion. Born with an incomplete divine core, Aion could only survive with his biological
    # FACTS: father’s essence. To save her son, Celestia returns to the divine realm. There she unexpectedly
    # FACTS: meets the Dragon King’s “daughter” Joey and feels an instinctive bond with the child. Azriel senses
    # FACTS: an inexplicable familiarity with Celestia and takes her and her son into the dragon palace. The
    # FACTS: story culminates in a grand wedding between Celestia and Azriel. The Dragon King swears to love only
    # FACTS: her for eternity, as their twin children witness their parents finally reunite.
    # FACTS: https://www.reelshort.com/movie/the-dragon-king-s-bride-6ab9c22a20b8ff5a830ffba7
    'the-dragon-king-s-bride':
        "Her stepsister stole her baby girl to become Dragon Queen.\nCelestia is a goddess, and her stepsister Mortis drugs her and betrays her. She spends one night with Azriel, the Dragon King, and later has twins, a dragon god son and daughter. Mortis wants the Dragon Queen's throne for herself, so she steals the baby girl, Joey, raises her as her own, and schemes to have Celestia executed. Celestia escapes to the barren wasteland with her son Aion, and for five years she lives there with nobody knowing who she is. But Aion was born with a divine core that isn't whole, and the only thing that can keep him alive is his real father's essence. So Celestia goes back to the divine realm to save him. There she meets Joey, the little girl everyone believes is the Dragon King's daughter, and feels drawn to her right away. Azriel can't explain why Celestia feels so familiar, and he brings her and Aion into the dragon palace. It all ends in a grand wedding, with the Dragon King swearing she's the only one he'll ever love, and both twins there to watch their parents finally come back together.",
}

SOURCES = {
    'never-enjoyed-divorce-like-this': ('platform', 'https://www.reelshort.com/movie/never-enjoyed-divorce-like-this-66da5b2863f055aeb90e1bf9'),
    'divorced-i-married-the-mafioso': ('platform', 'https://www.reelshort.com/movie/divorced-i-married-the-mafioso-6ab6084357304459cf0cfcc5'),
    'hearing-the-little-alpha-s-mind-saved-my-life': ('platform', 'https://www.reelshort.com/movie/hearing-the-little-alpha-s-mind-saved-my-life-6ab0966c2eac8bc8bb0d3e4d'),
    'sexting-my-pucking-nemesis': ('platform', 'https://www.reelshort.com/movie/sexting-my-pucking-nemesis-6ab3ba913eb244b17d031ed1'),
    'reborn-to-claim-my-alpha-king': ('platform', 'https://www.reelshort.com/movie/reborn-to-claim-my-alpha-king-6ab9e49dc7142fa1b005d0d7'),
    'the-campus-king-s-hidden-obsession': ('platform', 'https://www.reelshort.com/movie/the-campus-king-s-hidden-obsession-6abb71a6cfdea42e2f0f5b33'),
    'seducing-my-sister-s-husband-behind-her-back': ('platform', 'https://www.reelshort.com/movie/seducing-my-sister-s-husband-behind-her-back-6abd01b9dad9e551c60fad59'),
    'daddy-we-re-secret-billionaires': ('platform', 'https://www.reelshort.com/movie/daddy-we-re-secret-billionaires-6ab4b9cdc4ba90cc8d07abda'),
    'found-a-true-love-on-my-bachelor-party': ('platform', 'https://www.reelshort.com/movie/found-a-true-love-on-my-bachelor-party-6ac7ae4da506710b4d068a0b'),
    'she-stole-my-epipen-my-family-made-her-pay': ('platform', 'https://www.reelshort.com/movie/she-stole-my-epipen-my-family-made-her-pay-6ac7ae12978a8f90e207bf49'),
    'i-sexted-the-hockey-captain': ('platform', 'https://www.reelshort.com/movie/i-sexted-the-hockey-captain-6abc7af7147958ea14077eeb'),
    'the-beasts-kill-for-me': ('platform', 'https://www.reelshort.com/movie/the-beasts-kill-for-me-6abb68092027710dc506e960'),
    'maria-the-little-lucky-star': ('platform', 'https://www.reelshort.com/movie/maria-the-little-lucky-star-6abcbeb1b68f8046430a740a'),
    'i-slept-with-my-ex-s-father': ('platform', 'https://www.reelshort.com/movie/i-slept-with-my-ex-s-father-6ac73c314b4fca595707ba13'),
    'my-sister-got-the-party-i-got-the-scholarship': ('platform', 'https://www.reelshort.com/movie/my-sister-got-the-party-i-got-the-scholarship-6ac9f405c750922fe70106b9'),
    'i-traded-three-beasts-for-one-wolf-king': ('platform', 'https://www.reelshort.com/movie/i-traded-three-beasts-for-one-wolf-king-6ad02c9a3d67475767005f2c'),
    'he-left-me-for-a-senator-s-daughter': ('platform', 'https://www.reelshort.com/movie/he-left-me-for-a-senator-s-daughter-6ac99c5d1eb02e828b0ef0b5'),
    'w-king': ('platform', 'https://www.reelshort.com/movie/w-king-67c672350da5ecbdcc0f90c0'),
    'the-dragon-king-s-bride': ('platform', 'https://www.reelshort.com/movie/the-dragon-king-s-bride-6ab9c22a20b8ff5a830ffba7'),
}

FACTS = {  # the published synopsis each caption was written from
    'never-enjoyed-divorce-like-this': 'She is a wealthy heiress and a renowned fashion designer who gave up her career for her husband. However, his coldness and distrust broke her heart. After their divorce, she met a handsome, wealthy, and caring new man who helped her slowly forget the pain of her past. She thought she had found her true love, but little did she know that he was only after her money and power. When she discovered the deception and left him, he realized he had truly fallen for her. At the same time, her ex-husband wanted to reconcile. Who will she choose?',
    'divorced-i-married-the-mafioso': "Humiliated, divorced and broke, orphan Nina applies to be the step-mom for hire of Mafia Don Leon Marconi, wins little Gio over with a Spider-Man doll, and signs a marriage contract. His tenderness eases her depression, and when he names her his wife at a gala, Easton's family collapses. Drug-addled Easton kidnaps Nina and Gio; Leon drives him off, they marry for real, and Gio proves to be his sister's son. Carmen's revenge fails as Nina gives birth to Dahlia, and Easton dies by his own bomb.",
    'hearing-the-little-alpha-s-mind-saved-my-life': 'For Ava, Godfather Alexander’s Capone estate is the only safe place left in Hearing The Little Alpha’s Mind Saved My Life. At least, that’s what she believes as she desperately tries to stay inside. Beyond the estate, her husband has sent armed rogues after her, and every one of them is ready to tear her apart. When Ava first reaches the estate, wolf scratches cover her arms and legs, and she is bleeding badly. At first, Ava only hopes to find work as one of the maids. The job is far from easy. She is expected to tame Alexander’s cute but dangerous little pup, Leo. His raging bloodline can make him bite just about anyone—and anything—that gets too close. Something about Leo doesn’t make sense. Although he is dangerous around everyone else, he clings to Ava like a soft kitten. After she removes a nasty, sharp splinter from his mouth, she begins to discover what has really been happening to him. Through his thoughts, Leo tells Ava that his grandmother has been poisoning him. If Ava wants to earn her freedom, she must first find a way to cure the Young Master. Characters Ava Ava is the wolfless girl and main female character of Hearing The Little Alpha’s Mind Saved My Life. She possesses the unusual ability to hear Young Master Leo’s thoughts. Her connection with Leo catches Alexander’s attention and makes her the target of the Head Nanny’s jealousy. Alpha Alexander Alpha Alexander is the main male character and the feared King of the Black Werewolves. Other werewolves shiver at the sound of his name. He takes an interest in Ava after seeing how easily she can soothe Young Master Leo. Young Master Leo Young Master Leo is Alpha Alexander’s cute but dangerous little pup. His behavior is shaped by his raging bloodline and the mistreatment he suffers from his grandmother. Despite his aggression toward others, he quickly becomes attached to Ava. Head Nanny The Head Nanny is a minor villain in the series. She pretends to care for Young Master Leo while secretly conspiring with his grandmother. Ava’s growing connection with Leo also makes the Head Nanny jealous.',
    'sexting-my-pucking-nemesis': 'In Sexting My Pucking Nemesis, Ethan Miller may be a nerd, but he’s also the hockey player his teammates would rather avoid. He has never been good at respecting boundaries. Then he does the one thing his captain hates most: he publicly asks out Captain Hunter Kennedy’s younger sister, Hayley. For Hunter, few things could be more infuriating than watching the man he secretly wants chase after his sister. When he realizes Hayley plans to answer Ethan’s message, Hunter confiscates her phone. Ethan, using the username “Bad Boy,” sends Hayley a sexy text in the hope of winning her heart. What Ethan doesn’t know is that Hunter is the one answering those messages. Pretending to be Hayley, Hunter plays along with Ethan’s provocative texts and soon gets carried away. What begins as a trick turns into a private sexting relationship with Ethan—except Ethan has no idea who is really on the other side. As more people become involved, keeping the secret becomes harder. Can Hunter, Ethan’s biggest bully and hockey captain, pull him away from Hayley? Or will Ethan keep chasing the girl he thinks he wants without ever discovering who has truly captured his attention? Characters Ethan Miller Ethan Miller is a hockey player who loves learning and serves as one of the main male characters. He believes he’s straight and has his eyes on Hayley. Without realizing it, however, he ends up sexting her older brother—who also happens to be his nemesis. Hunter Kennedy Hunter Kennedy is the good-looking hockey captain and the second main male character. He is Hayley’s protective older brother and Ethan’s biggest bully. Beneath their rivalry, Hunter has had his eye on Ethan for a long time. Hayley Kennedy Hayley Kennedy is a supporting character and Ethan’s original love interest. She has a reputation for acting out of reach and is often accompanied by two other cheerleaders. Her phone unknowingly becomes the starting point of Ethan and Hunter’s secret connection. Trent Trent is the villain who considers himself Hunter’s best friend. He reacts badly when rumors and scandals involving Hunter and Ethan begin to surface. Their growing connection threatens the place Trent believes he holds in Hunter’s life.',
    'reborn-to-claim-my-alpha-king': "Kael raised Selene like a rose for eighteen years and never once let a thorn touch her — never dared to mark her, because everything he treasures gets taken. On the night of her eighteenth birthday, she tore their mate bond apart in front of the entire pack so she could run to Damian. It nearly killed her. But in the end, Damian killed her. She was never his love, only the blade he planned to gut Kael with. And when she died, her soul didn't leave. She watched Kael go through her enemies like a slaughter, then walk to her grave and follow her into the dark. Now she's reborn. This time, she isn't running anywhere. She will love Kael and take revenge on Damian.",
    'the-campus-king-s-hidden-obsession': "Ella's boyfriend Kyle kisses freshman Nina in a truth-or-dare game and tells her not to be a sore loser — so she quietly unfollows him. When the next dare lands on campus golden boy Owen Blackwood, he asks Ella to try him, and she takes his hand. What she thinks is one night of spite is the night Owen has waited three years for. Kyle tries everything to win her back and fails at every turn; when Nina attacks Ella online, Owen's prepared rebuttal destroys her. Owen takes Kyle's punch without dodging, and Ella tells Kyle the truth: Owen is better in every way that counts.",
    'seducing-my-sister-s-husband-behind-her-back': 'As William and Fiona\'s relationship begins to crumble, Fiona\'s younger brother, Leon, sees his chance to make a move. He urges the ever-honorable William to get back at Fiona by cheating, and even offers to help him "practice." William still sees Leon as the boy he\'s looked after since childhood, unaware that Leon has spent years plotting to make him his. But as they cross one boundary after another, William is horrified to realize he\'s falling for Leon. Consumed by guilt, he tries to walk away, only for Leon to chase after him and finally confess the love he\'s kept buried for ten years.',
    'daddy-we-re-secret-billionaires': 'Seven-year-old genius Daisy concealed her identity as the heir to a top-tier wealthy family. While secretly manipulating the stock market and controlling a large conglomerate, she quietly supported her ordinary father, Richard. At bidding conferences, at school, and at class reunions, she repeatedly humiliated the rich kids who looked down on Richard, step by step helping her father get to know Lila, a woman of quality. In the end, she publicly revealed her hidden identity as the wealthiest person in the shadows, shaking up the entire Los Angeles business world.',
    'found-a-true-love-on-my-bachelor-party': "The night before her wedding, Astrid's fiancé, Marco, makes a shocking proposal: they can both have one night with anyone they want. He thinks she'll never find someone better. Instead, Astrid walks straight to the man she loved seven years ago—Brennan, her fiancé's best friend and the only man she never forgot. What starts as one reckless night changes everything. By morning, Brennan begs her not to marry Marco. She says yes—and they go straight to the County Clerk's Office to get married. But Marco soon comes looking for his bride, only to discover that Astrid is already Brennan's wife. Then the truth about their seven-year separation comes out: Brennan's mother once offered Astrid ten million dollars to leave him forever.",
    'she-stole-my-epipen-my-family-made-her-pay': "Madison, my boyfriend's childhood sweetheart, learns I'm allergic to peanuts—then hides peanut extract in every party appetizer. When my airway clamps shut, I reach for my EpiPen and find it's been switched to a candy toy. My boyfriend calls me a drama queen. I stop explaining and press my watch's hidden SOS button, alerting my family's private security team.",
    'i-sexted-the-hockey-captain': 'Tilly, an ordinary high school student, is publicly humiliated after her crush on a popular hockey player is exposed. Devastated, she musters up the courage to send him nudes anonymously in hopes of catching his eye. But she accidentally sends the pics to Oliver instead, the captain of the hockey team who always teases her. What will happen between them?',
    'the-beasts-kill-for-me': "Dragged off to the Beast Wars, Ivar returns ten years later with no memory of his family's faces, but the ability to control the very beasts he was fighting. Disguised as a beggar, he uses the beasts to free his enslaved family and destroy the cruel nobles who tore them apart.",
    'maria-the-little-lucky-star': "Maria, a lop-eared rabbit orphan, grew up in a boar-folk village. Because whatever she said always came true, the villagers saw her as a cursed child and drove her into a cowshed to live alone. Duchess Ethelyn stumbled upon Maria while lost, and Maria's blessing unexpectedly cured Ethelyn of a chronic illness she'd suffered for years. Ethelyn brought Maria back to Avalon Ducal Manor, and Maria's arrival filled the lifeless castle with laughter again. With her power, she healed the crippled legs of the third young master, Cyrus, and slowly thawed the frozen heart of Duke Regulus. Yet Maria foresaw a conspiracy against the manor—Regulus would be assassinated, Ethelyn would die a horrible death, Cyrus would be crushed, and the entire manor would be reduced to ashes. How will Maria rewrite it all?",
    'i-slept-with-my-ex-s-father': "Olivia, 21, gets dumped when Lucas claims his adoptive father disapproves of her. Drunk and desperate to win him back, she knocks on the wrong door—and spends the night with Dylan Hill, the 32-year-old CEO. Lucas moves on within days, but Dylan keeps appearing: at her internship, at her hospital bedside, between her and every bad date. He's cold, controlled, and impossible to read—until he isn't. From one wrong door to a ring in Florida, this is the love story her ex will never forgive.",
    'my-sister-got-the-party-i-got-the-scholarship': 'Twin sister Ollie Campbell spent eighteen years as the family green leaf while porcelain-pretty Willow took the dresses, the MacBook, and the praise. Beck forgot her mango allergy for Willow\'s iced drinks; Hayes spent months of pay on Willow and blamed Ollie. On application night, they steered Willow to Stanford and Ollie to community college—never asking about her 1580 SAT. Beck dropped MIT for Willow; Ollie quietly chose UT Austin, 2,400 km away. When Mom stole her savings for Willow\'s graduation party, Ollie left. A reporter exposed her National Merit scholarships too late. In Texas, she rebuilt herself—honors, papers, NSF work—and refused Dad\'s regret, Hayes\'s scolding, and Beck\'s rain-soaked plea. Years later, she turns away their money pleas and harassment. At graduation, she smiles for the camera and toasts, "To the future." Willow got the party. Ollie got the scholarship—and a life that is finally hers. Favoritism breeds no loyalty; silence never buys being seen. An underestimated life can still bloom.',
    'i-traded-three-beasts-for-one-wolf-king': "Eldest princess Elsa keeps three fox beastmen—until they see her sister Luna. She trades all three for Luna's untouchable cold-faced werewolf. She wanted a servant; yet he bows only to her, and once he bites, won't let go. Forced to marry, she signs, schemes, and flees on her wedding day. Then the foxes kneel begging her back—but can't pass the gates. When the capital falls to chaos as Luna drains the treasury, Elsa returns with the mountain king. What she wants back was never just the throne.",
    'he-left-me-for-a-senator-s-daughter': "Inez hid her four-star general father and loved Lachlan for five years—until she found his prenup with Senator's daughter Sutton and saw him shield Sutton first in a crash. She left, took an NSC post, and met Lucian Sinclair. When Sutton's smear campaign backfired, Inez exposed the truth and both families fell. Lachlan begged mercy; she refused and began again with Lucian.",
    'w-king': 'Reborn with a chance at retribution, Sun vows revenge—but the threads of fate binding him to Liu Che refuse to sever. Amidst ruthless power struggles and shadowy conspiracies, they manipulate each other even as they burn with irresistible attraction. In a tempest of love and hatred, they rage against destiny’s grip, only to find themselves inexorably drawn back to the bond they cannot escape...',
    'the-dragon-king-s-bride': 'Celestia, the goddess, was drugged and betrayed by her stepsister Mortis. She spent one fateful night with Dragon King Azriel and later gave birth to a pair of dragon-god twins. Coveting the Dragon Queen’s throne, Mortis stole their baby daughter Joey, raised her as her own, and plotted to execute Celestia. Fleeing to the barren wasteland, Celestia lived in anonymity for five years with her son Aion. Born with an incomplete divine core, Aion could only survive with his biological father’s essence. To save her son, Celestia returns to the divine realm. There she unexpectedly meets the Dragon King’s “daughter” Joey and feels an instinctive bond with the child. Azriel senses an inexplicable familiarity with Celestia and takes her and her son into the dragon palace. The story culminates in a grand wedding between Celestia and Azriel. The Dragon King swears to love only her for eternity, as their twin children witness their parents finally reunite.',
}
