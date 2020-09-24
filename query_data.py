#%%
import mysql.connector
from sqlalchemy import create_engine
import numpy as np
import pandas as pd
import glob
import unidecode
from cong_thuc import ChiSo
engine = create_engine("mysql+pymysql://root:@localhost/faviz")
#%%
test_data = pd.read_sql_query("select id from Bao_cao_tai_chinh where Ticker = 'HPG'", engine)
test_data
# %%
ticker_query = 'HPG'
def query_FS(ticker):
    data = pd.read_sql_query('select * from Bao_cao_tai_chinh where Ticker = "{}" '.format(ticker),engine).sort_values(['Ticker','Nam','Quy'],ascending=[True,True,True])
    data_nam = data.loc[data.Quy == 5]
    data_quy = data.loc[data.Quy != 5]
    return data_nam,data_quy,data
a,b,c = query_FS('HPG')
so_cp = ChiSo(a,b).So_co_phieu()
so_cp
# %%
