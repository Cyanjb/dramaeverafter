import { Ring } from './Ring';

export interface ActorTileProps {
  /** Actor name. */
  name: string;
  /** Sub-line, e.g. "24 titles". */
  sub?: string;
  /** Monogram fallback, e.g. "SM". */
  initials: string;
  /** Photo URL. */
  src?: string;
  href?: string;
  /** Pass when the tile sits on the warm background. */
  onWarm?: boolean;
}

/**
 * Centered actor tile — 78px ring above the name and title count. Used in
 * "Faces you keep seeing" grids and actor rails.
 */
export function ActorTile({ name, sub, initials, src, href = '#', onWarm = false }: ActorTileProps) {
  return (
    <a className="actor-tile" href={href}>
      <Ring initials={initials} src={src} size="rail" onWarm={onWarm} />
      <span className="stack">
        {/* block-level: the site's inline spans only stack because narrow tiles force a wrap */}
        <span className="name" style={{ display: 'block' }}>{name}</span>
        {sub && <span className="sub" style={{ display: 'block' }}>{sub}</span>}
      </span>
    </a>
  );
}
