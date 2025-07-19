CREATE TABLE
    "ingredients" (
        "id" INTEGER,
        "name" TEXT NOT NULL,
        "unit" TEXT NOT NULL,
        "price" INTEGER NOT NULL,
        PRIMARY KEY ("id")
    );

CREATE TABLE
    "donuts" (
        "id" INTEGER,
        "name" TEXT NOT NULL,
        "gluten_free" INTEGER NOT NULL CHECK ("gluten_free" IN (0, 1)),
        "price" INTEGER NOT NULL CHECK ("price" > 0),
        PRIMARY KEY ("id")
    );

CREATE TABLE
    "donuts_ingredients" (
        "ingredient_id" INTEGER,
        "donut_id" INTEGER NOT NULL,
        PRIMARY KEY ("ingredient_id", "donut_id"),
        FOREIGN KEY ("ingredient_id") REFERENCES "ingredients" ("id"),
        FOREIGN KEY ("donut_id") REFERENCES "donuts" ("id")
    );

CREATE TABLE
    "orders" (
        "id" INTEGER,
        "order_number" TEXT NOT NULL,
        "customer_id" INTEGER,
        PRIMARY KEY ("id"),
        FOREIGN KEY ("customer_id") REFERENCES "customers" ("id")
    );

CREATE TABLE
    "order_items" (
        "order_id" INTEGER,
        "donut_id" INTEGER,
        "amount" INTEGER NOT NULL,
        PRIMARY KEY ("order_id", "donut_id"),
        FOREIGN KEY ("order_id") REFERENCES "orders" ("id"),
        FOREIGN KEY ("donut_id") REFERENCES "donuts" ("id")
    );

CREATE TABLE
    "customers" (
        "id" INTEGER,
        "first_name" TEXT NOT NULL,
        "last_name" TEXT NOT NULL,
        PRIMARY KEY ("id")
    );
