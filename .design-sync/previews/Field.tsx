import { Field } from 'dramaeverafter-ds';

export const Text = () => (
  <div style={{ width: 320 }}>
    <Field label="Your name" id="pv-name" placeholder="Optional" />
  </div>
);

export const Email = () => (
  <div style={{ width: 320 }}>
    <Field label="Email" id="pv-email" kind="email" placeholder="Only if you want a reply" hint="Never shared, never sold." />
  </div>
);

export const Select = () => (
  <div style={{ width: 320 }}>
    <Field label="App" id="pv-app" kind="select" options={['ReelShort', 'GoodShort', 'DramaBox', 'Vigloo']} />
  </div>
);

export const Textarea = () => (
  <div style={{ width: 320 }}>
    <Field label="Your message" id="pv-msg" kind="textarea" placeholder="What should we fix?" rows={4} />
  </div>
);
