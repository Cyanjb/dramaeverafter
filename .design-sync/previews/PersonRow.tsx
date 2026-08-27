import { PersonRow, Grid } from 'dramaeverafter-ds';

export const Single = () => (
  <div style={{ width: 300 }}>
    <PersonRow name="Sarah Moliski" sub="as Vivian Cole" initials="SM" />
  </div>
);

export const CastGrid = () => (
  <div style={{ width: 560 }}>
    <Grid variant="cast">
      <PersonRow name="Marc Herrmann" sub="as Damian Cross" initials="MH" sm />
      <PersonRow name="Kasey Esser" sub="as Ethan Reed" initials="KE" sm />
      <PersonRow name="Haley Lohrli" sub="as Aurora West" initials="HL" sm />
      <PersonRow name="Jesse Morales" sub="as Marco Valen" initials="JM" sm />
    </Grid>
  </div>
);
