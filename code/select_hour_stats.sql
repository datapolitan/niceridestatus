SELECT 
    ROUND(AVG(minneapolis)) AS minneapolis,
    ROUND(AVG(st_paul)) AS st_paul,
    ROUND(AVG(falcon_heights + golden_valley + fort_snelling)) AS other
FROM niceride_mn.nr_city_stats
WHERE execution_time >= NOW() - INTERVAL '1 hour'