import streamlit as st
import json

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Multi-Check Pro", page_icon="📊", layout="wide")

# 2. ปรับแต่ง CSS ให้เหมาะกับมือถือ (Mobile First)
st.markdown("""
    <style>
    /* ปรับปุ่มให้ใหญ่กดง่ายในมือถือ */
    .stButton>button {
        width: 100%;
        height: 60px;
        font-size: 18px;
        border-radius: 15px;
        margin-bottom: 10px;
    }
    /* ปรับแต่งการ์ดรายชื่อให้โปร่งแสงและดูดีในโหมดมืด */
    .user-card { 
        padding: 15px; 
        border-radius: 12px; 
        background-color: rgba(128, 128, 128, 0.1); 
        margin-bottom: 10px; 
        border-left: 6px solid #E1306C;
        backdrop-filter: blur(10px);
    }
    /* ซ่อนขอบเขตที่รกๆ */
    [data-testid="stMetric"] {
        background-color: rgba(128, 128, 128, 0.05);
        border-radius: 15px;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. จัดการหน้า (Session State)
if 'page' not in st.session_state:
    st.session_state.page = 'home'

def go_to_page(page_name):
    st.session_state.page = page_name
    st.rerun()

# --- ฟังก์ชันขุดข้อมูล ---
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
    st.title("🚀 Social Analytics")
    st.write("เลือกแพลตฟอร์มที่ต้องการใช้งาน")
    
    # บนมือถือใช้ columns แบบนี้จะช่วยให้ปุ่มไม่เบียดกันมาก
    st.info("💡 แนะนำ: โหลดไฟล์ JSON จาก IG มาเตรียมไว้ก่อนนะ")
    
    if st.button("📸 Instagram Tracker"):
        go_to_page('instagram')
    
    if st.button("🎵 TikTok Tracker (เร็วๆ นี้)"):
        go_to_page('tiktok')

# --- หน้า Instagram ---
elif st.session_state.page == 'instagram':
    # ปุ่มย้อนกลับแบบสะอาดๆ
    if st.button("⬅️ กลับหน้าเลือกแพลตฟอร์ม"):
        go_to_page('home')
    
    st.header("📸 Instagram Tracker")
    st.write("อัปโหลดไฟล์เพื่อเริ่มการตรวจสอบ")

    # ส่วนอัปโหลด
    file_ing = st.file_uploader("📥 ขั้นตอนที่ 1: ใส่ไฟล์ following.json", type="json")
    file_ers = st.file_uploader("📥 ขั้นตอนที่ 2: ใส่ไฟล์ followers_1.json", type="json")

    # โชว์ผลลัพธ์เฉพาะตอนที่มีไฟล์ครบเท่านั้น!
    if file_ing and file_ers:
        try:
            data_ing = json.load(file_ing)
            data_ers = json.load(file_ers)
            ing = extract_users(data_ing)
            ers = extract_users(data_ers)
            
            not_back = sorted(list(ing - ers))
            i_not_back = sorted(list(ers - ing))

            st.success("✅ วิเคราะห์เสร็จสิ้น!")
            
            # Metric โชว์เรียงกันสวยๆ
            m1, m2, m3 = st.columns(3)
            m1.metric("Following", len(ing))
            m2.metric("Followers", len(ers))
            m3.metric("ไม่ฟอลกลับ", len(not_back))

            tab1, tab2 = st.tabs([f"❌ เขาไม่ตามเรา ({len(not_back)})", f"⚠️ เราไม่ตามเขา ({len(i_not_back)})"])

            with tab1:
                if not_back:
                    for user in not_back:
                        st.markdown(f'<div class="user-card"><b><a href="https://www.instagram.com/{user}/" target="_blank" style="color: #E1306C; text-decoration: none;">@{user}</a></b></div>', unsafe_allow_html=True)
                else:
                    st.write("ไม่มีคนที่ไม่ฟอลกลับ")

            with tab2:
                if i_not_back:
                    for user in i_not_back:
                        st.markdown(f'<div class="user-card" style="border-left-color: #28a745;"><b><a href="https://www.instagram.com/{user}/" target="_blank" style="color: #28a745; text-decoration: none;">@{user}</a></b></div>', unsafe_allow_html=True)
        
        except Exception as e:
            st.error(f"เกิดข้อผิดพลาด: {e}")
    else:
        st.warning("รออัปโหลดไฟล์ให้ครบทั้ง 2 ช่องด้านบนครับ")

# --- หน้า TikTok ---
elif st.session_state.page == 'tiktok':
    if st.button("⬅️ กลับ"):
        go_to_page('home')
    st.title("🎵 TikTok Analytics")
    st.write("ฟีเจอร์นี้กำลังถูกพัฒนา... อดใจรอหน่อยนะเพื่อน!")
                                   
