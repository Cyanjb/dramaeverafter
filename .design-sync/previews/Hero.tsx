import { Hero } from 'dramaeverafter-ds';

export const Homepage = () => (
  <div style={{ width: 760 }}>
    <Hero
      eyebrow="Looking for that app? that actor? that drama?"
      title="All the Drama Ever After. Find it. Watch it. Love it."
      lede="Every micro-drama we can find, the cast behind it, and the one app it actually streams on. No account, no algorithm, no autoplay."
      searchPlaceholder="e.g. Silver Fox, or Sarah Moliski"
      stats={[
        { n: '3,513', label: 'titles' },
        { n: '2,212', label: 'actors' },
        { n: '16', label: 'apps' },
      ]}
    />
  </div>
);

export const Minimal = () => (
  <div style={{ width: 640 }}>
    <Hero
      eyebrow="Vertical drama · 2025 · 82 episodes"
      title="Browse every trope"
      lede="The shortcut most people actually use. 178 in all."
    />
  </div>
);
