SELECT
    *
FROM
    "users"
WHERE
    "username" = 'claudine';

SELECT
    *
FROM
    "users"
WHERE
    "username" = 'reid';

SELECT
    *
FROM
    "educational_institutions"
WHERE
    "name" = 'Harvard University';

SELECT
    *
FROM
    "companies"
WHERE
    "name" = 'LinkedIn';

SELECT
    "users"."first_name",
    "users"."last_name",
    "educational_institutions"."name",
    "enrollment"."degree",
    "enrollment"."start_date",
    "enrollment"."end_date"
FROM
    "users"
    JOIN "enrollment" ON "users"."id" = "enrollment"."user_id"
    JOIN "educational_institutions" ON "enrollment"."educational_institution_id" = "educational_institutions"."id"
WHERE
    "users"."first_name" = 'Claudine'
    AND "users"."last_name" = 'Gay';

SELECT
    "users"."first_name",
    "users"."last_name",
    "companies"."name",
    "employment"."start_date",
    "employment"."end_date"
FROM
    "users"
    JOIN "employment" ON "users"."id" = "employment"."user_id"
    JOIN "companies" ON "employment"."company_id" = "companies"."id"
WHERE
    "users"."first_name" = 'Reid'
    AND "users"."last_name" = 'Hoffman';

;
