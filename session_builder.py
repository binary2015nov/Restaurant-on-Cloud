from snowflake.snowpark import Session

def getSession():
    connection_parameters = {
    "account": "DNBTGEE-CN03889",
    "user": "APP_ACCESS_USER",
    "password": "123456Aa",
    "role": "MYROLE",
    "warehouse": "APP_ACCESS_WH",
    "database": "ORDERING_SYSTEM",
    "schema": "CORE"
    ,"client_session_keep_alive": True
    }

    session = Session.builder.configs(connection_parameters).create()

    return session

session = getSession()
