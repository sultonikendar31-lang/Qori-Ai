import streamlit as st
import streamlit.components.v1 as components
import base64
import random
import time
import os
import hashlib
import hmac
import html
import csv
import io
import sqlite3
from openai import OpenAI
try:
    from streamlit_autorefresh import st_autorefresh
except:
    st_autorefresh = None

st.set_page_config(page_title="QORI AI", page_icon="🕌", layout="wide")
api_key = st.secrets.get("OPENAI_API_KEY", "")

# ===== DATABASE SQLITE =====
DB = os.environ.get("QORI_DB_PATH", "qori_ai.db")  # Atur ke disk persisten bila tersedia
def db():
    c = sqlite3.connect(DB, check_same_thread=False, timeout=30)
    c.execute("PRAGMA journal_mode=WAL")
    c.execute("PRAGMA foreign_keys=ON")
    c.execute("CREATE TABLE IF NOT EXISTS hasil (nama TEXT PRIMARY KEY, nilai INTEGER, ulang INTEGER)")
    c.execute("CREATE TABLE IF NOT EXISTS aktivitas (id INTEGER PRIMARY KEY AUTOINCREMENT, nama TEXT, kelas TEXT, aktivitas TEXT, jam TEXT, lama TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS saran (id INTEGER PRIMARY KEY AUTOINCREMENT, pengirim TEXT, label TEXT, role TEXT, jenis TEXT, isi TEXT, jam TEXT, balasan TEXT, pembalas TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS ujian_sesi (nama TEXT PRIMARY KEY, mulai REAL NOT NULL, seed INTEGER NOT NULL)")
    c.commit()
    return c
CONN = db()
# Catatan hosting: SQLite lokal cocok untuk uji coba/satu instance. Untuk data produksi
# multi-pengguna di Streamlit Cloud, gunakan PostgreSQL/Supabase atau disk persisten.
def get_hasil():
    return {r[0]: r[1] for r in CONN.execute("SELECT nama,nilai FROM hasil")}
def get_ulang():
    return {r[0]: r[1] for r in CONN.execute("SELECT nama,ulang FROM hasil")}
def simpan_hasil(nama, nilai):
    cur = CONN.execute("SELECT ulang FROM hasil WHERE nama=?", (nama,))
    row = cur.fetchone()
    ulang = (row[0]+1) if row else 1
    CONN.execute("INSERT INTO hasil(nama,nilai,ulang) VALUES(?,?,?) ON CONFLICT(nama) DO UPDATE SET nilai=excluded.nilai, ulang=excluded.ulang", (nama, nilai, ulang))
    CONN.commit()
    return ulang
def get_aktivitas():
    return [{"nama":r[0],"kelas":r[1],"aktivitas":r[2],"jam":r[3],"lama":r[4]} for r in CONN.execute("SELECT nama,kelas,aktivitas,jam,lama FROM aktivitas ORDER BY id DESC")]
def tambah_aktivitas(nama, kelas, aktivitas, jam, lama):
    CONN.execute("INSERT INTO aktivitas(nama,kelas,aktivitas,jam,lama) VALUES(?,?,?,?,?)", (nama, kelas, aktivitas, jam, lama))
    CONN.commit()
def get_saran():
    return [{"id":r[0],"pengirim":r[1],"label":r[2],"role":r[3],"jenis":r[4],"isi":r[5],"jam":r[6],"balasan":r[7] or "","pembalas":r[8] or ""} for r in CONN.execute("SELECT id,pengirim,label,role,jenis,isi,jam,balasan,pembalas FROM saran ORDER BY id DESC")]
def tambah_saran(pengirim, label, role, jenis, isi, jam):
    CONN.execute("INSERT INTO saran(pengirim,label,role,jenis,isi,jam,balasan,pembalas) VALUES(?,?,?,?,?,?,?,?)", (pengirim, label, role, jenis, isi, jam, "", ""))
    CONN.commit()
def balas_saran(sid, balasan, pembalas):
    CONN.execute("UPDATE saran SET balasan=?, pembalas=? WHERE id=?", (balasan, pembalas, sid))
    CONN.commit()
def hapus_saran(sid):
    CONN.execute("DELETE FROM saran WHERE id=?", (sid,))
    CONN.commit()
def simpan_sesi_ujian(nama, mulai, seed):
    CONN.execute("INSERT INTO ujian_sesi(nama,mulai,seed) VALUES(?,?,?) ON CONFLICT(nama) DO UPDATE SET mulai=excluded.mulai, seed=excluded.seed", (nama, mulai, seed))
    CONN.commit()
def ambil_sesi_ujian(nama):
    return CONN.execute("SELECT mulai,seed FROM ujian_sesi WHERE nama=?", (nama,)).fetchone()
def hapus_sesi_ujian(nama):
    CONN.execute("DELETE FROM ujian_sesi WHERE nama=?", (nama,))
    CONN.commit()

# ===== TIM =====
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

for k, v in [("login_nama",None),("login_role",None),("login_jabatan",None),("kategori_pilih",None),("messages",[]),("siswa_pilih",None),("seed_acak",1),("soal_acak",None),("kunci_acak",None),("kat_acak",None),("waktu_mulai",None),("waktu_habis",False),("ujian_selesai",False),("hasil_ujian",None),("lihat_nilai",False),("lihat_riwayat",False),("lihat_saran",False),("lihat_video",True),("waktu_login",None),("sudah_catat_masuk",False),("jawaban_tersimpan",{})]:
    if k not in st.session_state:
        st.session_state[k] = v

