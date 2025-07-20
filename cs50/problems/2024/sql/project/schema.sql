-- Drop the database if it already exists (useful during development)
DROP DATABASE IF EXISTS `agenda_ace`;

-- Create the database
CREATE DATABASE IF NOT EXISTS `agenda_ace`;

-- Use the newly created database
USE `agenda_ace`;

-- Table of all users (clients and providers)
CREATE TABLE IF NOT EXISTS `users` (
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `first_name` VARCHAR(50) NOT NULL,
    `last_name` VARCHAR(50) NOT NULL,
    `email` VARCHAR(100) NOT NULL UNIQUE, -- email must be unique
    `password` VARCHAR(100) NOT NULL,
    PRIMARY KEY (`id`)
);

-- Table to connect providers with their clients
CREATE TABLE IF NOT EXISTS `connections` (
    `provider_id` INT UNSIGNED NOT NULL,
    `client_id` INT UNSIGNED NOT NULL,
    PRIMARY KEY (`provider_id`, `client_id`), -- each pair is unique
    FOREIGN KEY (`provider_id`) REFERENCES `users` (`id`),
    FOREIGN KEY (`client_id`) REFERENCES `users` (`id`),
    CHECK (`provider_id` <> `client_id`) -- no self-connections
);

-- Index to speed up client lookups
CREATE INDEX `idx_client_id` ON `connections` (`client_id`);

-- Table where providers define available time slots
CREATE TABLE IF NOT EXISTS `slots` (
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `provider_id` INT UNSIGNED NOT NULL,
    `slot_time` DATETIME NOT NULL, -- the time of the appointment
    `is_booked` BOOLEAN NOT NULL DEFAULT FALSE, -- shows if booked
    PRIMARY KEY (`id`),
    FOREIGN KEY (`provider_id`) REFERENCES `users` (`id`),
    UNIQUE (`provider_id`, `slot_time`) -- no duplicate slots
);

-- Indexes for faster filtering and joins on provider and time
CREATE INDEX `idx_provider_id` ON `slots` (`provider_id`);

CREATE INDEX `idx_slot_time` ON `slots` (`slot_time`);

