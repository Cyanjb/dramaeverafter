import { EmptyState } from 'dramaeverafter-ds';

export const MyListEmpty = () => (
  <div style={{ width: 460 }}>
    <EmptyState title="Nothing saved yet">
      Tap the ★ on any title and it will wait for you here — no account needed.
    </EmptyState>
  </div>
);

export const NoResults = () => (
  <div style={{ width: 460 }}>
    <EmptyState title="No titles match">
      Try fewer filters, or search for the actor instead.
    </EmptyState>
  </div>
);
