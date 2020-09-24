#%%
import mysql.connector
from sqlalchemy import create_engine
import numpy as np
import pandas as pd
import glob

engine = create_engine("mysql+pymysql://root:@localhost/faviz")

# %%
filenames = glob.glob("Data_gia_cuoi_ngay/CafeF.RAW*.csv")
df = pd.DataFrame()
filenames_NN = glob.glob("Data_gia_cuoi_ngay/CafeF.NN*.csv")
df_tempt_NN = pd.DataFrame()

print("Found Raw data")
#%%

for file in filenames_NN:
    df_tempt1 = pd.read_csv(file)
    df_tempt_NN = df_tempt_NN.append(df_tempt1, sort=False)
# %%

df_tempt_NN["Ticker"] = df_tempt_NN["<Ticker>"].astype(str).str[-3:]
df_tempt_NN["Nn_mua"] = df_tempt_NN["<Open>"]
df_tempt_NN["Nn_ban"] = df_tempt_NN["<Close>"]
df_tempt_NN["Gt_nn_mua"] = df_tempt_NN["<Volume>"]
df_tempt_NN["Gt_nn_ban"] = df_tempt_NN["<OI>"]
df_tempt_NN["Ngay"] = pd.to_datetime(
    df_tempt_NN["<DTYYYYMMDD>"].astype(str), format="%Y%m%d"
)
df_tempt_NN["id"] = df_tempt_NN["Ticker"] + df_tempt_NN["<DTYYYYMMDD>"].astype(str)
df_NN = df_tempt_NN[
    ["id", "Ticker", "Ngay", "Nn_mua", "Nn_ban", "Gt_nn_mua", "Gt_nn_ban"]
].set_index("id")
# %%
for file in filenames:
    df_tempt = pd.read_csv(file)
    df = df.append(df_tempt, sort=False)
df1 = df
df1["Ngay"] = pd.to_datetime(df1["<DTYYYYMMDD>"].astype(str), format="%Y%m%d")
col_name = pd.DataFrame(df1.columns, columns=["old_col"])
col_name["new_col"] = col_name["old_col"].str.replace("<", "").str.replace(">", "")
df1.rename(columns=dict(col_name.values), inplace=True)
df1["id"] = df1.Ticker + df1["DTYYYYMMDD"].astype(str)
df1[["Open", "High", "Low", "Close"]] = df1[["Open", "High", "Low", "Close"]] * 1000
df1.set_index('id',inplace=True)

# %%
data_gia = df1.merge(df_NN)
data_gia['id'] = data_gia.Ticker + data_gia['DTYYYYMMDD'].astype(str)
data_gia = data_gia.set_index('id').reset_index()
#%%
old_index = pd.read_sql_query('select "id" from Gia',engine)
old_index
# %%
data_gia.drop_duplicates(subset='id',inplace=True)
result = engine.execute("DROP TABLE IF EXISTS Gia;")
data_gia.to_sql("Gia", engine,if_exists='append', index=False)
# %%
test_data = pd.read_sql_query('select id from gia where Ticker = "HPG"',engine)
test_data
# %%
# %%
