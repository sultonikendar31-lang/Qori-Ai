import streamlit as st
import base64
from google import genai

st.set_page_config(page_title="QORI AI", page_icon="🕌", layout="wide")

api_key = st.secrets.get("GEMINI_API_KEY", "")

if "kategori_pilih" not in st.session_state:
    st.session_state["kategori_pilih"] = None
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "siswa_pilih" not in st.session_state:
    st.session_state["siswa_pilih"] = None

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
        border-radius: 20px !important;
    }}
    /* === REVISI: TULISAN SOAL JADI PUTIH BIAR KELIATAN === */
    .block-container p, .block-container span, .block-container label, .block-container h2, .block-container h3 {{
        color: white !important;
    }}
    [data-testid="stRadio"] label {{
        color: white !important;
        font-weight: 600 !important;
    }}
    [data-testid="stRadio"] div {{
        color: white !important;
    }}
    [data-testid="stRadio"] p {{
        color: white !important;
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

# ===== DATA 20 SISWA =====
DATA_SISWA = {
    "MUHAMAD HARTANTO": {"kategori": "Iqro", "level": "Iqro Dasar, nilai 63"},
    "DAFFAN OKTAFFIL HIDAYAT": {"kategori": "Iqro", "level": "Iqro Dasar, nilai 62"},
    "FRISCHA BUNGA LESTARI": {"kategori": "Tahsin", "level": "Tahsin, nilai 73"},
    "RABHAN": {"kategori": "Tahsin", "level": "Tahsin, nilai 72"},
    "ANGGA FADILLAH": {"kategori": "Tahsin", "level": "Tahsin, nilai 71"},
    "ANDY RAMADANI ABDULLAH": {"kategori": "Tahsin", "level": "Tahsin, nilai 76"},
    "ZALFATUSSYIFA RAMADANTI": {"kategori": "Tahfidz", "level": "Tahfidz, nilai 85"},
    "ZAIN RAHMANITA": {"kategori": "Tahfidz", "level": "Tahfidz, nilai 86"},
    "YUSUF IMAM MA'RUF": {"kategori": "Tahfidz", "level": "Tahfidz, nilai 85"},
    "FEBRIANSYAH RACHMAT HIDAYAT": {"kategori": "Tahfidz", "level": "Tahfidz, nilai 85"},
    "MUHAMMAD HAFIDZ": {"kategori": "Tahfidz", "level": "Tahfidz, nilai 89"},
    "ANGGI RATU MAHADEWI": {"kategori": "Tahfidz", "level": "Tahfidz, nilai 88"},
    "RIZQI RAMADHANY": {"kategori": "Tahfidz", "level": "Tahfidz, nilai 85"},
    "KAWI LUJENGAN RASYIDA RAIHANUN": {"kategori": "Tahfidz", "level": "Tahfidz, nilai 84"},
    "MIFTAHUL JANNAH": {"kategori": "Tahfidz", "level": "Tahfidz, nilai 81"},
    "MUHAMAD AZHAM FATAHILAH": {"kategori": "Tahfidz", "level": "Tahfidz, nilai 82"},
    "ROSMALATI KHOLISHA": {"kategori": "Tahfidz", "level": "Tahfidz, nilai 83"},
    "M. ARIF ZAKARIYA": {"kategori": "Tahfidz", "level": "Tahfidz, nilai 85"},
    "MOCHAMMAD ALKAHFI MUBAROK": {"kategori": "Tahfidz", "level": "Tahfidz, nilai 86"},
    "IMAM MANSYUR IBNU HULKAN": {"kategori": "Tahfidz", "level": "Tahfidz, nilai 80"},
}

KUNCI = {
    "Iqro": ["C","C","B","A","C","B","A","B","C","C","B","C","C","C","B","B","S","B","B","B","B","S","B","S","B"],
    "Tahsin": ["C","C","B","D","D","B","C","B","B","A","B","C","B","C","C","B","B","S","B","B","B","S","B","B","S"],
    "Tahfidz": ["C","B","C","A","C","B","C","C","C","B","B","B","C","C","B","B","B","S","B","B","B","S","B","B","B"]
}

SOAL_IQRO = [
("1. Jumlah huruf hijaiyah yang umum digunakan adalah ....", ["A. 26 huruf","B. 27 huruf","C. 28 huruf","D. 29 huruf","E. 30 huruf"]),
("2. Tanda baca fathah menghasilkan bunyi ....", ["A. i","B. u","C. a","D. an","E. in"]),
("3. Huruf hijaiyah diberi harakat kasrah, dibaca bunyi ....", ["A. A","B. I","C. U","D. An","E. Un"]),
("4. Tanwin fathah menghasilkan bunyi ....", ["A. An","B. In","C. Un","D. A","E. I"]),
("5. Tanda sukun menunjukkan huruf dibaca ....", ["A. Panjang","B. Berdengung","C. Mati / tidak berharakat","D. Tebal","E. Samar"]),
("6. Tanda tasydid menunjukkan huruf ....", ["A. Dibaca panjang 2 harakat","B. Dibaca rangkap / ditekan","C. Dibaca samar","D. Tidak dibaca","E. Dibaca pendek"]),
("7. Huruf mad yang terdiri atas alif, wau, dan ya adalah ....", ["A. ا، و، ي","B. ب، ت، ث","C. ج، ح، خ","D. د، ذ، ر","E. س، ش، ص"]),
("8. Huruf berharakat fathah diikuti alif, dibaca ....", ["A. Pendek 1 harakat","B. Panjang 2 harakat","C. Panjang 4 harakat","D. Dengung","E. Samar"]),
("9. Kemampuan mengenali dan mengucapkan huruf sesuai tempat keluarnya disebut ....", ["A. Tafsir","B. Tarjamah","C. Makharijul huruf","D. Tadabbur","E. Tahfidz"]),
("10. Tanda waqaf مـ menunjukkan ....", ["A. Boleh berhenti","B. Lebih baik melanjutkan","C. Harus berhenti","D. Dilarang berhenti","E. Berhenti sejenak tanpa napas"]),
("11. Salah satu tujuan mempelajari metode Iqro' adalah ....", ["A. Menghafal seluruh hadis","B. Membaca Al-Qur'an secara bertahap dan benar","C. Mempelajari sejarah Islam","D. Menguasai ilmu tafsir","E. Mempelajari ilmu fikih"]),
("12. Membaca huruf hijaiyah dengan mengubah bunyi karena salah makhraj, akibatnya ....", ["A. Bacaan semakin indah","B. Tidak memengaruhi bacaan","C. Dapat mengubah bunyi dan berpotensi mengubah makna","D. Bacaan menjadi lebih cepat","E. Tidak perlu diperbaiki"]),
("13. Membaca Al-Qur'an secara tartil berarti ....", ["A. Membaca sangat cepat","B. Membaca tanpa tajwid","C. Membaca perlahan, jelas, sesuai kaidah","D. Membaca dengan suara keras","E. Membaca tanpa berhenti"]),
("14. Tanda baca dhammah menghasilkan bunyi ....", ["A. A","B. I","C. U","D. An","E. In"]),
("15. Sikap yang tepat ketika menemukan kesalahan membaca Al-Qur'an adalah ....", ["A. Membiarkannya","B. Mengulangi dan memperbaiki bacaan","C. Mempercepat bacaan","D. Menghindari membaca","E. Mengabaikan koreksi guru"]),
("16. Huruf hijaiyah merupakan huruf yang digunakan untuk menulis bahasa Arab.", ["B - Benar","S - Salah"]),
("17. Harakat fathah menghasilkan bunyi i.", ["B - Benar","S - Salah"]),
("18. Tanwin terdiri atas fathatain, kasratain, dan dhammatain.", ["B - Benar","S - Salah"]),
("19. Tanda sukun menunjukkan bahwa huruf tidak memiliki harakat.", ["B - Benar","S - Salah"]),
("20. Tasydid menunjukkan bahwa huruf dibaca rangkap.", ["B - Benar","S - Salah"]),
("21. Huruf mad terdiri atas alif, wau, dan ya dengan ketentuan tertentu.", ["B - Benar","S - Salah"]),
("22. Membaca Al-Qur'an dengan tartil berarti membaca secepat mungkin.", ["B - Benar","S - Salah"]),
("23. Kesalahan pengucapan makharijul huruf dapat memengaruhi ketepatan bacaan.", ["B - Benar","S - Salah"]),
("24. Belajar membaca Al-Qur'an tidak membutuhkan bimbingan guru.", ["B - Benar","S - Salah"]),
("25. Membiasakan membaca Al-Qur'an secara rutin dapat meningkatkan kelancaran membaca.", ["B - Benar","S - Salah"]),
]

SOAL_TAHSIN = [
("1. Secara umum, makharijul huruf terbagi menjadi ....", ["A. 3 tempat","B. 4 tempat","C. 5 tempat","D. 6 tempat","E. 7 tempat"]),
("2. Hukum nun sukun / tanwin bertemu huruf ب adalah ....", ["A. Idzhar","B. Idgham bighunnah","C. Iqlab","D. Ikhfa haqiqi","E. Idgham bilaghunnah"]),
("3. Huruf-huruf idgham bighunnah adalah ....", ["A. ل dan ر","B. ي، ن، م، و","C. ء، ه، ع، ح، غ، خ","D. ب، ج، د، ط","E. ص، ض، ط، ظ"]),
("4. Hukum nun sukun / tanwin bertemu huruf ل adalah ....", ["A. Idzhar","B. Iqlab","C. Ikhfa","D. Idgham bilaghunnah","E. Idgham bighunnah"]),
("5. Jumlah huruf ikhfa haqiqi adalah ....", ["A. 6 huruf","B. 10 huruf","C. 12 huruf","D. 15 huruf","E. 17 huruf"]),
("6. Hukum mim sukun bertemu huruf ب disebut ....", ["A. Idzhar syafawi","B. Ikhfa syafawi","C. Idgham mimi","D. Iqlab","E. Idgham bilaghunnah"]),
("7. Mim sukun bertemu mim, hukumnya ....", ["A. Ikhfa syafawi","B. Idzhar syafawi","C. Idgham mimi","D. Iqlab","E. Idzhar halqi"]),
("8. Bacaan qalqalah terjadi pada huruf ....", ["A. ا، و، ي","B. ق، ط، ب، ج، د","C. س، ش، ص","D. ل، ر، ن","E. م، ن، و"]),
("9. Panjang bacaan mad thabi'i adalah ....", ["A. 1 harakat","B. 2 harakat","C. 3 harakat","D. 4 harakat","E. 6 harakat"]),
("10. Mad wajib muttasil terjadi apabila ....", ["A. Huruf mad bertemu hamzah dalam satu kata","B. Huruf mad bertemu sukun asli","C. Huruf mad bertemu tasydid","D. Huruf mad bertemu qalqalah","E. Huruf mad di awal kalimat"]),
("11. Mad jaiz munfasil terjadi apabila ....", ["A. Huruf mad bertemu hamzah dalam satu kata","B. Huruf mad di akhir kata bertemu hamzah di awal kata berikutnya","C. Huruf mad bertemu tasydid","D. Huruf mad bertemu sukun asli","E. Huruf mad bertemu qalqalah"]),
("12. Ghunnah secara istilah berarti ....", ["A. Bacaan memantul","B. Bacaan samar","C. Bacaan dengung","D. Bacaan panjang","E. Bacaan pendek"]),
("13. Huruf ra (ر) dibaca tafkhim apabila ....", ["A. Berharakat kasrah","B. Berharakat fathah atau dhammah","C. Selalu didahului kasrah","D. Berada di akhir kata saja","E. Tidak memiliki harakat"]),
("14. Tujuan mempelajari ilmu tajwid adalah ....", ["A. Mempercepat bacaan","B. Memperindah suara tanpa makhraj","C. Menjaga bacaan agar sesuai kaidah yang benar","D. Menghafal seluruh ayat","E. Mengubah cara membaca sesuai keinginan"]),
("15. Berhenti pada tempat yang tidak tepat sehingga merusak makna ayat, berkaitan dengan ....", ["A. Makharijul huruf","B. Sifat huruf","C. Waqaf dan ibtida'","D. Ghunnah","E. Qalqalah"]),
("16. Ilmu tajwid mempelajari cara membaca Al-Qur'an dengan benar sesuai makhraj dan sifat huruf.", ["B - Benar","S - Salah"]),
("17. Hukum iqlab terjadi apabila nun sukun / tanwin bertemu huruf ب.", ["B - Benar","S - Salah"]),
("18. Idgham bilaghunnah dibaca dengan dengung.", ["B - Benar","S - Salah"]),
("19. Huruf idzhar halqi berjumlah enam.", ["B - Benar","S - Salah"]),
("20. Ikhfa syafawi terjadi apabila mim sukun bertemu huruf ب.", ["B - Benar","S - Salah"]),
("21. Mad thabi'i dibaca sepanjang dua harakat.", ["B - Benar","S - Salah"]),
("22. Qalqalah hanya berlaku pada huruf alif, wau, dan ya.", ["B - Benar","S - Salah"]),
("23. Ghunnah merupakan suara dengung yang keluar melalui rongga hidung.", ["B - Benar","S - Salah"]),
("24. Membaca Al-Qur'an dengan tajwid yang benar membantu menjaga ketepatan pelafalan ayat.", ["B - Benar","S - Salah"]),
("25. Semua huruf ra dalam Al-Qur'an harus selalu dibaca tebal.", ["B - Benar","S - Salah"]),
]

SOAL_TAHFIDZ = [
("1. Tahfidz berasal dari kata hafizha yang artinya ....", ["A. Membaca","B. Menulis","C. Menjaga / memelihara","D. Mendengarkan","E. Memahami"]),
("2. Tujuan utama pembelajaran tahfidz adalah ....", ["A. Menghafal tanpa memahami adab","B. Menghafal ayat dan menjaga hafalannya","C. Membaca dengan cepat","D. Menguasai bahasa Arab saja","E. Menghafal terjemahan saja"]),
("3. Mengulang hafalan agar tidak mudah lupa disebut ....", ["A. Tafsir","B. Tadabbur","C. Muraja'ah","D. Tarjamah","E. Tilawah"]),
("4. Menghafal dengan mendengarkan bacaan guru / rekaman berulang disebut ....", ["A. Metode sima'i","B. Metode kitabah","C. Metode diskusi","D. Metode ceramah","E. Metode demonstrasi"]),
("5. Faktor penting keberhasilan menghafal adalah ....", ["A. Menghafal hanya ketika ujian","B. Menghafal tanpa jadwal","C. Konsistensi dan kedisiplinan","D. Menghafal sebanyak mungkin sekaligus","E. Tidak melakukan pengulangan"]),
("6. Surah Al-Ikhlas terdiri atas ....", ["A. 3 ayat","B. 4 ayat","C. 5 ayat","D. 6 ayat","E. 7 ayat"]),
("7. Surah yang menjelaskan keesaan Allah adalah ....", ["A. Al-Falaq","B. An-Nas","C. Al-Ikhlas","D. Al-Ma'un","E. Al-Kautsar"]),
("8. Surah Al-Falaq terdiri atas ....", ["A. 3 ayat","B. 4 ayat","C. 5 ayat","D. 6 ayat","E. 7 ayat"]),
("9. Surah An-Nas mengajarkan memohon perlindungan kepada ....", ["A. Malaikat","B. Nabi","C. Allah Swt.","D. Manusia","E. Jin"]),
("10. Surah Al-Kautsar terdiri atas ....", ["A. 2 ayat","B. 3 ayat","C. 4 ayat","D. 5 ayat","E. 6 ayat"]),
("11. Surah Al-'Asr menjelaskan pentingnya ....", ["A. Kekayaan dan jabatan","B. Waktu, keimanan, amal saleh, nasihat kebenaran & kesabaran","C. Perdagangan","D. Kekuatan fisik","E. Kedudukan sosial"]),
("12. Surah Al-Ma'un memberikan pelajaran tentang ....", ["A. Pentingnya kesombongan","B. Kepedulian terhadap anak yatim dan orang miskin","C. Keutamaan kekayaan","D. Larangan bekerja","E. Pentingnya kedudukan"]),
("13. Salah satu adab menghafal Al-Qur'an adalah ....", ["A. Menghafal sambil bercanda","B. Tidak memperhatikan kebersihan","C. Menjaga niat, kesungguhan, menghormati Al-Qur'an","D. Mengabaikan koreksi guru","E. Menghafal hanya untuk dipuji"]),
("14. Ketika kesulitan menghafal suatu ayat, langkah yang tepat adalah ....", ["A. Menghentikan hafalan","B. Menghafal ayat lain","C. Membaca berulang, mendengarkan contoh, minta bimbingan guru","D. Mengabaikan ayat tersebut","E. Menunggu sampai ujian"]),
("15. Hubungan tahsin dan tahfidz adalah ....", ["A. Tidak ada hubungan","B. Tahsin membantu menjaga ketepatan bacaan dalam menghafal","C. Tahfidz tidak butuh tajwid","D. Tahsin hanya untuk yang belum bisa baca","E. Tahfidz hanya utamakan kecepatan"]),
("16. Tahfidz merupakan kegiatan menghafalkan ayat-ayat Al-Qur'an.", ["B - Benar","S - Salah"]),
("17. Muraja'ah adalah mengulang hafalan yang sudah dipelajari.", ["B - Benar","S - Salah"]),
("18. Menghafal Al-Qur'an cukup dilakukan satu kali tanpa pengulangan.", ["B - Benar","S - Salah"]),
("19. Surah Al-Ikhlas terdiri atas empat ayat.", ["B - Benar","S - Salah"]),
("20. Surah Al-Kautsar terdiri atas tiga ayat.", ["B - Benar","S - Salah"]),
("21. Surah Al-'Asr menjelaskan manusia dalam kerugian kecuali yang beriman, beramal saleh, saling menasihati kebenaran & kesabaran.", ["B - Benar","S - Salah"]),
("22. Menghafal Al-Qur'an harus mengutamakan kuantitas tanpa ketepatan bacaan.", ["B - Benar","S - Salah"]),
("23. Mendengarkan bacaan Al-Qur'an dapat membantu proses menghafal.", ["B - Benar","S - Salah"]),
("24. Menjaga hafalan membutuhkan kedisiplinan dan muraja'ah rutin.", ["B - Benar","S - Salah"]),
("25. Menghafal Al-Qur'an sebaiknya dengan niat ikhlas karena Allah Swt.", ["B - Benar","S - Salah"]),
]

SOAL_ALL = {"Iqro": SOAL_IQRO, "Tahsin": SOAL_TAHSIN, "Tahfidz": SOAL_TAHFIDZ}

def tampilkan_daftar(kategori):
    if kategori == "Iqro":
        daftar = ["MUHAMAD HARTANTO", "DAFFAN OKTAFFIL HIDAYAT"]
    elif kategori == "Tahsin":
        daftar = ["FRISCHA BUNGA LESTARI", "RABHAN", "ANGGA FADILLAH", "ANDY RAMADANI ABDULLAH"]
    else:
        daftar = ["ZALFATUSSYIFA RAMADANTI", "ZAIN RAHMANITA", "YUSUF IMAM MA'RUF", "FEBRIANSYAH RACHMAT HIDAYAT", "MUHAMMAD HAFIDZ", "ANGGI RATU MAHADEWI", "RIZQI RAMADHANY", "KAWI LUJENGAN RASYIDA RAIHANUN", "MIFTAHUL JANNAH", "MUHAMAD AZHAM FATAHILAH", "ROSMALATI KHOLISHA", "M. ARIF ZAKARIYA", "MOCHAMMAD ALKAHFI MUBAROK", "IMAM MANSYUR IBNU HULKAN"]
    for item in daftar:
        if st.button(item, key=f"{kategori}-{item}"):
            st.session_state["siswa_pilih"] = item
            st.rerun()

cari = st.text_input("🔍 Ketik nama siswa...", placeholder="Contoh: MUHAMAD HARTANTO")
if cari:
    cari_besar = cari.upper().strip()
    for nama_siswa in DATA_SISWA.keys():
        if cari_besar in nama_siswa:
            st.session_state["siswa_pilih"] = nama_siswa
            st.rerun()

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
            tampilkan_daftar("Iqro")
    if st.session_state["kategori_pilih"] == "Tahsin":
        with c2:
            tampilkan_daftar("Tahsin")
    if st.session_state["kategori_pilih"] == "Tahfidz":
        with c3:
            tampilkan_daftar("Tahfidz")

# ===== HALAMAN SOAL - SUDAH PUTIH =====
if st.session_state["siswa_pilih"]:
    nama = st.session_state["siswa_pilih"]
    info = DATA_SISWA.get(nama, {"kategori": "Iqro", "level": "Pemula"})
    kat = info["kategori"]
    st.markdown(f"<div style='background-color: rgba(20,50,35,0.92); padding:20px; border-radius:15px; text-align:center;'><h2 style='color:#F9D423; margin:0;'>Assalamualaikum, {nama} 👋</h2><p style='color:white;'>Kelas: {kat} | Level: {info['level']} | Soal: 25 Soal (15 PG + 10 Benar/Salah) | Nilai: Benar x 4</p></div>", unsafe_allow_html=True)
    if st.button("⬅️ Kembali ke Daftar Nama"):
        st.session_state["siswa_pilih"] = None
        st.rerun()
    soal_list = SOAL_ALL[kat]
    kunci = KUNCI[kat]
    st.markdown(f"<h2 style='color:white; background-color: rgba(0,0,0,0.65); padding:10px; border-radius:10px; text-align:center;'>📝 Soal {kat} - Kelas XI MA</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:white; background-color: rgba(0,0,0,0.65); padding:8px; border-radius:10px; text-align:center;'>Jawab semua soal, lalu klik LIHAT NILAI di bawah.</p>", unsafe_allow_html=True)
    jawaban_siswa = []
    for i, (soal, opsi) in enumerate(soal_list):
        st.markdown(f"<div style='background-color: rgba(0,0,0,0.65); padding:12px; border-radius:10px; margin-bottom:5px;'><p style='color:white; font-weight:bold; font-size:17px; margin:0;'>{soal}</p></div>", unsafe_allow_html=True)
        pilih = st.radio(f"Pilih jawaban No.{i+1}", opsi, key=f"soal_{kat}_{i}", index=None)
        jawaban_siswa.append(pilih)
    if st.button("✅ LIHAT NILAI SAYA", use_container_width=True):
        benar = 0
        for i, pilih in enumerate(jawaban_siswa):
            if pilih and pilih[0] == kunci[i]:
                benar += 1
        nilai = (benar / 25) * 100
        st.success(f"🎉 HASIL {nama} - Kelas {kat}")
        st.markdown(f"<div style='background-color: rgba(0,0,0,0.65); padding:15px; border-radius:10px; text-align:center;'><h1 style='color:#F9D423;'>Nilai: {int(nilai)}</h1><p style='color:white;'>Jawaban Benar: {benar} / 25 | Salah / Kosong: {25-benar}</p><p style='color:white;'>Perhitungan: ({benar} ÷ 25) × 100 = {int(nilai)}</p></div>", unsafe_allow_html=True)
        if nilai == 100:
            st.balloons()
            st.markdown("<p style='color:white;'>MasyaAllah Sempurna! 🌟 Pertahankan ya!</p>", unsafe_allow_html=True)
        elif nilai >= 80:
            st.markdown("<p style='color:white;'>Bagus Sekali! Sedikit lagi sempurna. Semangat Muraja'ah! 💪</p>", unsafe_allow_html=True)
        elif nilai >= 60:
            st.markdown("<p style='color:white;'>Sudah Bagus! Ayo ulangi yang salah, kamu pasti bisa! 📖</p>", unsafe_allow_html=True)
        else:
            st.markdown("<p style='color:white;'>Jangan menyerah! Ayo belajar lagi bersama QORI AI, kamu pasti bisa! 🤲</p>", unsafe_allow_html=True)
        st.markdown("<div style='background-color: rgba(0,0,0,0.65); padding:10px; border-radius:10px;'><p style='color:white; font-weight:bold;'>Pembahasan Kunci Jawaban:</p></div>", unsafe_allow_html=True)
        for i in range(25):
            st.markdown(f"<p style='color:white;'>No.{i+1} = {kunci[i]}</p>", unsafe_allow_html=True)
    st.stop()

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
