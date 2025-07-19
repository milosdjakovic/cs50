INSERT INTO
    "users" ("first_name", "last_name", "username", "password")
VALUES
    ('Claudine', 'Gay', 'claudine', 'password');

INSERT INTO
    "users" ("first_name", "last_name", "username", "password")
VALUES
    ('Reid', 'Hoffman', 'reid', 'password');

INSERT INTO
    "educational_institutions" ("name", "type", "location", "founded_year")
VALUES
    (
        'Harvard University',
        'Higher Education',
        'Cambridge, Massachusetts',
        1636
    );

INSERT INTO
    "companies" ("name", "industry", "location")
VALUES
    ('LinkedIn', 'Technology', 'Sunnyvale, California');

INSERT INTO
    "enrollment" (
        "user_id",
        "educational_institution_id",
        "start_date",
        "end_date",
        "degree"
    )
VALUES
    (
        (
            SELECT
                "id"
            FROM
                "users"
            WHERE
                "first_name" = 'Claudine'
                AND "last_name" = 'Gay'
        ),
        (
            SELECT
                "id"
            FROM
                "educational_institutions"
            WHERE
                name = 'Harvard'
        ),
        '1993-01-01',
        '1998-12-31',
        'PhD'
    );

INSERT INTO
    "employment" ("user_id", "company_id", "start_date", "end_date")
VALUES
    (
        (
            SELECT
                "id"
            FROM
                "users"
            WHERE
                "first_name" = 'Reid'
                AND "last_name" = 'Hoffman'
        ),
        (
            SELECT
                "id"
            FROM
                "companies"
            WHERE
                "name" = 'LinkedIn'
        ),
        "2003-01-01",
        "2007-02-01"
    )
