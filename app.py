import streamlit as st
import json

# 1. ตั้งค่าหน้าเว็บให้ดูทันสมัย
st.set_page_config(page_title="IG Insight Pro", page_icon="📸", layout="wide")

# 2. ใส่ CSS ตกแต่งให้เหมือนแอปมือถือหรูๆ
st.markdown("""
    <style>
    .main { background-color: #fafafa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
    .user-card { 
        padding: 12px; border-radius: 12px; background-color: white; 
        margin-bottom: 10px; border-left: 6px solid #E1306C;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .stButton>button { width: 100%; border-radius: 10px; background-color: #E1306C; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("📸 IG Follower Analytics Pro")
st.write("เช็คคนไม่ฟอลกลับได้แม่นยำ ปลอดภัย ไม่ใช้รหัสผ่าน")

# 3. ส่วนอัปโหลดไฟล์ (เอามาไว้ตรงกลางให้เห็นชัดๆ!)
st.info("📌 ขั้นตอนแรก: อัปโหลดไฟล์ .json ของคุณที่นี่")
up_col1, up_col2 = st.columns(2)
with up_col1:
    file_ing = st.file_uploader("📥 เลือกไฟล์ following.json", type="json")
with up_col2:
    file_ers = st.file_uploader("📥 เลือกไฟล์ followers_1.json", type="json")

# 4. ฟังก์ชันขุดข้อมูล (ตัวเก่งที่เช็คทั้ง title และ value)
def extract_instagram_users(data):
    users = set()
    if isinstance(data, dict):
        for key in data:
            if isinstance(data[key], list):
                for item in data[key]:
                    if 'title' in item and item['title']: users.add(item['title'])
                    try:
                        val = item['string_list_data'][0]['value']
                        if val: users.add(val)
                    except: pass
    elif isinstance(data, list):
        for item in data:
            try:
                val = item['string_list_data'][0]['value']
                if val: users.add(val)
            except: pass
            if 'title' in item and item['title']: users.add(item['title'])
    users.discard("")
    return users

# 5. ส่วนประมวลผลและแสดงผล
if file_ing and file_ers:
    try:
        with st.spinner('กำลังวิเคราะห์ข้อมูล...'):
            data_ing = json.load(file_ing)
            data_ers = json.load(file_ers)
            following = extract_instagram_users(data_ing)
            followers = extract_instagram_users(data_ers)
            
            not_back = sorted(list(following - followers))
            i_not_back = sorted(list(followers - following))

        # แสดงตัวเลขสรุปสวยๆ
        st.divider()
        m1, m2, m3 = st.columns(3)
        m1.metric("Following (ตามเขา)", len(following))
        m2.metric("Followers (เขาตาม)", len(followers))
        m3.metric("ใจร้าย (ไม่ฟอลกลับ)", len(not_back))

        st.markdown("### 🔍 ผลการวิเคราะห์")
        tab1, tab2 = st.tabs([f"❌ เขาไม่ฟอลเรา ({len(not_back)})", f"⚠️ เราไม่ฟอลเขา ({len(i_not_back)})"])

        with tab1:
            if not_back:
                cols = st.columns(3)
                for idx, user in enumerate(not_back):
                    with cols[idx % 3]:
                        st.markdown(f'<div class="user-card"><small>Username</small><br><b><a href="https://www.instagram.com/{user}/" target="_blank" style="color: #E1306C; text-decoration: none;">@{user}</a></b></div>', unsafe_allow_html=True)
            else:
                st.success("ว้าว! ทุกคนที่คุณติดตาม เขาก็ติดตามคุณกลับหมดเลย")

        with tab2:
            if i_not_back:
                cols = st.columns(3)
                for idx, user in enumerate(i_not_back):
                    with cols[idx % 3]:
                        st.markdown(f'<div class="user-card" style="border-left-color: #28a745;"><small>Username</small><br><b><a href="https://www.instagram.com/{user}/" target="_blank" style="color: #28a745; text-decoration: none;">@{user}</a></b></div>', unsafe_allow_html=True)
            else:
                st.write("ไม่มีคนตกค้างที่คุณยังไม่ได้ฟอลกลับ")

    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการอ่านไฟล์: {e}")
else:
    # หน้าต้อนรับตอนยังไม่ได้อัปโหลด
    st.divider()
    st.markdown("""
    ### 💡 วิธีใช้งานเบื้องต้น
    1. อัปโหลดไฟล์ที่ได้จาก Instagram ทั้งสองไฟล์ข้างบน
    2. ระบบจะทำการเปรียบเทียบชื่อให้โดยอัตโนมัติ
    3. รายชื่อจะปรากฏขึ้นมาพร้อมลิงก์ที่คลิกไปหน้าโปรไฟล์ได้ทันที
    """)
    st.warning("หมายเหตุ: ข้อมูลของคุณจะไม่ถูกเก็บไว้ในเซิร์ฟเวอร์ จะถูกประมวลผลสดๆ บนหน้าเว็บนี้เท่านั้น")
                    
