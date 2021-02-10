CREATE TABLE forex_data_EURUSD (
  id BIGSERIAL PRIMARY KEY,
  time timestamp NOT NULL UNIQUE,
  value_open NUMERIC
);
