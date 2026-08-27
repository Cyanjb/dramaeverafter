export interface CrumbItem {
  label: string;
  /** Omit on the final (current-page) item. */
  href?: string;
}

export interface CrumbProps {
  /** Trail items in order; the last one renders as the non-link current page. */
  items: CrumbItem[];
}

/**
 * Breadcrumb trail with `/` separators; the current page is muted, not linked.
 */
export function Crumb({ items }: CrumbProps) {
  return (
    <nav className="crumb">
      {items.map((item, i) => {
        const last = i === items.length - 1;
        return (
          <span key={item.label} style={{ display: 'contents' }}>
            {item.href && !last
              ? <a href={item.href}>{item.label}</a>
              : <span className={last ? 'current' : undefined}>{item.label}</span>}
            {!last && <span>/</span>}
          </span>
        );
      })}
    </nav>
  );
}
