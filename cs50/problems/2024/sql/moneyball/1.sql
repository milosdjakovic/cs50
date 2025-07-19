SELECT
    YEAR,
    ROUND(AVG(salary), 2) AS "average salary"
FROM
    salaries
GROUP BY
    YEAR
ORDER BY
    "year" DESC;
