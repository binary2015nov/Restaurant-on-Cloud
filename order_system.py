# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
from datetime import datetime
from session_builder import session

import pytz

# st.set_page_config(page_title="Start your order", page_icon="✅")
# st.markdown("# Start your order")
# st.sidebar.header("Start your order")

def insert_order(order_id, selected_table):
    order_table_no=selected_table
    order_details_id = f'{order_id}_{order_table_no}'
    data = [order_id, order_table_no, localtime, order_details_id]
    
    insert_stm = f"insert into ORDERING_SYSTEM.CORE.DISH_ORDER values ('{data[0]}','{data[1]}','{data[2]}','{data[3]}','{data[2]}');"
    st.write(insert_stm)
    session.sql(insert_stm).collect()

def insert_order_detail(order_id, food_dict):
    for key in food_dict.keys():
        #insert_stm = f"insert into {table_name} values ({data[0]},{data[1]},'{data[2]}')"
        insert_stm = f"insert into ORDERING_SYSTEM.CORE.ORDER_DETAILS\
                (DISH_ID, DISH_AMOUNT, ORDER_DETAILS_ID)\
                select a.DISH_ID, {food_dict[key]}, b.ORDER_DETAILS_ID \
                from ORDERING_SYSTEM.CORE.MENU a\
                , ORDERING_SYSTEM.CORE.DISH_ORDER  b\
                where a.dish_name = '{key}'\
                and b.order_id = '{order_id}';"
        st.write(insert_stm)
        session.sql(insert_stm).collect()

def insert_inventory(order_id):
    select_stm = f"select \
                d.ingre_id, sum(d.amount*b.dish_amount)\
                from ORDERING_SYSTEM.CORE.DISH_ORDER a \
                inner join ORDERING_SYSTEM.CORE.ORDER_DETAILS b\
                  on a.order_details_id = b.order_details_id\
                inner join ORDERING_SYSTEM.CORE.MENU c \
                  on b.dish_id = c.dish_id\
                inner join ORDERING_SYSTEM.CORE.INGREDIENT d\
                  on d.dish_id = c.dish_id\
                where a.order_id = '{order_id}'\
                group by d.ingre_id ;"
    st.write(select_stm)
    res = session.sql(select_stm).collect() 
    for r in res: 
        inger_id= r[0]
        change_count = r[1]
        insert_stm = f"insert into ORDERING_SYSTEM.CORE.INVENTORY\
                    (INGRE_ID, REMIAN_AMOUNT, BASE_UNIT, UPDATE_TIME, INSERT_TIME, CHANGED_AMOUNT, INGRE_COST)\
                    select INGRE_ID, REMIAN_AMOUNT - {change_count}, BASE_UNIT, '{localtime}','{localtime}' , -1*{change_count}, INGRE_COST\
                    from ORDERING_SYSTEM.CORE.INVENTORY where INGRE_ID = {inger_id}\
                    order by insert_time desc limit 1 ;"
        st.write(insert_stm)
        session.sql(insert_stm).collect()


def get_max_order_id():
    table_name = 'ORDERING_SYSTEM.CORE.DISH_ORDER'
    select_stm = f"select max(order_id) from {table_name}"
    #st.write(select_stm)
    return session.sql(select_stm).collect() 

def generate_order_id():
    max_order_id = get_max_order_id()[0][0]
    #st.write(max_order_id)
    if localdate == max_order_id[0:8]:
        return int(max_order_id)+1
    else:
        return localdate+"0001"

localtime=datetime.now().astimezone(pytz.timezone("Asia/Shanghai"))
#st.write(localtime)
localdate = str(localtime.date()).replace("-","")
#st.write(localdate)

table_no = ['01-01','01-02','01-03','01-04','02-01','02-02','02-03','02-04','03-01','03-02','03-03','03-04','04-01','04-02','04-03','04-04','05-01','05-02','05-03','05-04']

st.title(":cup_with_straw: Restaurant :cup_with_straw:")


df = session.table("ORDERING_SYSTEM.CORE.MENU").select(col("DISH_NAME"))

selected_table = st.selectbox(
    label ="Choose table"
    ,options = table_no
    ,index=None

)

ingredients = ''
ingredients = st.multiselect(
    "Choose food in your menu"
    ,df
    ,default = None
)

food_dict = {}
if ingredients:
    for food in ingredients: 
        food_count = st.number_input(label = food, 
                             min_value=1, 
                             max_value=100, 
                             value=1, 
                             step=1
                            )
        food_dict.update({food:food_count})
    st.text(food_dict)

if ingredients and selected_table:
    insert_flag = st.button("Submit order")
    if insert_flag:
        order_id = generate_order_id() 

        insert_order(order_id, selected_table)
        insert_order_detail(order_id, food_dict)
        insert_inventory(order_id)
        st.success('Ordered!', icon="✅")
