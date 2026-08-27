import type { ReactNode } from 'react';

export interface EmptyStateProps {
  /** Short Fraunces heading, e.g. "Nothing saved yet". */
  title: string;
  /** Supporting line under the heading. */
  children?: ReactNode;
}

/**
 * Dashed-border empty state used for empty lists and zero-result panels.
 */
export function EmptyState({ title, children }: EmptyStateProps) {
  return (
    <div className="empty-state">
      <h3>{title}</h3>
      {children && <p>{children}</p>}
    </div>
  );
}
