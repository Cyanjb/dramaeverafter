export interface AppTileProps {
  /** Platform name, e.g. "ReelShort". */
  name: string;
  /** Small caption, e.g. "575 titles". */
  caption?: string;
  href?: string;
}

/**
 * White tile linking to a streaming app's page — name in Fraunces, count below.
 * Hover shows the gold border. Lay several out with `Grid variant="apps"`.
 */
export function AppTile({ name, caption, href = '#' }: AppTileProps) {
  return (
    <a className="app-tile" href={href}>
      <span className="n">{name}</span>
      {caption && <span className="c">{caption}</span>}
    </a>
  );
}
