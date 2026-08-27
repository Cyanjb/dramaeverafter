export interface FooterCol {
  /** Small uppercase column heading, e.g. "Browse". */
  heading: string;
  links: { label: string; href: string }[];
}

export interface SiteFooterProps {
  /** Brand blurb under the wordmark. */
  blurb?: string;
  /** Link columns on the right. */
  cols?: FooterCol[];
}

const DEFAULT_BLURB =
  'A reader-made index of vertical dramas — which app, which cast, what next. Some links earn a commission.';

/**
 * The plum site footer: wordmark and blurb on the left, uppercase-headed link
 * columns on the right.
 */
export function SiteFooter({ blurb = DEFAULT_BLURB, cols = [] }: SiteFooterProps) {
  return (
    <footer className="site-footer">
      <div className="footer-brand">
        <div className="wordmark"><span>Drama</span><em>EverAfter</em></div>
        <p>{blurb}</p>
      </div>
      <div className="footer-cols">
        {cols.map((col) => (
          <div className="footer-col" key={col.heading}>
            <span className="h">{col.heading}</span>
            {col.links.map((l) => <a key={l.label} href={l.href}>{l.label}</a>)}
          </div>
        ))}
      </div>
    </footer>
  );
}
