SELECT strftime('%Y', air_date) AS year, MIN(strftime('%m-%d', air_date)) AS first_release FROM episodes GROUP BY year;
