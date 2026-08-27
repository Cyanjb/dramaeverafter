import { SideCard, SideCardKv } from 'dramaeverafter-ds';

export const WithKv = () => (
  <div style={{ width: 300 }}>
    <SideCard title="Good to know">
      <SideCardKv k="Response time">Usually within a week</SideCardKv>
      <SideCardKv k="Corrections">Checked against the app first</SideCardKv>
    </SideCard>
  </div>
);

export const Warning = () => (
  <div style={{ width: 300 }}>
    <SideCard title="Before you write" warn>
      <ul>
        <li>We don't host any videos — each title links out to its app.</li>
        <li>Episode counts come from the platforms and can lag.</li>
      </ul>
    </SideCard>
  </div>
);
