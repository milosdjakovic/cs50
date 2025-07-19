-- *** The Lost Letter ***
-- I will check if both addresses exist in addresses table
SELECT
    *
FROM
    addresses
WHERE
    address = '900 Somerville Avenue';

SELECT
    *
FROM
    addresses
WHERE
    address = '2 Finnegan Street';

-- I could not find the "2 Finnegan Street" in the addresses table, so I will proceed with "900 Somerville Avenue"
-- I will use nested query to retrieve the package originating from "900 Somerville Avenue"
SELECT
    *
FROM
    packages
WHERE
    from_address_id = (
        SELECT
            id
        FROM
            addresses
        WHERE
            address = '900 Somerville Avenue'
    );

-- In following statement I will just use JOIN instead of nested query, and also check for content of the package
SELECT
    *
FROM
    packages
    JOIN addresses ON packages.from_address_id = addresses.id
WHERE
    addresses.address = '900 Somerville Avenue'
    AND packages.contents = 'Congratulatory letter';

-- Now I will try to expand the previous query to try and get address property type where the package has been shipped
SELECT
    *
FROM
    addresses
WHERE
    id = (
        SELECT
            packages.to_address_id
        FROM
            packages
            JOIN addresses ON packages.from_address_id = addresses.id
        WHERE
            addresses.address = '900 Somerville Avenue'
            AND packages.contents = 'Congratulatory letter'
    );

-- Same query just purely using JOIN instead of nested query
SELECT
    a2.*
FROM
    packages p
    JOIN addresses a1 ON p.from_address_id = a1.id
    JOIN addresses a2 ON p.to_address_id = a2.id
WHERE
    a1.address = '900 Somerville Avenue'
    AND p.contents = 'Congratulatory letter';

-- From results it seams that the address where the letter ended up to was " 2 Finnigan Street" and not "2 Finnegan Street"
-- *** The Devious Delivery ***
-- From the text it seems that the package has no from address, so I will try to find that one.
SELECT
    *
FROM
    packages
WHERE
    from_address_id IS NULL;

-- There is one package with contents of "Duck debugger"
SELECT
    addresses.type
FROM
    addresses
    JOIN packages ON addresses.id = packages.to_address_id
WHERE
    packages.from_address_id IS NULL;

-- Now I will try to get the latest scan by that package ID manually
SELECT
    *
FROM
    scans
WHERE
    package_id = 5098
ORDER BY
    "timestamp" DESC
LIMIT
    1;

-- I got address ID from scans and I will try to get it manually
SELECT
    *
FROM
    addresses
WHERE
    id = 348;

-- I got a "Police Station" address type. Now to combine queries into single query using JOIN
SELECT
    addresses.type
FROM
    addresses
    JOIN scans ON addresses.id = scans.address_id
    JOIN packages ON scans.package_id = packages.id
WHERE
    packages.from_address_id IS NULL
ORDER BY
    "timestamp" DESC
LIMIT
    1;

-- *** The Forgotten Gift ***
-- Here the sender claims that the package has been sent to "728 Maple Place" from "109 Tileston Street" so lets check if those addresses exist
SELECT
    *
FROM
    addresses
WHERE
    address = '728 Maple Place';

SELECT
    *
FROM
    addresses
WHERE
    address = '109 Tileston Street';

-- It seems both addresses exist, now lets try to match them with packages from attribute for "109 Tileston Street";
SELECT
    *
FROM
    packages
    JOIN addresses ON packages.from_address_id = addresses.id
WHERE
    addresses.address = '109 Tileston Street';

-- I found package from the "109 Tileston Street" wich has contents of "Flowers".
-- Next step would be to get all this package in scans, order them by newest scan, and get the first result in order to get the driver's name that has the current package
SELECT
    drivers.name
FROM
    scans
    JOIN packages ON scans.package_id = packages.id
    JOIN addresses ON packages.from_address_id = addresses.id
    JOIN drivers ON drivers.id = scans.driver_id
WHERE
    addresses.address = '109 Tileston Street'
ORDER BY
    "timestamp" DESC
LIMIT
    1;