-- Table to record actual appointments
CREATE TABLE IF NOT EXISTS `appointments` (
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `slot_id` INT UNSIGNED NOT NULL UNIQUE, -- one appointment per slot
    `client_id` INT UNSIGNED NOT NULL,
    `booked_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`slot_id`) REFERENCES `slots` (`id`),
    FOREIGN KEY (`client_id`) REFERENCES `users` (`id`)
);

-- Indexes for faster filtering by client or date
CREATE INDEX `idx_client_id` ON `appointments` (`client_id`);

CREATE INDEX `idx_booked_at` ON `appointments` (`booked_at`);

-- Create a view to simplify getting all providers for a given client.
CREATE VIEW `client_providers` AS
SELECT
    `clients`.`id` AS `client_id`,
    `clients`.`first_name` AS `client_first_name`,
    `clients`.`last_name` AS `client_last_name`,
    `clients`.`email` AS `client_email`,
    `providers`.`id` AS `provider_id`,
    `providers`.`first_name` AS `provider_first_name`,
    `providers`.`last_name` AS `provider_last_name`,
    `providers`.`email` AS `provider_email`
FROM
    `users` AS `clients`
    JOIN `connections` ON `clients`.`id` = `connections`.`client_id`
    JOIN `users` AS `providers` ON `connections`.`provider_id` = `providers`.`id`;

-- Create a view that lists clients for each provider.
CREATE VIEW `provider_clients` AS
SELECT
    `providers`.`id` AS `provider_id`,
    `providers`.`first_name` AS `provider_first_name`,
    `providers`.`last_name` AS `provider_last_name`,
    `providers`.`email` AS `provider_email`,
    `clients`.`id` AS `client_id`,
    `clients`.`first_name` AS `client_first_name`,
    `clients`.`last_name` AS `client_last_name`,
    `clients`.`email` AS `client_email`
FROM
    `users` AS `providers`
    JOIN `connections` ON `providers`.`id` = `connections`.`provider_id`
    JOIN `users` AS `clients` ON `connections`.`client_id` = `clients`.`id`;

-- View for listing all booked provider appointments.
CREATE VIEW `provider_appointments` AS
SELECT
    `providers`.`first_name` AS `provider_first_name`,
    `providers`.`last_name` AS `provider_last_name`,
    `providers`.`email` AS `provider_email`,
    `clients`.`first_name` AS `client_first_name`,
    `clients`.`last_name` AS `client_last_name`,
    `clients`.`email` AS `client_email`,
    `slots`.`slot_time` AS `slot_time`,
    `appointments`.`booked_at` AS `booked_at`
FROM
    `appointments`
    JOIN `users` AS `clients` ON `appointments`.`client_id` = `clients`.`id`
    JOIN `slots` ON `appointments`.`slot_id` = `slots`.`id`
    JOIN `users` AS `providers` ON `slots`.`provider_id` = `providers`.`id`;

-- View for listing client-side booked appointments.
CREATE VIEW `client_appointments` AS
SELECT
    `clients`.`first_name` AS `client_first_name`,
    `clients`.`last_name` AS `client_last_name`,
    `clients`.`email` AS `client_email`,
    `providers`.`first_name` AS `provider_first_name`,
    `providers`.`last_name` AS `provider_last_name`,
    `providers`.`email` AS `provider_email`,
    `slots`.`slot_time` AS `slot_time`,
    `appointments`.`booked_at` AS `booked_at`
FROM
    `appointments`
    JOIN `users` AS `clients` ON `appointments`.`client_id` = `clients`.`id`
    JOIN `slots` ON `appointments`.`slot_id` = `slots`.`id`
    JOIN `users` AS `providers` ON `slots`.`provider_id` = `providers`.`id`;

DELIMITER $$

CREATE PROCEDURE `delete_user_by_email`(IN `target_email` VARCHAR(100))
BEGIN
    DECLARE `target_id` INT;

    -- Get the user ID from the email
    SELECT `id` INTO `target_id`
    FROM `users`
    WHERE `email` = `target_email`;

    START TRANSACTION;

    -- Delete appointments where user is client
    DELETE FROM `appointments` WHERE `client_id` = `target_id`;

    -- Delete appointments where user is provider (via slot)
    DELETE FROM `appointments`
    WHERE `slot_id` IN (
        SELECT `id` FROM `slots` WHERE `provider_id` = `target_id`
    );

    -- Delete slots created by the user
    DELETE FROM `slots` WHERE `provider_id` = `target_id`;

    -- Delete connections where user is involved
    DELETE FROM `connections`
    WHERE `client_id` = `target_id` OR `provider_id` = `target_id`;

    -- Finally, delete the user
    DELETE FROM `users` WHERE `id` = `target_id`;

    COMMIT;
END $$

DELIMITER ;

DELIMITER $$

CREATE PROCEDURE `book_appointment`(
    IN `provider_email` VARCHAR(100),
    IN `client_email` VARCHAR(100),
    IN `appointment_time` DATETIME
)
BEGIN
    DECLARE `slot_id_val` INT;
    DECLARE `client_id_val` INT;

    -- Get the slot ID
    SELECT `slots`.`id`
    INTO `slot_id_val`
    FROM `slots`
    JOIN `users` AS `providers` ON `slots`.`provider_id` = `providers`.`id`
    WHERE `slots`.`slot_time` = `appointment_time`
        AND `providers`.`email` = `provider_email`
    LIMIT 1;

    -- Get the client ID
    SELECT `id`
    INTO `client_id_val`
    FROM `users`
    WHERE `email` = `client_email`
    LIMIT 1;

    START TRANSACTION;

    -- Insert the appointment
    INSERT INTO `appointments` (`slot_id`, `client_id`)
    VALUES (`slot_id_val`, `client_id_val`);

    -- Mark the slot as booked
    UPDATE `slots`
    SET `is_booked` = TRUE
    WHERE `id` = `slot_id_val`;

    COMMIT;
END $$

DELIMITER ;
