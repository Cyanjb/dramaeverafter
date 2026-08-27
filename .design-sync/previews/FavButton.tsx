import type { CSSProperties } from 'react';
import { FavButton } from 'dramaeverafter-ds';

const box: CSSProperties = {
  position: 'relative', width: 120, height: 60,
  background: 'var(--blush)', border: '1px solid var(--line)', borderRadius: 3,
};

export const Idle = () => (
  <div style={box}>
    <FavButton ariaLabel="Save to my list" />
  </div>
);

export const Pressed = () => (
  <div style={box}>
    <FavButton ariaLabel="Saved to my list" pressed />
  </div>
);
