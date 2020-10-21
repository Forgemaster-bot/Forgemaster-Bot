import pyodbc
from sqlalchemy import create_engine
from Connections import config

def make_pyodbc_connection():
    driver = config["sql-driver"]
    database = config["sql-database"]
    server = config["sql-server"]
    uid = config["sql-uid"]
    pwd = config["sql-pwd"]
    port = config["sql-port"]
    return pyodbc.connect('', driver=driver, database=database, server=server, uid=uid, pwd=pwd, port=port,
                          tds_version='8.0', charset='utf-8')

# Define engine based on pyodbc connection
engine = create_engine('mssql+pyodbc://', creator=make_pyodbc_connection)
