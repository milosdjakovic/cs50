-- DROP VIEW IF EXISTS "available";
CREATE VIEW
    "available" AS
SELECT
    "listings"."id" AS "id",
    "listings"."property_type" AS "property_type",
    "listings"."host_name" AS "host_name",
    "availabilities"."date" AS "date"
FROM
    "listings"
    JOIN "availabilities" ON "listings"."id" = "availabilities"."listing_id"
WHERE
    "availabilities"."available" = "TRUE";
