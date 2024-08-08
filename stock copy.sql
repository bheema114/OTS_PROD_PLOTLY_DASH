SELECT
    'Total_CC_Stock'   AS category,
    COUNT(no_of_cards) AS count,
    ' '                AS station_id,
    product_id
FROM
    tb_emv_stock_inventory_details
WHERE
    ( ( stock_id = 10
        AND insert_date <= sysdate )
      OR ( stock_id = 10
           AND update_date <= sysdate ) )
GROUP BY
    product_id
UNION ALL
SELECT
    'Total_SC_Stock'   AS category,
    COUNT(no_of_cards) AS count,
    ' '                AS station_id,
    product_id
FROM
    tb_emv_stock_inventory_details
WHERE
    ( ( stock_id IN ( 30, 60, 70, 90 )
        AND insert_date <= sysdate )
      OR ( stock_id IN ( 30, 60, 70, 90 )
           AND update_date <= sysdate ) )
GROUP BY
    product_id
UNION ALL
SELECT
    'Total_Equipment_Stock' AS category,
    COUNT(no_of_cards)      AS count,
    ' '                     AS station_id,
    product_id
FROM
    tb_emv_stock_distribution
WHERE
    ( ( stock_id = 70
        AND TO_DATE(transaction_date_time, 'dd-mm-yy') <= sysdate )
      OR ( stock_id = 70
           AND update_date <= sysdate ) )
GROUP BY
    product_id
UNION ALL
SELECT
    'No_of_Cards_Sold'           AS category,
    COUNT(DISTINCT phone_number) AS count,
    station_id,
    product_id
FROM
    tb_emv_card_issuance
WHERE
    insert_date <= sysdate
GROUP BY
    station_id,
    product_id
UNION ALL
SELECT
    'Total_CC_Defective_Stock' AS category,
    COUNT(no_of_cards)         AS count,
    ' '                        AS station_id,
    product_id
FROM
    tb_emv_stock_inventory_details
WHERE
    ( ( stock_id IN ( 50 )
        AND insert_date <= sysdate )
      OR ( stock_id IN ( 50 )
           AND update_date <= sysdate ) )
GROUP BY
    product_id;

