SELECT english_title AS "Highest entropy from Hokusai" FROM views WHERE artist = "Hokusai" ORDER BY entropy DESC LIMIT 1;
