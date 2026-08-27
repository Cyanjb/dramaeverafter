export interface FaqItem {
  /** The question (summary line). */
  q: string;
  /** The answer paragraph. */
  a: string;
  /** Render this item expanded. */
  open?: boolean;
}

export interface FaqProps {
  /** Section heading (default "FAQ"). */
  title?: string;
  items: FaqItem[];
  /** Small muted note under the list. */
  note?: string;
}

/**
 * The plum FAQ band — white heading and expandable question rows on the dark
 * background.
 */
export function Faq({ title = 'FAQ', items, note }: FaqProps) {
  return (
    <section className="faq">
      <h2>{title}</h2>
      {items.map((item) => (
        <details key={item.q} open={item.open}>
          <summary>{item.q}</summary>
          <p>{item.a}</p>
        </details>
      ))}
      {note && <p className="note">{note}</p>}
    </section>
  );
}
