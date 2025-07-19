UPDATE "meteorites_temp"
SET
    "mass" = NULL
WHERE
    TRIM("mass") = '';
