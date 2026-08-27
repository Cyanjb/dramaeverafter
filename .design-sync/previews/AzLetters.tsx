import { AzLetters } from 'dramaeverafter-ds';

export const FullStrip = () => (
  <div style={{ width: 620 }}>
    <AzLetters />
  </div>
);

export const WithEmpties = () => (
  <div style={{ width: 620 }}>
    <AzLetters letters={[
      { letter: 'A', href: '#' }, { letter: 'B', href: '#' }, { letter: 'C', href: '#' },
      { letter: 'Q', empty: true }, { letter: 'R', href: '#' }, { letter: 'S', href: '#' },
      { letter: 'X', empty: true }, { letter: 'Z', empty: true }, { letter: '#', href: '#' },
    ]} />
  </div>
);
