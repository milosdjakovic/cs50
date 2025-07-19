-- SELECT * FROM episodes WHERE air_date LIKE '%-12-%';
SELECT * FROM episodes WHERE strftime('%m', air_date) = '12';
