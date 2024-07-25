import streamlit as st
import time
from datetime import timedelta,date,datetime
import numpy as np
import pandas as pd
from session_builder import session

from snowflake.snowpark.functions import col

# st.set_page_config(page_title="History Trend", page_icon="📈")
# st.markdown("# History Trend")
# st.sidebar.header("History Trend")

start = st.date_input("Select the start date", date.today()+timedelta(days=-30) )

end = st.date_input("Select the end date", date.today())

df_table = session.table('ORDERING_SYSTEM.CORE.STATISTICS')

profit_trend = df_table[['stat_date', 'profit','turnover']].filter(
    f"stat_date between date'{start}' and date'{end}'").orderBy(['stat_date']).to_pandas()

st.line_chart(profit_trend.set_index('STAT_DATE'))

num_orders_trend = df_table[['stat_date', 'total_orders']].filter(
    f"stat_date between date'{start}' and date'{end}'").orderBy(['stat_date']).to_pandas()

st.bar_chart(num_orders_trend.set_index('STAT_DATE'))




