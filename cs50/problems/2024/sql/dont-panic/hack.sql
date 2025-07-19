INSERT INTO
    user_logs (
        type,
        "old_username",
        "new_username",
        "old_password",
        "new_password"
    )
SELECT
    'update',
    "u1"."username",
    "u1"."username",
    "u1"."password",
    "u2"."password"
FROM
    (
        SELECT
            "username",
            "password"
        FROM
            "users"
        WHERE
            "username" = 'admin'
    ) AS "u1",
    (
        SELECT
            "username",
            "password"
        FROM
            "users"
        WHERE
            "username" = 'emily33'
    ) AS "u2";

UPDATE "users"
SET
    "password" = '982c0381c279d139fd221fce974916e7'
WHERE
    "username" = 'admin';

DELETE FROM "user_logs"
WHERE
    "new_password" = (
        SELECT
            "password"
        FROM
            "users"
        WHERE
            "username" = 'admin'
    );
