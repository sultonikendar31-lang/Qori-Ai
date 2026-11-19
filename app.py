import streamlit as st
import streamlit.components.v1 as components
import base64
import random
import time
import os
import sqlite3
import hashlib
import hmac
import html
from contextlib import closing
from openai import OpenAI
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="QORI AI", page_icon="🕌", layout="wide")

api_key = st.secrets.get("OPENAI_API_KEY", "")

# ===== PINTU MASUK / KUNCI NAMA =====
TIM_PENYUSUN = {
    "MUHAMAD RAIS": "Guru Pamong",
    "MUHAMAD SIDDIQ ASYHARI": "Dosen Pembimbing",
    "SYAMSUL HADI": "Kepala MA Al-Barokah",
    "KENDAR SULTONI": "Mahasiswa / Pembuat Aplikasi",
}

NAMA_LENGKAP_TIM = {
    "MUHAMAD RAIS": "Bapak Muhamad Rais, S.Pd.I",
    "MUHAMAD SIDDIQ ASYHARI": "Dr. Muhamad Siddiq Asyhari, M.Pd",
    "SYAMSUL HADI": "Bapak Syamsul Hadi, S.Pd.I",
    "KENDAR SULTONI": "Kendar Sultoni",
}

if "login_nama" not in st.session_state:
    st.session_state["login_nama"] = None
if "login_role" not in st.session_state:
    st.session_state["login_role"] = None
if "login_jabatan" not in st.session_state:
    st.session_state["login_jabatan"] = None
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
if "sudah_bersihkan_no7" not in st.session_state:
    st.session_state["sudah_bersihkan_no7"] = False
if "riwayat_aktivitas" not in st.session_state:
    st.session_state["riwayat_aktivitas"] = []
if "waktu_login" not in st.session_state:
    st.session_state["waktu_login"] = None
if "lihat_riwayat" not in st.session_state:
    st.session_state["lihat_riwayat"] = False
if "sudah_catat_masuk" not in st.session_state:
    st.session_state["sudah_catat_masuk"] = False
if "saran_list" not in st.session_state:
    st.session_state["saran_list"] = []
if "lihat_saran" not in st.session_state:
    st.session_state["lihat_saran"] = False

if not st.session_state["sudah_bersihkan_no7"]:
    st.session_state["sudah_bersihkan_no7"] = True
    if "ZALFATUSSYIFA RAMADANTI" in st.session_state.get("hasil_semua", {}):
        del st.session_state["hasil_semua"]["ZALFATUSSYIFA RAMADANTI"]
    if "ZALFATUSSYIFA RAMADANTI" in st.session_state.get("hitung_ulang", {}):
        del st.session_state["hitung_ulang"]["ZALFATUSSYIFA RAMADANTI"]


DURASI_UJIAN = 10 * 60
KKM = 75
prompt_awal = None

# ===== DATABASE PERSISTEN QORI AI =====
# Untuk server lokal gunakan qori_ai.db. Pada deployment cloud multi-instance,
# arahkan QORI_DB_PATH ke volume persisten atau ganti adapter dengan PostgreSQL/Supabase.
DB_PATH = os.getenv("QORI_DB_PATH", "qori_ai.db")

