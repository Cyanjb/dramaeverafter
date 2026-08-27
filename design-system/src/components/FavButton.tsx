import type { MouseEventHandler } from 'react';

export interface FavButtonProps {
  /** Accessible label, e.g. `"Save How to Tame a Silver Fox to my list"`. */
  ariaLabel: string;
  /** Saved state — pressed shows the solid gold star. */
  pressed?: boolean;
  onClick?: MouseEventHandler;
}

/**
 * The circular star button that floats over a poster's top-left corner to save
 * a title. Position is absolute — place it inside a `PosterCard` (or any
 * `position: relative` parent).
 */
export function FavButton({ ariaLabel, pressed = false, onClick }: FavButtonProps) {
  return (
    <button className="fav-btn" type="button" aria-label={ariaLabel} aria-pressed={pressed} onClick={onClick}>
      <span aria-hidden="true">★</span>
    </button>
  );
}
