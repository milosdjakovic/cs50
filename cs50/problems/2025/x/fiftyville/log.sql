/*
Info:
The theft took place on July 28, 2024 and that it took place on Humphrey Street.

Leads:
- July 28, 2024 <- Date of theft
- Humphrey Street <- Street
*/

-- Find crime details in crime_scene_reports
SELECT *
FROM crime_scene_reports
WHERE street = 'Humphrey Street'
AND year = 2024
AND month = 7
AND day = 28;

/*
Info:
Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery. Interviews were conducted today with three witnesses who were present at the time – each of their interview transcripts mentions the bakery.

Leads:
- 10:15am <- Time
- bakery <- Location
- 3 witnesses
*/

-- Inspect the inverviews.
SELECT *
FROM interviews
WHERE "year" = 2024
AND "month" = 7
and "day" = 28;

/*
Info:
I managed to find statements from all 3 witnesses:
  - Witness #1: Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away. If you have security footage from the bakery parking lot, you might want to look for cars that left the parking lot in that time frame.
  - Witness #2: I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at Emma's bakery, I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.
  - Witness #3: As the thief was leaving the bakery, they called someone who talked to them for less than a minute. In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow. The thief then asked the person on the other end of the phone to purchase the flight ticket.

Leads:
1. 10 minutes after the theft, thief drove off in a car from the bakery's parking lot
2. Thief withdrawed money from ATM on Leggett Street
3. While leaving thief made phone call with duration of less than a minute asking other participant to get airplane tickets for the first first flight from Fiftville
*/

-- Get the license plates of vehicles that exited bakery's parking lot within 10 minutes after the theft on July 24 2024
SELECT license_plate
 FROM bakery_security_logs
WHERE activity = 'exit'
  AND "year" = 2024
  AND "month" = 7
  AND "day" = 28
  AND "hour" = 10
  AND "minute" >= 15
  AND "minute" <= 25;

-- Get the account numbers on which transaction was made on July 28 2024
SELECT account_number
  FROM atm_transactions
 WHERE atm_location = 'Leggett Street'
   AND transaction_type = 'withdraw'
   AND "year" = 2024
   AND "month" = 7
   AND "day" = 28;

-- Get the phone calls lasting less than a minute on Joly 28 2024
SELECT "caller", "receiver"
  FROM phone_calls
 WHERE duration < 60
   AND "year" = 2024
   AND "month" = 7
   AND "day" = 28;

-- Get the ID of the airport in Fiftyville
SELECT id as "Fiftyville Airport ID"
  FROM airports
 WHERE city = 'Fiftyville';

-- Get the earliest flight from Fiftyville on July 28 2024
SELECT id AS "Flight ID", destination_airport_id AS "Flight Destination Airport ID"
  FROM flights
 WHERE origin_airport_id = (SELECT id FROM airports WHERE city = 'Fiftyville')
   AND "year" = 2024
   AND "month" = 7
   AND "day" = 29
 ORDER BY "hour", "minute"
 LIMIT 1;
/*
Flight ID: 36
Destination ariport ID: 4
*/

-- Get the city of the destination airport by airport's ID determined in previous query
SELECT city AS "Destination Airport City"
  FROM airports
 WHERE id = 4;
/*
The airport with id 4 is in 'New York City', so that should be the place where the thief escaped
*/

-- Get the passport numbers of passengers on the flight by ID determined in previous query
SELECT passport_number AS "Passenger Passport Numbers"
  FROM passengers
 WHERE flight_id = 36;

-- Get the person with matching license plate, phone number, passport number, and bank account
SELECT p.name AS "Thief"
  FROM bank_accounts AS ba
  JOIN people AS p
    ON ba.person_id = p.id
 WHERE ba.account_number IN
       (SELECT account_number
          FROM atm_transactions
         WHERE atm_location = 'Leggett Street'
           AND transaction_type = 'withdraw'
           AND "year" = 2024
           AND "month" = 7
           AND "day" = 28)
   AND p.passport_number IN
       (SELECT passport_number
          FROM passengers
         WHERE flight_id = 36)
   AND p.license_plate IN
       (SELECT license_plate
          FROM bakery_security_logs
         WHERE activity = 'exit'
           AND "year" = 2024
           AND "month" = 7
           AND "day" = 28
           AND "hour" = 10
           AND "minute" >= 15
           AND "minute" <= 25)
   AND p.phone_number IN
       (SELECT "caller"
          FROM phone_calls
         WHERE duration < 60
           AND "year" = 2024
           AND "month" = 7
           AND "day" = 28);
/*
The data of the person:
+--------+-------+----------------+-----------------+---------------+
|   id   | name  |  phone_number  | passport_number | license_plate |
+--------+-------+----------------+-----------------+---------------+
| 686048 | Bruce | (367) 555-5533 | 5773159633      | 94KL13X       |
+--------+-------+----------------+-----------------+---------------+

The thief's name is 'Bruce'
*/

-- Get the name of the person Bruce called to arrange flight in the time frame described by witness
SELECT "name" AS "Accomplice"
  FROM people
 WHERE people.phone_number =
       (SELECT receiver
          FROM phone_calls
         WHERE "caller" = '(367) 555-5533'
           AND duration < 60
           AND "year" = 2024
           AND "month" = 7
           AND "day" = 28);
/*
Accomplice's name is 'Robin'
*/

--
SELECT city AS "Thief Escaped To"
  FROM airports
 WHERE id = 4;
