# -*- coding: utf-8 -*-
"""September caption gap, first five for Cyan to calibrate the new writer.

62 caption gaps on main from the 3 and 13 Sep scrapes: 61 blanks and one old
one-line blurb, together 1.05B recorded plays. These are five of the blank entries.
This is only the first five by reach. No captions applied or approved.
Facts: linked ReelShort book ids, banked by the 25 Oct scrape. Live web fetch
was blocked on 26 Oct; these are saved platform sources, not a fresh read.
The cowboy source is short but contains the central story. Dragon King ends
with a question about the child; the caption preserves that uncertainty.

Unreviewed draft overlap: Caine, Dante and Cowboy also have 25 Sep drafts on
claude/available-tropes-coverage-8f0mvn, captions_2026_09_25_r0.py. Those never
went live or entered the current queue. These replacement drafts use the saved
25 Oct sources; none has a recorded Cyan approval. When migrating r0, keep one
entry per title and never overwrite a caption Cyan has since ticked or edited.
"""

BATCH_TAG = "September gap: first five"

CAPTIONS = {
    # FACTS: Orphaned Caine spent ten years of his life prioritizing his five mates in Rejecting My Five Female
    # FACTS: Mates. They were his foster father’s beloved daughters—spoiled, cherished, and fearless in their own
    # FACTS: ways. They became the anchor of his existence, and for so long, he thought one of them would become
    # FACTS: his fated mate. Everything changed when Seth, a notorious rogue, came onto the scene. Blinded by
    # FACTS: Seth’s lies, the five female mates turned against Caine, relentlessly humiliating him and constantly
    # FACTS: challenging his honor as the next-in-line alpha of the pack. Their treatment of Caine eventually
    # FACTS: became more than he could bear. Rather than stay and endure another humiliation, he left the pack
    # FACTS: and looked elsewhere for a future. His search took him to a foreign pack, where a marriage alliance
    # FACTS: brought him together with Princess Sylvia. He didn’t expect to fall for her so quickly, but he did.
    # FACTS: Caine thought leaving would put the worst behind him, but his life with Sylvia soon ran into
    # FACTS: trouble. One problem followed another, testing a relationship that had only just begun. Still, they
    # FACTS: refused to turn against each other and managed to get through it. For a brief moment, their future
    # FACTS: finally looked secure. That was until his five female mates crashed their wedding, demanding to
    # FACTS: settle the score and begging him to take them back. Would Caine accept their apology, or would it be
    # FACTS: the last time they ever brought up the past? Characters Caine Caine is the central character of
    # FACTS: Rejecting My Five Female Mates. He’s resilient, compassionate, and humble, always acting out of
    # FACTS: honor and always determined to fight for the truth. Enduring the hardships eventually pays off when
    # FACTS: he discovers a place where no one can doubt him again. Princess Sylvia Princess Sylvia is the
    # FACTS: reigning princess of the Silvermoon Pack. She’s mature, morally upright, and perceptive, exactly the
    # FACTS: kind of traits that match Caine’s personality. No wonder fate brought them together and allowed them
    # FACTS: to live happily ever after. Seth Seth is the notorious rogue who lies his way into the five female
    # FACTS: mates’ hearts. He creates stories to attack Caine’s character, believing they would be enough to get
    # FACTS: everything Caine has. His schemes fall through when Caine exposes him and he is punished for his
    # FACTS: sins.
    # 195.4M | Rejecting My Five Female Mates
    'rejecting-my-five-female-mates': "He leaves five women behind and finds the one who chooses him.\nFor ten years Caine has put his foster father's five daughters first, believing one of them will be his fated mate. Then a rogue called Seth wins them over with lies about him. The women Caine loves turn on him, humiliating him and questioning his right to become their Alpha. He finally walks away. An arranged marriage in another pack brings him Princess Sylvia, and what begins as an alliance becomes love. They weather the trouble that follows, only for his five former mates to interrupt their wedding. Now they want him back. But is an apology enough after everything they put him through?",

    # FACTS: In Fiancée's Betrayal Dante's Inferno movie, Dante Bosch returns home after 3 years in the Marine
    # FACTS: Raiders on a top secret mission, only to discover not only is his fiancée Lilith pregnant with his
    # FACTS: brother Virgil's baby, but Virgil has also spent all his money. To add insult to injury, his parents
    # FACTS: take Virgil's side. After suffering betrayals and humiliations, Dante exposes Virgil's lies with a
    # FACTS: video at his wedding.
    # 131.8M | Fiancée's Betrayal, Dante's Inferno
    'fiancee-s-betrayal-dante-s-inferno': "His brother got his fiancee pregnant. His parents took his brother's side.\nDante Bosch comes back from a secret Marine Raiders assignment to find that his family has betrayed him. He has been away for three years. In that time, Virgil has spent Dante's money and got his fiancee Lilith pregnant. His parents defend Virgil, leaving Dante to take the humiliation as well as the loss. But Dante has proof of what his brother has done, and a wedding gives him the chance to make everyone face it.",

    # FACTS: She came to town for a fresh start. Instead, Penelope Harris got pregnant by her ex’s powerful older
    # FACTS: brother, Knox Grant– the rugged cowboy who owns the ranch where she works. Now Penelope is caught
    # FACTS: between the man who would burn the world down for her and her ex, who wants to see her burn.
    # 61.6M | Keeping the Cowboy's Baby
    'keeping-the-cowboy-s-baby': "Her boss is her ex's older brother. Now she's pregnant.\nKnox Grant owns the ranch where Penelope Harris works. He's also the older brother of the man she used to date, and now he's the father of her baby. Penelope wanted a new beginning when she came to town. Instead, her past is close enough to threaten it. Knox will do anything for her, but his brother wants her hurt.",

    # FACTS: Marcus, a warlord who controls America’s economy and weapons, attends his brother Reed’s wedding.
    # FACTS: Mistaken for a delivery worker because of his mission uniform, he is looked down upon by the fiancée
    # FACTS: and her family. As a result, Marcus tries to set Reed up with the famous 'Three Goddesses of
    # FACTS: America,' but no one would believe him and they humiliate him. Reed defends him, so the fiancée’s
    # FACTS: family turns on Reed — she publicly dumps him to marry her ex instead, who has secretly been
    # FACTS: bankrupting Reed's business. Enraged, Marcus strikes back and humiliates them all. Only then do they
    # FACTS: learn his true identity—and regret it too late.
    # 46.1M | A Ruler in Disguise
    'a-ruler-in-disguise': "They picked the wrong brother to humiliate.\nReed stands up for Marcus at his wedding, and his fiancee's family turns on him too. They see Marcus in uniform and assume he makes deliveries. In fact, he's a warlord with control over America's economy and weapons. His offer to match Reed with one of the Three Goddesses of America only brings more humiliation. Then Reed's fiancee drops him in public for her ex, the very man secretly ruining Reed's business. Marcus has had enough. He's going to make them regret how they treated his brother, and their mistake about who he is.",

    # FACTS: In Accidentally His The Dragon King Won't Let Go movie, on a Blood Moon night, a drunken human girl
    # FACTS: steps into a cabin where the Dragon King lies in heat. After a steamy night with him, her belly
    # FACTS: suddenly swells, terrifying her into fleeing and leaving the loyal Dragon King to believe she has
    # FACTS: abandoned him. Days later, fate brings them together again, only for him to discover that she
    # FACTS: remembers nothing about him! But wait... is she secretly raising a child with horns all by herself?
    # 37.5M | Accidentally His: The Dragon King Won't Let Go
    'accidentally-his-the-dragon-king-won-t-let-go': "He thinks she's abandoned him. She doesn't remember him.\nThe Dragon King has been left waiting for a woman who ran from him. She's human, and their encounter on a Blood Moon ended with her belly swelling and her fleeing in fright. She had stumbled into his cabin drunk while he was in heat. Now they've found each other again, but she doesn't recognize the man she slept with. And there may be a child with horns to explain.",

}

