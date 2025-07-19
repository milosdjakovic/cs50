CREATE TABLE
    "passengers" (
        "id" INTEGER,
        "first_name" TEXT NOT NULL,
        "last_name" TEXT NOT NULL,
        "age" INTEGER NOT NULL,
        PRIMARY KEY ("id")
    );

CREATE TABLE
    "checkins" (
        "id" INTEGER,
        "checkin_time" DATETIME NOT NULL,
        "flight_id" INTEGER NOT NULL,
        "passenger_id" "flight_id" INTEGER NOT NULL,
        PRIMARY KEY ("id"),
        FOREIGN KEY ("flight_id") REFERENCES "flights" ("id"),
        FOREIGN KEY ("passenger_id") REFERENCES "passengers" ("id")
    );

CREATE TABLE
    "airlines" (
        "id" INTEGER,
        "name" INTEGER NOT NULL,
        PRIMARY KEY ("id")
    );

CREATE TABLE
    "concourses" (
        airline_id INTEGER NOT NULL,
        concourse TEXT NOT NULL CHECK (concourse IN ('A', 'B', 'C', 'D', 'E', 'F', 'T')),
        PRIMARY KEY (airline_id, concourse),
        FOREIGN KEY (airline_id) REFERENCES airlines (id)
    );

CREATE TABLE
    "flights" (
        "id" INTEGER,
        "flight_number" TEXT NOT NULL,
        "airline_id" INTEGER,
        "origin" TEXT NOT NULL,
        "destination" TEXT NOT NULL,
        "departure_time" DATETIME,
        "arrival_time" DATETIME,
        PRIMARY KEY ("id"),
        FOREIGN KEY ("airline_id") REFERENCES "airlines" ("id")
    );
