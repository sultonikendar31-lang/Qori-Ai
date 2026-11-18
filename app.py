import streamlit as st
import streamlit.components.v1 as components
import base64
import random
import time
from openai import OpenAI

st.set_page_config(page_title="QORI AI", page_icon="🕌", layout="wide")

api_key = st.secrets.get("OPENAI_API_KEY", "")

if "kategori_pilih" not in st.session_state:
    st.session_state["kategori_pilih"] = None
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "siswa_pilih" not in st.session_state:
    st.session_state["siswa_pilih"] = None
if "seed_acak" not in st.session_state:
    st.session_state["seed_acak"] = 1
if "soal_acak" not in st.session_state:
    st.session_state["soal_acak"] = None
if "kunci_acak" not in st.session_state:
    st.session_state["kunci_acak"] = None
if "kat_acak" not in st.session_state:
    st.session_state["kat_acak"] = None
if "waktu_mulai" not in st.session_state:
    st.session_state["waktu_mulai"] = None
if "waktu_habis" not in st.session_state:
    st.session_state["waktu_habis"] = False
if "ujian_selesai" not in st.session_state:
    st.session_state["ujian_selesai"] = False
if "hasil_ujian" not in st.session_state:
    st.session_state["hasil_ujian"] = None
if "curang_refresh" not in st.session_state:
    st.session_state["curang_refresh"] = None
if "lihat_nilai" not in st.session_state:
    st.session_state["lihat_nilai"] = False
if "hasil_semua" not in st.session_state:
    st.session_state["hasil_semua"] = {}
if "hitung_ulang" not in st.session_state:
    st.session_state["hitung_ulang"] = {}

DURASI_UJIAN = 10 * 60
KKM = 75
prompt_awal = None

try:
    qp = st.query_params
    status_ujian_url = qp.get("ujian", "")
    nama_url = qp.get("nama", "")
    if status_ujian_url == "jalan" and st.session_state["siswa_pilih"] is None and st.session_state["curang_refresh"] is None:
        st.session_state["curang_refresh"] = nama_url if nama_url else "SISWA"
except:
    pass

SYSTEM_PROMPT_KUNCI = """
Kamu adalah QORI AI, guru ngaji yang ramah untuk anak Madrasah Aliyah Al-Barokah.
Kamu HANYA boleh menjawab tentang 3 topik ini:
1. IQRO - belajar membaca Al-Qur'an pemula, huruf hijaiyah, harakat, Iqro 1-6
2. TAHSIN - memperbaiki bacaan, makhraj, tajwid, sifat huruf, ghunnah, qalqalah, mad, waqaf, ibtida', hukum bacaan
3. TAHFIDZ - menghafal Al-Qur'an, muraja'ah, metode menghafal, surah-surah hafalan, Juz 30, Juz 29, adab menghafal. Semua nama surah termasuk Tahfidz, contoh: An-Naba, An-Naziat, Abasa, Al-Ikhlas, dll.
ATURAN KUNCI - WAJIB DIPATUHI:
- Jika pertanyaan di luar 3 topik di atas (misal: shalat, puasa, zakat, fikih, matematika, game, pacaran, politik, dll), kamu WAJIB menolak.
- Jawaban penolakan: "Maaf, saya QORI AI hanya bisa membantu tentang Iqro, Tahsin, dan Tahfidz saja. Silakan tanya seputar membaca dan menghafal Al-Qur'an ya! 🕌"
- Jawab dengan Bahasa Indonesia yang mudah, sopan, dan islami.
ATURAN TAMPILAN HURUF HIJAIYAH - WAJIB:
- Setiap menyebut huruf hijaiyah, WAJIB pakai format: 1. Alif (ا) - dibaca "A"
- JANGAN PERNAH tulis huruf Arab saja tanpa nama Latin dan cara bacanya.
- JANGAN tulis huruf Arab berderet-deret seperti "ا ب ت ث".
"""

HIJAIYAH_IQRO1 = [
    ("1", "Alif", "ا", "A"),("2", "Ba", "ب", "Ba"),("3", "Ta", "ت", "Ta"),("4", "Tsa", "ث", "Tsa"),
    ("5", "Jim", "ج", "Ja"),("6", "Ha", "ح", "Ha"),("7", "Kha", "خ", "Kha"),("8", "Dal", "د", "Da"),
    ("9", "Dzal", "ذ", "Dza"),("10", "Ra", "ر", "Ra"),("11", "Zai", "ز", "Za"),("12", "Sin", "س", "Sa"),
    ("13", "Syin", "ش", "Sya"),("14", "Shad", "ص", "Sha"),("15", "Dhad", "ض", "Dha"),("16", "Tha", "ط", "Tha"),
    ("17", "Zha", "ظ", "Zha"),("18", "Ain", "ع", "A"),("19", "Ghain", "غ", "Gha"),("20", "Fa", "ف", "Fa"),
    ("21", "Qaf", "ق", "Qa"),("22", "Kaf", "ك", "Ka"),("23", "Lam", "ل", "La"),("24", "Mim", "م", "Ma"),
    ("25", "Nun", "ن", "Na"),("26", "Wau", "و", "Wa"),("27", "Ha", "ه", "Ha"),("28", "Hamzah / Ya", "ء / ي", "A / Ya"),
]
def jawaban_hijaiyah_iqro1():
    teks = "Baik, mari kita belajar Iqro 1. Di Iqro 1 kita belajar huruf hijaiyah dasar. Bacalah satu per satu ya:\n\n"
    for no, nama, arab, baca in HIJAIYAH_IQRO1:
        teks += f"**{no}. {nama} ({arab}) - dibaca \"{baca}\"**\n\n"
    teks += "Coba ulangi lagi dari nomor 1 sampai 28. Kalau sudah hafal, bilang saja \"Lanjut Iqro 1 pakai harakat\" ya! 📖"
    return teks

