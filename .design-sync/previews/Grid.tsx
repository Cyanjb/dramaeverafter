import { Grid, PosterCard, AppTile, TropeIdxRow } from 'dramaeverafter-ds';

export const Posters = () => (
  <div style={{ width: 560 }}>
    <Grid>
      <PosterCard title="Mic Drop Diva" app="ReelShort" meta="96M views" saved={false} />
      <PosterCard title="Meet My Brothers" app="ReelShort" meta="54M views" saved={false} />
      <PosterCard title="Gideon" app="CandyJar" saved={false} />
    </Grid>
  </div>
);

export const Apps = () => (
  <div style={{ width: 560 }}>
    <Grid variant="apps">
      <AppTile name="GoodShort" caption="1,835 titles" />
      <AppTile name="ReelShort" caption="575 titles" />
      <AppTile name="NetShort" caption="168 titles" />
    </Grid>
  </div>
);

export const TropeIndex = () => (
  <div style={{ width: 560 }}>
    <Grid variant="tropeIdx">
      <TropeIdxRow name="billionaire" count="1,036" />
      <TropeIdxRow name="contract marriage" count="1,032" />
      <TropeIdxRow name="cinderella" count="849" />
      <TropeIdxRow name="love triangle" count="837" />
    </Grid>
  </div>
);