DURASI_UJIAN = 10*60
KKM = 75
prompt_awal = None
SYSTEM_PROMPT_KUNCI = "Kamu adalah QORI AI, guru yang ramah dan pintar untuk anak Madrasah Aliyah Al-Barokah. Kamu BEBAS menjawab pertanyaan apa saja: Iqro, Tahsin, Tahfidz, pelajaran sekolah, agama, umum. Jawab Bahasa Indonesia mudah, sopan, islami. Kalau menyebut huruf hijaiyah, WAJIB format: 1. Alif (ا) - dibaca \"A\"."

# ===== CEK PASSWORD =====
def cek_password(nama, password_input):
    """Memeriksa password akun; mempertahankan password lama sesuai permintaan."""
    # Jika USER_PASSWORDS di Streamlit Secrets berisi akun ini, gunakan
    # password/hash yang dikonfigurasi di sana.
    pw_dict = st.secrets.get("USER_PASSWORDS", {})
    stored = pw_dict.get(nama) if hasattr(pw_dict, "get") else None
    if stored:
        # Format: pbkdf2_sha256$<salt_hex>$<digest_hex>.
        # SHA-256 tetap didukung untuk kompatibilitas dengan konfigurasi lama.
        if str(stored).startswith("pbkdf2_sha256$"):
            try:
                _, salt, digest = str(stored).split("$", 2)
                calculated = hashlib.pbkdf2_hmac(
                    "sha256", password_input.encode(), bytes.fromhex(salt), 300_000
                ).hex()
                return hmac.compare_digest(calculated, digest)
            except (ValueError, TypeError):
                return False
        calculated = hashlib.sha256(password_input.encode()).hexdigest()
        return hmac.compare_digest(calculated, str(stored))

    # Password bawaan tetap seperti versi sebelumnya:
    # Tim penyusun = 123, siswa = 321.
    if nama in TIM_PENYUSUN:
        return password_input == "123"
    if nama in DATA_SISWA:
        return password_input == "321"
    return False

def catat_aktivitas(aktivitas):
    if st.session_state.get("login_role") != "siswa": return
    if not st.session_state.get("login_nama"): return
    sekarang = time.time()
    jam = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime(sekarang))
    lama_detik = int(sekarang - st.session_state["waktu_login"]) if st.session_state.get("waktu_login") else 0
    lama = f"{lama_detik//60} mnt {lama_detik%60} dtk" if lama_detik//60>0 else f"{lama_detik} dtk"
    info = DATA_SISWA.get(st.session_state["login_nama"], {})
    tambah_aktivitas(st.session_state["login_nama"], info.get("kategori","-"), aktivitas, jam, lama)

def get_base64(file):
    try:
        with open(file, "rb") as f: return base64.b64encode(f.read()).decode()
    except: return ""

def tampilkan_tim_pembuat():
    st.markdown("""
    <div style='background-color: rgba(255,255,255,0.12); border: 1.5px solid rgba(255,255,255,0.6); padding: 16px; border-radius: 15px; margin-top: 10px;'>
        <p style='color:#F9D423; font-weight:bold; font-size:18px; text-align:center; margin:0 0 12px 0;'>👨‍🎓 Tim Penyusun QORI AI</p>
        <div style='display:flex; flex-wrap:wrap; justify-content:center; gap:10px;'>
            <div style='background-color: rgba(0,0,0,0.55); padding:10px 14px; border-radius:10px; text-align:center; min-width:160px;'><p style='color:#F9D423; font-weight:bold; margin:0; font-size:15px;'>Bapak Muhamad Rais, S.Pd.I</p><p style='color:white; margin:2px 0 0 0; font-size:13px;'>Guru Pamong</p></div>
            <div style='background-color: rgba(0,0,0,0.55); padding:10px 14px; border-radius:10px; text-align:center; min-width:160px;'><p style='color:#F9D423; font-weight:bold; margin:0; font-size:15px;'>Dr. Muhamad Siddiq Asyhari, M.Pd</p><p style='color:white; margin:2px 0 0 0; font-size:13px;'>Dosen Pembimbing</p></div>
            <div style='background-color: rgba(0,0,0,0.55); padding:10px 14px; border-radius:10px; text-align:center; min-width:160px;'><p style='color:#F9D423; font-weight:bold; margin:0; font-size:15px;'>Bapak Syamsul Hadi, S.Pd.I</p><p style='color:white; margin:2px 0 0 0; font-size:13px;'>Kepala MA Al-Barokah</p></div>
            <div style='background-color: rgba(0,0,0,0.55); padding:10px 14px; border-radius:10px; text-align:center; min-width:160px;'><p style='color:#F9D423; font-weight:bold; margin:0; font-size:15px;'>Kendar Sultoni</p><p style='color:white; margin:2px 0 0 0; font-size:13px;'>Mahasiswa / Pembuat Aplikasi</p></div>
        </div>
        <p style='color:white; text-align:center; font-size:12px; margin:10px 0 0 0;'>QORI AI - Madrasah Aliyah Al-Barokah | Media Belajar Iqro, Tahsin & Tahfidz</p>
    </div>
    """, unsafe_allow_html=True)

