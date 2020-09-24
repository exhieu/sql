#%%
import mysql.connector
from sqlalchemy import create_engine
import numpy as np
import pandas as pd
import glob
import unidecode

engine = create_engine("mysql+pymysql://root:@localhost/faviz")
# %%
thong_tin_co_ban = pd.read_csv('Thong_tin_co_ban/Thong_tin_co_ban.csv')
# nganh_nghe = thong_tin_co_ban[['Level1','Level2','Level3','Level4']].drop_duplicates().copy()
Level1 = pd.DataFrame(thong_tin_co_ban['Level1'].drop_duplicates())
Level1.rename(columns={'Level1':'Nganh'},inplace=True)
Level1['stt'] = np.arange(1,len(Level1)+1,1)
Level1['Ma_nganh'] = 'A' + Level1['stt'].astype(str)
# Level1.set_index('Level1',inplace=True)
Level1
# %%
Level2 = pd.DataFrame(thong_tin_co_ban['Level2'].drop_duplicates())
Level2.rename(columns={'Level2':'Nganh'},inplace=True)
Level2['stt'] = np.arange(1,len(Level2)+1,1)
Level2['Ma_nganh'] = 'B' + Level2['stt'].astype(str)
# Level2.set_index('Level2',inplace=True)
# %%
Level3 = pd.DataFrame(thong_tin_co_ban['Level3'].drop_duplicates())
Level3.rename(columns={'Level3':'Nganh'},inplace=True)
Level3['stt'] = np.arange(1,len(Level3)+1,1)
Level3['Ma_nganh'] = 'C' + Level3['stt'].astype(str)
# Level3.set_index('Level3',inplace=True)
# %%
Level4 = pd.DataFrame(thong_tin_co_ban['Level4'].drop_duplicates())
Level4.rename(columns={'Level4':'Nganh'},inplace=True)
Level4['stt'] = np.arange(1,len(Level4)+1,1)
Level4['Ma_nganh'] = 'D' + Level4['stt'].astype(str)
# Level4.set_index('Level4',inplace=True)

# %%
Level = Level1.append([Level2,Level3,Level4])
# level = Level.reset_index()
level_dict = dict(zip(Level.Nganh,Level.Ma_nganh))
level_dict

# %%
Parent1 = pd.DataFrame(thong_tin_co_ban[['Level2','Level1']].drop_duplicates())
Parent1['Parent'] = Parent1['Level1'].map(level_dict)
Parent1.rename(columns={"Level2":'Nganh','Level1':'Nganh_me'},inplace=True)
Parent2 = pd.DataFrame(thong_tin_co_ban[['Level3','Level2']].drop_duplicates())
Parent2['Parent'] = Parent2['Level2'].map(level_dict)
Parent2.rename(columns={"Level3":'Nganh','Level2':'Nganh_me'},inplace=True)
Parent3 = pd.DataFrame(thong_tin_co_ban[['Level4','Level3']].drop_duplicates())
Parent3['Parent'] = Parent3['Level3'].map(level_dict)
Parent3.rename(columns={"Level4":'Nganh','Level3':'Nganh_me'},inplace=True)
Parent = pd.concat([Parent1,Parent2,Parent3],ignore_index=True)
Parent
perent_dict = dict(zip(Parent['Nganh'],Parent['Parent']))
perent_dict
# %%
Level['Parent'] = Level.Nganh.map(perent_dict)
Level
# %%
Level_db = Level[['Ma_nganh','Nganh','Parent']].copy()
Level_db
# %%
# result = engine.execute("DROP TABLE IF EXISTS Ma_nganh;")
# Level_db.to_sql("Ma_nganh", engine, index=False)
# %%
ma_nganh_dict = dict(zip(Level_db['Nganh'],Level_db['Ma_nganh']))
ma_nganh_dict
thong_tin_co_ban['Ma_nganh'] = thong_tin_co_ban['Level4'].map(ma_nganh_dict)
thong_tin_co_ban.rename(columns={'Sàn NY':'San','Số CP niêm yết':'So_cp_niem_yet','Số CP lưu hành':'So_cp_luu_hanh'},inplace=True)
thong_tin_co_ban_db = thong_tin_co_ban[['Ticker','Ma_nganh','San','shortname','So_cp_niem_yet','So_cp_luu_hanh']].copy()
thong_tin_co_ban_db
# %%
result = engine.execute("DROP TABLE IF EXISTS Thong_tin_co_ban;")
thong_tin_co_ban_db.to_sql("Thong_tin_co_ban", engine, index=False)
# %%
