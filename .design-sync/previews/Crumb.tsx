import { Crumb } from 'dramaeverafter-ds';

export const TwoLevel = () => (
  <div style={{ width: 620 }}>
    <Crumb items={[
      { label: 'Home', href: '#' },
      { label: 'How to Tame a Silver Fox' },
    ]} />
  </div>
);

export const ThreeLevel = () => (
  <div style={{ width: 620 }}>
    <Crumb items={[
      { label: 'Home', href: '#' },
      { label: 'Tropes', href: '#' },
      { label: 'contract marriage' },
    ]} />
  </div>
);
