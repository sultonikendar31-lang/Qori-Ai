import streamlit as st

DATA_SOAL = {
    "Iqro 1": [
        {"q": "Huruf ini apa?  ا", "opsi": ["Alif", "Ba", "Ta", "Jim"], "jawaban": "Alif"},
        {"q": "Huruf ini apa?  ب", "opsi": ["Ta", "Ba", "Tsa", "Jim"], "jawaban": "Ba"},
    ],
    "Iqro 2": [
        {"q": "Bacaan ini apa?  بَا", "opsi": ["Ba", "Baa", "Bi", "Bu"], "jawaban": "Baa"},
    ],
    "Iqro 3": [
        {"q": "Bacaan ini apa?  كَتَبَ", "opsi": ["Kataba", "Kutiba", "Katuba", "Kitaba"], "jawaban": "Kataba"},
    ],
    "Iqro 4": [
        {"q": "Bacaan ini apa?  مِنْ", "opsi": ["Min", "Man", "Mun", "Ma"], "jawaban": "Min"},
    ],
    "Iqro 5": [
        {"q": "Bacaan ini apa?  قُلْ", "opsi": ["Qul", "Qol", "Qil", "Qal"], "jawaban": "Qul"},
    ],
    "Iqro 6": [
        {"q": "Bacaan ini apa?  الرَّحْمَنِ", "opsi": ["Ar-Rahman", "Ar-Rahim", "Al-Malik", "Al-Quddus"], "jawaban": "Ar-Rahman"},
    ],
    "Tahsin": [
        {"q": "Hukum nun mati bertemu ب adalah?", "opsi": ["Idgham", "Iqlab", "Ikhfa", "Idzhar"], "jawaban": "Iqlab"},
    ],
    "Juz 30": [
        {"q": "Surah pertama di Juz 30 adalah?", "opsi": ["An-Naba", "An-Naziat", "Abasa", "Al-Fatihah"], "jawaban": "An-Naba"},
        {"q": "Surah Al-Ikhlas ada berapa ayat?", "opsi": ["3", "4", "5", "6"], "jawaban": "4"},
    ],
}

def tampilkan_game_qori():
    st.header("🎲 Game QORI")
    level = st.selectbox("Pilih Level:", list(DATA_SOAL.keys()))
    if "game_jawaban" not in st.session_state:
        st.session_state.game_jawaban = {}
    if "game_selesai" not in st.session_state:
        st.session_state.game_selesai = False
    soal_list = DATA_SOAL[level]
    for i, s in enumerate(soal_list):
        key = f"{level}_{i}"
        st.write(f"Soal {i+1}: {s['q']}")
        st.session_state.game_jawaban[key] = st.radio(f"Pilih jawaban soal {i+1}:", s["opsi"], key=key+"_radio")
    if st.button("✅ Selesai & Lihat Nilai", use_container_width=True):
        benar = sum(1 for i, s in enumerate(soal_list) if st.session_state.game_jawaban.get(f"{level}_{i}") == s["jawaban"])
        total = len(soal_list)
        st.session_state.game_nilai = int(benar / total * 100) if total > 0 else 0
        st.session_state.game_level = level
        st.session_state.game_benar = benar
        st.session_state.game_total = total
        st.session_state.game_selesai = True
        st.rerun()
    if st.session_state.game_selesai:
        tampilkan_hasil_game()

def tampilkan_hasil_game():
    nilai = st.session_state.get("game_nilai", 0)
    benar = st.session_state.get("game_benar", 0)
    total = st.session_state.get("game_total", 0)
    level = st.session_state.get("game_level", "-")
    st.success(f"🎉 Selesai! Level: {level}")
    st.metric("Nilai Kamu", f"{nilai}")
    st.write(f"Benar: {benar} dari {total} soal")
    if nilai == 100:
        st.balloons()
        st.write("MasyaAllah, sempurna! 🌟")
    elif nilai >= 70:
        st.write("Bagus, terus semangat! 💪")
    else:
        st.write("Jangan menyerah, coba lagi ya! 📖")
    if st.button("🔄 Main Lagi"):
        st.session_state.game_selesai = False
        st.session_state.game_jawaban = {}
        st.rerun()