bg = get_base64("background.jpeg")
if bg:
    st.markdown(f"""<style>.stApp {{ background-image: url("data:image/jpeg;base64,{bg}") !important; background-size: cover !important; background-position: center !important; background-attachment: fixed !important; }} .stApp::before {{ content:""; position:fixed; top:0; left:0; right:0; bottom:0; background: rgba(0,0,0,0.55); z-index:0; pointer-events:none; }} .block-container {{ position:relative; z-index:1; padding-top:20px !important; max-width:900px !important; }} .block-container p, .block-container span, .block-container label, .block-container h2 {{ color:white !important; }} div[data-testid="stButton"] > button {{ background-color: rgba(255,255,255,0.25) !important; color:white !important; border:1.5px solid rgba(255,255,255,0.8) !important; font-weight:bold !important; font-size:17px !important; border-radius:12px !important; }} [data-testid="stChatMessage"] {{ background-color: rgba(10,35,25,0.97) !important; border:2px solid #F9D423 !important; border-radius:14px !important; }} [data-testid="stChatMessage"] p {{ color:#FFF !important; font-size:20px !important; line-height:2.0 !important; }} [data-testid="stAlert"] {{ background-color: #FFD6D6 !important; }} [data-testid="stAlert"] p, [data-testid="stAlert"] span, [data-testid="stAlert"] div {{ color: #000000 !important; }} </style>""", unsafe_allow_html=True)

st.markdown("""<div style='background-color: rgba(20,50,35,0.92); padding: 25px; border-radius: 15px; text-align:center;'><h1 style='color:#F9D423; margin:0; font-size:36px;'>🕌 QORI AI Madrasah Aliyah Al-Barokah</h1><p style='color:white; margin-top:10px; font-size:16px;'>Assalamualaikum warahmatullahi wabarakatuh! Tanya apa saja, QORI AI siap membantu</p></div>""", unsafe_allow_html=True)

# ===== LOGIN + VIDEO PEMBUKA =====
if st.session_state["login_nama"] is None:
    if st.session_state.get("lihat_video", True) and os.path.exists("video_pembuka.mp4"):
        st.markdown("<div style='background-color: rgba(0,0,0,0.65); padding:12px; border-radius:12px; text-align:center; margin-top:15px;'><p style='color:#F9D423; font-weight:bold; margin:0;'>🎬 Video Pembuka - Peringatan Hari Santri Nasional</p><p style='color:white; font-size:13px; margin:4px 0 0 0;'>MA Al-Barokah | 22 Oktober 2026</p></div>", unsafe_allow_html=True)
        st.video("video_pembuka.mp4")
        if st.button("⏭️ Lewati Video - Langsung Isi Nama", use_container_width=True):
            st.session_state["lihat_video"] = False
            st.rerun()
        st.write("")
    st.markdown("""<div style='background-color: rgba(255,255,255,0.12); border: 1.5px solid #F9D423; padding: 20px; border-radius: 15px; margin-top: 15px; text-align:center;'><h2 style='color:#F9D423; margin:0;'>🔐 Silakan Masukkan Nama & Password</h2><p style='color:white; margin-top:8px;'>Untuk masuk ke QORI AI</p></div>""", unsafe_allow_html=True)
    st.write("")
    nama_input = st.text_input("✍️ Nama Lengkap:", placeholder="Tulis nama lengkapmu...", key="input_nama_login")
    pw_input = st.text_input("🔑 Password:", type="password", placeholder="Masukkan passwordmu...", key="input_pw_login")
    if not st.secrets.get("USER_PASSWORDS", {}):
        st.error("Konfigurasi USER_PASSWORDS belum tersedia. Admin perlu mengatur password setiap akun di Streamlit Secrets.")
    if st.button("🚪 Masuk ke QORI AI", use_container_width=True):
        nama_bersih = nama_input.strip().upper()
        if not nama_bersih or not pw_input:
            st.warning("⚠️ Nama & Password harus diisi!")
        elif nama_bersih in TIM_PENYUSUN or nama_bersih in DATA_SISWA:
            if not cek_password(nama_bersih, pw_input):
                st.error("❌ Password salah! Tanya ke guru / tim kalau lupa.")
            else:
                st.session_state["login_nama"] = nama_bersih
                if nama_bersih in TIM_PENYUSUN:
                    st.session_state["login_role"] = "tim"
                    st.session_state["login_jabatan"] = TIM_PENYUSUN[nama_bersih]
                    tampil = NAMA_LENGKAP_TIM.get(nama_bersih, nama_bersih)
                else:
                    st.session_state["login_role"] = "siswa"
                    st.session_state["login_jabatan"] = f"Siswa {DATA_SISWA[nama_bersih]['kategori']}"
                    tampil = nama_bersih
                st.session_state["waktu_login"] = time.time()
                st.session_state["sudah_catat_masuk"] = False
                st.success(f"✅ Selamat datang, {tampil}")
                time.sleep(0.5)
                st.rerun()
        else:
            st.error("❌ Nama tidak ditemukan! Cek lagi ejaannya, atau tanya ke guru.")
    st.write("")
    st.stop()

# ===== BANNER SELAMAT DATANG =====
if st.session_state["login_role"] == "siswa":
    kelas_login = DATA_SISWA.get(st.session_state["login_nama"], {}).get("kategori", "")
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
        if st.session_state["login_role"] == "siswa": catat_aktivitas("Keluar Aplikasi")
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
        st.session_state["lihat_video"] = True
        st.rerun()

