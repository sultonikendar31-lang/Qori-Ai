import streamlit as st
import google.generativeai as genai

# --- 1. SETTING HALAMAN ---
st.set_page_config(page_title="QORI AI - Al Barokah", page_icon="🕌", layout="centered")

# --- 2. MASUKIN API KEY ---
# Kalau di Streamlit Cloud, taruh di Secrets. Kalau di laptop, ganti tulisan di bawah
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    API_KEY = "MASUKKAN_API_KEY_KAMU_DI_SINI"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

# --- 3. CSS TEMA HIJAU EMAS ---
st.markdown("""
<style>
    /* Background Utama */
    .stApp {
        background: linear-gradient(180deg, #06281F 0%, #0A3D2E 40%, #06281F 100%);
        background-image: radial-gradient(circle at 50% 0%, rgba(212,175,55,0.15) 0%, transparent 50%);
    }
    /* Hilangkan header bawaan */
    header {visibility: hidden;}
    .block-container {padding-top: 10px; max-width: 750px;}

    /* Judul Utama */
    .header-box {
        text-align: center;
        background: linear-gradient(135deg, #0E5A41 0%, #0A3D2E 100%);
        border: 2px solid #D4AF37;
        border-radius: 20px;
        padding: 22px 15px 18px 15px;
        margin-bottom: 5px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.4);
    }
    .header-box h1 {
        color: #FFD700 !important;
        font-size: 32px !important;
        margin: 0px !important;
        font-family: 'Georgia', serif;
        letter-spacing: 1px;
        text-shadow: 0 2px 10px rgba(0,0,0,0.5);
    }
    .header-box p {
        color: #E8DCC0 !important;
        font-size: 14px !important;
        margin-top: 8px !important;
    }
    .gold-line {
        height: 2px;
        background: linear-gradient(90deg, transparent, #D4AF37, transparent);
        margin: 12px 0px 0px 0px;
    }

    /* Tombol Cepat */
    .stButton > button {
        background: #1A6B4D !important;
        color: #FFEB99 !important;
        border: 1px solid #D4AF37 !important;
        border-radius: 20px !important;
        font-weight: 600 !important;
        width: 100%;
    }
    .stButton > button:hover {
        background: #D4AF37 !important;
        color: #06281F !important;
    }

    /* Chat Bubble */
    [data-testid="stChatMessage"] {
        border-radius: 18px !important;
        padding: 12px 15px !important;
    }
    /* Chat User - Emas */
    [data-testid="stChatMessage"][data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
        background: linear-gradient(135deg, #D4AF37, #B8962E) !important;
        color: #1A1A1A !important;
    }
    /* Chat AI - Hijau Tua */
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {
        background: #0E4A35 !important;
        border: 1px solid rgba(212,175,55,0.4) !important;
        color: white !important;
    }
    [data-testid="stChatMessage"] p { color: white !important; }
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) p { color: #1A1A1A !important; font-weight: 500; }

    /* Kotak Input */
    [data-testid="stChatInput"] {
        background: #0E4A35 !important;
        border: 1.5px solid #D4AF37 !important;
        border-radius: 25px !important;
    }
    [data-testid="stChatInput"] textarea { color: white !important; }
    [data-testid="stChatInput"] textarea::placeholder { color: #B8CFC4 !important; }

    /* Teks kecil bawah */
    .footer { text-align:center; color:#A8C4B5; font-size:11px; margin-top:15px; }
</style>
""", unsafe_allow_html=True)

# --- 4. HEADER ---
st.markdown("""
<div class="header-box">
    <h1>🕌 QORI AI - Al Barokah</h1>
    <p>Assalamu'alaikum! Tanya apa saja tentang Islam, Al-Qur'an, Hadits, dan Pelajaran Sekolah.</p>
    <div class="gold-line"></div>
</div>
""", unsafe_allow_html=True)

# --- 5. TOMBOL CEPAT ---
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("📖 Arti Al-Qur'an"): st.session_state["quick"] = "Jelaskan arti Al-Qur'an dengan bahasa sederhana untuk anak sekolah"
with c2:
    if st.button("📜 Arti Hadits"): st.session_state["quick"] = "Jelaskan apa itu Hadits dan contohnya untuk anak sekolah"
with c3:
    if st.button("🕌 Kisah Nabi"): st.session_state["quick"] = "Ceritakan kisah Nabi Muhammad SAW yang inspiratif untuk anak sekolah"

# --- 6. CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Assalamu'alaikum! 👋 Saya QORI AI. Silahkan tanya apa saja, saya siap membantu belajar dengan cara yang mudah dipahami."}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Ambil input dari tombol cepat atau ketikan
prompt = st.chat_input("Tulis pertanyaanmu di sini...")
if "quick" in st.session_state and st.session_state["quick"]:
    prompt = st.session_state.pop("quick")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("QORI sedang berpikir..."):
            try:
                system = "Kamu adalah QORI AI, guru Islami yang ramah untuk anak sekolah Al Barokah di Bekasi. Jawab dengan bahasa Indonesia sederhana, sopan, gunakan dalil Al-Qur'an/Hadits jika relevan, dan selalu akhiri dengan pelajaran yang bisa diambil. Jangan menjawab hal di luar adab Islam."
                res = model.generate_content(f"{system}\n\nPertanyaan: {prompt}")
                jawaban = res.text
            except Exception as e:
                jawaban = "Maaf, sedang ada gangguan. Coba lagi sebentar ya. (Pastikan API Key & Billing sudah aktif)"
            st.markdown(jawaban)
            st.session_state.messages.append({"role": "assistant", "content": jawaban})

st.markdown('<div class="footer">✨ QORI AI - Madrasah Al Barokah • Belajar Islam Jadi Lebih Menyenangkan ✨</div>', unsafe_allow_html=True)
