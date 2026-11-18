import streamlit as st
from google import genai

st.set_page_config(page_title="QORI AI", page_icon="🕌")

api_key = st.secrets.get("GEMINI_API_KEY", "")

if "kategori_pilih" not in st.session_state:
    st.session_state["kategori_pilih"] = None
if "messages" not in st.session_state:
    st.session_state["messages"] = []

prompt_awal = None

st.markdown("<h1 style='text-align:center;'>🕌 QORI AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Guru Ngaji - Madrasah Aliyah Al Barokah</p>", unsafe_allow_html=True)

def tampilkan_daftar(kategori):
    if kategori == "Iqro":
        daftar = ["Iqro 1", "Iqro 2", "Iqro 3", "Iqro 4", "Iqro 5", "Iqro 6"]
    elif kategori == "Tahsin":
        daftar = ["Makhraj Huruf", "Tajwid Dasar", "Mad & Qalqalah", "Gharib"]
    else:
        daftar = ["Juz 30 - An-Naba", "Juz 30 - An-Naziat", "Juz 30 - Abasa", "Surat Al-Fatihah"]
    for item in daftar:
        if st.button(item, key=f"{kategori}-{item}"):
            st.session_state["prompt_pilih"] = f"Tolong ajarkan saya {item} dengan cara yang mudah untuk anak Madrasah Aliyah"
    if "prompt_pilih" in st.session_state:
        return st.session_state.pop("prompt_pilih")
    return None

c_btn1, c_btn2, c_btn3 = st.columns(3)
with c_btn1:
    klik_iqro = st.button("📖 Iqro", use_container_width=True)
with c_btn2:
    klik_tahsin = st.button("🎙️ Tahsin", use_container_width=True)
with c_btn3:
    klik_tahfidz = st.button("🧠 Tahfidz", use_container_width=True)

if api_key:
    client = genai.Client(api_key=api_key)
    model = "gemini-2.5-flash"

if klik_iqro:
    if st.session_state["kategori_pilih"] == "Iqro":
        st.session_state["kategori_pilih"] = None
    else:
        st.session_state["kategori_pilih"] = "Iqro"

if klik_tahsin:
    if st.session_state["kategori_pilih"] == "Tahsin":
        st.session_state["kategori_pilih"] = None
    else:
        st.session_state["kategori_pilih"] = "Tahsin"

if klik_tahfidz:
    if st.session_state["kategori_pilih"] == "Tahfidz":
        st.session_state["kategori_pilih"] = None
    else:
        st.session_state["kategori_pilih"] = "Tahfidz"

# Tampilkan lurus di bawah tombolnya
if st.session_state["kategori_pilih"]:
    c1, c2, c3 = st.columns(3)
    if st.session_state["kategori_pilih"] == "Iqro":
        with c1:
            p = tampilkan_daftar("Iqro")
            if p:
                prompt_awal = p
    if st.session_state["kategori_pilih"] == "Tahsin":
        with c2:
            p = tampilkan_daftar("Tahsin")
            if p:
                prompt_awal = p
    if st.session_state["kategori_pilih"] == "Tahfidz":
        with c3:
            p = tampilkan_daftar("Tahfidz")
            if p:
                prompt_awal = p

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])

prompt = st.chat_input("Tulis pertanyaanmu di sini...")
if prompt_awal:
    prompt = prompt_awal

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    with st.chat_message("assistant"):
        try:
            response = client.models.generate_content(model=model, contents=f"Kamu adalah QORI AI, guru ngaji yang ramah untuk anak Madrasah Aliyah Al Barokah. Jawab dengan bahasa Indonesia yang mudah, sopan, dan islami. Pertanyaan: {prompt}")
            st.write(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.write("Maaf, sedang ada gangguan. Coba lagi ya.")

st.markdown("<p style='text-align:center; font-size:12px; margin-top:20px; background-color:white; padding:8px; border-radius:10px;'> QORI AI - Madrasah Aliyah Al Barokah ✨ خَيْرُكُمْ مَنْ تَعَلَّمَ الْقُرْآنَ وَعَلَّمَهُ ✨ Sebaik-baik kalian adalah yang belajar Al-Qur'an dan mengajarkannya</p>", unsafe_allow_html=True)
