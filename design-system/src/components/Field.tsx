import type { ReactNode, ChangeEventHandler } from 'react';

export interface FieldProps {
  /** Small uppercase label above the control. */
  label: string;
  /** Control id — links the label to the input. */
  id: string;
  /** Control kind (default text input). */
  kind?: 'text' | 'email' | 'search' | 'select' | 'textarea';
  placeholder?: string;
  /** Options when `kind="select"`. */
  options?: string[];
  /** Muted helper line under the control. */
  hint?: string;
  value?: string;
  onChange?: ChangeEventHandler<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>;
  /** Textarea rows (default 5). */
  rows?: number;
}

/**
 * Labeled form field — uppercase label, bordered control with the wine focus
 * ring, optional hint. Covers text, email, search, select, and textarea.
 */
export function Field({
  label, id, kind = 'text', placeholder, options = [], hint, value, onChange, rows = 5,
}: FieldProps) {
  return (
    <div className="field">
      <label htmlFor={id}>{label}</label>
      {kind === 'textarea' ? (
        <textarea id={id} placeholder={placeholder} rows={rows} value={value} onChange={onChange} />
      ) : kind === 'select' ? (
        <select id={id} value={value} onChange={onChange}>
          {options.map((o) => <option key={o}>{o}</option>)}
        </select>
      ) : (
        <input id={id} type={kind} placeholder={placeholder} value={value} onChange={onChange} />
      )}
      {hint && <span className="hint">{hint}</span>}
    </div>
  );
}

export interface SortLabelProps {
  /** Label text before the select (default "Sort"). */
  label?: string;
  /** Sort options. */
  options: string[];
  value?: string;
  onChange?: ChangeEventHandler<HTMLSelectElement>;
}

/** Inline "Sort" label + select pair from the browse results header. */
export function SortLabel({ label = 'Sort', options, value, onChange }: SortLabelProps) {
  return (
    <label className="sort-label">
      {label}
      <select aria-label={`${label} titles`} value={value} onChange={onChange}>
        {options.map((o) => <option key={o}>{o}</option>)}
      </select>
    </label>
  );
}

export interface NewsletterBlockProps {
  /** Heading above the copy. */
  title?: string;
  /** Persuasion line. */
  copy: string;
  placeholder?: string;
  buttonLabel?: string;
  children?: ReactNode;
}

/**
 * Blush email-capture card — copy, input, and a gold button.
 */
export function NewsletterBlock({
  title, copy, placeholder = 'your@email.com', buttonLabel = 'Sign up', children,
}: NewsletterBlockProps) {
  return (
    <div className="newsletter-block">
      {title && <h2 style={{ fontSize: '19px', marginBottom: '8px' }}>{title}</h2>}
      <p style={{ marginBottom: '12px' }}>{copy}</p>
      <input type="email" placeholder={placeholder} aria-label="Email address" />
      <button className="btn btn-gold" type="button" style={{ width: '100%' }}>{buttonLabel}</button>
      {children}
    </div>
  );
}
