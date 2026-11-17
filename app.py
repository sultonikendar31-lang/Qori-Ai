import streamlit as st
import json
import urllib.request
import os

st.set_page_config(page_title="QORI AI - Al Barokah", page_icon="🕌")
st.title("🕌 QORI AI - Al Barokah")
st.write("Assalamu'alaikum! Tanya apa saja tentang Islam, Al-Qur'an, Hadits, dan pelajaran sekolah.")

try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    API_KEY = ""

# JAWABAN CADANGAN - ini yang bikin siswa selalu dapat jawaban
def jawaban_cadangan(p):
    p = p.lower()
    if "hadits" in p or "hadis" in p:
        return "Hadits adalah segala perkataan, perbuatan, dan persetujuan Nabi Muhammad SAW. Hadits adalah sumber hukum Islam kedua setelah Al-Qur'an. Contohnya Hadits tentang niat: 'Sesungguhnya segala amal itu tergantung niatnya.' (HR. Bukhari dan Muslim)"
    if "iqro" in p or "iqra" in p:
        return "Iqro artinya 'Bacalah!'. Itu wahyu pertama yang diterima Nabi Muhammad SAW di Gua Hira, Surah Al-'Alaq ayat 1-5. Artinya Allah memerintahkan kita untuk rajin belajar dan membaca."
    if "wudhu" in p or "wudu" in p:
        return "Tata cara wudhu: 1. Niat, 2. Basuh telapak tangan, 3. Kumur-kumur, 4. Basuh hidung, 5. Basuh muka, 6. Basuh tangan sampai siku, 7. Usap kepala, 8. Basuh telinga, 9. Basuh kaki sampai mata kaki."
    if "sholat" in p or "shalat" in p or "solat" in p:
        return "Sholat 5 waktu: Subuh 2 rakaat, Dzuhur 4 rakaat, Ashar 4 rakaat, Maghrib 3 rakaat, Isya 4 rakaat. Sholat itu tiang agama, jangan sampai ditinggalkan ya!"
    if "puasa" in p:
        return "Puasa artinya menahan diri dari makan, minum, dan hal yang membatalkan dari terbit fajar sampai terbenam matahari. Puasa Ramadhan wajib bagi umat Islam yang sudah baligh."
    if "quran" in p or "qur'an" in p or "al-quran" in p:
        return "Al-Qur'an adalah kitab suci umat Islam, firman Allah yang diturunkan kepada Nabi Muhammad SAW melalui Malaikat Jibril. Terdiri dari 30 juz, 114 surah, dan 6236 ayat."
    return None

def tanya_gemini(prompt):
    for nama_model in ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{nama_model}:generateContent?key={API_KEY}"
            data = {"contents": [{"parts": [{"text": prompt}]}]}
            req = urllib.request.Request(url, data=json.dumps(data).encode("utf-8"), headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=30) as res:
                hasil = json.loads(res.read().decode("utf-8"))
            return hasil["candidates"][0]["content"]["parts"][0]["text"]
        except Exception:
            continue
    return None

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
            jawaban = tanya_gemini(f"Kamu QORI AI, ustadz AI ramah untuk anak sekolah Al Barokah. Jawab bahasa Indonesia mudah, sopan, berdasarkan Al-Qur'an dan Hadits. Pertanyaan: {pertanyaan}")
            if not jawaban:
                jawaban = jawaban_cadangan(pertanyaan)
            if not jawaban:
                jawaban = "Maaf ya, Gemini lagi sibuk banget. Coba tanya lagi dengan kata lain, contoh: 'arti hadits', 'arti iqro', 'tata cara wudhu', 'sholat 5 waktu'. InsyaAllah QORI jawab!"
            st.write(jawaban)
            st.session_state.chat.append({"role": "assistant", "isi": jawaban})
