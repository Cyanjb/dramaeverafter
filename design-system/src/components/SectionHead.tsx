export interface SectionHeadProps {
  /** Section heading (Fraunces h2). */
  title: string;
  /** Right-aligned "view all" link text, e.g. "All titles →". */
  allLabel?: string;
  allHref?: string;
  /** Muted hint text on the right instead of a link. */
  hint?: string;
  /** Adds side padding when the section head sits at a full-bleed edge. */
  pad?: boolean;
}

/**
 * Section heading row — h2 on the left, an underlined "view all" link or a
 * muted hint on the right.
 */
export function SectionHead({ title, allLabel, allHref = '#', hint, pad = false }: SectionHeadProps) {
  return (
    <div className={pad ? 'section-head pad' : 'section-head'}>
      <h2>{title}</h2>
      {allLabel && <a className="all" href={allHref}>{allLabel}</a>}
      {hint && !allLabel && <span className="hint" style={{ fontSize: '13.5px', color: 'var(--tert)' }}>{hint}</span>}
    </div>
  );
}
