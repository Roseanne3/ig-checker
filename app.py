import streamlit as st
import json

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="IG Unfollow Tracker", page_icon="📸", layout="wide")

# ตกแต่ง CSS (แก้จุดที่ผิดแล้วครับ)
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    </style>
    """, unsafe_allow_html=True)

st.title("🕵️‍♂️ เครื่องมือเช็คยอด Follower Instagram")
st.subheader("เปรียบเทียบข้อมูลได้ง่ายๆ โดยไม่ต้องใช้ Password")

# สร้าง Sidebar
with st.sidebar:
    st.header("📌 วิธีการใช้งาน")
    st.markdown("""
    1. เข้าแอป IG > Your Activity
    2. เลือก **Download Your Information**
    3. เลือกเฉพาะไฟล์ **Followers and Following**
    4. เลือก Format เป็น **JSON**
    5. อัปโหลดไฟล์ `following.json` และ `followers.json` ที่นี่
    """)
    st.divider()
    st.write("สร้างโดย: เพื่อน AI ของคุณ 🤖")

# ส่วนอัปโหลดไฟล์
col1, col2 = st.columns(2)
with col1:
    file_following = st.file_uploader("📂 อัปโหลดไฟล์ following.json", type="json")
with col2:
    file_followers = st.file_uploader("📂 อัปโหลดไฟล์ followers.json", type="json")

# ฟังก์ชันจัดการแกะข้อมูล
def extract_usernames(data, key_name):
    try:
        if key_name in data:
            return {item['string_list_data'][0]['value'] for item in data[key_name]}
        return set()
    except:
        return set()

if file_following and file_followers:
    try:
        data_ing = json.load(file_following)
        data_ers = json.load(file_followers)

        # แกะข้อมูล (รองรับโครงสร้าง JSON ของ Instagram)
        # ปกติ following จะอยู่ใน key 'relationships_following'
        # ส่วน followers จะอยู่ใน key 'relationships_followers' หรือเป็น List โดยตรง
        
        following = extract_usernames(data_ing, 'relationships_following')
        
        # สำหรับ followers บางครั้ง IG ให้มาเป็น List เลย
        if isinstance(data_ers, list):
            followers = {item['string_list_data'][0]['value'] for item in data_ers}
        else:
            followers = extract_usernames(data_ers, 'relationships_followers')

        # คำนวณ
        not_back = sorted(list(following - followers))
        i_not_back = sorted(list(followers - following))

        # แสดงผล
        st.divider()
        m1, m2, m3 = st.columns(3)
        m1.metric("Following (เราตามเขา)", len(following))
        m2.metric("Followers (เขาตามเรา)", len(followers))
        m3.metric("ไม่ฟอลกลับ", len(not_back))

        res_col1, res_col2 = st.columns(2)
        
        with res_col1:
            st.error(f"❌ เขาไม่ฟอลเรากลับ ({len(not_back)} คน)")
            for user in not_back:
                st.markdown(f"👉 [{user}](https://instagram.com/{user})")
        
        with res_col2:
            st.warning(f"⚠️ เราไม่ได้ฟอลเขากลับ ({len(i_not_back)} คน)")
            for user in i_not_back:
                st.markdown(f"✅ [{user}](https://instagram.com/{user})")

    except Exception as e:
        st.error(f"เกิดข้อผิดพลาด: {e}")
else:
    st.info("รออัปโหลดไฟล์เพื่อเริ่มประมวลผล...")
