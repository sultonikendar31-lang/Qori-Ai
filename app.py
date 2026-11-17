import streamlit as st
import json
import urllib.request
import os

st.set_page_config(page_title="QORI AI - Al Barokah", page_icon="🕌")
st.title("🕌 QORI AI - Al Barokah")
st.write("Assalamu'alaikum! Tanya apa saja tentang Islam, Al-Qur'an, Hadits, dan pelajaran sekolah.")

# Ambil kunci dari Secrets Streamlit
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    API_KEY = os.getenv("GEMINI_API_KEY", "")

def tanya_gemini(prompt):
    for nama_model in ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{nama_model}:generateContent?key={API_KEY}"
            data = {"contents": [{"parts": [{"text": prompt}]}]}
            req = urllib.request.Request(url, data=json.dumps(data).encode("utf-8"), headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=60) as res:
                hasil = json.loads(res.read().decode("utf-8"))
            return hasil["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            if "404" in str(e):
                continue
            raise e
    raise Exception("Semua model Gemini lagi gak bisa diakses, coba lagi 1 menit ya!")

if "chat" not in st.session_state:
    st.session_state.chat = []

for pesan in st.session_state.chat:
    with st.chat_message(pesan["role"]):
        st.write(pesan["isi"])

pertanyaan = st.chat_input("Tulis pertanyaanmu di sini...")

if pertanyaan:
    st.session_state.chat.append({"role": "user", "isi": pertanyaan})
    with st.chat_message("user"):
        st.write(pertanyaan)
    with st.chat_message("assistant"):
        with st.spinner("QORI lagi mikir..."):
            try:
                jawaban = tanya_gemini(f"Kamu adalah QORI AI, ustadz AI yang ramah untuk anak sekolah di Al Barokah. Jawab dengan bahasa Indonesia yang mudah dimengerti, sopan, dan berdasarkan Al-Qur'an dan Hadits. Pertanyaan: {pertanyaan}")
                st.write(jawaban)
                st.session_state.chat.append({"role": "assistant", "isi": jawaban})
            except Exception as e:
                st.error(f"Maaf, ada error: {e}")
