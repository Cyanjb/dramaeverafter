# -*- coding: utf-8 -*-
"""APPROVED captions only. Cyan has signed off on every line in this file.

WHY THIS FILE IS SEPARATE FROM THE DRAFT BATCH. captions_2026_08_15_r0.py holds
work in progress that she has not ruled on, and applying it wholesale would put
unreviewed copy on the site. Approved captions move HERE, and only this file is
ever applied. The draft file is a workspace; this one is the record of what she
said yes to.

Apply with:
    py generator/caption_pipeline.py check generator/staging/captions_approved_2026_08_15.py
    py generator/caption_pipeline.py apply generator/staging/captions_approved_2026_08_15.py
then rebuild.
"""

CAPTIONS = {

    # APPROVED by Cyan 15 Aug 2026, after four rounds on the middle sentence.
    # THE SITE'S HIGHEST TRAFFIC TITLE, 522.7M views. What it was publishing before
    # this: "ReelShort's breakout megahit, 500M+ views on platform." - a stat, not a
    # synopsis, on the most visited page on the site.
    'the-double-life-of-my-billionaire-husband':
        "The marriage was supposed to be paperwork.\n"
        "Natalie and Sebastian marry on paper only, strictly business with no "
        "feelings involved. But the arrangement doesn't stay that simple. Her family "
        "is quietly plotting her downfall, and the man she married is living a life "
        "she knows nothing about.\n"
        "We love a marriage of convenience that refuses to stay convenient.",
}

FACTS = {
    # Fetched 15 Aug 2026 from the platform's own page, because the text on disk was
    # a stat line and the accuracy guard correctly refused a caption written against
    # it. 60 episodes. Cast listed: Avery Lynch, Jarred Harper, Molly Anderson.
    # https://www.reelshort.com/movie/the-double-life-of-my-billionaire-husband-65a8cec883959aedd8001107
    #
    # NOTE ON ONE DELIBERATE VAGUENESS: the source says "her estranged husband" plots
    # something deadly but never states whether that is Sebastian or another man. The
    # caption says "the man she married is living a life she knows nothing about",
    # which is true either way and is supported by the title itself.
    'the-double-life-of-my-billionaire-husband':
        "It was supposed to be an emotionless contract marriage and nothing more. But "
        "Sebastian couldn't resist growing a soft spot for Natalie. With her family "
        "planning her downfall and her estranged husband cooking up a deadly plan, "
        "what should Natalie expect?",
}
