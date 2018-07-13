drop table entries;
create table entries (
  id INTEGER primary key,
  name VARCHAR(50) not null,
  type VARCHAR(50) not null,
  amount FLOAT not null,
  price FLOAT not null,
  month1 VARCHAR(50) not null
);