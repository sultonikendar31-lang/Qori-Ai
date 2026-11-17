try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    API_KEY = ""

if not API_KEY:
    st.info("Tempel Kunci Gemini kamu di bawah ini (sekali aja, biar bisa jalan):")
    API_KEY = st.text_input("Kunci Gemini (AIzaSy...):", type="password").strip()

if not API_KEY:
    st.error("⚠️ Belum ada kuncinya. Daftar dulu di aistudio.google.com -> Get API Key -> Create API Key, terus tempel di sini.")
    st.stop()
