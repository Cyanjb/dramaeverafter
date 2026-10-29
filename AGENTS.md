# DramaEverAfter session guide

## Read first, in order
1. [DEA handoff for Codex, 26 Oct 2026](https://docs.google.com/document/d/1DGa5e-4hQexyfva1OaGlfXGpLyIhdXnYYd3krEGNdRM).
2. Craft: Coding Projects (Websites/ Apps) > DramaEverAfter > "7. DEA READ FIRST (Current State + Traps)", document id `1fba6dad-6c71-ae1f-a7c5-e38796cca201`. Read newest entries first. WAITING ON CYAN lists her pending decisions.
3. `README.md` and `data/CONVENTIONS.md`.
4. Before any caption work, read `.claude/skills/dea-captions/SKILL.md` and `generator/CAPTION-TRAINING.md` in full.

Cyan's current instructions take precedence over historical notes. Recheck GitHub and data before quoting pending work.

## Work safely
- Fetch and check status before work. Preserve other sessions' files; use a separate checkout when needed.
- CSVs in `data/` are the database. Edit sources, then run `generator/build.py` and `generator/check_site.py`; require zero failures.
- Main publishes live through Netlify. Never push work to main or merge a PR without Cyan's explicit instruction. Caption batches go to her as PRs.
- The Sunday 12:00 UTC scrape pushes to main automatically. Confirm ownership of the separate Sunday caption routine before replacing or duplicating it.
- Resolve CSV conflicts with a row-level three-way merge, never by taking one side. Rebuild generated HTML. Keep all pending review queue lines, oldest first.

## Captions and review
- Retell verified platform stories; never copy text or invent facts. Match sources to the linked book id, not just the slug. Skip and report sources with no story.
- Run `caption_pipeline.py check`, `lift_check.py --n 6` and `readback.py` for every batch. Read the readback; NOT CHECKED fails.
- Maintain ONE review file: `C:/Users/cyanj/DEA-review/review.html`, outside the repo. Rebuild with `generator/make_review_page.py --queue`, overwriting that same file. Never change STANDING_KEY.
- Ticked or edited captions are final. Apply Cyan's edits verbatim using the handoff section 6 process; list only obvious typo fixes. Report her word edit rate. Jethro's ticks count; his edits are excluded from her training and score.

## Standing boundaries
- Never email or post publicly until Cyan sees the exact final text and explicitly says send.
- Duplicate rulings need links to both sides. No YouTube platform. Slugs stay permanent; posters stay 3:4. Follow CONVENTIONS for data changes.
- Never handle passwords. Cyan signs into RS Boost herself with email and password, never Google.
- Speak plainly, step by step, without fluff or em dashes. Ask when unsure.
