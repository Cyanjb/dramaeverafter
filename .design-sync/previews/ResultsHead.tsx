import { ResultsHead, SortLabel } from 'dramaeverafter-ds';

export const Canonical = () => (
  <div style={{ width: 620 }}>
    <ResultsHead count="1,036" countLabel="titles match">
      <SortLabel options={['Most watched', 'Newest', 'A → Z']} />
    </ResultsHead>
  </div>
);
