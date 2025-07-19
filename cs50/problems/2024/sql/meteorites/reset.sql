DROP TABLE IF EXISTS "meteorites_temp";

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

-- .import --csv --skip 1 meteorites.csv meteorites_temp