def db_connect():
    conn = sqlite3.connect(DB_PATH, timeout=20, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn

def init_database():
    with closing(db_connect()) as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS exam_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,
            category TEXT NOT NULL,
            score INTEGER NOT NULL,
            correct_count INTEGER NOT NULL,
            attempt_no INTEGER NOT NULL,
            created_at TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_exam_student ON exam_results(student_name, id);
        CREATE TABLE IF NOT EXISTS activity_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,
            category TEXT,
            activity TEXT NOT NULL,
            created_at TEXT NOT NULL,
            duration TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS suggestions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT NOT NULL,
            sender_label TEXT NOT NULL,
            role TEXT NOT NULL,
            kind TEXT NOT NULL,
            body TEXT NOT NULL,
            created_at TEXT NOT NULL,
            reply TEXT DEFAULT '',
            replied_by TEXT DEFAULT ''
        );
        """)
        conn.commit()

def load_persistent_data():
    """Muat ulang data bersama setiap rerun agar perubahan sesi lain terlihat."""
    init_database()
    with closing(db_connect()) as conn:
        latest = conn.execute("""
            SELECT e.* FROM exam_results e
            INNER JOIN (SELECT student_name, MAX(id) AS max_id
                        FROM exam_results GROUP BY student_name) x
            ON e.id=x.max_id
        """).fetchall()
        attempts = conn.execute("""
            SELECT student_name, COUNT(*) AS n FROM exam_results GROUP BY student_name
        """).fetchall()
        activities = conn.execute("""
            SELECT student_name AS nama, category AS kelas, activity AS aktivitas,
                   created_at AS jam, duration AS lama
            FROM activity_log ORDER BY id
        """).fetchall()
        suggestions = conn.execute("""
            SELECT id, sender AS pengirim, sender_label AS label, role, kind AS jenis,
                   body AS isi, created_at AS jam, reply AS balasan, replied_by AS pembalas
            FROM suggestions ORDER BY id
        """).fetchall()
    st.session_state["hasil_semua"] = {r["student_name"]: int(r["score"]) for r in latest}
    st.session_state["hitung_ulang"] = {r["student_name"]: int(r["n"]) for r in attempts}
    st.session_state["riwayat_aktivitas"] = [dict(r) for r in activities]
    st.session_state["saran_list"] = [dict(r) for r in suggestions]

def simpan_hasil_database(nama, kategori, nilai, benar, percobaan):
    with closing(db_connect()) as conn:
        conn.execute("""
            INSERT INTO exam_results(student_name, category, score, correct_count, attempt_no, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nama, kategori, int(nilai), int(benar), int(percobaan),
              time.strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()

def verifikasi_password(nama, password):
    """USER_PASSWORDS berisi SHA-256 password, bukan password teks biasa."""
    users = st.secrets.get("USER_PASSWORDS", {})
    hash_tersimpan = users.get(nama, "")
    if not hash_tersimpan:
        return False
    hash_input = hashlib.sha256(password.encode("utf-8")).hexdigest()
    return hmac.compare_digest(str(hash_tersimpan), hash_input)


# Deteksi refresh berbasis query string dihapus karena mudah dimanipulasi dan dapat memberi nilai 0 kepada siswa lain.

SYSTEM_PROMPT_KUNCI = """
Kamu adalah QORI AI, guru yang ramah dan pintar untuk anak Madrasah Aliyah Al-Barokah.
Kamu BEBAS menjawab pertanyaan apa saja: Iqro, Tahsin, Tahfidz, pelajaran sekolah, agama, umum, dll.
Keahlian utamamu tetap Iqro, Tahsin, dan Tahfidz, tapi kalau ditanya hal lain, jawab saja dengan baik, jangan menolak.
Jawab dengan Bahasa Indonesia yang mudah, sopan, dan islami.
Kalau menyebut huruf hijaiyah, WAJIB pakai format: 1. Alif (ا) - dibaca "A". Jangan tulis huruf Arab berderet-deret tanpa nama Latinnya.
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
                <p style='color:#F9D423; font-weight:bold; margin:0; font-size:15px;'>Bapak Muhamad Rais, S.Pd.I</p>
                <p style='color:white; margin:2px 0 0 0; font-size:13px;'>Guru Pamong</p>
            </div>
            <div style='background-color: rgba(0,0,0,0.55); padding:10px 14px; border-radius:10px; text-align:center; min-width:160px;'>
                <p style='color:#F9D423; font-weight:bold; margin:0; font-size:15px;'>Dr. Muhamad Siddiq Asyhari, M.Pd</p>
                <p style='color:white; margin:2px 0 0 0; font-size:13px;'>Dosen Pembimbing</p>
            </div>
            <div style='background-color: rgba(0,0,0,0.55); padding:10px 14px; border-radius:10px; text-align:center; min-width:160px;'>
                <p style='color:#F9D423; font-weight:bold; margin:0; font-size:15px;'>Bapak Syamsul Hadi, S.Pd.I</p>
                <p style='color:white; margin:2px 0 0 0; font-size:13px;'>Kepala MA Al-Barokah</p>
            </div>
            <div style='background-color: rgba(0,0,0,0.55); padding:10px 14px; border-radius:10px; text-align:center; min-width:160px;'>
                <p style='color:#F9D423; font-weight:bold; margin:0; font-size:15px;'>Kendar Sultoni</p>
                <p style='color:white; margin:2px 0 0 0; font-size:13px;'>Mahasiswa / Pembuat Aplikasi</p>
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

# Muat data bersama dari database setelah daftar siswa tersedia.
load_persistent_data()

# ===== RIWAYAT / STORY SISWA - KHUSUS TIM =====
def catat_aktivitas(aktivitas):
    if st.session_state.get("login_role") != "siswa":
        return
    if not st.session_state.get("login_nama"):
        return
    sekarang = time.time()
    jam = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime(sekarang))
    lama_detik = int(sekarang - st.session_state["waktu_login"]) if st.session_state.get("waktu_login") else 0
    menit = lama_detik // 60
    detik = lama_detik % 60
    lama = f"{menit} mnt {detik} dtk" if menit > 0 else f"{detik} dtk"
    info = DATA_SISWA.get(st.session_state["login_nama"], {})
    record = {
        "nama": st.session_state["login_nama"],
        "kelas": info.get("kategori", "-"),
        "aktivitas": aktivitas,
        "jam": jam,
        "lama": lama,
    }
    st.session_state["riwayat_aktivitas"].append(record)
    with closing(db_connect()) as conn:
        conn.execute(
            "INSERT INTO activity_log(student_name, category, activity, created_at, duration) VALUES (?, ?, ?, ?, ?)",
            (record["nama"], record["kelas"], record["aktivitas"], record["jam"], record["lama"])
        )
        conn.commit()

def tampilkan_riwayat_siswa():
    st.markdown("<div style='background-color: rgba(20,50,35,0.95); padding:18px; border-radius:15px; text-align:center; border:2px solid #F9D423;'><h2 style='color:#F9D423; margin:0;'>📋 Riwayat / Story Siswa</h2><p style='color:white; margin:5px 0 0 0;'>Khusus Tim Penyusun - Siswa TIDAK bisa lihat ini</p></div>", unsafe_allow_html=True)
    st.write("")
    if not st.session_state["riwayat_aktivitas"]:
        st.info("Belum ada siswa yang pakai aplikasi di sesi ini.")
    else:
        rows = ""
        for i, r in enumerate(reversed(st.session_state["riwayat_aktivitas"]), 1):
            rows += f"<tr><td style='padding:10px; text-align:center; color:white;'>{i}</td><td style='padding:10px; color:white; font-weight:bold;'>{r['nama']}</td><td style='padding:10px; text-align:center; color:white;'>{r['kelas']}</td><td style='padding:10px; color:white;'>{r['aktivitas']}</td><td style='padding:10px; text-align:center; color:white;'>{r['jam']}</td><td style='padding:10px; text-align:center; color:#F9D423; font-weight:bold;'>{r['lama']}</td></tr>"
        st.markdown(f"""
        <div style='background-color: rgba(0,0,0,0.75); padding:15px; border-radius:15px;'>
        <table style='width:100%; border-collapse:collapse;'>
        <tr style='background-color:#F9D423;'>
            <th style='padding:10px; color:#000;'>No</th>
            <th style='padding:10px; color:#000; text-align:left;'>Nama Siswa</th>
            <th style='padding:10px; color:#000;'>Kelas</th>
            <th style='padding:10px; color:#000; text-align:left;'>Buka Apa</th>
            <th style='padding:10px; color:#000;'>Jam</th>
            <th style='padding:10px; color:#000;'>Berapa Lama</th>
        </tr>
        {rows}
        </table>
        </div>
        """, unsafe_allow_html=True)
    st.write("")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("⬅️ Tutup Riwayat", use_container_width=True):
            st.session_state["lihat_riwayat"] = False
            st.rerun()
    with c2:
        if st.button("🗑️ Hapus Riwayat", use_container_width=True):
            st.session_state["riwayat_aktivitas"] = []
            with closing(db_connect()) as conn:
                conn.execute("DELETE FROM activity_log")
                conn.commit()
            st.rerun()

# ===== KOTAK SARAN / KRITIK / KELUHAN - TIM & SISWA =====
def tampilkan_kotak_saran():
    st.markdown("<div style='background-color: rgba(20,50,35,0.95); padding:18px; border-radius:15px; text-align:center; border:2px solid #F9D423;'><h2 style='color:#F9D423; margin:0;'>💬 Kotak Saran / Kritik / Keluhan</h2><p style='color:white; margin:5px 0 0 0;'>Sampaikan saran, kritik, atau keluhanmu di sini. Dibaca langsung oleh Tim Penyusun.</p></div>", unsafe_allow_html=True)
    st.write("")
    # --- FORM KIRIM ---
    st.markdown("<div style='background-color: rgba(0,0,0,0.65); padding:15px; border-radius:12px;'><p style='color:white; font-weight:bold;'>✍️ Tulis Saran / Kritik / Keluhan Baru:</p></div>", unsafe_allow_html=True)
    jenis_saran = st.selectbox("Jenis Pesan:", ["💡 Saran", "📝 Kritik", "😟 Keluhan"], key="jenis_saran")
    isi_saran = st.text_area("Isi Pesan:", placeholder="Contoh: Soalnya susah di bagian..., Tolong tambahin materi..., Aplikasinya kadang lemot...", height=120, key="isi_saran")
    if st.button("📩 Kirim Saran / Kritik / Keluhan", use_container_width=True):
        if not isi_saran.strip():
            st.warning("⚠️ Isi pesannya masih kosong!")
        else:
            if st.session_state["login_role"] == "siswa":
                info_s = DATA_SISWA.get(st.session_state["login_nama"], {})
                label_pengirim = f"{st.session_state['login_nama']} | Kelas: {info_s.get('kategori','-')}"
            else:
                nama_t = NAMA_LENGKAP_TIM.get(st.session_state["login_nama"], st.session_state["login_nama"])
                label_pengirim = f"{nama_t} | {TIM_PENYUSUN.get(st.session_state['login_nama'],'Tim')}"
            data_saran = {
                "pengirim": st.session_state["login_nama"],
                "label": label_pengirim,
                "role": st.session_state["login_role"],
                "jenis": jenis_saran,
                "isi": isi_saran.strip(),
                "jam": time.strftime("%d/%m/%Y %H:%M", time.localtime(time.time())),
                "balasan": "",
                "pembalas": "",
            }
            with closing(db_connect()) as conn:
                cur = conn.execute(
                    """INSERT INTO suggestions(sender, sender_label, role, kind, body, created_at)
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    (data_saran["pengirim"], data_saran["label"], data_saran["role"],
                     data_saran["jenis"], data_saran["isi"], data_saran["jam"])
                )
                data_saran["id"] = cur.lastrowid
                conn.commit()
            st.session_state["saran_list"].append(data_saran)
            catat_aktivitas(f"Kirim {jenis_saran}")
            st.success("✅ Terima kasih! Saran / Kritik / Keluhanmu sudah terkirim ke Tim.")
            st.rerun()
    st.write("")
    # --- DAFTAR PESAN ---
    if st.session_state["login_role"] == "siswa":
        daftar_saran = [s for s in st.session_state["saran_list"] if s["pengirim"] == st.session_state["login_nama"]]
        judul_daftar = "📩 Saran / Kritik / Keluhan Kamu:"
    else:
        daftar_saran = list(reversed(st.session_state["saran_list"]))
        judul_daftar = f"📩 Semua Saran / Kritik / Keluhan ({len(daftar_saran)} pesan):"
    st.markdown(f"<div style='background-color: rgba(0,0,0,0.65); padding:12px; border-radius:10px;'><p style='color:white; font-weight:bold; margin:0;'>{judul_daftar}</p></div>", unsafe_allow_html=True)
    st.write("")
    if not daftar_saran:
        st.info("Belum ada pesan. Yuk jadi yang pertama kirim saran!")
    else:
        # Untuk siswa tampilkan urutan lama ke baru, untuk tim baru ke lama sudah di-reverse di atas
        tampil = daftar_saran if st.session_state["login_role"] == "tim" else list(reversed(daftar_saran))
        for idx, s in enumerate(tampil):
            # Cari index asli di list utama untuk balas / hapus
            idx_asli = st.session_state["saran_list"].index(s)
            jenis_html = html.escape(str(s.get("jenis", "")))
            label_html = html.escape(str(s.get("label", "")))
            jam_html = html.escape(str(s.get("jam", "")))
            isi_html = html.escape(str(s.get("isi", "")))
            st.markdown(f"<div style='background-color: rgba(255,255,255,0.12); border:1.5px solid rgba(255,255,255,0.5); padding:14px; border-radius:12px; margin-bottom:10px;'><p style='color:#F9D423; font-weight:bold; margin:0;'>{jenis_html} - {label_html}</p><p style='color:#AAAAAA; font-size:12px; margin:2px 0 8px 0;'>{jam_html}</p><p style='color:white; margin:0;'>{isi_html}</p></div>", unsafe_allow_html=True)
            if s.get("balasan"):
                pembalas_html = html.escape(str(s.get("pembalas", "")))
                balasan_html = html.escape(str(s.get("balasan", "")))
                st.markdown(f"<div style='background-color: rgba(20,50,35,0.9); border:1.5px solid #F9D423; padding:12px; border-radius:12px; margin:-5px 0 12px 20px;'><p style='color:#F9D423; font-weight:bold; margin:0;'>↩️ Balasan dari {pembalas_html}:</p><p style='color:white; margin:4px 0 0 0;'>{balasan_html}</p></div>", unsafe_allow_html=True)
            # Tim bisa balas
            if st.session_state["login_role"] == "tim":
                balas = st.text_input(f"Balas pesan ini (Tim):", key=f"balas_{idx_asli}", placeholder="Tulis balasan untuk pengirim...")
                cb1, cb2 = st.columns(2)
                with cb1:
                    if st.button("↩️ Kirim Balasan", key=f"kirim_balas_{idx_asli}", use_container_width=True):
                        if not balas.strip():
                            st.warning("⚠️ Balasannya masih kosong!")
                        else:
                            nama_t = NAMA_LENGKAP_TIM.get(st.session_state["login_nama"], st.session_state["login_nama"])
                            pembalas = f"{nama_t} | {TIM_PENYUSUN.get(st.session_state['login_nama'],'Tim')}"
                            st.session_state["saran_list"][idx_asli]["balasan"] = balas.strip()
                            st.session_state["saran_list"][idx_asli]["pembalas"] = pembalas
                            saran_id = st.session_state["saran_list"][idx_asli].get("id")
                            if saran_id:
                                with closing(db_connect()) as conn:
                                    conn.execute("UPDATE suggestions SET reply=?, replied_by=? WHERE id=?",
                                                 (balas.strip(), pembalas, saran_id))
                                    conn.commit()
                            st.success("✅ Balasan terkirim!")
                            st.rerun()
                with cb2:
                    if st.button("🗑️ Hapus Pesan", key=f"hapus_saran_{idx_asli}", use_container_width=True):
                        item_hapus = st.session_state["saran_list"][idx_asli]
                        if item_hapus.get("id"):
                            with closing(db_connect()) as conn:
                                conn.execute("DELETE FROM suggestions WHERE id=?", (item_hapus["id"],))
                                conn.commit()
                        item_hapus = st.session_state["saran_list"][idx_asli]
                        if item_hapus.get("id"):
                            with closing(db_connect()) as conn:
                                conn.execute("DELETE FROM suggestions WHERE id=?", (item_hapus["id"],))
                                conn.commit()
                        del st.session_state["saran_list"][idx_asli]
                        st.rerun()
            # Siswa bisa hapus pesan sendiri yang belum dibalas
            if st.session_state["login_role"] == "siswa" and not s.get("balasan"):
                if st.button("🗑️ Hapus Pesan Saya", key=f"hapus_saran_siswa_{idx_asli}"):
                    del st.session_state["saran_list"][idx_asli]
                    st.rerun()
    st.write("")
    if st.button("⬅️ Tutup Kotak Saran", use_container_width=True):
        st.session_state["lihat_saran"] = False
        st.rerun()

