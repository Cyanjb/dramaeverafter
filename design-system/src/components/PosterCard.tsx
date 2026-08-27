import { FavButton } from './FavButton';

export interface PosterCardProps {
  /** Drama title, e.g. "How to Tame a Silver Fox". */
  title: string;
  /** Platform/app name shown under the poster, e.g. "ReelShort". */
  app: string;
  /** Poster image URL. Omit to show the styled blush "No poster" fallback. */
  poster?: string;
  /** Meta line under the app name, e.g. `"417M views · age gap"`. */
  meta?: string;
  /** Link target for the title. */
  href?: string;
  /** Link target for the app name. */
  appHref?: string;
  /** Smaller 158px rail size. */
  sm?: boolean;
  /** Set when the card sits inside a `Rail` (adds the rail-item sizing). */
  railItem?: boolean;
  /** Shows the dark "AI" pill on the poster's top-right. */
  aiBadge?: boolean;
  /** Shows the wine "SOON" pill on the poster's top-left (unreleased titles). */
  soonBadge?: boolean;
  /** Renders the floating save-star; true = already saved. Omit to hide the star. */
  saved?: boolean;
}

/**
 * The 2:3 drama poster card used in every rail and grid. Always renders the
 * blush "No poster" fallback beneath the image, so a dead poster URL degrades
 * gracefully — exactly like the live site.
 */
export function PosterCard({
  title, app, poster, meta, href = '#', appHref = '#',
  sm = false, railItem = false, aiBadge = false, soonBadge = false, saved,
}: PosterCardProps) {
  const cls = ['poster-card', railItem && 'rail-item', sm && 'sm'].filter(Boolean).join(' ');
  return (
    <div className={cls}>
      <a className="poster-link" href={href}>
        <span className="poster">
          <span className="poster--empty">
            <span className="label">No poster</span>
            <span className="ttl">{title}</span>
            <span className="app">{app}</span>
          </span>
          {poster && <img src={poster} alt={title} loading="lazy" />}
          {aiBadge && <span className="ai-badge">AI</span>}
          {soonBadge && <span className="soon-badge">SOON</span>}
        </span>
      </a>
      {saved !== undefined && <FavButton ariaLabel={`Save ${title} to my list`} pressed={saved} />}
      <a className="app-name" href={appHref}>{app}</a>
      {meta && <a className="meta" href={href}>{meta}</a>}
    </div>
  );
}
