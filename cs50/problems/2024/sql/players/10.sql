SELECT first_name, last_name, height AS "Height (in)" FROM players WHERE birth_state = "NY" AND bats = "L" AND throws = "L" ORDER BY height DESC, first_name ASC, last_name ASC LIMIT 10;
