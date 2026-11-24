import streamlit as st
import streamlit.components.v1 as components
import os
try:
    from supabase import create_client
except ImportError:
    create_client = None

@st.cache_resource(show_spinner=False)
def get_supabase_client():
    url = key = None
    try:
        url = st.secrets.get("SUPABASE_URL")
        key = st.secrets.get("SUPABASE_ANON_KEY")
    except Exception:
        pass
    url = url or os.getenv("SUPABASE_URL")
    key = key or os.getenv("SUPABASE_ANON_KEY")
    if not url or not key:
        return None, "SUPABASE_URL atau SUPABASE_ANON_KEY belum diatur."
    if create_client is None:
        return None, "Paket supabase belum terpasang. Jalankan pip install -r requirements.txt."
    try:
        return create_client(url, key), None
    except Exception as exc:
        return None, f"Gagal membuat klien Supabase: {exc}"

@st.cache_data(ttl=60, show_spinner=False)
def load_students():
    client, error = get_supabase_client()
    if error:
        return [], error
    try:
        result = client.table("siswa").select("*").execute()
        return result.data or [], None
    except Exception as exc:
        return [], f"Tidak dapat membaca tabel public.siswa: {exc}"

# ============================================================
# QORI AI - Islamic Learning Management System
# Dashboard UI (Streamlit)
# Jalankan: streamlit run app.py
# ============================================================

