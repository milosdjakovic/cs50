-- Cities with spendings higher than average and graduations lower than average ordered by expenditures from highest to lowest and by graduation from lowest to highest
SELECT
    schools.city AS city,
    AVG(expenditures.per_pupil_expenditure) AS avg_expenditure_above_state,
    AVG(graduation_rates.graduated) AS avg_graduation_below_state
FROM
    schools
    JOIN graduation_rates ON schools.id = graduation_rates.school_id
    JOIN districts ON schools.district_id = districts.id
    JOIN expenditures ON districts.id = expenditures.district_id
GROUP BY
    schools.city
HAVING
    AVG(expenditures.per_pupil_expenditure) > (
        SELECT
            AVG(per_pupil_expenditure)
        FROM
            expenditures
    )
    AND AVG(graduation_rates.graduated) < (
        SELECT
            AVG(graduated)
        FROM
            graduation_rates
    )
ORDER BY
    AVG(expenditures.per_pupil_expenditure) DESC,
    AVG(graduation_rates.graduated) ASC;
