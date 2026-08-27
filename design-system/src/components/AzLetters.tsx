export interface AzLetter {
  /** The letter (or "#") shown in the box. */
  letter: string;
  href?: string;
  /** Greyed-out non-link state for letters with no entries. */
  empty?: boolean;
}

export interface AzLettersProps {
  /** The full letter strip; defaults to A–Z all active. */
  letters?: AzLetter[];
  /** Wrap in the sticky blurred bar the actors index uses. */
  sticky?: boolean;
}

const DEFAULT_LETTERS: AzLetter[] = Array.from('ABCDEFGHIJKLMNOPQRSTUVWXYZ', (l) => ({ letter: l, href: '#' }));

/**
 * A–Z jump strip from the actors index. `empty` letters render greyed and
 * unclickable; `sticky` adds the translucent sticky bar wrapper.
 */
export function AzLetters({ letters = DEFAULT_LETTERS, sticky = false }: AzLettersProps) {
  const strip = (
    <div className="az-letters">
      {letters.map((l) =>
        l.empty
          ? <span className="az-letter empty" key={l.letter}>{l.letter}</span>
          : <a className="az-letter" href={l.href ?? '#'} key={l.letter}>{l.letter}</a>
      )}
    </div>
  );
  return sticky ? <div className="az-bar">{strip}</div> : strip;
}
