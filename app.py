import streamlit as st
import json

# ตั้งค่าหน้าเว็บแบบกว้างและชื่อเท่ๆ
st.set_page_config(page_title="IG Insights Pro", page_icon="📈", layout="wide")

# คลุมโทนด้วย CSS (Custom Styling)
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .user-card { 
        padding: 10px; border-radius: 10px; background-color: white; 
        margin-bottom: 8px; border-left: 5px solid #E1306C;
        transition: transform 0.2s;
    }
    .user-card:hover { transform: scale(1.02); }
    </style>
    """, unsafe_allow_html=True)

st.title("📸 IG Follower Analytics Pro")
st.markdown("---")

with st.sidebar:
    st.header("🚀 Dashboard Control")
    st.write("อัปโหลดไฟล์เพื่อปลดล็อกฟีเจอร์")
    file_ing = st.file_uploader("📥 Following JSON", type="json")
    file_ers = st.file_uploader("📥 Followers JSON", type="json")
    st.divider()
    st.caption("ข้อมูลของคุณจะถูกประมวลผลบน Browser เท่านั้น ปลอดภัย 100%")

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

if file_ing and file_ers:
    try:
        data_ing = json.load(file_ing)
        data_ers = json.load(file_ers)
        following = extract_users(data_ing)
        followers = extract_users(data_ers)
        
        not_back = sorted(list(following - followers))
        i_not_back = sorted(list(followers - following))

        # --- ส่วนของ Visual Metrics ---
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        col_m1.metric("Following", len(following))
        col_m2.metric("Followers", len(followers))
        col_m3.metric("Not Following Back", len(not_back), delta=f"{len(not_back)} users", delta_color="inverse")
        col_m4.metric("You Don't Follow back", len(i_not_back))

        st.markdown("### 🔍 Detailed Analysis")
        tab1, tab2 = st.tabs(["❌ คนที่ไม่ฟอลกลับ", "⚠️ เรายังไม่ฟอลกลับ"])

        with tab1:
            st.info(f"มีทั้งหมด {len(not_back)} คนที่คุณติดตามแต่เขาไม่ได้ติดตามคุณ")
            # แบ่งเป็น Grid 3 คอลัมน์เพื่อความสวยงาม
            cols = st.columns(3)
            for idx, user in enumerate(not_back):
                with cols[idx % 3]:
                    st.markdown(f"""
                        <div class="user-card">
                            <small>Username</small><br>
                            <b><a href="https://www.instagram.com/{user}/" target="_blank" style="color: #E1306C; text-decoration: none;">@{user}</a></b>
                        </div>
                    """, unsafe_allow_html=True)

        with tab2:
            st.success(f"มีทั้งหมด {len(i_not_back)} คนที่ฟอลคุณแต่คุณยังไม่ได้ฟอลกลับ")
            cols = st.columns(3)
            for idx, user in enumerate(i_not_back):
                with cols[idx % 3]:
                    st.markdown(f"""
                        <div class="user-card" style="border-left: 5px solid #28a745;">
                            <small>Username</small><br>
                            <b><a href="https://www.instagram.com/{user}/" target="_blank" style="color: #28a745; text-decoration: none;">@{user}</a></b>
                        </div>
                    """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Error parsing data: {e}")
else:
    # หน้าจอ Welcome ตอนยังไม่อัปโหลด
    st.container()
    col_l, col_r = st.columns(2)
    with col_l:
        st.image("https://cdn-icons-png.flaticon.com/512/3955/3955024.png", width=200)
    with col_r:
        st.markdown("### ยินดีต้อนรับสู่โปรแกรมวิเคราะห์ IG")
        st.write("กรุณาอัปโหลดไฟล์จากเมนูด้านซ้ายเพื่อเริ่มวิเคราะห์ข้อมูลแบบเจาะลึก")
        
