-- Insert sample users into the users table.
-- These users will serve as both providers and clients in the test data.
INSERT INTO
    `users` (
        `first_name`,
        `last_name`,
        `email`,
        `password`
    )
VALUES (
        'John',
        'Doe',
        'johndoe@example.com',
        '5XyEiHPhCFzP3izS5DBLW6WWpmCTGilJ'
    );

INSERT INTO
    `users` (
        `first_name`,
        `last_name`,
        `email`,
        `password`
    )
VALUES (
        'Mike',
        'Smith',
        'mikesmith@example.com',
        'dWaLQAP23gXjnPv42ZNXPoVQEIKP6XHR'
    );

INSERT INTO
    `users` (
        `first_name`,
        `last_name`,
        `email`,
        `password`
    )
VALUES (
        'Emily',
        'Clark',
        'emilyclark@example.com',
        'ZoItEkWtmHZ3eZ6B6kwORjqWCOdHe9AE'
    );

INSERT INTO
    `users` (
        `first_name`,
        `last_name`,
        `email`,
        `password`
    )
VALUES (
        'Daniel',
        'Hughes',
        'danielhughes@example.com',
        'uu4V6yGhD1iJOv8DQSKrDdpuelDrMNYv'
    );

INSERT INTO
    `users` (
        `first_name`,
        `last_name`,
        `email`,
        `password`
    )
VALUES (
        'Chloe',
        'Richardson',
        'chloerichardson@example.com',
        'IaXAVyF41ULARxZ0bakv6z8P7SOjLdK4'
    );

-- Confirm the inserted users.
SELECT * FROM `users`;

-- Connect users to establish provider-client relationships.
-- John is provider to Mike and Emily.
-- Daniel is provider to Emily.
INSERT INTO
    `connections` (`provider_id`, `client_id`)
VALUES (
        (
            SELECT `id`
            FROM `users`
            WHERE
                `email` = 'johndoe@example.com'
            LIMIT 1
        ),
        (
            SELECT `id`
            FROM `users`
            WHERE
                `email` = 'mikesmith@example.com'
            LIMIT 1
        )
    );

INSERT INTO
    `connections` (`provider_id`, `client_id`)
VALUES (
        (
            SELECT `id`
            FROM `users`
            WHERE
                `email` = 'johndoe@example.com'
            LIMIT 1
        ),
        (
            SELECT `id`
            FROM `users`
            WHERE
                `email` = 'emilyclark@example.com'
            LIMIT 1
        )
    );

INSERT INTO
    `connections` (`provider_id`, `client_id`)
VALUES (
        (
            SELECT `id`
            FROM `users`
            WHERE
                `email` = 'danielhughes@example.com'
            LIMIT 1
        ),
        (
            SELECT `id`
            FROM `users`
            WHERE
                `email` = 'emilyclark@example.com'
            LIMIT 1
        )
    );

-- Confirm the connections were established.
SELECT `clients`.`email` AS `client_email`
FROM
    `connections`
    JOIN `users` AS `providers` ON `connections`.`provider_id` = `providers`.`id`
    JOIN `users` AS `clients` ON `connections`.`client_id` = `clients`.`id`
WHERE
    `providers`.`email` = 'johndoe@example.com';

-- Insert appointment slots for providers.
-- One in the past to test filtering.
-- NOW() - INTERVAL 2 DAY ensures the slot is in the past relative to when the query is run.
INSERT INTO
    `slots` (`provider_id`, `slot_time`)
VALUES (
        (
            SELECT `id`
            FROM `users`
            WHERE
                `email` = 'johndoe@example.com'
            LIMIT 1
        ),
        NOW() - INTERVAL 2 DAY
    );

-- Insert a fixed date slot.
INSERT INTO
    `slots` (`provider_id`, `slot_time`)
VALUES (
        (
            SELECT `id`
            FROM `users`
            WHERE
                `email` = 'johndoe@example.com'
            LIMIT 1
        ),
        '2025-10-15 13:45:00'
    );

-- Insert a future slot using NOW() + INTERVAL 2 DAY so that it always remains in the future.
INSERT INTO
    `slots` (`provider_id`, `slot_time`)
VALUES (
        (
            SELECT `id`
            FROM `users`
            WHERE
                `email` = 'johndoe@example.com'
            LIMIT 1
        ),
        NOW() + INTERVAL 2 DAY
    );

-- Insert another future slot for a different provider.
INSERT INTO
    `slots` (`provider_id`, `slot_time`)
