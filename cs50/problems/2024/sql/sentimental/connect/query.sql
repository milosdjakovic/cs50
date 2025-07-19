SELECT
    *
FROM
    `users`
WHERE
    `username` = 'claudine';

SELECT
    *
FROM
    `users`
WHERE
    `username` = 'reid';

SELECT
    *
FROM
    `educational_institutions`
WHERE
    `name` = 'Harvard University';

SELECT
    *
FROM
    `companies`
WHERE
    `name` = 'LinkedIn';

SELECT
    `users`.`first_name`,
    `users`.`last_name`,
    `educational_institutions`.`name`,
    `enrollments`.`degree`,
    `enrollments`.`start_date`,
    `enrollments`.`end_date`
FROM
    `users`
    JOIN `enrollments` ON `users`.`id` = `enrollments`.`user_id`
    JOIN `educational_institutions` ON `enrollments`.`educational_institution_id` = `educational_institutions`.`id`
WHERE
    `users`.`first_name` = 'Claudine'
    AND `users`.`last_name` = 'Gay';

SELECT
    `users`.`first_name`,
    `users`.`last_name`,
    `companies`.`name`,
    `employments`.`start_date`,
    `employments`.`end_date`
FROM
    `users`
    JOIN `employments` ON `users`.`id` = `employments`.`user_id`
    JOIN `companies` ON `employments`.`company_id` = `companies`.`id`
WHERE
    `users`.`first_name` = 'Reid'
    AND `users`.`last_name` = 'Hoffman';
