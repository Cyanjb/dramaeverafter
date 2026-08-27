import { Ring } from 'dramaeverafter-ds';

export const Sizes = () => (
  <div style={{ display: 'flex', alignItems: 'center', gap: 18 }}>
    <Ring initials="SM" size="sm" />
    <Ring initials="SM" size="md" />
    <Ring initials="SM" size="rail" />
    <Ring initials="SM" size="hero" />
  </div>
);

export const Monograms = () => (
  <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
    <Ring initials="MH" size="rail" />
    <Ring initials="KE" size="rail" />
    <Ring initials="JT" size="rail" />
  </div>
);
