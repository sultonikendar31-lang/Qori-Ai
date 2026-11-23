import random
from datetime import datetime
import streamlit as st

SOAL_IQRO = [
    {"soal": "Huruf apa ini? **ب**", "pilihan": ["Ba", "Ta", "Tsa", "Jim"], "jawaban": "Ba"},
    {"soal": "Huruf apa ini? **ت**", "pilihan": ["Ba", "Ta", "Tsa", "Ha"], "jawaban": "Ta"},
    {"soal": "Huruf apa ini? **ث**", "pilihan": ["Tsa", "Jim", "Ha", "Kha"], "jawaban": "Tsa"},
    {"soal": "Huruf apa ini? **ج**", "pilihan": ["Ha", "Jim", "Kha", "Dal"], "jawaban": "Jim"},
    {"soal": "Huruf apa ini? **ح**", "pilihan": ["Jim", "Ha", "Kha", "Ain"], "jawaban": "Ha"},
    {"soal": "Huruf apa ini? **خ**", "pilihan": ["Ha", "Jim", "Kha", "Dal"], "jawaban": "Kha"},
    {"soal": "Huruf apa ini? **د**", "pilihan": ["Dzal", "Ro", "Dal", "Zay"], "jawaban": "Dal"},
    {"soal": "Huruf apa ini? **س**", "pilihan": ["Syin", "Sin", "Shod", "Dhod"], "jawaban": "Sin"},
    {"soal": "Huruf apa ini? **ش**", "pilihan": ["Sin", "Syin", "Shod", "Dhod"], "jawaban": "Syin"},
    {"soal": "Huruf **ا** dibaca?", "pilihan": ["A", "Ba", "Ta", "Sa"], "jawaban": "A"},
]
SOAL_TAHSIN = [
    {"soal": "Nun Sukun bertemu Ba (مِنْ بَعْدِ) hukumnya?", "pilihan": ["Iqlab", "Idgham", "Ikhfa", "Idzhar"], "jawaban": "Iqlab"},
    {"soal": "Nun Sukun bertemu Ya (مَنْ يَعْمَلْ) hukumnya?", "pilihan": ["Idgham Bighunnah", "Iqlab", "Ikhfa", "Idzhar"], "jawaban": "Idgham Bighunnah"},
    {"soal": "Mim Sukun bertemu Ba (هُمْ بِهِ) hukumnya?", "pilihan": ["Ikhfa Syafawi", "Idgham Mimi", "Idzhar Syafawi", "Iqlab"], "jawaban": "Ikhfa Syafawi"},
    {"soal": "Nun Sukun bertemu Ro (مِنْ رَبِّهِمْ) hukumnya?", "pilihan": ["Idgham Bilaghunnah", "Idgham Bighunnah", "Ikhfa", "Idzhar"], "jawaban": "Idgham Bilaghunnah"},
    {"soal": "Tanwin bertemu Jim hukumnya?", "pilihan": ["Ikhfa", "Idzhar", "Iqlab", "Idgham"], "jawaban": "Ikhfa"},
    {"soal": "Mad Thabi'i panjangnya?", "pilihan": ["2 harakat", "6 harakat", "4 harakat", "1 harakat"], "jawaban": "2 harakat"},
    {"soal": "Huruf Qolqolah ada berapa?", "pilihan": ["5", "4", "6", "3"], "jawaban": "5"},
    {"soal": "Huruf Qolqolah adalah?", "pilihan": ["ق - ط - ب - ج - د", "ا - و - ي", "ن - م", "خ - غ"], "jawaban": "ق - ط - ب - ج - د"},
    {"soal": "Mim Sukun bertemu Mim hukumnya?", "pilihan": ["Idgham Mimi", "Ikhfa Syafawi", "Idzhar Syafawi", "Iqlab"], "jawaban": "Idgham Mimi"},
    {"soal": "Lam Jalalah dibaca Tafkhim jika sebelumnya?", "pilihan": ["Fathah / Dhommah", "Kasrah", "Sukun", "Tanwin"], "jawaban": "Fathah / Dhommah"},
]
SOAL_TAHFIDZ = [
    {"soal": "Lanjutkan: بِسْمِ اللَّهِ الرَّحْمَٰنِ ...", "pilihan": ["الرَّحِيمِ", "الْعَالَمِينَ", "مَالِكِ يَوْمِ الدِّينِ", "إِيَّاكَ نَعْبُدُ"], "jawaban": "الرَّحِيمِ"},
    {"soal": "Lanjutkan: الْحَمْدُ لِلَّهِ رَبِّ ...", "pilihan": ["الْعَالَمِينَ", "الرَّحِيمِ", "مَالِكِ يَوْمِ الدِّينِ", "اهْدِنَا"], "jawaban": "الْعَالَمِينَ"},
    {"soal": "Lanjutkan: وَالْعَصْرِ إِنَّ الْإِنْسَانَ ...", "pilihan": ["لَفِي خُسْرٍ", "فِي جَنَّةٍ", "لَا يَمُوتُ", "فِي نَعِيمٍ"], "jawaban": "لَفِي خُسْرٍ"},
    {"soal": "Lanjutkan: قُلْ هُوَ اللَّهُ ...", "pilihan": ["أَحَدٌ", "الصَّمَدُ", "لَمْ يَلِدْ", "كُفُوًا"], "jawaban": "أَحَدٌ"},
    {"soal": "Lanjutkan: قُلْ أَعُوذُ بِرَبِّ ...", "pilihan": ["الْفَلَقِ", "النَّاسِ", "الْعَالَمِينَ", "الْفَاتِحَةِ"], "jawaban": "الْفَلَقِ"},
    {"soal": "Lanjutkan: إِنَّا أَعْطَيْنَاكَ ...", "pilihan": ["الْكَوْثَرَ", "الْفَلَقَ", "النَّاسَ", "الْعَصْرَ"], "jawaban": "الْكَوْثَرَ"},
    {"soal": "Lanjutkan: تَبَّتْ يَدَا أَبِي لَهَبٍ ...", "pilihan": ["وَتَبَّ", "وَمَا أَدْرَاكَ", "فِي جِيدِهَا", "سَيَصْلَى"], "jawaban": "وَتَبَّ"},
    {"soal": "Surat Al-Fatihah ada berapa ayat?", "pilihan": ["7", "5", "6", "8"], "jawaban": "7"},
    {"soal": "Lanjutkan: إِذَا جَاءَ نَصْرُ اللَّهِ ...", "pilihan": ["وَالْفَتْحُ", "وَالْعَصْرُ", "وَالْكَوْثَرُ", "وَالنَّاسُ"], "jawaban": "وَالْفَتْحُ"},
    {"soal": "Lanjutkan: وَالتِّينِ وَالزَّيْتُونِ ...", "pilihan": ["وَطُورِ سِينِينَ", "وَالْعَصْرِ", "وَالشَّمْسِ", "وَاللَّيْلِ"], "jawaban": "وَطُورِ سِينِينَ"},
]

