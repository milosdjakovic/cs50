SELECT
  AVG(danceability) AS danceability,
  AVG(energy) AS energy,
  AVG(loudness) AS loudness,
  AVG(speechiness) AS speechiness,
  AVG(valence) AS valence,
  AVG(tempo) AS tempo
FROM songs;

SELECT
  MAX(danceability) AS danceability,
  MAX(energy) AS energy,
  MAX(loudness) AS loudness,
  MAX(speechiness) AS speechiness,
  MAX(valence) AS valence,
  MAX(tempo) AS tempo
FROM songs;

SELECT
  MIN(danceability) AS danceability,
  MIN(energy) AS energy,
  MIN(loudness) AS loudness,
  MIN(speechiness) AS speechiness,
  MIN(valence) AS valence,
  MIN(tempo) AS tempo
FROM songs;
