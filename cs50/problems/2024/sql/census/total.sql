CREATE VIEW
    "total" AS
SELECT
    SUM("families") AS "families",
    SUM("households") AS "households",
    SUM("population") AS "polulation",
    COUNT("male") AS "male",
    COUNT("female") AS "female"
FROM
    "census";