def _key(nama, item):
    identitas = str(nama or "siswa").strip().lower().replace(" ", "_")
    return f"qori_game_{identitas}_{item}"

def _get(nama, item, default):
    k = _key(nama, item)
    if k not in st.session_state:
        st.session_state[k] = default
    return st.session_state[k]

def _set(nama, item, value):
    st.session_state[_key(nama, item)] = value

def _reset(nama):
    for item, value in {"posisi": 0, "poin": 0, "benar": 0, "salah": 0,
                        "soal": None, "dadu": 0, "selesai": False}.items():
        _set(nama, item, value)

def simpan_hasil_game(supabase, nama, mode, poin, benar, salah):
    try:
        supabase.table("hasil_game").insert({
            "nama": nama, "mode": mode, "poin": int(poin),
            "benar": int(benar), "salah": int(salah),
            "tanggal": datetime.now().strftime("%Y-%m-%d %H:%M")
        }).execute()
        return True
    except Exception as e:
        print(f"Gagal simpan hasil game: {e}")
        return False

def tampilkan_game_qori(supabase, nama_siswa):
    st.markdown("### 🎲 Game Petualangan QORI")
    st.write(f"Halo **{nama_siswa}**, kocok dadu, jalan, jawab soal! Sampai FINISH jadi Juara Qori!")
    mode = st.selectbox("Pilih Materi:",
        ["📖 Iqro - Mengenal Huruf", "🎙️ Tahsin - Tajwid", "🧠 Tahfidz - Hafalan"],
        key=_key(nama_siswa, "mode"))

    posisi, poin = _get(nama_siswa, "posisi", 0), _get(nama_siswa, "poin", 0)
    benar, salah = _get(nama_siswa, "benar", 0), _get(nama_siswa, "salah", 0)
    dadu, selesai = _get(nama_siswa, "dadu", 0), _get(nama_siswa, "selesai", False)
    soal = _get(nama_siswa, "soal", None)

    c1, c2, c3 = st.columns(3)
    c1.metric("📍 Posisi", f"{posisi} / 30")
    c2.metric("⭐ Poin", poin)
    c3.metric("🎲 Dadu", dadu or "-")
    st.progress(min(posisi / 30, 1.0))

    papan = ""
    for i in range(1, 31):
        papan += " 🧕 " if i == posisi else (" ❓ " if i % 5 == 0 else (" 🧩 " if i % 7 == 0 else f" {i} "))
        if i % 6 == 0:
            papan += "\\n"
    st.text(papan)
    st.caption("🧕 = Kamu | ❓ = Quiz | 🧩 = Puzzle")

    if selesai:
        st.balloons()
        st.success(f"🎉 MASYALLAH! {nama_siswa} FINISH! Poin: {poin} | Benar: {benar} | Salah: {salah}")
        if st.button("Main Lagi", key=_key(nama_siswa, "main_lagi")):
            _reset(nama_siswa)
            st.rerun()
        return

    if st.button("🎲 KOCOK DADU!", use_container_width=True, key=_key(nama_siswa, "kocok")):
        dadu = random.randint(1, 6)
        posisi += dadu
        _set(nama_siswa, "dadu", dadu)
        if posisi >= 30:
            posisi, poin = 30, poin + 50
            _set(nama_siswa, "posisi", posisi)
            _set(nama_siswa, "poin", poin)
            _set(nama_siswa, "selesai", True)
            simpan_hasil_game(supabase, nama_siswa, mode, poin, benar, salah)
            st.rerun()
        _set(nama_siswa, "posisi", posisi)
        if posisi % 5 == 0 or posisi % 7 == 0:
            bank = SOAL_IQRO if "Iqro" in mode else (SOAL_TAHSIN if "Tahsin" in mode else SOAL_TAHFIDZ)
            _set(nama_siswa, "soal", random.choice(bank))
        else:
            _set(nama_siswa, "soal", None)
            st.info(f"Jalan {dadu} langkah ke kotak {posisi}. Aman! Kocok lagi.")
        st.rerun()

    soal = _get(nama_siswa, "soal", None)
    if soal:
        st.markdown("---")
        st.markdown(f"### ❓ Tantangan Kotak {posisi}")
        st.markdown(f"**{soal['soal']}**")
        jawaban = st.radio("Pilih jawaban:", soal["pilihan"],
            key=_key(nama_siswa, f"pilihan_{posisi}_{dadu}"))
        if st.button("Jawab!", key=_key(nama_siswa, f"jawab_{posisi}_{dadu}")):
            if jawaban == soal["jawaban"]:
                _set(nama_siswa, "poin", _get(nama_siswa, "poin", 0) + 10)
                _set(nama_siswa, "benar", _get(nama_siswa, "benar", 0) + 1)
                _set(nama_siswa, "posisi", min(30, _get(nama_siswa, "posisi", 0) + 2))
                st.success("✅ BENAR! Maju 2 langkah + 10 Poin!")
            else:
                _set(nama_siswa, "salah", _get(nama_siswa, "salah", 0) + 1)
                _set(nama_siswa, "poin", max(0, _get(nama_siswa, "poin", 0) - 5))
                _set(nama_siswa, "posisi", max(0, _get(nama_siswa, "posisi", 0) - 2))
                st.error(f"❌ Jawabannya: {soal['jawaban']}. Mundur 2 langkah.")
            _set(nama_siswa, "soal", None)
            st.rerun()

    if st.button("🔄 Ulang dari Awal", key=_key(nama_siswa, "ulang")):
        _reset(nama_siswa)
        st.rerun()

def tampilkan_hasil_game(supabase):
    st.markdown("### 📊 Hasil Game QORI - Siswa")
    st.write("Tim hanya melihat hasil, tidak bisa memainkan game.")
    try:
        rows = supabase.table("hasil_game").select("*").order("id", desc=True).execute().data or []
    except Exception as e:
        st.warning(f"Tabel hasil_game belum tersedia atau tidak dapat dibaca. Error: {e}")
        return
    if not rows:
        st.info("Belum ada siswa yang main game.")
        return
    for row in rows:
        st.markdown(
            f"**{row.get('nama', '-')}** | {row.get('mode', '-')} | ⭐ {row.get('poin', 0)} Poin | "
            f"✅ {row.get('benar', 0)} Benar | ❌ {row.get('salah', 0)} Salah | {row.get('tanggal', '')}"
        )
        st.divider()
