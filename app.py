import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="ระบบบันทึกข้อมูลฟาร์มกุ้ง", page_icon="🦐", layout="wide")

# ส่วนหัวด้านบน: แสดงนาฬิกาและพยากรณ์อากาศที่มุมขวา
top_col1, top_col2 = st.columns([3, 1])

with top_col1:
    st.title("🦐 ระบบบันทึกข้อมูลฟาร์มกุ้ง (Shrimp Farm Management)")

with top_col2:
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    st.markdown(f"""
    <div style="text-align: right; background-color: #f0f2f6; padding: 10px; border-radius: 10px;">
        <span style="font-size: 14px; font-weight: bold;">⏰ เวลา: {current_time}</span><br>
        <span style="font-size: 12px; color: #555;">🌤️ พยากรณ์อากาศ (3 วัน):</span><br>
        <span style="font-size: 11px; color: #333;">วันนี้: 32°C ฝนฟ้าคะนอง<br>พรุ่งนี้: 33°C แดดจัด<br>มะรืน: 31°C มีเมฆมาก</span>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# เมนูด้านข้างแยกตามหัวข้อสำคัญ
menu = st.sidebar.selectbox(
    "เลือกเมนูหลัก",
    [
        "📋 1. บันทึกรายวัน (Daily Log)",
        "💧 2. ติดตามคุณภาพน้ำ (pH / DO)",
        "🦐 3. บันทึกการสุ่มยอและโต (Sampling)",
        "💰 4. บันทึกต้นทุนราย Crop",
        "📊 5. สรุปผลผลิตและกำไรขาดทุน"
    ]
)

# ---------------------------------------------------------
# เมนูที่ 1: บันทึกรายวัน (Daily Log)
# ---------------------------------------------------------
if menu == "📋 1. บันทึกรายวัน (Daily Log)":
    st.header("📋 บันทึกข้อมูลการเลี้ยงกุ้งรายวัน")
    
    with st.form("daily_log_form"):
        st.subheader("กรอกข้อมูลประจำวัน")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            log_date = st.date_input("วันที่", datetime.date.today())
            doc = st.number_input("อายุการเลี้ยง (DOC)", min_value=0, value=1)
            feed_no = st.text_input("เบอร์อาหาร / ล็อต")
            feed_amt = st.number_input("ปริมาณอาหารที่ให้ (กก.)", min_value=0.0, format="%.2f")
            
        with col2:
            dead_shrimp = st.number_input("จำนวนกุ้งตาย (ตัว)", min_value=0, value=0)
            aerator_hrs = st.number_input("ชั่วโมงเปิดเครื่องตีน้ำ", min_value=0.0, value=24.0, format="%.1f")
            chemical = st.text_input("สารเคมี / จุลินทรีย์ที่ใส่")
            
        with col3:
            behavior = st.text_area("พฤติกรรม / ลักษณะกุ้ง")
            note = st.text_area("หมายเหตุ / การเปลี่ยนน้ำ")
            
        submitted = st.form_submit_button("บันทึกข้อมูลรายวัน")
        if submitted:
            st.success(f"บันทึกข้อมูลวันที่ {log_date} (DOC {doc}) สำเร็จเรียบร้อย!")

    st.divider()
    st.subheader("📊 ตารางประวัติบันทึกรายวัน")
    sample_daily = pd.DataFrame({
        "วันที่": ["2026-06-01", "2026-06-02"],
        "DOC": [1, 2],
        "เบอร์อาหาร": ["No.1", "No.1"],
        "อาหาร (กก.)": [10.5, 12.0],
        "กุ้งตาย (ตัว)": [2, 1]
    })
    st.dataframe(sample_daily, use_container_width=True)

# ---------------------------------------------------------
# เมนูที่ 2: ติดตามคุณภาพน้ำ (pH / DO)
# ---------------------------------------------------------
elif menu == "💧 2. ติดตามคุณภาพน้ำ (pH / DO)":
    st.header("💧 บันทึกและวิเคราะห์คุณภาพน้ำ (pH / DO / อุณหภูมิ)")
    
    with st.form("water_form"):
        col1, col2 = st.columns(2)
        with col1:
            w_date = st.date_input("วันที่ตรวจน้ำ", datetime.date.today())
            ph_morning = st.number_input("ค่า pH (เช้า)", value=7.5, format="%.1f")
            ph_evening = st.number_input("ค่า pH (เย็น)", value=8.0, format="%.1f")
            do_morning = st.number_input("ค่า DO เช้า (mg/l)", value=5.5, format="%.1f")
        with col2:
            do_night = st.number_input("ค่า DO ดึก (mg/l)", value=5.0, format="%.1f")
            temp = st.number_input("อุณหภูมิ (°C)", value=28.0, format="%.1f")
            salinity = st.number_input("ความเค็ม (ppt)", value=15.0, format="%.1f")
            water_remark = st.text_input("หมายเหตุสภาพน้ำ")
            
        w_submitted = st.form_submit_button("บันทึกค่าคุณภาพน้ำ")
        if w_submitted:
            st.success("บันทึกข้อมูลคุณภาพน้ำสำเร็จ! (ระบบช่วยตรวจสอบความปลอดภัยของค่า pH และ DO ให้เรียบร้อย)")

    st.divider()
    st.subheader("📈 กราฟแสดงแนวโน้มคุณภาพน้ำย้อนหลัง")
    water_data = pd.DataFrame({
        "DOC": [1, 2, 3, 4, 5],
        "pH เช้า": [7.5, 7.6, 7.4, 7.5, 7.6],
        "pH เย็น": [8.0, 8.2, 7.9, 8.1, 8.0]
    }).set_index("DOC")
    st.line_chart(water_data)

# ---------------------------------------------------------
# เมนูที่ 3: บันทึกการสุ่มยอและโต (Sampling)
# ---------------------------------------------------------
elif menu == "🦐 3. บันทึกการสุ่มยอและโต (Sampling)":
    st.header("🦐 บันทึกผลการสุ่มยอและน้ำหนักเฉลี่ย (ABW)")
    
    with st.form("sample_form"):
        col1, col2 = st.columns(2)
        with col1:
            s_doc = st.number_input("อายุการเลี้ยง (DOC) ที่สุ่ม", min_value=1, value=30)
            abw = st.number_input("น้ำหนักเฉลี่ยต่อตัว (กรัม - ABW)", min_value=0.0, format="%.2f")
        with col2:
            check_result = st.text_input("ผลการเช็กยอ / การกินอาหาร")
            est_survival = st.slider("ประเมินอัตรารอด (%) คาดการณ์", 0, 100, 85)
            
        s_submitted = st.form_submit_button("บันทึกผลสุ่มยอ")
        if s_submitted:
            st.success(f"บันทึกสำเร็จที่ DOC {s_doc} | ABW: {abw} กรัม | อัตรารอดประเมิน: {est_survival}%")

    st.divider()
    st.subheader("📊 ตารางประวัติการเจริญเติบโต")
    sample_growth = pd.DataFrame({
        "DOC": [30, 45, 60],
        "น้ำหนักเฉลี่ย (ABW g.)": [3.5, 7.2, 12.5],
        "อัตรารอด (%)": [90, 88, 85]
    })
    st.dataframe(sample_growth, use_container_width=True)

# ---------------------------------------------------------
# เมนูที่ 4: บันทึกต้นทุนราย Crop
# ---------------------------------------------------------
elif menu == "💰 4. บันทึกต้นทุนราย Crop":
    st.header("💰 บันทึกต้นทุนประจำรอบการเลี้ยง (Crop Cost)")
    
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
            item_detail = st.text_input("รายการรายละเอียด (เช่น ค่าลูกกุ้ง, ค่าอาหารเบอร์ 1)")
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

# ---------------------------------------------------------
# เมนูที่ 5: สรุปผลผลิตและกำไรขาดทุน
# ---------------------------------------------------------
elif menu == "📊 5. สรุปผลผลิตและกำไรขาดทุน":
    st.header("📊 สรุปผลผลิต รายได้ และกำไรสุทธิประจำรอบการเลี้ยง")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="📦 ผลผลิตรวมที่จับได้ (กก.)", value="3,500 กก.")
    with col2:
        st.metric(label="💰 รายรับจากการขายกุ้ง", value="630,000 บาท")
    with col3:
        st.metric(label="📉 ต้นทุนรวมทั้งหมด", value="188,000 บาท")
        
    st.divider()
    net_profit = 630000 - 188000
    st.success(f"### 🎉 กำไรสุทธิประจำรอบ (Net Profit): {net_profit:,.2f} บาท")
    
    st.subheader("📋 รายละเอียดการจับขาย (Harvest Record)")
    harvest_df = pd.DataFrame({
        "1": ["รอบการเลี้ยง", "Crop 1/2026"],
        "2": ["น้ำหนักเฉลี่ยตอนจับ (กรับ/ตัว)", "14.2 กรัม"],
        "3": ["เปอร์เซ็นต์รอดจริง", "84.5%"],
        "4": ["ราคาขายเฉลี่ย (บาท/กก.)", "180 บาท"]
    })
    st.table(harvest_df)
