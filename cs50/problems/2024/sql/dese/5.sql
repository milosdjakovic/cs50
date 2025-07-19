SELECT
    "city",
    COUNT(type) AS "Public School Number"
FROM
    "schools"
WHERE
    "type" = 'Public School'
GROUP BY
    "city"
HAVING
    "Public School Number" <= 3
ORDER BY
    "Public School Number" DESC,
    "city" ASC;
