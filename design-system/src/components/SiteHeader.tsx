export interface NavItem {
  label: string;
  href: string;
}

export interface SiteHeaderProps {
  /** Navigation links (defaults to the site's six sections). */
  nav?: NavItem[];
  /** Search input placeholder. */
  searchPlaceholder?: string;
  /** Search form action URL. */
  searchAction?: string;
  /** Wordmark link target. */
  homeHref?: string;
}

const DEFAULT_NAV: NavItem[] = [
  { label: 'Browse', href: '#' },
  { label: 'Actors', href: '#' },
  { label: 'Apps', href: '#' },
  { label: 'Tropes', href: '#' },
  { label: 'Blog', href: '#' },
  { label: 'My List', href: '#' },
];

/**
 * The site header: Drama*EverAfter* wordmark, section nav with gold hover
 * underline, and the boxed search on the right.
 */
export function SiteHeader({
  nav = DEFAULT_NAV,
  searchPlaceholder = 'Search a title or actor',
  searchAction = '#',
  homeHref = '#',
}: SiteHeaderProps) {
  return (
    <header className="site-header">
      <a className="wordmark" href={homeHref}><span>Drama</span><em>EverAfter</em></a>
      <nav className="site-nav">
        {nav.map((item) => <a key={item.label} href={item.href}>{item.label}</a>)}
      </nav>
      <form className="site-search" action={searchAction} method="get">
        <span className="glyph">⌕</span>
        <input type="search" name="q" placeholder={searchPlaceholder} aria-label={searchPlaceholder} />
      </form>
    </header>
  );
}
