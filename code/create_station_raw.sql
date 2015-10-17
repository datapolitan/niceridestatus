DROP TABLE IF EXISTS niceride_mn.station_raw;

CREATE TABLE niceride_mn.station_raw (
    id int,
    name text,
    terminalName text,
    latestUpdateTime timestamp,
    lastCommWithServer timestamp,
    lat numeric,
    long numeric,
    installed boolean,
    locked boolean,
    installDate text,
    removalDate text,
    temporary boolean,
    public boolean,
    nbBikes int,
    nbEmptyDocks int
);

COMMENT TABLE ON niceride_mn.station_raw IS 'A sample of the station info xml to extract lat lon';

ALTER TABLE niceride_mn.station_raw ADD COLUMN geom geometry(POINT,4326);

UPDATE niceride_mn.station_raw SET geom = ST_SetSRID(ST_MakePoint(long,lat),4326);