def jawaban_mad_thobii():
    return """**Hukum Bacaan Mad Thobi'i - Tahsin** 📖
**1. Apa itu Mad Thobi'i?** Mad asli / mad dasar. Dibaca panjang secara alami.
**2. Berapa Panjangnya?** **2 harakat** (2 ketukan).
**3. Huruf Mad-nya Ada 3:**
**1. Alif (ا)** - setelah Fathah. Contoh: Ba (بَا) - dibaca "Baa"
**2. Wau (و)** - setelah Dhammah. Contoh: Bu (بُو) - dibaca "Buu"
**3. Ya (ي)** - setelah Kasrah. Contoh: Bi (بِي) - dibaca "Bii"
Ayo coba baca: **بَا - بُو - بِي** dibaca "Baa - Buu - Bii" ✅"""

def jawaban_an_naba():
    return """**Surat An-Naba - Tahfidz (Juz 30)** ⭐
**1. Identitas Surat:**
**1. Nama:** An-Naba (النبأ) artinya "Berita Besar"
**2. Nomor Surat:** Surat ke-78
**3. Jumlah Ayat:** 40 ayat
**4. Juz:** Juz 30 / Juz Amma
**5. Golongan:** Makkiyah
**2. Isi Pokok:** Tentang hari kiamat, bukti kekuasaan Allah, balasan neraka & surga.
**3. Tips Menghafal:** Bagi 3 bagian: Ayat 1-16, 17-30, 31-40. Hafal 5 ayat per hari, muraja'ah tiap pagi.
Mau lanjut hafalan ayat 1-5 dulu? Bilang saja "Hafal An-Naba ayat 1-5" ya! 🤲"""

KATA_TERLARANG = [
    "shalat", "sholat", "puasa", "zakat", "haji", "umroh", "fikih", "fiqih",
    "matematika", "fisika", "kimia", "biologi", "sejarah", "geografi",
    "game", "free fire", "ff", "mobile legend", "mlbb", "pubg", "roblox", "minecraft",
    "pacaran", "pacar", "politik", "presiden", "pemilu",
    "sepak bola", "bola", "musik", "lagu", "kpop",
    "resep", "masak", "bisnis", "crypto", "bitcoin"
]
def cek_dilarang(teks):
    t = teks.lower()
    for k in KATA_TERLARANG:
        if k in t:
            return True
    return False

PESAN_TOLAK = "Maaf, saya QORI AI hanya bisa membantu tentang Iqro, Tahsin, dan Tahfidz saja. Silakan tanya seputar membaca dan menghafal Al-Qur'an ya! 🕌"

