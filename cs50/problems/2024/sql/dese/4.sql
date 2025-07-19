SELECT
    city,
    COUNT(type) AS "Public School Number"
FROM
    "schools"
WHERE
    "type" = 'Public School'
GROUP BY
    "city"
ORDER BY
    "Public School Number" DESC,
    "city" ASC
LIMIT
    10;
