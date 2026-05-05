import streamlit as st
import json

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Social Analytics Pro", page_icon="📊", layout="wide")

# 2. CSS ตกแต่ง (เน้นตัวหนังสืออ่านง่ายในโหมดมืด)
st.markdown("""
    <style>
    .stButton>button { width: 100%; height: 60px; font-size: 18px; border-radius: 15px; margin-bottom: 10px; }
    .user-card { 
        padding: 15px; border-radius: 12px; background-color: rgba(128, 128, 128, 0.1); 
        margin-bottom: 10px; backdrop-filter: blur(10px); border-left: 6px solid #fe2c55;
    }
    [data-testid="stMetric"] { 
        background-color: rgba(128, 128, 128, 0.05); 
        border-radius: 15px; padding: 10px; border: 1px solid rgba(128, 128, 128, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

if 'page' not in st.session_state:
    st.session_state.page = 'home'

def go_to_page(page_name):
    st.session_state.page = page_name
    st.rerun()

# --- ฟังก์ชันดึงข้อมูล (IG) ---
def extract_ig_users(data):
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

# --- ฟังก์ชันดึงข้อมูล (TikTok) ---
def extract_tiktok_users(data, list_key):
    users = set()
    if isinstance(data, dict) and list_key in data:
        for item in data[list_key]:
            if 'UserName' in item: users.add(item['UserName'])
    return users

# --- หน้าแรก ---
if st.session_state.page == 'home':
    st.title("🚀 Social Analytics Hub")
    st.write("เลือกแพลตฟอร์มที่ต้องการตรวจสอบ")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📸 Instagram Tracker"): go_to_page('instagram')
    with col2:
        if st.button("🎵 TikTok Tracker"): go_to_page('tiktok')

# --- หน้า Instagram ---
elif st.session_state.page == 'instagram':
    if st.button("⬅️ กลับหน้าหลัก"): go_to_page('home')
    st.header("📸 Instagram Unfollow Tracker")
    f_ing = st.file_uploader("📥 ใส่ไฟล์ following.json", type="json", key="ig_ing")
    f_ers = st.file_uploader("📥 ใส่ไฟล์ followers_1.json", type="json", key="ig_ers")

    if f_ing and f_ers:
        ing = extract_ig_users(json.load(f_ing))
        ers = extract_ig_users(json.load(f_ers))
        not_back = sorted(list(ing - ers))
        i_not_back = sorted(list(ers - ing))
        
        st.divider()
        # แก้ตรงนี้! เพิ่มเป็น 4 คอลัมน์ให้ครบ
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Following", len(ing))
        m2.metric("Followers", len(ers))
        m3.metric("เขาไม่ฟอลเรา", len(not_back))
        m4.metric("เราไม่ฟอลเขา", len(i_not_back)) # <-- อันนี้แหละที่หายไป!

        tab1, tab2 = st.tabs([f"❌ เขาไม่ฟอลเรา ({len(not_back)})", f"⚠️ เราไม่ฟอลเขา ({len(i_not_back)})"])
        with tab1:
            for user in not_back:
                st.markdown(f'<div class="user-card" style="border-left-color: #E1306C;"><b><a href="https://www.instagram.com/{user}/" target="_blank" style="color: #E1306C; text-decoration: none;">@{user}</a></b></div>', unsafe_allow_html=True)
        with tab2:
            for user in i_not_back:
                st.markdown(f'<div class="user-card" style="border-left-color: #28a745;"><b><a href="https://www.instagram.com/{user}/" target="_blank" style="color: #28a745; text-decoration: none;">@{user}</a></b></div>', unsafe_allow_html=True)

# --- หน้า TikTok ---
elif st.session_state.page == 'tiktok':
    if st.button("⬅️ กลับหน้าหลัก"): go_to_page('home')
    st.header("🎵 TikTok Unfollow Tracker")
    f_ing = st.file_uploader("📥 ใส่ไฟล์ Following List.json", type="json", key="tt_ing")
    f_ers = st.file_uploader("📥 ใส่ไฟล์ Follower List.json", type="json", key="tt_ers")

    if f_ing and f_ers:
        ing = extract_tiktok_users(json.load(f_ing), "Following List")
        ers = extract_tiktok_users(json.load(f_ers), "Follower List")
        not_back = sorted(list(ing - ers))
        i_not_back = sorted(list(ers - ing))
        
        st.divider()
        # TikTok ก็เพิ่มให้ครบ 4 ช่องเหมือนกัน
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Following", len(ing))
        m2.metric("Followers", len(ers))
        m3.metric("เขาไม่ฟอลเรา", len(not_back))
        m4.metric("เราไม่ฟอลเขา", len(i_not_back))

        tab1, tab2 = st.tabs([f"❌ เขาไม่ฟอลเรา ({len(not_back)})", f"⚠️ เราไม่ฟอลเขา ({len(i_not_back)})"])
        with tab1:
            for user in not_back:
                st.markdown(f'<div class="user-card" style="border-left-color: #fe2c55;"><b><a href="https://www.tiktok.com/@{user}" target="_blank" style="color: #fe2c55; text-decoration: none;">@{user}</a></b></div>', unsafe_allow_html=True)
        with tab2:
            for user in i_not_back:
                st.markdown(f'<div class="user-card" style="border-left-color: #25d366;"><b><a href="https://www.tiktok.com/@{user}" target="_blank" style="color: #25d366; text-decoration: none;">@{user}</a></b></div>', unsafe_allow_html=True)
        