def tampilkan_daftar_hasil_nilai():
    st.markdown("<div style='background-color: rgba(20,50,35,0.95); padding:18px; border-radius:15px; text-align:center; border:2px solid #F9D423;'><h2 style='color:#F9D423; margin:0;'>📊 Daftar Hasil Nilai</h2><p style='color:white; margin:5px 0 0 0;'>KKM = 75 | Nilai < 75 = <b style=\"color:#FF5252;\">MERAH (Belum Tuntas)</b> | Nilai ≥ 75 = <b style=\"color:white;\">PUTIH (Tuntas)</b> | Belum Ujian = <b style=\"color:#AAAAAA;\">- (Belum Mengerjakan)</b></p></div>", unsafe_allow_html=True)
    st.write("")
    if st.session_state["login_role"] == "siswa":
        daftar_tampil = [st.session_state["login_nama"]] if st.session_state["login_nama"] in DATA_SISWA else []
    else:
        daftar_tampil = list(DATA_SISWA.keys())
    total_tuntas = 0
    total_belum_tuntas = 0
    total_belum_ujian = 0
    rows_html = ""
    no = 1
    for nama in daftar_tampil:
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
            if jml_ulang == 0:
                jml_ulang = 1
            teks_ulang = f"{jml_ulang}x" if jml_ulang <= 1 else f"{jml_ulang}x 🔁"
            if nilai < KKM:
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
    <p style='color:white; text-align:center; font-size:16px;'>Total: <b>{len(daftar_tampil)}</b> | <span style='color:#AAAAAA; font-weight:bold;'>⏳ Belum Mengerjakan: {total_belum_ujian}</span> | <span style='color:#4CAF50; font-weight:bold;'>✅ Tuntas: {total_tuntas}</span> | <span style='color:#FF5252; font-weight:bold;'>❌ Belum Tuntas: {total_belum_tuntas}</span></p>
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
    <p style='color:white; margin-top:10px; font-size:16px;'>Assalamualaikum warahmatullahi wabarakatuh! Tanya apa saja, QORI AI siap membantu</p>
