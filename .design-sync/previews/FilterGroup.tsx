import { FilterGroup, Chips, Chip } from 'dramaeverafter-ds';

export const Tropes = () => (
  <div style={{ width: 300 }}>
    <FilterGroup title="Tropes" hint="Pick any — titles matching all of them show.">
      <Chips tight>
        <Chip label="billionaire" state="on" />
        <Chip label="revenge" href="#" />
        <Chip label="mafia" href="#" />
        <Chip label="sweet" href="#" />
      </Chips>
    </FilterGroup>
  </div>
);

export const Apps = () => (
  <div style={{ width: 300 }}>
    <FilterGroup title="App">
      <Chips tight>
        <Chip label="ReelShort" count="575" href="#" />
        <Chip label="GoodShort" count="1,835" state="on" />
        <Chip label="Vigloo" count="193" href="#" />
      </Chips>
    </FilterGroup>
  </div>
);
