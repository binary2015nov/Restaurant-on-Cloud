from snowflake.snowpark import Session

def getSession():
    connection_parameters = {
    "account": "DNBTGEE-CN03889",
    "user": "bruceshen2024",
    "password": "Asdf.#34@1bin",
    "role": "ACCOUNTADMIN",
    "warehouse": "COMPUTE_WH",
    "database": "ORDERING_SYSTEM",
    "schema": "CORE"
    ,"client_session_keep_alive": True
    }

    session = Session.builder.configs(connection_parameters).create()

    return session

session = getSession()
