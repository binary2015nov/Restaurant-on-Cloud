import streamlit as st
import time
from datetime import timedelta,date,datetime
import numpy as np
import pandas as pd
from session_builder import session

from snowflake.snowpark.functions import col
import matplotlib.pyplot as plt


# st.set_page_config(page_title="Ingredient profit", page_icon="🌍")

# st.markdown("# Ingredient profit")
# st.sidebar.header("Ingredient profit")

start = st.date_input("Select the date", date.today())
# st.title(f'date {start}')

df_table = session.table('ORDERING_SYSTEM.CORE.order_rank')

profit_rank = df_table[[ 'dish_name','profit']].filter(
    f"stat_date = date'{start}'").to_pandas()

dish_names = profit_rank.loc[:,'DISH_NAME']

profits = profit_rank.loc[:,'PROFIT']
# plt.legend(title = "Profit percentage:")
plt.pie(profits, labels=dish_names, autopct='%1.1f%%')
 
# Display the plot in Streamlit
# st.set_option('deprecation.showPyplotGlobalUse', False)
st.pyplot()


st.bar_chart(profit_rank.set_index('DISH_NAME'))





