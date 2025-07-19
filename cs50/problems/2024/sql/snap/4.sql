-- EXPLAIN QUERY PLAN
SELECT
    "users"."username"
FROM
    "messages"
    JOIN "users" ON "messages"."to_user_id" = "users"."id"
GROUP BY
    "messages"."to_user_id"
ORDER BY
    COUNT("messages") DESC
LIMIT
    1;
