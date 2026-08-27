import { Chips, Chip, ChipAll } from 'dramaeverafter-ds';

export const TropeRow = () => (
  <div style={{ width: 620 }}>
    <Chips>
      <Chip label="toxic love" count="1,661" href="#" />
      <Chip label="sweet" count="1,632" href="#" />
      <Chip label="reborn" count="1,558" href="#" />
      <Chip label="cute kids" count="1,172" href="#" />
      <Chip label="misunderstanding" count="1,077" href="#" />
      <ChipAll label="All 178 tropes →" href="#" />
    </Chips>
  </div>
);

export const TightFilters = () => (
  <div style={{ width: 300 }}>
    <Chips tight>
      <Chip label="billionaire" state="on" />
      <Chip label="revenge" href="#" />
      <Chip label="mafia" href="#" />
      <Chip label="werewolf" state="off" />
    </Chips>
  </div>
);
