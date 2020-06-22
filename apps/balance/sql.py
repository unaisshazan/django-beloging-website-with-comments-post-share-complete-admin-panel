# args: account_id,year,year,divorcee1_id,year,divorcee2_id
of_year = """
SELECT * FROM 
(SELECT DISTINCT month_balanced
FROM expenses_expense
WHERE account_id=%s AND year_balanced=%s) table_all
LEFT JOIN (SELECT month_balanced,owner_id AS owner_id1,
SUM(expense_sum) AS sum1,
SUM(expense_sum/100*expense_divorcee_participate) AS participate2
FROM expenses_expense
WHERE year_balanced=%s AND owner_id=%s {approved_clause}
GROUP BY month_balanced) table_a
ON table_all.month_balanced = table_a.month_balanced
LEFT JOIN
(SELECT month_balanced,owner_id AS owner_id2,
SUM(expense_sum) AS sum2,
SUM(expense_sum/100*expense_divorcee_participate) AS participate1
FROM expenses_expense
WHERE year_balanced=%s AND owner_id=%s {approved_clause}
GROUP BY month_balanced) table_b
ON table_all.month_balanced = table_b.month_balanced
"""

sort_clause = "ORDER BY table_all.month_balanced"

# args: account_id,year,year,divorcee1_id,year,divorcee2_id,month
of_month = of_year + "WHERE table_all.month_balanced=%s"