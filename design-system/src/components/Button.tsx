import type { ReactNode, MouseEventHandler } from 'react';

export interface ButtonProps {
  /** Visual style: `gold` is the primary CTA (search, watch); `wine` is the outlined secondary. */
  variant?: 'gold' | 'wine';
  /** Renders an `<a>` when set, otherwise a `<button>`. */
  href?: string;
  /** button type when rendered as a `<button>` (default `"button"`; use `"submit"` in forms). */
  type?: 'button' | 'submit';
  onClick?: MouseEventHandler;
  children: ReactNode;
}

/**
 * The site's call-to-action button. Gold for the one primary action on a view,
 * wine (outlined) for secondary actions like "Show 24 more".
 */
export function Button({ variant = 'gold', href, type = 'button', onClick, children }: ButtonProps) {
  const cls = `btn btn-${variant}`;
  if (href) return <a className={cls} href={href} onClick={onClick}>{children}</a>;
  return <button className={cls} type={type} onClick={onClick}>{children}</button>;
}