def get_base64(file):
    try:
        with open(file, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return ""

def tampilkan_tim_pembuat():
    st.markdown("""
    <div style='background-color: rgba(255,255,255,0.12); border: 1.5px solid rgba(255,255,255,0.6); padding: 16px; border-radius: 15px; margin-top: 10px;'>
        <p style='color:#F9D423; font-weight:bold; font-size:18px; text-align:center; margin:0 0 12px 0;'>👨‍🎓 Tim Penyusun QORI AI</p>
        <div style='display:flex; flex-wrap:wrap; justify-content:center; gap:10px;'>
            <div style='background-color: rgba(0,0,0,0.55); padding:10px 14px; border-radius:10px; text-align:center; min-width:160px;'>
                <p style='color:#F9D423; font-weight:bold; margin:0; font-size:15px;'>Kendar Sultoni</p>
                <p style='color:white; margin:2px 0 0 0; font-size:13px;'>Mahasiswa / Pembuat Aplikasi</p>
            </div>
            <div style='background-color: rgba(0,0,0,0.55); padding:10px 14px; border-radius:10px; text-align:center; min-width:160px;'>
                <p style='color:#F9D423; font-weight:bold; margin:0; font-size:15px;'>Muhamad Siddiq Asyhari</p>
                <p style='color:white; margin:2px 0 0 0; font-size:13px;'>Dosen Pembimbing</p>
            </div>
            <div style='background-color: rgba(0,0,0,0.55); padding:10px 14px; border-radius:10px; text-align:center; min-width:160px;'>
                <p style='color:#F9D423; font-weight:bold; margin:0; font-size:15px;'>Syamsul Hadi</p>
                <p style='color:white; margin:2px 0 0 0; font-size:13px;'>Kepala MA Al-Barokah</p>
            </div>
            <div style='background-color: rgba(0,0,0,0.55); padding:10px 14px; border-radius:10px; text-align:center; min-width:160px;'>
                <p style='color:#F9D423; font-weight:bold; margin:0; font-size:15px;'>Muhamad Rais</p>
                <p style='color:white; margin:2px 0 0 0; font-size:13px;'>Guru Pamong</p>
            </div>
        </div>
        <p style='color:white; text-align:center; font-size:12px; margin:10px 0 0 0;'>QORI AI - Madrasah Aliyah Al-Barokah | Media Belajar Iqro, Tahsin & Tahfidz</p>
    </div>
    """, unsafe_allow_html=True)

def tampilkan_timer(sisa_detik):
    if sisa_detik < 0:
        sisa_detik = 0
    menit = int(sisa_detik // 60)
    detik = int(sisa_detik % 60)
    warna = "#F9D423"
    if sisa_detik <= 60:
        warna = "#FF5252"
    timer_html = f"""
    <div style="position:sticky; top:0; z-index:999; background:#0A2319; border:3px solid {warna}; border-radius:15px; padding:12px; text-align:center; margin-bottom:15px;">
        <div style="color:white; font-size:16px; font-weight:bold;">⏰ SISA WAKTU MENGERJAKAN</div>
        <div id="timer-qori" style="color:{warna}; font-size:48px; font-weight:bold; line-height:1.1;">{menit:02d}:{detik:02d}</div>
        <div id="pesan-timer" style="color:white; font-size:14px;">25 Soal - 10 Menit - Semangat! 💪</div>
    </div>
    <script>
    let sisa = {int(sisa_detik)};
    let sudahBunyi = {{}};
    window.onbeforeunload = function() {{ return "Yakin mau keluar? Nilai ujian akan jadi 0!"; }};
    function bunyiTit(panjang) {{
        try {{
            let ctx = new (window.AudioContext || window.webkitAudioContext)();
            let osc = ctx.createOscillator();
            let gain = ctx.createGain();
            osc.connect(gain); gain.connect(ctx.destination);
            osc.frequency.value = 880;
            osc.type = 'sine';
            gain.gain.setValueAtTime(0.5, ctx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + panjang);
            osc.start(); osc.stop(ctx.currentTime + panjang);
        }} catch(e) {{}}
    }}
    function updateTimer() {{
        let m = Math.floor(sisa / 60);
        let d = sisa % 60;
        let el = document.getElementById('timer-qori');
        if (el) el.textContent = String(m).padStart(2,'0') + ':' + String(d).padStart(2,'0');
        if (sisa <= 5 && sisa > 0) {{
            if (!sudahBunyi[sisa]) {{ sudahBunyi[sisa] = true; bunyiTit(0.25); }}
            let p = document.getElementById('pesan-timer');
            if (p) {{ p.textContent = '⚠️ SISA ' + sisa + ' DETIK LAGI! Segera klik LIHAT NILAI!'; p.style.color = '#FF5252'; p.style.fontWeight = 'bold'; p.style.fontSize = '18px'; }}
        }}
        if (sisa <= 0) {{
            let p = document.getElementById('pesan-timer');
            if (p) {{ p.textContent = '⛔ WAKTU HABIS! Segera klik tombol LIHAT NILAI di bawah!'; p.style.color = '#FF5252'; }}
            if (!sudahBunyi['habis']) {{ sudahBunyi['habis'] = true; bunyiTit(1.0); setTimeout(()=>bunyiTit(1.0), 400); }}
            clearInterval(iv);
            return;
        }}
        sisa -= 1;
    }}
    let iv = setInterval(updateTimer, 1000);
    </script>
    """
    components.html(timer_html, height=130)

DATA_SISWA = {
    "MUHAMAD HARTANTO": {"kategori": "Iqro", "level": "Iqro Dasar", "jk": "Laki-laki"},
    "DAFFAN OKTAFFIL HIDAYAT": {"kategori": "Iqro", "level": "Iqro Dasar", "jk": "Laki-laki"},
    "FRISCHA BUNGA LESTARI": {"kategori": "Tahsin", "level": "Tahsin", "jk": "Perempuan"},
    "RAIHAN": {"kategori": "Tahsin", "level": "Tahsin", "jk": "Laki-laki"},
    "ANGGA FADILLAH": {"kategori": "Tahsin", "level": "Tahsin", "jk": "Laki-laki"},
    "ANDY RAMADANI ABDULLAH": {"kategori": "Tahsin", "level": "Tahsin", "jk": "Laki-laki"},
    "ZALFATUSSYIFA RAMADANTI": {"kategori": "Tahfidz", "level": "Tahfidz", "jk": "Perempuan"},
    "ZAIN RAHMANITA": {"kategori": "Tahfidz", "level": "Tahfidz", "jk": "Perempuan"},
    "YUSUF IMAM MA'RUF": {"kategori": "Tahfidz", "level": "Tahfidz", "jk": "Laki-laki"},
    "FEBRIANSYAH RACHMAT HIDAYAT": {"kategori": "Tahfidz", "level": "Tahfidz", "jk": "Laki-laki"},
    "MUHAMMAD HAFIDZ": {"kategori": "Tahfidz", "level": "Tahfidz", "jk": "Laki-laki"},
    "ANGGI RATU MAHADEWI": {"kategori": "Tahfidz", "level": "Tahfidz", "jk": "Perempuan"},
    "RIZQI RAMADHANY": {"kategori": "Tahfidz", "level": "Tahfidz", "jk": "Laki-laki"},
    "KAWI LUJENGAN RASYIDA RAIHANUN": {"kategori": "Tahfidz", "level": "Tahfidz", "jk": "Perempuan"},
    "MIFTAHUL JANNAH": {"kategori": "Tahfidz", "level": "Tahfidz", "jk": "Perempuan"},
    "MUHAMAD AZHAM FATAHILAH": {"kategori": "Tahfidz", "level": "Tahfidz", "jk": "Laki-laki"},
    "ROSMALATI KHOLISHA": {"kategori": "Tahfidz", "level": "Tahfidz", "jk": "Perempuan"},
    "M. ARIF ZAKARIYA": {"kategori": "Tahfidz", "level": "Tahfidz", "jk": "Laki-laki"},
    "MOCHAMMAD ALKAHFI MUBAROK": {"kategori": "Tahfidz", "level": "Tahfidz", "jk": "Laki-laki"},
    "IMAM MANSYUR IBNU HULKAN": {"kategori": "Tahfidz", "level": "Tahfidz", "jk": "Laki-laki"},
}

def tampilkan_daftar_hasil_nilai():
    st.markdown("<div style='background-color: rgba(20,50,35,0.95); padding:18px; border-radius:15px; text-align:center; border:2px solid #F9D423;'><h2 style='color:#F9D423; margin:0;'>📊 Daftar Hasil Nilai</h2><p style='color:white; margin:5px 0 0 0;'>KKM = 75 | Nilai ≤ 75 = <b style=\"color:#FF5252;\">MERAH (Belum Tuntas)</b> | Nilai > 75 = <b style=\"color:white;\">PUTIH (Tuntas)</b> | Belum Ujian = <b style=\"color:#AAAAAA;\">- (Belum Mengerjakan)</b></p><p style='color:white; font-size:13px;'>Yang Belum Tuntas boleh Remedial / Mengulang sampai Tuntas. Jumlah mengulang tercatat di kolom Mengulang.</p></div>", unsafe_allow_html=True)
    st.write("")
    # Tombol reset khusus No.7 yang kemarin kena 0 gara-gara tes refresh
    if "ZALFATUSSYIFA RAMADANTI" in st.session_state["hasil_semua"]:
        st.warning("⚠️ No. 7 ZALFATUSSYIFA RAMADANTI masih ada nilai 0 bekas tes refresh. Klik tombol di bawah untuk menghapusnya.")
        if st.button("🗑️ Reset No.7 - ZALFATUSSYIFA Jadi Belum Mengerjakan", use_container_width=True):
            del st.session_state["hasil_semua"]["ZALFATUSSYIFA RAMADANTI"]
            if "ZALFATUSSYIFA RAMADANTI" in st.session_state["hitung_ulang"]:
                del st.session_state["hitung_ulang"]["ZALFATUSSYIFA RAMADANTI"]
            st.rerun()
    total_tuntas = 0
    total_belum_tuntas = 0
    total_belum_ujian = 0
    rows_html = ""
    no = 1
    for nama in DATA_SISWA:
        info = DATA_SISWA[nama]
        jk = info["jk"]
        kat = info["kategori"]
        jml_ulang = st.session_state["hitung_ulang"].get(nama, 0)
        if nama not in st.session_state["hasil_semua"]:
            teks_ulang = "-"
            rows_html += f"<tr><td style='padding:10px; text-align:center; color:white;'>{no}</td><td style='padding:10px; color:white; font-weight:bold;'>{nama}</td><td style='padding:10px; text-align:center; color:white;'>{jk}</td><td style='padding:10px; text-align:center; color:white;'>{kat}</td><td style='padding:10px; text-align:center; color:#AAAAAA; font-weight:bold; font-size:20px;'>-</td><td style='padding:10px; text-align:center; color:#AAAAAA; font-weight:bold;'>⏳ Belum Mengerjakan</td><td style='padding:10px; text-align:center; color:#AAAAAA;'>{teks_ulang}</td></tr>"
            total_belum_ujian += 1
        else:
            nilai = st.session_state["hasil_semua"][nama]
            # PERBAIKAN: Kalau ada nilai tapi hitungan 0, anggap 1x
            if jml_ulang == 0:
                jml_ulang = 1
            if jml_ulang <= 1:
                teks_ulang = f"{jml_ulang}x"
            else:
                teks_ulang = f"{jml_ulang}x 🔁"
            if nilai <= KKM:
                warna_nilai = "#FF5252"
                ket = "❌ Belum Tuntas"
                warna_ket = "#FF5252"
                total_belum_tuntas += 1
            else:
                warna_nilai = "#FFFFFF"
                ket = "✅ Tuntas"
                warna_ket = "#4CAF50"
                total_tuntas += 1
            rows_html += f"<tr><td style='padding:10px; text-align:center; color:white;'>{no}</td><td style='padding:10px; color:white; font-weight:bold;'>{nama}</td><td style='padding:10px; text-align:center; color:white;'>{jk}</td><td style='padding:10px; text-align:center; color:white;'>{kat}</td><td style='padding:10px; text-align:center; color:{warna_nilai}; font-weight:bold; font-size:20px;'>{nilai}</td><td style='padding:10px; text-align:center; color:{warna_ket}; font-weight:bold;'>{ket}</td><td style='padding:10px; text-align:center; color:white; font-weight:bold;'>{teks_ulang}</td></tr>"
        no += 1
    st.markdown(f"""
    <div style='background-color: rgba(0,0,0,0.75); padding:15px; border-radius:15px;'>
    <p style='color:white; text-align:center; font-size:16px;'>Total Siswa: <b>{len(DATA_SISWA)}</b> | <span style='color:#AAAAAA; font-weight:bold;'>⏳ Belum Mengerjakan: {total_belum_ujian}</span> | <span style='color:#4CAF50; font-weight:bold;'>✅ Tuntas: {total_tuntas}</span> | <span style='color:#FF5252; font-weight:bold;'>❌ Belum Tuntas: {total_belum_tuntas}</span></p>
    <table style='width:100%; border-collapse:collapse;'>
    <tr style='background-color:#F9D423;'>
        <th style='padding:10px; color:#000;'>No</th>
        <th style='padding:10px; color:#000; text-align:left;'>Nama Lengkap</th>
        <th style='padding:10px; color:#000;'>Jenis Kelamin</th>
        <th style='padding:10px; color:#000;'>Kategori</th>
        <th style='padding:10px; color:#000;'>Nilai</th>
        <th style='padding:10px; color:#000;'>Keterangan</th>
        <th style='padding:10px; color:#000;'>Mengulang</th>
    </tr>
    {rows_html}
    </table>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("⬅️ Tutup Daftar Nilai", use_container_width=True):
        st.session_state["lihat_nilai"] = False
        st.rerun()

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
    [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"] {{ background: transparent !important; }}
    .stApp::before {{ content: ""; position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.55); z-index: 0; pointer-events: none; }}
    .block-container {{ position: relative; z-index: 1; padding-top: 20px !important; max-width: 900px !important; }}
    [data-testid="stBottom"] {{ background-image: url("data:image/jpeg;base64,{bg}") !important; background-size: cover !important; background-position: center center !important; background-repeat: no-repeat !important; background-attachment: fixed !important; }}
    [data-testid="stBottomBlockContainer"], [data-testid="stChatInputContainer"] {{ background: transparent !important; background-image: none !important; background-color: transparent !important; }}
    [data-testid="stBottom"]::before {{ content: ""; position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.55); pointer-events: none; }}
    [data-testid="stChatInput"] {{ position: relative; z-index: 2; background-color: white !important; border-radius: 20px !important; }}
    .block-container p, .block-container span, .block-container label, .block-container h2, .block-container h3 {{ color: white !important; }}
    [data-testid="stRadio"] label {{ color: white !important; font-weight: 600 !important; }}
    [data-testid="stRadio"] div, [data-testid="stRadio"] p {{ color: white !important; }}
    div[data-testid="stButton"] > button {{ background-color: rgba(255,255,255,0.25) !important; background: rgba(255,255,255,0.25) !important; color: white !important; border: 1.5px solid rgba(255,255,255,0.8) !important; backdrop-filter: blur(4px) !important; font-weight: bold !important; font-size: 17px !important; border-radius: 12px !important; }}
    div[data-testid="stButton"] > button:hover {{ background-color: rgba(255,255,255,0.45) !important; color: white !important; border: 1.5px solid white !important; }}
    div[data-testid="stButton"] > button p, div[data-testid="stButton"] > button span {{ color: white !important; }}
    [data-testid="stChatMessage"] {{ background-color: rgba(10, 35, 25, 0.97) !important; backdrop-filter: none !important; border: 2px solid #F9D423 !important; border-radius: 14px !important; padding: 10px 14px !important; box-shadow: 0 4px 12px rgba(0,0,0,0.6) !important; }}
    [data-testid="stChatMessage"] p, [data-testid="stChatMessage"] span, [data-testid="stChatMessage"] li, [data-testid="stChatMessage"] strong {{ color: #FFFFFF !important; font-size: 20px !important; line-height: 2.0 !important; font-weight: 600 !important; text-shadow: 0 2px 4px rgba(0,0,0,1) !important; }}
    [data-testid="stChatMessage"] strong {{ color: #F9D423 !important; font-size: 21px !important; }}
    </style>
    """, unsafe_allow_html=True)

st.markdown("""
<div style='background-color: rgba(20, 50, 35, 0.92); padding: 25px; border-radius: 15px; text-align:center;'>
    <h1 style='color:#F9D423; margin:0; font-size:36px;'>🕌 QORI AI Madrasah Aliyah Al-Barokah</h1>
    <p style='color:white; margin-top:10px; font-size:16px;'>Assalamualaikum warahmatullahi wabarakatuh! Tanya apa saja tentang Iqro, Tahsin dan Tahfidz</p>
</div>
""", unsafe_allow_html=True)

if st.session_state["siswa_pilih"] is None:
    tampilkan_tim_pembuat()

st.write("")

if st.session_state["curang_refresh"]:
    nama_curang = st.session_state["curang_refresh"]
    st.session_state["hasil_semua"][nama_curang] = 0
    # Refresh juga dihitung 1x mengerjakan
    if nama_curang not in st.session_state["hitung_ulang"]:
        st.session_state["hitung_ulang"][nama_curang] = 1
    st.markdown(f"<div style='background-color:#7A0000; padding:25px; border-radius:15px; text-align:center; border:3px solid #FF5252;'><h1 style='color:white;'>⛔ TERDETEKSI REFRESH SAAT UJIAN!</h1><p style='color:white; font-size:20px;'>Nama: {nama_curang}</p><h1 style='color:#F9D423; font-size:60px;'>Nilai: 0</h1><p style='color:white; font-size:18px;'>Kamu keluar / refresh halaman saat ujian sedang berjalan.<br>Jawabanmu tidak disimpan dan nilai dianggap 0.<br>Kamu masih bisa Remedial / Mengulang sampai Tuntas.</p></div>", unsafe_allow_html=True)
    st.write("")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔁 Remedial - Ulangi Lagi", use_container_width=True):
            st.session_state["curang_refresh"] = None
            st.session_state["siswa_pilih"] = nama_curang
            st.session_state["seed_acak"] = st.session_state["seed_acak"] + 1
            st.session_state["soal_acak"] = None
            st.session_state["waktu_mulai"] = time.time()
            st.session_state["waktu_habis"] = False
            st.session_state["ujian_selesai"] = False
            st.session_state["hasil_ujian"] = None
            try:
                st.query_params["ujian"] = "jalan"
                st.query_params["nama"] = nama_curang
            except:
                pass
            st.rerun()
    with col2:
        if st.button("🏠 Saya Mengerti - Kembali ke Beranda", use_container_width=True):
            st.session_state["curang_refresh"] = None
            st.session_state["siswa_pilih"] = None
            try:
                st.query_params.clear()
            except:
                pass
            st.rerun()
    st.stop()

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
def buat_soal_acak(kat, seed):
    rng = random.Random(seed)
    data_asli = SOAL_ALL[kat]
    kunci_asli = KUNCI[kat]
    gabung = list(zip(data_asli, kunci_asli))
    rng.shuffle(gabung)
    soal_baru = []
    kunci_baru = []
    for (teks_soal, opsi_asli), kunci_lama in gabung:
        isi_jawaban = []
        for o in opsi_asli:
            if ". " in o:
                isi_jawaban.append(o.split(". ", 1)[1])
            elif " - " in o:
                isi_jawaban.append(o.split(" - ", 1)[1])
            else:
                isi_jawaban.append(o)
        if len(opsi_asli) == 5:
            idx_benar = ord(kunci_lama) - ord("A")
        else:
            idx_benar = 0 if kunci_lama == "B" else 1
        isi_benar = isi_jawaban[idx_benar]
        rng.shuffle(isi_jawaban)
        opsi_baru = []
        kunci_baru_satu = ""
        if len(opsi_asli) == 5:
            huruf = ["A","B","C","D","E"]
            for i, isi in enumerate(isi_jawaban):
                opsi_baru.append(f"{huruf[i]}. {isi}")
                if isi == isi_benar:
                    kunci_baru_satu = huruf[i]
        else:
            for i, isi in enumerate(isi_jawaban):
                label = "B" if isi == "Benar" else "S"
                opsi_baru.append(f"{label} - {isi}")
                if isi == isi_benar:
                    kunci_baru_satu = label
        teks_bersih = teks_soal
        if ". " in teks_bersih[:5]:
            teks_bersih = teks_bersih.split(". ", 1)[1]
        soal_baru.append((teks_bersih, opsi_baru))
        kunci_baru.append(kunci_baru_satu)
    return soal_baru, kunci_baru

def tampilkan_daftar(kategori):
    if kategori == "Iqro":
        daftar = ["MUHAMAD HARTANTO", "DAFFAN OKTAFFIL HIDAYAT"]
    elif kategori == "Tahsin":
        daftar = ["FRISCHA BUNGA LESTARI", "RAIHAN", "ANGGA FADILLAH", "ANDY RAMADANI ABDULLAH"]
    else:
        daftar = ["ZALFATUSSYIFA RAMADANTI", "ZAIN RAHMANITA", "YUSUF IMAM MA'RUF", "FEBRIANSYAH RACHMAT HIDAYAT", "MUHAMMAD HAFIDZ", "ANGGI RATU MAHADEWI", "RIZQI RAMADHANY", "KAWI LUJENGAN RASYIDA RAIHANUN", "MIFTAHUL JANNAH", "MUHAMAD AZHAM FATAHILAH", "ROSMALATI KHOLISHA", "M. ARIF ZAKARIYA", "MOCHAMMAD ALKAHFI MUBAROK", "IMAM MANSYUR IBNU HULKAN"]
    for item in daftar:
        if st.button(item, key=f"{kategori}-{item}"):
            st.session_state["siswa_pilih"] = item
            st.session_state["seed_acak"] = st.session_state["seed_acak"] + 1
            st.session_state["soal_acak"] = None
            st.session_state["waktu_mulai"] = time.time()
            st.session_state["waktu_habis"] = False
            st.session_state["ujian_selesai"] = False
            st.session_state["hasil_ujian"] = None
            st.session_state["curang_refresh"] = None
            st.session_state["lihat_nilai"] = False
            try:
                st.query_params["ujian"] = "jalan"
                st.query_params["nama"] = item
            except:
                pass
            st.rerun()

if st.session_state["siswa_pilih"] is None and not st.session_state["lihat_nilai"]:
    c_btn1, c_btn2, c_btn3, c_btn4 = st.columns(4)
    with c_btn1:
        klik_iqro = st.button("📖 Iqro", use_container_width=True)
    with c_btn2:
        klik_tahsin = st.button("📗 Tahsin", use_container_width=True)
    with c_btn3:
        klik_tahfidz = st.button("⭐ Tahfidz", use_container_width=True)
    with c_btn4:
        klik_nilai = st.button("📊 Daftar Hasil Nilai", use_container_width=True)
    if klik_iqro:
        st.session_state["kategori_pilih"] = None if st.session_state["kategori_pilih"] == "Iqro" else "Iqro"
        st.session_state["lihat_nilai"] = False
    if klik_tahsin:
        st.session_state["kategori_pilih"] = None if st.session_state["kategori_pilih"] == "Tahsin" else "Tahsin"
        st.session_state["lihat_nilai"] = False
    if klik_tahfidz:
        st.session_state["kategori_pilih"] = None if st.session_state["kategori_pilih"] == "Tahfidz" else "Tahfidz"
        st.session_state["lihat_nilai"] = False
    if klik_nilai:
        st.session_state["lihat_nilai"] = True
        st.session_state["kategori_pilih"] = None
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

if st.session_state["lihat_nilai"] and st.session_state["siswa_pilih"] is None:
    tampilkan_daftar_hasil_nilai()
    st.stop()

if st.session_state["siswa_pilih"]:
    nama = st.session_state["siswa_pilih"]
    info = DATA_SISWA.get(nama, {"kategori": "Iqro", "level": "Pemula", "jk": "-"})
    kat = info["kategori"]
    if st.session_state["waktu_mulai"] is None:
        st.session_state["waktu_mulai"] = time.time()
    sisa_detik = DURASI_UJIAN - (time.time() - st.session_state["waktu_mulai"])
    if sisa_detik <= 0:
        sisa_detik = 0
        st.session_state["waktu_habis"] = True
    jml_percobaan = st.session_state["hitung_ulang"].get(nama, 0)
    st.markdown(f"<div style='background-color: rgba(20,50,35,0.92); padding:20px; border-radius:15px; text-align:center;'><h2 style='color:#F9D423; margin:0;'>Assalamualaikum, {nama} 👋</h2><p style='color:white;'>Kelas: {kat} | Level: {info['level']} | Soal: 25 Soal | Nilai: Benar x 4 | Waktu: 10 Menit | KKM: 75 | Percobaan ke-{jml_percobaan + 1 if not st.session_state['ujian_selesai'] else jml_percobaan}</p></div>", unsafe_allow_html=True)
    if not st.session_state["ujian_selesai"]:
        st.warning("🔒 UJIAN TERKUNCI - Jangan refresh / tutup tab / pencet back! Kalau refresh, nilai langsung jadi 0!")
    tampilkan_timer(sisa_detik)
    if st.session_state["waktu_habis"] and not st.session_state["ujian_selesai"]:
        st.error("⛔ WAKTU HABIS! 10 menit sudah selesai. Silakan klik LIHAT NILAI di bawah.")
    if st.session_state["ujian_selesai"]:
        # Kalau sudah tuntas, tombol kembali. Kalau belum tuntas, tombol remedial + kembali
        if st.session_state["hasil_ujian"] and st.session_state["hasil_ujian"]["nilai"] <= KKM:
            col_r, col_k = st.columns(2)
            with col_r:
                if st.button("🔁 Remedial - Ulangi Lagi Sampai Tuntas", use_container_width=True):
                    # Hapus jawaban lama biar radio kosong lagi
                    for k in list(st.session_state.keys()):
                        if k.startswith("soal_"):
                            del st.session_state[k]
                    st.session_state["seed_acak"] = st.session_state["seed_acak"] + 1
                    st.session_state["soal_acak"] = None
                    st.session_state["waktu_mulai"] = time.time()
                    st.session_state["waktu_habis"] = False
                    st.session_state["ujian_selesai"] = False
                    st.session_state["hasil_ujian"] = None
                    try:
                        st.query_params["ujian"] = "jalan"
                        st.query_params["nama"] = nama
                    except:
                        pass
                    st.rerun()
            with col_k:
                if st.button("🏠 Kembali ke Beranda", use_container_width=True):
                    st.session_state["siswa_pilih"] = None
                    st.session_state["soal_acak"] = None
                    st.session_state["waktu_mulai"] = None
                    st.session_state["waktu_habis"] = False
                    st.session_state["ujian_selesai"] = False
                    st.session_state["hasil_ujian"] = None
                    st.session_state["kategori_pilih"] = None
                    try:
                        st.query_params.clear()
                    except:
                        pass
                    st.rerun()
        else:
            if st.button("🏠 Selesai - Kembali ke Beranda", use_container_width=True):
                st.session_state["siswa_pilih"] = None
                st.session_state["soal_acak"] = None
                st.session_state["waktu_mulai"] = None
                st.session_state["waktu_habis"] = False
                st.session_state["ujian_selesai"] = False
                st.session_state["hasil_ujian"] = None
                st.session_state["kategori_pilih"] = None
                try:
                    st.query_params.clear()
                except:
                    pass
                st.rerun()
    if st.session_state["soal_acak"] is None or st.session_state["kat_acak"] != kat:
        soal_list, kunci = buat_soal_acak(kat, st.session_state["seed_acak"])
        st.session_state["soal_acak"] = soal_list
        st.session_state["kunci_acak"] = kunci
        st.session_state["kat_acak"] = kat
    else:
        soal_list = st.session_state["soal_acak"]
        kunci = st.session_state["kunci_acak"]
    st.markdown(f"<h2 style='color:white; background-color: rgba(0,0,0,0.65); padding:10px; border-radius:10px; text-align:center;'>📝 Soal {kat} - Kelas XI MA</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:white; background-color: rgba(0,0,0,0.65); padding:8px; border-radius:10px; text-align:center;'>Jawab semua soal, lalu klik LIHAT NILAI di bawah.</p>", unsafe_allow_html=True)
    jawaban_siswa = []
    seed = st.session_state["seed_acak"]
    kunci_input = st.session_state["ujian_selesai"]
    for i, (soal, opsi) in enumerate(soal_list):
        st.markdown(f"<div style='background-color: rgba(0,0,0,0.65); padding:12px; border-radius:10px; margin-bottom:5px;'><p style='color:white; font-weight:bold; font-size:17px; margin:0;'>{i+1}. {soal}</p></div>", unsafe_allow_html=True)
        pilih = st.radio(f"Pilih jawaban No.{i+1}", opsi, key=f"soal_{kat}_{seed}_{i}", index=None, disabled=kunci_input)
        jawaban_siswa.append(pilih)
    if not st.session_state["ujian_selesai"]:
        if st.button("✅ LIHAT NILAI SAYA - SELESAI", use_container_width=True):
            benar = 0
            for i, pilih in enumerate(jawaban_siswa):
                if pilih and pilih[0] == kunci[i]:
                    benar += 1
            nilai = (benar / 25) * 100
            st.session_state["ujian_selesai"] = True
            st.session_state["hasil_ujian"] = {"benar": benar, "nilai": int(nilai)}
            st.session_state["hasil_semua"][nama] = int(nilai)
            st.session_state["hitung_ulang"][nama] = st.session_state["hitung_ulang"].get(nama, 0) + 1
            try:
                st.query_params.clear()
            except:
                pass
            st.rerun()
    if st.session_state["ujian_selesai"] and st.session_state["hasil_ujian"]:
        hasil = st.session_state["hasil_ujian"]
        benar = hasil["benar"]
        nilai = hasil["nilai"]
        percobaan = st.session_state["hitung_ulang"].get(nama, 1)
        warna_n = "#FF5252" if nilai <= KKM else "#FFFFFF"
        st.success(f"🎉 HASIL {nama} - Kelas {kat}")
        st.markdown(f"<div style='background-color: rgba(0,0,0,0.65); padding:15px; border-radius:10px; text-align:center;'><h1 style='color:{warna_n};'>Nilai: {nilai}</h1><p style='color:white;'>Jawaban Benar: {benar} / 25 | Salah / Kosong: {25-benar} | KKM: 75 | Percobaan ke-{percobaan} | {'❌ Belum Tuntas - Silakan klik Remedial di atas untuk mengulang!' if nilai <= KKM else '✅ Tuntas!'}</p><p style='color:white;'>Perhitungan: ({benar} ÷ 25) × 100 = {nilai}</p></div>", unsafe_allow_html=True)
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

if st.session_state["messages"]:
    for idx, m in enumerate(st.session_state["messages"]):
        with st.chat_message(m["role"]):
            st.markdown(m["content"])
            if st.button("🗑️ Hapus pesan ini", key=f"hapus_{idx}"):
                del st.session_state["messages"][idx]
                st.rerun()
    st.write("")
    if st.button("🗑️ Hapus Semua Chat", use_container_width=True):
        st.session_state["messages"] = []
        st.rerun()

prompt = None
if prompt_awal:
    prompt = prompt_awal
else:
    prompt = st.text_input("Tulis pertanyaanmu di sini...", placeholder="Tulis pertanyaanmu di sini... (Hanya Iqro, Tahsin, Tahfidz)", label_visibility="collapsed")
    kirim = st.button("Kirim ➤", use_container_width=True)
    if not kirim:
        prompt = None

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        t_lower = prompt.lower()
        if "mad" in t_lower and ("tobi" in t_lower or "thobi" in t_lower or "thabi" in t_lower or "tobii" in t_lower or "thobii" in t_lower):
            jawaban = jawaban_mad_thobii()
            st.markdown(jawaban)
            st.session_state.messages.append({"role": "assistant", "content": jawaban})
        elif "an-naba" in t_lower or "an naba" in t_lower or "annaba" in t_lower:
            jawaban = jawaban_an_naba()
            st.markdown(jawaban)
            st.session_state.messages.append({"role": "assistant", "content": jawaban})
        elif ("hijaiyah" in t_lower or "huruf" in t_lower or "iqro 1" in t_lower or "iqro satu" in t_lower or "iqro dasar" in t_lower):
            jawaban = jawaban_hijaiyah_iqro1()
            st.markdown(jawaban)
            st.session_state.messages.append({"role": "assistant", "content": jawaban})
        elif cek_dilarang(prompt):
            st.markdown(PESAN_TOLAK)
            st.session_state.messages.append({"role": "assistant", "content": PESAN_TOLAK})
        elif not api_key:
            st.markdown("Maaf, API Key belum dipasang di Secrets Streamlit.")
        else:
            try:
                client = OpenAI(api_key=api_key)
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "system", "content": SYSTEM_PROMPT_KUNCI}, {"role": "user", "content": prompt}],
                    temperature=0.7, max_tokens=800
                )
                jawaban = response.choices[0].message.content
                st.markdown(jawaban)
                st.session_state.messages.append({"role": "assistant", "content": jawaban})
            except Exception as e:
                st.markdown(f"Maaf, sedang ada gangguan. Coba lagi ya. Cek saldo OpenAI, mungkin habis. ({e})")
