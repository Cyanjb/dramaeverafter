import { ActorTile, Grid } from 'dramaeverafter-ds';

export const Single = () => (
  <div style={{ width: 150 }}>
    <ActorTile name="Sarah Moliski" sub="24 titles" initials="SM" />
  </div>
);

export const CirclesGrid = () => (
  <div style={{ width: 480 }}>
    <Grid variant="circles">
      <ActorTile name="Marc Herrmann" sub="32 titles" initials="MH" />
      <ActorTile name="Kasey Esser" sub="31 titles" initials="KE" />
      <ActorTile name="Seth Edeen" sub="31 titles" initials="SE" />
      <ActorTile name="Jackson Tiller" sub="27 titles" initials="JT" />
    </Grid>
  </div>
);
