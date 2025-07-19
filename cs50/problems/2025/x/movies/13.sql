-- SELECT "name"
-- FROM people
-- WHERE id IN (
--   SELECT person_id
--   FROM stars
--   WHERE movie_id IN (
--     SELECT id
--     FROM movies
--     WHERE id IN (
--       SELECT movie_id
--       FROM stars
--       WHERE person_id = (
--         SELECT id
--         FROM people
--         WHERE "name" = 'Kevin Bacon'
--         AND birth = 1958
--       )
--     )
--   )
-- )
-- AND people.name != 'Kevin Bacon';

SELECT people.name
FROM people
JOIN stars
ON people.id = stars.person_id
JOIN movies
ON movies.id = stars.movie_id
WHERE movies.id IN (
  SELECT movies.id
  FROM movies
  JOIN stars
  ON movies.id = stars.movie_id
  JOIN people
  ON people.id = stars.person_id
  WHERE people.name = 'Kevin Bacon'
  AND birth = 1958
)
AND people.name != 'Kevin Bacon'
