SELECT
    stationid,
    station_name,
    SUM(entry_count) entry_count,
    SUM(exit_count)  exit_count
FROM
    (
        SELECT
            nvl(x.entrystationid, b.station_uniqueid) stationid,
            b.station_name                            station_name,
            nvl(entry_count, 0)                       entry_count,
            0                                         exit_count
        FROM
            (
                SELECT
                    entrystationid,
                    COUNT(1) entry_count
                FROM
                    (
                        SELECT
                            station_id entrystationid
                        FROM
                            tb_emv_trx_gate_entry_tag
                        WHERE
                                trx_type = 1
                            AND insert_date BETWEEN TO_DATE('20230901 00:00:00', 'yyyy-mm-dd hh24:mi:ss') AND TO_DATE('20230901 23:59:59'
                            , 'yyyy-mm-dd hh24:mi:ss')
                    )
                GROUP BY
                    ROLLUP(entrystationid)
            )           x,
            tb_stations b
        WHERE
            b.station_uniqueid = x.entrystationid (+)
        UNION ALL
        SELECT
            nvl(x.station_id, b.station_uniqueid) stationid,
            b.station_name                        station_name,
            0                                     entry_count,
            nvl(exit_count, 0)                    exit_count
        FROM
            (
                SELECT
                    station_id,
                    COUNT(1) exit_count
                FROM
                    (
                        SELECT
                            station_id
                        FROM
                            tb_emv_trx_gate_exit_tag
                        WHERE
                                trx_type = 2
                            AND insert_date BETWEEN TO_DATE('20230901 00:00:00', 'yyyy-mm-dd hh24:mi:ss') AND TO_DATE('20230901 23:59:59'
                            , 'yyyy-mm-dd hh24:mi:ss')
                    )
                GROUP BY
                    ROLLUP(station_id)
            )           x,
            tb_stations b
        WHERE
            b.station_uniqueid = x.station_id (+)
    )
GROUP BY (
    stationid,
    station_name
)
ORDER BY
    stationid