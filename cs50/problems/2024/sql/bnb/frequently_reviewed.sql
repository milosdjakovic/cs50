-- DROP VIEW IF EXISTS "frequently_reviewed";
CREATE VIEW
    "frequently_reviewed" AS
SELECT
    "listings"."id" AS "id",
    "listings"."property_type" AS "property_type",
    "listings"."host_name" AS "host_name",
    COUNT("reviews") AS "reviews"
FROM
    "listings"
    JOIN "reviews" ON "listings"."id" = "reviews"."listing_id"
GROUP BY
    "listings"."id"
ORDER BY
    "reviews" DESC,
    "property_type" ASC,
    "host_name" ASC
LIMIT
    100;

-- SELECT
--     *
-- FROM
--     "frequently_reviewed"
-- LIMIT
--     5;
