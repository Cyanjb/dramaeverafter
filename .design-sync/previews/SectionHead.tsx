import { SectionHead } from 'dramaeverafter-ds';

export const WithAllLink = () => (
  <div style={{ width: 640 }}>
    <SectionHead title="Most watched right now" allLabel="All titles →" />
  </div>
);

export const WithHint = () => (
  <div style={{ width: 640 }}>
    <SectionHead title="If you liked this" hint="contract marriage · god of war" />
  </div>
);
