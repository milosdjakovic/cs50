-- EXPLAIN QUERY PLAN
SELECT
    "receivers"."id"
FROM
    "users"
    JOIN "messages" ON "users"."id" = "messages"."from_user_id"
    JOIN "users" AS "receivers" ON "messages"."to_user_id" = "receivers"."id"
WHERE
    "users"."username" = 'creativewisdom377'
GROUP BY
    "messages"."to_user_id"
ORDER BY
    COUNT("messages") DESC
LIMIT
    3;
