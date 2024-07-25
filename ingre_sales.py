import streamlit as st
import time
from datetime import timedelta,date,datetime
import numpy as np
import pandas as pd
from session_builder import session

from snowflake.snowpark.functions import col
import matplotlib.pyplot as plt

# st.set_page_config(page_title="Ingredient sales", page_icon="📊")

# st.markdown("# Ingredient sales")
# st.sidebar.header("Ingredient sales")

start = st.date_input("Select the date", date.today())
st.title(f'date {start}')

st.set_option('deprecation.showPyplotGlobalUse', False)
df_table = session.table('ORDERING_SYSTEM.CORE.order_rank')


#snowpark dataframe  is case insensitive
sale_rank = df_table[[ 'dish_name','sale_no']].filter(
    f"stat_date = date'{start}'").to_pandas()

dish_names = sale_rank.loc[:,'DISH_NAME']


#pandas dataframe is case sensitive
sales = sale_rank.loc[:,'SALE_NO']
plt.legend(title = "Sale numbers percentage:")
plt.pie(sales, labels=dish_names, autopct='%1.1f%%')
st.pyplot()

st.bar_chart(sale_rank.set_index('DISH_NAME'))




