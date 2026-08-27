import type { ReactNode, MouseEventHandler } from 'react';
import { ResetPill } from './Pills';

export interface ActiveFiltersProps {
  /** Summary of what's applied, e.g. `"2 filters · billionaire, revenge"`. */
  text: string;
  onReset?: MouseEventHandler;
  /** Reset pill label (default "Reset"). */
  resetLabel?: string;
}

/**
 * Blush bar summarizing applied browse filters, with the outlined reset pill
 * on the right.
 */
export function ActiveFilters({ text, onReset, resetLabel = 'Reset' }: ActiveFiltersProps) {
  return (
    <div className="active-filters">
      <span className="txt">{text}</span>
      <ResetPill label={resetLabel} onClick={onReset} />
    </div>
  );
}

export interface FilterGroupProps {
  /** Small uppercase group heading, e.g. "Tropes". */
  title: string;
  /** Muted helper line under the heading. */
  hint?: string;
  /** Usually a `Chips tight` set. */
  children: ReactNode;
}

/**
 * One labeled filter section from the browse sidebar — uppercase heading,
 * optional hint, then the filter chips.
 */
export function FilterGroup({ title, hint, children }: FilterGroupProps) {
  return (
    <div className="filter-group">
      <h2>{title}</h2>
      {hint && <p className="hint">{hint}</p>}
      {children}
    </div>
  );
}

export interface ResultsHeadProps {
  /** Bold Fraunces count, e.g. "1,036". */
  count: string;
  /** Text after the count, e.g. "titles match". */
  countLabel: string;
  /** Right side — typically a `SortLabel`. */
  children?: ReactNode;
}

/** Results header row: "N titles match" on the left, sort control on the right. */
export function ResultsHead({ count, countLabel, children }: ResultsHeadProps) {
  return (
    <div className="results-head">
      <p className="count"><b>{count}</b> {countLabel}</p>
      {children}
    </div>
  );
}