if st.session_state["siswa_pilih"] is None and st.session_state["login_role"] == "tim":
    tampilkan_tim_pembuat()
    hasil_dashboard = get_hasil()
    jumlah_tuntas = sum(1 for v in hasil_dashboard.values() if v >= KKM)
    jumlah_belum = sum(1 for v in hasil_dashboard.values() if v < KKM)
    jumlah_belum_ujian = max(0, len(DATA_SISWA) - len(hasil_dashboard))
    st.markdown("### 📊 Ringkasan Dashboard Tim")
    d1, d2, d3, d4 = st.columns(4)
    d1.metric("Jumlah Siswa", len(DATA_SISWA))
    d2.metric("Sudah Ujian", len(hasil_dashboard))
    d3.metric("Tuntas", jumlah_tuntas)
    d4.metric("Belum Ujian", jumlah_belum_ujian)
    if jumlah_belum:
        st.info(f"{jumlah_belum} siswa memperoleh nilai di bawah KKM dan perlu tindak lanjut/remedial.")
st.write("")

# ===== DATA SOAL =====
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
    data_asli = SOAL_ALL[kat]; kunci_asli = KUNCI[kat]
    gabung = list(zip(data_asli, kunci_asli)); rng.shuffle(gabung)
    soal_baru=[]; kunci_baru=[]
    for (teks_soal, opsi_asli), kunci_lama in gabung:
        isi_jawaban=[]
        for o in opsi_asli:
            if ". " in o: isi_jawaban.append(o.split(". ",1)[1])
            elif " - " in o: isi_jawaban.append(o.split(" - ",1)[1])
            else: isi_jawaban.append(o)
        idx_benar = ord(kunci_lama)-ord("A") if len(opsi_asli)==5 else (0 if kunci_lama=="B" else 1)
        isi_benar = isi_jawaban[idx_benar]; rng.shuffle(isi_jawaban)
        opsi_baru=[]; kb=""
        if len(opsi_asli)==5:
            for i, isi in enumerate(isi_jawaban):
                h=["A","B","C","D","E"][i]; opsi_baru.append(f"{h}. {isi}")
                if isi==isi_benar: kb=h
        else:
            for isi in isi_jawaban:
                lab="B" if isi=="Benar" else "S"; opsi_baru.append(f"{lab} - {isi}")
                if isi==isi_benar: kb=lab
        teks_bersih = teks_soal.split(". ",1)[1] if ". " in teks_soal[:5] else teks_soal
        soal_baru.append((teks_bersih, opsi_baru)); kunci_baru.append(kb)
    return soal_baru, kunci_baru

def tampilkan_daftar(kategori):
    if st.session_state["login_role"]=="siswa":
        if DATA_SISWA.get(st.session_state["login_nama"],{}).get("kategori")!=kategori: return
        daftar=[st.session_state["login_nama"]]
    else:
        if kategori=="Iqro":
            daftar=["MUHAMAD HARTANTO","DAFFAN OKTAFFIL HIDAYAT"]
        elif kategori=="Tahsin":
            daftar=["FRISCHA BUNGA LESTARI","RAIHAN","ANGGA FADILLAH","ANDY RAMADANI ABDULLAH"]
        else:
            daftar=[k for k,v in DATA_SISWA.items() if v["kategori"]=="Tahfidz"]
    for item in daftar:
        label = item if st.session_state["login_role"]=="tim" else f"▶️ Mulai Ujian - {item}"
        if st.button(label, key=f"{kategori}-{item}"):
            st.session_state["siswa_pilih"]=item; st.session_state["seed_acak"]+=1; st.session_state["soal_acak"]=None; st.session_state["waktu_mulai"]=time.time(); simpan_sesi_ujian(item, st.session_state["waktu_mulai"], st.session_state["seed_acak"]); st.session_state["waktu_habis"]=False; st.session_state["ujian_selesai"]=False; st.session_state["hasil_ujian"]=None; st.session_state["lihat_nilai"]=False; st.session_state["lihat_riwayat"]=False; st.session_state["lihat_saran"]=False; st.session_state["jawaban_tersimpan"]={}
            catat_aktivitas(f"Mulai Ujian - {kategori}")
            st.rerun()

# ===== MENU UTAMA =====
if st.session_state["siswa_pilih"] is None and not st.session_state["lihat_nilai"]:
    c1,c2,c3,c4 = st.columns(4)
    with c1: klik_iqro = st.button("📖 Iqro", use_container_width=True)
    with c2: klik_tahsin = st.button("📗 Tahsin", use_container_width=True)
    with c3: klik_tahfidz = st.button("⭐ Tahfidz", use_container_width=True)
    with c4: klik_nilai = st.button("📊 Daftar Hasil Nilai", use_container_width=True)
    if klik_iqro: st.session_state["kategori_pilih"] = None if st.session_state["kategori_pilih"]=="Iqro" else "Iqro"; st.session_state["lihat_nilai"]=False; st.session_state["lihat_riwayat"]=False; st.session_state["lihat_saran"]=False; catat_aktivitas("Buka Kelas Iqro")
    if klik_tahsin: st.session_state["kategori_pilih"] = None if st.session_state["kategori_pilih"]=="Tahsin" else "Tahsin"; st.session_state["lihat_nilai"]=False; st.session_state["lihat_riwayat"]=False; st.session_state["lihat_saran"]=False; catat_aktivitas("Buka Kelas Tahsin")
    if klik_tahfidz: st.session_state["kategori_pilih"] = None if st.session_state["kategori_pilih"]=="Tahfidz" else "Tahfidz"; st.session_state["lihat_nilai"]=False; st.session_state["lihat_riwayat"]=False; st.session_state["lihat_saran"]=False; catat_aktivitas("Buka Kelas Tahfidz")
    if klik_nilai: st.session_state["lihat_nilai"]=True; st.session_state["kategori_pilih"]=None; st.session_state["lihat_riwayat"]=False; st.session_state["lihat_saran"]=False; catat_aktivitas("Buka Daftar Hasil Nilai")
    if st.session_state["kategori_pilih"]:
        cc1,cc2,cc3 = st.columns(3)
        if st.session_state["kategori_pilih"]=="Iqro":
            with cc1: tampilkan_daftar("Iqro")
        if st.session_state["kategori_pilih"]=="Tahsin":
            with cc2: tampilkan_daftar("Tahsin")
        if st.session_state["kategori_pilih"]=="Tahfidz":
            with cc3: tampilkan_daftar("Tahfidz")

