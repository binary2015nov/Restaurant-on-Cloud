

# Import python packages
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from session_builder import session


sql = '''
with a as(
select * from (select ingre_id,remian_amount, update_time,
                ROW_NUMBER() OVER (PARTITION BY ingre_id order by UPDATE_TIME desc) as rk 
                from inventory)a where a.rk=1 order by ingre_id )
,b as (
select ingre_id,ingre_name from ingredient group by ingre_id,ingre_name
)
select a.remian_amount,b.ingre_name from a left join b 
on a.ingre_id=b.ingre_id
'''

# st.set_page_config(page_title="Inventory monitor", page_icon="🚨")
# st.markdown("# Inventory monitor")
# st.sidebar.header("Inventory monitor")


def get_recent_data():
    data = session.sql(sql).to_pandas().set_index('INGRE_NAME')
    return data


if "data" not in st.session_state:
    st.session_state.data = get_recent_data()

if "stream" not in st.session_state:
    st.session_state.stream = False


def toggle_streaming():
    st.session_state.stream = not st.session_state.stream


st.title("Ingredient Inventory data")
st.sidebar.slider(
    "Check for updates every: (seconds)", 0.5, 5.0, value=1.0, key="run_every"
)
st.sidebar.button(
    "Start streaming", disabled=st.session_state.stream, on_click=toggle_streaming
)
st.sidebar.button(
    "Stop streaming", disabled=not st.session_state.stream, on_click=toggle_streaming
)

if st.session_state.stream is True:
    run_every = st.session_state.run_every
else:
    run_every = None


@st.experimental_fragment(run_every=run_every)
def show_latest_data():
    
    st.session_state.data = pd.concat(
        [st.session_state.data, get_recent_data()]
    )
    st.session_state.data = st.session_state.data[-100:]
    st.bar_chart(st.session_state.data)
    # st.write(st.session_state.data.to_dict()['REMIAN_AMOUNT'].items())
    for k,v in st.session_state.data.to_dict()['REMIAN_AMOUNT'].items():
        if v < 1000:
            st.warning(f'Warning! Remain amount for {k} is less than 100000 g, currently remaining {v}.',icon="⚠️")

show_latest_data()