</div>
""", unsafe_allow_html=True)

# ===== HALAMAN KUNCI NAMA - WAJIB ISI SEBELUM MASUK =====
if st.session_state["login_nama"] is None:
    st.markdown("""
    <div style='background-color: rgba(255,255,255,0.12); border: 1.5px solid #F9D423; padding: 20px; border-radius: 15px; margin-top: 15px; text-align:center;'>
        <h2 style='color:#F9D423; margin:0;'>🔐 Silakan Masukkan Nama Lengkap</h2>
        <p style='color:white; margin-top:8px;'>Untuk masuk ke QORI AI</p>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    nama_input = st.text_input("✍️ Nama Lengkap:", placeholder="Tulis nama lengkap sesuai daftar...", key="input_nama_login")
    password_input = st.text_input("🔑 Password:", type="password", key="input_password_login")
    st.caption("Akun harus didaftarkan oleh administrator. Hubungi tim QORI AI jika belum memiliki password.")
    if st.button("🚪 Masuk ke QORI AI", use_container_width=True):
        nama_bersih = nama_input.strip().upper()
        if not nama_bersih or not password_input:
            st.warning("⚠️ Nama dan password wajib diisi.")
        elif nama_bersih not in TIM_PENYUSUN and nama_bersih not in DATA_SISWA:
            st.error("❌ Nama tidak terdaftar. Periksa kembali atau hubungi administrator.")
        elif not verifikasi_password(nama_bersih, password_input):
            st.error("⛔ Password salah atau akun belum dikonfigurasi oleh administrator.")
        elif nama_bersih in TIM_PENYUSUN:
            st.session_state["login_nama"] = nama_bersih
            st.session_state["login_role"] = "tim"
            st.session_state["login_jabatan"] = TIM_PENYUSUN[nama_bersih]
            st.session_state["waktu_login"] = time.time()
            st.session_state["sudah_catat_masuk"] = False
            st.success(f"✅ Selamat datang, {NAMA_LENGKAP_TIM.get(nama_bersih, nama_bersih)}")
            time.sleep(0.3)
            st.rerun()
        else:
            st.session_state["login_nama"] = nama_bersih
            st.session_state["login_role"] = "siswa"
            st.session_state["login_jabatan"] = f"Siswa {DATA_SISWA[nama_bersih]['kategori']}"
            st.session_state["waktu_login"] = time.time()
            st.session_state["sudah_catat_masuk"] = False
            st.success(f"✅ Selamat datang, {nama_bersih}")
            time.sleep(0.3)
            st.rerun()
    st.write("")
    st.stop()

