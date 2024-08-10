from config import config
import pymysql
import pandas as pd


conn = pymysql.connect(
    host=config['hostname'],
    user=config['username'],
    password=config['password'],
    db=config['dbname'],
)


def read_sql(query):
    try:
        return pd.read_sql(query, conn)
    except Exception as e:
        return pd.DataFrame()


def read_table(table):
    try:
        return pd.read_sql_table(table, conn)
    except Exception as e:
        # print(e)
        return pd.DataFrame()

# read_sql('''SELECT *
# FROM forecast_price_master_product''')
