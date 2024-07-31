import streamlit as st
from datetime import timedelta,date,datetime
from snowflake.snowpark.functions import col
from session_builder import session


check_date = st.date_input("Select the order date", date.today())

table_no = ['01-01','01-02','01-03','01-04','02-01','02-02','02-03','02-04','03-01','03-02','03-03','03-04','04-01','04-02','04-03','04-04','05-01','05-02','05-03','05-04']


selected_table = st.selectbox(
        label ="Choose table number"
        ,options = table_no
        ,index=None
    )


sql = f'''
with a as (select order_id,order_table_no,order_time,order_details_id from dish_order where to_date(order_time) = date'{check_date}' and order_table_no='{selected_table}')
,b as (
select a.*,b.dish_id,b.dish_amount,c.dish_price,c.dish_price*b.dish_amount as cost,c.dish_name
from a left join order_details b on a.order_details_id=b.order_details_id
left join menu c on b.dish_id=c.dish_id)
select b.order_id,b.order_table_no,b.order_time,b.order_details_id,
 LISTAGG(DISTINCT dish_name||' * '||dish_amount::int, ', ') as dish_detail,sum(cost) as total_cost from b group by 1,2,3,4 order by order_id
'''

st.write(session.sql(sql))



