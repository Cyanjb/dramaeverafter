import { SplitHero, WatchCard, ActButton, Chips, Chip, Ring } from 'dramaeverafter-ds';

export const TitlePage = () => (
  <div style={{ width: 860 }}>
    <SplitHero
      poster={
        <span className="poster">
          <span className="poster--empty">
            <span className="label">No poster</span>
            <span className="ttl">1,000 Years in the Void: Now Reality Bows to Me</span>
            <span className="app">GoodShort</span>
          </span>
        </span>
      }
    >
      <p className="eyebrow">Vertical drama · 2025 · 82 episodes</p>
      <h1>1,000 Years in the Void: Now Reality Bows to Me</h1>
      <p className="views-line">42K views · Urban · English original</p>
      <WatchCard appName="GoodShort" href="#" />
      <div className="title-actions">
        <ActButton icon="★" label="Save to my list" />
        <ActButton icon="↗" label="Share" />
      </div>
    </SplitHero>
  </div>
);

export const ActorPage = () => (
  <div style={{ width: 860 }}>
    <SplitHero tight poster={<Ring initials="SM" size="hero" />}>
      <p className="eyebrow">Actor</p>
      <h1>Sarah Moliski</h1>
      <p className="views-line">24 titles on record</p>
      <Chips>
        <Chip label="billionaire" count="9" href="#" />
        <Chip label="contract marriage" count="6" href="#" />
        <Chip label="revenge" count="4" href="#" />
      </Chips>
    </SplitHero>
  </div>
);
