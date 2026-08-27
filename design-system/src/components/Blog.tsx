export interface BlogFeaturedProps {
  /** Uppercase gold kicker, e.g. "This week". */
  kicker?: string;
  /** The big Fraunces headline. */
  title: string;
  /** Muted byline/date row, e.g. "24 Aug 2026 · 6 min read". */
  sub?: string;
  /** Cover image URL for the left art column. */
  image?: string;
  href?: string;
}

/**
 * The large featured-post card from the blog index — art on the left,
 * kicker/headline/sub on the right.
 */
export function BlogFeatured({ kicker, title, sub, image, href = '#' }: BlogFeaturedProps) {
  return (
    <a className="blog-featured" href={href}>
      {image && (
        <span className="art">
          <img src={image} alt="" loading="lazy" />
        </span>
      )}
      <span className="copy">
        {kicker && <span className="blog-kicker">{kicker}</span>}
        <h2>{title}</h2>
        {sub && <span className="blog-sub">{sub}</span>}
      </span>
    </a>
  );
}

export interface BlogRowProps {
  /** Post title. */
  title: string;
  /** Excerpt paragraph. */
  excerpt?: string;
  /** Muted meta line, e.g. "17 Aug 2026". */
  sub?: string;
  /** 2:3 thumbnail URL. */
  thumb?: string;
  href?: string;
}

/**
 * Compact blog list row — small 2:3 thumb, title, excerpt. Warm hover.
 */
export function BlogRow({ title, excerpt, sub, thumb, href = '#' }: BlogRowProps) {
  return (
    <a className="blog-row" href={href}>
      <span className="thumb">
        {thumb && <img src={thumb} alt="" loading="lazy" />}
      </span>
      <span className="body">
        <h3>{title}</h3>
        {sub && <span className="blog-sub">{sub}</span>}
        {excerpt && <p className="excerpt">{excerpt}</p>}
      </span>
    </a>
  );
}
