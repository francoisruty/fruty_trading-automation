CREATE DATABASE trading;

USE trading;

-- SET explicit_defaults_for_timestamp = 1;

-- DROP TABLE IF EXISTS tblForex;
CREATE TABLE trading.tblForex
(
    date date null,
    open     float,
    high     float,
    low      float,
    close    float,
    volume   float,
    average  float
);
