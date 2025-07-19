-- DROP VIEW IF EXISTS "june_vacancies";
CREATE VIEW
    "june_vacancies" AS
SELECT
    "listings"."id" AS "id",
    "listings"."property_type" AS "property_type",
    "listings"."host_name" AS "host_name",
    COUNT("listings") AS "days_vacant"
FROM
    "listings"
    JOIN "availabilities" ON "listings"."id" = "availabilities"."listing_id"
WHERE
    "availabilities"."available" = "TRUE"
    AND (
        "availabilities"."date" >= "2023-06-01"
        AND "availabilities"."date" <= "2023-06-30"
    )
GROUP BY
    "listings"."id";

-- SELECT
--     *
-- FROM
--     "june_vacancies"
-- LIMIT
--     5;