VALUES (
        (
            SELECT `id`
            FROM `users`
            WHERE
                `email` = 'danielhughes@example.com'
            LIMIT 1
        ),
        NOW() + INTERVAL 1 DAY
    );

-- Confirm slots were created correctly.
SELECT * FROM `slots`;

-- Use the view to list all providers for a specific client.
SELECT
    `provider_first_name`,
    `provider_last_name`,
    `provider_email`
FROM `client_providers`
WHERE
    `client_email` = 'emilyclark@example.com';

-- List all available appointment slots for a client along with their providers.
-- Helps clients browse available appointments.
SELECT `providers`.`first_name`, `providers`.`last_name`, `providers`.`email`, `slots`.`slot_time`, `slots`.`is_booked`
FROM
    `users` AS `clients`
    JOIN `connections` ON `clients`.`id` = `connections`.`client_id`
    JOIN `users` AS `providers` ON `connections`.`provider_id` = `providers`.`id`
    JOIN `slots` ON `providers`.`id` = `slots`.`provider_id`
WHERE
    `clients`.`email` = 'emilyclark@example.com';

-- Book an appointment using stored procedure
CALL `book_appointment` (
    'johndoe@example.com',
    'emilyclark@example.com',
    '2025-10-15 13:45:00'
);

-- Update the slot to reflect that it's now booked.
UPDATE `slots`
JOIN `users` AS `providers` ON `slots`.`provider_id` = `providers`.`id`
SET
    `slots`.`is_booked` = TRUE
WHERE
    `slots`.`slot_time` = '2025-10-15 13:45:00'
    AND `providers`.`email` = 'johndoe@example.com';

COMMIT;

-- Check that booking updated both slots and appointments.
SELECT * FROM `slots`;

SELECT * FROM `appointments`;

-- List only appointments that have been booked by a specific client.
SELECT `providers`.`first_name`, `providers`.`last_name`, `providers`.`email`, `slots`.`slot_time`
FROM
    `users` AS `clients`
    JOIN `connections` ON `clients`.`id` = `connections`.`client_id`
    JOIN `users` AS `providers` ON `connections`.`provider_id` = `providers`.`id`
    JOIN `slots` ON `providers`.`id` = `slots`.`provider_id`
WHERE
    `clients`.`email` = 'emilyclark@example.com'
    AND `slots`.`is_booked` = TRUE;

-- List provider's clients.
SELECT
    `client_first_name`,
    `client_last_name`,
    `client_email`
FROM `provider_clients`
WHERE
    `provider_email` = 'johndoe@example.com';

-- Query provider appointments.
SELECT
    `client_first_name`,
    `client_last_name`,
    `client_email`,
    `slot_time`,
    `booked_at`
FROM `provider_appointments`
WHERE
    `provider_email` = 'johndoe@example.com';

-- Get only future provider appointments.
SELECT
    `client_first_name`,
    `client_last_name`,
    `client_email`,
    `slot_time`,
    `booked_at`
FROM `provider_appointments`
WHERE
    `provider_email` = 'johndoe@example.com'
    AND `slot_time` > CURRENT_TIMESTAMP;

-- Get only past provider appointments.
SELECT
    `client_first_name`,
    `client_last_name`,
    `client_email`,
    `slot_time`,
    `booked_at`
FROM `provider_appointments`
WHERE
    `provider_email` = 'johndoe@example.com'
    AND `slot_time` < CURRENT_TIMESTAMP;

-- View client appointments by email.
SELECT
    `provider_first_name`,
    `provider_last_name`,
    `provider_email`,
    `slot_time`,
    `booked_at`
FROM `client_appointments`
WHERE
    `client_email` = 'emilyclark@example.com';

-- Filter future appointments for the client.
SELECT
    `provider_first_name`,
    `provider_last_name`,
    `provider_email`,
    `slot_time`,
    `booked_at`
FROM `client_appointments`
WHERE
    `client_email` = 'emilyclark@example.com'
    AND `slot_time` > CURRENT_TIMESTAMP;

-- Filter past appointments for the client.
SELECT
    `provider_first_name`,
    `provider_last_name`,
    `provider_email`,
    `slot_time`,
    `booked_at`
FROM `client_appointments`
WHERE
    `client_email` = 'emilyclark@example.com'
    AND `slot_time` < CURRENT_TIMESTAMP;

-- Delete user by calling a stored procedure
CALL `delete_user_by_email` ('emilyclark@example.com');