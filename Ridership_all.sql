SELECT
    station_id station_details,
    equp_grp_id,
    equp_id,
    0          entry_count,
    NULL       AS entry_trx_date,
    nvl(COUNT(trx_id),
        0)     exit_count,
    exit_trx_date,
    trx_type,
    trx_seq_num,
    line_id,
    aqur_id,
    oper_id,
    trm_id,
    crd_type,
    pan_sha,
    prd_type,
    trx_amt,
    crd_bal,
    paytm_tid,
    paytm_mid,
    insert_date
FROM
    (
        SELECT
            trx_id,
            m.trx_type
            || '-'
            || ticket_txn_code                              AS trx_type,
            trx_seq_num,
            m.line_id,
            m.station_id
            || '-'
            || b.station_name                               station_id,
            equp_grp_id,
            equp_id,
            aqur_id,
            oper_id,
            trm_id,
            m.crd_type
            || ' - '
            || c.product_type_desc                          crd_type,
            pan_sha,
            prd_type,
            TO_DATE(m.trx_dt_tm, 'yyyy-mm-dd hh24:mi:ss')   AS exit_trx_date,
            TO_DATE(m.business_dt, 'yyyy-mm-dd hh24:mi:ss') business_dt,
            trx_amt / 100                                   AS trx_amt,
            crd_bal / 100                                   AS crd_bal,
            paytm_tid,
            paytm_mid,
            m.insert_date
        FROM
            tb_emv_trx_gate_exit_tag m,
            tb_stations              b,
            tb_emv_card_type         c,
            tb_emv_trans_type        t
        WHERE
                m.station_id = b.station_uniqueid
            AND c.product_id = m.crd_type
            AND m.insert_date BETWEEN TO_DATE('20230914 00:00:00', 'yyyy-mm-dd hh24:mi:ss') AND TO_DATE('20230914 23:59:59', 'yyyy-mm-dd hh24:mi:ss'
            )
            AND m.crd_type = c.product_id
            AND m.trx_type = t.ticket_txn_type_id
        ORDER BY
            m.insert_date DESC
    )
GROUP BY (
    station_id,
    equp_grp_id,
    equp_id,
    exit_trx_date,
    trx_type,
    trx_seq_num,
    line_id,
    aqur_id,
    oper_id,
    trm_id,
    crd_type,
    pan_sha,
    prd_type,
    trx_amt,
    crd_bal,
    paytm_tid,
    paytm_mid,
    insert_date
)
UNION ALL
SELECT
    station_id station_details,
    equp_grp_id,
    equp_id,
    0          exit_count,
    NULL       AS exit_trx_date,
    nvl(COUNT(trx_id),
        0)     entry_count,
    entry_trx_date,
    trx_type,
    trx_seq_num,
    line_id,
    aqur_id,
    oper_id,
    trm_id,
    crd_type,
    pan_sha,
    prd_type,
    trx_amt,
    crd_bal,
    paytm_tid,
    paytm_mid,
    insert_date
FROM
    (
        SELECT
            m.trx_id,
            m.trx_type
            || '-'
            || ticket_txn_code                              AS trx_type,
            trx_seq_num,
            m.line_id,
            m.station_id
            || '-'
            || b.station_name                               station_id,
            m.equp_grp_id,
            m.equp_id,
            m.aqur_id,
            m.oper_id,
            m.trm_id,
            m.crd_type
            || ' - '
            || c.product_type_desc                          crd_type,
            m.pan_sha,
            m.prd_type,
            TO_DATE(m.trx_dt_tm, 'yyyy-mm-dd hh24:mi:ss')   AS entry_trx_date,
            TO_DATE(m.business_dt, 'yyyy-mm-dd hh24:mi:ss') business_dt,
            NULL                                            AS trx_amt,
            NULL                                            AS crd_bal,
            '0'                                             AS paytm_tid,
            'LTMetr33790038971459'                          AS paytm_mid,
            m.insert_date
        FROM
            tb_emv_trx_gate_entry_tag m,
            tb_stations               b,
            tb_emv_card_type          c,
            tb_emv_trans_type         t
        WHERE
                m.station_id = b.station_uniqueid
            AND c.product_id = m.crd_type
            AND m.insert_date BETWEEN TO_DATE('20230914 00:00:00', 'yyyy-mm-dd hh24:mi:ss') AND TO_DATE('20230914 23:59:59', 'yyyy-mm-dd hh24:mi:ss'
            )
            AND m.trx_type = t.ticket_txn_type_id
        ORDER BY
            m.insert_date DESC
    )
GROUP BY (
    station_id,
    equp_grp_id,
    equp_id,
    entry_trx_date,
    trx_type,
    trx_seq_num,
    line_id,
    aqur_id,
    oper_id,
    trm_id,
    crd_type,
    pan_sha,
    prd_type,
    trx_amt,
    crd_bal,
    paytm_tid,
    paytm_mid,
    insert_date
);