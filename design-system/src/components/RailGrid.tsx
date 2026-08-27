import type { ReactNode } from 'react';

export interface RailProps {
  /** Cards to scroll horizontally — typically `PosterCard railItem` items. */
  children: ReactNode;
}

/**
 * Horizontally scrolling, scroll-snapping card rail with the thin warm
 * scrollbar. Give each child `railItem` (on `PosterCard`) or the
 * `rail-item` class.
 */
export function Rail({ children }: RailProps) {
  return <div className="rail">{children}</div>;
}

export interface GridProps {
  /**
   * Column preset: default 158px posters · `cast` 230px person rows ·
   * `apps` 168px app tiles · `circles` 150px actor tiles ·
   * `tropeIdx` 210px index rows · `az` 238px A–Z entries.
   */
  variant?: 'cast' | 'apps' | 'circles' | 'tropeIdx' | 'az';
  children: ReactNode;
}

const VARIANT_CLASS: Record<string, string> = {
  cast: 'grid cast', apps: 'grid apps', circles: 'grid circles',
  tropeIdx: 'grid trope-idx', az: 'grid az',
};

/**
 * Auto-filling responsive grid with per-content presets matching the site's
 * poster, cast, app, actor-circle, and index layouts.
 */
export function Grid({ variant, children }: GridProps) {
  return <div className={variant ? VARIANT_CLASS[variant] : 'grid'}>{children}</div>;
}
