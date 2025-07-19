DROP TABLE IF EXISTS "book_cypher";

DROP VIEW IF EXISTS "message";

CREATE TABLE
    IF NOT EXISTS "book_cypher" (
        "sentence_number" TEXT NOT NULL,
        "character_number" TEXT NOT NULL,
        "message_length" TEXT NOT NULL
    );

INSERT INTO
    "book_cypher" (
        "sentence_number",
        "character_number",
        "message_length"
    )
VALUES
    (14, 98, 4),
    (114, 3, 5),
    (618, 72, 9),
    (630, 7, 3),
    (932, 12, 5),
    (2230, 50, 7),
    (2346, 44, 10),
    (3041, 14, 5);

CREATE VIEW
    "message" AS
SELECT
    substr (
        "sentences"."sentence",
        "book_cypher"."character_number",
        "book_cypher"."message_length"
    ) AS "phrase"
FROM
    "sentences"
    JOIN "book_cypher" ON "sentences"."id" = "book_cypher"."sentence_number";
