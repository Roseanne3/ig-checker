import streamlit as st
import json

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="IG Insight Pro", page_icon="📸", layout="wide")

# 2. ปรับ CSS ให้เป็น Glassmorphism (สวยทั้ง Light/Dark Mode)
st.markdown("""
    <style>
    /* ปรับแต่งกล่องตัวเลข Metric */
    [data-testid="stMetric"] {
        background-color: rgba(128, 128, 128, 0.1);
        padding: 15px;
        border-radius: 15px;
        border: 1px solid rgba(128, 128, 128, 0.2);
    }
    /* ปรับแต่งการ์ดรายชื่อ */
    .user-card { 
        padding: 12px; 
        border-radius: 12px; 
        background-color: rgba(128, 128, 128, 0.08); 
        margin-bottom: 10px; 
        border-left: 6px solid #E1306C;
        border: 1px solid rgba(128, 128, 128, 0.1);
        backdrop-filter: blur(10px);
    }
    /* ปรับสีลิงก์ให้เด่นขึ้น */
    .user-link {
        text-decoration: none;
        font-weight: bold;
        color: #E1306C !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📸 IG Follower Analytics Pro")
st.write("ระบบวิเคราะห์ข้อมูลส่วนตัว ปลอดภัย ไม่ผ่านเซิร์ฟเวอร์กลาง")

# 3. ส่วนอัปโหลดไฟล์
st.markdown("### 📥 ขั้นตอนแรก: อัปโหลดไฟล์ข้อมูล")
up_col1, up_col2 = st.columns(2)
with up_col1:
    file_ing = st.file_uploader("เลือกไฟล์ following.json", type="json")
with up_col2:
    file_ers = st.file_uploader("เลือกไฟล์ followers_1.json", type="json")

def extract_users(data):
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

if file_ing and file_ers:
    try:
        data_ing = json.load(file_ing)
        data_ers = json.load(file_ers)
        following = extract_users(data_ing)
        followers = extract_users(data_ers)
        
        not_back = sorted(list(following - followers))
        i_not_back = sorted(list(followers - following))

        st.divider()
        m1, m2, m3 = st.columns(3)
        m1.metric("Following", len(following))
        m2.metric("Followers", len(followers))
        m3.metric("ไม่ฟอลกลับ", len(not_back))

        tab1, tab2 = st.tabs([f"❌ เขาไม่ฟอลเรา ({len(not_back)})", f"⚠️ เราไม่ฟอลเขา ({len(i_not_back)})"])

        with tab1:
            if not_back:
                cols = st.columns(3)
                for idx, user in enumerate(not_back):
                    with cols[idx % 3]:
                        st.markdown(f'''
                            <div class="user-card">
                                <small style="opacity: 0.7;">Username</small><br>
                                <a class="user-link" href="https://www.instagram.com/{user}/" target="_blank">@{user}</a>
                            </div>
                        ''', unsafe_allow_html=True)
            else:
                st.success("ไม่มีคนที่ไม่ฟอลกลับเลย! สุดยอด")

        with tab2:
            if i_not_back:
                cols = st.columns(3)
                for idx, user in enumerate(i_not_back):
                    with cols[idx % 3]:
                        st.markdown(f'''
                            <div class="user-card" style="border-left-color: #28a745;">
                                <small style="opacity: 0.7;">Username</small><br>
                                <a class="user-link" href="https://www.instagram.com/{user}/" target="_blank" style="color: #28a745 !important;">@{user}</a>
                            </div>
                        ''', unsafe_allow_html=True)
            else:
                st.write("คุณฟอลกลับทุกคนแล้ว")

    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.info("อัปโหลดไฟล์ทั้งสองข้างบนเพื่อเริ่มใช้งาน")
                    
