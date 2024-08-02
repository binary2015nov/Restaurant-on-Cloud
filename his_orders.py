import streamlit as st
import pandas as pd
import numpy as np
from datetime import timedelta,date,datetime
from session_builder import session

start_date = st.date_input("Select the order start date", date.today())
end_date = st.date_input("Select the order end date", date.today() + timedelta(days = 1))

sql = f'''
SELECT A.ORDER_ID, A.ORDER_TABLE_NO AS TABLE_NO, A.ORDER_DETAILS_ID, DISH_NAME, ROUND(DISH_PRICE, 2) AS DISH_PRICE, ROUND(DISH_AMOUNT) AS DISH_AMOUNT, ORDER_TIME, DISH_PRICE * DISH_AMOUNT AS TOTAL_COST 
FROM ORDERING_SYSTEM.CORE.DISH_ORDER A 
  INNER JOIN ORDERING_SYSTEM.CORE.ORDER_DETAILS B 
    ON A.ORDER_DETAILS_ID = B.ORDER_DETAILS_ID
  INNER JOIN ORDERING_SYSTEM.CORE.MENU C 
    ON B.DISH_ID  = C.DISH_ID
WHERE ORDER_TIME >= '{start_date}' and ORDER_TIME < '{end_date}'
'''

df = session.sql(sql).to_pandas()
df_grouped = df.groupby('ORDER_ID')

# st.title(st.session_state.username + f"'s Orders history - {df_grouped.ngroups}:")
st.title(f"{df_grouped.ngroups} orders:")

for order_id, order_details in df_grouped:
    st.subheader(f"Order ID: {order_id}\tTotal Cost: ${order_details['TOTAL_COST'].sum():.2f}") 
    st.dataframe(order_details[['DISH_NAME', 'DISH_PRICE', 'DISH_AMOUNT', 'TABLE_NO', 'ORDER_TIME']], hide_index=True)




