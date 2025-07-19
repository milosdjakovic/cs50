CREATE TABLE
    IF NOT EXISTS "users" (
        "id" INTEGER,
        "first_name" TEXT NOT NULL,
        "last_name" TEXT NOT NULL,
        "username" TEXT NOT NULL UNIQUE,
        "password" TEXT NOT NULL,
        PRIMARY KEY ("id")
    );

CREATE TABLE
    IF NOT EXISTS "educational_institutions" (
        "id" INTEGER,
        "name" TEXT NOT NULL UNIQUE,
        "type" TEXT NOT NULL CHECK (
            "type" IN ('Primary', 'Secondary', 'Higher Education')
        ),
        "location" TEXT NOT NULL,
        "founded_year" INTEGER NOT NULL,
        PRIMARY KEY ("id")
    );

CREATE TABLE
    IF NOT EXISTS "companies" (
        "id" INTEGER,
        "name" TEXT NOT NULL UNIQUE,
        "industry" TEXT NOT NULL CHECK (
            "industry" IN ("Technology", "Education", "Business")
        ),
        "location" TEXT NOT NULL,
        PRIMARY KEY ("id")
    );

CREATE TABLE
    IF NOT EXISTS "connection" (
        "id" INTEGER,
        "user_a_id" INTEGER NOT NULL,
        "user_b_id" INTEGER NOT NULL,
        "created_at" DATETIME DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY ("id"),
        FOREIGN KEY ("user_a_id") REFERENCES "users" ("id"),
        FOREIGN KEY ("user_b_id") REFERENCES "users" ("id"),
        UNIQUE ("user_a_id", "user_b_id")
    );

CREATE TABLE
    IF NOT EXISTS "enrollment" (
        "id" INTEGER,
        "user_id" INTEGER NOT NULL,
        "educational_institution_id" INTEGER NOT NULL,
        "start_date" DATETIME NOT NULL,
        "end_date" DATETIME NOT NULL,
        "degree" TEXT NOT NULL,
        PRIMARY KEY ("id"),
        FOREIGN KEY ("user_id") REFERENCES "users" ("id"),
        FOREIGN KEY ("educational_institution_id") REFERENCES "educational_institutions" ("id"),
        CHECK ("end_date" > "start_date")
    );

CREATE TABLE
    IF NOT EXISTS "employment" (
        "id" INTEGER,
        "user_id" INTEGER NOT NULL,
        "company_id" INTEGER NOT NULL,
        "start_date" DATETIME NOT NULL,
        "end_date" DATETIME NOT NULL,
        PRIMARY KEY ("id"),
        FOREIGN KEY ("user_id") REFERENCES "users" ("id"),
        FOREIGN KEY ("company_id") REFERENCES "companies" ("id"),
        CHECK ("end_date" > "start_date")
    );
