#%%
import mysql.connector
from sqlalchemy import create_engine
import numpy as np
import pandas as pd


# %%
engine = create_engine("mysql+pymysql://root:@localhost/faviz")
# create = engine.execute('create database faviz')

# %%
faviz_table = pd.read_csv("C:/Users/Chi Hieu/project/Update/Data_final/data_export.csv")
#%%
column_faviz = pd.DataFrame(faviz_table.columns, columns=["Col"])
# column_faviz['col_table'] =
column_faviz_list = (column_faviz["Col"] + " " + "Float" + " " + "Not null").to_list()
string_col = (
    str(column_faviz_list)[1:-1]
    .replace("'", "")
    .replace("-", "")
    .replace("__", "_")
    .replace(".", "")
)
result = engine.execute("create table test_faviz ({})".format(string_col))
# %%
""" Create Export data to faviz table"""
obj_col = faviz_table.select_dtypes(include="object").columns.to_list()
for col in obj_col:
    faviz_table[col].astype(str)
faviz_table.replace([np.inf, -np.inf], np.nan, inplace=True)

# %%
result = engine.execute("DROP TABLE IF EXISTS faviz;")
faviz_table.to_sql("faviz", engine, index=False)
#%%
faviz_table.to_sql("test_faviz", engine, if_exists="append", index=False)
#%%
bank_table = pd.read_csv("C:/Users/Chi Hieu/project/Update/Data_final/bank_export.csv")
bank_table_col = pd.DataFrame(bank_table.columns,columns=['col'])
bank_table_col['range'] = range(1,len(bank_table_col)+1,1)
bank_table_col['rename_col'] = 'Bank' + bank_table_col['range'].astype(str)
bank_table.rename(columns=dict(zip(bank_table_col['col'],bank_table_col['rename_col'])),inplace=True)
#%%
""" Create Export data to bank table"""
obj_col = bank_table.select_dtypes(include="object").columns.to_list()
for col in obj_col:
    bank_table[col].astype(str)
bank_table.replace([np.inf, -np.inf], np.nan, inplace=True)

# %%
result = engine.execute("DROP TABLE IF EXISTS bank_table;")
bank_table.to_sql("bank_table", engine, index=False)
# %%
# %%

Thong_tin_co_ban_table = pd.read_csv(
    "C:/Users/Chi Hieu/project/Update/Data_final/thong_tin_co_ban.csv", encoding="utf8"
)
Thong_tin_co_ban_table.columns
column = [
    "Ticker",
    "Short_name",
    "San",
    "Level1",
    "Level2",
    "Level3",
    "Level4",
    "So_co_phieu_niem_yet",
    "So_co_phieu_luu_hanh",
    "So_co_phieu_luu_hanh_binh_quan",
    "Free_float",
    "Gia",
    "Von_hoa",
    "Khoi_luong_30_ngay",
    "Khoi_luong_30_ngay_tren_co_phieu",
    "90_ngay",
    "90_ngay/cp",
    "180_ngay",
    "180_ngay/cp",
]
column_name = Thong_tin_co_ban_table.columns.to_list()[:19]
col = zip(column_name, column)
re_col = dict(col)
Thong_tin_co_ban_table.rename(columns=re_col, inplace=True)
Thong_tin_co_ban_table_short = Thong_tin_co_ban_table[column]
for col in column[:7]:
    Thong_tin_co_ban_table_short[col].astype(str).str.decode(encoding="UTF-8")
Thong_tin_co_ban_table_short.head()
# %%
result = engine.execute("DROP TABLE IF EXISTS thong_tin_co_ban;")
#%%
Thong_tin_co_ban_table_short.to_sql("thong_tin_co_ban", engine, index=False)

# %%
gia_table = pd.read_csv(
    "C:/Users/Chi Hieu/project/Update/Data_final/data_gia.csv", encoding="utf8"
)
gia_table.head()
#%%
result = engine.execute("DROP TABLE IF EXISTS Gia;")
gia_table.to_sql("Gia", engine, index=False)
# %%
gia = pd.read_sql_query('select Ticker,Ngay,Gia from Gia where Ticker ="AAA"', engine)
gia.head()
gia.plot(x="Ngay", y="Gia")
# %%

ticker
# %%
