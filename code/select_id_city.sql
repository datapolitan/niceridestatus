-- A simple join to produce stations and the cities in which they fall

SELECT
    il.station_id,
    cb.name
FROM niceride_mn.id_loc il
LEFT OUTER JOIN niceride_mn.city_boundary cb
    ON ST_CONTAINS(ST_TRANSFORM(cb.geom,4326),il.geom);