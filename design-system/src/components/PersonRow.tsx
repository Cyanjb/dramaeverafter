import { Ring } from './Ring';

export interface PersonRowProps {
  /** Person's name. */
  name: string;
  /** Sub-line, e.g. a character name or "12 titles". */
  sub?: string;
  /** Monogram fallback for the ring. */
  initials: string;
  /** Photo URL. */
  src?: string;
  href?: string;
  /** Compact padding variant for dense cast lists. */
  sm?: boolean;
}

/**
 * Horizontal person row — small ring, name, and sub-line in a bordered white
 * bar. The cast-list workhorse; hover shows the wine border.
 */
export function PersonRow({ name, sub, initials, src, href = '#', sm = false }: PersonRowProps) {
  return (
    <a className={sm ? 'person-row sm' : 'person-row'} href={href}>
      <Ring initials={initials} src={src} size={sm ? 'sm' : 'md'} />
      <span className="stack">
        {/* block-level: the site's inline spans only stack because narrow rows force a wrap */}
        <span className="name" style={{ display: 'block' }}>{name}</span>
        {sub && <span className="sub" style={{ display: 'block' }}>{sub}</span>}
      </span>
    </a>
  );
}
