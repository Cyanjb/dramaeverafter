export interface WatchCardProps {
  /** App the title streams on, e.g. "GoodShort". */
  appName: string;
  /** Outbound watch link. */
  href?: string;
  /** Card heading (default "Where to watch"). */
  label?: string;
  /** Affiliate disclosure line under the button; pass `null` to omit. */
  disclosure?: string | null;
  /** Optional secondary link text, e.g. "Also on DramaBox →". */
  moreLabel?: string;
  moreHref?: string;
  /** No link yet — renders the dashed "pending" pill instead of the gold button. */
  pending?: boolean;
}

/**
 * The where-to-watch card from title pages: label, big gold watch button, and
 * the affiliate disclosure. `pending` swaps the button for the dashed
 * "link coming soon" state.
 */
export function WatchCard({
  appName, href = '#', label = 'Where to watch',
  disclosure = 'Opens the app. We may earn a commission, which is what keeps this database free.',
  moreLabel, moreHref = '#', pending = false,
}: WatchCardProps) {
  return (
    <div className="watch-card">
      <p className="label">{label}</p>
      {pending ? (
        <span className="watch-pending">Watch link coming soon</span>
      ) : (
        <a className="watch-btn" href={href}>
          <span>Watch on {appName}</span>
          <span className="arrow">→</span>
        </a>
      )}
      {moreLabel && <a className="watch-more" href={moreHref}>{moreLabel}</a>}
      {disclosure && <p className="watch-disclosure">{disclosure}</p>}
    </div>
  );
}
