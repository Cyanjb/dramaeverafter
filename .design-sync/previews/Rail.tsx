import { Rail, PosterCard } from 'dramaeverafter-ds';

export const PosterRail = () => (
  <div style={{ width: 760 }}>
    <Rail>
      <PosterCard railItem title="Blood and Bones of the Disowned Daughter" app="GoodShort" meta="37M views · alpha" saved={false} />
      <PosterCard railItem title="The Double Life of My Billionaire Husband" app="ReelShort" meta="523M views · billionaire" saved={false} />
      <PosterCard railItem title="True Heiress vs. Fake Queen Bee" app="ReelShort" meta="460M views · heiress" saved />
      <PosterCard railItem title="Kidnapped by the Mafia" app="GoodShort" meta="18M views · business" saved={false} />
      <PosterCard railItem sm title="Timeleap Joseon" app="Vigloo" meta="comeback" saved={false} />
    </Rail>
  </div>
);
