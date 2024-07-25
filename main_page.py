import streamlit as st

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


def login():
    form = st.form("my_form")
    username = form.text_input("Username", value='')
    pwd = form.text_input("Password", value='', type="password")
    if form.form_submit_button("Login"):
        if username == "admin" and pwd=="admin":
            st.session_state.logged_in = True
            st.rerun()
        else: 
            st.error("Username or password error", icon="⚠️")

def logout():
    st.session_state.logged_in = False
    st.rerun()

login_page = st.Page(login, title="Login", icon=":material/login:")
logout_page = st.Page(logout, title="Logout", icon=":material/logout:")

order_pg = st.Page("order_system.py", title="Start your order", icon="✅")
his_trend = st.Page("his_trend.py", title="History trend", icon="📈")
ingre_profits = st.Page("ingre_profits.py", title="Ingredient profit", icon="🌍")
ingre_sales = st.Page("ingre_sales.py", title="Ingredient sales", icon="📊")
ivt_monitor = st.Page("inventory_monitor.py", title="Inventory monitor", icon="🚨")

if st.session_state.logged_in:
    pg = st.navigation([order_pg, his_trend,ingre_profits,ingre_sales,ivt_monitor, logout_page])
else:
    pg = st.navigation([login_page])

st.set_page_config(
    page_title="Welcome",
    page_icon="👋",
)

#st.write("# Welcome ! 👋")

# st.snow()

pg.run()
