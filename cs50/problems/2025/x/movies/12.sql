-- SELECT title
-- FROM movies
-- WHERE id IN (
--   SELECT id
--   FROM movies
--   WHERE id IN (
--     SELECT movie_id
--     FROM stars
--     WHERE person_id = (
--       SELECT id
--       FROM people
--       WHERE name = 'Bradley Cooper'
--     )
--   )
-- )
-- AND id IN (
--   SELECT id
--   FROM movies
--   WHERE id IN (
--     SELECT movie_id
--     FROM stars
--     WHERE person_id = (
--       SELECT id
--       FROM people
--       WHERE name = 'Jennifer Lawrence'
--     )
--   )
-- );

SELECT title
FROM movies
WHERE id IN (
  SELECT movies.id
  FROM movies
  JOIN stars
  ON movies.id = stars.movie_id
  JOIN people
  ON stars.person_id = people.id
  WHERE people.name = 'Bradley Cooper'
)
AND id IN (
  SELECT movies.id
  FROM movies
  JOIN stars
  ON movies.id = stars.movie_id
  JOIN people
  ON stars.person_id = people.id
  WHERE people.name = 'Jennifer Lawrence'
);
