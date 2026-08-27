export interface PaginationProps {
  /** Previous-page link; omit on the first page. */
  prevHref?: string;
  prevLabel?: string;
  /** Next-page link (rendered bold wine); omit on the last page. */
  nextHref?: string;
  nextLabel?: string;
  /** Status line between the links, e.g. "Page 2 of 9". */
  status?: string;
}

/**
 * Prev/status/next pagination bar; the next link carries the emphasized wine
 * treatment.
 */
export function Pagination({ prevHref, prevLabel = '← Previous', nextHref, nextLabel = 'Next →', status }: PaginationProps) {
  return (
    <nav className="pagination">
      {prevHref && <a href={prevHref}>{prevLabel}</a>}
      {status && <span className="status">{status}</span>}
      {nextHref && <a className="next" href={nextHref}>{nextLabel}</a>}
    </nav>
  );
}
