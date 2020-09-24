#%%
import mysql.connector
from sqlalchemy import create_engine
import numpy as np
import pandas as pd
import glob
import unidecode

engine = create_engine("mysql+pymysql://root:@localhost/faviz")

# %%
""" Rename fiin_data excel to FiinPro* for not select unsave excel file"""
filenames = glob.glob("Data_tai_chinh/BCTC_nam/FiinPro*.xlsm")
# %%
data = pd.DataFrame()
for file in filenames:
    fiin_sheet = pd.read_excel(file, sheet_name="fiin", skiprows=8)
    fiin_sheet.dropna(subset=["Unnamed: 1", "Unnamed: 2"], inplace=True)
    data = data.append(fiin_sheet)
    print(file)
data.drop(
    [
        "Unnamed: 0",
        "Unnamed: 2",
        "Unnamed: 3",
        "Unnamed: 4",
        "Unnamed: 5",
        "Unnamed: 6",
        "Unnamed: 7",
    ],
    axis=1,
    inplace=True,
)
data.drop([0], axis=0, inplace=True)
data.rename(
    columns={
        "Unnamed: 1": "Ticker",
        # "Unnamed: 2": "Tên công ty",
        # "Unnamed: 3": "Sàn",
        # "Unnamed: 4": "Ngành cấp 1",
        # "Unnamed: 5": "Ngành cấp 2",
        # "Unnamed: 6": "Ngành cấp 3",
        # "Unnamed: 7": "Ngành cấp 4",
        "Unnamed: 8": "Quý",
        "Unnamed: 9": "Năm",
        "Unnamed: 10": "Kiểm toán",
        "Lưu chuyển tiền tệ ròng từ các hoạt động sản xuất kinh doanh Đơn vị: Tỷ VNĐ": "LCTT ròng từ HDSXKD Đơn vị: Tỷ VNĐ",
        "Tiền mua tài sản cố định và các tài sản dài hạn khác Đơn vị: Tỷ VNĐ": "Tiền mua TSCĐ và TSDH khác Đơn vị: Tỷ VNĐ",
        "Tiền thu từ cho vay hoặc thu từ phát hành công cụ nợ Đơn vị: Tỷ VNĐ": "Tiền thu từ cho vay hoặc PPCCN Đơn vị: Tỷ VNĐ",
        "Dự phòng giảm giá các khoản đầu tư ngắn hạn, dài hạn Đơn vị: Tỷ VNĐ": "Dự phòng DT NH và DH Đơn vị: Tỷ VNĐ",
        "VỐN CHỦ SỞ HỮU Đơn vị: Tỷ VNĐ": "Tổng vốn chủ sở hữu Đơn vị: Tỷ VNĐ",
    },
    inplace=True,
)
# %%
rename_col_df = pd.DataFrame(data.columns, columns=["Natural_name"])
col = {
    i: unidecode.unidecode(
        i.capitalize()
        .replace('"', "")
        .replace(',', "")
        .replace("\\", " ")
        .replace("/", " ")
        .replace("(", "")
        .replace(")", "")
        .replace("-", "").strip()
    )
    .replace(" ", "_")
    .replace("_don_vi:_ty_vnd", "")
    .replace("_don_vi:_undefined", "")
    # .strip()
    for i in list(rename_col_df["Natural_name"].astype(str))
}
col
rename_col_df['DB_name'] = col.values()
# %%
data.rename(columns=col, inplace=True)
data["id"] = data["Ticker"] + data["Nam"].astype(str) + "A"
# data["id"] = data["Ticker"] + data["Nam"].astype(str) + "Q" + data['Quy'].astype(str)
data
#%%
col = set(data.columns)
object_col = set(['Ticker','Trang_thai_kiem_toan','id','Ttgt'])
float_col = col.difference(object_col)
float_col
for col in float_col:
    data[col] = data[col].astype(float)

# %%
data.drop_duplicates(subset="id", inplace=True)
# data.set_index("id", inplace=True)
# result = engine.execute("DROP TABLE IF EXISTS Bao_cao_tai_chinh;")
data.to_sql("Bao_cao_tai_chinh", engine, if_exists="append", index=False)
# %%
result = engine.execute("DROP TABLE IF EXISTS Bao_cao_tai_chinh_column;")
rename_col_df.to_sql("Bao_cao_tai_chinh_column", engine, index=False)

# %quy