# ===== SUDAH LOGIN - SISWA = KELAS, TIM = GELAR + JABATAN =====
if st.session_state["login_role"] == "siswa":
    info_login = DATA_SISWA.get(st.session_state["login_nama"], {})
    kelas_login = info_login.get("kategori", "")
    teks_selamat = f"👤 Selamat datang, {st.session_state['login_nama']} | Kelas: {kelas_login}"
else:
    jabatan_tim = TIM_PENYUSUN.get(st.session_state["login_nama"], st.session_state.get("login_jabatan", ""))
    nama_tim = NAMA_LENGKAP_TIM.get(st.session_state["login_nama"], st.session_state["login_nama"])
    teks_selamat = f"👤 Selamat datang, {nama_tim} | {jabatan_tim}"
st.markdown(f"<div style='background-color: rgba(0,0,0,0.6); padding:10px; border-radius:10px; text-align:center; margin-top:10px;'><b style='color:white;'>{teks_selamat}</b></div>", unsafe_allow_html=True)

if st.session_state["login_role"] == "siswa" and not st.session_state["sudah_catat_masuk"]:
    st.session_state["sudah_catat_masuk"] = True
    catat_aktivitas("Masuk Aplikasi")

col_out1, col_out2 = st.columns([3,1])
with col_out2:
    if st.button("🚪 Keluar / Ganti Nama", use_container_width=True):
        if st.session_state["login_role"] == "siswa":
            catat_aktivitas("Keluar Aplikasi")
        st.session_state["login_nama"] = None
        st.session_state["login_role"] = None
        st.session_state["login_jabatan"] = None
        st.session_state["siswa_pilih"] = None
        st.session_state["kategori_pilih"] = None
        st.session_state["lihat_nilai"] = False
        st.session_state["lihat_riwayat"] = False
        st.session_state["lihat_saran"] = False
        st.session_state["sudah_catat_masuk"] = False
        st.session_state["waktu_login"] = None
        try:
            st.query_params.clear()
        except:
            pass
        st.rerun()

