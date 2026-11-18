import streamlit as st
import base64
from google import genai

st.set_page_config(page_title="QORI AI", page_icon="🕌", layout="wide")

api_key = st.secrets.get("GEMINI_API_KEY", "")

if "kategori_pilih" not in st.session_state:
    st.session_state["kategori_pilih"] = None
if "messages" not in st.session_state:
    st.session_state["messages"] = []

prompt_awal = None

def get_base64(file):
    try:
        with open(file, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return ""

bg = get_base64("background.jpeg")
if bg:
    st.markdown(f"""
    <style>
    /* INI YANG BAGUS KAYA FOTO PERTAMA - JANGAN DIUBAH LAGI */
    .stApp, [data-testid="stApp"], [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/jpeg;base64,{bg}") !important;
        background-size: cover !important;
        background-position: center center !important;
        background-repeat: no-repeat !important;
        background-attachment: fixed !important;
    }}
    [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"] {{
        background: transparent !important;
    }}
    .stApp::before {{
        content: "";
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background: rgba(0,0,0,0.40);
        z-index: 0;
        pointer-events: none;
    }}
    .block-container {{
        position: relative;
        z-index: 1;
        padding-top: 20px !important;
        max-width: 900px !important;
    }}
        /* BAWAH DIKASIH GAMBAR SAMA TAPI PAKAI FIXED BIAR NYATU, NGGAK DOBEL, NGGAK PUTIH */
    [data-testid="stBottom"] {{
        background-image: url("data:image/jpeg;base64,{bg}") !important;
        background-size: cover !important;
        background-position: center center !important;
        background-repeat: no-repeat !important;
        background-attachment: fixed !important;
    }}
    [data-testid="stBottomBlockContainer"], [data-testid="stChatInputContainer"] {{
        background: transparent !important;
        background-image: none !important;
        background-color: transparent !important;
    }}
    /* GELAPIN BAWAHNYA DIKIT BIAR SAMA KAYAK ATAS */
    [data-testid="stBottom"]::before {{
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: rgba(0,0,0,0.40);
        pointer-events: none;
    }}
    [data-testid="stChatInput"] {{
        position: relative;
        z-index: 2;
        background-color: white !important;
    }}
    [data-testid="stChatInput"] {{
        background-color: white !important;
        border-radius: 20px !important;
    }}
    </style>
    """, unsafe_allow_html=True)

st.markdown("""
<div style='background-color: rgba(20, 50, 35, 0.92); padding: 25px; border-radius: 15px; text-align:center;'>
    <h1 style='color:#F9D423; margin:0; font-size:36px;'>🕌 QORI AI Madrasah Aliyah Al-Barokah</h1>
    <p style='color:white; margin-top:10px; font-size:16px;'>Assalamualaikum warahmatullahi wabarakatuh! Tanya apa saja tentang Iqro, Tahsin dan Tahfidz</p>
</div>
""", unsafe_allow_html=True)

st.write("")

def tampilkan_daftar(kategori):
    if kategori == "Iqro":
        daftar = ["Iqro 1", "Iqro 2", "Iqro 3", "Iqro 4", "Iqro 5", "Iqro 6"]
    elif kategori == "Tahsin":
        daftar = ["Makhraj Huruf", "Tajwid Dasar", "Mad & Qalqalah", "Gharib"]
    else:
        daftar = ["Juz 30 - An-Naba", "Juz 30 - An-Naziat", "Juz 30 - Abasa", "Surat Al-Fatihah"]
    for item in daftar:
        if st.button(item, key=f"{kategori}-{item}"):
            return f"Tolong ajarkan saya {item} dengan cara yang mudah untuk anak Madrasah Aliyah"
    return None

c_btn1, c_btn2, c_btn3 = st.columns(3)
with c_btn1:
    klik_iqro = st.button("📖 Iqro", use_container_width=True)
with c_btn2:
    klik_tahsin = st.button("📗 Tahsin", use_container_width=True)
with c_btn3:
    klik_tahfidz = st.button("⭐ Tahfidz", use_container_width=True)

if klik_iqro:
    st.session_state["kategori_pilih"] = None if st.session_state["kategori_pilih"] == "Iqro" else "Iqro"
if klik_tahsin:
    st.session_state["kategori_pilih"] = None if st.session_state["kategori_pilih"] == "Tahsin" else "Tahsin"
if klik_tahfidz:
    st.session_state["kategori_pilih"] = None if st.session_state["kategori_pilih"] == "Tahfidz" else "Tahfidz"

if st.session_state["kategori_pilih"]:
    c1, c2, c3 = st.columns(3)
    if st.session_state["kategori_pilih"] == "Iqro":
        with c1:
            p = tampilkan_daftar("Iqro")
            if p: prompt_awal = p
    if st.session_state["kategori_pilih"] == "Tahsin":
        with c2:
            p = tampilkan_daftar("Tahsin")
            if p: prompt_awal = p
    if st.session_state["kategori_pilih"] == "Tahfidz":
        with c3:
            p = tampilkan_daftar("Tahfidz")
            if p: prompt_awal = p

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])

prompt = None
if prompt_awal:
    prompt = prompt_awal
else:
    prompt = st.text_input("Tulis pertanyaanmu di sini...", placeholder="Tulis pertanyaanmu di sini...", label_visibility="collapsed")
    kirim = st.button("Kirim ➤", use_container_width=True)
    if not kirim:
        prompt = None

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    with st.chat_message("assistant"):
        if not api_key:
            st.write("Maaf, API Key belum dipasang di Secrets Streamlit.")
        else:
            try:
                client = genai.Client(api_key=api_key)
                response = client.models.generate_content(model="gemini-2.5-flash", contents=f"Kamu adalah QORI AI, guru ngaji yang ramah untuk anak Madrasah Aliyah Al Barokah. Jawab dengan bahasa Indonesia yang mudah, sopan, dan islami. Pertanyaan: {prompt}")
                st.write(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.write(f"Maaf, sedang ada gangguan. Coba lagi ya. ({e})")

st.markdown("<p style='text-align:center; font-size:12px; margin-top:20px; background-color:white; padding:8px; border-radius:10px;'> QORI AI - Madrasah Aliyah Al Barokah</p>", unsafe_allow_html=True)
