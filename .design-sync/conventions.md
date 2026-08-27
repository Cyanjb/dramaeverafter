# Building with the DramaEverAfter design system

This kit is the visual language of dramaeverafter.com — a warm, editorial, romance-novel-adjacent index of vertical dramas. Paper backgrounds, wine and gold accents, serif display type. No dark mode, no neon, no glassmorphism.

## Setup

No provider or wrapper is needed. Components style themselves from `styles.css` (always loaded). Fonts load from Google Fonts: **Fraunces** (display serif) and **Atkinson Hyperlegible** (body). Never substitute other fonts.

## Styling idiom: CSS custom properties + the site's own classes

Style your layout glue with the kit's tokens, not hard-coded colors:

- Surfaces: `var(--paper)` #FBF7F2 page ground · `var(--warm)` warm section band · `var(--blush)` rosy accent panels · `#fff` cards
- Text: `var(--ink)` body · `var(--plum)` headings · `var(--muted)` ledes · `var(--sec)` secondary · `var(--tert)` faint · `var(--ph)` placeholders
- Accents: `var(--wine)` links/selected states · `var(--wine-hover)` hover · `var(--gold)` primary CTAs · `var(--gold-deep)` CTA hover
- Borders: `var(--line)` hairlines · `var(--blush-bd)` on blush · `var(--input-bd)` inputs · `var(--chip-bd)` chips

Radii are small and consistent: 2px buttons/inputs, 3px posters/cards, 999px only for pill chips. Headings are Fraunces 600 with tight line-height; eyebrows are 12-13px uppercase with `.14em` letter-spacing in `var(--gold-deep)` or `var(--tert)`.

Useful layout classes from the shipped stylesheet: `.wrap` (760px column), `.wrap-wide` (1320px), `.pad` (22px side padding), `.section-warm` (warm full-bleed band), `.eyebrow`, `.lede`.

## Where the truth lives

Read `styles.css` before inventing any style — every component's real CSS is there. Each component's `.prompt.md` shows its props and a working example.

## Idiomatic composition

```tsx
<SectionHead title="Most watched right now" allLabel="All titles →" allHref="#" />
<Rail>
  <PosterCard railItem title="How to Tame a Silver Fox" app="ReelShort"
    meta="417M views · age gap" saved={false} />
  <PosterCard railItem title="Timeleap Joseon" app="Vigloo" meta="comeback" saved={false} />
</Rail>
```

Composition rules the site follows: one gold `Button` per view at most (everything else wine/outline); posters always 2:3 with the blush no-poster fallback; `PosterCard` lives inside `Rail` (with `railItem`) or `Grid`; people render as `Ring`/`ActorTile`/`PersonRow`, never raw `<img>` avatars; trope tags are `Chip`s, and a chip row ends with `ChipAll`; page frames are `SiteHeader` on `var(--paper)` and the plum `SiteFooter`/`Faq` at the bottom.
