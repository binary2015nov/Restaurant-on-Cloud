import streamlit as st



order_pg = st.Page("order_system.py", title="Start your order", icon="✅")
his_trend = st.Page("his_trend.py", title="History trend", icon="📈")
ingre_profits = st.Page("ingre_profits.py", title="Ingredient profit", icon="🌍")
ingre_sales = st.Page("ingre_sales.py", title="Ingredient sales", icon="📊")
ivt_monitor = st.Page("inventory_monitor.py", title="Inventory monitor", icon="🚨")

pg = st.navigation([order_pg, his_trend,ingre_profits,ingre_sales,ivt_monitor])

st.set_page_config(
    page_title="Welcome",
    page_icon="👋",
)

st.write("# Welcome ! 👋")

# st.snow()

pg.run()
