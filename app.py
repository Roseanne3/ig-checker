import streamlit as st
import json

st.set_page_config(page_title="IG Unfollow Tracker", page_icon="🕵️‍♂️", layout="wide")

st.title("🕵️‍♂️ สแกนยอดติดตามใน Instagram กัน 😊👈🏻")
st.subheader("ใครไม่ฟอลเรากลับ โดนแน่😠")

# ฟังก์ชันสกัดชื่อที่ปรับปรุงมาเพื่อไฟล์ของเพื่อนโดยเฉพาะ
def extract_instagram_users(data):
    users = set()
    
    # กรณีเป็น Dictionary (เหมือนในไฟล์ following.json ของเพื่อน)
    if isinstance(data, dict):
        for key in data:
            if isinstance(data[key], list):
                for item in data[key]:
                    # เช็คใน 'title' (อันนี้แหละที่เพื่อนมีปัญหา)
                    if 'title' in item and item['title']:
                        users.add(item['title'])
                    # เช็คใน 'string_list_data' -> 'value' (เผื่อไว้)
                    try:
                        val = item['string_list_data'][0]['value']
                        if val: users.add(val)
                    except:
                        pass
    
    # กรณีเป็น List (เหมือนในไฟล์ followers_1.json ของเพื่อน)
    elif isinstance(data, list):
        for item in data:
            try:
                # ดึงจาก value ใน string_list_data
                val = item['string_list_data'][0]['value']
                if val: users.add(val)
            except:
                # ถ้าไม่มี value ให้ลองดูที่ title
                if 'title' in item and item['title']:
                    users.add(item['title'])
    
    return users

col1, col2 = st.columns(2)
with col1:
    file_following = st.file_uploader("📂 อัปโหลด following.json", type="json")
with col2:
    file_followers = st.file_uploader("📂 อัปโหลด followers_1.json", type="json")

if file_following and file_followers:
    try:
        data_ing = json.load(file_following)
        data_ers = json.load(file_followers)

        following = extract_instagram_users(data_ing)
        followers = extract_instagram_users(data_ers)

        # ลบชื่อที่อาจเป็นค่าว่างออก
        following.discard("")
        followers.discard("")

        not_back = sorted(list(following - followers))
        i_not_back = sorted(list(followers - following))

        st.divider()
        m1, m2, m3 = st.columns(3)
        m1.metric("Following (เราตามเขา)", len(following))
        m2.metric("Followers (เขาตามเรา)", len(followers))
        m3.metric("ไม่ฟอลกลับ", len(not_back))

        res_col1, res_col2 = st.columns(2)
        with res_col1:
            st.error(f"❌ คนใจร้ายไม่ฟอลกลับ ({len(not_back)} คน)")
            for user in not_back:
                st.markdown(f"👉 [{user}](https://www.instagram.com/{user}/)")
        
        with res_col2:
            st.warning(f"⚠️ แหะๆ ลืมฟอลกลับ ({len(i_not_back)} คน)")
            for user in i_not_back:
                st.markdown(f"✅ [{user}](https://instagram.com/{user})")

    except Exception as e:
        st.error(f"เกิดข้อผิดพลาด: {e}")
else:
    st.info("อัปโหลดไฟล์ JSON ทั้งสองเพื่อเริ่มประมวลผลครับเพื่อน")
        
