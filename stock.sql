Select 'Total_CC_Stock' as Category,count (no_of_cards) as count,' ' as station_id from tb_emv_stock_inventory_details
where (stock_id = 10 and insert_date <= SYSDATE) or (stock_id = 10 and update_date <= SYSDATE)
union all
Select 'Total_SC_Stock' as Category,count(no_of_cards) as count,' ' as station_id from tb_emv_stock_inventory_details
where (stock_id in( 30,60,70,90) and insert_date <= SYSDATE) 
or (stock_id in( 30,60,70,90) and update_date <= SYSDATE)
union all
Select 'Total_Equipment_Stock' as Category,count (no_of_cards) as count,' ' as station_id from tb_emv_stock_distribution
where(stock_id = 70 AND to_date(transaction_date_time,'dd-mm-yy') <= SYSDATE) 
or (stock_id = 70 and update_date <= SYSDATE)
union all
select 'No_of_Cards_Sold' as Category,count(distinct phone_number) as count,station_id from tb_emv_card_issuance 
where insert_date  <= SYSDATE group by tb_emv_card_issuance.station_id
UNION ALL
Select 'Total_CC_Defective_Stock' as Category, count(no_of_cards) as count,' ' as station_id from tb_emv_stock_inventory_details
where (stock_id in( 50) and insert_date <= SYSDATE) 
or (stock_id in( 50) and update_date <= SYSDATE);
