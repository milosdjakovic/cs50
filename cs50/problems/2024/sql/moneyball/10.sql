SELECT
    players.first_name,
    players.last_name,
    salaries.salary,
    salaries.year,
    performances.year,
    performances.HR
FROM
    players
    JOIN salaries ON players.id = salaries.player_id
    JOIN performances ON players.id = performances.player_id
    AND performances.year = salaries.year
ORDER BY
    players.id ASC,
    salaries.year DESC,
    performances.HR DESC,
    salaries.salary DESC;
