import streamlit as st
import google.generativeai as genai
import base64

st.set_page_config(page_title="QORI AI - Al Barokah", page_icon="🕌", layout="centered")

# --- BACKGROUND FOTO ---
def pasang_background(nama_file):
    try:
        with open(nama_file, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:image/jpeg;base64,{data}");
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
            }}
            .stApp::before {{
                content: "";
                position: fixed;
                inset: 0;
                background: rgba(0,0,0,0.55);
                z-index: 0;
            }}
            .stApp > header, .stApp > div {{
                position: relative;
                z-index: 1;
            }}
            [data-testid="stChatMessage"] {{
                background: white !important;
                border-radius: 15px !important;
                padding: 12px 15px !important;
                color: black !important;
                box-shadow: 0 2px 10px rgba(0,0,0,0.2);
            }}
            [data-testid="stChatMessage"] p {{
                color: black !important;
            }}
            div[data-testid="column"] {{
    display: flex !important;
    align-items: stretch !important;
}}
div[data-testid="column"] > div {{
    width: 100% !important;
}}
.stButton {{
    width: 100% !important;
}}
.stButton > button {{
    width: 100% !important;
    height: 50px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    margin-top: 0px !important;
    padding-top: 0px !important;
    padding-bottom: 0px !important;
}}
            </style>
            """,
            unsafe_allow_html=True
        )
    except:
        pass

pasang_background("background.jpeg")

# --- TEMA ---
st.markdown("""
<style>
.header-box {
    background-color: #1A3C34;
    padding: 25px 20px;
    border-radius: 15px;
    text-align: center;
    margin-bottom: 20px;
}
.header-box h1 { color: #D4AF37 !important; font-size: 32px !important; margin: 0px; }
.header-box p { color: white !important; font-size: 15px; margin-top: 8px; }
.stButton > button {
    background-color: #1A3C34 !important;
    color: white !important;
    border-radius: 12px !important;
    width: 100%;
    padding: 12px !important;
    font-weight: bold;
    border: none !important;
}
</style>
""", unsafe_allow_html=True)

# --- API KEY ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except:
    api_key = ""

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

# --- HEADER BARU ---
st.markdown("""
<div class="header-box">
<h1>🕌 QORI AI - Al Barokah</h1>
<p>Assalamualaikum warahmatullahi wabarakatuh! Tanya apa saja tentang Iqro, Tahsin dan Tahfidz</p>
</div>
""", unsafe_allow_html=True)

# --- 3 TOMBOL ---
# --- DATA SISWA ---
DATA_SISWA = {
    "Iqro": [
        ("Muhamad Hartanto", "Laki-laki", 63, "Iqro Dasar"),
        ("Daffan Oktaffil Hidayat", "Laki-laki", 62, "Iqro"),
    ],
    "Tahsin": [
        ("Frischa Bunga Lestari", "Perempuan", 73, "Udah bisa baca, Tajwid masih salah"),
        ("Raihan", "Laki-laki", 72, "Udah bisa baca, Tajwid masih salah"),
        ("Angga Fadillah", "Laki-laki", 71, "Udah bisa baca, Tajwid masih salah"),
        ("Andy Ramadani Abdullah", "Laki-laki", 76, "Udah bisa baca, Tajwid masih salah"),
    ],
    "Tahfidz": [
        ("Zalfatussyifa Ramadanti", "Perempuan", 85, "Udah Lancar, Tinggal Hafalan"),
        ("Zain Rahmanita", "Perempuan", 86, "Udah Lancar, Tinggal Hafalan"),
        ("Yusuf Imam Ma'ruf", "Laki-laki", 85, "Udah Lancar, Tinggal Hafalan"),
        ("Febriansyah Rachmat Hidayat", "Laki-laki", 85, "Udah Lancar, Tinggal Hafalan"),
        ("Muhammad Hafidz", "Laki-laki", 89, "Udah Lancar, Tinggal Hafalan"),
        ("Anggi Ratu Mahadewi", "Perempuan", 88, "Udah Lancar, Tinggal Hafalan"),
        ("Rizqi Ramadhany", "Laki-laki", 85, "Udah Lancar, Tinggal Hafalan"),
        ("Kawilujeungan Rasyida Raihanun", "Perempuan", 84, "Udah Lancar, Tinggal Hafalan"),
        ("Miftahul Jannah", "Perempuan", 81, "Udah Lancar, Tinggal Hafalan"),
        ("Muhamad Azham Fatahilah", "Laki-laki", 82, "Udah Lancar, Tinggal Hafalan"),
        ("Rosmalati Kholisha", "Perempuan", 83, "Udah Lancar, Tinggal Hafalan"),
        ("M. Arif Zakariya", "Laki-laki", 85, "Udah Lancar, Tinggal Hafalan"),
        ("Mochammad Alkahfi Mubarok", "Laki-laki", 86, "Udah Lancar, Tinggal Hafalan"),
        ("Imam Mansyur Ibnu Hulkarim", "Laki-laki", 80, "Udah Lancar, Tinggal Hafalan"),
    ],
}

def tampilkan_daftar(kategori):
    st.markdown(f"### Daftar Siswa {kategori} - {len(DATA_SISWA[kategori])} Siswa")
    for i, (nama, jk, nilai, ket) in enumerate(DATA_SISWA[kategori], 1):
        st.markdown(f"**{i}. {nama}** - {jk} - Nilai: {nilai} - {ket}")
col1, col2, col3 = st.columns(3)
with col1:
        klik_iqro = st.button("📖 Iqro", use_container_width=True)
with col2:
        klik_tahsin = st.button("📗 Tahsin", use_container_width=True)
with col3:
        klik_tahfidz = st.button("⭐ Tahfidz", use_container_width=True)

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Assalamu'alaikum! 👋 Saya QORI AI. Silahkan tanya apa saja, saya siap membantu belajar dengan cara yang mudah dipahami."}]

if klik_iqro:
    tampilkan_daftar("Iqro")
    prompt_awal = "Ajari saya membaca Iqro dari dasar, dengan cara yang mudah untuk anak Madrasah. Mulai dari huruf hijaiyah."
elif klik_tahsin:
    tampilkan_daftar("Tahsin")
    prompt_awal = "Ajari saya Tahsin Al-Qur'an, cara membaca dengan tajwid yang benar, makhraj huruf dan contohnya."
elif klik_tahfidz:
    tampilkan_daftar("Tahfidz")
    prompt_awal = "Bantu saya Tahfidz / menghafal Al-Qur'an, beri tips menghafal yang mudah dan ayat pendek untuk dihafal hari ini."
else:
    prompt_awal = None

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

prompt = st.chat_input("Tulis pertanyaanmu di sini...")
if prompt_awal:
    prompt = prompt_awal

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

st.markdown("<p style='text-align:center; font-size:12px; margin-top:20px; background-color:white; padding:8px; border-radius:10px;'>✨ QORI AI - Madrasah Al Barokah • Belajar Islam Jadi Lebih Menyenangkan ✨</p>", unsafe_allow_html=True)