SOURCES = {
    'rejecting-my-five-female-mates': ('platform', 'https://www.reelshort.com/movie/rejecting-my-five-female-mates-6a99555185913218590748f3'),
    'fiancee-s-betrayal-dante-s-inferno': ('platform', 'https://www.reelshort.com/movie/fiancee-s-betrayal-dante-s-inferno-6a2b076bbe129b998d0fa894'),
    'keeping-the-cowboy-s-baby': ('platform', 'https://www.reelshort.com/movie/keeping-the-cowboy-s-baby-6a580b359cc3a55a2b08ad6d'),
    'a-ruler-in-disguise': ('platform', 'https://www.reelshort.com/movie/a-ruler-in-disguise-6a4ff019ce4e4e0aef058c23'),
    'accidentally-his-the-dragon-king-won-t-let-go': ('platform', 'https://www.reelshort.com/movie/accidentally-his-the-dragon-king-won-t-let-go-6a9a22922dffdf54e50ba5a5'),
}

FACTS = {
    'rejecting-my-five-female-mates': 'Orphaned Caine spent ten years of his life prioritizing his five mates in Rejecting My Five Female Mates. They were his foster father’s beloved daughters—spoiled, cherished, and fearless in their own ways. They became the anchor of his existence, and for so long, he thought one of them would become his fated mate. Everything changed when Seth, a notorious rogue, came onto the scene. Blinded by Seth’s lies, the five female mates turned against Caine, relentlessly humiliating him and constantly challenging his honor as the next-in-line alpha of the pack. Their treatment of Caine eventually became more than he could bear. Rather than stay and endure another humiliation, he left the pack and looked elsewhere for a future. His search took him to a foreign pack, where a marriage alliance brought him together with Princess Sylvia. He didn’t expect to fall for her so quickly, but he did. Caine thought leaving would put the worst behind him, but his life with Sylvia soon ran into trouble. One problem followed another, testing a relationship that had only just begun. Still, they refused to turn against each other and managed to get through it. For a brief moment, their future finally looked secure. That was until his five female mates crashed their wedding, demanding to settle the score and begging him to take them back. Would Caine accept their apology, or would it be the last time they ever brought up the past? Characters Caine Caine is the central character of Rejecting My Five Female Mates. He’s resilient, compassionate, and humble, always acting out of honor and always determined to fight for the truth. Enduring the hardships eventually pays off when he discovers a place where no one can doubt him again. Princess Sylvia Princess Sylvia is the reigning princess of the Silvermoon Pack. She’s mature, morally upright, and perceptive, exactly the kind of traits that match Caine’s personality. No wonder fate brought them together and allowed them to live happily ever after. Seth Seth is the notorious rogue who lies his way into the five female mates’ hearts. He creates stories to attack Caine’s character, believing they would be enough to get everything Caine has. His schemes fall through when Caine exposes him and he is punished for his sins.',
    'fiancee-s-betrayal-dante-s-inferno': "In Fiancée's Betrayal Dante's Inferno movie, Dante Bosch returns home after 3 years in the Marine Raiders on a top secret mission, only to discover not only is his fiancée Lilith pregnant with his brother Virgil's baby, but Virgil has also spent all his money. To add insult to injury, his parents take Virgil's side. After suffering betrayals and humiliations, Dante exposes Virgil's lies with a video at his wedding.",
    'keeping-the-cowboy-s-baby': 'She came to town for a fresh start. Instead, Penelope Harris got pregnant by her ex’s powerful older brother, Knox Grant– the rugged cowboy who owns the ranch where she works. Now Penelope is caught between the man who would burn the world down for her and her ex, who wants to see her burn.',
    'a-ruler-in-disguise': "Marcus, a warlord who controls America’s economy and weapons, attends his brother Reed’s wedding. Mistaken for a delivery worker because of his mission uniform, he is looked down upon by the fiancée and her family. As a result, Marcus tries to set Reed up with the famous 'Three Goddesses of America,' but no one would believe him and they humiliate him. Reed defends him, so the fiancée’s family turns on Reed — she publicly dumps him to marry her ex instead, who has secretly been bankrupting Reed's business. Enraged, Marcus strikes back and humiliates them all. Only then do they learn his true identity—and regret it too late.",
    'accidentally-his-the-dragon-king-won-t-let-go': "In Accidentally His The Dragon King Won't Let Go movie, on a Blood Moon night, a drunken human girl steps into a cabin where the Dragon King lies in heat. After a steamy night with him, her belly suddenly swells, terrifying her into fleeing and leaving the loyal Dragon King to believe she has abandoned him. Days later, fate brings them together again, only for him to discover that she remembers nothing about him! But wait... is she secretly raising a child with horns all by herself?",
}