if st.session_state["login_role"]=="tim" and st.session_state["siswa_pilih"] is None:
    if st.button("📋 Riwayat / Story Siswa (Khusus Tim)", use_container_width=True):
        st.session_state["lihat_riwayat"]=True; st.session_state["kategori_pilih"]=None; st.session_state["lihat_nilai"]=False; st.session_state["lihat_saran"]=False; st.rerun()
if st.session_state["siswa_pilih"] is None:
    jml_baru = len([s for s in get_saran() if not s["balasan"]]) if st.session_state["login_role"]=="tim" else len([s for s in get_saran() if s["pengirim"]==st.session_state["login_nama"] and s["balasan"]])
    label_saran = f"💬 Kotak Saran / Kritik / Keluhan ({jml_baru} Baru)" if jml_baru>0 else "💬 Kotak Saran / Kritik / Keluhan"
    if st.button(label_saran, use_container_width=True):
        st.session_state["lihat_saran"]=True; st.session_state["kategori_pilih"]=None; st.session_state["lihat_nilai"]=False; st.session_state["lihat_riwayat"]=False; catat_aktivitas("Buka Kotak Saran"); st.rerun()

# ===== KOTAK SARAN =====
if st.session_state.get("lihat_saran") and st.session_state["siswa_pilih"] is None:
    st.markdown("<div style='background-color: rgba(20,50,35,0.95); padding:18px; border-radius:15px; text-align:center; border:2px solid #F9D423;'><h2 style='color:#F9D423; margin:0;'>💬 Kotak Saran / Kritik / Keluhan</h2></div>", unsafe_allow_html=True)
    st.write("")
    jenis_saran = st.selectbox("Jenis Pesan:", ["💡 Saran","📝 Kritik","😟 Keluhan"], key="jenis_saran")
    isi_saran = st.text_area("Isi Pesan:", placeholder="Tulis saran / kritik / keluhanmu...", height=120, key="isi_saran")
    if st.button("📩 Kirim Saran / Kritik / Keluhan", use_container_width=True):
        if not isi_saran.strip(): st.warning("⚠️ Isi pesannya masih kosong!")
        else:
            if st.session_state["login_role"]=="siswa":
                label = f"{st.session_state['login_nama']} | Kelas: {DATA_SISWA.get(st.session_state['login_nama'],{}).get('kategori','-')}"
            else:
                label = f"{NAMA_LENGKAP_TIM.get(st.session_state['login_nama'], st.session_state['login_nama'])} | {TIM_PENYUSUN.get(st.session_state['login_nama'],'Tim')}"
            tambah_saran(st.session_state["login_nama"], label, st.session_state["login_role"], jenis_saran, isi_saran.strip(), time.strftime("%d/%m/%Y %H:%M", time.localtime(time.time())))
            catat_aktivitas(f"Kirim {jenis_saran}"); st.success("✅ Terima kasih! Sudah terkirim ke Tim."); st.rerun()
    st.write("")
    semua = get_saran()
    daftar = [s for s in semua if s["pengirim"]==st.session_state["login_nama"]] if st.session_state["login_role"]=="siswa" else semua
    if not daftar: st.info("Belum ada pesan.")
    else:
        for s in daftar:
            st.markdown(f"<div style='background-color: rgba(255,255,255,0.12); border:1.5px solid rgba(255,255,255,0.5); padding:14px; border-radius:12px;'><p style='color:#F9D423; font-weight:bold; margin:0;'>{html.escape(str(s['jenis']))} - {html.escape(str(s['label']))}</p><p style='color:#AAAAAA; font-size:12px;'>{html.escape(str(s['jam']))}</p><p style='color:white;'>{html.escape(str(s['isi']))}</p></div>", unsafe_allow_html=True)
            if s["balasan"]: st.markdown(f"<div style='background-color: rgba(20,50,35,0.9); border:1.5px solid #F9D423; padding:12px; border-radius:12px; margin:5px 0 12px 20px;'><p style='color:#F9D423; font-weight:bold; margin:0;'>↩️ Balasan dari {html.escape(str(s['pembalas']))}:</p><p style='color:white;'>{html.escape(str(s['balasan']))}</p></div>", unsafe_allow_html=True)
            if st.session_state["login_role"]=="tim":
                balas = st.text_input("Balas pesan ini (Tim):", key=f"balas_{s['id']}")
                cb1,cb2 = st.columns(2)
                with cb1:
                    if st.button("↩️ Kirim Balasan", key=f"kirim_balas_{s['id']}", use_container_width=True):
                        if balas.strip():
                            balas_saran(s['id'], balas.strip(), f"{NAMA_LENGKAP_TIM.get(st.session_state['login_nama'], st.session_state['login_nama'])} | {TIM_PENYUSUN.get(st.session_state['login_nama'],'Tim')}")
                            st.rerun()
                with cb2:
                    if st.button("🗑️ Hapus", key=f"hapus_saran_{s['id']}", use_container_width=True):
                        hapus_saran(s['id']); st.rerun()
    st.write("")
    if st.button("⬅️ Tutup Kotak Saran", use_container_width=True):
        st.session_state["lihat_saran"]=False; st.rerun()
    st.stop()

