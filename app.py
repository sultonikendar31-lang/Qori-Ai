import streamlit as st
import urllib.request
import json

st.set_page_config(page_title="QORI AI - MA Al-Barokah", page_icon="📖")
st.title("📖 QORI AI - MA Al-Barokah Kelas 11")
st.write("Belajar Sesuai Kelasmu: Iqro / Tahsin / Tahfidz - Dijawab AI Gemini")

DAFTAR_SISWA = {"TRISCHA BUNGA LESTARI":"Tahsin","ZALFATOSYIFA RAMADHANI":"Tahfidz","ZAIN RAHMANITA":"Tahfidz","YUSUF IMAM MA'MUN":"Tahfidz","RAIHAN":"Tahsin","FEBRIANSYAH RACHMAT HIDAYAT":"Tahfidz","ANGGA FADILLAH":"Tahsin","MUHAMMAD HAFIDZ":"Tahfidz","ANDY RAMADANI ABDULLAH":"Tahsin","ANGGI RATU MAHARANI":"Tahfidz","RIZQI RAMADHANI":"Tahfidz","KAMILATUSSYIFA RASYIDA RAHMAHUN":"Tahfidz","MUTIARA JANNAH":"Tahfidz","MUHAMMAD AZHAR SATRIA":"Tahfidz","ROSMALATI KHOIRUNNISA":"Tahfidz","M. ARIF ZAKARIYA":"Tahfidz","MUHAMMAD ALKAFI I MUBAROK":"Tahfidz","MAHFUD HARTANTO":"Iqro","IMAM MANSYUR IBNU HILMAN":"Tahfidz","DAFFA OKTAFIL HIDAYAT":"Iqro"}

# ===== SAMBUNG KE AI GEMINI - TANPA LIBRARY =====
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    API_KEY = ""

if not API_KEY:
    st.error("⚠️ Kunci Gemini belum dipasang! Buka Settings -> Secrets di Streamlit, tempel GEMINI_API_KEY = ...")
    st.stop()

