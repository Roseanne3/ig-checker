import streamlit as st
import json

st.set_page_config(page_title="IG Unfollow Tracker", page_icon="📸", layout="wide")

st.title("🕵️‍♂️ เช็คยอด ติดตามใน Instagram (เวอร์ชันขุดรากถอนโคน)")

# ฟังก์ชันขุดหา Username แบบไม่สนโครงสร้าง (Recursive Search)
def find_usernames(obj):
    found = set()
    if isinstance(obj, dict):
        # ถ้าเจอ key ชื่อ 'value' และข้างบนมันมี 'string_list_data' (โครงสร้างหลักของ IG)
        if 'value' in obj and isinstance(obj['value'], str):
            # กรองเฉพาะตัวที่ดูเหมือน username (ไม่มีเว้นวรรค และไม่ใช่วันที่)
            name = obj['value']
            if ' ' not in name and ':' not in name:
                found.add(name)
        for k, v in obj.items():
            found.update(find_usernames(v))
    elif isinstance(obj, list):
        for item in obj:
            found.update(find_usernames(item))
    return found

col1, col2 = st.columns(2)
with col1:
    file_following = st.file_uploader("📂 อัปโหลด following.json", type="json")
with col2:
    file_followers = st.file_uploader("📂 อัปโหลด followers_1.json", type="json")

if file_following and file_followers:
    try:
        data_ing = json.load(file_following)
        data_ers = json.load(file_followers)

        # สั่งขุดข้อมูล
        following = find_usernames(data_ing)
        followers = find_usernames(data_ers)

        # ลบชื่อตัวเองออก (บางที IG ใส่ชื่อเจ้าของบัญชีมาในไฟล์ด้วย)
        # ปกติชื่อเราจะอยู่ในทั้งสองไฟล์อยู่แล้ว ผลลัพธ์เลยไม่เพี้ยน

        not_back = sorted(list(following - followers))
        i_not_back = sorted(list(followers - following))

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
    st.info("อัปโหลดไฟล์ทั้งสองเพื่อเริ่มเช็คเลยเพื่อน!")
    
