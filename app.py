# ---------------------------------------------------------
# เมนูที่ 4: บันทึกต้นทุนและวางแผนรอบ Crop (แบบ Interactive)
# ---------------------------------------------------------
elif menu == "💰 4. บันทึกต้นทุนและวางแผนรอบ Crop":
    st.header(f"💰 บันทึกต้นทุนและวางแผนรอบการเลี้ยง — [ กำลังจัดการ: {selected_pond} ]")
    
    with st.expander("📅 กำหนดข้อมูลตั้งต้นรอบการเลี้ยง (Crop Setup & AI Estimation)", expanded=True):
        with st.form("crop_setup_form"):
            col_s1, col_s2, col_s3 = st.columns(3)
            with col_s1:
                crop_name = st.selectbox("รอบการเลี้ยง (Crop)", ["Crop 1/2026", "Crop 2/2026"])
            with col_s2:
                # เลือกชนิดกุ้ง
                shrimp_type = st.selectbox("🦐 ชนิดกุ้ง", ["กุ้งขาวแวนนาไม", "กุ้งก้ามกราม"])
            with col_s3:
                start_date = st.date_input("📅 วันที่ลงเลี้ยง (ปล่อยลูกกุ้ง)", datetime.date.today())
                
            # 🔄 ทำให้อีเวนต์ Interactive ตามชนิดกุ้งที่เลือกจริง
            if shrimp_type == "กุ้งก้ามกราม":
                days_to_grow = 180
            else:
                days_to_grow = 120
                
            estimated_harvest_date = start_date + datetime.timedelta(days=days_to_grow)
            
            # แสดงข้อความ AI แบบเปลี่ยนตามชนิดกุ้งที่เลือกทันที
            st.info(f"🤖 **AI แนะนำ (ประมาณการ):** สำหรับ **{shrimp_type}** จะใช้ระยะเวลาเลี้ยงประมาณ **{days_to_grow} วัน** | วันที่คาดว่าจะจับผลผลิต: **{estimated_harvest_date.strftime('%d/%m/%Y')}**")
            
            setup_submitted = st.form_submit_button("บันทึกข้อมูลตั้งต้นรอบ Crop")
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
            
        cost_submitted = st.form_submit_button(f"เพิ่มรายการต้นทุนเข้า {selected_pond}")
        if cost_submitted:
            st.success(f"บันทึกรายการ '{item_detail}' ของ {selected_pond} จำนวน {amount:,.2f} บาท สำเร็จ!")

    st.divider()
    st.subheader(f"📈 สรุปต้นทุนรวมแยกตามหมวดหมู่ของ {selected_pond}")
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
