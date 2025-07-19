-- EXPLAIN QUERY PLAN
SELECT
    "friend"."id"
FROM
    "users"
    JOIN "friends" ON "users"."id" = "friends"."user_id"
    JOIN "users" "friend" ON "friends"."friend_id" = "friend"."id"
WHERE
    "users"."username" = 'lovelytrust487'
INTERSECT
SELECT
    "friend"."id"
FROM
    "users"
    JOIN "friends" ON "users"."id" = "friends"."user_id"
    JOIN "users" "friend" ON "friends"."friend_id" = "friend"."id"
WHERE
    "users"."username" = 'exceptionalinspiration482';
