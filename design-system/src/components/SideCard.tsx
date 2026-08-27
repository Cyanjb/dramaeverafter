import type { ReactNode } from 'react';

export interface SideCardProps {
  /** Card heading. */
  title?: string;
  /** Blush warning variant (used for "before you write" notes). */
  warn?: boolean;
  children: ReactNode;
}

/**
 * White sidebar card with a Fraunces heading. `warn` switches to the blush
 * cautionary style. Body is free-form; use `SideCardKv` for label/value pairs.
 */
export function SideCard({ title, warn = false, children }: SideCardProps) {
  return (
    <div className={warn ? 'side-card warn' : 'side-card'}>
      {title && <h2>{title}</h2>}
      {children}
    </div>
  );
}

export interface SideCardKvProps {
  /** Small uppercase key, e.g. "Response time". */
  k: string;
  /** Value line below it. */
  children: ReactNode;
}

/** Key/value block inside a `SideCard`. */
export function SideCardKv({ k, children }: SideCardKvProps) {
  return (
    <div className="kv">
      <div className="k">{k}</div>
      <div>{children}</div>
    </div>
  );
}
