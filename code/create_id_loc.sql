DROP TABLE IF EXISTS niceride_mn.id_loc;

CREATE TABLE niceride_mn.id_loc (
    station_id int PRIMARY KEY,
    geom geometry(POINT,4326),
    created_at TIMESTAMP WITH TIME ZONE
    );

COMMENT ON TABLE niceride_mn.id_loc IS 'Normalized table of ids and geom';
