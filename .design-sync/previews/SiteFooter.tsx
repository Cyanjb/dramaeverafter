import { SiteFooter } from 'dramaeverafter-ds';

export const Canonical = () => (
  <div style={{ width: 740 }}>
    <SiteFooter
      cols={[
        { heading: 'Browse', links: [
          { label: 'All titles', href: '#' }, { label: 'Actors', href: '#' },
          { label: 'Apps', href: '#' }, { label: 'Tropes', href: '#' },
        ]},
        { heading: 'About', links: [
          { label: 'Blog', href: '#' }, { label: 'Contact', href: '#' },
          { label: 'My List', href: '#' },
        ]},
      ]}
    />
  </div>
);
