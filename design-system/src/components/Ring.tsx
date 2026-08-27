export interface RingProps {
  /** Monogram shown when no photo loads, e.g. "SM" for Sarah Moliski. */
  initials: string;
  /** Actor photo URL, layered over the monogram. */
  src?: string;
  /** `sm` 46px · `md` 50px · `rail` 78px · `hero` 132px. */
  size?: 'sm' | 'md' | 'rail' | 'hero';
  /** Set when the ring sits on the warm background so the inner ring matches. */
  onWarm?: boolean;
}

/**
 * The circular actor identity ring — blush monogram fallback with an optional
 * photo on top, ringed by an inset border.
 */
export function Ring({ initials, src, size = 'md', onWarm = false }: RingProps) {
  const cls = ['ring', `ring--${size}`, onWarm && 'on-warm'].filter(Boolean).join(' ');
  return (
    <span className={cls}>
      <span>{initials}</span>
      {src && <img src={src} alt="" loading="lazy" />}
    </span>
  );
}
