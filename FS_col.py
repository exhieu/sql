#%%
import mysql.connector
from sqlalchemy import create_engine
import numpy as np
import pandas as pd
import glob
import unidecode
engine = create_engine("mysql+pymysql://root:@localhost/faviz")
bctc_col = pd.read_excel('Data_tai_chinh/FAViz DB Reference.xlsx')
bctc_col.dropna(how='all',inplace=True)
bctc_col
# %%
df=pd.DataFrame()
for col in bctc_col.columns[:6]:
    bctc_col_1 = bctc_col[col].to_frame().dropna()
    bctc_col_1['stt'] = np.arange(1,len(bctc_col_1)+1,1)
    bctc_col_1['Col_id'] = col+bctc_col_1['stt'].astype(str)
    bctc_col_1.rename(columns={col:'Col_name'},inplace=True)
    df = df.append(bctc_col_1)
df_dict = dict(zip(df['Col_name'],df['Col_id']))
df_dict
# %%
df1 = bctc_col.iloc[:,0].dropna().to_frame()
df1['Col_name'] = df1['I_FS']
df1['Parent'] = np.nan
parent = df1[['Parent','Col_name']].copy()
parent

for i in range(0,5):
    col = pd.DataFrame(bctc_col.iloc[:,i:i+2].dropna(how='all').values,columns=['Parent','Col_name'])
    col['Parent'] = col['Parent'].fillna(method='ffill')
    col.dropna(subset=['Col_name'],inplace=True)
    parent = parent.append(col)
parent
# %%
df_col_name = parent[['Col_name','Parent']]
df_col_name['Col_id'] = df_col_name['Col_name'].map(df_dict)
df_col_name['Parent_id'] = df_col_name['Parent'].map(df_dict)
df_col_name_db = df_col_name[['Col_id','Col_name','Parent_id']].copy()
df_col_name_db
# %%
result = engine.execute("DROP TABLE IF EXISTS Column_hierarchy;")
df_col_name_db.to_sql("Column_hierarchy", engine, index=False)
# %%