# ===== RIWAYAT =====
if st.session_state.get("lihat_riwayat") and st.session_state["siswa_pilih"] is None:
    st.markdown("<div style='background-color: rgba(20,50,35,0.95); padding:18px; border-radius:15px; text-align:center; border:2px solid #F9D423;'><h2 style='color:#F9D423; margin:0;'>📋 Riwayat / Story Siswa</h2><p style='color:white;'>Khusus Tim - Siswa TIDAK bisa lihat</p></div>", unsafe_allow_html=True)
    st.write("")
    riw = get_aktivitas()
    if not riw: st.info("Belum ada aktivitas.")
    else:
        rows=""
        for i,r in enumerate(riw,1):
            rows+=f"<tr><td style='padding:10px; text-align:center; color:white;'>{i}</td><td style='padding:10px; color:white; font-weight:bold;'>{html.escape(str(r['nama']))}</td><td style='padding:10px; text-align:center; color:white;'>{html.escape(str(r['kelas']))}</td><td style='padding:10px; color:white;'>{html.escape(str(r['aktivitas']))}</td><td style='padding:10px; text-align:center; color:white;'>{html.escape(str(r['jam']))}</td><td style='padding:10px; text-align:center; color:#F9D423;'>{html.escape(str(r['lama']))}</td></tr>"
        st.markdown(f"<div style='background-color: rgba(0,0,0,0.75); padding:15px; border-radius:15px;'><table style='width:100%;'><tr style='background-color:#F9D423;'><th style='padding:10px; color:#000;'>No</th><th style='padding:10px; color:#000;'>Nama</th><th style='padding:10px; color:#000;'>Kelas</th><th style='padding:10px; color:#000;'>Buka Apa</th><th style='padding:10px; color:#000;'>Jam</th><th style='padding:10px; color:#000;'>Lama</th></tr>{rows}</table></div>", unsafe_allow_html=True)
    st.write("")
    if st.button("⬅️ Tutup Riwayat", use_container_width=True):
        st.session_state["lihat_riwayat"]=False; st.rerun()
    st.stop()

# ===== DAFTAR NILAI =====
if st.session_state["lihat_nilai"] and st.session_state["siswa_pilih"] is None:
    st.markdown("<div style='background-color: rgba(20,50,35,0.95); padding:18px; border-radius:15px; text-align:center; border:2px solid #F9D423;'><h2 style='color:#F9D423; margin:0;'>📊 Daftar Hasil Nilai</h2><p style='color:white;'>KKM = 75 | Nilai >= 75 = Tuntas | Nilai < 75 = Belum Tuntas</p></div>", unsafe_allow_html=True)
    st.write("")
    hasil = get_hasil(); ulang = get_ulang()
    daftar_tampil = [st.session_state["login_nama"]] if st.session_state["login_role"]=="siswa" else list(DATA_SISWA.keys())
    rows=""; tuntas=belum=belum_ujian=0
    for no,nama in enumerate(daftar_tampil,1):
        info=DATA_SISWA[nama]
        if nama not in hasil:
            rows+=f"<tr><td style='padding:10px; text-align:center; color:white;'>{no}</td><td style='padding:10px; color:white; font-weight:bold;'>{nama}</td><td style='padding:10px; text-align:center; color:white;'>{info['jk']}</td><td style='padding:10px; text-align:center; color:white;'>{info['kategori']}</td><td style='padding:10px; text-align:center; color:#AAAAAA; font-weight:bold; font-size:20px;'>-</td><td style='padding:10px; text-align:center; color:#AAAAAA;'>⏳ Belum Mengerjakan</td><td style='padding:10px; text-align:center; color:#AAAAAA;'>-</td></tr>"; belum_ujian+=1
        else:
            nilai=hasil[nama]; u=ulang.get(nama,1)
            if nilai>=KKM: warna="#FFFFFF"; ket="✅ Tuntas"; wk="#4CAF50"; tuntas+=1
            else: warna="#FF5252"; ket="❌ Belum Tuntas"; wk="#FF5252"; belum+=1
            rows+=f"<tr><td style='padding:10px; text-align:center; color:white;'>{no}</td><td style='padding:10px; color:white; font-weight:bold;'>{nama}</td><td style='padding:10px; text-align:center; color:white;'>{info['jk']}</td><td style='padding:10px; text-align:center; color:white;'>{info['kategori']}</td><td style='padding:10px; text-align:center; color:{warna}; font-weight:bold; font-size:20px;'>{nilai}</td><td style='padding:10px; text-align:center; color:{wk}; font-weight:bold;'>{ket}</td><td style='padding:10px; text-align:center; color:white;'>{u}x</td></tr>"
    st.markdown(f"<div style='background-color: rgba(0,0,0,0.75); padding:15px; border-radius:15px;'><p style='color:white; text-align:center;'>Total: {len(daftar_tampil)} | ⏳ Belum: {belum_ujian} | ✅ Tuntas: {tuntas} | ❌ Belum Tuntas: {belum}</p><table style='width:100%;'><tr style='background-color:#F9D423;'><th style='padding:10px; color:#000;'>No</th><th style='padding:10px; color:#000;'>Nama</th><th style='padding:10px; color:#000;'>JK</th><th style='padding:10px; color:#000;'>Kategori</th><th style='padding:10px; color:#000;'>Nilai</th><th style='padding:10px; color:#000;'>Ket</th><th style='padding:10px; color:#000;'>Ulang</th></tr>{rows}</table></div>", unsafe_allow_html=True)
    if st.session_state["login_role"] == "tim":
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Nama", "Jenis Kelamin", "Kategori", "Nilai", "Status", "Jumlah Ujian"])
        for nama_export in daftar_tampil:
            info_export = DATA_SISWA[nama_export]
            nilai_export = hasil.get(nama_export)
            writer.writerow([nama_export, info_export["jk"], info_export["kategori"], nilai_export if nilai_export is not None else "", "Tuntas" if nilai_export is not None and nilai_export >= KKM else ("Belum Tuntas" if nilai_export is not None else "Belum Ujian"), ulang.get(nama_export, 0)])
        st.download_button("⬇️ Unduh Daftar Nilai (CSV - bisa dibuka di Excel)", data="\ufeff" + output.getvalue(), file_name="daftar_nilai_qori_ai.csv", mime="text/csv", use_container_width=True)
    st.write("")
    if st.button("⬅️ Tutup Daftar Nilai", use_container_width=True):
        st.session_state["lihat_nilai"]=False; st.rerun()
    st.stop()

