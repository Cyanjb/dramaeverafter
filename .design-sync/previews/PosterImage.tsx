import { PosterImage } from 'dramaeverafter-ds';

const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="200" height="300"><rect width="200" height="300" fill="#EFD9DE"/><text x="100" y="150" text-anchor="middle" font-family="Georgia" font-size="18" fill="#7A2B4A">2:3 poster</text></svg>`;
const posterData = 'data:image/svg+xml;utf8,' + encodeURIComponent(svg);

export const Canonical = () => (
  <div style={{ width: 220 }}>
    <PosterImage src={posterData} alt="Sample poster" />
  </div>
);
