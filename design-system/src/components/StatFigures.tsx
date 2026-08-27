export interface StatFigure {
  /** The Fraunces number, e.g. "32". */
  n: string;
  /** Label under it, e.g. "titles on record". */
  label: string;
}

export interface StatFiguresProps {
  /** Figures, rendered with thin dividers between them. */
  stats: StatFigure[];
}

/**
 * Row of big Fraunces numbers with small labels, divided by hairlines — the
 * actor-page stats treatment.
 */
export function StatFigures({ stats }: StatFiguresProps) {
  return (
    <div className="stat-figures">
      {stats.map((s, i) => (
        <span key={s.label} style={{ display: 'contents' }}>
          <span className="stat">
            <span className="n">{s.n}</span>
            <span className="l">{s.label}</span>
          </span>
          {i < stats.length - 1 && <span className="divider" />}
        </span>
      ))}
    </div>
  );
}