if st.session_state["siswa_pilih"] is None and st.session_state["login_role"] == "tim":
    tampilkan_tim_pembuat()

st.write("")

# Status ujian tidak lagi ditentukan oleh query parameter yang dapat diubah pengguna.
# Timer dan penilaian dilakukan berdasarkan waktu server pada sesi ujian.


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
    if st.session_state["login_role"] == "siswa":
        nama_login = st.session_state["login_nama"]
        if DATA_SISWA.get(nama_login, {}).get("kategori") != kategori:
            return
        daftar = [nama_login]
    else:
        if kategori == "Iqro":
            daftar = ["MUHAMAD HARTANTO", "DAFFAN OKTAFFIL HIDAYAT"]
        elif kategori == "Tahsin":
            daftar = ["FRISCHA BUNGA LESTARI", "RAIHAN", "ANGGA FADILLAH", "ANDY RAMADANI ABDULLAH"]
        else:
            daftar = ["ZALFATUSSYIFA RAMADANTI", "ZAIN RAHMANITA", "YUSUF IMAM MA'RUF", "FEBRIANSYAH RACHMAT HIDAYAT", "MUHAMMAD HAFIDZ", "ANGGI RATU MAHADEWI", "RIZQI RAMADHANY", "KAWI LUJENGAN RASYIDA RAIHANUN", "MIFTAHUL JANNAH", "MUHAMAD AZHAM FATAHILAH", "ROSMALATI KHOLISHA", "M. ARIF ZAKARIYA", "MOCHAMMAD ALKAHFI MUBAROK", "IMAM MANSYUR IBNU HULKAN"]
    for item in daftar:
        label_tombol = item if st.session_state["login_role"] == "tim" else f"▶️ Mulai Ujian - {item}"
        if st.button(label_tombol, key=f"{kategori}-{item}"):
            st.session_state["siswa_pilih"] = item
            st.session_state["seed_acak"] = st.session_state["seed_acak"] + 1
            st.session_state["soal_acak"] = None
            st.session_state["waktu_mulai"] = time.time()
            st.session_state["waktu_habis"] = False
            st.session_state["ujian_selesai"] = False
            st.session_state["hasil_ujian"] = None
            st.session_state["curang_refresh"] = None
            st.session_state["lihat_nilai"] = False
            st.session_state["lihat_riwayat"] = False
            st.session_state["lihat_saran"] = False
            catat_aktivitas(f"Mulai Ujian - {kategori}")
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
        st.session_state["lihat_riwayat"] = False
        st.session_state["lihat_saran"] = False
        catat_aktivitas("Buka Kelas Iqro")
    if klik_tahsin:
        st.session_state["kategori_pilih"] = None if st.session_state["kategori_pilih"] == "Tahsin" else "Tahsin"
        st.session_state["lihat_nilai"] = False
        st.session_state["lihat_riwayat"] = False
        st.session_state["lihat_saran"] = False
        catat_aktivitas("Buka Kelas Tahsin")
    if klik_tahfidz:
        st.session_state["kategori_pilih"] = None if st.session_state["kategori_pilih"] == "Tahfidz" else "Tahfidz"
        st.session_state["lihat_nilai"] = False
        st.session_state["lihat_riwayat"] = False
        st.session_state["lihat_saran"] = False
        catat_aktivitas("Buka Kelas Tahfidz")
    if klik_nilai:
        st.session_state["lihat_nilai"] = True
        st.session_state["kategori_pilih"] = None
        st.session_state["lihat_riwayat"] = False
        st.session_state["lihat_saran"] = False
        catat_aktivitas("Buka Daftar Hasil Nilai")
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

