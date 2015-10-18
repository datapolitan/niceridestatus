DROP TABLE IF EXISTS niceride_mn.nr_city_stats;

CREATE TABLE niceride_mn.nr_city_stats (
    execution_time timestamp,
    minneapolis int,
    st_paul int,
    falcon_heights int,
    golden_valley int,
    fort_snelling int
);

COMMENT ON TABLE niceride_mn.nr_city_stats IS 'Values from each run of the niceridestatus.py';

