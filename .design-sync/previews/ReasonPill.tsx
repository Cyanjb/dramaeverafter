import { ReasonPill } from 'dramaeverafter-ds';

export const Row = () => (
  <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap', width: 480 }}>
    <ReasonPill label="A correction" on />
    <ReasonPill label="A missing title" />
    <ReasonPill label="I'm an actor" />
    <ReasonPill label="Something else" />
  </div>
);
