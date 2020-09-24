#%%
import pandas as pd
import numpy as np

# import matplotlib as mpl


class ChiSoTaiChinhNam:
    def __init__(self, data_tai_chinh):
        self.data_tai_chinh = data_tai_chinh
        # self.data_tai_chinh_quy = data_tai_chinh_quy

    def trung_binh(self, bien):
        # trung binh chi dung de tinh khi cong thuc co ca so cong don va so thoi diem.
        self.bien = bien
        return self.bien.rolling(window=2, min_periods=1).mean()

    def Cong_don(self, bien):
        # trung binh chi dung de tinh khi cong thuc co ca so cong don va so thoi diem.
        self.bien = bien
        return self.bien.rolling(window=4, min_periods=1).sum()

    def So_co_phieu_trung_binh(self):
        return self.trung_binh(self.data_tai_chinh.Von_gop) / 10000

    def So_co_phieu(self):
        return self.data_tai_chinh.Von_gop / 10000

    def EPS(self):
        return (
            self.data_tai_chinh.Co_dong_cua_cong_ty_me
            / self.So_co_phieu_trung_binh()
        )

    def PE(self):
        return self.data_tai_chinh["Gia"] / self.EPS()

    def EBIT(self):
        return (
            self.data_tai_chinh.Lai_gop
            + self.data_tai_chinh.Chi_phi_tien_lai
            + self.data_tai_chinh.Chi_phi_thue_thu_nhap_doanh_nghiep
        )

    def Bien_EBIT(self):
        return 100 * self.EBIT() / self.data_tai_chinh.Doanh_so_thuan

    def Bien_lai_gop(self):
        return (
            100
            * self.data_tai_chinh.Lai_gop
            / self.data_tai_chinh.Doanh_so_thuan
        )

    def EBITDA(self):
        return (
            self.data_tai_chinh.Lai_gop
            + self.data_tai_chinh.Chi_phi_tien_lai
            + self.data_tai_chinh.Chi_phi_thue_thu_nhap_doanh_nghiep
            + self.data_tai_chinh.Khau_hao_tscd
        )

    def Ty_le_khau_hao(self):
        return (
            100
            * self.data_tai_chinh.Khau_hao_tscd
            / (
                self.data_tai_chinh.Gtcl_tscd_huu_hinh
                + self.data_tai_chinh.Khau_hao_tscd
            )
        )

    def Bien_lai_rong(self):
        return (
            100
            * self.data_tai_chinh.Lai_thuan_sau_thue
            / self.data_tai_chinh.Doanh_so_thuan
        )

    def BV(self):
        return (
            self.data_tai_chinh.Von_chu_so_huu
            - self.data_tai_chinh.Loi_ich_co_dong_khong_kiem_soat
        )

    def BVPS(self):
        return self.BV() / self.So_co_phieu()

    def PB(self):
        return self.data_tai_chinh.Gia / self.BVPS()

    def PS(self):
        return self.data_tai_chinh.Gia / self.data_tai_chinh_nam.Doanh_so_thuan

    def Von_hoa(self):
        return self.data_tai_chinh.Gia * self.So_co_phieu()

    def EV(self):
        return (
            self.Von_hoa()
            + self.data_tai_chinh.No_phai_tra
            - self.data_tai_chinh.Tien_va_tuong_duong_tien
        )

    def EV_tren_EBITDA(self):
        return self.EV() / self.EBITDA()

    def NCAV(self):
        return (
            self.data_tai_chinh.Tien_va_tuong_duong_tien
            - self.data_tai_chinh.No_ngan_han
        )

    def Chi_phi_hoat_dong_tren_doanh_thu(self):
        return (
            100
            * abs(
                self.data_tai_chinh.Chi_phi_ban_hang
                + self.data_tai_chinh.Chi_phi_quan_ly_doanh__nghiep
            )
            / self.data_tai_chinh.Doanh_so_thuan
        )

    def Chi_phi_ban_hang_tren_doanh_thu(self):
        return (
            100
            * abs(self.data_tai_chinh.Chi_phi_ban_hang)
            / self.data_tai_chinh.Doanh_so_thuan
        )

    def ROA(self):
        return (
            100
            * self.data_tai_chinh.Co_dong_cua_cong_ty_me
            / self.data_tai_chinh.Tong_cong_tai_san
        )

    def ROE(self):
        return (
            100
            * self.data_tai_chinh.Co_dong_cua_cong_ty_me
            / abs(self.data_tai_chinh.Von_chu_so_huu)
        )

    def Vong_quay_tai_san(self):
        return (
            self.data_tai_chinh.Doanh_so_thuan
            / self.data_tai_chinh.Tong_cong_tai_san.shift()
        )

    def IC(self):
        return (
            self.data_tai_chinh.Von_chu_so_huu
            + self.data_tai_chinh.Vay_va_no_nh
            + self.data_tai_chinh.Vay_dai_han
        )

    def ROIC(self):
        return (
            100
            * self.EBIT()
            / (
                self.trung_binh(
                    (
                        self.data_tai_chinh.Von_chu_so_huu
                        + self.data_tai_chinh.Vay_va_no_nh
                        + self.data_tai_chinh.Vay_dai_han
                    )
                    # - (
                    #     self.data_tai_chinh.Tien_va_tuong_duong_tien
                    #     + self.data_tai_chinh.Gia_tri_thuan_dau_tu_ngan_han
                    #     + self.data_tai_chinh.Dau_tu_dai_han
                    # )
                )
            )
        )

    def Working_IC(self):
        return (
            self.data_tai_chinh.Von_chu_so_huu
            + self.data_tai_chinh.Vay_va_no_nh
            + self.data_tai_chinh.Vay_dai_han
        ) - (
            self.data_tai_chinh.Tien_va_tuong_duong_tien
            + self.data_tai_chinh.Gia_tri_thuan_dau_tu_ngan_han
            + self.data_tai_chinh.Dau_tu_dai_han
        )

    def No_chiem_dung(self):
        return self.data_tai_chinh.Tong_cong_nguon_von - self.IC()

    def Chi_so_tien_mat(self):
        return (
            self.data_tai_chinh.Tien_va_tuong_duong_tien
            + self.data_tai_chinh.Gia_tri_thuan_dau_tu_ngan_han
        ) / self.data_tai_chinh.No_ngan_han

    def Chi_so_thanh_toan_nhanh(self):
        return (
            self.data_tai_chinh.Tai_san_ngan_han
            - self.data_tai_chinh.Hang_ton_kho
        ) / self.data_tai_chinh.No_ngan_han

    def Chi_so_thanh_toan_hien_hanh(self):
        return (
            self.data_tai_chinh.Tai_san_ngan_han
            / self.data_tai_chinh.No_ngan_han
        )

    def Dau_tu_tscd_rong(self):
        return (
            self.data_tai_chinh.Tien_mua_tai_san_co_dinh_va_cac_tai_san_dai_han_khac
            + self.data_tai_chinh.Tien_thu_duoc_tu_thanh_ly_tai_san_co_dinh
        )

    def Dau_tu_tai_chinh_rong(self):
        return (
            self.data_tai_chinh.Tien_cho_vay_hoac_mua_cong_cu_no
            + self.data_tai_chinh.Tien_thu_tu_cho_vay_hoac_thu_tu_phat_hanh_cong_cu_no
            + self.data_tai_chinh.Dau_tu_vao_cac_doanh_nghiep_khac
        )

    def Dau_tu_khac(self):
        return self.data_tai_chinh.Luu_chuyen_tien_te_rong_tu_hoat_dong_dau_tu - (
            self.Dau_tu_tscd_rong() + self.Dau_tu_tai_chinh_rong()
        )

    def Dong_tien_tu_do(self):
        return (
            self.data_tai_chinh.Luu_chuyen_tien_te_rong_tu_cac_hoat_dong_san_xuat_kinh_doanh
            + self.Dau_tu_tscd_rong()
        )

    def Ty_le_co_tuc_tien_mat(self):
        return abs(self.data_tai_chinh.Co_tuc_da_tra) / self.trung_binh(
            self.data_tai_chinh.Von_gop
        )

    def Ty_le_co_tuc_so_voi_dong_tien_tu_do(self):
        return abs(self.data_tai_chinh.Co_tuc_da_tra) / self.Dong_tien_tu_do()

    def Ty_le_tien_va_dau_tu_tai_chinh_tren_tts(self):
        return (
            self.data_tai_chinh.Tien_va_tuong_duong_tien
            + self.data_tai_chinh.Gia_tri_thuan_dau_tu_ngan_han
        ) / self.data_tai_chinh.Tong_cong_tai_san

    def So_ngay_phai_thu(self):
        return round(
            360
            * self.trung_binh(self.data_tai_chinh.Cac_khoan_phai_thu)
            / self.data_tai_chinh.Doanh_so_thuan
        )

    def So_ngay_phai_tra(self):
        return round(
            360
            * self.trung_binh(self.data_tai_chinh.Phai_tra_nguoi_ban)
            / self.data_tai_chinh.Doanh_so_thuan
        )

    def So_ngay_ton_kho(self):
        return round(
            360
            * self.trung_binh(self.data_tai_chinh.Hang_ton_kho)
            / self.data_tai_chinh.Doanh_so_thuan
        )

    def Chu_ky_tien_mat(self):
        return (
            self.So_ngay_ton_kho() + self.So_ngay_phai_thu() - self.So_ngay_phai_tra()
        )

    def Tong_no_vay(self):
        return (
            self.data_tai_chinh.Vay_va_no_nh + self.data_tai_chinh_nam.Vay_dai_han
        )

    def No_vay_rong(self):
        return (
            self.Tong_no_vay()
            - self.data_tai_chinh.Tien_va_tuong_duong_tien
            - self.data_tai_chinh.Gia_tri_thuan_dau_tu_ngan_han
        )

    def VCSH(self):
        return (
            self.data_tai_chinh.Von_chu_so_huu
            - self.data_tai_chinh.Loi_ich_co_dong_khong_kiem_soat
        )

    def D_tren_E(self):
        return self.Tong_no_vay() / self.VCSH()

    def F_score(self):
        F_score = self.data_tai_chinh[["Ticker", "Yearreport"]]

        F_score["LN_tang_truong"] = [
            # Positive netincome replace by positive growth EBIT to get grow copany
            1 if x > 0 else 0
            for x in self.EBIT().diff()
        ]

        F_score["Dong_tien_duong"] = [
            1 if x > 0 else 0
            for x in self.data_tai_chinh.Luu_chuyen_tien_te_rong_tu_cac_hoat_dong_san_xuat_kinh_doanh
        ]
        # Nên thay ROA bằng ROIC để xác định các doanh nghiệp kinh doanh tốt hơn từ vốn chủ sở hữu.
        F_score["Tang_hq_tai_san"] = [1 if x > 0 else 0 for x in self.ROA().diff()]

        F_score["Dong_tien_tot"] = [
            1 if x > y else 0
            for x, y in zip(
                self.data_tai_chinh.Luu_chuyen_tien_te_rong_tu_cac_hoat_dong_san_xuat_kinh_doanh,
                self.data_tai_chinh.Lai_thuan_sau_thue
                + self.data_tai_chinh.Khau_hao_tscd,
            )
        ]

        F_score["Don_bay_giam"] = [
            1 if x < 0 else 0
            for x in (
                self.data_tai_chinh.No_dai_han
                / self.data_tai_chinh.Von_chu_so_huu
            ).diff()
        ]

        F_score["Kn_tt_tang"] = [
            1 if x > 0 else 0 for x in self.Chi_so_thanh_toan_hien_hanh().diff()
        ]
        # loại bỏ tang vôn từ lọi nhuận chưa phân phối.
        F_score["Khong_phat_hanh_tang_von"] = [
            1 if x < y * 1.05 else 0
            for x, y in zip(
                self.data_tai_chinh.Von_gop,
                self.data_tai_chinh.Von_chu_so_huu.shift()
                + self.data_tai_chinh.Lai_thuan_sau_thue
                + self.data_tai_chinh.Co_tuc_da_tra
                - (
                    self.data_tai_chinh.Von_chu_so_huu
                    - self.data_tai_chinh.Von_gop
                ),
            )
        ]
        # dung biên ebit thay vì Biên lãi gộp trong trường hợp doanh nghiêp tăng dtu tài sản vào sản xuất
        F_score["Bien_ebit_tang"] = [1 if x > 0 else 0 for x in self.Bien_EBIT().diff()]
        # nen thay bang vong quay tai san co dinh nhưng chưa kiểm soát dc thay đỏi tài sản cố định
        F_score["Vong_quay_ts_tang"] = [
            1 if x > 0 else 0 for x in self.Vong_quay_tai_san().diff()
        ]

        F_score["F"] = (
            F_score["LN_tang_truong"]
            + F_score["Dong_tien_duong"]
            + F_score["Tang_hq_tai_san"]
            + F_score["Dong_tien_tot"]
            + F_score["Don_bay_giam"]
            + F_score["Kn_tt_tang"]
            + F_score["Khong_phat_hanh_tang_von"]
            + F_score["Bien_ebit_tang"]
            + F_score["Vong_quay_ts_tang"]
        )
        return F_score


class ChiSoTaiChinhQuy(ChiSoTaiChinhNam):

    def Doanh_so_thuan_gop(self):
        return self.Cong_don(self.data_tai_chinh.Doanh_so_thuan)
    
    def PS_gop(self):
        return self.data_tai_chinh.Gia / self.Doanh_so_thuan_gop()
    
    def EBIT_gop(self):
        return self.Cong_don(
            self.data_tai_chinh.Lai_gop
            + self.data_tai_chinh.Chi_phi_tien_lai
            + self.data_tai_chinh.Chi_phi_thue_thu_nhap_doanh_nghiep
        )
    def EPS_gop(self):
        return self.Cong_don(
            (
                    self.data_tai_chinh.Co_dong_cua_cong_ty_me
                / self.So_co_phieu_trung_binh()
            )
        )
    def PE_quy(self):
        return self.data_tai_chinh["Gia"] / self.EPS_gop()