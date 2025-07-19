-- DROP VIEW IF EXISTS "no_descriptions";
CREATE VIEW
    "no_descriptions" AS
SELECT
    "id",
    "property_type",
    "host_name",
    "accommodates",
    "bedrooms"
FROM
    "listings";

-- SELECT
--     *
-- FROM
--     "no_descriptions"
-- LIMIT
--     5;