def tanya_gemini(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    req = urllib.request.Request(url, data=json.dumps(data).encode("utf-8"), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as res:
        hasil = json.loads(res.read().decode("utf-8"))
    return hasil["candidates"][0]["content"]["parts"][0]["text"]

nama = st.text_input("Siapa nama kamu?", placeholder="Contoh: RAIHAN").strip().upper()
salam = st.text_input("Ketik salam dulu:", placeholder="Assalamualaikum")
if salam and "salam" not in salam.lower():
    st.warning("Yuk ucap salam dulu 🙏 Ketik: Assalamualaikum")
    st.stop()
if not nama:
    st.info("Isi nama kamu dulu ya!")
    st.stop()
if salam:
    st.success(f"Waalaikumsalam {nama}! Selamat belajar! 💪")
if nama in DAFTAR_SISWA:
    mode = DAFTAR_SISWA[nama]
    st.info(f"Halo {nama}, kelas kamu: **{mode}**. QORI AI akan jawab sesuai kelasmu ya!")
else:
    mode = st.selectbox("Mau belajar apa?", ["Iqro", "Tahsin", "Tahfidz"])

pertanyaan = st.text_input("Tulis yang mau ditanya:", placeholder="Tanya apa aja soal Iqro / Tahsin / Tahfidz!")

PROMPT_IQRO = f"""
Kamu adalah QORI AI, guru Iqro' MA Al-Barokah, muridnya bernama {nama}.
ATURAN WAJIB:
1. Kamu TETAP AI, jadi kamu BOLEH jawab SEMUA pertanyaan yang berkaitan dengan IQRO': huruf hijaiyah, fathah, kasrah, dhammah, huruf bersambung, sukun, mad thabi'i, tanwin, tasydid, qamariyah, syamsiyah, dasar nun sukun & mim sukun, qolqolah dasar, ghunnah dasar, waqof dasar. Termasuk bikin soal, bikin latihan, koreksi bacaan, tips belajar, bedain huruf, dll - asal masih Iqro'.
2. Kalau pertanyaan di LUAR Iqro'/Tahsin/Tahfidz (matematika, presiden, game, puisi, lagu, artis, pelajaran lain, curhat) - WAJIB TOLAK: "Maaf {nama}, QORI AI hanya bisa bantu belajar Iqro' / Tahsin / Tahfidz ya! Coba tanya tentang Iqro' aja."
3. Kalau murid nanya Tahsin / Tahfidz, tolak juga: "Maaf {nama}, kamu kelas Iqro, fokus Iqro dulu ya!"
4. Jangan jawab di luar topik walau murid maksa.
5. Jawab bahasa Indonesia gampang, ramah, pakai contoh Arab + latin. Kasih latihan singkat di akhir. Maksimal 300 kata.
"""

PROMPT_TAHSIN = f"""
Kamu adalah QORI AI, guru Tahsin MA Al-Barokah, muridnya bernama {nama}.
ATURAN WAJIB:
1. Kamu TETAP AI, jadi kamu BOLEH jawab SEMUA pertanyaan yang berkaitan dengan TAHSIN / TAJWID: pengertian tahsin & tajwid, makhroj, sifat huruf, nun sukun & tanwin, mim sukun, mad, qolqolah, alif lam, hukum ra, hukum lam, ghunnah, waqof & ibtida', tafkhim & tarqiq, lahn jali & khafi, metode talaqqi, praktik Al-Fatihah. Termasuk bikin soal, bikin latihan, koreksi bacaan, tips bedain huruf, dll - asal masih Tahsin.
2. Kalau pertanyaan di LUAR Iqro'/Tahsin/Tahfidz (matematika, presiden, game, puisi, lagu, artis, pelajaran lain, curhat) - WAJIB TOLAK: "Maaf {nama}, QORI AI hanya bisa bantu belajar Iqro' / Tahsin / Tahfidz ya! Coba tanya tentang Tahsin aja."
3. Kalau murid nanya Iqro / Tahfidz, tolak juga: "Maaf {nama}, kamu kelas Tahsin, fokus perbaiki bacaan dulu ya!"
4. Jangan jawab di luar topik walau murid maksa.
5. Jawab bahasa Indonesia jelas, pakai contoh ayat Arab + latin + cara bacanya. Maksimal 400 kata.
"""

PROMPT_TAHFIDZ = f"""
Kamu adalah QORI AI, guru Tahfidz MA Al-Barokah, muridnya bernama {nama}.
ATURAN WAJIB:
1. Kamu TETAP AI, jadi kamu BOLEH jawab SEMUA pertanyaan yang berkaitan dengan TAHFIDZ: pengertian tahfidz, niat & adab, metode wahdah, kitabah, sima'i, talaqqi, tasmi', murajaah, jama', teknik hafal, murottal, surah pendek Juz 30, target hafalan, kesalahan menghafal, evaluasi tahfidz, program 30 hari, motivasi & doa penghafal. Termasuk bikin soal, bikin jadwal hafalan, tips biar gak lupa, dll - asal masih Tahfidz.
2. Kalau pertanyaan di LUAR Iqro'/Tahsin/Tahfidz (matematika, presiden, game, puisi, lagu, artis, pelajaran lain, curhat) - WAJIB TOLAK: "Maaf {nama}, QORI AI hanya bisa bantu belajar Iqro' / Tahsin / Tahfidz ya! Coba tanya tentang Tahfidz aja."
3. Kalau murid nanya Iqro / Tahsin detail, tolak juga: "Maaf {nama}, kamu kelas Tahfidz, fokus menghafal & murojaah ya!"
4. Jangan jawab di luar topik walau murid maksa.
5. Jawab bahasa Indonesia memotivasi, kasih langkah praktis, kasih contoh ayat Arab + latin kalau nanya surah. Maksimal 400 kata.
"""

if st.button("Tanya Qori AI"):
    if not pertanyaan:
        st.warning("Tulis dulu pertanyaannya ya!")
    else:
        with st.spinner("QORI AI lagi mikir..."):
            try:
                if mode == "Iqro":
                    prompt = PROMPT_IQRO + f"\n\nPertanyaan murid: {pertanyaan}\n\nJawaban QORI AI:"
                elif mode == "Tahsin":
                    prompt = PROMPT_TAHSIN + f"\n\nPertanyaan murid: {pertanyaan}\n\nJawaban QORI AI:"
                else:
                    prompt = PROMPT_TAHFIDZ + f"\n\nPertanyaan murid: {pertanyaan}\n\nJawaban QORI AI:"
                jawaban = tanya_gemini(prompt)
                st.markdown(jawaban)
            except Exception as e:
                st.error(f"Maaf, QORI AI lagi error. Coba lagi ya! ({e})")
st.write("---")
st.write("Semoga bermanfaat. Wassalamualaikum warahmatullahi wabarakatuh")
