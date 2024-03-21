-- List bands with Glam rock as main style, ranked by longevity
-- Script should execute on any database

SELECT band_name, COALESCE(split, 2022) - formed as lifespan FROM metal_bands
WHERE style LIKE '%Glam rock%' ORDER BY lifespan DESC;
