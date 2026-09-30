import streamlit as st
st.image("logo.jpg")
# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="Tính lãi tiết kiệm",
    page_icon="💰",
    layout="centered"
)

# =========================
# TIÊU ĐỀ
# =========================
st.title("💰 APP TÍNH LÃI TIẾT KIỆM")
st.write("Tính tiền lãi theo phương pháp lãi đơn và lãi kép.")

st.divider()

# =========================
# NHẬP DỮ LIỆU
# =========================
st.subheader("📌 Thông tin tiền gửi")

tien_gui = st.number_input(
    "Số tiền gửi (VNĐ)",
    min_value=0.0,
    value=10000000.0,
    step=500000.0,
    format="%.0f"
)

ky_han = st.number_input(
    "Kỳ hạn (tháng)",
    min_value=1,
    max_value=120,
    value=12,
    step=1
)

lai_suat = st.number_input(
    "Lãi suất (%/năm)",
    min_value=0.0,
    max_value=100.0,
    value=6.0,
    step=0.1
)

hinh_thuc_lai = st.selectbox(
    "Hình thức tính lãi",
    [
        "Lãi đơn",
        "Lãi kép"
    ]
)

hinh_thuc_nhan = st.selectbox(
    "Hình thức nhận lãi",
    [
        "Lãnh lãi theo tháng",
        "Lãnh lãi theo quý",
        "Lãnh lãi cuối kỳ"
    ]
)

# =========================
# NÚT TÍNH
# =========================
if st.button("🧮 TÍNH LÃI", use_container_width=True):

    if tien_gui <= 0:
        st.error("Vui lòng nhập số tiền gửi lớn hơn 0.")
    elif lai_suat < 0:
        st.error("Lãi suất không được âm.")
    else:

        # Chuyển lãi suất năm sang số thập phân
        r = lai_suat / 100

        # Kỳ hạn tính theo năm
        so_nam = ky_han / 12

        # =========================
        # LÃI ĐƠN
        # =========================
        if hinh_thuc_lai == "Lãi đơn":

            tong_lai = tien_gui * r * so_nam

            tong_tien = tien_gui + tong_lai

            # Lãi theo tháng
            lai_thang = tien_gui * r / 12

            # Lãi theo quý
            lai_quy = tien_gui * r / 4

            if hinh_thuc_nhan == "Lãnh lãi theo tháng":
                tien_lai_dinh_ky = lai_thang

            elif hinh_thuc_nhan == "Lãnh lãi theo quý":
                tien_lai_dinh_ky = lai_quy

            else:
                tien_lai_dinh_ky = tong_lai

        # =========================
        # LÃI KÉP
        # =========================
        else:

            # Lãi kép phụ thuộc vào số lần nhập lãi
            if hinh_thuc_nhan == "Lãnh lãi theo tháng":

                so_ky = ky_han
                lai_ky = r / 12

                tong_tien = tien_gui * (1 + lai_ky) ** so_ky

                tong_lai = tong_tien - tien_gui

                # Lãi của kỳ đầu tiên
                tien_lai_dinh_ky = tien_gui * lai_ky

            elif hinh_thuc_nhan == "Lãnh lãi theo quý":

                so_ky = ky_han / 3
                lai_ky = r / 4

                tong_tien = tien_gui * (1 + lai_ky) ** so_ky

                tong_lai = tong_tien - tien_gui

                # Lãi của quý đầu tiên
                tien_lai_dinh_ky = tien_gui * lai_ky

            else:
                # Lãnh lãi cuối kỳ:
                # Tiền được nhập lãi theo năm
                # Nếu kỳ hạn dưới 12 tháng thì tính theo tỷ lệ thời gian

                tong_tien = tien_gui * (1 + r) ** so_nam

                tong_lai = tong_tien - tien_gui

                tien_lai_dinh_ky = tong_lai

        # =========================
        # HIỂN THỊ KẾT QUẢ
        # =========================
        st.divider()

        st.subheader("📊 Kết quả")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "💵 Tiền lãi định kỳ",
                f"{tien_lai_dinh_ky:,.0f} VNĐ"
            )

        with col2:
            st.metric(
                "📈 Tổng tiền lãi",
                f"{tong_lai:,.0f} VNĐ"
            )

        st.metric(
            "💰 Tổng tiền gốc + lãi",
            f"{tong_tien:,.0f} VNĐ"
        )

        # =========================
        # THÔNG TIN CHI TIẾT
        # =========================
        st.divider()

        st.subheader("📋 Thông tin khoản gửi")

        st.write(f"**Số tiền gửi:** {tien_gui:,.0f} VNĐ")
        st.write(f"**Kỳ hạn:** {ky_han} tháng")
        st.write(f"**Lãi suất:** {lai_suat:.2f}%/năm")
        st.write(f"**Phương pháp:** {hinh_thuc_lai}")
        st.write(f"**Hình thức nhận lãi:** {hinh_thuc_nhan}")
