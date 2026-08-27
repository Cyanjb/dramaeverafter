import { Pagination } from 'dramaeverafter-ds';

export const Middle = () => (
  <div style={{ width: 500 }}>
    <Pagination prevHref="#" nextHref="#" status="Page 2 of 9" />
  </div>
);

export const FirstPage = () => (
  <div style={{ width: 500 }}>
    <Pagination nextHref="#" status="Page 1 of 9" />
  </div>
);
