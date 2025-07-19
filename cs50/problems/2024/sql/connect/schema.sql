CREATE TABLE
    "users" (
        "id" INTEGER,
        "first_name" TEXT NOT NULL,
        "last_name" TEXT NOT NULL,
        "username" TEXT NOT NULL,
        "password" TEXT NOT NULL,
        PRIMARY KEY ("id")
    );

CREATE TABLE
    "educational_institutions" (
        "id" INTEGER,
        "name" TEXT NOT NULL,
        "type" TEXT NOT NULL,
        "location" TEXT NOT NULL,
        "founded" INTEGER NOT NULL,
        PRIMARY KEY ("id")
    );

CREATE TABLE
    "companies" (
        "id" INTEGER,
        "name" TEXT NOT NULL,
        "industry" TEXT NOT NULL,
        "location" TEXT NOT NULL,
        PRIMARY KEY ("id")
    );

CREATE TABLE
    "user_connections" (
        "user_id" INTEGER NOT NULL,
        "connected_user_id" INTEGER NOT NULL,
        PRIMARY KEY ("user_id", "connected_user_id"),
        FOREIGN KEY ("user_id") REFERENCES "users" ("id"),
        FOREIGN KEY ("connected_user_id") REFERENCES "users" ("id")
    );

CREATE TABLE
    "user_educational_institutions_affiliations" (
        "user_id" INTEGER NOT NULL,
        "educational_institution_id" INTEGER NOT NULL,
        "start_date" DATETIME NOT NULL,
        "end_date" DATETIME,
        "degree" TEXT NOT NULL,
        PRIMARY KEY ("user_id", "educational_institution_id", "start_date"),
        FOREIGN KEY ("user_id") REFERENCES "users" ("id"),
        FOREIGN KEY ("educational_institution_id") REFERENCES "educational_institutions" ("id")
    );

CREATE TABLE
    "user_company_affiliations" (
        "user_id" INTEGER NOT NULL,
        "company_id" INTEGER NOT NULL,
        "start_date" DATETIME NOT NULL,
        "end_date" DATETIME,
        "title" TEXT NOT NULL,
        PRIMARY KEY ("user_id", "company_id", "start_date"),
        FOREIGN KEY ("user_id") REFERENCES "users" ("id"),
        FOREIGN KEY ("company_id") REFERENCES "companies" ("id")
    );
