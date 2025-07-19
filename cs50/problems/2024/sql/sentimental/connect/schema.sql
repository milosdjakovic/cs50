CREATE DATABASE IF NOT EXISTS `linkedin`;

USE `linkedin`;

CREATE TABLE
    IF NOT EXISTS `users` (
        `id` INT AUTO_INCREMENT,
        `first_name` VARCHAR(50) NOT NULL,
        `last_name` VARCHAR(50) NOT NULL,
        `username` VARCHAR(50) NOT NULL UNIQUE,
        `password` VARCHAR(255) NOT NULL,
        PRIMARY KEY (`id`)
    );

CREATE TABLE
    IF NOT EXISTS `educational_institutions` (
        `id` INT AUTO_INCREMENT,
        `name` VARCHAR(150) NOT NULL UNIQUE,
        `type` ENUM ('Primary', 'Secondary', 'Higher Education') NOT NULL,
        `location` VARCHAR(100) NOT NULL,
        `founded_year` INT NOT NULL,
        PRIMARY KEY (`id`)
    );

CREATE TABLE
    IF NOT EXISTS `companies` (
        `id` INT AUTO_INCREMENT,
        `name` VARCHAR(150) NOT NULL UNIQUE,
        `industry` ENUM ('Technology', 'Education', 'Business') NOT NULL,
        `location` VARCHAR(150) NOT NULL,
        PRIMARY KEY (`id`)
    );

CREATE TABLE
    IF NOT EXISTS `connections` (
        `id` INT AUTO_INCREMENT,
        `user_a_id` INT NOT NULL,
        `user_b_id` INT NOT NULL,
        `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (`id`),
        FOREIGN KEY (`user_a_id`) REFERENCES `users` (`id`),
        FOREIGN KEY (`user_b_id`) REFERENCES `users` (`id`),
        UNIQUE (`user_a_id`, `user_b_id`)
    );

CREATE TABLE
    IF NOT EXISTS `enrollments` (
        `id` INT AUTO_INCREMENT,
        `user_id` INT NOT NULL,
        `educational_institution_id` INT NOT NULL,
        `start_date` DATETIME NOT NULL,
        `end_date` DATETIME NOT NULL,
        `degree` VARCHAR(30) NOT NULL,
        PRIMARY KEY (`id`),
        FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
        FOREIGN KEY (`educational_institution_id`) REFERENCES `educational_institutions` (`id`),
        CHECK (`end_date` > `start_date`)
    );

CREATE TABLE
    IF NOT EXISTS `employments` (
        `id` INT AUTO_INCREMENT,
        `user_id` INT NOT NULL,
        `company_id` INT NOT NULL,
        `start_date` DATETIME NOT NULL,
        `end_date` DATETIME NOT NULL,
        PRIMARY KEY (`id`),
        FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
        FOREIGN KEY (`company_id`) REFERENCES `companies` (`id`),
        CHECK (`end_date` > `start_date`)
    );
