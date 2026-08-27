import type { ReactNode } from 'react';

export interface SplitHeroProps {
  /** Left column — typically a 2:3 poster image or a large `Ring`. */
  poster: ReactNode;
  /** Tighter spacing variant used on actor pages. */
  tight?: boolean;
  /** Right column — eyebrow, `<h1>`, views line, `WatchCard`, chips, etc. */
  children: ReactNode;
}

/**
 * Two-column gradient hero for title/actor/app pages: poster column on the
 * left, info column on the right. Wraps on narrow screens.
 */
export function SplitHero({ poster, tight = false, children }: SplitHeroProps) {
  return (
    <section className={tight ? 'split-hero tight' : 'split-hero'}>
      <div className="poster-col">{poster}</div>
      <div className="info-col">{children}</div>
    </section>
  );
}

export interface PosterImageProps {
  /** Poster URL. */
  src: string;
  alt?: string;
}

/** Bordered 2:3 poster image for a `SplitHero`'s poster column. */
export function PosterImage({ src, alt = '' }: PosterImageProps) {
  return (
    <span className="poster">
      <img src={src} alt={alt} loading="lazy" />
    </span>
  );
}
