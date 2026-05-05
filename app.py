import streamlit as st
import json

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Multi-Check Analytics", page_icon="📊", layout="wide")

# 2. ปรับแต่ง CSS (Glassmorphism + แถบเมนู)
st.markdown("""
    <style>
    [data-testid="stMetric"] { background-color: rgba(128, 128, 128, 0.1); padding: 15px; border-radius: 15px; }
    .platform-card {
        padding: 30px; border-radius: 20px; border: 2px solid rgba(128, 128, 128, 0.2);
        text-align: center; cursor: pointer; transition: 0.3s; background-color: rgba(128, 128, 128, 0.05);
    }
    .platform-card:hover { transform: translateY(-10px); border-color: #E1306C; background-color: rgba(225, 48, 108, 0.05); }
    .user-card { padding: 12px; border-radius: 12px; background-color: rgba(128, 128, 128, 0.08); margin-bottom: 10px; border-left: 6px solid #E1306C; }
    .back-btn { margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 3. จัดการสถานะการเลือกหน้า (Session State)
if 'page' not in st.session_state:
    st.session_state.page = 'home'

def go_to_page(page_name):
    st.session_state.page = page_name
    st.rerun()

# --- ฟังก์ชันสกัดชื่อ (ใช้ได้กับหลายโครงสร้าง) ---
def extract_users(data):
    users = set()
    if isinstance(data, dict):
        for key in data:
            if isinstance(data[key], list):
                for item in data[key]:
                    if 'title' in item: users.add(item['title'])
                    try: users.add(item['string_list_data'][0]['value'])
                    except: pass
    elif isinstance(data, list):
        for item in data:
            try: users.add(item['string_list_data'][0]['value'])
            except: pass
            if 'title' in item: users.add(item['title'])
    users.discard("")
    return users

# --- หน้าแรก (HOME) ---
if st.session_state.page == 'home':
    st.title("🚀 Social Analytics Hub")
    st.subheader("เลือกแพลตฟอร์มที่ต้องการตรวจสอบ")
    st.write("เลือกหนึ่งในบริการด้านล่างเพื่อเริ่มวิเคราะห์ข้อมูล")

    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="platform-card">', unsafe_allow_html=True)
        st.header("📸 Instagram")
        st.write("เช็คคนไม่ฟอลกลับ (Unfollow Tracker)")
        if st.button("เข้าใช้งาน Instagram", key="ig_btn"):
            go_to_page('instagram')
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="platform-card">', unsafe_allow_html=True)
        st.header("🎵 TikTok")
        st.write("เช็คสถานะการติดตาม (เร็วๆ นี้)")
        if st.button("เข้าใช้งาน TikTok", key="tt_btn"):
            go_to_page('tiktok')
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="platform-card">', unsafe_allow_html=True)
        st.header("🐦 Twitter / X")
        st.write("วิเคราะห์ผู้ติดตามของคุณ")
        st.button("เร็วๆ นี้", disabled=True)
        st.markdown('</div>', unsafe_allow_html=True)

# --- หน้า Instagram ---
elif st.session_state.page == 'instagram':
    if st.button("⬅️ กลับหน้าหลัก", key="back_ig"):
        go_to_page('home')
    
    st.title("📸 Instagram Unfollow Tracker")
    up_col1, up_col2 = st.columns(2)
    with up_col1:
        file_ing = st.file_uploader("อัปโหลด following.json", type="json")
    with up_col2:
        file_ers = st.file_uploader("อัปโหลด followers_1.json", type="json")

    if file_ing and file_ers:
        data_ing = json.load(file_ing)
        data_ers = json.load(file_ers)
        ing = extract_users(data_ing)
        ers = extract_users(data_ers)
        not_back = sorted(list(ing - ers))
        
        st.divider()
        st.metric("ไม่ฟอลกลับ", len(not_back))
        cols = st.columns(3)
        for idx, user in enumerate(not_back):
            with cols[idx % 3]:
                st.markdown(f'<div class="user-card"><b><a href="https://www.instagram.com/{user}/" target="_blank" style="color: #E1306C; text-decoration: none;">@{user}</a></b></div>', unsafe_allow_html=True)

# --- หน้า TikTok (ตัวอย่าง) ---
elif st.session_state.page == 'tiktok':
    if st.button("⬅️ กลับหน้าหลัก", key="back_tt"):
        go_to_page('home')
    
    st.title("🎵 TikTok Analytics")
    st.info("กำลังพัฒนา: สำหรับ TikTok เพื่อนต้องโหลดไฟล์ข้อมูล (Data Request) มาจากแอป TikTok เหมือนกันครับ เดี๋ยวผมจะอัปเดตวิธีแกะไฟล์ของ TikTok ให้เร็วๆ นี้!")
        
