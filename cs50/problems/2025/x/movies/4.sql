-- SELECT COUNT(*)
-- FROM movies
-- WHERE id IN (
--   SELECT movie_id
--   FROM ratings
--   WHERE rating = '10.0'
-- );

SELECT COUNT(*)
FROM ratings
JOIN movies
ON ratings.movie_id = movies.id
WHERE ratings.rating = '10.0';
