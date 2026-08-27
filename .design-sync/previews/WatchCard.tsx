import { WatchCard } from 'dramaeverafter-ds';

export const Canonical = () => (
  <div style={{ width: 440 }}>
    <WatchCard appName="GoodShort" href="#" />
  </div>
);

export const WithMoreLink = () => (
  <div style={{ width: 440 }}>
    <WatchCard appName="ReelShort" href="#" moreLabel="Also on DramaBox →" moreHref="#" />
  </div>
);

export const Pending = () => (
  <div style={{ width: 440 }}>
    <WatchCard appName="Vigloo" pending disclosure={null} />
  </div>
);