# ===== UJIAN =====
if st.session_state["siswa_pilih"]:
    nama = st.session_state["siswa_pilih"]
    if st.session_state["login_role"]=="siswa" and nama!=st.session_state["login_nama"]:
        st.error("⛔ Kamu hanya boleh ujian atas nama sendiri!")
        if st.button("Kembali"): st.session_state["siswa_pilih"]=None; st.rerun()
        st.stop()
    info = DATA_SISWA.get(nama, {"kategori":"Iqro","level":"Pemula","jk":"-"})
    kat = info["kategori"]
    if st.session_state["waktu_mulai"] is None:
        sesi_tersimpan = ambil_sesi_ujian(nama)
        if sesi_tersimpan:
            st.session_state["waktu_mulai"] = sesi_tersimpan[0]
            st.session_state["seed_acak"] = sesi_tersimpan[1]
        else:
            st.session_state["waktu_mulai"] = time.time()
            simpan_sesi_ujian(nama, st.session_state["waktu_mulai"], st.session_state["seed_acak"])
    sisa = DURASI_UJIAN - (time.time()-st.session_state["waktu_mulai"])
    if sisa<=0: sisa=0; st.session_state["waktu_habis"]=True
    if not st.session_state["ujian_selesai"] and st_autorefresh:
        st_autorefresh(interval=1000, key="timer_refresh")
    menit=int(sisa//60); detik=int(sisa%60)
    st.markdown(f"<div style='background-color: rgba(20,50,35,0.92); padding:20px; border-radius:15px; text-align:center;'><h2 style='color:#F9D423; margin:0;'>Assalamualaikum, {nama} 👋</h2><p style='color:white;'>Kelas: {kat} | Soal: 25 | Nilai: Benar x 4 | Waktu: 10 Menit | KKM: 75 | Sisa: {menit:02d}:{detik:02d}</p></div>", unsafe_allow_html=True)
    if not st.session_state["ujian_selesai"]:
        st.warning("🔒 Jangan tutup tab saat ujian! Jawabanmu tersimpan otomatis di sesi ini.")
    if st.session_state["soal_acak"] is None or st.session_state["kat_acak"]!=kat:
        soal_list, kunci = buat_soal_acak(kat, st.session_state["seed_acak"])
        st.session_state["soal_acak"]=soal_list; st.session_state["kunci_acak"]=kunci; st.session_state["kat_acak"]=kat
    else:
        soal_list=st.session_state["soal_acak"]; kunci=st.session_state["kunci_acak"]
    if st.session_state["waktu_habis"] and not st.session_state["ujian_selesai"]:
        benar=0
        for i in range(25):
            pilih = st.session_state["jawaban_tersimpan"].get(i)
            if pilih and pilih[0]==kunci[i]: benar+=1
        nilai=int((benar/25)*100)
        st.session_state["ujian_selesai"]=True; st.session_state["hasil_ujian"]={"benar":benar,"nilai":nilai}
        simpan_hasil(nama, nilai); hapus_sesi_ujian(nama); catat_aktivitas(f"Selesai Ujian (Waktu Habis) - Nilai {nilai}"); st.rerun()
    st.markdown(f"<h2 style='color:white; background-color: rgba(0,0,0,0.65); padding:10px; border-radius:10px; text-align:center;'>📝 Soal {kat} - Kelas XI MA</h2>", unsafe_allow_html=True)
    jawaban=[]
    for i,(soal,opsi) in enumerate(soal_list):
        st.markdown(f"<div style='background-color: rgba(0,0,0,0.65); padding:12px; border-radius:10px;'><p style='color:white; font-weight:bold; font-size:17px; margin:0;'>{i+1}. {soal}</p></div>", unsafe_allow_html=True)
        idx_default = opsi.index(st.session_state["jawaban_tersimpan"][i]) if i in st.session_state["jawaban_tersimpan"] and st.session_state["jawaban_tersimpan"][i] in opsi else None
        pilih = st.radio(f"Pilih jawaban No.{i+1}", opsi, key=f"soal_{kat}_{st.session_state['seed_acak']}_{i}", index=idx_default, disabled=st.session_state["ujian_selesai"])
        if pilih: st.session_state["jawaban_tersimpan"][i]=pilih
        jawaban.append(pilih)
    if not st.session_state["ujian_selesai"]:
        if st.button("✅ LIHAT NILAI SAYA - SELESAI", use_container_width=True):
            benar=sum(1 for i,p in enumerate(jawaban) if p and p[0]==kunci[i])
            nilai=int((benar/25)*100)
            st.session_state["ujian_selesai"]=True; st.session_state["hasil_ujian"]={"benar":benar,"nilai":nilai}
            simpan_hasil(nama, nilai); hapus_sesi_ujian(nama); catat_aktivitas(f"Selesai Ujian - Nilai {nilai}"); st.rerun()
    if st.session_state["ujian_selesai"] and st.session_state["hasil_ujian"]:
        h=st.session_state["hasil_ujian"]; benar=h["benar"]; nilai=h["nilai"]
        warna="#FF5252" if nilai<KKM else "#FFFFFF"
        st.success(f"🎉 HASIL {nama} - Kelas {kat}")
        st.markdown(f"<div style='background-color: rgba(0,0,0,0.65); padding:15px; border-radius:10px; text-align:center;'><h1 style='color:{warna};'>Nilai: {nilai}</h1><p style='color:white;'>Benar: {benar} / 25 | KKM: 75 | {'❌ Belum Tuntas - Klik Remedial di bawah!' if nilai<KKM else '✅ Tuntas!'}</p><p style='color:white;'>Perhitungan: ({benar} ÷ 25) × 100 = {nilai}</p></div>", unsafe_allow_html=True)
        if nilai==100: st.balloons()
        st.markdown("<div style='background-color: rgba(0,0,0,0.65); padding:10px; border-radius:10px;'><p style='color:white; font-weight:bold;'>Pembahasan Kunci Jawaban:</p></div>", unsafe_allow_html=True)
        for i in range(25): st.markdown(f"<p style='color:white;'>No.{i+1} = {kunci[i]}</p>", unsafe_allow_html=True)
        col_r,col_k = st.columns(2)
        with col_r:
            if nilai<KKM:
                if st.button("🔁 Remedial - Ulangi Lagi", use_container_width=True):
                    for k in list(st.session_state.keys()):
                        if k.startswith("soal_"): del st.session_state[k]
                    st.session_state["seed_acak"]+=1; st.session_state["soal_acak"]=None; st.session_state["waktu_mulai"]=time.time(); simpan_sesi_ujian(nama, st.session_state["waktu_mulai"], st.session_state["seed_acak"]); st.session_state["waktu_habis"]=False; st.session_state["ujian_selesai"]=False; st.session_state["hasil_ujian"]=None; st.session_state["jawaban_tersimpan"]={}; st.rerun()
        with col_k:
            if st.button("🏠 Kembali ke Beranda", use_container_width=True):
                hapus_sesi_ujian(nama)
                st.session_state["siswa_pilih"]=None; st.session_state["soal_acak"]=None; st.session_state["waktu_mulai"]=None; st.session_state["waktu_habis"]=False; st.session_state["ujian_selesai"]=False; st.session_state["hasil_ujian"]=None; st.session_state["kategori_pilih"]=None; st.session_state["jawaban_tersimpan"]={}; st.rerun()
    st.stop()

# ===== CHAT QORI AI =====
if st.session_state["messages"]:
    for idx,m in enumerate(st.session_state["messages"]):
        with st.chat_message(m["role"]):
            st.markdown(m["content"])
            if st.button("🗑️ Hapus pesan ini", key=f"hapus_{idx}"):
                del st.session_state["messages"][idx]; st.rerun()
    if st.button("🗑️ Hapus Semua Chat", use_container_width=True):
        st.session_state["messages"]=[]; st.rerun()
prompt = st.text_input("Tulis pertanyaanmu di sini...", placeholder="Tulis pertanyaanmu di sini... Tanya apa saja ya!", label_visibility="collapsed")
kirim = st.button("Kirim ➤", use_container_width=True)
if kirim and prompt:
    st.session_state.messages.append({"role":"user","content":prompt})
    catat_aktivitas(f"Tanya AI: {prompt[:40]}")
    with st.chat_message("user"): st.markdown(prompt)
    with st.chat_message("assistant"):
        if not api_key: st.markdown("Maaf, API Key belum dipasang di Secrets.")
        else:
            try:
                client=OpenAI(api_key=api_key)
                riwayat_chat = [m for m in st.session_state["messages"][-20:] if m.get("role") in ("user", "assistant")]
                res=client.chat.completions.create(model="gpt-4o-mini", messages=[{"role":"system","content":SYSTEM_PROMPT_KUNCI}] + riwayat_chat, temperature=0.7, max_tokens=800, timeout=45)
                jawaban=res.choices[0].message.content; st.markdown(jawaban); st.session_state.messages.append({"role":"assistant","content":jawaban})
            except Exception:
                st.error("Maaf, QORI AI sedang mengalami gangguan. Silakan coba kembali beberapa saat lagi.")
