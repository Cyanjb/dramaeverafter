import type { ReactNode, MouseEventHandler } from 'react';

export interface ChipProps {
  /** Chip text, e.g. a trope name like "contract marriage". */
  label: string;
  /** Optional count rendered small and muted after the label. */
  count?: string | number;
  /** `on` = selected (wine fill); `off` = disabled/unavailable; default = idle outline. */
  state?: 'on' | 'off';
  /** Renders an `<a>` when set, otherwise a `<button>`. */
  href?: string;
  onClick?: MouseEventHandler;
}

/**
 * Rounded filter/tag chip — the site's trope tags and browse filters.
 * `state="on"` is the selected wine fill; `state="off"` is greyed out.
 */
export function Chip({ label, count, state, href, onClick }: ChipProps) {
  const cls = state ? `chip ${state}` : 'chip';
  const body = (
    <>
      {label}
      {count !== undefined && <span className="c">{count}</span>}
    </>
  );
  if (href) return <a className={cls} href={href} onClick={onClick}>{body}</a>;
  return <button className={cls} type="button" onClick={onClick}>{body}</button>;
}

export interface ChipsProps {
  /** Tighter 8px gap variant. */
  tight?: boolean;
  children: ReactNode;
}

/** Wrapping flex container for a set of `Chip`s. */
export function Chips({ tight = false, children }: ChipsProps) {
  return <div className={tight ? 'chips tight' : 'chips'}>{children}</div>;
}

export interface ChipAllProps {
  /** e.g. `"All 178 tropes →"`. */
  label: string;
  href: string;
}

/** The bold wine "view all" chip that ends a chip row. */
export function ChipAll({ label, href }: ChipAllProps) {
  return <a className="chip-all" href={href}>{label}</a>;
}

export interface ChipDashedProps {
  /** e.g. `"Show 12 more tropes"`. */
  label: string;
  onClick?: MouseEventHandler;
}

/** Dashed-border chip used as a "show more" expander under a collapsed chip set. */
export function ChipDashed({ label, onClick }: ChipDashedProps) {
  return <button className="chip-dashed" type="button" onClick={onClick}>{label}</button>;
}
