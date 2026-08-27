import type { MouseEventHandler } from 'react';

export interface ActButtonProps {
  /** Leading glyph, e.g. "★" for save, "↗" for share. */
  icon?: string;
  /** Visible label, e.g. "Save to my list". */
  label: string;
  /** Toggled state — pressed shows the gold fill (e.g. already saved). */
  pressed?: boolean;
  onClick?: MouseEventHandler;
}

/**
 * Outlined action button used on title pages (Save to my list, Share).
 * `pressed` flips it to the gold "active" state via `aria-pressed`.
 */
export function ActButton({ icon = '★', label, pressed = false, onClick }: ActButtonProps) {
  return (
    <button className="act-btn" type="button" aria-pressed={pressed} onClick={onClick}>
      <span aria-hidden="true">{icon}</span>
      <span className="act-label">{label}</span>
    </button>
  );
}