# Tombol Riwayat HANYA untuk Tim
if st.session_state["login_role"] == "tim" and st.session_state["siswa_pilih"] is None:
    if st.button("📋 Riwayat / Story Siswa (Khusus Tim)", use_container_width=True):
        st.session_state["lihat_riwayat"] = True
        st.session_state["kategori_pilih"] = None
        st.session_state["lihat_nilai"] = False
        st.session_state["lihat_saran"] = False
        st.rerun()

# Tombol Kotak Saran - untuk TIM & SISWA
if st.session_state["siswa_pilih"] is None:
    jml_baru = len([s for s in st.session_state["saran_list"] if not s.get("balasan")]) if st.session_state["login_role"] == "tim" else len([s for s in st.session_state["saran_list"] if s["pengirim"] == st.session_state["login_nama"] and s.get("balasan")])
    label_saran = f"💬 Kotak Saran / Kritik / Keluhan ({jml_baru} Baru)" if jml_baru > 0 else "💬 Kotak Saran / Kritik / Keluhan"
    if st.button(label_saran, use_container_width=True):
        st.session_state["lihat_saran"] = True
        st.session_state["kategori_pilih"] = None
        st.session_state["lihat_nilai"] = False
        st.session_state["lihat_riwayat"] = False
        catat_aktivitas("Buka Kotak Saran")
        st.rerun()

if st.session_state.get("lihat_saran") and st.session_state["siswa_pilih"] is None:
    tampilkan_kotak_saran()
    st.stop()

if st.session_state.get("lihat_riwayat") and st.session_state["siswa_pilih"] is None:
    tampilkan_riwayat_siswa()
    st.stop()

if st.session_state["lihat_nilai"] and st.session_state["siswa_pilih"] is None:
    tampilkan_daftar_hasil_nilai()
    st.stop()

