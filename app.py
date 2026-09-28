import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="ระบบบันทึกข้อมูลฟาร์มกุ้งหลายบ่อ", page_icon="🦐", layout="wide")

# ส่วนหัวด้านบน: แสดงนาฬิกา พยากรณ์อากาศ และข้อมูลน้ำขึ้น-ลงรายวัน
top_col1, top_col2 = st.columns([2.3, 1.7])

with top_col1:
    st.title("🦐 ระบบบันทึกข้อมูลฟาร์มกุ้ง (Multi-Pond Management)")

with top_col2:
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    current_date_str = datetime.date.today().strftime("%d/%m/%Y")
    st.markdown(f"""
    <div style="text-align: right; background-color: #f0f2f6; padding: 10px; border-radius: 10px;">
        <span style="font-size: 14px; font-weight: bold;">⏰ เวลา: {current_time}</span><br>
        <span style="font-size: 12px; color: #555;">🌤️ พยากรณ์อากาศ (3 วัน):</span><br>
        <span style="font-size: 11px; color: #333;">วันนี้: 32°C ฝนฟ้าคะนอง | พรุ่งนี้: 33°C แดดจัด</span><hr style="margin: 5px 0;">
        <span style="font-size: 12px; color: #0056b3; font-weight: bold;">🌊 น้ำขึ้น-ลงรายวัน (ต.คลองขุด อ.บ้านโพธิ์):</span><br>
        <span style="font-size: 11px; color: #333;">
        📅 วันที่: <b>{current_date_str}</b><br>
        • ⬆️ น้ำขึ้นสูงสุด: <b>06:09 น.</b> (2.72 ม.) และ <b>17:59 น.</b> (2.82 ม.)<br>
        • ⬇️ น้ำลงต่ำสุด: <b>00:52 น.</b> (0.89 ม.) และ <b>12:40 น.</b> (1.07 ม.)
        </span>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# --- จัดการเก็บรายชื่อบ่อและสต็อกอาหารใน Session State ---
if 'ponds_list' not in st.session_state:
    st.session_state['ponds_list'] = ["บ่อที่ 01", "บ่อที่ 02", "บ่อที่ 03"]

if 'feed_types' not in st.session_state:
    st.session_state['feed_types'] = ["เบอร์ 1 (ผง/เม็ดเล็ก)", "เบอร์ 2", "เบอร์ 3", "เบอร์ 4", "เบอร์ 5"]

if 'feed_stock_log' not in st.session_state:
    st.session_state['feed_stock_log'] = pd.DataFrame(columns=[
        "วันที่", "ร้านที่ซื้อ", "เบอร์อาหาร", "จำนวนรับเข้า (กระสอบ/ถุง)", "มูลค่า (บาท)", "จ่ายออก (กระสอบ/ถุง)"
    ])

# 📌 แถบเลือกบ่อหลัก (Global Pond Selector) ด้านบน Sidebar
st.sidebar.markdown("### 🔍 เลือกบ่อที่ต้องการทำงาน")
selected_pond = st.sidebar.selectbox("เลือกบ่อ", st.session_state['ponds_list'])

st.sidebar.divider()

# เมนูด้านข้างเพิ่มเมนูสต็อกอาหาร
menu = st.sidebar.selectbox(
    "เลือกเมนูหลัก",
    [
        "📈 0. แดชบอร์ดภาพรวมทุกบ่อ (Dashboard)",
        "🏷️ 1. ตั้งชื่อและจัดการบ่อเลี้ยง",
        "📦 2. สต็อกอาหาร (Feed Stock)",
        "📋 3. บันทึกรายวัน (Daily Log)",
        "💧 4. ติดตามคุณภาพน้ำ (pH / DO)",
        "🦐 5. บันทึกการสุ่มยอและโต (Sampling)",
        "💰 6. บันทึกต้นทุนและวางแผนรอบ Crop",
        "📊 7. สรุปผลผลิตและกำไร (แยกรายบ่อ)"
    ]
)

# 📌 เพิ่มรูปภาพการ์ดและเครดิตด้านล่าง Sidebar (ขนาดใหญ่ขึ้นตามต้องการ)
st.sidebar.markdown("---")
st.sidebar.image("https://i.ibb.co/3yk5075/indy-card.jpg", width=250)
st.sidebar.markdown(
    "<p style='text-align: center; color: gray; font-size: 11px; margin-top: 5px;'>ออกแบบและพัฒนาโดย พ่ออินดี้</p>", 
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# เมนูที่ 0: แดชบอร์ดภาพรวมทุกบ่อ (Dashboard)
# ---------------------------------------------------------
if "0." in menu:
    st.header("📈 แดชบอร์ดภาพรวมฟาร์มกุ้งทั้งหมด (Multi-Pond Overview Dashboard)")
    st.info("💡 ข้อมูลด้านล่างนี้เป็น **[ตัวอย่างการแสดงผล]** ภาพรวมของทุกบ่อในฟาร์ม เพื่อใช้ประเมินสถานะเบื้องต้น")

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        st.metric(label="🏊‍♂️ จำนวนบ่อทั้งหมด", value="3 บ่อ", delta="ปกติ")
    with kpi2:
        st.metric(label="🦐 ผลผลิตคาดการณ์รวม", value="10,500 กก.", delta="+5% จากรอบก่อน")
    with kpi3:
        st.metric(label="💰 ต้นทุนรวมทุกบ่อ", value="564,000 บาท", delta="-2% ประหยัดขึ้น")
    with kpi4:
        st.metric(label="🎉 กำไรสุทธิคาดการณ์", value="1,326,000 บาท", delta="ROI ~235%")

    st.divider()

    st.subheader("📋 [ตัวอย่างการแสดงผล] ตารางสรุปสถานะรายบ่อเปรียบเทียบ")
    overview_df = pd.DataFrame({
        "ชื่อบ่อ": ["บ่อที่ 01", "บ่อที่ 02", "บ่อที่ 03"],
        "ชนิดกุ้ง": ["กุ้งขาวแวนนาไม", "กุ้งขาวแวนนาไม", "กุ้งก้ามกราม"],
        "อายุ (DOC)": [45, 30, 60],
        "อัตรารอดคาดการณ์ (%)": ["88%", "92%", "85%"],
        "ต้นทุนปัจจุบัน (บาท)": [188000, 160000, 216000],
        "สถานะบ่อ": ["ปกติ", "ปกติ", "เฝ้าระวัง pH"]
    })
    st.dataframe(overview_df, use_container_width=True)

# ---------------------------------------------------------
# เมนูที่ 1: ตั้งชื่อและจัดการบ่อเลี้ยง
# ---------------------------------------------------------
elif "1." in menu:
    st.header("🏷️ ระบบจัดการและตั้งชื่อบ่อเลี้ยงกุ้ง")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("➕ เพิ่มบ่อเลี้ยงใหม่")
        with st.form("add_pond_form"):
            new_pond_name = st.text_input("ชื่อบ่อ / รหัสบ่อ (เช่น บ่อที่ 04 หรือ Zone A-1)")
            add_submitted = st.form_submit_button("เพิ่มบ่อใหม่")
            if add_submitted and new_pond_name:
                if new_pond_name not in st.session_state['ponds_list']:
                    st.session_state['ponds_list'].append(new_pond_name)
                    st.success(f"เพิ่มบ่อ '{new_pond_name}' สำเร็จเรียบร้อย!")
                    st.rerun()
                else:
                    st.warning("มีชื่อบ่อนี้อยู่ในระบบแล้ว!")
                    
    with col2:
        st.subheader("📋 รายชื่อบ่อทั้งหมดในฟาร์มปัจจุบัน")
        pond_df = pd.DataFrame({"ลำดับ": range(1, len(st.session_state['ponds_list'])+1), "ชื่อบ่อ": st.session_state['ponds_list']})
        st.dataframe(pond_df, use_container_width=True)

# ---------------------------------------------------------
# เมนูที่ 2: สต็อกอาหาร (Feed Stock) - เพิ่มใหม่ตามสั่ง
# ---------------------------------------------------------
elif "2." in menu:
    st.header("📦 ระบบจัดการสต็อกอาหารกุ้ง")
    
    tab1, tab2, tab3 = st.tabs(["📥 รับเข้าอาหารและเพิ่มเบอร์", "📤 เบิกจ่ายอาหารไปใช้", "📊 สต็อกอาหารคงเหลือ"])
    
    with tab1:
        st.subheader("➕ เพิ่มเบอร์อาหารใหม่ (ถ้ามี)")
        with st.form("add_feed_type_form"):
            new_feed = st.text_input("ชื่อเบอร์อาหารใหม่ (เช่น เบอร์พิเศษ, เบอร์ 0)")
            add_feed_sub = st.form_submit_button("เพิ่มเบอร์อาหาร")
            if add_feed_sub and new_feed:
                if new_feed not in st.session_state['feed_types']:
                    st.session_state['feed_types'].append(new_feed)
                    st.success(f"เพิ่มเบอร์อาหาร '{new_feed}' เรียบร้อย!")
                    st.rerun()
                else:
                    st.warning("มีเบอร์อาหารนี้อยู่ในระบบแล้ว!")

        st.divider()
        st.subheader("📥 บันทึกรับเข้าอาหาร (ซื้ออาหารเข้าฟาร์ม)")
        with st.form("feed_in_form"):
            f_date = st.date_input("วันที่ซื้อ / รับเข้า", datetime.date.today())
            f_store = st.text_input("ร้านที่ซื้อ (เช่น ร้านสหกรณ์การเกษตร, เจริญโภคภัณฑ์)")
            f_type = st.selectbox("เลือกเบอร์อาหาร", st.session_state['feed_types'])
            f_qty = st.number_input("จำนวนที่รับเข้า (กระสอบ / ถุง)", min_value=0.0, format="%.2f", value=10.0)
            f_cost = st.number_input("ค่าอาหารรวมทั้งหมด (บาท)", min_value=0.0, format="%.2f", value=5000.0)
            
            f_submit = st.form_submit_button("บันทึกรับเข้าสต็อก")
            if f_submit:
                new_row = pd.DataFrame({
                    "วันที่": [str(f_date)],
                    "ร้านที่ซื้อ": [f_store],
                    "เบอร์อาหาร": [f_type],
                    "จำนวนรับเข้า (กระสอบ/ถุง)": [f_qty],
                    "มูลค่า (บาท)": [f_cost],
                    "จ่ายออก (กระสอบ/ถุง)": [0.0]
                })
                st.session_state['feed_stock_log'] = pd.concat([st.session_state['feed_stock_log'], new_row], ignore_index=True)
                st.success(f"บันทึกรับเข้า {f_type} จำนวน {f_qty} ถุง จากร้าน {f_store} เรียบร้อย!")

    with tab2:
        st.subheader("📤 บันทึกการเบิกจ่ายอาหาร (นำไปให้กุ้งกิน)")
        if st.session_state['feed_stock_log'].empty:
            st.info("ยังไม่มีประวัติการรับเข้าอาหาร กรุณาบันทึกรับเข้าก่อน")
        else:
            with st.form("feed_out_form"):
                out_date = st.date_input("วันที่จ่ายออก", datetime.date.today())
                out_pond = st.selectbox("เลือกบ่อที่นำไปใช้", st.session_state['ponds_list'])
                out_type = st.selectbox("เลือกเบอร์อาหารที่ต้องการเบิก", st.session_state['feed_types'])
                out_qty = st.number_input("จำนวนที่จ่ายออก (กระสอบ / ถุง)", min_value=0.0, format="%.2f", value=1.0)
                
                out_submit = st.form_submit_button("บันทึกจ่ายออกอาหาร")
                if out_submit:
                    new_out_row = pd.DataFrame({
                        "วันที่": [str(out_date)],
                        "ร้านที่ซื้อ": [f"เบิกใช้ให้ {out_pond}"],
                        "เบอร์อาหาร": [out_type],
                        "จำนวนรับเข้า (กระสอบ/ถุง)": [0.0],
                        "มูลค่า (บาท)": [0.0],
                        "จ่ายออก (กระสอบ/ถุง)": [out_qty]
                    })
                    st.session_state['feed_stock_log'] = pd.concat([st.session_state['feed_stock_log'], new_out_row], ignore_index=True)
                    st.success(f"บันทึกเบิกจ่าย {out_type} จำนวน {out_qty} ถุง ให้ {out_pond} สำเร็จ!")

    with tab3:
        st.subheader("📊 ตารางสรุปสต็อกอาหารคงเหลือแต่ละเบอร์")
        if not st.session_state['feed_stock_log'].empty:
            df = st.session_state['feed_stock_log']
            # คำนวณหายอดคงเหลือแยกตามเบอร์อาหาร
            summary_stock = df.groupby("เบอร์อาหาร")[["จำนวนรับเข้า (กระสอบ/ถุง)", "จ่ายออก (กระสอบ/ถุง)"]].sum()
            summary_stock["คงเหลือ (กระสอบ/ถุง)"] = summary_stock["จำนวนรับเข้า (กระสอบ/ถุง)"] - summary_stock["จ่ายออก (กระสอบ/ถุง)"]
            st.dataframe(summary_stock.reset_index(), use_container_width=True)
            
            st.divider()
            st.subheader("📋 ประวัติการเคลื่อนไหวสต็อกอาหารทั้งหมด")
            st.dataframe(df, use_container_width=True)
        else:
            st.info("ยังไม่มีข้อมูลในระบบสต็อกอาหาร")

# ---------------------------------------------------------
# เมนูที่ 3: บันทึกรายวัน (Daily Log)
# ---------------------------------------------------------
elif "3." in menu:
    st.header(f"📋 บันทึกข้อมูลการเลี้ยงกุ้งรายวัน — [ กำลังจัดการ: {selected_pond} ]")
    
    with st.form("daily_log_form"):
        st.subheader("📝 กรอกข้อมูลประจำวัน")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            log_date = st.date_input("วันที่", datetime.date.today())
            doc = st.number_input("อายุการเลี้ยง (DOC)", min_value=0, value=1)
            feed_no = st.selectbox("เบอร์อาหาร", st.session_state['feed_types'])
            feed_amt = st.number_input("ปริมาณอาหารที่ให้ (กก.)", min_value=0.0, format="%.2f")
            
        with col2:
            dead_shrimp = st.number_input("จำนวนกุ้งตาย (ตัว)", min_value=0, value=0)
            aerator_hrs = st.number_input("ชั่วโมงเปิดเครื่องตีน้ำ", min_value=0.0, value=24.0, format="%.1f")
            chemical = st.text_input("สารเคมี / จุลินทรีย์ที่ใส่")
            
        with col3:
            behavior = st.text_area("พฤติกรรม / ลักษณะกุ้ง")
            note = st.text_area("หมายเหตุ / การเปลี่ยนน้ำ")
            
        submitted = st.form_submit_button(f"💾 บันทึกข้อมูลสำหรับ {selected_pond}")
        if submitted:
            st.success(f"บันทึกข้อมูลของ {selected_pond} วันที่ {log_date} (DOC {doc}) สำเร็จเรียบร้อย!")

    st.divider()
    st.subheader(f"📊 [ตัวอย่างการแสดงผล] ตารางประวัติบันทึกรายวันของ {selected_pond}")
    sample_daily = pd.DataFrame({
        "บ่อ": [selected_pond, selected_pond],
        "วันที่": ["2026-06-01", "2026-06-02"],
        "DOC": [1, 2],
        "เบอร์อาหาร": [st.session_state['feed_types'][0], st.session_state['feed_types'][0]],
        "อาหาร (กก.)": [10.5, 12.0],
        "กุ้งตาย (ตัว)": [2, 1]
    })
    st.dataframe(sample_daily, use_container_width=True)

# ---------------------------------------------------------
# เมนูที่ 4: ติดตามคุณภาพน้ำ (pH / DO)
# ---------------------------------------------------------
elif "4." in menu:
    st.header(f"💧 บันทึกและวิเคราะห์คุณภาพน้ำ — [ กำลังจัดการ: {selected_pond} ]")
    
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
            
        w_submitted = st.form_submit_button(f"💾 บันทึกค่าคุณภาพน้ำสำหรับ {selected_pond}")
        if w_submitted:
            st.success(f"บันทึกข้อมูลคุณภาพน้ำของ {selected_pond} สำเร็จ!")

    st.divider()
    st.subheader(f"📈 [ตัวอย่างการแสดงผล] กราฟแสดงแนวโน้มคุณภาพน้ำย้อนหลังของ {selected_pond}")
    water_data = pd.DataFrame({
        "DOC": [1, 2, 3, 4, 5],
        "pH เช้า": [7.5, 7.6, 7.4, 7.5, 7.6],
        "pH เย็น": [8.0, 8.2, 7.9, 8.1, 8.0]
    }).set_index("DOC")
    st.line_chart(water_data)

# ---------------------------------------------------------
# เมนูที่ 5: บันทึกการสุ่มยอและโต (Sampling)
# ---------------------------------------------------------
elif "5." in menu:
    st.header(f"🦐 บันทึกผลการสุ่มยอและน้ำหนัก (ABW) — [ กำลังจัดการ: {selected_pond} ]")
    
    with st.form("sample_form"):
        col1, col2 = st.columns(2)
        with col1:
            s_doc = st.number_input("อายุการเลี้ยง (DOC) ที่สุ่ม", min_value=1, value=30)
            abw = st.number_input("น้ำหนักเฉลี่ยต่อตัว (กรัม - ABW)", min_value=0.0, format="%.2f")
        with col2:
            check_result = st.text_input("ผลการเช็กยอ / การกินอาหาร")
            est_survival = st.slider("ประเมินอัตรารอด (%) คาดการณ์", 0, 100, 85)
            
        s_submitted = st.form_submit_button(f"💾 บันทึกผลสุ่มยอสำหรับ {selected_pond}")
        if s_submitted:
            st.success(f"บันทึกสำเร็จสำหรับ {selected_pond} (DOC {s_doc} | ABW: {abw} กรัม)")

    st.divider()
    st.subheader(f"📊 [ตัวอย่างการแสดงผล] ตารางประวัติการเจริญเติบโตของ {selected_pond}")
    sample_growth = pd.DataFrame({
        "DOC": [30, 45, 60],
        "น้ำหนักเฉลี่ย (ABW g.)": [3.5, 7.2, 12.5],
        "อัตรารอด (%)": [90, 88, 85]
    })
    st.dataframe(sample_growth, use_container_width=True)

# ---------------------------------------------------------
# เมนูที่ 6: บันทึกต้นทุนและวางแผนรอบ Crop (Interactive)
# ---------------------------------------------------------
elif "6." in menu:
    st.header(f"💰 บันทึกต้นทุนและวางแผนรอบการเลี้ยง — [ กำลังจัดการ: {selected_pond} ]")
    
    with st.expander("📅 กำหนดข้อมูลตั้งต้นรอบการเลี้ยง (Crop Setup & AI Estimation)", expanded=True):
        with st.form("crop_setup_form"):
            col_s1, col_s2, col_s3 = st.columns(3)
            with col_s1:
                crop_name = st.selectbox("รอบการเลี้ยง (Crop)", ["Crop 1/2026", "Crop 2/2026"])
            with col_s2:
                shrimp_type = st.selectbox("🦐 ชนิดกุ้ง", ["กุ้งขาวแวนนาไม", "กุ้งก้ามกราม"])
            with col_s3:
                start_date = st.date_input("📅 วันที่ลงเลี้ยง (ปล่อยลูกกุ้ง)", datetime.date.today())
                
            if shrimp_type == "กุ้งก้ามกราม":
                days_to_grow = 180
            else:
                days_to_grow = 120
                
            estimated_harvest_date = start_date + datetime.timedelta(days=days_to_grow)
            
            st.info(f"🤖 **AI แนะนำ (ประมาณการ):** สำหรับ **{shrimp_type}** จะใช้ระยะเวลาเลี้ยงประมาณ **{days_to_grow} วัน** | วันที่คาดว่าจะจับผลผลิต: **{estimated_harvest_date.strftime('%d/%m/%Y')}**")
            
            setup_submitted = st.form_submit_button("💾 บันทึกข้อมูลตั้งต้นรอบ Crop")
            if setup_submitted:
                st.success(f"บันทึกตั้งค่ารอบ {crop_name} ({shrimp_type}) สำเร็จ!")

    st.divider()
    st.subheader("💸 บันทึกรายการค่าใช้จ่ายตามหมวดหมู่ต้นทุน")
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
            remark = st.text_input("หมายเหตุเพิ่มเติม")
            
        cost_submitted = st.form_submit_button(f"➕ เพิ่มรายการต้นทุนเข้า {selected_pond}")
        if cost_submitted:
            st.success(f"บันทึกรายการ '{item_detail}' ของ {selected_pond} จำนวน {amount:,.2f} บาท สำเร็จ!")

    st.divider()
    st.subheader(f"📈 [ตัวอย่างการแสดงผล] สรุปต้นทุนรวมแยกตามหมวดหมู่ของ {selected_pond}")
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
    st.metric(label=f"💸 ต้นทุนรวมทั้งสิ้นของ {selected_pond}", value=f"{total_cost:,.2f} บาท")

# ---------------------------------------------------------
# เมนูที่ 7: สรุปผลผลิตและกำไร (แยกรายบ่อ)
# ---------------------------------------------------------
elif "7." in menu:
    st.header(f"📊 สรุปผลผลิตและกำไรสุทธิ — [ กำลังวิเคราะห์: {selected_pond} ]")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="📦 ผลผลิตรวมที่จับได้", value="3,500 กก.")
    with col2:
        st.metric(label="💰 รายรับจากการขาย", value="630,000 บาท")
    with col3:
        st.metric(label="📉 ต้นทุนรวมบ่อนี้", value="188,000 บาท")
        
    st.divider()
    net_profit = 630000 - 188000
    st.success(f"### 🎉 กำไรสุทธิของ {selected_pond}: {net_profit:,.2f} บาท")
    
    st.subheader(f"📋 [ตัวอย่างการแสดงผล] รายละเอียดการจับขายประจำ {selected_pond}")
    harvest_df = pd.DataFrame({
        "หัวข้อ": ["รอบการเลี้ยง", "ชนิดกุ้ง", "น้ำหนักเฉลี่ยตอนจับ", "เปอร์เซ็นต์รอดจริง", "ราคาขายเฉลี่ย"],
        "รายละเอียด": ["Crop 1/2026", "กุ้งขาวแวนนาไม", "14.2 กรัม", "84.5%", "180 บาท/กก."]
    })
    st.table(harvest_df)
