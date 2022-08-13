from sqlalchemy import create_engine
import config
import pandas as pd

def myConnection():
    connection = create_engine(
        config.mysql_url
        + config.user
        + ":"
        + config.password
        + "@"
        + config.host_name
        + "/"
        + config.schema
    )
    return connection


def pullTable(tbl: str):
    connection = myConnection()
    tbl = pd.read_sql(f"SELECT * FROM simple_crm.{tbl}", con=connection)
    connection.connect().close()
    return tbl