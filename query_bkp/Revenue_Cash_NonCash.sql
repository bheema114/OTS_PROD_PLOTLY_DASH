SELECT
    transaction_date,
    mid,
    station_name,
    transactiontype,
    payment_type,
    payment_mode,
    revenue_type,
    equipment_id,
    SUM(transaction_count)          AS transaction_count,
    SUM(income)                     AS income,
    SUM(outgoing)                   AS outgoing,
    ( SUM(income) - SUM(outgoing) ) AS total
FROM
    (
        SELECT
            trunc(TO_DATE(a.trx_dt_tm, 'yyyy-mm-dd hh24:mi:ss')) AS transaction_date,
            1                                                    AS mid,
            a.station_id
            || '-'
            || b.station_name                                    AS station_name,
            a.trx_type
            || '-'
            || c.ticket_txn_code                                 AS transactiontype,
            CASE
                WHEN pay_md = 100 THEN
                    'cash'
                ELSE
                    'non_cash'
            END                                                  AS payment_type,
            e.payment_type_code                                  AS payment_mode,
            CASE
                WHEN pay_md IN ( 100, 101, 102 ) THEN
                    'revenue'
                ELSE
                    'nonrevenue'
            END                                                  AS revenue_type,
            equp_id                                              AS equipment_id,
            COUNT(trx_id)                                        AS transaction_count,
            SUM(add_val_amt)                                     AS income,
            0                                                    AS outgoing
        FROM
                 tb_emv_trx_tom_add_global_balance a
            JOIN tb_stations         b ON a.station_id = b.station_uniqueid
            JOIN tb_emv_trans_type   c ON a.trx_type = c.ticket_txn_type_id
                                --JOIN tb_payment_method d ON d.payment_method_id = a.pay_md
            JOIN tb_emv_payment_type e ON e.payment_type_id = a.pay_md
        WHERE
            TO_DATE(trx_dt_tm, 'yyyy-mm-dd hh24:mi:ss') = TO_DATE(sysdate, 'yyyy-mm-dd hh24:mi:ss')
            --TO_DATE(trx_dt_tm, 'yyyy-mm-dd hh24:mi:ss') BETWEEN TO_DATE('20230914 00:00:00', 'yyyy-mm-dd hh24:mi:ss') AND TO_DATE('20230914 23:59:59'
            --, 'yyyy-mm-dd hh24:mi:ss')
            AND
            a.equp_id = decode(1, 1, a.equp_id, 1)
            AND TO_DATE(transaction_date_time, 'yyyy-mm-dd hh24:mi:ss') = TO_DATE(sysdate, 'yyyy-mm-dd hh24:mi:ss')
            AND a.station_id = decode(1, 1, a.station_id, 1)
            AND a.pay_md = decode(1, 1, a.pay_md, 1)
        GROUP BY
            trunc(TO_DATE(a.trx_dt_tm, 'yyyy-mm-dd hh24:mi:ss')),
            a.station_id,
            b.station_name,
            a.trx_type,
            pay_md,
            equp_id,
            c.ticket_txn_code,
            e.payment_type_code
        UNION ALL
        SELECT
            trunc(TO_DATE(a.trx_dt_tm, 'yyyy-mm-dd hh24:mi:ss')) AS transaction_date,
            1                                                    AS mid,
            a.station_id
            || '-'
            || b.station_name                                    AS station_name,
            a.trx_type
            || '-'
            || c.ticket_txn_code                                 AS transactiontype,
            CASE
                WHEN plt_pay_md = 100 THEN
                    'cash'
                ELSE
                    'non_cash'
            END                                                  AS payment_type,
            e.payment_type_code                                  AS payment_mode,
            CASE
                WHEN plt_pay_md IN ( 100, 101, 102 ) THEN
                    'revenue'
                ELSE
                    'nonrevenue'
            END                                                  AS revenue_type,
            equp_id                                              AS equipment_id,
            COUNT(trx_id)                                        AS transaction_count,
            SUM(plt_amt)                                         AS income,
            0                                                    AS outgoing
        FROM
                 tb_emv_trx_tom_ticket_adjustment a
            JOIN tb_stations         b ON a.station_id = b.station_uniqueid
            JOIN tb_emv_trans_type   c ON a.trx_type = c.ticket_txn_type_id
                               -- JOIN tb_payment_method d ON d.payment_method_id = a.plt_pay_md
            JOIN tb_emv_payment_type e ON e.payment_type_id = a.plt_pay_md
        WHERE
            TO_DATE(trx_dt_tm, 'yyyy-mm-dd hh24:mi:ss') = TO_DATE(sysdate, 'yyyy-mm-dd hh24:mi:ss')
            --TO_DATE(trx_dt_tm, 'yyyy-mm-dd hh24:mi:ss') BETWEEN TO_DATE('20230914 00:00:00', 'yyyy-mm-dd hh24:mi:ss') AND TO_DATE('20230914 23:59:59'
            --, 'yyyy-mm-dd hh24:mi:ss')
            AND 
            
            a.equp_id = decode(1, 1, a.equp_id, 1)
            AND a.station_id = decode(1, 1, a.station_id, 1)
            AND a.plt_pay_md = decode(1, 1, a.plt_pay_md, 1)
        GROUP BY
            trunc(TO_DATE(a.trx_dt_tm, 'yyyy-mm-dd hh24:mi:ss')),
            a.station_id,
            b.station_name,
            a.trx_type,
            plt_pay_md,
            equp_id,
            c.ticket_txn_code,
            e.payment_type_code
        UNION ALL
        SELECT
            trunc(TO_DATE(m.trx_dt_tm, 'yyyy-mm-dd hh24:mi:ss')) AS transaction_date,
            1                                                    AS mid,
            m.station_id
            || '-'
            || b.station_name                                    AS station_name,
            m.trx_type
            || '-'
            || ticket_txn_code                                   AS transactiontype,
            CASE
                WHEN m.payment_method = 100 THEN
                    'cash'
                ELSE
                    'non_cash'
            END                                                  AS payment_type,
            p.payment_type_code                                  AS payment_mode,
            CASE
                WHEN m.payment_method IN ( 100, 101, 102 ) THEN
                    'revenue'
                ELSE
                    'nonrevenue'
            END                                                  AS revenue_type,
            equipment_id                                         AS equipment_id,
            COUNT(DISTINCT m.trx_id)                             AS transaction_count,
            SUM(add_val_amount)                                  AS income,
            0                                                    outgoing
        FROM
            tb_emv_trx_tom_balance_update_online m,
            tb_emv_stations                      b,
            tb_emv_card_type                     c,
            tb_emv_trans_type                    t,
            tb_emv_payment_type                  p
        WHERE
                m.station_id = b.station_uniqueid
                             --   AND c.product_id = m.card_type
            AND TO_DATE(m.trx_dt_tm, 'yyyy-mm-dd hh24:mi:ss') = TO_DATE(sysdate, 'yyyy-mm-dd hh24:mi:ss')
            --TO_DATE(m.trx_dt_tm, 'yyyy-mm-dd hh24:mi:ss') BETWEEN TO_DATE('20230914 00:00:00', 'yyyy-mm-dd hh24:mi:ss') AND TO_DATE
            --('20230914 23:59:59', 'yyyy-mm-dd hh24:mi:ss')
            AND m.trx_type = t.ticket_txn_type_id
            AND m.payment_method = p.payment_type_id
            AND m.equipment_id = decode(1, 1, m.equipment_id, 1)
            AND m.station_id = decode(1, 1, m.station_id, 1)
            AND m.payment_method = decode(1, 1, m.payment_method, 1)
        GROUP BY
            trunc(TO_DATE(m.trx_dt_tm, 'yyyy-mm-dd hh24:mi:ss')),
            m.station_id
            || '-'
            || b.station_name,
            m.trx_type
            || '-'
            || ticket_txn_code,
            m.payment_method,
            equipment_id,
            p.payment_type_code
        UNION ALL
        SELECT
            trunc(TO_DATE(a.transaction_date_time, 'yyyy-mm-dd hh24:mi:ss')) AS transaction_date,
            1                                                                AS mid,
            a.station_id
            || '-'
            || b.station_name                                                AS station_name,
            '10-Card Issuance'                                               AS transactiontype,
            CASE
                WHEN a.payment_mode = 100 THEN
                    'cash'
                ELSE
                    'non_cash'
            END                                                              AS payment_type,
            d.payment_type_code                                              AS payment_mode,
            CASE
                WHEN a.payment_mode IN ( 100, 101, 102 ) THEN
                    'revenue'
                ELSE
                    'nonrevenue'
            END                                                              AS revenue_type,
            equipment_id                                                     AS equipment_id,
            COUNT(order_id)                                                  AS transaction_count,
            SUM(total_amount)                                                AS income,
            0                                                                AS outgoing
        FROM
                 tb_emv_card_issuance a
            JOIN tb_stations         b ON a.station_id = b.station_uniqueid
            JOIN tb_emv_payment_type d ON d.payment_type_id = a.payment_mode
        WHERE
            TO_DATE(transaction_date_time, 'yyyy-mm-dd hh24:mi:ss') = TO_DATE(sysdate, 'yyyy-mm-dd hh24:mi:ss')
            --TO_DATE(transaction_date_time, 'yyyy-mm-dd hh24:mi:ss') BETWEEN TO_DATE('20230914 00:00:00', 'yyyy-mm-dd hh24:mi:ss') AND
            --TO_DATE('20230914 23:59:59', 'yyyy-mm-dd hh24:mi:ss')
            AND 
            a.equipment_id = decode(1, 1, a.equipment_id, 1)
            AND a.station_id = decode(1, 1, a.station_id, 1)
            AND a.payment_mode = decode(1, 1, a.payment_mode, 1)
        GROUP BY
            trunc(TO_DATE(a.transaction_date_time, 'yyyy-mm-dd hh24:mi:ss')),
            a.station_id,
            b.station_name,
            equipment_id,
            a.payment_mode,
            d.payment_type_code
    )
WHERE
    revenue_type IN ( 'revenue', 'nonrevenue' )
GROUP BY (
    transaction_date,
    mid,
    station_name,
    equipment_id,
    transactiontype,
    payment_type,
    payment_mode,
    revenue_type
)
ORDER BY
    transaction_date;
