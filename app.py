import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="QORI AI - Al Barokah", page_icon="🕌")

# --- TEMA HIJAU-EMAS ---
st.markdown("""
<style>
.stApp { background-color: #F2F4F3; }
div[data-testid="stVerticalBlock"] > div:first-child {
    background-color: #1A3C34; padding: 25px; border-radius: 15px; text-align: center;
}
h1 { color: #D4AF37 !important; font-size: 32px !important; }
.chat-box { background-color: #1A3C34; color: white; padding: 15px; border-radius: 12px; }
</style>
""", unsafe_allow_html=True)

# --- KUNCI API ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except:
    api_key = ""
    st.error("API Key belum diisi di Secrets!")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

# --- HEADER ---
st.markdown("""
<div>
<h1>🕌 QORI AI - Al Barokah</h1>
<p style="color:white;">Assalamu'alaikum! Tanya apa saja tentang Islam, Al-Qur'an, Hadits dan Pelajaran Sekolah.</p>
</div>
""", unsafe_allow_html=True)

# --- 3 TOMBOL BARU: IQRO, TAHSIN, TAHFIDZ ---
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("📖 Iqro"):
        st.session_state.prompt = "Ajari saya membaca Iqro dari dasar, dengan cara yang mudah untuk anak Madrasah. Mulai dari huruf hijaiyah."
with col2:
    if st.button("📗 Tahsin"):
        st.session_state.prompt = "Ajari saya Tahsin Al-Qur'an, cara membaca dengan tajwid yang benar, makhraj huruf dan contohnya."
with col3:
    if st.button("⭐ Tahfidz"):
        st.session_state.prompt = "Bantu saya Tahfidz / menghafal Al-Qur'an, beri tips menghafal yang mudah dan ayat pendek untuk dihafal hari ini."

# --- CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Assalamu'alaikum! 👋 Saya QORI AI. Silahkan tanya apa saja, saya siap membantu belajar dengan cara yang mudah dipahami."}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Jika tombol diklik, langsung jawab
prompt = st.chat_input("Tulis pertanyaanmu di sini...")
if "prompt" in st.session_state and st.session_state.prompt:
    prompt = st.session_state.prompt
    st.session_state.prompt = ""

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    with st.chat_message("assistant"):
        try:
            response = model.generate_content(f"Kamu adalah QORI AI, guru ngaji yang ramah untuk anak Madrasah Al Barokah. Jawab dengan bahasa Indonesia yang mudah, sopan, dan islami. Pertanyaan: {prompt}")
            st.write(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.write("Maaf, sedang ada gangguan. Coba lagi ya.")

st.markdown("<p style='text-align:center; font-size:12px;'>✨ QORI AI - Madrasah Al Barokah • Belajar Islam Jadi Lebih Menyenangkan ✨</p>", unsafe_allow_html=True)