if st.session_state["siswa_pilih"]:
    nama = st.session_state["siswa_pilih"]
    if st.session_state["login_role"] == "siswa" and nama != st.session_state["login_nama"]:
        st.error("⛔ Kamu hanya boleh ujian atas nama sendiri!")
        if st.button("Kembali"):
            st.session_state["siswa_pilih"] = None
            st.rerun()
        st.stop()
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
        st.warning("🔒 UJIAN BERLANGSUNG - Jangan refresh atau menutup tab. Sisa waktu dihitung oleh server; jawaban yang tersimpan di sesi akan dinilai saat waktu habis.")
        st_autorefresh(interval=1000, key=f"qori_timer_{nama}_{st.session_state['seed_acak']}")
    tampilkan_timer(sisa_detik)
    if st.session_state["waktu_habis"] and not st.session_state["ujian_selesai"]:
        st.error("⛔ WAKTU HABIS! 10 menit sudah selesai. Silakan klik LIHAT NILAI di bawah.")
    if st.session_state["ujian_selesai"]:
        if st.session_state["hasil_ujian"] and st.session_state["hasil_ujian"]["nilai"] < KKM:
            col_r, col_k = st.columns(2)
            with col_r:
                if st.button("🔁 Remedial - Ulangi Lagi Sampai Tuntas", use_container_width=True):
                    for k in list(st.session_state.keys()):
                        if k.startswith("soal_"):
                            del st.session_state[k]
                    st.session_state["seed_acak"] = st.session_state["seed_acak"] + 1
                    st.session_state["soal_acak"] = None
                    st.session_state["waktu_mulai"] = time.time()
                    st.session_state["waktu_habis"] = False
                    st.session_state["ujian_selesai"] = False
                    st.session_state["hasil_ujian"] = None
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
        pilih = st.radio(f"Pilih jawaban No.{i+1}", opsi, key=f"soal_{kat}_{seed}_{i}", index=None, disabled=(kunci_input or st.session_state["waktu_habis"]))
        jawaban_siswa.append(pilih)

    def proses_simpan_nilai(jawaban, kunci_jawaban):
        benar = sum(1 for i, pilihan in enumerate(jawaban)
                    if pilihan and pilihan[0] == kunci_jawaban[i])
        nilai_hitung = int(round((benar / len(kunci_jawaban)) * 100))
        st.session_state["ujian_selesai"] = True
        st.session_state["waktu_habis"] = True if time.time() - st.session_state["waktu_mulai"] >= DURASI_UJIAN else st.session_state["waktu_habis"]
        st.session_state["hasil_ujian"] = {"benar": benar, "nilai": nilai_hitung}
        st.session_state["hasil_semua"][nama] = nilai_hitung
        st.session_state["hitung_ulang"][nama] = st.session_state["hitung_ulang"].get(nama, 0) + 1
        simpan_hasil_database(nama, kat, nilai_hitung, benar, st.session_state["hitung_ulang"][nama])
        catat_aktivitas(f"Selesai Ujian - Nilai {nilai_hitung}")
        try:
            st.query_params.clear()
        except Exception:
            pass

    if st.session_state["waktu_habis"] and not st.session_state["ujian_selesai"]:
        proses_simpan_nilai(jawaban_siswa, kunci)
        st.rerun()

    if not st.session_state["ujian_selesai"]:
        if st.button("✅ LIHAT NILAI SAYA - SELESAI", use_container_width=True):
            proses_simpan_nilai(jawaban_siswa, kunci)
            st.rerun()
    if st.session_state["ujian_selesai"] and st.session_state["hasil_ujian"]:
        hasil = st.session_state["hasil_ujian"]
        benar = hasil["benar"]
        nilai = hasil["nilai"]
        percobaan = st.session_state["hitung_ulang"].get(nama, 1)
        warna_n = "#FF5252" if nilai < KKM else "#FFFFFF"
        st.success(f"🎉 HASIL {nama} - Kelas {kat}")
        st.markdown(f"<div style='background-color: rgba(0,0,0,0.65); padding:15px; border-radius:10px; text-align:center;'><h1 style='color:{warna_n};'>Nilai: {nilai}</h1><p style='color:white;'>Jawaban Benar: {benar} / 25 | Salah / Kosong: {25-benar} | KKM: 75 | Percobaan ke-{percobaan} | {'❌ Belum Tuntas - Silakan klik Remedial di atas untuk mengulang!' if nilai < KKM else '✅ Tuntas!'}</p><p style='color:white;'>Perhitungan: ({benar} ÷ 25) × 100 = {nilai}</p></div>", unsafe_allow_html=True)
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
    prompt = st.text_input("Tulis pertanyaanmu di sini...", placeholder="Tulis pertanyaanmu di sini... Tanya apa saja ya!", label_visibility="collapsed")
    kirim = st.button("Kirim ➤", use_container_width=True)
    if not kirim:
        prompt = None

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    catat_aktivitas(f"Tanya AI: {prompt[:40]}")
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
        elif not api_key:
            jawaban = "Maaf, layanan AI belum dikonfigurasi. Silakan hubungi administrator QORI AI."
            st.markdown(jawaban)
            st.session_state.messages.append({"role": "assistant", "content": jawaban})
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
                st.error("Maaf, QORI AI sedang mengalami gangguan. Silakan coba beberapa saat lagi.")
