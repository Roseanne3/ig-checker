import streamlit as st
import json

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="IG Unfollow Tracker", page_icon="📸", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    </style>
    """, unsafe_allow_html=True)

st.title("🕵️‍♂️ เครื่องมือเช็คยอด Follower Instagram")
st.subheader("เปรียบเทียบข้อมูลได้ง่ายๆ โดยไม่ต้องใช้ Password")

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

col1, col2 = st.columns(2)
with col1:
    file_following = st.file_uploader("📂 อัปโหลดไฟล์ following.json", type="json")
with col2:
    file_followers = st.file_uploader("📂 อัปโหลดไฟล์ followers.json", type="json")

# ฟังก์ชันสกัดชื่อแบบใหม่ (ทะลวงทุกโครงสร้างของ Instagram!)
def extract_users(data):
    users = set()
    items = []
    
    # ไม่ว่าไฟล์จะมาเป็น List หรือ Dictionary เราจะดึงข้อมูลมาให้หมด
    if isinstance(data, list):
        items = data
    elif isinstance(data, dict):
        for val in data.values():
            if isinstance(val, list):
                items.extend(val)
                
    # ค้นหา Username จากโครงสร้างมาตรฐาน
    for item in items:
        try:
            username = item['string_list_data'][0]['value']
            users.add(username)
        except:
            pass
            
    return users

if file_following and file_followers:
    try:
        data_ing = json.load(file_following)
        data_ers = json.load(file_followers)

        # ใช้ฟังก์ชันครอบจักรวาลดึงข้อมูล
        following = extract_users(data_ing)
        followers = extract_users(data_ers)

        not_back = sorted(list(following - followers))
        i_not_back = sorted(list(followers - following))

        st.divider()
        m1, m2, m3 = st.columns(3)
        # ตรวจสอบยอดให้แน่ใจว่าไม่ได้เป็น 0
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
