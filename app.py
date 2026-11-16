import streamlit as st

st.set_page_config(page_title="QORI AI - MA Al-Barokah", page_icon="📖")
st.title("📖 QORI AI - MA Al-Barokah Kelas 11")
st.write("Asisten Pengajian Digital: Iqro, Tahsin, Tahfidz")

DAFTAR_SISWA = {
    "FRISCHA BUNGA LESTARI": "Tahsin",
    "ZALFATUSSYIFA RAMADANTI": "Tahfidz",
    "ZAIN RAHMANITA": "Tahfidz",
    "YUSUF IMAM MA'RUF": "Tahfidz",
    "RAIHAN": "Tahsin",
    "FEBRIANSYAH RACHMAT HIDAYAT": "Tahfidz",
    "ANGGA FADILLAH": "Tahsin",
    "MUHAMMAD HAFIDZ": "Tahfidz",
    "ANDY RAMADANI ABDULLAH": "Tahsin",
    "ANGGI RATU MAHADEWI": "Tahfidz",
    "RIZQI RAMADHANY": "Tahfidz",
    "KAWILUJEUNGAN RASYIDA RAIHANUN": "Tahfidz",
    "MIFTAHUL JANNAH": "Tahfidz",
    "MUHAMAD AZHAM FATAHILAH": "Tahfidz",
    "ROSMALATI KHOLISHA": "Tahfidz",
    "M. ARIF ZAKARIYA": "Tahfidz",
    "MOCHAMMAD ALKAHFI MUBAROK": "Tahfidz",
    "MUHAMAD HARTANTO": "Iqro Dasar",
    "IMAM MANSYUR IBNU HULKARIM": "Tahfidz",
    "DAFFAN OKTAFFIL HIDAYAT": "Iqro",
}
DAFTAR_DEWASA = {
    "KENDAR SULTONI": "Mahasiswa / Admin Utama",
    "MUHAMMAD SIDDIQ ASYHARI": "Dosen Pembimbing",
    "SYAMSUL HADI": "Kepala MA Al-Barokah",
    "ADE ROMLI": "Guru Al-Qur'an Hadits",
    "MUHAMAD RAIS": "Guru Bahasa Arab",
}

if "step" not in st.session_state:
    st.session_state.step = "salam"
    st.session_state.nama = ""
    st.session_state.role = ""

# LANGKAH 0 - SALAM
if st.session_state.step == "salam":
    st.info("Waalaikumsalam warahmatullahi wabarakatuh 👋")
    st.write("Sebelum mulai, biasakan salam lengkap dulu ya.")
    salam = st.text_input("Ketik salam lengkap kamu:")
    if st.button("Kirim Salam"):
        if "assalamualaikum warahmatullahi wabarakatuh" in salam.lower():
            st.session_state.step = "nama"
            st.rerun()
        else:
            st.warning("Yuk sempurnakan: Assalamualaikum warahmatullahi wabarakatuh")

# LANGKAH 1 - NAMA
elif st.session_state.step == "nama":
    st.success("Barakallah, salam kamu sudah lengkap!")
    nama = st.text_input("Nama lengkap kamu siapa sesuai absen?")
    if st.button("Masuk"):
        nama_bersih = " ".join(nama.strip().upper().split())
        if nama_bersih in DAFTAR_DEWASA:
            st.session_state.nama = nama_bersih
            st.session_state.role = "DEWASA"
            st.session_state.step = "belajar"
            st.rerun()
        elif nama_bersih in DAFTAR_SISWA:
            st.session_state.nama = nama_bersih
            st.session_state.role = "SISWA"
            st.session_state.step = "belajar"
            st.rerun()
        else:
            st.error("Maaf, nama kamu tidak terdaftar di Kelas 11 MA Al-Barokah. Silakan hubungi Kendar Sultoni. Wassalamualaikum warahmatullahi wabarakatuh")

# LANGKAH 2 - BELAJAR
elif st.session_state.step == "belajar":
    nama = st.session_state.nama
    if st.session_state.role == "DEWASA":
        st.success(f"Selamat datang Bapak {nama}, {DAFTAR_DEWASA[nama]}. Mau cek rekap 20 siswa hari ini?")
        st.write("**Daftar 20 Siswa Kelas 11:**")
        for s, m in DAFTAR_SISWA.items():
            st.write(f"- {s} - {m}")
    else:
        mode = DAFTAR_SISWA[nama]
        st.success(f"Selamat belajar {nama}, Mode kamu: {mode} 💪")
        st.write(f"Mode terkunci: **{mode}** - Kamu hanya bisa belajar di mode ini.")
        pilihan = st.selectbox("Mau belajar apa?", ["Pilih...", "Iqro", "Tahsin", "Tahfidz"])
        pertanyaan = st.text_input("Tulis ayat / huruf yang mau dikoreksi:")
        if st.button("Tanya Qori AI"):
            if pilihan == "Pilih...":
                st.warning("Pilih dulu modenya ya.")
            else:
                st.info(f"MasyaAllah bagus {nama}. Yuk kita perbaiki sama-sama di mode {pilihan}. Coba baca lagi 3x dengan pelan, perhatikan makhrojnya. Semangat murojaahnya ya!")
    st.write("---")
    st.write("Semoga bermanfaat. Wassalamualaikum warahmatullahi wabarakatuh")
    if st.button("Keluar / Ganti Nama"):
        st.session_state.clear()
        st.rerun()