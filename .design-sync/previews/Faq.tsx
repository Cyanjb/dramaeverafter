import { Faq } from 'dramaeverafter-ds';

export const Canonical = () => (
  <div style={{ width: 640 }}>
    <Faq
      items={[
        { q: 'Is DramaEverAfter free?', a: 'Yes. We index the dramas; the apps stream them. Some links earn us a commission.', open: true },
        { q: 'Why is a title missing?', a: 'The apps release faster than any database can blink. Tell us via the contact page and we will add it.' },
        { q: 'Do you host any episodes?', a: 'No — every watch button opens the app that actually streams the title.' },
      ]}
      note="Answers checked against the apps, not press releases."
    />
  </div>
);
