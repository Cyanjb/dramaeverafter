import { AppTile, Grid } from 'dramaeverafter-ds';

export const Single = () => (
  <div style={{ width: 180 }}>
    <AppTile name="ReelShort" caption="575 titles" />
  </div>
);

export const AppsGrid = () => (
  <div style={{ width: 560 }}>
    <Grid variant="apps">
      <AppTile name="GoodShort" caption="1,835 titles" />
      <AppTile name="ReelShort" caption="575 titles" />
      <AppTile name="Vigloo" caption="193 titles" />
      <AppTile name="My Drama" caption="186 titles" />
      <AppTile name="NetShort" caption="168 titles" />
      <AppTile name="CandyJar" caption="96 titles" />
    </Grid>
  </div>
);
