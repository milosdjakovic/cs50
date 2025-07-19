CREATE VIEW
    "by_district" AS
SELECT
    "district",
    SUM("families") AS "families",
    SUM("households") AS "households",
    SUM("population") AS "polulation",
    COUNT("male") AS "count",
    COUNT("female") AS "count"
FROM
    "census"
GROUP BY
    "district";
