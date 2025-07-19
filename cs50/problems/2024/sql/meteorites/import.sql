CREATE TABLE
    "meteorites_temp" (
        "name" TEXT,
        "id" INTEGER,
        "nametype" TEXT,
        "class" TEXT,
        "mass" REAL,
        "discovery" TEXT,
        "year" INTEGER,
        "lat" REAL,
        "long" REAL
    );

.import --csv --skip 1 meteorites.csv meteorites_temp

-- %%% UPDATE NULL VALUES START %%%
UPDATE "meteorites_temp"
SET
    "mass" = NULL
WHERE
    TRIM("mass") = '';

UPDATE "meteorites_temp"
SET
    "year" = NULL
WHERE
    TRIM("year") = '';

UPDATE "meteorites_temp"
SET
    "lat" = NULL
WHERE
    TRIM("lat") = '';

UPDATE "meteorites_temp"
SET
    "long" = NULL
WHERE
    TRIM("long") = '';

-- %%% ROUND TO 2 DECIMALS %%%
UPDATE "meteorites_temp"
SET
    "mass" = ROUND("mass", 2);

UPDATE "meteorites_temp"
SET
    "lat" = ROUND("lat", 2);

UPDATE "meteorites_temp"
SET
    "long" = ROUND("long", 2);

-- %%% DELETE RELICT METEORITES %%%
DELETE FROM "meteorites_temp"
WHERE
    "nametype" = 'Relict';

DROP TABLE IF EXISTS "meteorites";

-- %%% CREATE METEORITES %%%
CREATE TABLE
    "meteorites" (
        "id" INTEGER,
        "name" TEXT,
        "class" TEXT,
        "mass" REAL,
        "discovery" TEXT CHECK("discovery" IN ("Fell","Found")),
        "year" INTEGER,
        "lat" REAL,
        "long" REAL,
        PRIMARY KEY ("id")
    );

-- -- %%% COPY INTO METEORITES TABLE %%%
INSERT INTO
    "meteorites" (
        "name",
        "class",
        "mass",
        "discovery",
        "year",
        "lat",
        "long"
    )
SELECT
    "name",
    "class",
    "mass",
    "discovery",
    "year",
    "lat",
    "long"
FROM
    "meteorites_temp"
ORDER BY
    "year" ASC,
    "name" ASC;
