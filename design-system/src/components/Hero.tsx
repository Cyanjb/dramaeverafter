import type { ReactNode } from 'react';
import { Button } from './Button';

export interface HeroStat {
  /** The Fraunces number, e.g. "3,513". */
  n: string;
  /** Its label, e.g. "titles". */
  label: string;
}

export interface HeroProps {
  /** Small gold uppercase line above the headline. */
  eyebrow?: string;
  /** The big Fraunces headline. */
  title: string;
  /** Muted paragraph under the headline. */
  lede?: string;
  /** Renders the search input + gold button when set. */
  searchPlaceholder?: string;
  searchAction?: string;
  searchButtonLabel?: string;
  /** Dot-separated stats under the search. */
  stats?: HeroStat[];
  /** Extra content below everything else. */
  children?: ReactNode;
}

/**
 * The gradient homepage hero: eyebrow, display headline, lede, search form,
 * and the bold-number stat line.
 */
export function Hero({
  eyebrow, title, lede, searchPlaceholder, searchAction = '#',
  searchButtonLabel = 'Search', stats, children,
}: HeroProps) {
  return (
    <section className="hero">
      <div className="inner">
        {eyebrow && <p className="eyebrow">{eyebrow}</p>}
        <h1>{title}</h1>
        {lede && <p className="lede">{lede}</p>}
        {searchPlaceholder && (
          <form className="hero-search-form" action={searchAction} method="get">
            <input type="search" name="q" placeholder={searchPlaceholder} aria-label={searchPlaceholder} />
            <Button variant="gold" type="submit">{searchButtonLabel}</Button>
          </form>
        )}
        {stats && stats.length > 0 && (
          <div className="stat-line">
            {stats.map((s, i) => (
              <span key={s.label} style={{ display: 'contents' }}>
                <span><b>{s.n}</b> {s.label}</span>
                {i < stats.length - 1 && <span className="dot">·</span>}
              </span>
            ))}
          </div>
        )}
        {children}
      </div>
    </section>
  );
}
