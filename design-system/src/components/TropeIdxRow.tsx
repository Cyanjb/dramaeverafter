export interface TropeIdxRowProps {
  /** Trope name, e.g. "contract marriage". */
  name: string;
  /** Title count on the right. */
  count?: string | number;
  href?: string;
}

/**
 * One row of the all-tropes index — name left, count right, warm hover.
 */
export function TropeIdxRow({ name, count, href = '#' }: TropeIdxRowProps) {
  return (
    <a className="trope-idx-row" href={href}>
      <span className="n">{name}</span>
      {count !== undefined && <span className="c">{count}</span>}
    </a>
  );
}
