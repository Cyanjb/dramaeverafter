import type { MouseEventHandler } from 'react';

export interface ReasonPillProps {
  /** Pill text, e.g. "A correction". */
  label: string;
  /** Selected state (wine fill). */
  on?: boolean;
  onClick?: MouseEventHandler;
}

/** Single-select pill used on the contact form to pick a reason for writing. */
export function ReasonPill({ label, on = false, onClick }: ReasonPillProps) {
  return (
    <button className={on ? 'reason-pill on' : 'reason-pill'} type="button" aria-pressed={on} onClick={onClick}>
      {label}
    </button>
  );
}

export interface ResetPillProps {
  /** Pill text (default "Reset"). */
  label?: string;
  onClick?: MouseEventHandler;
}

/** Small outlined pill that clears active filters, used inside `ActiveFilters`. */
export function ResetPill({ label = 'Reset', onClick }: ResetPillProps) {
  return <button className="reset-pill" type="button" onClick={onClick}>{label}</button>;
}
