import { PosterCard, Grid } from 'dramaeverafter-ds';

export const Canonical = () => (
  <div style={{ width: 174 }}>
    <PosterCard
      title="How to Tame a Silver Fox"
      app="ReelShort"
      meta="417M views · age gap"
      saved={false}
    />
  </div>
);

export const Saved = () => (
  <div style={{ width: 174 }}>
    <PosterCard
      title="The Double Life of My Billionaire Husband"
      app="ReelShort"
      meta="523M views · billionaire"
      saved={true}
    />
  </div>
);

export const WithBadges = () => (
  <div style={{ width: 174 }}>
    <PosterCard
      title="Kissed by Claw and Fang"
      app="ReelShort"
      meta="88M views · werewolf"
      aiBadge
      soonBadge
    />
  </div>
);

export const InAGrid = () => (
  <div style={{ width: 560 }}>
    <Grid>
      <PosterCard title="Married The Mafioso I Saved" app="ReelShort" meta="231M views · mafia" saved={false} />
      <PosterCard title="Mic Drop Diva" app="ReelShort" meta="96M views · fake relationship" saved={false} />
      <PosterCard title="Timeleap Joseon" app="Vigloo" meta="comeback" saved />
    </Grid>
  </div>
);
