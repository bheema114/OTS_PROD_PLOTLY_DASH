SELECT
    x.transaction_date,
    x.entrystationid
    || '-'
    || b.station_name station_id,
    x.equipment_id,
    x.aqur_id,
    x.oper_id,
    x.equipment_group,
    card_type,
    product_type,
    transaction_count
FROM
    (
        SELECT
            c.insert_date transaction_date,
            c.entrystationid,
            c.equipment_group,
            c.equipment_id,
            c.aqur_id,
            c.oper_id,
            c.card_type,
            c.product_type,
            COUNT(1)      transaction_count
        FROM
            (
                SELECT
                    trunc(TO_DATE(trx_dt_tm, 'yyyy-mm-dd hh24:mi:ss')) insert_date,
                    station_id                                         entrystationid,
                    equp_id                                            equipment_id,
                    aqur_id,
                    oper_id,
                    equp_grp_id                                        equipment_group,
                    crd_type                                           card_type,
                    c.product_type
                FROM
                    tb_emv_trx_gate_exit_tag a,
                    tb_emv_card_type         c
                WHERE
                        a.crd_type = c.product_id
                    AND TO_DATE(trx_dt_tm, 'yyyy-mm-dd hh24:mi:ss') BETWEEN TO_DATE('20230901 00:00:00', 'yyyy-mm-dd hh24:mi:ss') AND
                    TO_DATE('20230901 23:59:59', 'yyyy-mm-dd hh24:mi:ss')
            ) c
        GROUP BY (
            c.insert_date,
            c.entrystationid,
            c.equipment_group,
            c.equipment_id,
            c.aqur_id,
            c.oper_id,
            c.card_type,
            c.product_type
        )
    )           x,
    tb_stations b
WHERE
    x.entrystationid = b.station_uniqueid (+)
ORDER BY
    x.transaction_date,
    x.entrystationid,
    x.card_type,
    x.product_type,
    x.equipment_id,
    x.aqur_id,
    x.oper_id;