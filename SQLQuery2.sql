SELECT
    geo.state,
    CAST(SUM(CASE WHEN g.gun_stolen = 'Stolen' THEN c.crime_gravity ELSE 0 END) AS DECIMAL(18, 2)) AS StolenGravity,
    CAST(SUM(CASE WHEN g.gun_stolen IN ('Stolen', 'Not-stolen', 'Unknown') THEN c.crime_gravity ELSE 0 END) AS DECIMAL(18, 2)) AS OverallGravity,
    CASE
        WHEN SUM(CASE WHEN g.gun_stolen = 'Stolen' THEN c.crime_gravity ELSE 0 END) = 0 THEN 0
        ELSE CAST(SUM(CASE WHEN g.gun_stolen = 'Stolen' THEN c.crime_gravity ELSE 0 END) AS DECIMAL(18, 2)) / NULLIF(CAST(SUM(CASE WHEN g.gun_stolen IN ('Stolen', 'Not-stolen', 'Unknown') THEN c.crime_gravity ELSE 0 END) AS DECIMAL(18, 2)), 0)
    END AS StolenGravityIndex
FROM
    Custody c
JOIN
    Gun g ON c.gun_id = g.gun_id
JOIN
    Geography geo ON c.geo_id = geo.geo_id
GROUP BY
    geo.state;