st.set_page_config(
    page_title="QORI AI | Dashboard",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- CSS ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');

:root {
  --navy:#092653; --blue:#1677e8; --ink:#102448; --muted:#61718d;
  --green:#08a979; --purple:#843fe0;
}
html, body, [class*="css"] { font-family:'Poppins',sans-serif; }
.stApp { background:linear-gradient(135deg,#eef4ff 0%,#f8faff 55%,#edf3ff 100%); color:var(--ink); }
.block-container { padding-top:1.2rem; padding-bottom:2rem; max-width:1600px; }
[data-testid="stSidebar"] { background:linear-gradient(180deg,#08234d,#10396d); }
[data-testid="stSidebar"] * { color:#fff !important; }
[data-testid="stSidebar"] .stButton button {
  text-align:left; border:0; border-radius:12px; background:transparent;
  color:white; font-weight:600; padding:10px 12px;
}
[data-testid="stSidebar"] .stButton button:hover { background:#1b67bd; }
.brand { text-align:center; padding:10px 4px 24px; }
.brand-icon { font-size:42px; }
.brand h1 { font-size:29px; line-height:1; margin:8px 0 5px; color:white; font-weight:800; }
.brand p { font-size:11px; color:#d5e5ff; margin:0; }
.side-note { margin-top:50px; padding:14px; border-radius:14px; background:#ffffff14; color:#d9e8ff; font-size:12px; }
.welcome { display:flex; justify-content:space-between; align-items:center; margin-bottom:16px; }
.welcome h2 { margin:0; font-size:25px; font-weight:800; color:#102448; }
.welcome p { margin:2px 0 0; color:#5d7194; font-size:13px; }
.pill { background:#e1edff; color:#1459ae; border-radius:30px; padding:9px 15px; font-weight:600; font-size:12px; }
.hero {
  border-radius:23px; padding:28px 34px; min-height:225px; color:white;
  background:radial-gradient(circle at 88% 20%,#1d75b9 0,#103d75 30%,#092653 75%);
  box-shadow:0 12px 28px #0b326326; position:relative; overflow:hidden;
}
.hero:after { content:'☪'; position:absolute; right:4%; top:-65px; font-size:260px; color:#ffffff0d; }
.hero-kicker { font-size:13px; color:#b8dcff; letter-spacing:2px; font-weight:700; }
.hero h1 { font-size:52px; line-height:1.05; margin:8px 0; font-weight:800; letter-spacing:1px; }
.hero h1 span { color:#5ce0e0; }
.hero p { font-size:15px; color:#e0edff; max-width:650px; margin:0 0 18px; }
.hero-tags { display:flex; flex-wrap:wrap; gap:9px; }
.hero-tag { border:1px solid #b5d8ff8a; background:#ffffff12; padding:8px 14px; border-radius:30px; font-size:12px; font-weight:600; }
.hero-art { position:absolute; right:5%; bottom:20px; font-size:100px; opacity:.95; filter:drop-shadow(0 10px 12px #0005); }
.section-title { font-size:18px; font-weight:800; color:#102448; margin:18px 0 10px; }
.mode-card { border-radius:18px; padding:19px 20px; color:white; min-height:145px; box-shadow:0 8px 20px #153b6b20; }
.mode-card h3 { margin:0 0 5px; font-size:20px; font-weight:800; }
.mode-card p { font-size:12px; line-height:1.5; margin:0 0 13px; opacity:.95; }
.mode-card .symbol { font-size:30px; float:right; margin-left:10px; }
.mode-card a { color:#14315b; background:#fff; padding:7px 15px; border-radius:30px; text-decoration:none; font-size:12px; font-weight:700; }
.iqro { background:linear-gradient(120deg,#08a978,#12cba0); }
.tahsin { background:linear-gradient(120deg,#1677e8,#0752a8); }
.tahfidz { background:linear-gradient(120deg,#9b4ce9,#6428c5); }
.panel { background:#ffffffd9; border:1px solid #e4ecfa; border-radius:18px; padding:17px 18px; box-shadow:0 7px 22px #163c7010; min-height:190px; }
.panel h3 { margin:0 0 13px; font-size:16px; font-weight:800; color:#102448; }
.progress-row { margin:12px 0; }
.progress-head { display:flex; justify-content:space-between; font-size:12px; font-weight:700; margin-bottom:5px; }
.track { background:#e4ebf7; height:10px; border-radius:20px; overflow:hidden; }
.fill { height:10px; border-radius:20px; }
.stat-grid { display:grid; grid-template-columns:1fr 1fr; gap:9px; }
.stat { background:#edf5ff; border-radius:13px; padding:12px; }
.stat strong { display:block; font-size:22px; color:#102448; }
.stat span { font-size:11px; color:#5d7194; font-weight:600; }
.rank { display:flex; align-items:center; justify-content:space-between; border-bottom:1px solid #edf1f8; padding:7px 0; font-size:12px; font-weight:600; }
.rank:last-child { border:0; }
.rank .who { display:flex; gap:9px; align-items:center; }
.rank .medal { font-size:17px; }
.feature-grid { display:grid; grid-template-columns:repeat(5,1fr); gap:8px; text-align:center; }
.feature { padding:12px 5px; border-right:1px solid #e4ebf6; }
.feature:last-child { border:0; }
.feature b { display:block; font-size:12px; margin-top:5px; }
.feature span { font-size:25px; }
.activity { font-size:11px; padding:9px 0; border-bottom:1px solid #edf1f8; color:#243b60; }
.activity:last-child { border:0; }
.small-muted { color:#7383a0; font-size:11px; }
div[data-testid="stMetric"] { background:#f0f6ff; border-radius:13px; padding:10px; }
div[data-testid="stMetric"] label { color:#607492; }
.stButton button[kind="primary"] { border-radius:10px; }
@media(max-width:900px) {
 .hero h1 {font-size:38px;} .hero-art {font-size:65px; right:2%;}
 .feature-grid {grid-template-columns:repeat(2,1fr);}
}
</style>
""", unsafe_allow_html=True)

# ---------- Login & role access ----------
PENGELOLA = {
    "kendar sultoni": "123",
    "ade romli": "123",
    "muhamad rais": "123",
}
DAFTAR_SISWA = [
    "frischa bunga lestari",
    "zalfatussyifa ramadanti",
    "zain rahmanita",
    "yusuf imam ma'ruf",
    "raihan",
    "febriansyah rachmat hidayat",
    "angga fadillah",
    "muhammad hafidz",
    "andy ramadani abdullah",
    "anggi ratu mahadewi",
    "rizqi ramadhany",
    "kawilujeungan rasyida raihanun",
    "miftahul jannah",
    "muhamad azham fatahila",
    "rosmalati kholisha",
    "m. arif zakariya",
    "mochammad alkahfi mubarok",
    "muhamad hartanto",
    "imam mansyur ibnu hulkarim",
    "daffan oktaffil hidayat",
]

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "user_role" not in st.session_state:
    st.session_state.user_role = ""

if not st.session_state.authenticated:
    st.markdown("""
    <div style="max-width:620px;margin:7vh auto 12px;text-align:center">
      <div style="font-size:58px">📖☪️</div>
      <h1 style="color:#102448;font-weight:800;margin-bottom:0">QORI AI</h1>
      <p style="color:#61718d">Islamic Learning Management System</p>
      <p style="color:#1459ae;font-weight:700;background:#e1edff;padding:12px;border-radius:12px">
        Pengelola password 123, Siswa password 321
      </p>
    </div>
    """, unsafe_allow_html=True)
    with st.form("qori_login_form"):
        st.subheader("Masuk ke QORI AI")
        username_input = st.text_input("Username – Nama Lengkap", placeholder="contoh: frischa bunga lestari")
        password_input = st.text_input("Password", type="password", placeholder="Masukkan password")
        submitted = st.form_submit_button("Login", type="primary", use_container_width=True)
    if submitted:
        username = " ".join(username_input.strip().lower().split())
        password = password_input.strip()
        if username in PENGELOLA and password == PENGELOLA[username]:
            st.session_state.authenticated = True
            st.session_state.user_name = username.title()
            st.session_state.user_role = "Pengelola"
            st.session_state.menu = "Dashboard"
            st.rerun()
        elif username in DAFTAR_SISWA and password == "321":
            st.session_state.authenticated = True
            st.session_state.user_name = username
            st.session_state.user_role = "Siswa"
            st.session_state.menu = "Dashboard"
            st.rerun()
        else:
            st.error("Username atau password salah. Periksa nama lengkap dan password Anda.")
    st.stop()

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("""
    <div class="brand">
      <div class="brand-icon">📖☪️</div>
      <h1>QORI AI</h1>
      <p>Islamic Learning<br>Management System</p>
    </div>
    """, unsafe_allow_html=True)

    st.caption(f"Login: {st.session_state.user_name} ({st.session_state.user_role})")
    if st.button("🚪 Keluar", key="logout", use_container_width=True):
        for key in ["authenticated", "user_name", "user_role", "menu", "mode"]:
            st.session_state.pop(key, None)
        st.rerun()

    _client, _error = get_supabase_client()
    if _error:
        st.warning("Supabase belum terhubung")
    else:
        st.success("Supabase: konfigurasi siap")

    if "menu" not in st.session_state:
        st.session_state.menu = "Dashboard"

    menu_items = [
        ("🏠", "Dashboard"),
        ("🎮", "Belajar & Game"),
        ("📝", "Ujian"),
        ("📊", "Nilai & Hasil"),
        ("🏆", "Leaderboard"),
        ("📚", "Materi"),
        ("📖", "Al-Qur'an (Juz 30)"),
        ("👥", "Data Siswa"),
        ("⚙️", "Pengaturan"),
    ]
    for icon, label in menu_items:
        if st.button(f"{icon}  {label}", key=f"nav_{label}", use_container_width=True):
            st.session_state.menu = label
            st.rerun()

    st.markdown("""
    <div class="side-note">
      <b>✨ Belajar dengan istiqamah</b><br>
      Terus tingkatkan kemampuan membaca,
      memperbaiki bacaan, dan menghafal Al-Qur'an.
    </div>
    """, unsafe_allow_html=True)

# ---------- Header ----------
left, right = st.columns([5, 1])
with left:
    st.markdown(f"""
    <div class="welcome">
      <div>
        <h2>Selamat Datang, {st.session_state.user_name} 👋</h2>
        <p>Di QORI AI – Media Pembelajaran Al-Qur'an Berbasis Artificial Intelligence</p>
      </div>
    </div>
    """, unsafe_allow_html=True)
with right:
    st.markdown(f'<div class="pill">👤 {st.session_state.user_role} ▾</div>', unsafe_allow_html=True)

# ---------- Page content ----------
if st.session_state.menu == "Dashboard":
    _students, _students_error = load_students()
    if _students_error:
        st.caption("🔴 Data siswa Supabase belum tersedia: " + _students_error)
    else:
        st.caption(f"🟢 Supabase terhubung · {len(_students)} siswa terdaftar")
    st.markdown("""
    <div class="hero">
      <div class="hero-kicker">ISLAMIC LEARNING MANAGEMENT SYSTEM</div>
      <h1>QORI <span>AI</span></h1>
      <p>Belajar Al-Qur'an lebih mudah, interaktif, dan menyenangkan dengan dukungan teknologi Artificial Intelligence.</p>
      <div class="hero-tags">
        <div class="hero-tag">🔤 Iqro' · Mengenal Huruf</div>
        <div class="hero-tag">🎙️ Tahsin · Memperbaiki Bacaan</div>
        <div class="hero-tag">📚 Tahfidz · Menghafal Al-Qur'an</div>
      </div>
      <div class="hero-art">🕌 📖</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">✨ Pilih Mode Pembelajaran</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="mode-card iqro">
          <span class="symbol">📗</span><h3>Mode Iqro'</h3>
          <p>Belajar membaca Al-Qur'an dari dasar melalui pengenalan huruf hijaiyah dan tingkat Iqro' 1–6.</p>
          <b>🔰 Pemula hingga mahir</b>
        </div>""", unsafe_allow_html=True)
        if st.button("Mulai Belajar Iqro' →", key="go_iqro", use_container_width=True, type="primary"):
            st.session_state.menu = "Belajar & Game"; st.session_state.mode = "Iqro'"; st.rerun()
    with c2:
        st.markdown("""
        <div class="mode-card tahsin">
          <span class="symbol">🎙️</span><h3>Mode Tahsin</h3>
          <p>Memperbaiki kualitas bacaan Al-Qur'an sesuai makharijul huruf, sifat huruf, dan hukum tajwid.</p>
          <b>🎯 Bacaan lebih tartil</b>
        </div>""", unsafe_allow_html=True)
        if st.button("Mulai Belajar Tahsin →", key="go_tahsin", use_container_width=True, type="primary"):
            st.session_state.menu = "Belajar & Game"; st.session_state.mode = "Tahsin"; st.rerun()
    with c3:
        st.markdown("""
        <div class="mode-card tahfidz">
          <span class="symbol">📚</span><h3>Mode Tahfidz</h3>
          <p>Menghafal, mengulang, dan menjaga hafalan Al-Qur'an melalui latihan sambung ayat.</p>
          <b>🌙 Muraja'ah terarah</b>
        </div>""", unsafe_allow_html=True)
        if st.button("Mulai Belajar Tahfidz →", key="go_tahfidz", use_container_width=True, type="primary"):
            st.session_state.menu = "Belajar & Game"; st.session_state.mode = "Tahfidz"; st.rerun()

    st.markdown('<div class="section-title">📈 Ringkasan Pembelajaran</div>', unsafe_allow_html=True)
    p1, p2, p3 = st.columns([1.15, 1.15, 1])
    with p1:
        st.markdown('<div class="panel"><h3>📊 Progress Belajar Saya</h3>', unsafe_allow_html=True)
        progress = [("Iqro'", "Level 4 / 6", 67, "#08ae7c"), ("Tahsin", "Level 3 / 6", 50, "#1677e8"), ("Tahfidz", "Level 2 / 6", 33, "#9145dc")]
        for name, level, pct, color in progress:
            st.markdown(f"""
            <div class="progress-row">
              <div class="progress-head"><span>{name} · {level}</span><span>{pct}%</span></div>
              <div class="track"><div class="fill" style="width:{pct}%;background:{color}"></div></div>
            </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with p2:
        st.markdown("""
        <div class="panel"><h3>📋 Statistik Aktivitas</h3>
          <div class="stat-grid">
            <div class="stat">🎮 <span>Game</span><strong>12 kali</strong></div>
            <div class="stat">📝 <span>Ujian</span><strong>3 kali</strong></div>
            <div class="stat">🏆 <span>Rata-rata Nilai</span><strong>85</strong></div>
            <div class="stat">✅ <span>Ketuntasan</span><strong>80%</strong></div>
          </div>
        </div>""", unsafe_allow_html=True)
    with p3:
        st.markdown("""
        <div class="panel"><h3>🏆 Leaderboard (Game)</h3>
          <div class="rank"><span class="who"><span class="medal">🥇</span> Raihan Al-Faruq</span><b>98</b></div>
          <div class="rank"><span class="who"><span class="medal">🥈</span> Fadli Saputra</span><b>96</b></div>
          <div class="rank"><span class="who"><span class="medal">🥉</span> Aisyah Nur</span><b>94</b></div>
          <div class="rank"><span class="who"><span class="medal">4.</span> Dinda Aprilia</span><b>92</b></div>
          <div class="rank"><span class="who"><span class="medal">5.</span> Kendar Sultoni</span><b>90</b></div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="section-title">🚀 Fitur Unggulan & Aktivitas Terbaru</div>', unsafe_allow_html=True)
    f1, f2 = st.columns([1.8, 1])
    with f1:
        st.markdown("""
        <div class="panel"><h3>🌟 Fitur Unggulan QORI AI</h3>
          <div class="feature-grid">
            <div class="feature"><span>🎮</span><b>Game Interaktif</b><small>Iqro', Tahsin, Tahfidz</small></div>
            <div class="feature"><span>📖</span><b>Ujian Online</b><small>Evaluasi pemahaman</small></div>
            <div class="feature"><span>📊</span><b>Analisis Nilai</b><small>Progress belajar</small></div>
            <div class="feature"><span>🕌</span><b>Al-Qur'an Digital</b><small>Juz 30 & navigasi ayat</small></div>
            <div class="feature"><span>🤖</span><b>AI Assistant</b><small>Tanya Al-Qur'an & Tajwid</small></div>
          </div>
        </div>""", unsafe_allow_html=True)
    with f2:
        st.markdown("""
        <div class="panel"><h3>🕒 Aktivitas Terbaru</h3>
          <div class="activity">🟢 Selesai Game Tahsin (Level 3) – Nilai 80 <span class="small-muted">Hari ini</span></div>
          <div class="activity">🟢 Selesai Ujian Iqro' – Nilai 85 <span class="small-muted">Hari ini</span></div>
          <div class="activity">🟢 Selesai Game Tahfidz (Level 2) – Nilai 78 <span class="small-muted">Kemarin</span></div>
        </div>""", unsafe_allow_html=True)

elif st.session_state.menu == "Belajar & Game":
    st.title("🎮 Belajar & Game")
    selected = st.session_state.get("mode", "Iqro'")
    mode = st.selectbox("Pilih mode pembelajaran", ["Iqro'", "Tahsin", "Tahfidz"],
                        index=["Iqro'", "Tahsin", "Tahfidz"].index(selected))
    st.session_state.mode = mode
    descriptions = {
        "Iqro'": "Latihan mengenal huruf hijaiyah, harakat, dan membaca bertahap tingkat Iqro' 1–6.",
        "Tahsin": "Latihan makharijul huruf, sifat huruf, hukum nun sukun, mim sukun, dan tajwid.",
        "Tahfidz": "Latihan hafalan dan muraja'ah melalui sambung ayat serta penguatan hafalan."
    }
    st.info(descriptions[mode])
    st.subheader(f"Mode {mode}")
    level = st.select_slider("Pilih tingkat pembelajaran", options=[1, 2, 3, 4, 5, 6], value=1)
    st.write(f"**Tingkat {level}** · Maksimal 25 soal per sesi.")
    st.button("Mulai Game", type="primary", use_container_width=True)
    st.caption("Hubungkan tombol ini dengan modul game dan penyimpanan hasil pada aplikasi QORI AI Anda.")

elif st.session_state.menu == "Ujian":
    st.title("📝 Ujian Online")
    st.write("Pilih kategori ujian untuk mengukur pemahaman pembelajaran Al-Qur'an.")
    st.selectbox("Kategori", ["Iqro'", "Tahsin", "Tahfidz"])
    st.selectbox("Tingkat", [1, 2, 3, 4, 5, 6])
    st.button("Mulai Ujian", type="primary")

elif st.session_state.menu == "Nilai & Hasil":
    st.title("📊 Nilai & Hasil")
    a, b, c = st.columns(3)
    a.metric("Rata-rata Nilai", "85")
    b.metric("Tuntas", "80%")
    c.metric("Jumlah Aktivitas", "15")
    st.info("Bagian ini dapat dihubungkan ke tabel hasil_game dan hasil_ujian di Supabase.")

elif st.session_state.menu == "Leaderboard":
    st.title("🏆 Leaderboard")
    st.dataframe([
        {"Peringkat": 1, "Nama": "Raihan Al-Faruq", "Nilai": 98},
        {"Peringkat": 2, "Nama": "Fadli Saputra", "Nilai": 96},
        {"Peringkat": 3, "Nama": "Aisyah Nur", "Nilai": 94},
        {"Peringkat": 4, "Nama": "Dinda Aprilia", "Nilai": 92},
        {"Peringkat": 5, "Nama": "Kendar Sultoni", "Nilai": 90},
    ], use_container_width=True, hide_index=True)

elif st.session_state.menu == "Materi":
    st.title("📚 Materi Pembelajaran")
    st.write("Materi Iqro', Tahsin, dan Tahfidz dapat ditampilkan berdasarkan tingkat pembelajaran.")
    st.selectbox("Kategori materi", ["Iqro'", "Tahsin", "Tahfidz"])
    st.selectbox("Tingkat", [1, 2, 3, 4, 5, 6])

elif st.session_state.menu == "Al-Qur'an (Juz 30)":
    st.title("📖 Al-Qur'an Digital – Juz 30")
    st.write("Tempat untuk menampilkan daftar surah, teks Arab, terjemahan, dan navigasi ayat.")
    st.info("Integrasikan dengan API Al-Qur'an yang digunakan pada aplikasi Anda.")

elif st.session_state.menu == "Data Siswa":
    st.title("👥 Data Siswa")
    students, student_error = load_students()
    if student_error:
        st.error(student_error)
        st.caption("Pastikan tabel public.siswa tersedia dan kebijakan RLS mengizinkan SELECT untuk anon/publishable key.")
    else:
        st.success(f"Terhubung ke Supabase · {len(students)} siswa ditemukan")
        if students:
            import pandas as pd
            st.metric("Total Siswa", len(students))
            st.dataframe(pd.DataFrame(students), use_container_width=True, hide_index=True)
            if len(students) == 20:
                st.success("Sesuai target: 20 siswa berhasil dimuat.")
            else:
                st.warning(f"Target 20 siswa; saat ini terbaca {len(students)}. Periksa isi tabel dan kebijakan RLS.")
        else:
            st.warning("Belum ada data siswa yang dapat dibaca dari tabel siswa.")

elif st.session_state.menu == "Pengaturan":
    st.title("⚙️ Pengaturan")
    st.write("Pengaturan profil, akun, kategori belajar, dan preferensi aplikasi.")

st.markdown("""
<div style="text-align:center;color:#8291aa;font-size:11px;padding:24px 0 5px">
  © 2026 QORI AI · Islamic Learning Management System · Belajar Al-Qur'an dengan lebih interaktif
</div>
""", unsafe_allow_html=True)
