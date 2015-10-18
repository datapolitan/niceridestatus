--Average by hour for the plot

WITH hour_ex AS (
    SELECT 
        extract(hour from execution_time) as hour_ex, 
        minneapolis,
        st_paul,
        falcon_heights,
        golden_valley,
        fort_snelling 
    FROM niceride_mn.nr_city_stats
    --account for the 4 hours for UTC
    WHERE execution_time >= now() - interval '28 hours'
    )

SELECT 
    hour_ex,
    ROUND(AVG(minneapolis),0) AS minneapolis,
    ROUND(AVG(st_paul),0) AS st_paul,
    ROUND(AVG(falcon_heights + golden_valley + fort_snelling),0) AS other_city
FROM hour_ex
GROUP BY hour_ex
ORDER BY hour_ex;
