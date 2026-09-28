import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="ระบบบันทึกข้อมูลฟาร์มกุ้ง", page_icon="🦐", layout="wide")

st.title("🦐 ระบบบันทึกข้อมูลฟาร์มกุ้ง (Shrimp Farm Management)")

# เมนูด้านข้าง
menu = st.sidebar.selectbox(
    "เลือกเมนูหลัก",
    ["1. บันทึกรายวัน (Daily Log)", "2. บันทึกต้นทุนราย Crop"]
)

# ---------------------------------------------------------
# เมนูที่ 1: บันทึกรายวัน (Daily Log)
# ---------------------------------------------------------
if menu == "1. บันทึกรายวัน (Daily Log)":
    st.header("📋 บันทึกข้อมูลการเลี้ยงกุ้งรายวัน")
    
    with st.form("daily_log_form"):
        st.subheader("กรอกข้อมูลประจำวันตามเกณฑ์บ่อกุ้ง")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            log_date = st.date_input("วันที่", datetime.date.today())
            doc = st.number_input("อายุการเลี้ยง (DOC)", min_value=0, value=1)
            feed_no = st.text_input("เบอร์อาหาร / ล็อต")
            feed_amt = st.number_input("ปริมาณอาหารที่ให้ (กก.)", min_value=0.0, format="%.2f")
            check_yhor = st.text_input("ผลการเช็กยอ (มื้อหลัก)")
            
        with col2:
            water_time = st.text_input("เวลาตรวจน้ำ", "06:00 / 18:00")
            do_val = st.text_input("DO (mg/l) [เช้า/ดึก]")
            ph_val = st.text_input("pH [เช้า/เย็น]")
            temp = st.number_input("อุณหภูมิ (°C)", value=28.0, format="%.1f")
            salinity = st.number_input("ความเค็ม (ppt)", value=15.0, format="%.1f")
            
        with col3:
            dead_shrimp = st.number_input("จำนวนกุ้งตาย (ตัว)", min_value=0, value=0)
            behavior = st.text_area("พฤติกรรม / ลักษณะกุ้ง")
            aerator_hrs = st.number_input("ชั่วโมงเปิดเครื่องตีน้ำ", min_value=0.0, value=24.0, format="%.1f")
            chemical = st.text_input("สารเคมี / จุลินทรีย์ที่ใส่")
            note = st.text_area("หมายเหตุ / การเปลี่ยนน้ำ")
            
        submitted = st.form_submit_button("บันทึกข้อมูลรายวัน")
        if submitted:
            st.success(f"บันทึกข้อมูลวันที่ {log_date} (DOC {doc}) สำเร็จเรียบร้อย!")

    st.divider()
    st.subheader("📊 ตัวอย่างตารางบันทึกรายวัน")
    sample_daily = pd.DataFrame({
        "วันที่": ["2026-06-01", "2026-06-02"],
        "DOC": [1, 2],
        "เบอร์อาหาร": ["No.1", "No.1"],
        "ปริมาณอาหาร (กก.)": [10.5, 12.0],
        "กุ้งตาย (ตัว)": [2, 1],
        "DO (เช้า/ดึก)": ["6.2 / 5.8", "6.0 / 5.5"],
        "อุณหภูมิ (°C)": [28.5, 29.0]
    })
    st.dataframe(sample_daily, use_container_width=True)

# ---------------------------------------------------------
# เมนูที่ 2: บันทึกต้นทุนราย Crop
# ---------------------------------------------------------
elif menu == "2. บันทึกต้นทุนราย Crop":
    st.header("💰 บันทึกต้นทุนและการคำนวณกำไรประจำรอบการเลี้ยง (Crop Cost)")
    
    category = st.selectbox(
        "หมวดหมู่ต้นทุน",
        [
            "1. ค่าพันธุ์สัตว์น้ำและเตรียมบ่อ",
            "2. ค่าอาหารกุ้ง",
            "3. ค่ายา สารเคมี และจุลินทรีย์",
            "4. ค่าพลังงาน (ไฟ/น้ำ/น้ำมัน)",
            "5. ค่าแรงงานและค่าใช้จ่ายเบ็ดเตล็ด"
        ]
    )
    
    with st.form("cost_form"):
        col1, col2 = st.columns(2)
        with col1:
            item_detail = st.text_input("รายการรายละเอียด (เช่น ค่าลูกกุ้ง, ค่าปูนขาว)")
            amount = st.number_input("จำนวนเงิน (บาท)", min_value=0.0, format="%.2f")
        with col2:
            crop_name = st.selectbox("รอบการเลี้ยง (Crop)", ["Crop 1/2026", "Crop 2/2026"])
            remark = st.text_input("หมายเหตุ")
            
        cost_submitted = st.form_submit_button("เพิ่มรายการต้นทุน")
        if cost_submitted:
            st.success(f"บันทึกรายการ '{item_detail}' จำนวน {amount:,.2f} บาท สำเร็จ!")

    st.divider()
    st.subheader("📈 สรุปต้นทุนรวมแยกตามหมวดหมู่")
    
    cost_summary = pd.DataFrame({
        "หมวดหมู่ต้นทุน": [
            "1. ค่าพันธุ์สัตว์น้ำและเตรียมบ่อ",
            "2. ค่าอาหารกุ้ง",
            "3. ค่ายา สารเคมี และจุลินทรีย์",
            "4. ค่าพลังงาน (ไฟ/น้ำ/น้ำมัน)",
            "5. ค่าแรงงานและค่าใช้จ่ายเบ็ดเตล็ด"
        ],
        "จำนวนเงินรวม (บาท)": [25000.00, 120000.00, 15000.00, 18000.00, 10000.00]
    })
    
    st.dataframe(cost_summary, use_container_width=True)
    
    total_cost = cost_summary["จำนวนเงินรวม (บาท)"].sum()
    st.metric(label="💸 ต้นทุนรวมทั้งสิ้น (Total Cost)", value=f"{total_cost:,.2f} บาท")
