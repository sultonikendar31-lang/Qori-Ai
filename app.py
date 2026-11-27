"""QORI AI — Islamic Learning Management System (dashboard Streamlit)."""

from __future__ import annotations

import base64
import difflib
import hashlib
import gzip
import html
import json
import os
import random
import re
import time
from datetime import date, datetime, time as datetime_time, timedelta
from zoneinfo import ZoneInfo
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

try:
    from supabase import create_client
except ImportError:
    create_client = None

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

BASE_DIR = Path(__file__).resolve().parent
if load_dotenv is not None:
    load_dotenv(dotenv_path=BASE_DIR / ".env", override=False)


def kredensial(nama: str) -> str:
    try:
        nilai = st.secrets.get(nama)
    except Exception:
        nilai = None
    if nilai is None or not str(nilai).strip():
        nilai = os.getenv(nama, "")
    return str(nilai or "").strip()


OPENAI_API_KEY = kredensial("OPENAI_API_KEY")
DATA_DIR = BASE_DIR / "data"
STORE = DATA_DIR / "qori.json"
ASSETS = BASE_DIR / "assets"
USERS_FILE = DATA_DIR / "users.json"
NILAI_FILE = DATA_DIR / "nilai.json"
PENGUMUMAN_FILE = DATA_DIR / "pengumuman.json"
NOTIF_FILE = DATA_DIR / "notifikasi.json"
FOTO_DIR = ASSETS / "profile_pics"
MATERI_FILE = DATA_DIR / "materi.json"
SOAL_FILE = DATA_DIR / "soal.json"
SETTINGS_FILE = DATA_DIR / "settings.json"
IZIN_FILE = DATA_DIR / "permintaan_izin.json"
CHAT_AI_FILE = DATA_DIR / "chat_ai.json"
KURIKULUM_FILE = DATA_DIR / "materi_kurikulum.json"
MATERI_ASSET_DIR = ASSETS / "materi"
LEADERBOARD_FILE = DATA_DIR / "leaderboard.json"
GLOBAL_SNAPSHOT_FILE = DATA_DIR / "qori_global_snapshot.json"
GLOBAL_SETTINGS_USER_ID = "qori_ai:global"
GLOBAL_SNAPSHOT_KEY = "qori_global_snapshot_v1"


def asset_b64(nama: str) -> str:
    path = ASSETS / nama
    if not path.exists():
        return ""
    return "data:image/jpeg;base64," + base64.b64encode(path.read_bytes()).decode()


def foto_data_uri(foto) -> str:
    if not foto or not foto.get("data"):
        return ""
    mime = foto.get("mime") or "image/png"
    return f"data:{mime};base64," + base64.b64encode(foto["data"]).decode()

BATAS_TUNTAS = 75
MAX_LEVEL = 6
XP_PER_LEVEL = 200
MODE_LIST = ["Iqro'", "Tahsin", "Tahfidz"]
MODE_COLOR = {"Iqro'": "#08ae7c", "Tahsin": "#1677e8", "Tahfidz": "#9145dc"}
MODE_ICON = {"Iqro'": "📗", "Tahsin": "🎙️", "Tahfidz": "📚"}
MODE_DESKRIPSI = {
    "Iqro'": "Latihan mengenal huruf hijaiyah, harakat, dan membaca bertahap tingkat Iqro' 1–6.",
    "Tahsin": "Latihan makharijul huruf, sifat huruf, hukum nun/mim sukun, mad, dan tajwid.",
    "Tahfidz": "Latihan hafalan dan muraja'ah melalui sambung ayat serta penguatan hafalan.",
}

PENGELOLA = {
    "syamsul hadi": "123",
    "muhamad sidiq asyhari": "123",
    "kendar sultoni": "123",
    "ade romli": "123",
    "muhamad rais": "123",
}
SUPER_ADMIN = {"kendar sultoni"}
PENGELOLA_2 = {"syamsul hadi", "muhamad sidiq asyhari",
               "muhamad rais", "ade romli"}
PESAN_AKSES_DITOLAK = ("⚠️ Akses Ditolak. Menu ini hanya untuk Pengelola 1 "
                       "(Kendar Sultoni). Silakan minta izin ke Pengelola 1 "
                       "terlebih dahulu.")
PASSWORD_SISWA = "321"
MENU_SLUGS = {
    "dashboard": "Dashboard",
    "belajar": "Belajar & Game",
    "ujian": "Ujian",
    "nilai": "Nilai & Hasil",
    "leaderboard": "Leaderboard",
    "materi": "Materi",
    "quran": "Al-Qur'an (Juz 30)",
    "siswa": "Data Siswa",
    "pengaturan": "Pengaturan",
}
MODE_SLUGS = {"iqro": "Iqro'", "tahsin": "Tahsin", "tahfidz": "Tahfidz"}

# ---------------------------------------------------------------------------
# Data statis
# ---------------------------------------------------------------------------
HIJAIYAH = [
    ("Alif", "ا"), ("Ba", "ب"), ("Ta", "ت"), ("Tsa", "ث"), ("Jim", "ج"),
    ("Ha", "ح"), ("Kha", "خ"), ("Dal", "د"), ("Dzal", "ذ"), ("Ra", "ر"),
    ("Zai", "ز"), ("Sin", "س"), ("Syin", "ش"), ("Shad", "ص"), ("Dhad", "ض"),
    ("Tha", "ط"), ("Zha", "ظ"), ("'Ain", "ع"), ("Ghain", "غ"), ("Fa", "ف"),
    ("Qaf", "ق"), ("Kaf", "ك"), ("Lam", "ل"), ("Mim", "م"), ("Nun", "ن"),
    ("Wau", "و"), ("Ha (besar)", "ه"), ("Hamzah", "ء"), ("Ya", "ي"),
    ("Lam-Alif", "لا"),
]
HARAKAT_HURUF = [
    ("ب", "b"), ("ت", "t"), ("ج", "j"), ("د", "d"), ("ر", "r"), ("س", "s"),
    ("ك", "k"), ("ل", "l"), ("م", "m"), ("ن", "n"), ("ف", "f"), ("ي", "y"),
]
MAD_HURUF = [
    ("ب", "b"), ("ت", "t"), ("ج", "j"), ("ر", "r"), ("س", "s"), ("ك", "k"),
    ("ل", "l"), ("م", "m"), ("ن", "n"), ("ف", "f"), ("ي", "y"), ("و", "w"),
]
PASANGAN_MIRIP = [
    ("ت", "ث"), ("ج", "ح"), ("ح", "خ"), ("د", "ذ"), ("ر", "ز"), ("س", "ش"),
    ("ص", "ض"), ("ط", "ظ"), ("ع", "غ"), ("ف", "ق"), ("ب", "ت"), ("ك", "ق"),
]
QALQALAH = ["ق", "ط", "ب", "ج", "د"]

TAJWID_Q = [
    ("مِنْ وَرَائِهِمْ", "Idgham", ["Idgham", "Ikhfa", "Iqlab", "Izhar"],
     "Nun sukun bertemu wau termasuk idgham bighunnah."),
    ("مِنْ شَرِّ", "Ikhfa", ["Ikhfa", "Izhar", "Iqlab", "Qalqalah"],
     "Nun sukun bertemu syin termasuk ikhfa."),
    ("مِنْ بَعْدِ", "Iqlab", ["Iqlab", "Idgham", "Izhar", "Mad"],
     "Nun sukun bertemu ba dibaca iqlab."),
    ("مِنْ هَادٍ", "Izhar", ["Izhar", "Ikhfa", "Iqlab", "Idgham"],
     "Nun sukun bertemu ha termasuk izhar halqi."),
    ("أَحَدٌ", "Qalqalah", ["Qalqalah", "Ikhfa", "Mad", "Idgham"],
     "Huruf دْ ketika waqaf dibaca memantul."),
    ("قَالَ", "Mad Thabi'i", ["Mad Thabi'i", "Ikhfa", "Iqlab", "Qalqalah"],
     "Fathah diikuti alif dibaca panjang dua harakat."),
    ("الشَّمْسِ", "Alif Lam Syamsiyah", ["Alif Lam Syamsiyah", "Alif Lam Qamariyah", "Iqlab", "Izhar"],
     "Lam pada alif lam tidak dibaca karena bertemu syin."),
    ("الْقَمَرُ", "Alif Lam Qamariyah", ["Alif Lam Qamariyah", "Alif Lam Syamsiyah", "Ikhfa", "Idgham"],
     "Lam dibaca jelas karena bertemu qaf."),
    ("أَنْعَمْتَ", "Izhar", ["Izhar", "Ikhfa", "Iqlab", "Idgham"],
     "Nun sukun bertemu ain termasuk izhar halqi."),
    ("تَبَّتْ", "Qalqalah", ["Qalqalah", "Mad", "Ikhfa", "Iqlab"],
     "Ba bertasydid memiliki sifat pantulan ketika sukun."),
]
MAD_PANJANG = [
    ("قَالَ", "2 harakat", "Fathah diikuti alif termasuk mad thabi'i."),
    ("يَقُولُ", "2 harakat", "Dhammah diikuti wau termasuk mad thabi'i."),
    ("قِيلَ", "2 harakat", "Kasrah diikuti ya termasuk mad thabi'i."),
    ("جَاءَ", "4–6 harakat", "Mad wajib muttashil: mad bertemu hamzah dalam satu kata."),
    ("سَمَاءِ", "4–6 harakat", "Mad wajib muttashil dibaca panjang 4–5 harakat."),
    ("الْقُرْآنُ", "4–6 harakat", "Mad wajib muttashil pada huruf mad bertemu hamzah."),
    ("رَبِّ", "Pendek (1 harakat)", "Tidak ada huruf mad, dibaca pendek."),
    ("مِنْ", "Pendek (1 harakat)", "Tidak ada huruf mad pada kata ini."),
    ("قُلْ", "Pendek (1 harakat)", "Tidak ada huruf mad, dibaca pendek."),
    ("نُوحِيهَا", "2 harakat", "Ya mad thabi'i dibaca panjang dua harakat."),
]
PUZZLE_AYAT = {
    1: [
        ["قُلْ", "هُوَ", "اللّٰهُ", "أَحَدٌ"],
        ["قُلْ", "أَعُوذُ", "بِرَبِّ", "النَّاسِ"],
        ["قُلْ", "أَعُوذُ", "بِرَبِّ", "الْفَلَقِ"],
        ["مِنْ", "شَرِّ", "مَا", "خَلَقَ"],
        ["إِنَّا", "أَعْطَيْنَاكَ", "الْكَوْثَرَ"],
        ["فَصَلِّ", "لِرَبِّكَ", "وَانْحَرْ"],
    ],
    2: [
        ["الَّذِي", "يُوَسْوِسُ", "فِي", "صُدُورِ", "النَّاسِ"],
        ["وَمِنْ", "شَرِّ", "حَاسِدٍ", "إِذَا", "حَسَدَ"],
        ["وَمِنْ", "شَرِّ", "غَاسِقٍ", "إِذَا", "وَقَبَ"],
        ["وَمِنْ", "شَرِّ", "النَّفَّاثَاتِ", "فِي", "الْعُقَدِ"],
        ["وَالْعَصْرِ", "إِنَّ", "الْإِنْسَانَ", "لَفِي", "خُسْرٍ"],
    ],
    3: [
        ["إِلَّا", "الَّذِينَ", "آمَنُوا", "وَعَمِلُوا", "الصَّالِحَاتِ",
         "وَتَوَاصَوْا", "بِالْحَقِّ"],
        ["إِنَّا", "أَنْزَلْنَاهُ", "فِي", "لَيْلَةِ", "الْقَدْرِ", "وَمَا",
         "أَدْرَاكَ"],
        ["أَلَمْ", "نَشْرَحْ", "لَكَ", "صَدْرَكَ", "وَوَضَعْنَا", "عَنكَ",
         "وِزْرَكَ"],
        ["وَمَا", "أَدْرَاكَ", "مَا", "لَيْلَةُ", "الْقَدْرِ", "لَيْلَةُ",
         "الْقَدْرِ", "خَيْرٌ"],
    ],
}
AYAT_HILANG = {
    1: [
        ("قُلْ هُوَ اللّٰهُ ...", "أَحَدٌ",
         ["أَحَدٌ", "الصَّمَدُ", "النَّاسِ", "الْفَلَقِ"]),
        ("قُلْ أَعُوذُ بِرَبِّ ...", "النَّاسِ",
         ["النَّاسِ", "الْفَلَقِ", "أَحَدٌ", "الصَّمَدُ"]),
        ("مِنْ شَرِّ مَا ...", "خَلَقَ",
         ["خَلَقَ", "حَسَدَ", "وَقَبَ", "يُوسْوِسُ"]),
        ("اللّٰهُ ...", "الصَّمَدُ",
         ["الصَّمَدُ", "أَحَدٌ", "الْفَلَقِ", "النَّاسِ"]),
    ],
    2: [
        ("وَالْعَصْرِ إِنَّ الْإِنْسَانَ لَفِي ...", "خُسْرٍ",
         ["خُسْرٍ", "يُسْرًا", "عِلْمٍ", "صَبْرٍ"]),
        ("إِنَّ مَعَ الْعُسْرِ ...", "يُسْرًا",
         ["يُسْرًا", "خُسْرٍ", "شَرًّا", "عُسْرًا"]),
        ("فَصَلِّ لِرَبِّكَ ...", "وَانْحَرْ",
         ["وَانْحَرْ", "وَاسْجُدْ", "وَاقْنُتْ", "وَاذْكُرْ"]),
        ("إِنَّا أَعْطَيْنَاكَ ...", "الْكَوْثَرَ",
         ["الْكَوْثَرَ", "الْحَوْضَ", "الْمُلْكَ", "الْعِلْمَ"]),
    ],
    3: [
        ("وَمِنْ شَرِّ حَاسِدٍ إِذَا ...", "حَسَدَ",
         ["حَسَدَ", "خَلَقَ", "وَقَبَ", "جَاءَ"]),
        ("لَكُمْ دِينُكُمْ وَلِيَ ...", "دِينِ",
         ["دِينِ", "عَمَلِ", "يَوْمِ", "نَاسِ"]),
        ("وَمَا أَدْرَاكَ مَا لَيْلَةُ ...", "الْقَدْرِ",
         ["الْقَدْرِ", "الْفَجْرِ", "الْعَصْرِ", "الضُّحَى"]),
        ("إِنَّ الْإِنْسَانَ لَفِي ...", "خُسْرٍ",
         ["خُسْرٍ", "يُسْرًا", "عُسْرًا", "صَبْرٍ"]),
    ],
}
MEMORY_AYAT = [
    ("قُلْ", "Katakanlah"),
    ("اللّٰهُ", "Allah"),
    ("أَحَدٌ", "Maha Esa"),
    ("النَّاسِ", "Manusia"),
]
GAMES_MINI = {
    "Iqro'": ["Tebak Huruf", "Pasangkan Huruf", "Tangkap Huruf"],
    "Tahsin": ["Warna-Warni Tajwid", "Tebak Panjang Mad", "Susun Tajwid"],
    "Tahfidz": ["Puzzle Ayat", "Ayat Hilang", "Memory Ayat"],
}
MINI_RONDE = 10
MINI_NYAWA = 3
MINI_POIN = {1: 10, 2: 15, 3: 20}
MINI_LEVEL_NAMA = {1: ("⭐", "MUDAH"), 2: ("⭐⭐", "SEDANG"), 3: ("⭐⭐⭐", "SULIT")}
BATAS_UJIAN = 600

SISWA_AWAL = [
    ("FRISCHA BUNGA LESTARI", "Tahsin"),
    ("ZALFATUSSYIFA RAMADANTI", "Tahfidz"),
    ("ZAIN RAHMANITA", "Tahfidz"),
    ("YUSUF IMAM MA'RUF", "Tahfidz"),
    ("RAIHAN", "Tahsin"),
    ("FEBRIANSYAH RACHMAT HIDAYAT", "Tahfidz"),
    ("ANGGA FADILLAH", "Tahsin"),
    ("MUHAMMAD HAFIDZ", "Tahfidz"),
    ("ANDY RAMADANI ABDULLAH", "Tahsin"),
    ("ANGGI RATU MAHADEWI", "Tahfidz"),
    ("RIZQI RAMADHANY", "Tahfidz"),
    ("KAWILUJEUNGAN RASYIDA RAIHANUN", "Tahfidz"),
    ("MIFTAHUL JANNAH", "Tahfidz"),
    ("MUHAMAD AZHAM FATAHILAH", "Tahfidz"),
    ("ROSMALATI KHOLISHA", "Tahfidz"),
    ("M. ARIF ZAKARIYA", "Tahfidz"),
    ("MOCHAMMAD ALKAHFI MUBAROK", "Tahfidz"),
    ("MUHAMAD HARTANTO", "Iqro'"),
    ("IMAM MANSYUR IBNU HULKARIM", "Tahfidz"),
    ("DAFFAN OKTAFFIL HIDAYAT", "Iqro'"),
]
KELAS_OPSI = ["Kelas 4A", "Kelas 4B", "Kelas 5A", "Kelas 5B", "Kelas 6A"]

SURAH_JUZ30 = [
    (78, "An-Naba'", 40, "Berita Besar"),
    (79, "An-Nazi'at", 46, "Malaikat yang Mencabut"),
    (80, "'Abasa", 42, "Ia Bermuka Masam"),
    (81, "At-Takwir", 29, "Menggulung"),
    (82, "Al-Infitar", 19, "Terbelah"),
    (83, "Al-Mutaffifin", 36, "Orang yang Curang"),
    (84, "Al-Insyiqaq", 25, "Terbelah"),
    (85, "Al-Buruj", 22, "Gugusan Bintang"),
    (86, "At-Tariq", 17, "Yang Datang Malam Hari"),
    (87, "Al-A'la", 19, "Yang Maha Tinggi"),
    (88, "Al-Ghasyiyah", 26, "Hari Kiamat"),
    (89, "Al-Fajr", 30, "Fajar"),
    (90, "Al-Balad", 20, "Negeri"),
    (91, "Asy-Syams", 15, "Matahari"),
    (92, "Al-Lail", 21, "Malam"),
    (93, "Ad-Dhuha", 11, "Waktu Duha"),
    (94, "Al-Insyirah", 8, "Kelapangan"),
    (95, "At-Tin", 8, "Buah Tin"),
    (96, "Al-'Alaq", 19, "Segumpal Darah"),
    (97, "Al-Qadr", 5, "Kemuliaan"),
    (98, "Al-Bayyinah", 8, "Bukti Nyata"),
    (99, "Az-Zalzalah", 8, "Kegoncangan"),
    (100, "Al-'Adiyat", 11, "Kuda yang Berpacu"),
    (101, "Al-Qari'ah", 11, "Hari Kiamat"),
    (102, "At-Takatsur", 8, "Bermegah-Megahan"),
    (103, "Al-'Asr", 3, "Waktu Sore"),
    (104, "Al-Humazah", 9, "Pengumpat"),
    (105, "Al-Fil", 5, "Gajah"),
    (106, "Quraisy", 4, "Suku Quraisy"),
    (107, "Al-Ma'un", 7, "Barang Berguna"),
    (108, "Al-Kautsar", 3, "Nikmat yang Banyak"),
    (109, "Al-Kafirun", 6, "Orang Kafir"),
    (110, "An-Nasr", 3, "Pertolongan"),
    (111, "Al-Lahab", 5, "Api yang Bergejolak"),
    (112, "Al-Ikhlas", 4, "Kemurnian Iman"),
    (113, "Al-Falaq", 5, "Waktu Subuh"),
    (114, "An-Nas", 6, "Manusia"),
]
SURAH_INFO = {n: (nama, ayat, arti) for n, nama, ayat, arti in SURAH_JUZ30}

QORI_LIST = [
    "Mishary Rashid Alafasy (Kuwait) - Merdu, Cocok Pemula",
    "Abdul Basit Abdul Samad (Mesir) - Tartil, Cocok Belajar Tajwid",
    "Saud Al-Shuraim (Mekkah) - Imam Masjidil Haram",
    "Maher Al-Muaiqly (Mekkah) - Merdu & Tenang",
    "Abdurrahman Al Ausy (Mekkah) - Merdu, Viral",
]

QORI_AUDIO = [
    ("Mishary", "Mishary Rashid Alafasy (Kuwait)",
     "https://server8.mp3quran.net/afs/{n:03d}.mp3"),
    ("Abdul Basit", "Abdul Basit Abdul Samad (Mesir)",
     "https://server7.mp3quran.net/basit/{n:03d}.mp3"),
    ("Saud", "Saud Al-Shuraim (Mekkah)",
     "https://server11.mp3quran.net/shur/{n:03d}.mp3"),
    ("Maher", "Maher Al-Muaiqly (Mekkah)",
     "https://server12.mp3quran.net/maher/{n:03d}.mp3"),
    ("Ausy", "Abdurrahman Al Ausy (Mekkah)",
     "https://server8.mp3quran.net/aloosi/{n:03d}.mp3"),
]


def audio_qori(pilihan: str, nomor_surah: int):
    """Nama qori aktif + URL audio surah yang bisa langsung diputar st.audio."""
    for kata, nama, pola in QORI_AUDIO:
        if kata in pilihan:
            return nama, pola.format(n=nomor_surah)
    nama, pola = QORI_AUDIO[0][1], QORI_AUDIO[0][2]
    return nama, pola.format(n=nomor_surah)

FALLBACK_SURAH = {
    103: [
        ("وَالْعَصْرِ", "Demi waktu,"),
        ("إِنَّ الْإِنسَانَ لَفِي خُسْرٍ", "sesungguhnya manusia itu benar-benar dalam kerugian,"),
        ("إِلَّا الَّذِينَ آمَنُوا وَعَمِلُوا الصَّالِحَاتِ وَتَوَاصَوْا بِالْحَقِّ وَتَوَاصَوْا بِالصَّبْرِ",
         "kecuali orang-orang yang beriman dan mengerjakan amal saleh serta saling menasihati untuk kebenaran dan kesabaran."),
    ],
    108: [
        ("إِنَّا أَعْطَيْنَاكَ الْكَوْثَرَ", "Sungguh, Kami telah memberimu (Muhammad) nikmat yang banyak."),
        ("فَصَلِّ لِرَبِّكَ وَانْحَرْ", "Maka laksanakanlah salat karena Tuhanmu, dan berkurbanlah."),
        ("إِنَّ شَانِئَكَ هُوَ الْأَبْتَرُ", "Sungguh, orang yang membencimu dialah yang terputus."),
    ],
    110: [
        ("إِذَا جَاءَ نَصْرُ اللَّهِ وَالْفَتْحُ", "Apabila telah datang pertolongan Allah dan kemenangan,"),
        ("وَرَأَيْتَ النَّاسَ يَدْخُلُونَ فِي دِينِ اللَّهِ أَفْوَاجًا",
         "dan engkau melihat manusia berbondong-bondong masuk agama Allah,"),
        ("فَسَبِّحْ بِحَمْدِ رَبِّكَ وَاسْتَغْفِرْهُ إِنَّهُ كَانَ تَوَّابًا",
         "maka bertasbihlah dengan memuji Tuhanmu dan mohonlah ampunan kepada-Nya. Sungguh, Dia Maha Penerima tobat."),
    ],
    112: [
        ("قُلْ هُوَ اللَّهُ أَحَدٌ", "Katakanlah, “Dialah Allah, Yang Maha Esa.”"),
        ("اللَّهُ الصَّمَدُ", "Allah tempat meminta segala sesuatu."),
        ("لَمْ يَلِدْ وَلَمْ يُولَدْ", "(Allah) tidak beranak dan tidak pula diperanakkan."),
        ("وَلَمْ يَكُن لَّهُ كُفُوًا أَحَدٌ", "Dan tidak ada sesuatu yang setara dengan Dia."),
    ],
    113: [
        ("قُلْ أَعُوذُ بِرَبِّ الْفَلَقِ", "Katakanlah, “Aku berlindung kepada Tuhan yang menguasai subuh,”"),
        ("مِن شَرِّ مَا خَلَقَ", "dari kejahatan makhluk yang Dia ciptakan,"),
        ("وَمِن شَرِّ غَاسِقٍ إِذَا وَقَبَ", "dan dari kejahatan malam apabila telah gelap gulita,"),
        ("وَمِن شَرِّ النَّفَّاثَاتِ فِي الْعُقَدِ", "dan dari kejahatan penyihir yang meniup pada buhul-buhul,"),
        ("وَمِن شَرِّ حَاسِدٍ إِذَا حَسَدَ", "dan dari kejahatan orang yang dengki apabila dia dengki.”"),
    ],
    114: [
        ("قُلْ أَعُوذُ بِرَبِّ النَّاسِ", "Katakanlah, “Aku berlindung kepada Tuhannya manusia,"),
        ("مَلِكِ النَّاسِ", "Raja manusia,"),
        ("إِلَٰهِ النَّاسِ", "sembahan manusia,"),
        ("مِن شَرِّ الْوَسْوَاسِ الْخَنَّاسِ", "dari kejahatan bisikan setan yang bersembunyi,"),
        ("الَّذِي يُوَسْوِسُ فِي صُدُورِ النَّاسِ", "yang membisikkan kejahatan ke dalam dada manusia,"),
        ("مِنَ الْجِنَّةِ وَالنَّاسِ", "dari golongan jin dan manusia.”"),
    ],
}

MATERI = {
    "Iqro'": {
        1: "Mengenal 29 huruf hijaiyah beserta bentuk tunggalnya, mulai dari alif hingga ya.",
        2: "Membaca huruf berharakat fathah, kasrah, dan dammah secara terpisah.",
        3: "Huruf bersambung (di awal, tengah, dan akhir kata) serta bacaan mad sederhana.",
        4: "Harakat sukun, tanwin, dan latihan membaca kata dua sampai tiga huruf.",
        5: "Membedakan huruf yang mirip, makhraj dasar, serta tanda baca Al-Qur'an.",
        6: "Latihan membaca kata dan ayat pendek dengan lancar dan tartil.",
    },
    "Tahsin": {
        1: "Makharijul huruf: rongga mulut, bibir, lidah, tenggorokan, dan rongga hidung.",
        2: "Sifat huruf: hams–jahr, syiddah–rakhawah, isti'la–istifal, dan lainnya.",
        3: "Hukum nun sukun dan tanwin: izhar, idgham, ikhfa, dan iqlab.",
        4: "Hukum mim sukun: izhar syafawi, idgham mimi, dan ikhfa syafawi.",
        5: "Hukum mad: thabi'i, wajib muttashil, dan jaiz munfashil.",
        6: "Qalqalah, waqaf, serta tanda-tanda waqaf dalam mushaf.",
    },
    "Tahfidz": {
        1: "Surah pendek: Al-Ikhlas, Al-Falaq, An-Nas, Al-Kautsar, dan Al-'Asr.",
        2: "Al-Ma'un, Quraisy, Al-Fil, Al-Kafirun, dan An-Nasr.",
        3: "Al-Qadr, Al-Lahab, dan penguatan surah pada level sebelumnya.",
        4: "At-Tin, Al-Insyirah, Ad-Dhuha, dan Al-'Alaq 1–5.",
        5: "Al-Lail, Asy-Syams, Al-Balad, dan Al-Fajr.",
        6: "Al-Ghasyiyah, Al-A'la, At-Tariq, Al-Buruj, dan An-Naba'.",
    },
}

# ---------------------------------------------------------------------------
# Kurikulum materi lengkap
# ---------------------------------------------------------------------------
VIDEO_MATERI = "https://www.youtube.com/watch?v=3h0aGg8w6aA"
KATEGORI_MATERI = ["Iqro'", "Tajwid", "Tahfidz"]
NAMA_KATEGORI = {
    "Iqro'": ("Iqro'", "Iqro'", "إقرأ"),
    "Tajwid": ("Tajwid", "Tajweed", "التجويد"),
    "Tahfidz": ("Tahfidz", "Memorization", "التحفيظ"),
}
TINGKAT_MATERI = ["Pemula", "Menengah", "Lanjutan", "Semua"]


def _materi(id_, kategori, judul, deskripsi, durasi, level, lv,
            huruf, latin, arti, contoh, makhraj, tips, surah=None):
    return {
        "id": id_, "kategori": kategori, "judul": judul, "deskripsi": deskripsi,
        "durasi": durasi, "level": level, "lv": lv, "huruf": huruf, "latin": latin,
        "arti": arti, "contoh": contoh, "video": VIDEO_MATERI,
        "makhraj": makhraj, "tips": tips, "surah": surah, "kustom": False,
    }


DAFTAR_MATERI = [
    # --- Iqro' (6) ---
    _materi("iqro1", "Iqro'", "Iqro' Level 1 - Mengenal Huruf Hijaiyah",
            "Mengenal huruf Alif sampai Ya, bentuk tunggal", 15, "Pemula", 1,
            "ا ب ت ث ج ح خ", "a ba ta tsa ja ha kho",
            "Alif, Ba, Ta, Tsa, Jim, Ha, Kho", "اَ بَ تَ - A Ba Ta",
            "Huruf keluar dari tenggorokan & bibir",
            "Latihan 10 menit setiap hari, jangan terburu-buru"),
    _materi("iqro2", "Iqro'", "Iqro' Level 2 - Huruf Berharakat Fathah",
            "Huruf dengan harokat atas (a)", 20, "Pemula", 2,
            "بَ تَ ثَ جَ", "ba ta tsa ja", "Dibaca pendek 'a'",
            "كَتَبَ - Kataba (Dia telah menulis)",
            "Bibir terbuka, suara pendek", "Bedakan bunyi panjang dan pendek"),
    _materi("iqro3", "Iqro'", "Iqro' Level 3 - Kasrah & Dhommah",
            "Harakat bawah (i) dan depan (u)", 20, "Pemula", 3,
            "بِ بُ تِ تُ", "bi bu ti tu", "Kasrah = i, Dhommah = u",
            "كُتِبَ - Kutiba", "Mulut mencucu untuk dhommah",
            "Jangan tertukar i dan u"),
    _materi("iqro4", "Iqro'", "Iqro' Level 4 - Tanwin & Mad",
            "Tanwin an, in, un dan bacaan panjang", 25, "Menengah", 4,
            "بًا بٍ بٌ", "ban bin bun", "Tanwin = nun mati di akhir",
            "كِتَابٌ - Kitaabun (Sebuah buku)",
            "Dengung dari hidung untuk tanwin", "Panjang mad 2 harokat"),
    _materi("iqro5", "Iqro'", "Iqro' Level 5 - Nun Sukun & Qalqalah",
            "Hukum nun sukun, mim sukun, qalqalah", 30, "Menengah", 5,
            "ق ط ب ج د", "qo tho ba ja da", "Huruf Qalqalah memantul",
            "مِنْ قَبْلِ - Min Qobli", "Qalqalah memantul dari tenggorokan",
            "Qalqalah kubra lebih kuat saat waqaf"),
    _materi("iqro6", "Iqro'", "Iqro' Level 6 - Cara Membaca Al-Qur'an",
            "Praktek membaca Al-Qur'an dengan tajwid dasar", 30, "Lanjutan", 6,
            "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ", "Bismillahirrahmanirrahim",
            "Dengan nama Allah Yang Maha Pengasih, Maha Penyayang",
            "Al-Fatihah ayat 1", "Latihan tartil pelan-pelan",
            "Baca pelan, jangan kejar cepat"),
    # --- Tajwid (6) ---
    _materi("tajwid1", "Tajwid", "Tajwid - Makhraj Huruf Lengkap",
            "Tempat keluarnya huruf hijaiyah", 25, "Menengah", 1,
            "ا هـ ع ح غ خ", "Alif, Ha, Ain, Ha, Ghoin, Kho",
            "Makhraj Halq (Tenggorokan)", "عَلِيمٌ - 'Aliim",
            "Tenggorokan atas, tengah, bawah",
            "Gambar makhraj di bawah sangat membantu"),
    _materi("tajwid2", "Tajwid", "Tajwid - Hukum Nun Sukun & Tanwin",
            "Idzhar, Idgham, Iqlab, Ikhfa", 30, "Menengah", 2,
            "مِنْ رَبِّهِمْ", "Mir Rabbihim", "Idgham bila ghunnah",
            "مَنْ يَعْمَلْ - Mayya'mal", "Dengung dari hidung 2 harokat",
            "Hafalkan huruf Idgham: ي ر م ل و ن"),
    _materi("tajwid3", "Tajwid", "Tajwid - Mad Thabi'i & Mad Wajib",
            "Bacaan panjang 2, 4, 6 harokat", 25, "Menengah", 3,
            "قَالَ", "Qoola", "Mad Thabi'i 2 harokat",
            "السَّمَاء - Assamaa' (Mad Wajib 4-5)",
            "Suara panjang dari rongga mulut", "Jangan kurang dari 2 harokat"),
    _materi("tajwid4", "Tajwid", "Tajwid - Qalqalah Sughra & Kubra",
            "Huruf memantul ق ط ب ج د", 20, "Pemula", 4,
            "ق ط ب ج د", "Qo Tho Ba Ja Da", "Qalqalah = pantulan",
            "الْحَقُّ - Al-Haqq (Kubra)", "Pangkal lidah memantul",
            "Kubra saat waqaf lebih kuat"),
    _materi("tajwid5", "Tajwid", "Tajwid - Hukum Mim Sukun",
            "Ikhfa Syafawi, Idgham Mimi, Idzhar Syafawi", 20, "Menengah", 5,
            "لَكُمْ مِنْ", "Lakum Min", "Idzhar Syafawi",
            "هُمْ بِهِ - Hum Bih (Ikhfa Syafawi)", "Bibir rapat + dengung",
            "Bedakan mim sukun dan nun sukun"),
    _materi("tajwid6", "Tajwid", "Tajwid - Waqaf & Ibtida'",
            "Cara berhenti dan memulai bacaan yang benar", 20, "Lanjutan", 6,
            "وقف - Waqaf", "Waqaf = Berhenti", "Berhenti di tempat yang benar",
            "Tanda waqaf: م - لا - ج - صلى", "Ambil nafas dulu sebelum lanjut",
            "Jangan waqaf di tengah kalimat yang merubah arti"),
    # --- Tahfidz (4) ---
    _materi("tahfidz1", "Tahfidz", "Tahfidz - Juz 30 Surah An-Nas sampai Al-Fil",
            "Target hafalan 1 minggu", 30, "Pemula", 1,
            "قُلْ أَعُوذُ بِرَبِّ النَّاسِ", "Qul a'udzu birobbin naas",
            "Katakanlah: Aku berlindung kepada Tuhan manusia", "An-Nas 1-6",
            "Ulangi 20x per ayat", "Hafal 1 ayat, baru lanjut ayat berikutnya",
            surah=114),
    _materi("tahfidz2", "Tahfidz", "Tahfidz - Surah Al-Mulk Ayat 1-12",
            "Hafalan surah ke-67, keutamaan penjaga dari azab kubur", 40,
            "Menengah", 2, "تَبَارَكَ الَّذِي بِيَدِهِ الْمُلْكُ",
            "Tabaarokalladzii biyadihil mulk",
            "Maha Suci Allah yang di tangan-Nya segala kerajaan",
            "Al-Mulk ayat 1", "Baca sebelum tidur",
            "Murojaah setiap pagi 10 menit", surah=67),
    _materi("tahfidz3", "Tahfidz", "Tahfidz - Metode 3x Ulangi + Tulis",
            "Cara cepat menghafal: Baca 10x, tutup, tulis, setoran", 15,
            "Semua", 3, "Metode Tikrar", "Tikrar = Pengulangan",
            "Ulangi sampai nempel", "1 ayat = 10x baca + 3x tutup",
            "Gunakan 1 mushaf yang sama", "Jangan ganti-ganti mushaf"),
    _materi("tahfidz4", "Tahfidz", "Tahfidz - Cara Menjaga Hafalan (Murojaah)",
            "Agar hafalan tidak hilang", 15, "Semua", 4,
            "مُرَاجَعَة", "Murojaah", "Mengulang hafalan lama",
            "Jadwal: Baru 30 menit, Lama 60 menit", "Setoran ke teman / guru",
            "Hafalan baru tanpa murojaah = hilang dalam 7 hari"),
]

_CSS_MATERI = """
<style>
.mk-arab{font-size:30px;line-height:2;text-align:right;color:var(--text-color);
  font-family:'Amiri','Scheherazade New','Traditional Arabic',serif;direction:rtl;
  background:color-mix(in srgb, var(--primary-color) 10%, transparent);
  border:1px solid color-mix(in srgb, var(--primary-color) 35%, transparent);
  border-radius:14px;padding:14px 18px;margin:6px 0 10px}
.mk-latin,.mk-arti{font-size:14px;color:var(--text-color);margin:2px 0}
.mk-box{border-radius:12px;padding:10px 14px;margin:8px 0;font-size:13.5px;
  color:var(--text-color);line-height:1.65}
.mk-kuning{background:color-mix(in srgb, #f7c948 22%, var(--background-color));
  border:1px solid color-mix(in srgb, #f7c948 60%, transparent)}
.mk-biru{background:color-mix(in srgb, #1677e8 14%, var(--background-color));
  border:1px solid color-mix(in srgb, #1677e8 45%, transparent)}
.mk-hijau{background:color-mix(in srgb, #08a979 14%, var(--background-color));
  border:1px solid color-mix(in srgb, #08a979 45%, transparent)}
.mk-chips{margin:2px 0 8px}
.mk-chip{display:inline-block;font-size:11.5px;font-weight:700;border-radius:999px;
  padding:3px 10px;margin:0 6px 4px 0;color:var(--text-color);
  background:color-mix(in srgb, var(--primary-color) 16%, transparent);
  border:1px solid color-mix(in srgb, var(--primary-color) 40%, transparent)}
.mk-chip.hijau{background:color-mix(in srgb, #08a979 20%, transparent);
  border-color:color-mix(in srgb, #08a979 50%, transparent)}
.mk-chip.kuning{background:color-mix(in srgb, #f7c948 26%, transparent);
  border-color:color-mix(in srgb, #f7c948 60%, transparent)}
.mk-svg{color:var(--text-color);max-width:520px;margin:4px auto 2px;opacity:.95}
.mk-svg text{font-family:'Poppins',sans-serif;font-size:12px;fill:currentColor}
</style>
"""


def _bahasa_nama_kategori(kategori: str) -> str:
    return T(*NAMA_KATEGORI.get(kategori, (kategori, kategori, kategori)))


def _makhraj_svg() -> str:
    bibir = opsi_aman(T("Bibir", "Lips", "الشفتان"))
    lidah = opsi_aman(T("Lidah", "Tongue", "اللسان"))
    tenggorokan = opsi_aman(T("Tenggorokan", "Throat", "الحلق"))
    hidung = opsi_aman(T("Rongga hidung", "Nasal cavity", "الخيشوم"))
    return f"""
    <div class="mk-svg">
    <svg viewBox="0 0 560 210" width="100%" role="img" aria-label="{bibir}">
      <ellipse cx="285" cy="108" rx="235" ry="78" fill="none" stroke="currentColor"
        stroke-width="2" opacity=".45"/>
      <path d="M70 86 C 170 52, 400 52, 505 88" fill="none" stroke="#1677e8"
        stroke-width="3.4" stroke-linecap="round" opacity=".85"/>
      <path d="M96 142 C 180 104, 350 102, 486 136 C 380 158, 210 162, 96 142 Z"
        fill="#08a979" fill-opacity=".38" stroke="#08a979" stroke-width="2.4"/>
      <path d="M486 136 C 504 118, 508 96, 500 78" fill="none" stroke="#9145dc"
        stroke-width="3" stroke-linecap="round" opacity=".85"/>
      <path d="M60 110 h-30" stroke="currentColor" stroke-width="1.4" opacity=".7"/>
      <circle cx="285" cy="166" r="4" fill="#08a979"/>
      <path d="M285 160 v70" stroke="#08a979" stroke-width="1.2" opacity=".7"/>
      <path d="M285 60 v-34" stroke="#1677e8" stroke-width="1.2" opacity=".7"/>
      <text x="26" y="114" text-anchor="end">{bibir}</text>
      <text x="285" y="204" text-anchor="middle">{lidah}</text>
      <text x="522" y="64" text-anchor="start">{tenggorokan}</text>
      <text x="285" y="22" text-anchor="middle">{hidung}</text>
    </svg>
    </div>
    """
def mcq(prompt, answer, distractors, level, arab=None, bahas=""):
    options = [answer]
    seen = {answer}
    for d in distractors:
        if d not in seen:
            options.append(d)
            seen.add(d)
    random.Random(len(prompt) + len(answer)).shuffle(options)
    return {
        "prompt": prompt,
        "answer": answer,
        "options": options,
        "arab": arab,
        "bahas": bahas,
        "level": level,
    }


def build_bank_iqro():
    rnd = random.Random(11)
    bank = []
    for name, glyph in HIJAIYAH:
        salah = rnd.sample([n for n, _ in HIJAIYAH if n != name], 3)
        bank.append(mcq(
            "Huruf hijaiyah ini bernama ...", name, salah, 1, arab=glyph,
            bahas=f"Lafal {glyph} dibaca “{name}”.",
        ))
    for name, glyph in HIJAIYAH:
        salah = rnd.sample([g for _, g in HIJAIYAH if g != glyph], 3)
        bank.append(mcq(
            f"Manakah tulisan huruf “{name}”?", glyph, salah, 1,
            bahas=f"Tulisan huruf {name} adalah {glyph}.",
        ))
    for glyph, lat in HARAKAT_HURUF:
        for mark, vokal in (("َ", "a"), ("ِ", "i"), ("ُ", "u")):
            jawab = f"{lat}{vokal}"
            lain = [f"{lat}{v}" for v in ("a", "i", "u", "an") if v != vokal][:3]
            bank.append(mcq(
                "Bagaimana huruf berharakat ini dibaca?", jawab, lain, 2,
                arab=glyph + mark,
                bahas=f"{glyph + mark} dibaca “{jawab}”.",
            ))
    for glyph, lat in HARAKAT_HURUF:
        bank.append(mcq(
            "Huruf ini berharakat sukun, dibaca ...", f"{lat} (sukun)",
            [f"{lat}a", f"{lat}i", f"{lat}u"], 3, arab=glyph + "ْ",
            bahas=f"{glyph}ْ dibaca “{lat}” dengan suara tertahan (sukun).",
        ))
        for mark, tanwin in (("ً", "an"), ("ٍ", "in"), ("ٌ", "un")):
            jawab = f"{lat}{tanwin}"
            lain = [f"{lat}{x}" for x in ("a", "i", "u") if x != tanwin[:1]]
            bank.append(mcq(
                "Huruf ini berharakat tanwin, dibaca ...", jawab, lain, 3,
                arab=glyph + mark,
                bahas=f"{glyph + mark} dibaca “{jawab}” (tanwin).",
            ))
    for glyph, lat in MAD_HURUF:
        for part, vokal in (("َا", "aa"), ("ِي", "ii"), ("ُو", "uu")):
            jawab = f"{lat}{vokal} (panjang 2 harakat)"
            lain = [
                f"{lat}a (dibaca pendek)",
                f"{lat}i (dibaca pendek)",
                f"{lat}u (dibaca pendek)",
            ]
            bank.append(mcq(
                "Tentukan cara membaca huruf mad berikut.", jawab, lain, 4,
                arab=glyph + part,
                bahas=f"{glyph + part} adalah mad thabi'i: dibaca panjang 2 harakat.",
            ))
    for a, b in PASANGAN_MIRIP:
        lain = [g for _, g in HIJAIYAH if g not in (a, b)]
        bank.append(mcq(
            f"Huruf yang makhrajnya dekat dengan huruf “{a}” adalah ...",
            b, rnd.sample(lain, 3), 5,
            bahas=f"Huruf {a} dan {b} makhrajnya berdekatan sehingga sering tertukar.",
        ))
    makhraj = [
        ("Huruf ب (ba) keluar dari ...", "Dua bibir (syafatain)",
         ["Ujung lidah", "Pangkal tenggorokan", "Rongga mulut"]),
        ("Huruf ق (qaf) keluar dari ...", "Pangkal lidah",
         ["Ujung lidah", "Dua bibir", "Tengah tenggorokan"]),
        ("Huruf mad ا، و، ي keluar dari ...", "Rongga mulut (al-jauf)",
         ["Tenggorokan", "Rongga hidung", "Dua bibir"]),
        ("Huruf ء dan هـ keluar dari ...", "Pangkal tenggorokan (aqshal halq)",
         ["Tengah tenggorokan", "Ujung tenggorokan", "Pangkal lidah"]),
        ("Huruf ع dan ح keluar dari ...", "Tengah tenggorokan (wasathul halq)",
         ["Pangkal tenggorokan", "Ujung tenggorokan", "Dua bibir"]),
        ("Huruf غ dan خ keluar dari ...", "Ujung tenggorokan (adnal halq)",
         ["Pangkal tenggorokan", "Tengah tenggorokan", "Ujung lidah"]),
        ("Huruf ت، د، ط keluar dari ...", "Ujung lidah",
         ["Dua bibir", "Pangkal tenggorokan", "Rongga mulut"]),
    ]
    for prompt, jawab, salah in makhraj:
        bank.append(mcq(prompt, jawab, salah, 5, bahas="Perhatikan makhraj huruf agar bacaan tepat."))
    for q in QALQALAH:
        salah = [g for _, g in HIJAIYAH if g not in QALQALAH]
        bank.append(mcq(
            "Manakah yang termasuk huruf qalqalah?", q, rnd.sample(salah, 3), 6,
            bahas="Huruf qalqalah ada lima: ق ط ب ج د.",
        ))
    bank.append(mcq(
        "Berapa jumlah huruf qalqalah?", "5 huruf",
        ["4 huruf", "6 huruf", "7 huruf"], 6,
        bahas="Huruf qalqalah: ق، ط، ب، ج، د.",
    ))
    return bank


TAHSIN_SOAL = [
    # Level 1 — makharijul huruf
    (1, "Huruf ب (ba) keluar dari ...", "Dua bibir (syafatain)",
     ["Ujung lidah", "Pangkal tenggorokan", "Rongga mulut"],
     "Huruf ba termasuk huruf syafawi karena keluar dari dua bibir."),
    (1, "Huruf ق (qaf) keluar dari ...", "Pangkal lidah",
     ["Ujung lidah", "Dua bibir", "Tengah tenggorokan"],
     "Qaf dibaca dari pangkal lidah yang menempel ke langit-langit mulut."),
    (1, "Huruf mad ا، و، ي keluar dari ...", "Rongga mulut (al-jauf)",
     ["Tenggorokan", "Rongga hidung", "Dua bibir"],
     "Huruf mad keluar dari rongga mulut dan tenggorokan (al-jauf)."),
    (1, "Huruf ء dan هـ keluar dari ...", "Pangkal tenggorokan (aqshal halq)",
     ["Tengah tenggorokan", "Ujung tenggorokan", "Pangkal lidah"],
     "Hamzah dan ha termasuk huruf yang keluar dari pangkal tenggorokan."),
    (1, "Huruf ع dan ح keluar dari ...", "Tengah tenggorokan (wasathul halq)",
     ["Pangkal tenggorokan", "Ujung tenggorokan", "Dua bibir"],
     "'Ain dan ha dibaca dari tengah tenggorokan."),
    (1, "Huruf غ dan خ keluar dari ...", "Ujung tenggorokan (adnal halq)",
     ["Pangkal tenggorokan", "Tengah tenggorokan", "Ujung lidah"],
     "Ghain dan kha keluar dari ujung tenggorokan yang paling dekat mulut."),
    # Level 2 — sifat huruf
    (2, "Sifat hams artinya ...", "Mengalirnya udara saat huruf dibaca",
     ["Tertahannya udara saat huruf dibaca", "Bergetarnya pita suara", "Tebalnya suara huruf"],
     "Hams: udara mengalir ketika huruf dilafalkan."),
    (2, "Huruf yang memiliki sifat jahr adalah ...", "د",
     ["ت", "س", "ف"],
     "Jahr: udara tertahan. Contohnya huruf dal, sedangkan ta, sin, dan fa bersifat hams."),
    (2, "Huruf “ت” memiliki sifat ...", "Hams, syiddah, infitah",
     ["Jahr, syiddah, ithbaq", "Hams, rakhawah, isti'la", "Jahr, rakhawah, idzlaq"],
     "Ta memiliki sifat hams, syiddah, dan infitah."),
    (2, "Huruf yang dibaca tebal (isti'la) adalah ...", "ص",
     ["س", "ب", "م"],
     "Shad termasuk huruf isti'la sehingga dibaca tebal."),
    (2, "Huruf yang dibaca tipis (istifal) adalah ...", "س",
     ["ق", "ط", "خ"],
     "Sin termasuk huruf istifal sehingga dibaca tipis."),
    (2, "Sifat syiddah artinya ...", "Suara tertahan saat huruf dibaca",
     ["Suara mengalir saat huruf dibaca", "Suara menjadi tipis", "Suara menjadi tebal"],
     "Syiddah: suara tertahan karena tekanan pada makhraj."),
    # Level 3 — nun sukun / tanwin
    (3, "Nun sukun bertemu huruf ب hukumnya ...", "Iqlab",
     ["Izhar halqi", "Idgham bighunnah", "Ikhfa syafawi"],
     "Nun sukun bertemu ba dibaca iqlab: bunyi nun berubah menjadi mim."),
    (3, "Nun sukun bertemu huruf ي، ن، م، و hukumnya ...", "Idgham bighunnah",
     ["Idgham bilaghunnah", "Iqlab", "Izhar halqi"],
     "Bertemu ya, nun, mim, atau wau dibaca idgham bighunnah (dengan dengung)."),
    (3, "Nun sukun bertemu huruf ل dan ر hukumnya ...", "Idgham bilaghunnah",
     ["Idgham bighunnah", "Ikhfa haqiqi", "Iqlab"],
     "Bertemu lam dan ra dibaca idgham bilaghunnah (tanpa dengung)."),
    (3, "Nun sukun bertemu huruf إ، ح، ع، هـ hukumnya ...", "Izhar halqi",
     ["Ikhfa haqiqi", "Iqlab", "Idgham bighunnah"],
     "Bertemu huruf halqi dibaca jelas (izhar halqi)."),
    (3, "Nun sukun bertemu huruf selain huruf izhar, idgham, dan iqlab hukumnya ...",
     "Ikhfa haqiqi", ["Izhar halqi", "Iqlab", "Idgham bilaghunnah"],
     "Sisanya dibaca ikhfa haqiqi, yaitu samar dengan dengung."),
    (3, "Hukum bacaan pada lafal مِنْ بَعْدِ adalah ...", "Iqlab",
     ["Ikhfa haqiqi", "Idgham bighunnah", "Izhar halqi"],
     "Nun sukun bertemu ba sehingga dibaca iqlab.", "مِنْ بَعْدِ"),
    (3, "Hukum bacaan pada lafal مَنْ عَمِلَ adalah ...", "Izhar halqi",
     ["Iqlab", "Idgham bighunnah", "Ikhfa haqiqi"],
     "Nun sukun bertemu 'ain sehingga dibaca jelas.", "مَنْ عَمِلَ"),
    (3, "Hukum bacaan pada lafal مِنْ رَبِّهِمْ adalah ...", "Idgham bilaghunnah",
     ["Idgham bighunnah", "Ikhfa haqiqi", "Izhar halqi"],
     "Nun sukun bertemu ra sehingga dibaca idgham tanpa dengung.", "مِنْ رَبِّهِمْ"),
    (3, "Hukum bacaan pada lafal كُفُوًا أَحَدٌ adalah ...", "Izhar halqi",
     ["Iqlab", "Idgham bighunnah", "Ikhfa syafawi"],
     "Tanwin bertemu hamzah sehingga dibaca jelas.", "كُفُوًا أَحَدٌ"),
    (3, "Hukum bacaan pada lafal أَنْزَلْنَا adalah ...", "Ikhfa haqiqi",
     ["Izhar halqi", "Iqlab", "Idgham bilaghunnah"],
     "Nun sukun bertemu zai sehingga dibaca samar.", "أَنْزَلْنَا"),
    # Level 4 — mim sukun
    (4, "Mim sukun bertemu huruf ب hukumnya ...", "Ikhfa syafawi",
     ["Idgham mimi", "Izhar syafawi", "Iqlab"],
     "Mim sukun bertemu ba dibaca samar di bibir (ikhfa syafawi)."),
    (4, "Mim sukun bertemu huruf م hukumnya ...", "Idgham mimi",
     ["Ikhfa syafawi", "Izhar syafawi", "Idgham bilaghunnah"],
     "Mim sukun bertemu mim dibaca idgham mimi dengan dengung."),
    (4, "Mim sukun bertemu huruf selain ب dan م hukumnya ...", "Izhar syafawi",
     ["Ikhfa syafawi", "Idgham mimi", "Iqlab"],
     "Selain ba dan mim, mim sukun dibaca jelas (izhar syafawi)."),
    (4, "Lafal تَرْمِيهِمْ بِحِجَارَةٍ mengandung hukum ...", "Ikhfa syafawi",
     ["Izhar syafawi", "Idgham mimi", "Iqlab"],
     "Mim sukun bertemu ba.", "تَرْمِيهِمْ بِحِجَارَةٍ"),
    (4, "Lafal لَهُمْ مَا mengandung hukum ...", "Idgham mimi",
     ["Ikhfa syafawi", "Izhar syafawi", "Idgham bilaghunnah"],
     "Mim sukun bertemu mim.", "لَهُمْ مَا"),
    (4, "Lafal عَلَيْهِمْ غَيْرِ mengandung hukum ...", "Izhar syafawi",
     ["Ikhfa syafawi", "Idgham mimi", "Iqlab"],
     "Mim sukun bertemu ghain sehingga dibaca jelas.", "عَلَيْهِمْ غَيْرِ"),
    (4, "Lafal يَنْصُرُ mengandung hukum ...", "Ikhfa haqiqi",
     ["Izhar halqi", "Iqlab", "Idgham bighunnah"],
     "Nun sukun bertemu shad sehingga dibaca samar.", "يَنْصُرُ"),
    (4, "Lafal مِنْ نِعْمَةٍ mengandung hukum ...", "Idgham bighunnah",
     ["Idgham bilaghunnah", "Ikhfa haqiqi", "Iqlab"],
     "Nun sukun bertemu nun.", "مِنْ نِعْمَةٍ"),
    (4, "Lafal أَنْتُمْ mengandung hukum ...", "Ikhfa haqiqi",
     ["Izhar halqi", "Iqlab", "Idgham mimi"],
     "Nun sukun bertemu ta sehingga dibaca samar.", "أَنْتُمْ"),
    # Level 5 — mad
    (5, "Mad thabi'i dibaca panjang ...", "2 harakat",
     ["1 harakat", "4 harakat", "6 harakat"],
     "Mad thabi'i panjangnya dua harakat."),
    (5, "Mad wajib muttashil dibaca panjang ...", "4–5 harakat",
     ["2 harakat", "2, 4, atau 5 harakat", "6 harakat"],
     "Huruf mad bertemu hamzah dalam satu kata: 4–5 harakat."),
    (5, "Mad jaiz munfashil boleh dibaca panjang ...", "2, 4, atau 5 harakat",
     ["Hanya 2 harakat", "Hanya 6 harakat", "4–5 harakat saja"],
     "Huruf mad bertemu hamzah di kata berikutnya: 2, 4, atau 5 harakat."),
    (5, "Lafal الرَّحْمَٰنِ mengandung mad ...", "Mad thabi'i",
     ["Mad wajib muttashil", "Mad jaiz munfashil", "Mad 'aridh lissukun"],
     "Alif setelah ha berharakat dibaca panjang dua harakat.", "الرَّحْمَٰنِ"),
    (5, "Lafal وَمَا أُنْزِلَ mengandung mad ...", "Mad jaiz munfashil",
     ["Mad thabi'i", "Mad wajib muttashil", "Mad lazim"],
     "Mad bertemu hamzah pada kata berikutnya.", "وَمَا أُنْزِلَ"),
    (5, "Lafal جَاءَ mengandung mad ...", "Mad wajib muttashil",
     ["Mad thabi'i", "Mad jaiz munfashil", "Mad badal"],
     "Mad bertemu hamzah dalam satu kata.", "جَاءَ"),
    (5, "Lafal قَالَ mengandung mad ...", "Mad thabi'i",
     ["Mad wajib muttashil", "Mad jaiz munfashil", "Mad lazim"],
     "Alif setelah qaf dibaca panjang dua harakat.", "قَالَ"),
    (5, "Lafal الْقُرْآنُ mengandung mad ...", "Mad wajib muttashil",
     ["Mad thabi'i", "Mad jaiz munfashil", "Mad 'aridh lissukun"],
     "Mad bertemu hamzah dalam satu kata.", "الْقُرْآنُ"),
    (5, "Mad badal dibaca panjang ...", "2 harakat",
     ["4 harakat", "5 harakat", "6 harakat"],
     "Mad badal (hamzah sebelum huruf mad) dibaca dua harakat."),
    # Level 6 — qalqalah & waqaf
    (6, "Huruf qalqalah dibaca memantul apabila ...", "Bersukun atau diwaqafkan",
     ["Berharakat fathah", "Berharakat kasrah", "Bertasyid"],
     "Qalqalah muncul saat huruf qalqalah bersukun atau diwaqafkan."),
    (6, "Qalqalah sughra terjadi apabila huruf qalqalah berada ...",
     "Di tengah kata dalam keadaan sukun",
     ["Di akhir kata dan diwaqafkan", "Di awal kata", "Di akhir ayat yang disambung"],
     "Qalqalah sughra: huruf qalqalah sukun di tengah kata, pantulannya ringan."),
    (6, "Qalqalah kubra terjadi apabila huruf qalqalah berada ...",
     "Di akhir kata dan diwaqafkan",
     ["Di tengah kata", "Di awal kata", "Setelah harakat fathah"],
     "Qalqalah kubra: huruf qalqalah di akhir kata saat waqaf, pantulannya lebih kuat."),
    (6, "Tanda waqaf م (waqaf lazim) berarti ...", "Harus berhenti",
     ["Boleh berhenti atau lanjut", "Lebih baik lanjut", "Tidak boleh berhenti"],
     "Waqaf lazim: wajib berhenti karena maknanya berkaitan."),
    (6, "Tanda waqaf ج (jaiz) berarti ...", "Boleh berhenti atau lanjut",
     ["Harus berhenti", "Harus lanjut", "Berhenti dengan mengulang"],
     "Waqaf jaiz: boleh memilih berhenti atau melanjutkan."),
    (6, "Lafal قُلْ هُوَ اللَّهُ أَحَدٌ diwaqafkan pada kata أَحَدٌ. Hukumnya ...",
     "Qalqalah kubra",
     ["Qalqalah sughra", "Mad thabi'i", "Idgham mimi"],
     "Dal di akhir kata diwaqafkan sehingga dibaca memantul kuat.", "قُلْ هُوَ اللَّهُ أَحَدٌ"),
    (6, "Lafal يَجْعَلُونَ mengandung ...", "Qalqalah sughra",
     ["Qalqalah kubra", "Mad wajib muttashil", "Ikhfa syafawi"],
     "Jim sukun di tengah kata sehingga pantulannya ringan.", "يَجْعَلُونَ"),
    (6, "Lafal فَوَيْلٌ لِلْمُصَلِّينَ mengandung hukum ...", "Idgham bilaghunnah",
     ["Idgham bighunnah", "Iqlab", "Izhar halqi"],
     "Tanwin bertemu lam dibaca idgham tanpa dengung.", "فَوَيْلٌ لِلْمُصَلِّينَ"),
    (6, "Lafal الْقَمَرُ mengandung hukum ...", "Izhar qamariyah",
     ["Idgham syamsiyah", "Ikhfa haqiqi", "Idgham mimi"],
     "Alif lam bertemu qaf dibaca jelas (qamariyah).", "الْقَمَرُ"),
    (6, "Lafal الشَّمْسُ mengandung hukum ...", "Idgham syamsiyah",
     ["Izhar qamariyah", "Iqlab", "Ikhfa haqiqi"],
     "Alif lam bertemu syin dibaca lebur (syamsiyah).", "الشَّمْسُ"),
]

TAHFIDZ_SOAL = [
    (1, "قُلْ هُوَ اللَّهُ أَحَدٌ", "اللَّهُ الصَّمَدُ", "Al-Ikhlas", "1–2"),
    (1, "لَمْ يَلِدْ وَلَمْ يُولَدْ", "وَلَمْ يَكُن لَّهُ كُفُوًا أَحَدٌ", "Al-Ikhlas", "3–4"),
    (1, "إِنَّا أَعْطَيْنَاكَ الْكَوْثَرَ", "فَصَلِّ لِرَبِّكَ وَانْحَرْ", "Al-Kautsar", "1–2"),
    (1, "قُلْ أَعُوذُ بِرَبِّ الْفَلَقِ", "مِن شَرِّ مَا خَلَقَ", "Al-Falaq", "1–2"),
    (1, "قُلْ أَعُوذُ بِرَبِّ النَّاسِ", "مَلِكِ النَّاسِ", "An-Nas", "1–2"),
    (1, "وَالْعَصْرِ", "إِنَّ الْإِنسَانَ لَفِي خُسْرٍ", "Al-'Asr", "1–2"),
    (2, "أَرَأَيْتَ الَّذِي يُكَذِّبُ بِالدِّينِ", "فَذَٰلِكَ الَّذِي يَدُعُّ الْيَتِيمَ", "Al-Ma'un", "1–2"),
    (2, "لِإِيلَافِ قُرَيْشٍ", "إِيلَافِهِمْ رِحْلَةَ الشِّتَاءِ وَالصَّيْفِ", "Quraisy", "1–2"),
    (2, "أَلَمْ تَرَ كَيْفَ فَعَلَ رَبُّكَ بِأَصْحَابِ الْفِيلِ",
     "أَلَمْ يَجْعَلْ كَيْدَهُمْ فِي تَضْلِيلٍ", "Al-Fil", "1–2"),
    (2, "قُلْ يَا أَيُّهَا الْكَافِرُونَ", "لَا أَعْبُدُ مَا تَعْبُدُونَ", "Al-Kafirun", "1–2"),
    (2, "إِذَا جَاءَ نَصْرُ اللَّهِ وَالْفَتْحُ",
     "وَرَأَيْتَ النَّاسَ يَدْخُلُونَ فِي دِينِ اللَّهِ أَفْوَاجًا", "An-Nasr", "1–2"),
    (2, "فَلْيَعْبُدُوا رَبَّ هَٰذَا الْبَيْتِ",
     "الَّذِي أَطْعَمَهُم مِّن جُوعٍ وَآمَنَهُم مِّنْ خَوْفٍ", "Quraisy", "3–4"),
    (3, "إِنَّا أَنْزَلْنَاهُ فِي لَيْلَةِ الْقَدْرِ", "وَمَا أَدْرَاكَ مَا لَيْلَةُ الْقَدْرِ", "Al-Qadr", "1–2"),
    (3, "تَبَّتْ يَدَا أَبِي لَهَبٍ وَتَبَّ", "مَا أَغْنَىٰ عَنْهُ مَالُهُ وَمَا كَسَبَ", "Al-Lahab", "1–2"),
    (3, "فَإِنَّ مَعَ الْعُسْرِ يُسْرًا", "إِنَّ مَعَ الْعُسْرِ يُسْرًا", "Al-Insyirah", "5–6"),
    (3, "لَا أَعْبُدُ مَا تَعْبُدُونَ", "وَلَا أَنتُمْ عَابِدُونَ مَا أَعْبُدُ", "Al-Kafirun", "2–3"),
    (3, "وَمَا أَدْرَاكَ مَا لَيْلَةُ الْقَدْرِ", "لَيْلَةُ الْقَدْرِ خَيْرٌ مِّنْ أَلْفِ شَهْرٍ", "Al-Qadr", "2–3"),
    (3, "إِنَّ الْإِنسَانَ لَفِي خُسْرٍ",
     "إِلَّا الَّذِينَ آمَنُوا وَعَمِلُوا الصَّالِحَاتِ", "Al-'Asr", "2–3"),
    (4, "اقْرَأْ بِاسْمِ رَبِّكَ الَّذِي خَلَقَ", "خَلَقَ الْإِنسَانَ مِنْ عَلَقٍ", "Al-'Alaq", "1–2"),
    (4, "وَالضُّحَىٰ", "وَاللَّيْلِ إِذَا سَجَىٰ", "Ad-Dhuha", "1–2"),
    (4, "أَلَمْ نَشْرَحْ لَكَ صَدْرَكَ", "وَوَضَعْنَا عَنكَ وِزْرَكَ", "Al-Insyirah", "1–2"),
    (4, "وَالتِّينِ وَالزَّيْتُونِ", "وَطُورِ سِينِينَ", "At-Tin", "1–2"),
    (4, "وَوَجَدَكَ ضَالًّا فَهَدَىٰ", "وَوَجَدَكَ عَائِلًا فَأَغْنَىٰ", "Ad-Dhuha", "7–8"),
    (4, "فَأَمَّا الْيَتِيمَ فَلَا تَقْهَرْ", "وَأَمَّا السَّائِلَ فَلَا تَنْهَرْ", "Ad-Dhuha", "9–10"),
    (5, "وَاللَّيْلِ إِذَا يَغْشَىٰ", "وَالنَّهَارِ إِذَا تَجَلَّىٰ", "Al-Lail", "1–2"),
    (5, "وَالشَّمْسِ وَضُحَاهَا", "وَالْقَمَرِ إِذَا تَلَاهَا", "Asy-Syams", "1–2"),
    (5, "لَا أُقْسِمُ بِهَٰذَا الْبَلَدِ", "وَأَنتَ حِلٌّ بِهَٰذَا الْبَلَدِ", "Al-Balad", "1–2"),
    (5, "وَالْفَجْرِ", "وَلَيَالٍ عَشْرٍ", "Al-Fajr", "1–2"),
    (5, "وَنَفْسٍ وَمَا سَوَّاهَا", "فَأَلْهَمَهَا فُجُورَهَا وَتَقْوَاهَا", "Asy-Syams", "7–8"),
    (5, "أَلَمْ نَجْعَل لَّهُ عَيْنَيْنِ", "وَلِسَانًا وَشَفَتَيْنِ", "Al-Balad", "8–9"),
    (6, "عَمَّ يَتَسَاءَلُونَ", "عَنِ النَّبَإِ الْعَظِيمِ", "An-Naba'", "1–2"),
    (6, "هَلْ أَتَاكَ حَدِيثُ الْغَاشِيَةِ", "وُجُوهٌ يَوْمَئِذٍ خَاشِعَةٌ", "Al-Ghasyiyah", "1–2"),
    (6, "سَبِّحِ اسْمَ رَبِّكَ الْأَعْلَى", "الَّذِي خَلَقَ فَسَوَّىٰ", "Al-A'la", "1–2"),
    (6, "وَالسَّمَاءِ وَالطَّارِقِ", "وَمَا أَدْرَاكَ مَا الطَّارِقُ", "At-Tariq", "1–2"),
    (6, "وَالسَّمَاءِ ذَاتِ الْبُرُوجِ", "وَالْيَوْمِ الْمَوْعُودِ", "Al-Buruj", "1–2"),
    (6, "إِذَا السَّمَاءُ انشَقَّتْ", "وَأَذِنَتْ لِرَبِّهَا وَحُقَّتْ", "Al-Insyiqaq", "1–2"),
    (1, "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ", "الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ", "Al-Fatihah", "1–2"),
    (1, "الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ", "الرَّحْمَٰنِ الرَّحِيمِ", "Al-Fatihah", "2–3"),
    (1, "الرَّحْمَٰنِ الرَّحِيمِ", "مَالِكِ يَوْمِ الدِّينِ", "Al-Fatihah", "3–4"),
    (1, "مَالِكِ يَوْمِ الدِّينِ", "إِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ", "Al-Fatihah", "4–5"),
    (1, "إِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ", "اهْدِنَا الصِّرَاطَ الْمُسْتَقِيمَ", "Al-Fatihah", "5–6"),
    (1, "اهْدِنَا الصِّرَاطَ الْمُسْتَقِيمَ",
     "صِرَاطَ الَّذِينَ أَنْعَمْتَ عَلَيْهِمْ غَيْرِ الْمَغْضُوبِ عَلَيْهِمْ وَلَا الضَّالِّينَ",
     "Al-Fatihah", "6–7"),
    (2, "تَبَارَكَ الَّذِي بِيَدِهِ الْمُلْكُ", "وَهُوَ عَلَىٰ كُلِّ شَيْءٍ قَدِيرٌ", "Al-Mulk", "1–2"),
    (2, "الَّذِي خَلَقَ الْمَوْتَ وَالْحَيَاةَ",
     "لِيَبْلُوَكُمْ أَيُّكُمْ أَحْسَنُ عَمَلًا", "Al-Mulk", "2–3"),
    (2, "وَهُوَ الْعَزِيزُ الْغَفُورُ", "الَّذِي خَلَقَ سَبْعَ سَمَاوَاتٍ طِبَاقًا", "Al-Mulk", "2–4"),
    (2, "مَا تَرَىٰ فِي خَلْقِ الرَّحْمَٰنِ مِن تَفَاوُتٍ",
     "فَارْجِعِ الْبَصَرَ هَلْ تَرَىٰ مِن فُطُورٍ", "Al-Mulk", "3–4"),
    (2, "وَلَقَدْ زَيَّنَّا السَّمَاءَ الدُّنْيَا بِمَصَابِيحَ",
     "وَجَعَلْنَاهَا رُجُومًا لِّلشَّيَاطِينِ", "Al-Mulk", "5–6"),
]


def build_bank_tahsin():
    bank = []
    for item in TAHSIN_SOAL:
        level, prompt, jawab, salah, bahas = item[:5]
        arab = item[5] if len(item) > 5 else None
        bank.append(mcq(prompt, jawab, salah, level, arab=arab, bahas=bahas))
    return bank


def build_bank_tahfidz():
    rnd = random.Random(23)
    semua_jawaban = [t[2] for t in TAHFIDZ_SOAL]
    bank = []
    for level, awal, jawab, surah, ayat in TAHFIDZ_SOAL:
        salah = rnd.sample([j for j in semua_jawaban if j != jawab], 3)
        bank.append(mcq(
            "Lanjutkan ayat berikut:", jawab, salah, level, arab=awal,
            bahas=f"QS. {surah}: {ayat}.",
        ))
    return bank


BANKS = {
    "Iqro'": build_bank_iqro(),
    "Tahsin": build_bank_tahsin(),
    "Tahfidz": build_bank_tahfidz(),
}

# ---------------------------------------------------------------------------
# Halaman & CSS
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="QORI AI | Dashboard",
    page_icon="📖",
    layout="wide",
    # "auto": sidebar terbuka di desktop, otomatis tertutup di HP/tablet kecil
    initial_sidebar_state="auto",
)

# --- AUTOSAVE PENGATURAN: muat dari disk agar tetap setelah refresh ---
AUTOSAVE_FILE = BASE_DIR / "pengaturan_qori.json"


def _baca_autosave() -> dict:
    try:
        with open(AUTOSAVE_FILE, "r", encoding="utf-8") as f:
            isi = json.load(f)
        return isi if isinstance(isi, dict) else {}
    except Exception:
        return {}


_DISK_CFG = _baca_autosave()
if _DISK_CFG:
    st.session_state.setdefault("data_tersimpan", _DISK_CFG)
    for _kunci, _field in (
        ("set_nama", "nama"),
        ("set_lembaga", "sekolah"),
        ("set_email", "email"),
        ("set_jam_input", "jam_pengingat"),
        ("set_suara", "qori"),
        ("set_mode", "level"),
        ("set_iqro", "level_iqro"),
        ("set_target", "target"),
        ("set_reminder", "notifikasi"),
        ("set_huruf", "huruf"),
        ("set_kecepatan", "kecepatan"),
        ("set_autoplay", "autoplay"),
        ("set_tajwid", "tajwid"),
        ("set_notif_leader", "notif_leader"),
    ):
        _nilai = _DISK_CFG.get(_field)
        if _nilai in (None, ""):
            continue
        if _kunci == "set_suara" and _nilai not in QORI_LIST:
            continue
        st.session_state.setdefault(_kunci, _nilai)

# --- TEMA & BAHASA GLOBAL ---
_BAHASA_OPSI = ["Bahasa Indonesia", "English", "العربية (Arab)"]
_TEMA_OPSI = ("Terang", "Gelap")
_CFG_AWAL = st.session_state.get("pengaturan_tersimpan", {}) or {}
_MIRROR_TAMPILAN = st.session_state.get("_tampilan_aktif", {}) or {}
_MENU_AWAL = st.session_state.get("menu")
if _MENU_AWAL == "Pengaturan":
    if st.session_state.get("tema_aplikasi") not in _TEMA_OPSI:
        st.session_state["tema_aplikasi"] = next(
            (v for v in (_MIRROR_TAMPILAN.get("tema"),
                         _DISK_CFG.get("tema"),
                         _CFG_AWAL.get("tema_aplikasi"), "Terang")
             if v in _TEMA_OPSI), "Terang")
    if st.session_state.get("bahasa_aplikasi") not in _BAHASA_OPSI:
        st.session_state["bahasa_aplikasi"] = next(
            (v for v in (_MIRROR_TAMPILAN.get("bahasa"),
                         _DISK_CFG.get("bahasa"),
                         _CFG_AWAL.get("bahasa_aplikasi"), "Bahasa Indonesia")
             if v in _BAHASA_OPSI), "Bahasa Indonesia")
    tema = st.session_state["tema_aplikasi"]
    bahasa = st.session_state["bahasa_aplikasi"]
else:
    # Nilai widget bisa terhapus saat halaman Pengaturan tidak dirender;
    # pakai salinan terakhir agar tema/bahasa tidak berubah sendiri.
    st.session_state.pop("tema_aplikasi", None)
    st.session_state.pop("bahasa_aplikasi", None)
    tema = next(
        (v for v in (_MIRROR_TAMPILAN.get("tema"),
                     _DISK_CFG.get("tema"),
                     _CFG_AWAL.get("tema_aplikasi"), "Terang")
         if v in _TEMA_OPSI), "Terang")
    bahasa = next(
        (v for v in (_MIRROR_TAMPILAN.get("bahasa"),
                     _DISK_CFG.get("bahasa"),
                     _CFG_AWAL.get("bahasa_aplikasi"), "Bahasa Indonesia")
         if v in _BAHASA_OPSI), "Bahasa Indonesia")

BAHASA_ARAB = "Arab" in bahasa or "العربية" in bahasa


def T(id_text, en_text, ar_text):
    if bahasa == "English":
        return en_text
    if BAHASA_ARAB:
        return ar_text
    return id_text


st.session_state["T"] = T


# --- AUTOSAVE PENGATURAN GLOBAL ---
def _kumpulkan_pengaturan() -> dict:
    """Kumpulkan pengaturan dengan satu nama key kanonis agar nilai kosong/tidak hilang."""
    mirror = st.session_state.get("_tampilan_aktif", {}) or {}
    sebelumnya = st.session_state.get("data_tersimpan") or _DISK_CFG or {}

    def nilai_widget(kunci, kunci_lama, default):
        if kunci in st.session_state:
            return st.session_state[kunci]
        if kunci_lama in sebelumnya:
            return sebelumnya[kunci_lama]
        return default

    qori = nilai_widget("set_suara", "qori", QORI_LIST[0])
    if qori not in QORI_LIST:
        qori = QORI_LIST[0]
    tema_aktif = next(
        (v for v in (st.session_state.get("tema_aplikasi"), mirror.get("tema"),
                     sebelumnya.get("tema"), tema)
         if v in _TEMA_OPSI), "Terang")
    bahasa_aktif = next(
        (v for v in (st.session_state.get("bahasa_aplikasi"), mirror.get("bahasa"),
                     sebelumnya.get("bahasa"), bahasa)
         if v in _BAHASA_OPSI), "Bahasa Indonesia")
    jam = nilai_widget("set_jam_input", "jam_pengingat", "19:00")
    return {
        "nama": nilai_widget("set_nama", "nama", "Kendar Sultoni"),
        # Key kanonis nama lembaga: selalu "sekolah"; jangan membuat key alternatif.
        "sekolah": nilai_widget("set_lembaga", "sekolah", "TPQ Nurul Ilmi"),
        # Nama field internal tetap "email" agar data lama tidak hilang; label UI menjadi Username.
        "email": nilai_widget("set_email", "email", "kendar@gmail.com"),
        "qori": qori,
        "tema": tema_aktif,
        "bahasa": bahasa_aktif,
        "level": nilai_widget("set_mode", "level", "Tahsin"),
        "level_iqro": nilai_widget("set_iqro", "level_iqro", "Iqro' 3"),
        "target": nilai_widget("set_target", "target", 30),
        "notifikasi": bool(nilai_widget("set_reminder", "notifikasi", True)),
        "jam_pengingat": str(jam if jam is not None else "19:00"),
        "huruf": nilai_widget("set_huruf", "huruf", "Sedang"),
        "kecepatan": nilai_widget("set_kecepatan", "kecepatan", "Normal (1x)"),
        "autoplay": bool(nilai_widget("set_autoplay", "autoplay", True)),
        "tajwid": bool(nilai_widget("set_tajwid", "tajwid", True)),
        "notif_leader": bool(nilai_widget("set_notif_leader", "notif_leader", True)),
    }


def autosave_pengaturan():
    """Simpan perubahan kotak pengaturan segera saat callback widget berjalan."""
    st.session_state["_pengaturan_dirty"] = True
    st.session_state["_pengaturan_dirty_at"] = time.time()
    st.session_state["_pengaturan_status"] = "saving"
    cfg = _kumpulkan_pengaturan()
    # Mirror permanen mencegah nilai widget hilang ketika halaman Pengaturan
    # tidak dirender dan Streamlit membersihkan state widget yang tidak aktif.
    st.session_state["data_tersimpan"] = dict(cfg)
    st.session_state["pengaturan_tersimpan"] = dict(cfg)
    try:
        _tulis_json(AUTOSAVE_FILE, cfg)
    except Exception as exc:
        st.session_state["_pengaturan_save_error"] = str(exc)
    # Callback dipanggil sebelum halaman dirender; snapshot langsung membaca
    # nilai widget terbaru dan mengirimkannya ke Supabase + JSON global.
    simpan_global = globals().get("_qori_simpan_snapshot_global")
    if callable(simpan_global):
        ok, detail = simpan_global(alasan="perubahan_kotak_pengaturan", manual=False)
        if ok:
            st.session_state["_pengaturan_status"] = "saved"
            st.session_state["_pengaturan_save_error"] = ""
            st.session_state["_qori_global_refresh_after_autosave"] = True
        else:
            st.session_state["_pengaturan_status"] = "error"
            st.session_state["_pengaturan_save_error"] = str(detail)
    return cfg


def _muat_pengaturan_supabase():
    """Gunakan pengaturan snapshot global; baca baris personal lama hanya sebagai fallback migrasi."""
    global tema, bahasa, BAHASA_ARAB
    if st.session_state.get("_pengaturan_global_hydrated"):
        return
    st.session_state["_pengaturan_global_hydrated"] = True
    data = st.session_state.get("data_tersimpan") or st.session_state.get("pengaturan_tersimpan") or {}
    if not (isinstance(data, dict) and data):
        nama_user = str(st.session_state.get("user_name") or "anonim").strip().casefold()
        role_user = str(st.session_state.get("user_role") or "pengguna").strip().casefold()
        user_id = f"{role_user}:{nama_user}"
        client, _error = get_supabase_client()
        if client is not None:
            try:
                hasil = (client.table("app_settings").select("settings")
                         .eq("user_id", user_id).limit(1).execute())
                rows = getattr(hasil, "data", None) or []
                if rows and isinstance(rows[0].get("settings"), dict):
                    data = rows[0]["settings"]
            except Exception as exc:
                st.session_state["_pengaturan_load_error"] = str(exc)
    if not isinstance(data, dict) or not data:
        return
    st.session_state["data_tersimpan"] = data.copy()
    st.session_state["pengaturan_tersimpan"] = data.copy()
    pemetaan = {
        "set_nama": "nama", "set_lembaga": "sekolah", "set_email": "email",
        "set_suara": "qori", "set_mode": "level", "set_iqro": "level_iqro",
        "set_target": "target", "set_reminder": "notifikasi",
        "set_jam_input": "jam_pengingat", "set_huruf": "huruf",
        "set_kecepatan": "kecepatan", "set_autoplay": "autoplay",
        "set_tajwid": "tajwid", "set_notif_leader": "notif_leader",
        "tema_aplikasi": "tema", "bahasa_aplikasi": "bahasa",
    }
    for key, field in pemetaan.items():
        if field not in data:
            continue
        value = data[field]
        if key == "set_jam_input" and isinstance(value, str):
            try:
                value = datetime.strptime(value, "%H:%M").time()
            except Exception:
                value = None
        st.session_state[key] = value
    tema = data.get("tema", tema)
    bahasa = data.get("bahasa", bahasa)
    BAHASA_ARAB = "Arab" in str(bahasa) or "العربية" in str(bahasa)
    st.session_state["_tampilan_aktif"] = {"tema": tema, "bahasa": bahasa}
    # Hidrasi data lama/global bukan perubahan pengguna: jangan mengubah jam simpan.
    if "_qori_buat_snapshot" in globals():
        st.session_state["_qori_global_signature"] = _qori_signature_snapshot(_qori_buat_snapshot())


def qori_terpilih() -> str:
    pilihan = st.session_state.get("set_suara")
    if pilihan in QORI_LIST:
        return pilihan
    pilihan = (st.session_state.get("data_tersimpan") or _DISK_CFG or {}).get("qori")
    return pilihan if pilihan in QORI_LIST else QORI_LIST[0]

# CSS GLOBAL: paksa Light Mode dan keterbacaan di desktop/HP.
# Blok CSS ini ditempatkan setelah set_page_config agar sesuai aturan Streamlit.
rtl = """html, body, .stApp, [data-testid="stSidebar"], [data-testid="stMainBlockContainer"] { direction: rtl !important; }
[data-testid="stSidebar"] .stButton button { text-align: right !important; }
[data-testid="stSidebar"] .sb-brand { text-align: center !important; }""" if BAHASA_ARAB else ""
st.markdown(f"""
<style>
:root, html, body, .stApp, [data-testid="stApp"],
[data-testid="stAppViewContainer"], [data-testid="stMain"],
[data-testid="stMainBlockContainer"] {{ color-scheme:light !important; background:#fff !important; color:#111 !important; }}
html body [data-testid="stApp"] div.stButton > button:not([kind="primary"]),
html body [data-testid="stApp"] [data-testid="stDownloadButton"] button {{ background:#fff !important; background-color:#fff !important; color:#111 !important; border:1.5px solid #111 !important; font-weight:700 !important; opacity:1 !important; }}
html body [data-testid="stApp"] div.stButton > button:not([kind="primary"]) *,
html body [data-testid="stApp"] [data-testid="stDownloadButton"] button * {{ color:#111 !important; font-weight:700 !important; opacity:1 !important; }}
html body [data-testid="stApp"] div.stButton > button[kind="primary"],
html body [data-testid="stApp"] div.stButton > button[data-testid="stBaseButton-primary"] {{ background:#2563eb !important; background-color:#2563eb !important; color:#fff !important; border:1.5px solid #2563eb !important; font-weight:700 !important; }}
html body [data-testid="stApp"] div.stButton > button[kind="primary"] *,
html body [data-testid="stApp"] div.stButton > button[data-testid="stBaseButton-primary"] * {{ color:#fff !important; font-weight:700 !important; }}
html body [data-testid="stApp"] [data-testid="stWidgetLabel"],
html body [data-testid="stApp"] [data-testid="stWidgetLabel"] *,
html body [data-testid="stApp"] .stRadio label,
html body [data-testid="stApp"] .stRadio label * {{ color:#111 !important; font-weight:700 !important; opacity:1 !important; }}
html body [data-testid="stApp"] .stRadio label {{ font-size:17px !important; }}
html body [data-testid="stApp"] [data-testid="stMetricValue"],
html body [data-testid="stApp"] [data-testid="stMetricValue"] * {{ color:#111 !important; font-weight:800 !important; opacity:1 !important; }}
html body [data-testid="stApp"] input,
html body [data-testid="stApp"] textarea,
html body [data-testid="stApp"] [data-baseweb="select"] > div,
html body [data-testid="stApp"] [data-baseweb="input"] > div,
html body [data-testid="stApp"] [data-testid="stFileUploaderDropzone"],
html body [data-testid="stApp"] [data-testid="stFileUploader"] section {{ background:#fff !important; background-color:#fff !important; color:#111 !important; border-color:#94a3b8 !important; opacity:1 !important; }}
html body [data-testid="stApp"] input::placeholder,
html body [data-testid="stApp"] textarea::placeholder {{ color:#64748b !important; opacity:1 !important; }}
html body [data-testid="stApp"] [data-baseweb="select"] *,
html body [data-testid="stApp"] [data-baseweb="input"] *,
html body [data-testid="stApp"] [data-testid="stFileUploader"] * {{ color:#111 !important; }}
html body [data-baseweb="popover"], html body [role="listbox"], html body [role="option"] {{ background:#fff !important; color:#111 !important; }}
@media (prefers-color-scheme:dark) {{ html, body, .stApp, [data-testid="stApp"] {{ color-scheme:light !important; }} }}
{rtl if BAHASA_ARAB else ''}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&family=Amiri:wght@400;700&display=swap');

:root {
  --navy:#092653; --blue:#1677e8; --ink:#102448; --muted:#61718d;
  --green:#08a979; --purple:#843fe0;
}
html, body, [class*="css"] { font-family:'Poppins',sans-serif; }
h1, h2, h3, h4, h5, h6, .brand h1, .welcome h2, .section-title, .panel h3, .mode-card h3,
.hero h1, .hero-small h2, .result-title, .welcome p, .activity, .rank { font-family:'Poppins',sans-serif !important; }
.stApp { background:#E9EDF2; color:var(--ink); }
.block-container { padding-top:4.6rem; padding-bottom:2rem; max-width:1600px; }
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
.pill { background:#e1edff; color:#1459ae; border-radius:30px; padding:9px 15px; font-weight:600; font-size:12px; text-align:center; }
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
.mode-card { border-radius:18px; padding:19px 20px; color:white; min-height:150px; box-shadow:0 8px 20px #153b6b20; }
.mode-card h3 { margin:0 0 5px; font-size:20px; font-weight:800; }
.mode-card p { font-size:12px; line-height:1.5; margin:0 0 13px; opacity:.95; }
.mode-card .symbol { font-size:30px; float:right; margin-left:10px; }
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
.rank.me { background:#eef6ff; border-radius:10px; padding-left:8px; padding-right:8px; }
.feature-grid { display:grid; grid-template-columns:repeat(5,1fr); gap:8px; text-align:center; }
.feature { padding:12px 5px; border-right:1px solid #e4ebf6; }
.feature:last-child { border:0; }
.feature b { display:block; font-size:12px; margin-top:5px; }
.feature span { font-size:25px; }
.feature small { color:#7383a0; font-size:10px; }
.activity { font-size:11px; padding:9px 0; border-bottom:1px solid #edf1f8; color:#243b60; }
.activity:last-child { border:0; }
.small-muted { color:#7383a0; font-size:11px; }
div[data-testid="stMetric"] { background:#f0f6ff; border-radius:13px; padding:10px; }
div[data-testid="stMetric"] label { color:#607492; }
.stButton button[kind="primary"] { border-radius:10px; background:linear-gradient(120deg,#1677e8,#0f5fc4); border:0; }
.stButton button[kind="primary"] p, .stButton button[kind="primary"] span { color:#fff !important; }
.stButton button { border-radius:10px; }
[data-testid="stRadio"] label p { font-size:16px; line-height:1.55; }

.chip-row { display:flex; gap:8px; flex-wrap:wrap; margin:4px 0 12px; }
.chip { background:#e8f1ff; color:#1459ae; border-radius:20px; padding:6px 13px; font-size:12px; font-weight:700; }
.chip.green { background:#e3f8f0; color:#067a55; }
.chip.purple { background:#f1e9fe; color:#6a2bc0; }
.quiz-card { background:#fff; border:1px solid #e2ebf9; border-radius:20px; padding:22px 26px; box-shadow:0 10px 26px #163c7012; margin-bottom:14px; }
.quiz-prompt { font-size:16px; font-weight:700; color:#102448; line-height:1.6; }
.quiz-arab { font-family:'Amiri',serif; font-size:36px; direction:rtl; text-align:right; line-height:1.95; color:#0c2d5f; margin:12px 0 2px; }
.arab { direction:rtl; text-align:right; unicode-bidi:embed; }
.lvl-badge { display:inline-block; border-radius:20px; padding:6px 14px; font-size:13px;
  font-weight:800; margin:2px 0 10px; border:1px solid transparent; }
.lvl-1 { background:#e3f8ec; color:#07734f; border-color:#08a979; }
.lvl-2 { background:#fff6dc; color:#8a6100; border-color:#e7b32b; }
.lvl-3 { background:#fdeaea; color:#a42328; border-color:#e5484d; }
[class*="st-key-radio_"] label p:dir(rtl) { direction:rtl; text-align:right; }
.quiz-note { font-size:11px; color:#7383a0; }
.result-hero { background:radial-gradient(circle at 85% 20%,#1d75b9 0,#103d75 35%,#092653 78%); border-radius:22px; padding:28px 30px; color:#fff; text-align:center; box-shadow:0 12px 28px #0b326326; }
.result-score { font-size:62px; font-weight:800; line-height:1; margin:10px 0 4px; }
.result-score span { font-size:22px; opacity:.7; }
.result-title { font-size:20px; font-weight:800; }
.result-sub { font-size:13px; color:#d5e5ff; }
.badge { display:inline-block; background:#ffffff1c; border:1px solid #ffffff33; border-radius:20px; padding:6px 14px; font-size:12px; font-weight:700; margin:12px 4px 0; }
.ayah { border-bottom:1px solid #eef2f9; padding:16px 2px; }
.ayah:last-child { border:0; }
.ayah-arab { font-family:'Amiri',serif; font-size:30px; direction:rtl; text-align:right; line-height:2; color:#0d2f5e; margin:8px 0 2px; }
.ayah-terjemah { font-size:13px; color:#3c5170; margin:4px 0 0; }
.ayah-latin { font-size:11px; color:#7383a0; font-style:italic; margin-top:4px; }
.ayah-no { display:inline-flex; width:28px; height:28px; border-radius:50%; background:#e6f0ff; color:#1359ae; font-size:12px; font-weight:700; align-items:center; justify-content:center; }
.meta-card { background:#fff; border:1px solid #e4ecfa; border-radius:18px; padding:16px 18px; box-shadow:0 7px 22px #163c7010; }
.materi-box { background:#f7faff; border:1px solid #e4ecfa; border-radius:12px; padding:12px 14px; font-size:13px; color:#31486b; }
.hero-small { border-radius:20px; padding:20px 24px; color:#fff; background:linear-gradient(120deg,#0f4a8c,#092653); margin-bottom:6px; }
.hero-small h2 { margin:0; font-size:24px; font-weight:800; }
.hero-small p { margin:4px 0 0; font-size:13px; color:#cfe2ff; }
.stRadio label p { font-size:15px; }
@media(max-width:900px) {
 .hero h1 {font-size:38px;} .hero-art {font-size:65px; right:2%;}
 .feature-grid {grid-template-columns:repeat(2,1fr);}
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
/* ===== Layout 2026 ===== */
.block-container { padding-top:2.2rem; padding-bottom:1.6rem;
  padding-left:1rem; padding-right:1rem; max-width:100%; }
.stApp { background:#E9EDF2; }
/* Header disembunyikan isinya, tapi tetap hidup agar tombol buka sidebar tampil */
header[data-testid="stHeader"] { display:block !important; background:transparent !important;
  height:auto !important; min-height:0 !important; pointer-events:none !important; }
[data-testid="stToolbar"] { display:flex !important; background:transparent !important;
  pointer-events:none !important; }
[data-testid="stToolbarActions"] { display:none !important; }
[data-testid="stDecoration"] { display:none !important; }
/* Tombol buka menu saat sidebar tertutup (mobile & desktop) */
[data-testid="stSidebarCollapsedControl"], button[data-testid="collapsedControl"],
[data-testid="stExpandSidebarButton"] { display:flex !important;
  position:fixed !important; top:12px !important; left:12px !important;
  width:42px !important; height:42px !important; align-items:center !important;
  justify-content:center !important; background:#0b2a5b !important; border:0 !important;
  border-radius:12px !important; box-shadow:0 6px 18px #0b2a5b55 !important;
  pointer-events:auto !important; visibility:visible !important; z-index:998000 !important; }
[data-testid="stExpandSidebarButton"] span { color:#fff !important; }
/* Saat sidebar tertutup, beri ruang di atas agar tombol tidak menutupi judul */
body:has([data-testid="stSidebar"][data-collapsed="true"]) .block-container,
body:has([data-testid="stSidebar"][data-collapsed="true"]) [data-testid="stMainBlockContainer"] {
  padding-top:84px !important; }

/* ---- Sidebar ---- */
[data-testid="stSidebar"] { background:#0b2a5b !important;
  width:278px !important; min-width:278px !important;
  max-width:278px !important; flex:0 0 278px !important;
  padding-top:14px !important; }
[data-testid="stSidebar"] > div:first-child { width:278px !important; min-width:278px !important;
  padding-top:0 !important; margin-top:0 !important; }
[data-testid="stSidebarHeader"] { display:flex !important; height:auto !important;
  min-height:34px !important; padding:2px 8px !important;
  justify-content:flex-end !important; }
[data-testid="stSidebarCollapseButton"], [data-testid="stSidebarCollapsedControl"],
button[data-testid="collapsedControl"] { display:flex !important;
  visibility:visible !important; }
[data-testid="stSidebarContent"] { padding:14px 0 0 !important; }
[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] { padding:0 16px 1rem; }
.sb-brand { text-align:center; padding:0 4px 12px; }
.sb-brand svg { width:66px; height:66px; margin-top:0; filter:drop-shadow(0 8px 14px #0005); }
.sb-brand h1 { font-size:30px; font-weight:800; letter-spacing:.5px; color:#fff; margin:6px 0 2px; padding-top:0 !important; line-height:1; }
.sb-brand p { font-size:11.5px; line-height:1.4; color:#c9dcff; margin:0; }
.sb-user { display:flex; align-items:center; gap:10px; margin:0 6px 12px; padding:8px 10px;
  border-radius:14px; background:#ffffff14; border:1px solid #ffffff1f; }
.sb-user img.sb-avatar { width:54px; height:54px; border-radius:50%; object-fit:cover;
  border:2px solid #ffffff66; flex:none; }
.sb-user .sb-avatar-emoji { width:54px; height:54px; border-radius:50%; display:flex;
  align-items:center; justify-content:center; background:#ffffff1f; font-size:26px; flex:none; }
.sb-user .sb-nama { font-size:12.5px; font-weight:700; color:#fff; line-height:1.25; }
.sb-user .sb-peran { font-size:10.5px; color:#c9dcff; margin-top:1px; line-height:1.35;
  white-space:normal; }
.sb-nav { display:flex; flex-direction:column; gap:2px; margin-top:4px; }
.nav-item { display:flex; align-items:center; gap:12px; padding:10px 13px; border-radius:11px;
  color:#d6e5ff !important; text-decoration:none !important; font-size:14px; font-weight:600;
  transition:background .18s, color .18s; }
.nav-item svg { width:19px; height:19px; flex:none; opacity:.92; }
.nav-item:hover { background:#ffffff12; color:#fff !important; }
.nav-item.active { background:#1f6feb; color:#fff !important; box-shadow:0 8px 18px #1f6feb4d; }
.nav-item .chev { margin-left:auto; font-size:11px; opacity:.85; }
.sub-nav { margin:2px 0 4px 21px; padding-left:12px; border-left:1px solid #ffffff1c;
  display:flex; flex-direction:column; gap:2px; }
.sub-item { display:flex; align-items:center; gap:10px; padding:8px 11px; border-radius:9px;
  color:#bcd2f5 !important; text-decoration:none !important; font-size:13px; font-weight:500; }
.sub-item svg { width:16px; height:16px; flex:none; opacity:.85; }
.sub-item:hover { background:#ffffff10; color:#fff !important; }
.sub-item.active { background:#ffffff17; color:#fff !important; }
.sb-note { margin-top:16px; padding:12px 14px; border-radius:13px; background:#ffffff0e;
  border:1px solid #ffffff12; font-size:11px; line-height:1.55; color:#c9dcff; }
.sb-note b { color:#fff; font-size:11.5px; }
.sb-status { display:flex; align-items:center; gap:8px; font-size:10.5px; color:#a7c4ee; margin:14px 2px 0; }
.sb-status.ok { color:#b6ecd2; }
.sb-dot { width:8px; height:8px; border-radius:50%; background:#f5a524; flex:none; }
.sb-dot.ok { background:#35d07f; }
.sb-logout { display:block; text-align:center; margin-top:10px; padding:8px; border-radius:10px;
  border:1px solid #ffffff24; color:#d6e5ff !important; text-decoration:none !important;
  font-size:11.5px; font-weight:600; }
.sb-logout:hover { background:#ffffff12; color:#fff !important; }
.sb-mosque { height:70px; margin:14px -14px -16px; }
.sb-mosque svg { width:100%; height:100%; display:block; }
.sb-save { font-size:10px; line-height:1.55; color:#9fb4d6; text-align:center;
  margin:8px 2px 0; }

/* ---- Topbar ---- */
.topbar { display:flex; align-items:center; justify-content:space-between; gap:18px; margin:0 2px 16px; }
.topbar h1 { font-size:26px; font-weight:800; color:#0f2549; margin:0; line-height:1.25; }
.topbar p { margin:3px 0 0; font-size:13px; color:#2f6fd0; font-weight:500; }
.topbar-right { display:flex; align-items:center; gap:14px; flex:none; }
.icon-btn { width:42px; height:42px; border-radius:50%; background:#fff; display:flex;
  align-items:center; justify-content:center; border:1px solid #e3ebf7;
  box-shadow:0 4px 12px #163c7012; position:relative; color:#27123b; }
.icon-btn svg { width:20px; height:20px; }
.icon-btn .notif-dot { position:absolute; top:8px; right:9px; width:9px; height:9px;
  border-radius:50%; background:#ef4444; border:2px solid #fff; }
.profile { display:flex; align-items:center; gap:10px; background:#fff; border:1px solid #e3ebf7;
  border-radius:30px; padding:5px 14px 5px 5px; box-shadow:0 4px 12px #163c7012;
  font-size:13.5px; font-weight:600; color:#173a6b; }
.profile .avatar { width:34px; height:34px; border-radius:50%; display:flex; align-items:center;
  justify-content:center; color:#fff; background:linear-gradient(135deg,#5aa9f5,#0b4fa8); }
.profile .avatar svg { width:19px; height:19px; }
.profile .chev { font-size:11px; color:#5d7194; }

/* ---- Hero ---- */
.hero { position:relative; border-radius:22px; min-height:330px; padding:32px 40px;
  color:#fff; overflow:hidden; background-size:cover; background-position:center 38%;
  box-shadow:0 18px 40px #0b32632e; display:flex; align-items:center; }
.hero:before { content:''; position:absolute; inset:0;
  background:linear-gradient(90deg,#061c3fe8 0%,#061c3f99 34%,#061c3f1a 58%,#061c3f00 72%,#061c3f66 100%); }
.hero:after { content:none; }
.hero-content { position:relative; z-index:1; margin-left:31%; max-width:640px; }
.hero-title { font-size:58px; font-weight:800; letter-spacing:1px; line-height:1; }
.hero-title span { color:#63dcec; }
.hero-sub { font-size:16px; line-height:1.5; color:#eaf3ff; margin:12px 0 20px; }
.hero-chips { display:flex; gap:12px; flex-wrap:wrap; }
.hero-chip { display:flex; align-items:center; gap:10px; border:1px solid #ffffff3d;
  background:#04152f66; border-radius:30px; padding:8px 17px 8px 9px; }
.hero-chip .ico { width:30px; height:30px; border-radius:9px; display:flex; align-items:center;
  justify-content:center; font-size:15px; color:#0b2a55; flex:none; }
.hero-chip b { display:block; font-size:13px; color:#fff; line-height:1.2; }
.hero-chip small { font-size:10px; color:#cfe2ff; }

/* ---- Mode cards ---- */
.mode-card { display:block; position:relative; border-radius:18px; min-height:172px;
  padding:22px 24px 20px; color:#fff; text-decoration:none !important; overflow:hidden;
  background-size:cover; background-position:right center; box-shadow:0 12px 26px #153b6b26;
  transition:transform .2s, box-shadow .2s; }
.mode-card:hover { transform:translateY(-3px); box-shadow:0 18px 34px #153b6b38; }
.mode-card:before { content:''; position:absolute; inset:0; }
.mode-card.iqro:before { background:linear-gradient(90deg,#04503aeb 0%,#04503aa6 48%,#04503a0d 82%); }
.mode-card.tahsin:before { background:linear-gradient(90deg,#073a7aeb 0%,#073a7aa6 48%,#073a7a0d 82%); }
.mode-card.tahfidz:before { background:linear-gradient(90deg,#3c1475eb 0%,#3c1475a6 48%,#3c14750d 82%); }
.mode-card > * { position:relative; z-index:1; }
.mode-card h3 { font-size:22px; margin:0 0 6px; font-weight:800; color:#fff; }
.mode-card p { font-size:12.5px; line-height:1.55; margin:0 0 16px; max-width:300px; color:#eaf4ff; }
.mode-btn { display:inline-flex; align-items:center; gap:8px; background:#fff; color:#0f3a6b;
  font-size:12.5px; font-weight:700; padding:9px 20px; border-radius:24px;
  box-shadow:0 6px 14px #0003; }
.mode-card:hover .mode-btn { background:#f2f8ff; }

/* ---- Panels ---- */
.panel { background:#fff; border:1px solid #e6eefb; border-radius:16px; padding:18px 20px;
  box-shadow:0 8px 22px #163c700f; height:100%; }
.panel-head { display:flex; align-items:center; justify-content:space-between; margin-bottom:12px; }
.panel-head h3 { margin:0; font-size:15.5px; font-weight:800; color:#102448;
  display:flex; align-items:center; gap:8px; }
.panel-link { font-size:12px; font-weight:700; color:#1677e8; text-decoration:none !important; }
.panel-link:hover { text-decoration:underline !important; }
.p-row { display:flex; align-items:center; gap:12px; margin:13px 0; }
.p-ico { width:40px; height:40px; border-radius:12px; display:flex; align-items:center;
  justify-content:center; font-size:18px; color:#fff; flex:none; }
.p-body { flex:1; min-width:0; }
.p-top { display:flex; justify-content:space-between; align-items:baseline;
  font-size:12px; font-weight:700; color:#1d3557; margin-bottom:6px; }
.p-top .lvl { font-style:normal; font-weight:600; color:#93a3bd; margin-left:8px; }
.p-top .pct { color:#7383a0; }
.stat-grid { display:grid; grid-template-columns:1fr 1fr; gap:10px; }
.stat { border-radius:14px; padding:12px 14px; border:1px solid #eef3fb;
  display:flex; flex-direction:column; gap:7px; }
.stat-ico { width:34px; height:34px; border-radius:10px; background:#fff; display:flex;
  align-items:center; justify-content:center; font-size:16px; box-shadow:0 3px 8px #163c700f; }
.stat span { font-size:11px; font-weight:600; color:#61718d; }
.stat strong { font-size:22px; line-height:1; color:#102448; font-weight:800; }
.stat strong small { font-size:11px; font-weight:600; color:#61718d; margin-left:3px; }
.rank { display:flex; align-items:center; gap:10px; padding:7px 8px; border-radius:12px; }
.rank.me { background:#e8f2ff; }
.rank-badge { width:22px; height:22px; border-radius:50%; display:flex; align-items:center;
  justify-content:center; font-size:11px; font-weight:800; color:#5b4300; background:#eef2f9;
  flex:none; }
.rank-badge.r1 { background:#ffd75e; }
.rank-badge.r2 { background:#dfe7f2; color:#4b5b70; }
.rank-badge.r3 { background:#f4c9a0; color:#6b3f1c; }
.rank-ava { width:30px; height:30px; border-radius:50%; display:flex; align-items:center;
  justify-content:center; font-size:10.5px; font-weight:700; color:#fff; flex:none; }
.rank-name { flex:1; font-size:12.5px; font-weight:600; color:#1d3557;
  white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.rank-score { font-size:12.5px; font-weight:800; color:#0f2549; }

/* ---- Features & activities ---- */
.feature-grid { display:grid; grid-template-columns:repeat(5,1fr); gap:6px; }
.feature { text-align:center; padding:6px 8px; position:relative; }
.feature + .feature:before { content:''; position:absolute; left:0; top:14%; bottom:14%;
  width:1px; background:#e8eef9; }
.f-ico { width:46px; height:46px; border-radius:50%; display:flex; align-items:center;
  justify-content:center; margin:0 auto 8px; font-size:21px; }
.feature b { display:block; font-size:12px; color:#102448; }
.feature small { display:block; font-size:10px; color:#7383a0; margin-top:2px; line-height:1.35; }

/* ---- Feature cards as real buttons ---- */
.st-key-panel_fitur { background:#fff; border:1px solid #e6eefb; border-radius:16px;
  padding:17px 18px 14px; box-shadow:0 7px 22px #163c7010; }
.st-key-panel_fitur .panel-head { margin-bottom:10px; }
.st-key-panel_fitur [data-testid="stHorizontalBlock"] { gap:6px; }
.st-key-panel_fitur [data-testid="stButton"] { margin:0; }
.st-key-fitur_btn_game button, .st-key-fitur_btn_ujian button,
.st-key-fitur_btn_nilai button, .st-key-fitur_btn_quran button,
.st-key-fitur_btn_ai button { background:#fff !important; border:1px solid #eef3fa !important;
  border-radius:14px !important; min-height:112px; padding:10px 6px !important;
  box-shadow:0 3px 10px #163c700a; white-space:normal; cursor:pointer;
  transition:transform .18s ease, box-shadow .18s ease, border-color .18s ease; }
.st-key-fitur_btn_game button:hover, .st-key-fitur_btn_ujian button:hover,
.st-key-fitur_btn_nilai button:hover, .st-key-fitur_btn_quran button:hover,
.st-key-fitur_btn_ai button:hover { transform:translateY(-3px);
  box-shadow:0 12px 24px #163c7022; border-color:#cfe3ff !important; background:#fbfdff !important; }
.st-key-fitur_btn_game button p, .st-key-fitur_btn_ujian button p,
.st-key-fitur_btn_nilai button p, .st-key-fitur_btn_quran button p,
.st-key-fitur_btn_ai button p { display:flex; flex-direction:column; align-items:center;
  font-size:12px !important; font-weight:700 !important; color:#102448 !important;
  line-height:1.3; margin:0; }
.st-key-fitur_btn_game button p::before, .st-key-fitur_btn_ujian button p::before,
.st-key-fitur_btn_nilai button p::before, .st-key-fitur_btn_quran button p::before,
.st-key-fitur_btn_ai button p::before { width:38px; height:38px; border-radius:50%;
  display:flex; align-items:center; justify-content:center; font-size:19px; margin:0 auto 7px; }
.st-key-fitur_btn_game button p::after, .st-key-fitur_btn_ujian button p::after,
.st-key-fitur_btn_nilai button p::after, .st-key-fitur_btn_quran button p::after,
.st-key-fitur_btn_ai button p::after { font-size:10px; font-weight:500; color:#7383a0;
  margin-top:2px; }
.st-key-fitur_btn_game button p::before { content:"🎮"; background:#e9f2ff; }
.st-key-fitur_btn_game button p::after { content:"Iqro', Tahsin, Tahfidz"; }
.st-key-fitur_btn_ujian button p::before { content:"📝"; background:#eaf8f1; }
.st-key-fitur_btn_ujian button p::after { content:"Evaluasi pemahaman"; }
.st-key-fitur_btn_nilai button p::before { content:"📊"; background:#eaf8f1; }
.st-key-fitur_btn_nilai button p::after { content:"Progress belajar"; }
.st-key-fitur_btn_quran button p::before { content:"📖"; background:#fdf4e3; }
.st-key-fitur_btn_quran button p::after { content:"Juz 30 & Navigasi Ayat"; }
.st-key-fitur_btn_ai button p::before { content:"🤖"; background:#f2eafe; }
.st-key-fitur_btn_ai button p::after { content:"Tanya Seputar Al-Qur'an & Tajwid"; }

/* ---- Nilai & Hasil: aksi pengelola ---- */
.st-key-btn_reset_nilai button { background:#e5484d !important; border:1px solid #e5484d !important;
  box-shadow:0 6px 16px #e5484d33; }
.st-key-btn_reset_nilai button:hover { background:#cf3a3f !important; border-color:#cf3a3f !important; }
.st-key-btn_reset_nilai button p { color:#fff !important; font-weight:800; }
.st-key-btn_reset_ya button { background:#e5484d !important; border:1px solid #e5484d !important; }
.st-key-btn_reset_ya button:hover { background:#cf3a3f !important; border-color:#cf3a3f !important; }
.st-key-btn_reset_ya button p { color:#fff !important; font-weight:700; }
.nilai-meta { font-size:11px; color:#7383a0; }
.nilai-sep { height:1px; background:#eef2f9; margin:6px 0 10px; }
.act { display:flex; align-items:flex-start; gap:10px; padding:9px 0;
  border-bottom:1px solid #eef2f9; }
.act:last-child { border:0; }
.act-check { width:18px; height:18px; border-radius:50%; background:#e3f8ec; color:#08a979;
  display:flex; align-items:center; justify-content:center; font-size:10px; font-weight:800;
  flex:none; margin-top:1px; }
.act-body { flex:1; font-size:11.5px; color:#243b60; line-height:1.5; }
.act-time { font-size:10.5px; color:#8291aa; white-space:nowrap; text-align:right; }

@media(max-width:1200px) {
  .hero-content { margin-left:0; }
  .hero { background-position:center; }
  .hero:before { background:linear-gradient(90deg,#061c3fe8 0%,#061c3f99 60%,#061c3f66 100%); }
}
@media(max-width:900px) {
  .feature-grid { grid-template-columns:repeat(2,1fr); }
  .feature + .feature:before { display:none; }
  .hero-title { font-size:42px; }
  .topbar h1 { font-size:21px; }
  .topbar p { font-size:11.5px; }
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Penyimpanan
# ---------------------------------------------------------------------------
def rapikan_nama(nama: str) -> str:
    return " ".join(w.capitalize() for w in nama.split())


def _username_pengelola(nama: str | None = None) -> str:
    n = nama if nama is not None else st.session_state.get("user_name")
    return " ".join(str(n or "").strip().lower().split())


def level_pengelola(nama: str | None = None) -> str:
    n = _username_pengelola(nama)
    if n in SUPER_ADMIN:
        return "super_admin"
    if n in PENGELOLA_2 or n in PENGELOLA:
        return "pengelola_2"
    return ""


def aku_pengelola() -> bool:
    return st.session_state.get("user_role") == "Pengelola"


def aku_super_admin() -> bool:
    return aku_pengelola() and level_pengelola() == "super_admin"


def _muat_permintaan_izin() -> list:
    isi = _baca_json(IZIN_FILE, {"versi": 1, "permintaan": []})
    daftar = isi.get("permintaan") if isinstance(isi, dict) else None
    if not isinstance(daftar, list):
        daftar = []
    st.session_state["permintaan_izin"] = daftar
    return daftar


def _simpan_permintaan_izin(daftar: list):
    st.session_state["permintaan_izin"] = daftar
    _tulis_json(IZIN_FILE, {"versi": 1, "permintaan": daftar})


def _izin_aktif(nama: str | None = None) -> bool:
    if aku_super_admin():
        return True
    if not aku_pengelola():
        return False
    n = _username_pengelola(nama)
    daftar = st.session_state.get("permintaan_izin")
    if not isinstance(daftar, list):
        daftar = _muat_permintaan_izin()
    for p in daftar:
        if str(p.get("username") or "").strip().lower() != n:
            continue
        if p.get("status") != "disetujui":
            continue
        try:
            if datetime.fromisoformat(str(p.get("berlaku_hingga"))) > datetime.now():
                return True
        except (TypeError, ValueError):
            continue
    return False


def _boleh_ubah() -> bool:
    return aku_pengelola() and ((level_pengelola() == "super_admin")
                                or _izin_aktif())


def _izin_saya_terakhir() -> dict | None:
    n = _username_pengelola()
    daftar = st.session_state.get("permintaan_izin")
    if not isinstance(daftar, list):
        daftar = _muat_permintaan_izin()
    for p in daftar:
        if str(p.get("username") or "").strip().lower() == n:
            return p
    return None


def _batas_izin_teks(p: dict) -> str:
    try:
        return datetime.fromisoformat(str(p.get("berlaku_hingga"))).strftime("%d/%m/%Y %H:%M")
    except (TypeError, ValueError):
        return "-"


def kirim_permintaan_izin(aksi: str, alasan: str):
    daftar = _muat_permintaan_izin()
    daftar.insert(0, {
        "id": f"iz{int(datetime.now().timestamp() * 1000)}",
        "username": _username_pengelola(),
        "nama": st.session_state.get("user_name") or rapikan_nama(_username_pengelola()),
        "aksi": aksi,
        "alasan": alasan,
        "waktu": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "status": "menunggu",
        "berlaku_hingga": "",
    })
    _simpan_permintaan_izin(daftar)


def form_minta_izin(konteks: str):
    if not aku_pengelola() or aku_super_admin():
        return
    if _izin_aktif():
        st.success("✅ Izin edit aktif sampai "
                   + _batas_izin_teks(_izin_saya_terakhir() or {})
                   + ". Setelah waktu itu akses terkunci otomatis.")
        return
    terakhir = _izin_saya_terakhir()
    pesan = st.session_state.pop(f"_izin_info_{konteks}", None)
    if pesan:
        st.success(pesan)
    if terakhir and terakhir.get("status") == "menunggu":
        st.info("📨 Permintaan izin Anda masih menunggu persetujuan Pengelola 1: "
                + str(terakhir.get("aksi") or "-"))
        return
    with st.expander("📩 Minta Izin ke Pengelola 1", expanded=False):
        with st.form(f"form_minta_izin_{konteks}"):
            apa = st.text_area("Mau ubah apa?", key=f"izin_aksi_{konteks}",
                               placeholder="Contoh: Tambah siswa baru")
            alasan = st.text_area("Alasan", key=f"izin_alasan_{konteks}",
                                  placeholder="Contoh: Ada siswa pindahan")
            kirim = st.form_submit_button("Kirim Permintaan", type="primary",
                                          key=f"izin_kirim_{konteks}")
        if kirim:
            if not apa.strip():
                st.warning("Isi dulu bagian 'Mau ubah apa?'.")
            else:
                kirim_permintaan_izin(apa.strip(), alasan.strip())
                st.session_state[f"_izin_info_{konteks}"] = (
                    "✅ Permintaan izin terkirim. Menunggu persetujuan "
                    "Pengelola 1 (Kendar Sultoni).")
                st.rerun()


def data_awal():
    kelas_opsi = KELAS_OPSI
    siswa = [
        {"nama": rapikan_nama(nama), "program": program, "kelas": kelas_opsi[i % len(kelas_opsi)]}
        for i, (nama, program) in enumerate(SISWA_AWAL)
    ]
    return {
        "profil": {"nama": "Kendar Sultoni", "peran": "Siswa", "target": 15},
        "progress": {"Iqro'": {"xp": 0}, "Tahsin": {"xp": 0}, "Tahfidz": {"xp": 0}},
        "hasil": [],
        "papan": {},
        "siswa": siswa,
    }


def _baca_json(path: Path, default):
    try:
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
    except (json.JSONDecodeError, OSError):
        pass
    return default


def _tulis_json(path: Path, isi):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(isi, f, ensure_ascii=False, indent=2)


def _slug_nama(nama: str) -> str:
    bersih = "".join(c if c.isalnum() else "_" for c in str(nama).lower()).strip("_")
    return bersih or "pengguna"


def _hapus_berkas_foto(nama: str, kecuali: str | None = None):
    for ext in ("png", "jpg", "jpeg"):
        if kecuali and ext == kecuali:
            continue
        try:
            (FOTO_DIR / f"{_slug_nama(nama)}.{ext}").unlink(missing_ok=True)
        except Exception:
            pass


def _foto_data_uri_dari_nilai(nilai) -> str:
    """Normalisasi foto lama/data URI/bytes menjadi data URI."""
    if isinstance(nilai, dict):
        data = nilai.get("data")
        mime = nilai.get("mime") or "image/jpeg"
        if isinstance(data, str) and data.startswith("data:"):
            return data
        if isinstance(data, str):
            return f"data:{mime};base64,{data}"
        if isinstance(data, (bytes, bytearray)):
            return f"data:{mime};base64," + base64.b64encode(bytes(data)).decode("ascii")
        return ""
    rel = str(nilai or "").strip()
    if rel.startswith("data:image/"):
        return rel
    if rel:
        path = ASSETS / rel
        try:
            if path.exists():
                mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
                return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode("ascii")
        except Exception:
            pass
    return ""


def _foto_id_siswa(record=None, nama=None) -> str:
    record = record or {}
    if not record and nama:
        target = rapikan_nama(str(nama)).casefold()
        record = next((x for x in st.session_state.data.get("siswa", [])
                       if rapikan_nama(str(x.get("nama") or "")).casefold() == target), {})
    identitas = (record.get("id") or record.get("nis") or record.get("nisn")
                 or record.get("nama") or nama or "siswa")
    return re.sub(r"[^A-Za-z0-9_-]+", "_", str(identitas).strip())


def _user_settings_id() -> str:
    role = str(st.session_state.get("user_role") or "pengguna").strip().casefold()
    nama = str(st.session_state.get("user_name") or "anonim").strip().casefold()
    return f"{role}:{nama}"


def _app_settings_merge(user_id: str, perubahan: dict) -> tuple[bool, str | None]:
    """Tandai perubahan foto di state; snapshot global menyimpannya pada akhir rerun."""
    backup = st.session_state.setdefault("foto_profil_backup", {})
    for key, value in (perubahan or {}).items():
        if not str(key).startswith("foto_profil_"):
            continue
        if value:
            backup[str(key)] = value
        else:
            backup.pop(str(key), None)
    return True, None

def _muat_foto_profil_supabase():
    """Tampilkan foto dari snapshot global; fallback baca foto lama untuk migrasi tanpa mengubah jam."""
    marker = _user_settings_id()
    if st.session_state.get("_foto_supabase_loaded_for") == marker:
        return
    st.session_state["_foto_supabase_loaded_for"] = marker
    backup = st.session_state.setdefault("foto_profil_backup", {})
    # Snapshot global biasanya sudah memulihkan backup foto ke Session State.
    if not backup:
        client, _error = get_supabase_client()
        if client is not None:
            user_ids = [marker, "pengelola:kendar sultoni"]
            try:
                for uid in dict.fromkeys(user_ids):
                    hasil = (client.table("app_settings").select("settings")
                             .eq("user_id", uid).limit(1).execute())
                    rows = getattr(hasil, "data", None) or []
                    if rows and isinstance(rows[0].get("settings"), dict):
                        for key, value in rows[0]["settings"].items():
                            if str(key).startswith("foto_profil_") and isinstance(value, str) and value.startswith("data:image/"):
                                backup.setdefault(key, value)
            except Exception as exc:
                st.session_state["_foto_supabase_load_error"] = str(exc)
    for key, value in backup.items():
        if not isinstance(value, str) or not value.startswith("data:image/"):
            continue
        try:
            raw = base64.b64decode(value.split(",", 1)[1])
        except Exception:
            continue
        if key == "foto_profil_pengelola" and st.session_state.get("user_role") == "Pengelola":
            nama = st.session_state.get("user_name") or "Kendar Sultoni"
            st.session_state.setdefault("foto_profil", {})[nama] = {"data": raw, "mime": "image/jpeg"}
        elif key.startswith("foto_profil_siswa_"):
            sid = key[len("foto_profil_siswa_"):]
            for siswa_rec in st.session_state.data.get("siswa", []):
                if _foto_id_siswa(siswa_rec) == sid:
                    siswa_rec["foto"] = value
                    break
            if st.session_state.get("user_role") == "Siswa":
                nama_login = rapikan_nama(str(st.session_state.get("user_name") or "")).casefold()
                rec = next((x for x in st.session_state.data.get("siswa", [])
                            if rapikan_nama(str(x.get("nama") or "")).casefold() == nama_login), None)
                if rec and _foto_id_siswa(rec) == sid:
                    st.session_state.setdefault("foto_profil", {})[st.session_state.user_name] = {"data": raw, "mime": "image/jpeg"}
    # Hydrasi foto dari baris lama bukan perubahan pengguna; jangan ubah timestamp.
    if "_qori_buat_snapshot" in globals():
        st.session_state["_qori_global_signature"] = _qori_signature_snapshot(_qori_buat_snapshot())

def _pastikan_berkas_data():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    FOTO_DIR.mkdir(parents=True, exist_ok=True)
    bawaan = {
        USERS_FILE: {"akun": {}, "progress": {}, "siswa": [], "papan": {},
                     "foto": {}, "login_pertama": []},
        NILAI_FILE: {"hasil": []},
        PENGUMUMAN_FILE: {"pengumuman": []},
        NOTIF_FILE: {"notif": {}, "dilihat": {}, "seq": 0},
        MATERI_FILE: {"versi": 1, "materi": {}},
        SOAL_FILE: {"versi": 1, "banks": {}},
        SETTINGS_FILE: {"versi": 1, "terakhir_simpan": ""},
        IZIN_FILE: {"versi": 1, "permintaan": []},
    }
    for path, isi in bawaan.items():
        if not path.exists():
            _tulis_json(path, isi)


def _tulis_semua(data):
    foto_map = {}
    for nama, f in st.session_state.get("foto_profil", {}).items():
        if not f or not f.get("data"):
            continue
        ext = "png" if "png" in str(f.get("mime") or "png") else "jpg"
        FOTO_DIR.mkdir(parents=True, exist_ok=True)
        berkas = f"{_slug_nama(nama)}.{ext}"
        (FOTO_DIR / berkas).write_bytes(f["data"])
        foto_map[nama] = f"profile_pics/{berkas}"
    foto_base64_backup = dict(st.session_state.get("foto_profil_backup", {}) or {})
    for nama, foto_item in st.session_state.get("foto_profil", {}).items():
        uri = _foto_data_uri_dari_nilai(foto_item)
        if uri:
            foto_base64_backup[f"foto_profil_pengelola:{_slug_nama(nama)}"] = uri
    for siswa_item in data.get("siswa", []):
        sid = _foto_id_siswa(siswa_item)
        uri = _foto_data_uri_dari_nilai(siswa_item.get("foto"))
        if uri:
            foto_base64_backup[f"foto_profil_siswa_{sid}"] = uri
    _tulis_json(USERS_FILE, {
        "versi": 1,
        "akun": data.get("profil", {}),
        "progress": data.get("progress", {}),
        "siswa": data.get("siswa", []),
        "papan": data.get("papan", {}),
        "foto": foto_map,
        "foto_base64": foto_base64_backup,
        "login_pertama": sorted(st.session_state.get("login_pertama", set())),
        "nilai_mode": st.session_state.get("nilai_mode", "contoh"),
        "pengelola": dict(PENGELOLA),
    })
    _tulis_json(NILAI_FILE, {"versi": 1, "hasil": data.get("hasil", [])})
    _tulis_json(PENGUMUMAN_FILE, {
        "versi": 1, "pengumuman": st.session_state.get("pengumuman", []),
    })
    _tulis_json(NOTIF_FILE, {
        "versi": 1,
        "notif": st.session_state.get("notif", {}),
        "dilihat": {k: sorted(v) for k, v in
                    st.session_state.get("notif_dilihat", {}).items()},
        "seq": st.session_state.get("notif_seq", 0),
    })
    _tulis_json(MATERI_FILE, {
        "versi": 1,
        "materi": {m: {str(lvl): html for lvl, html in levels.items()}
                   for m, levels in MATERI.items()},
    })
    _tulis_json(SOAL_FILE, {"versi": 1, "banks": BANKS})
    cap_waktu = datetime.now().strftime("%d/%m/%Y %H:%M")
    st.session_state["terakhir_simpan"] = cap_waktu
    _tulis_json(SETTINGS_FILE, {"versi": 1, "terakhir_simpan": cap_waktu})


def _muat_pengelola():
    akun = _baca_json(USERS_FILE, {}).get("pengelola")
    if isinstance(akun, dict) and akun:
        PENGELOLA.clear()
        PENGELOLA.update({str(k).strip().lower(): str(v)
                          for k, v in akun.items() if str(k).strip()})


def load_all_data():
    _pastikan_berkas_data()
    lama = _baca_json(STORE, {})
    users = _baca_json(USERS_FILE, {})
    nilai = _baca_json(NILAI_FILE, {})
    peng = _baca_json(PENGUMUMAN_FILE, {})
    notif = _baca_json(NOTIF_FILE, {})
    materi = _baca_json(MATERI_FILE, {})
    soal = _baca_json(SOAL_FILE, {})
    settings = _baca_json(SETTINGS_FILE, {})

    data = data_awal()
    akun_pengelola = users.get("pengelola")
    if isinstance(akun_pengelola, dict) and akun_pengelola:
        PENGELOLA.clear()
        PENGELOLA.update({str(k).strip().lower(): str(v)
                          for k, v in akun_pengelola.items() if str(k).strip()})
    data["profil"] = users.get("akun") or lama.get("profil") or data["profil"]
    data["progress"] = users.get("progress") or lama.get("progress") or data["progress"]
    data["siswa"] = users.get("siswa") or lama.get("siswa") or data["siswa"]
    data["papan"] = users.get("papan") if "papan" in users else (lama.get("papan") or {})
    if nilai.get("versi"):
        data["hasil"] = nilai.get("hasil", [])
    elif lama.get("hasil"):
        data["hasil"] = lama["hasil"]
    for i, s in enumerate(data.get("siswa", [])):
        s.setdefault("kelas", KELAS_OPSI[i % len(KELAS_OPSI)])

    for mode, levels in (materi.get("materi") or {}).items():
        if mode in MATERI:
            for lvl, html in levels.items():
                try:
                    MATERI[mode][int(lvl)] = html
                except (ValueError, TypeError):
                    continue
    for mode, bank in (soal.get("banks") or {}).items():
        if mode in BANKS and isinstance(bank, list) and bank:
            BANKS[mode] = bank

    st.session_state.pengumuman = peng.get("pengumuman", [])
    st.session_state.notif = notif.get("notif", {})
    st.session_state.notif_dilihat = {
        k: set(v) for k, v in (notif.get("dilihat") or {}).items()
    }
    st.session_state.notif_seq = int(notif.get("seq", 0) or 0)
    st.session_state.login_pertama = set(users.get("login_pertama", []))
    st.session_state.nilai_mode = users.get("nilai_mode") or "contoh"
    st.session_state.mode_pengelola = ("Contoh" if st.session_state.nilai_mode == "contoh"
                                       else "Asli")
    st.session_state.login_baru = []
    st.session_state.peringkat_terakhir = {}
    st.session_state.terakhir_simpan = settings.get("terakhir_simpan") or ""

    foto = {}
    for nama, rel in (users.get("foto") or {}).items():
        path = ASSETS / str(rel)
        if path.exists():
            mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
            foto[nama] = {"data": path.read_bytes(), "mime": mime, "path": str(path)}
    st.session_state.foto_profil = foto
    foto_backup = users.get("foto_base64") or _baca_json(SETTINGS_FILE, {}).get("foto_profil", {})
    st.session_state["foto_profil_backup"] = foto_backup if isinstance(foto_backup, dict) else {}
    for siswa_item in data.get("siswa", []):
        sid = _foto_id_siswa(siswa_item)
        uri = st.session_state["foto_profil_backup"].get(f"foto_profil_siswa_{sid}")
        if uri and not siswa_item.get("foto"):
            siswa_item["foto"] = uri

    if (not users.get("versi") or not nilai.get("versi")
            or not materi.get("materi") or not soal.get("banks")):
        _tulis_semua(data)
    return data


def save_all_data():
    # Deteksi perubahan data yang dikelola Pengelola agar aktivitas CRUD ikut masuk notifikasi.
    if (st.session_state.get("user_role") == "Pengelola"
            and not st.session_state.get("_qori_memuat_snapshot")):
        objek_dilacak = {
            "siswa": st.session_state.get("data", {}).get("siswa", []),
            "materi": globals().get("MATERI", {}),
            "bank_soal": globals().get("BANKS", {}),
        }
        for nama_objek, nilai_objek in objek_dilacak.items():
            try:
                tanda = hashlib.sha256(json.dumps(
                    nilai_objek, ensure_ascii=False, sort_keys=True, default=str
                ).encode("utf-8")).hexdigest()
            except Exception:
                tanda = ""
            kunci_tanda = f"_qori_admin_sig_{nama_objek}"
            sebelumnya = st.session_state.get(kunci_tanda)
            if sebelumnya and tanda and tanda != sebelumnya:
                deskripsi = {
                    "siswa": "Data Siswa ditambah, diubah, atau dihapus oleh Pengelola.",
                    "materi": "Materi pembelajaran ditambah, diubah, atau dihapus oleh Pengelola.",
                    "bank_soal": "Bank soal diperbarui oleh Pengelola.",
                }.get(nama_objek, "Data aplikasi diperbarui oleh Pengelola.")
                menu_tujuan = {
                    "siswa": "Data Siswa", "materi": "Materi",
                    "bank_soal": "Ujian",
                }.get(nama_objek, "Dashboard")
                if "_qori_tambah_notif_admin" in globals():
                    _qori_tambah_notif_admin(
                        deskripsi, menu_tujuan,
                        event_key=f"admin:{nama_objek}:{tanda}",
                    )
            if tanda:
                st.session_state[kunci_tanda] = tanda

    _tulis_semua(st.session_state.data)
    # Sinkronkan seluruh data aplikasi setelah perubahan data inti.
    if "_qori_simpan_snapshot_global" in globals() and not st.session_state.get("_qori_memuat_snapshot"):
        _qori_simpan_snapshot_global(alasan="perubahan_data")


def _qori_tambah_notif_admin(teks: str, menu: str = "Dashboard",
                             event_key: str | None = None, mode: str = ""):
    """Tambahkan aktivitas ke kotak notifikasi seluruh akun Pengelola."""
    notif_map = st.session_state.setdefault("notif", {})
    seq = int(st.session_state.get("notif_seq", 0) or 0)
    sekarang = datetime.now(ZoneInfo("Asia/Jakarta"))
    waktu = sekarang.strftime("%d/%m/%Y %H:%M:%S WIB")
    dibuat = False
    for nama_admin in PENGELOLA:
        kunci_admin = str(nama_admin).title()
        daftar = notif_map.setdefault(kunci_admin, [])
        if event_key and any(n.get("event_key") == event_key for n in daftar):
            continue
        seq += 1
        daftar.insert(0, {
            "id": f"evt{seq}_{sekarang.strftime('%Y%m%d%H%M%S%f')}",
            "event_key": event_key or "",
            "teks": teks,
            "waktu": waktu,
            "dibaca": False,
            "menu": menu,
            "mode": mode,
        })
        del daftar[300:]
        dibuat = True
    if dibuat:
        st.session_state["notif_seq"] = seq
    return dibuat


def _qori_catat_aktivitas_siswa(teks: str, menu: str = "Dashboard",
                                 event_key: str | None = None, mode: str = "",
                                 persist: bool = True):
    """Catat aktivitas siswa untuk seluruh Pengelola dan simpan secara permanen."""
    if st.session_state.get("user_role") != "Siswa":
        return False
    nama = str(st.session_state.get("user_name")
               or st.session_state.get("data", {}).get("profil", {}).get("nama")
               or "Siswa")
    pesan = f"🧑‍🎓 <b>{html.escape(nama)}</b> — {teks}"
    dibuat = _qori_tambah_notif_admin(
        pesan, menu=menu, event_key=event_key, mode=mode
    )
    if dibuat and persist:
        save_all_data()
    return dibuat


def _segarkan_materi():
    """Muat materi tersimpan setiap rerun agar tambahan AI tidak hilang."""
    tersimpan = _baca_json(MATERI_FILE, {})
    levels = tersimpan.get("materi") if isinstance(tersimpan, dict) else None
    if not isinstance(levels, dict):
        return
    for mode, isi_level in levels.items():
        if mode not in MATERI or not isinstance(isi_level, dict):
            continue
        for lvl, isi in isi_level.items():
            try:
                MATERI[mode][int(lvl)] = isi
            except (ValueError, TypeError):
                continue


if "data" not in st.session_state:
    st.session_state.data = load_all_data()
_segarkan_materi()
_muat_pengelola()
if "menu" not in st.session_state:
    st.session_state.menu = "Dashboard"
if "mode" not in st.session_state:
    st.session_state.mode = "Iqro'"

PROGRAM_AWAL = {rapikan_nama(nama).lower(): program for nama, program in SISWA_AWAL}


def kelas_siswa():
    """Kelas akses siswa yang sedang login (None untuk Pengelola)."""
    if st.session_state.get("user_role") != "Siswa":
        return None
    nama = rapikan_nama(st.session_state.get("user_name")
                        or st.session_state.data["profil"]["nama"]).lower()
    for s in st.session_state.data.get("siswa", []):
        if rapikan_nama(str(s.get("nama") or "")).lower() == nama:
            program = str(s.get("program") or "").strip()
            if program in MODE_LIST:
                return program
    return PROGRAM_AWAL.get(nama, "Iqro'")


def mode_terkunci(mode: str) -> bool:
    kelas = kelas_siswa()
    return kelas is not None and mode != kelas


def kartu_terkunci(mode: str, key: str):
    kelas = kelas_siswa() or "Iqro'"
    st.markdown(f"""
    <div style="max-width:640px;margin:26px auto;background:#fff;border:1px solid #e3ebf7;
         border-radius:20px;padding:38px 34px;text-align:center;box-shadow:0 14px 34px #163c7014">
      <div style="font-size:52px;line-height:1">🔒</div>
      <h2 style="margin:12px 0 8px;color:#0f2549;font-size:24px">{T("Akses Terkunci", "Access Locked", "الوصول مقفل")}</h2>
      <p style="color:#4a5b78;font-size:14px;line-height:1.7;margin:0 auto;max-width:470px">
        {T("Kamu terdaftar di", "You are enrolled in", "أنت مسجل في")}
        <b>{T("Kelas", "Class", "الفصل")} {opsi_aman(kelas)}</b>.
        {T("Menu", "The menu", "قائمة")} {opsi_aman(mode)}
        {T("hanya untuk siswa Kelas", "is only for students of Class", "مخصصة فقط لطلاب الفصل")}
        {opsi_aman(mode)}.
        {T("Silakan hubungi Pengelola jika ingin pindah kelas.",
           "Please contact the Administrator if you want to change class.",
           "يرجى التواصل مع المشرف إذا أردت تغيير الفصل.")}
      </p>
    </div>
    """, unsafe_allow_html=True)
    _k1, k2, _k3 = st.columns([1.5, 1.2, 1.5])
    with k2:
        if st.button(T("🏠 Kembali ke Dashboard", "🏠 Back to Dashboard",
                       "🏠 العودة إلى لوحة التحكم"),
                     key=key, type="primary", use_container_width=True):
            st.session_state.menu = "Dashboard"
            st.session_state.pop("locked_mode", None)
            st.rerun()


def page_terkunci():
    kartu_terkunci(st.session_state.get("locked_mode") or "Tahsin",
                   "kembali_dashboard_terkunci")


# ---------------------------------------------------------------------------
# Supabase
# ---------------------------------------------------------------------------
@st.cache_resource(show_spinner=False)
def get_supabase_client():
    url = kredensial("SUPABASE_URL")
    key = kredensial("SUPABASE_ANON_KEY") or kredensial("SUPABASE_KEY")
    if not url or not key:
        return None, "Supabase belum dikonfigurasi (SUPABASE_URL & SUPABASE_KEY)."
    if create_client is None:
        return None, "Paket supabase belum terpasang. Jalankan: pip install supabase"
    try:
        return create_client(url, key), None
    except Exception as exc:
        return None, f"Gagal membuat klien Supabase: {exc}"


def _qori_json_aman(nilai):
    """Ubah nilai aplikasi menjadi struktur JSON; objek widget sementara dilewati."""
    if nilai is None or isinstance(nilai, (str, int, float, bool)):
        return nilai
    if isinstance(nilai, bytes):
        return {"__qori_bytes__": base64.b64encode(nilai).decode("ascii")}
    if isinstance(nilai, datetime):
        return {"__qori_datetime__": nilai.isoformat()}
    if isinstance(nilai, date):
        return {"__qori_date__": nilai.isoformat()}
    if isinstance(nilai, datetime_time):
        return {"__qori_time__": nilai.isoformat()}
    if isinstance(nilai, timedelta):
        return {"__qori_timedelta__": str(nilai)}
    if isinstance(nilai, set):
        return [_qori_json_aman(x) for x in sorted(nilai, key=str)]
    if isinstance(nilai, (list, tuple)):
        return [_qori_json_aman(x) for x in nilai]
    if isinstance(nilai, dict):
        hasil = {}
        for k, v in nilai.items():
            aman = _qori_json_aman(v)
            if aman is not _QORI_SKIP:
                hasil[str(k)] = aman
        return hasil
    # UploadedFile, client, fungsi, dan objek UI tidak boleh masuk ke JSONB.
    if hasattr(nilai, "getvalue") or callable(nilai):
        return _QORI_SKIP
    if hasattr(nilai, "to_dict"):
        try:
            return _qori_json_aman(nilai.to_dict())
        except Exception:
            return _QORI_SKIP
    return _QORI_SKIP


_QORI_SKIP = object()


def _qori_json_pulihkan(nilai):
    if isinstance(nilai, list):
        return [_qori_json_pulihkan(x) for x in nilai]
    if isinstance(nilai, dict):
        if set(nilai) == {"__qori_bytes__"}:
            try:
                return base64.b64decode(nilai["__qori_bytes__"])
            except Exception:
                return b""
        if set(nilai) == {"__qori_datetime__"}:
            try:
                return datetime.fromisoformat(nilai["__qori_datetime__"])
            except Exception:
                return nilai["__qori_datetime__"]
        if set(nilai) == {"__qori_date__"}:
            try:
                return date.fromisoformat(nilai["__qori_date__"])
            except Exception:
                return nilai["__qori_date__"]
        if set(nilai) == {"__qori_time__"}:
            try:
                return datetime_time.fromisoformat(nilai["__qori_time__"])
            except Exception:
                return nilai["__qori_time__"]
        if set(nilai) == {"__qori_timedelta__"}:
            return nilai["__qori_timedelta__"]
        return {k: _qori_json_pulihkan(v) for k, v in nilai.items()}
    return nilai


def _qori_key_tombol_sementara(nama: str) -> bool:
    """Tombol/aksi sekali klik tidak dipulihkan sebagai nilai input permanen."""
    nama = str(nama or "")
    return (
        nama in {"logout", "qori_simpan_global_pengaturan", "qori_download_global_json",
                 "qori_reset_global_data"}
        or nama.startswith(("nav_", "setujui_izin_", "tolak_izin_"))
        or nama.endswith(("_btn", "_button"))
        or "_submit_" in nama
    )


def _qori_kumpulkan_session():
    """Ambil state seluruh menu, tanpa kredensial dan metadata sementara penyimpanan/UI."""
    abaikan_tepat = {
        "T", "user_name", "user_role", "password", "login_password", "logged_in", "menu",
        "_global_snapshot_payload", "_global_snapshot_signature", "_qori_memuat_snapshot",
        "_qori_snapshot_loaded", "_qori_snapshot_loading", "_qori_global_signature",
        "_qori_global_last_saved", "_qori_global_dirty", "_qori_global_save_error",
        "_qori_global_load_error", "_pengaturan_dirty", "_pengaturan_dirty_at",
        "_pengaturan_status", "_pengaturan_last_saved", "_pengaturan_saved_signature",
        "_pengaturan_last_attempt_signature", "_pengaturan_global_hydrated",
        "_sig_autosave", "_foto_supabase_loaded_for", "_foto_supabase_load_error",
        "_foto_json_error", "_qori_widget_values",
    }
    hasil = {}
    for k in list(st.session_state.keys()):
        nama = str(k)
        nama_lc = nama.casefold()
        if (nama in abaikan_tepat or _qori_key_tombol_sementara(nama)
                or nama.startswith("foto_upload_") or nama.startswith("ai_mic")
                or any(token in nama_lc for token in ("password", "pass", "secret", "api_key", "token"))):
            continue
        try:
            aman = _qori_json_aman(st.session_state[k])
        except Exception:
            continue
        if aman is not _QORI_SKIP:
            hasil[nama] = aman
    return hasil

def _qori_kumpulkan_widget_values():
    """Simpan nilai widget lintas-menu agar state tidak hilang saat widget tidak dirender."""
    hasil = dict(st.session_state.get("_qori_widget_values") or {})
    abaikan = {
        "T", "user_name", "user_role", "password", "login_password", "logged_in",
        "menu", "data", "foto_profil", "foto_profil_backup", "pengumuman", "notif",
        "notif_dilihat", "notif_seq", "login_pertama", "login_baru", "quiz", "mini",
        "terakhir_simpan", "foto_profil_path", "confirm_reset",
    }
    for k in list(st.session_state.keys()):
        nama = str(k)
        nama_lc = nama.casefold()
        if (not nama or nama.startswith(("_", "$$")) or nama in abaikan
                or _qori_key_tombol_sementara(nama)
                or nama.startswith(("ai_mic", "foto_upload_"))
                or any(token in nama_lc for token in
                       ("password", "pass", "secret", "api_key", "token"))):
            continue
        try:
            aman = _qori_json_aman(st.session_state[k])
        except Exception:
            continue
        if aman is not _QORI_SKIP:
            hasil[nama] = aman
    return hasil


def _qori_pulihkan_widget_values():
    """Pulihkan nilai widget yang dibersihkan Streamlit ketika berpindah menu."""
    values = st.session_state.get("_qori_widget_values") or {}
    if not isinstance(values, dict):
        return
    for nama, nilai in values.items():
        nama = str(nama)
        if (not nama or nama.startswith(("_", "$$")) or
                any(token in nama.casefold() for token in
                    ("password", "pass", "secret", "api_key", "token"))):
            continue
        if nama not in st.session_state:
            try:
                st.session_state[nama] = _qori_json_pulihkan(nilai)
            except Exception:
                continue


def _qori_file_snapshot():
    """Ambil cadangan JSON dan berkas materi/foto yang sudah tersimpan lokal."""
    files = {}
    candidates = []
    if DATA_DIR.exists():
        # users.json memuat password pengelola; jangan pernah menyalinnya ke JSONB global.
        candidates.extend(p for p in DATA_DIR.rglob("*")
                          if p.is_file() and p != GLOBAL_SNAPSHOT_FILE and p != USERS_FILE)
    if AUTOSAVE_FILE.exists():
        candidates.append(AUTOSAVE_FILE)
    for folder in (FOTO_DIR, MATERI_ASSET_DIR):
        if folder.exists():
            candidates.extend(p for p in folder.rglob("*") if p.is_file())
    for path in dict.fromkeys(candidates):
        try:
            rel = str(path.relative_to(BASE_DIR)).replace("\\", "/")
            raw = path.read_bytes()
            files[rel] = base64.b64encode(raw).decode("ascii")
        except Exception:
            # File yang tidak dapat dibaca tidak menghentikan penyimpanan data lain.
            continue
    return files


def _qori_buat_snapshot():
    """Kumpulkan data inti, materi, chat, pengaturan, state semua menu, dan berkas terkait."""
    global_data = {}
    for nama in ("MATERI", "BANKS"):
        nilai = globals().get(nama)
        aman = _qori_json_aman(nilai)
        if aman is not _QORI_SKIP:
            global_data[nama] = aman
    widget_values = _qori_kumpulkan_widget_values()
    st.session_state["_qori_widget_values"] = widget_values
    return {
        "versi": 2,
        "data": _qori_json_aman(st.session_state.get("data", {})),
        # Key kanonis pengaturan dan nilai widget disimpan eksplisit agar
        # nilai tetap ada meskipun Streamlit membersihkan widget lintas halaman.
        "pengaturan": _qori_json_aman(_kumpulkan_pengaturan()),
        "widget_values": widget_values,
        "session": _qori_kumpulkan_session(),
        "globals": global_data,
        "files": _qori_file_snapshot(),
    }


def _qori_signature_snapshot(snapshot=None):
    if snapshot is None:
        snapshot = _qori_buat_snapshot()
    teks = json.dumps(snapshot, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(teks.encode("utf-8")).hexdigest()


def _qori_snapshot_encode(snapshot):
    raw = json.dumps(snapshot, ensure_ascii=False, separators=(",", ":"), default=str).encode("utf-8")
    packed = gzip.compress(raw, compresslevel=6, mtime=0)
    return base64.b64encode(packed).decode("ascii")


def _qori_snapshot_decode(encoded):
    packed = base64.b64decode(encoded)
    raw = gzip.decompress(packed)
    result = json.loads(raw.decode("utf-8"))
    return _qori_json_pulihkan(result)


def _qori_simpan_snapshot_global(alasan="autosave", manual=False):
    """Simpan seluruh state/data/berkas serializable semua menu tanpa menghapus key lama."""
    try:
        snapshot = _qori_buat_snapshot()
        signature = _qori_signature_snapshot(snapshot)
        if not manual and signature == st.session_state.get("_qori_global_signature"):
            return True, st.session_state.get("_qori_global_last_saved", "")
        saat = datetime.now(ZoneInfo("Asia/Jakarta"))
        waktu = saat.strftime("%d/%m/%Y %H:%M")
        snapshot["terakhir_disimpan"] = waktu
        encoded = _qori_snapshot_encode(snapshot)
        # Cadangan JSON lokal; Supabase tetap menjadi penyimpanan lintas perangkat.
        GLOBAL_SNAPSHOT_FILE.parent.mkdir(parents=True, exist_ok=True)
        GLOBAL_SNAPSHOT_FILE.write_text(json.dumps({
            "versi": 1, "encoding": "gzip+base64", "payload": encoded,
            "terakhir_disimpan": waktu,
        }, ensure_ascii=False, indent=2), encoding="utf-8")
        client, error = get_supabase_client()
        if client is None:
            st.session_state["_qori_global_save_error"] = error or "Supabase tidak tersedia."
            return False, st.session_state["_qori_global_save_error"]
        hasil = (client.table("app_settings").select("id,settings")
                 .eq("user_id", GLOBAL_SETTINGS_USER_ID).limit(1).execute())
        rows = getattr(hasil, "data", None) or []
        patch = {GLOBAL_SNAPSHOT_KEY: {
            "encoding": "gzip+base64", "payload": encoded,
            "terakhir_disimpan": waktu, "alasan": alasan,
        }}
        if rows:
            row = rows[0]
            settings_lama = row.get("settings") if isinstance(row, dict) else {}
            gabungan = dict(settings_lama) if isinstance(settings_lama, dict) else {}
            gabungan.update(patch)
            client.table("app_settings").update({
                "settings": gabungan, "updated_at": saat.isoformat(),
            }).eq("id", row["id"]).execute()
        else:
            client.table("app_settings").insert({
                "user_id": GLOBAL_SETTINGS_USER_ID, "settings": patch,
                "updated_at": saat.isoformat(),
            }).execute()
        st.session_state["_qori_global_signature"] = signature
        st.session_state["_qori_global_last_saved"] = waktu
        st.session_state["_qori_global_save_error"] = ""
        st.session_state["_qori_global_dirty"] = False
        st.session_state["_pengaturan_dirty"] = False
        st.session_state["_pengaturan_status"] = "saved"
        # Samakan cache pengaturan dan file JSON khusus dengan snapshot terbaru.
        cfg_terbaru = snapshot.get("pengaturan") or {}
        if isinstance(cfg_terbaru, dict):
            st.session_state["data_tersimpan"] = dict(cfg_terbaru)
            st.session_state["pengaturan_tersimpan"] = dict(cfg_terbaru)
            try:
                _tulis_json(AUTOSAVE_FILE, cfg_terbaru)
            except Exception:
                pass
        # Sidebar dirender sebelum isi halaman; satu rerun diperlukan agar jamnya sama.
        st.session_state["_qori_global_refresh_after_autosave"] = True
        return True, waktu
    except Exception as exc:
        st.session_state["_qori_global_dirty"] = True
        st.session_state["_qori_global_save_error"] = str(exc)
        return False, str(exc)


def _qori_terapkan_snapshot(snapshot):
    """Pulihkan berkas, data, materi, dan state sebelum halaman dirender."""
    if not isinstance(snapshot, dict):
        return False
    st.session_state["_qori_memuat_snapshot"] = True
    try:
        for rel, encoded in (snapshot.get("files") or {}).items():
            try:
                path = (BASE_DIR / str(rel)).resolve()
                if BASE_DIR.resolve() not in path.parents and path != BASE_DIR.resolve():
                    continue
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(base64.b64decode(encoded))
            except Exception:
                continue
        for nama, nilai in (snapshot.get("globals") or {}).items():
            if nama in ("MATERI", "BANKS") and isinstance(nilai, dict):
                target = globals().get(nama)
                if isinstance(target, dict):
                    target.clear()
                    target.update(nilai)
        data = snapshot.get("data")
        if isinstance(data, dict) and data:
            st.session_state["data"] = data
        pengaturan = snapshot.get("pengaturan")
        if isinstance(pengaturan, dict):
            # Pulihkan juga ke dua cache pengaturan lama agar widget lama tetap kompatibel.
            st.session_state["data_tersimpan"] = dict(pengaturan)
            st.session_state["pengaturan_tersimpan"] = dict(pengaturan)
            pemetaan_pengaturan = {
                "set_nama": "nama", "set_lembaga": "sekolah", "set_email": "email",
                "set_suara": "qori", "set_mode": "level", "set_iqro": "level_iqro",
                "set_target": "target", "set_reminder": "notifikasi",
                "set_jam_input": "jam_pengingat", "set_huruf": "huruf",
                "set_kecepatan": "kecepatan", "set_autoplay": "autoplay",
                "set_tajwid": "tajwid", "set_notif_leader": "notif_leader",
                "tema_aplikasi": "tema", "bahasa_aplikasi": "bahasa",
            }
            for kunci_widget, kunci_data in pemetaan_pengaturan.items():
                if kunci_data in pengaturan:
                    st.session_state[kunci_widget] = pengaturan[kunci_data]
        for k, v in (snapshot.get("session") or {}).items():
            if k in ("user_name", "user_role", "password", "login_password", "logged_in"):
                continue
            try:
                st.session_state[k] = v
            except Exception:
                continue
        widget_values = snapshot.get("widget_values") or {}
        if isinstance(widget_values, dict):
            st.session_state["_qori_widget_values"] = widget_values
            _qori_pulihkan_widget_values()
        st.session_state["_qori_global_last_saved"] = snapshot.get("terakhir_disimpan", "")
        return True
    finally:
        st.session_state.pop("_qori_memuat_snapshot", None)


def _qori_muat_snapshot_global():
    """Utamakan snapshot Supabase; JSON lokal menjadi fallback bila offline."""
    if st.session_state.get("_qori_snapshot_loaded"):
        return
    snapshot = None
    client, error = get_supabase_client()
    if client is not None:
        try:
            hasil = (client.table("app_settings").select("settings")
                     .eq("user_id", GLOBAL_SETTINGS_USER_ID).limit(1).execute())
            rows = getattr(hasil, "data", None) or []
            if rows:
                settings = rows[0].get("settings") or {}
                blob = settings.get(GLOBAL_SNAPSHOT_KEY) if isinstance(settings, dict) else None
                if isinstance(blob, dict) and blob.get("payload"):
                    snapshot = _qori_snapshot_decode(blob["payload"])
        except Exception as exc:
            st.session_state["_qori_global_load_error"] = str(exc)
    if snapshot is None:
        local = _baca_json(GLOBAL_SNAPSHOT_FILE, {})
        if isinstance(local, dict) and local.get("payload"):
            try:
                snapshot = _qori_snapshot_decode(local["payload"])
            except Exception:
                snapshot = None
    if snapshot:
        _qori_terapkan_snapshot(snapshot)
        # Jangan memuat ulang data lokal di atas snapshot Supabase: file lokal
        # pada perangkat baru bisa kosong/lama dan akan menimpa data terbaru.
        try:
            for nama, nilai in (snapshot.get("globals") or {}).items():
                target = globals().get(nama)
                if nama in ("MATERI", "BANKS") and isinstance(target, dict) and isinstance(nilai, dict):
                    target.clear()
                    target.update(nilai)
            for k, v in (snapshot.get("session") or {}).items():
                if k not in ("user_name", "user_role", "password", "login_password", "logged_in"):
                    st.session_state[k] = v
            widget_values = snapshot.get("widget_values") or {}
            if isinstance(widget_values, dict):
                st.session_state["_qori_widget_values"] = widget_values
                _qori_pulihkan_widget_values()
        except Exception as exc:
            st.session_state["_qori_global_load_error"] = str(exc)
        st.session_state["_qori_global_last_saved"] = snapshot.get("terakhir_disimpan", "")
        st.session_state["_qori_global_signature"] = _qori_signature_snapshot(_qori_buat_snapshot())
    st.session_state["_qori_snapshot_loaded"] = True


def _qori_pantau_perubahan_global():
    """Autosave semua perubahan state/widget sebelum dan sesudah halaman dirender."""
    if st.session_state.get("_qori_memuat_snapshot"):
        return
    # Pastikan input pengaturan selalu memiliki satu cache kanonis.
    if any(k in st.session_state for k in
           ("set_nama", "set_lembaga", "set_email", "tema_aplikasi", "bahasa_aplikasi")):
        cfg = _kumpulkan_pengaturan()
        st.session_state["data_tersimpan"] = dict(cfg)
        st.session_state["pengaturan_tersimpan"] = dict(cfg)
    snapshot = _qori_buat_snapshot()
    signature = _qori_signature_snapshot(snapshot)
    sebelumnya = st.session_state.get("_qori_global_signature")
    if sebelumnya is None:
        st.session_state["_qori_global_signature"] = signature
        return
    if signature != sebelumnya:
        st.session_state["_qori_global_dirty"] = True
        ok, detail = _qori_simpan_snapshot_global(alasan="perubahan_otomatis")
        if ok:
            st.session_state["_qori_global_refresh_after_autosave"] = True
        else:
            st.session_state["_qori_global_save_error"] = str(detail)


# Pulihkan snapshot global setelah konektor Supabase tersedia dan sebelum halaman dirender.
_qori_muat_snapshot_global()
_qori_pulihkan_widget_values()

@st.cache_resource(show_spinner=False)
def get_openai_client():
    if not OPENAI_API_KEY or OpenAI is None:
        return None
    try:
        return OpenAI(api_key=OPENAI_API_KEY, timeout=30.0, max_retries=1)
    except Exception:
        return None


@st.cache_data(ttl=60, show_spinner=False)
def load_students_supabase():
    client, error = get_supabase_client()
    if error:
        return [], error
    try:
        result = client.table("siswa").select("*").execute()
        return result.data or [], None
    except Exception as exc:
        return [], f"Tidak dapat membaca tabel public.siswa: {exc}"


def save_student_supabase(data, student_id=None):
    client, error = get_supabase_client()
    if error:
        return False, error
    try:
        if student_id is None:
            client.table("siswa").insert(data).execute()
        else:
            client.table("siswa").update(data).eq("id", student_id).execute()
        load_students_supabase.clear()
        return True, None
    except Exception as exc:
        return False, f"Gagal menyimpan data siswa: {exc}"


def delete_student_supabase(student_id):
    client, error = get_supabase_client()
    if error:
        return False, error
    try:
        client.table("siswa").delete().eq("id", student_id).execute()
        load_students_supabase.clear()
        return True, None
    except Exception as exc:
        return False, f"Gagal menghapus data siswa: {exc}"


# Hasil game & ujian: lokal (nilai.json) tetap jadi sumber utama,
# lalu disalin ke Supabase bila tersedia.
KOLOM_HASIL_GAME = ("nama", "mode", "benar", "salah", "poin", "tanggal",
                    "level", "jumlah_soal", "nilai")
KOLOM_HASIL_UJIAN = ("nama_siswa", "kelas", "materi", "skor", "jawaban",
                     "kategori", "nilai", "status_lulus", "tanggal")


@st.cache_data(ttl=600, show_spinner=False)
def kolom_hasil_supabase(tabel: str, kandidat: tuple) -> tuple:
    """Kolom yang benar-benar ada di tabel, agar cocok dengan skema Supabase guru."""
    client, error = get_supabase_client()
    if error:
        return ()
    ada = []
    for kolom in kandidat:
        try:
            client.table(tabel).select(kolom).limit(0).execute()
            ada.append(kolom)
        except Exception:
            pass
    return tuple(ada)


def _kirim_hasil_supabase(tabel, isi, kandidat) -> bool:
    client, error = get_supabase_client()
    if error:
        return False
    kolom = kolom_hasil_supabase(tabel, kandidat)
    if not kolom:
        return False
    data = {k: v for k, v in isi.items() if k in kolom}
    try:
        client.table(tabel).insert(data).execute()
        return True
    except Exception:
        st.toast("Hasil tersimpan di aplikasi, tetapi gagal dikirim ke Supabase.",
                 icon="⚠️")
        return False


def simpan_hasil_game(nama_siswa, mode, level, benar, total_soal, nilai):
    return _kirim_hasil_supabase("hasil_game", {
        "nama": nama_siswa,
        "mode": mode,
        "benar": int(benar),
        "salah": max(0, int(total_soal) - int(benar)),
        "poin": int(nilai),
        "tanggal": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "level": int(level),
        "jumlah_soal": int(total_soal),
        "nilai": int(nilai),
    }, KOLOM_HASIL_GAME)


def simpan_hasil_ujian(nama_siswa, kategori, materi, jawaban, nilai, status,
                       kelas=""):
    return _kirim_hasil_supabase("hasil_ujian", {
        "nama_siswa": nama_siswa,
        "kelas": kelas,
        "materi": materi,
        "skor": int(nilai),
        "jawaban": jawaban,
        "kategori": kategori,
        "nilai": int(nilai),
        "status_lulus": status,
        "tanggal": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }, KOLOM_HASIL_UJIAN)


# ---------------------------------------------------------------------------
# Login
# ---------------------------------------------------------------------------
SISWA_LOGIN = {
    nama.strip().lower(): nama for nama, _program in SISWA_AWAL
}


LOGIN_LOGO_SVG = (
    '<svg viewBox="0 0 220 190" xmlns="http://www.w3.org/2000/svg">'
    '<g fill="none" stroke="#22d7a6" stroke-width="9" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M46 138V88c0-28 28-44 64-44s64 16 64 44v50"/>'
    '<path d="M26 138h168"/>'
    '<path d="M46 104c-12 3-18 12-18 23v11h18M174 104c12 3 18 12 18 23v11h-18"/>'
    '<path d="M22 138h12M186 138h12"/>'
    '</g>'
    '<path d="M110 26c-17 11-29 21-29 34h58c0-13-12-23-29-34Z" fill="#f6c94a"/>'
    '<path d="M126 6a12 12 0 1 0 0 22 15 15 0 1 1 0-22Z" fill="#f6c94a"/>'
    '<path d="M110 104c-15-9-33-10-52-4v40c19-6 37-5 52 4 15-9 33-10 52-4v-40c-19-6-37-5-52 4Z" '
    'fill="#fffaf0" stroke="#f6c94a" stroke-width="6" stroke-linejoin="round"/>'
    '<path d="M110 104v40" stroke="#f6c94a" stroke-width="5" stroke-linecap="round"/>'
    '</svg>'
)


def render_login():
    login_bg_url = "https://raw.githubusercontent.com/sultonikendar31-lang/Qori-Ai/main/assets/login-bg.jpg"
    st.markdown(
        "<style>"
        "@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');"
        f"html,body,[data-testid='stApp'],.stApp,[data-testid='stAppViewContainer']{{"
        f"background-image:linear-gradient(rgba(0,0,0,.35),rgba(0,0,0,.35)),url('{login_bg_url}') !important;"
        "background-size:cover !important;background-position:center !important;"
        "background-repeat:no-repeat !important;background-attachment:fixed !important;"
        "background-color:transparent !important;}"
        "[data-testid='stMain'],.main,[data-testid='stMainBlockContainer']{"
        "background:transparent !important;}"
        ".login-brand,.login-brand .tag,.login-brand p{"
        "background:transparent !important;background-color:transparent !important;"
        "border-radius:0 !important;box-shadow:none !important;}"
        "header[data-testid='stHeader'],[data-testid='stToolbar'],[data-testid='stDecoration'],"
        "[data-testid='stSidebar'],[data-testid='stSidebarCollapsedControl']{display:none !important}"
        ".block-container{max-width:1560px;padding:8vh 48px 5vh !important}"
        "html,body,.stApp,.stMarkdown,input,button{font-family:'Poppins',system-ui,sans-serif}"
        ".login-brand{text-align:center;color:#fff;padding:0 16px}"
        ".login-logo svg{width:212px;height:auto;filter:drop-shadow(0 14px 34px #000c) "
        "drop-shadow(0 0 26px #22d7a655)}"
        ".login-brand h1{margin:0 0 8px;font-size:88px;font-weight:800;letter-spacing:4px;"
        "line-height:1;color:#fff;"
        "text-shadow:0 3px 0 #00000066,0 5px 16px #000000b3,0 12px 44px #000e}"
        ".login-brand h1 span{color:#fff}"
        ".login-brand .sub{display:inline-block;font-size:17px;font-weight:700;"
        "letter-spacing:1.6px;text-transform:lowercase;color:#FFD700 !important;margin:4px 0 0;"
        "padding:7px 24px;border-top:1.5px solid #ffd70099;border-bottom:1.5px solid #ffd70099;"
        "text-shadow:0 2px 10px #000c}"
        ".login-divider{display:flex;align-items:center;justify-content:center;gap:14px;"
        "margin:22px auto 20px;width:min(440px,82%);color:#f3cd72;font-size:13px}"
        ".login-divider:before,.login-divider:after{content:'';height:1.5px;flex:1;"
        "background:linear-gradient(90deg,transparent,#f3cd72b3)}"
        ".login-divider:after{background:linear-gradient(90deg,#f3cd72b3,transparent)}"
        ".login-brand .tag{font-size:19px;line-height:1.6;font-weight:500;color:#fff !important;"
        "max-width:540px;margin:0 auto;text-align:center;background:transparent !important;"
        "border:0 !important;border-radius:0;padding:0;text-shadow:0 2px 12px #000b}"
        ".login-footer{margin:26px auto 0;max-width:540px;text-align:left;font-size:12.5px;"
        "font-weight:500;color:#e3ecf8 !important;opacity:.92;text-shadow:0 1px 8px #000c}"
        ".st-key-login_card{background:linear-gradient(180deg,#ffffff,#fbfdff);border-radius:26px;"
        "padding:44px 44px 34px;border:1px solid #ffffffb0;"
        "box-shadow:0 34px 80px #0211268c,0 1px 0 #ffffff66 inset}"
        ".st-key-login_card [data-testid='stForm']{border:none;padding:0;background:transparent}"
        ".login-head h2{margin:0;font-size:38px;font-weight:800;color:#0c1c3a;"
        "text-align:center;letter-spacing:-.4px}"
        ".login-head p{margin:12px 0 30px;font-size:15px;line-height:1.6;color:#42557a;"
        "text-align:center}"
        ".login-mini{display:flex;align-items:center;justify-content:center;gap:11px;"
        "margin:-6px 0 16px}"
        ".login-mini svg{width:50px;height:auto;filter:drop-shadow(0 5px 14px #0c1c3a33)}"
        ".login-mini b{font-size:14.5px;font-weight:700;color:#0c1c3a;letter-spacing:.4px}"
        ".st-key-login_card [data-testid='InputInstructions']{display:none !important}"
        ".st-key-login_card [data-testid='stTextInput'] button{color:#1466d8 !important;"
        "opacity:1 !important;font-size:19px}"
        ".st-key-login_card label p{font-size:14.5px !important;font-weight:700 !important;"
        "color:#102448 !important;display:flex;align-items:center;gap:7px}"
        ".st-key-login_card [data-testid='stWidgetLabel'] p>span[role='img']{"
        "color:#102448 !important;font-size:21px !important;margin-right:5px;"
        "vertical-align:middle}"
        ".st-key-login_card [data-testid='stTextInput'] input{height:52px;border-radius:11px;"
        "border:1.5px solid #cdd9ea;font-size:15px;color:#102448;background:#fbfdff;"
        "padding-left:14px}"
        ".st-key-login_card [data-testid='stTextInput'] input:focus{border-color:#2b7fe8;"
        "box-shadow:0 0 0 3px #2b7fe822}"
        ".st-key-login_card [data-testid='stTextInput'] input::placeholder{color:#8fa3c2}"
        ".st-key-login_card [data-testid='stFormSubmitButton'] button{height:56px;border-radius:12px;"
        "background:linear-gradient(135deg,#1e7cf0 0%,#12b8a6 100%);border:0;font-size:17px;"
        "font-weight:700;color:#fff;box-shadow:0 14px 30px rgba(16,124,150,.38);"
        "margin-top:6px;transition:all .2s ease}"
        ".st-key-login_card [data-testid='stFormSubmitButton'] button:hover{"
        "background:linear-gradient(135deg,#3492ff 0%,#26d4c0 100%);box-shadow:0 18px 38px "
        "rgba(16,124,150,.5);transform:translateY(-1px)}"
        ".st-key-login_card [data-testid='stFormSubmitButton'] button p{font-size:17px !important;"
        "font-weight:700 !important;color:#fff !important}"
        ".st-key-login_card [data-testid='stFormSubmitButton'] [data-testid='stIconMaterial']{"
        "font-size:21px !important;color:#fff !important}"
        ".st-key-login_card [data-testid='stAlert']{border-radius:10px;margin-top:6px}"
        ".login-hint{display:flex;align-items:center;gap:10px;background:#d9f5f9;border-radius:11px;"
        "padding:13px 16px;margin-top:26px;font-size:14px;font-weight:600;color:#124457}"
        ".login-hint .pin{width:22px;height:22px;border-radius:50%;background:#18a8d8;color:#fff;"
        "display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:800;"
        "flex:none;font-style:italic}"
        ".login-hint b{background:#2f8fe6;color:#fff;border-radius:999px;padding:2px 10px;"
        "margin:0 2px;font-weight:700}"
        ".st-key-login_card [data-testid='stPopover'] button{background:#eef4fb;color:#1466d8;"
        "border:1px solid #cddff2;font-weight:600;font-size:12.5px;height:34px;"
        "border-radius:999px;padding:0 16px;margin:14px auto 0;display:block}"
        ".st-key-login_card [data-testid='stPopover'] button p{font-size:12.5px !important;"
        "font-weight:600 !important;color:#1466d8 !important}"
        "@media(max-width:1100px){.login-brand h1{font-size:64px;letter-spacing:2px}"
        ".login-brand .tag{font-size:16px}"
        ".login-brand .sub{font-size:14px}.login-logo svg{width:150px}"
        ".st-key-login_card{padding:30px 28px 26px}.login-head h2{font-size:31px}}"
        f"@media(max-width:860px){{"
        "html,body,[data-testid='stApp'],.stApp,[data-testid='stAppViewContainer']{"
        f"background-image:linear-gradient(rgba(0,0,0,.35),rgba(0,0,0,.35)),url('{login_bg_url}') !important;"
        "background-size:cover !important;background-position:center !important;"
        "background-repeat:no-repeat !important;background-attachment:scroll !important;"
        "background-color:transparent !important;}"
        "[data-testid='stMain'],.main,[data-testid='stMainBlockContainer']{background:transparent !important;}"
        ".block-container{padding:26px 16px !important}"
        ".login-brand{padding:6px 4px 0}.login-divider{display:none}"
        ".login-brand h1{font-size:46px;letter-spacing:1.5px}"
        ".login-brand .sub{font-size:12.5px;letter-spacing:1px;padding:6px 14px}"
        ".login-brand .tag{font-size:14px;padding:11px 16px;margin-top:16px}"
        ".login-footer{text-align:center;font-size:11.5px;margin-top:18px}"
        ".login-logo svg{width:116px}"
        ".st-key-login_card{padding:26px 20px 22px;border-radius:20px;margin-top:18px}"
        ".login-head h2{font-size:27px}.login-head p{font-size:13.5px;margin-bottom:18px}}"
        "</style>",
        unsafe_allow_html=True,
    )

    kiri, kanan = st.columns([1.15, 1], gap="large", vertical_alignment="center")
    with kiri:
        st.markdown(
            '<div class="login-brand"><div class="login-logo">' + LOGIN_LOGO_SVG + '</div>'
            '<h1>QORI <span>AI</span></h1>'
            '<p class="sub">Islamic Learning Management System</p>'
            '<div class="login-divider">◆</div>'
            '<p class="tag">'
            + T("Belajar Al-Qur'an lebih mudah, interaktif, dan menyenangkan "
                "dengan dukungan Artificial Intelligence.",
                "Learning the Qur'an is easier, interactive, and fun "
                "with Artificial Intelligence.",
                "تعلّم القرآن بسهولة وتفاعل ومتعة بدعم الذكاء الاصطناعي.")
            + '</p>'
            '<div class="login-footer">© 2026 QORI AI - Dibuat oleh Kendar Sultoni - Kelas 11</div>'
            '</div>',
            unsafe_allow_html=True,
        )
    with kanan:
        with st.container(key="login_card"):
            st.markdown(
                '<div class="login-mini">' + LOGIN_LOGO_SVG
                + '<b>QORI AI - Kelas 11</b></div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                '<div class="login-head"><h2>'
                + T("Login ke QORI AI", "Log in to QORI AI", "تسجيل الدخول إلى QORI AI")
                + '</h2><p>'
                + T("Silakan masukkan username dan password Anda<br>untuk mengakses aplikasi.",
                    "Please enter your username and password<br>to access the app.",
                    "يرجى إدخال اسم المستخدم وكلمة المرور<br>للوصول إلى التطبيق.")
                + '</p></div>',
                unsafe_allow_html=True,
            )
            with st.form("qori_login"):
                username_input = st.text_input(
                    T(":material/person: Username", ":material/person: Username",
                      ":material/person: اسم المستخدم"),
                    placeholder=T("Ketik nama lengkap (huruf kecil)",
                                  "Enter full name (lowercase)",
                                  "اكتب الاسم الكامل (بحروف صغيرة)"),
                )
                password_input = st.text_input(
                    T(":material/lock: Password", ":material/lock: Password",
                      ":material/lock: كلمة المرور"), type="password",
                    placeholder=T("Masukkan password", "Enter password", "أدخل كلمة المرور"),
                )
                masuk = st.form_submit_button(
                    T("Masuk", "Log in", "دخول"), type="primary", use_container_width=True,
                    icon=":material/arrow_forward:",
                )
            with st.popover("Lihat Daftar 20 Siswa"):
                daftar_nama = sorted(SISWA_LOGIN.values())
                kiri_nama, kanan_nama = st.columns(2)
                for i, nama_siswa in enumerate(daftar_nama):
                    (kiri_nama if i % 2 == 0 else kanan_nama).markdown(
                        f"{i + 1}. {nama_siswa}")
            if masuk:
                username = " ".join(username_input.strip().lower().split())
                password = password_input.strip()
                nama = peran = None
                if username in PENGELOLA and password == PENGELOLA[username]:
                    nama, peran = username.title(), "Pengelola"
                elif username in SISWA_LOGIN and password == PASSWORD_SISWA:
                    nama, peran = SISWA_LOGIN[username], "Siswa"
                if nama:
                    st.session_state.user_name = nama
                    st.session_state.user_role = peran
                    st.session_state["pengelola_level"] = (
                        level_pengelola(username) if peran == "Pengelola" else "")
                    st.session_state.data["profil"].update({"nama": nama, "peran": peran})
                    st.session_state.menu = "Dashboard"
                    st.session_state.pop("quiz", None)
                    if peran == "Siswa":
                        sudah_login = st.session_state.setdefault("login_pertama", set())
                        if nama not in sudah_login:
                            sudah_login.add(nama)
                            st.session_state.setdefault("login_baru", []).append(nama)
                        _qori_catat_aktivitas_siswa(
                            f"login ke QORI AI pada {datetime.now(ZoneInfo('Asia/Jakarta')).strftime('%H:%M:%S WIB')}.",
                            menu="Dashboard",
                            event_key=f"login:{nama}:{datetime.now(ZoneInfo('Asia/Jakarta')).strftime('%Y%m%d%H%M%S%f')}",
                            persist=False,
                        )
                        st.session_state["_qori_last_activity_menu"] = None
                    save_all_data()
                    st.rerun()
                else:
                    st.error(T("Username atau password salah. Periksa nama lengkap dan password Anda.",
                               "Incorrect username or password. Check your full name and password.",
                               "اسم المستخدم أو كلمة المرور غير صحيحة. تحقق من اسمك الكامل وكلمة المرور."))


if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "user_role" not in st.session_state:
    st.session_state.user_role = ""

if not st.session_state.user_name:
    render_login()
    st.stop()

_muat_pengaturan_supabase()
_muat_foto_profil_supabase()
st.session_state["permintaan_izin"] = _muat_permintaan_izin()
if st.session_state.get("user_role") == "Pengelola":
    st.session_state["pengelola_level"] = level_pengelola()
else:
    st.session_state["pengelola_level"] = ""


def level_dari_xp(xp: int):
    level = min(MAX_LEVEL, xp // XP_PER_LEVEL + 1)
    frac = 0.0 if level >= MAX_LEVEL else (xp % XP_PER_LEVEL) / XP_PER_LEVEL
    return level, frac


def tanggal_relatif(teks: str) -> str:
    try:
        dt = datetime.strptime(teks, "%Y-%m-%d %H:%M").date()
    except ValueError:
        return teks
    hari_ini = datetime.now().date()
    if dt == hari_ini:
        return "Hari ini"
    if dt == hari_ini - timedelta(days=1):
        return "Kemarin"
    return dt.strftime("%d %b")


def waktu_aktivitas(teks: str) -> str:
    rel = tanggal_relatif(teks)
    bagian = teks.split(" ")
    jam = bagian[-1].replace(":", ".") if len(bagian) > 1 else ""
    if rel in ("Hari ini", "Kemarin") and jam:
        return f"{rel}, {jam}"
    return rel


def papan_skor():
    rows = {}
    for h in st.session_state.data.get("hasil", []):
        nama_h = str(h.get("siswa") or "").strip()
        if not nama_h:
            continue
        rows[nama_h] = max(rows.get(nama_h, 0), int(h.get("skor", 0) or 0))
    return sorted(rows.items(), key=lambda kv: (-kv[1], kv[0]))


# ---------------------------------------------------------------------------
# Mesin kuis
# ---------------------------------------------------------------------------
def _nama_peserta():
    if st.session_state.get("user_role") == "Siswa":
        return str(st.session_state.data.get("profil", {}).get("nama") or "Siswa")
    return str(st.session_state.get("user_name") or "Pengelola")


def _rng_sesi(username, mode, level):
    """Acak deterministik per siswa per hari: refresh tetap sama, siswa/besok beda."""
    tgl = datetime.now().strftime("%Y%m%d")
    return random.Random(f"{str(username).strip().lower()}_{tgl}_{mode}_{level}")


def _kode_sesi(username, mode, level):
    nama = str(username).strip().upper().split()
    awal = nama[0] if nama else "SISWA"
    tgl = datetime.now().strftime("%d%m")
    level_teks = str(level).strip().upper().replace(" ", "-")
    if level_teks.isdigit():
        level_teks = "L" + level_teks
    return f"{awal}-{tgl}-{str(mode).strip().upper()}-{level_teks}"


def susun_soal(mode: str, level: int, tipe: str, rng=None):
    rng = rng or random
    bank = BANKS[mode]
    utama = [q for q in bank if q["level"] == level]
    lain = [q for q in bank if q["level"] != level]
    lain.sort(key=lambda q: (abs(int(q["level"]) - int(level)), int(q["level"])))
    batas = 10 if tipe == "ujian" else 20
    pilih = list(utama)
    if len(pilih) > batas:
        pilih = rng.sample(pilih, batas)
    elif len(pilih) < batas and lain:
        pilih += rng.sample(lain, min(batas - len(pilih), len(lain)))
    rng.shuffle(pilih)
    return pilih


def acak_pilihan(soal, rng=None):
    rng = rng or random
    salinan = dict(soal)
    salinan["options"] = list(salinan["options"])
    rng.shuffle(salinan["options"])
    return salinan


def susun_soal_ujian(mode: str, rng=None):
    rng = rng or random
    bank = BANKS[mode]

    def ambil(levels, n):
        pool = [q for q in bank if q["level"] in levels]
        rng.shuffle(pool)
        return [acak_pilihan(q, rng) for q in pool[:n]]

    soal = ambil((1, 2), 3) + ambil((3, 4), 4) + ambil((5, 6), 3)
    if len(soal) < 10:
        sisa = [acak_pilihan(q, rng) for q in bank if q not in soal]
        rng.shuffle(sisa)
        soal += sisa[:10 - len(soal)]
    return soal


def level_kelompok(level: int) -> int:
    return 1 if level <= 2 else (2 if level <= 4 else 3)


def badge_level(level: int):
    badge_tier(level_kelompok(level))


def badge_tier(tier: int):
    bintang, nama = MINI_LEVEL_NAMA[tier]
    st.markdown(f'<div class="lvl-badge lvl-{tier}">{bintang} Level: {nama}</div>',
                unsafe_allow_html=True)


def mulai_sesi(tipe: str, mode: str, level: int):
    data = st.session_state.data
    peserta = _nama_peserta()
    rng = _rng_sesi(peserta, mode, level)
    mulai = datetime.now()
    xp_awal = data["progress"].get(mode, {"xp": 0})["xp"]
    if tipe == "ujian":
        soal = susun_soal_ujian(mode, rng)
        if soal:
            level = round(sum(q["level"] for q in soal) / len(soal))
    else:
        soal = [acak_pilihan(q, rng) for q in susun_soal(mode, level, tipe, rng)]
    st.session_state.quiz = {
        "id": mulai.strftime("%H%M%S%f"),
        "acak_id": rng.randint(1, 99999),
        "tipe": tipe,
        "mode": mode,
        "level": level,
        "peserta": peserta,
        "seed": _kode_sesi(peserta, mode, level),
        "mulai": mulai.strftime("%Y-%m-%d %H:%M"),
        "selesai": None,
        "soal": soal,
        "idx": 0,
        "benar": 0,
        "picked": None,
        "finished": False,
        "xp_awal": xp_awal,
        "naik": False,
        "skor": 0,
        "batas": (mulai + timedelta(seconds=BATAS_UJIAN)) if tipe == "ujian" else None,
        "expired": False,
    }
    st.rerun()


def simpan_hasil(tipe: str, mode: str, level: int, benar: int, total: int, xp_awal: int):
    data = st.session_state.data
    skor = round(benar / total * 100)
    if st.session_state.user_role != "Siswa":
        return skor, False
    q = st.session_state.get("quiz") or {}
    selesai = datetime.now().strftime("%Y-%m-%d %H:%M")
    nama = data["profil"]["nama"]
    posisi_sebelum = next((i + 1 for i, (n, _) in enumerate(papan_skor()) if n == nama), None)
    data["hasil"].append({
        "siswa": data["profil"]["nama"],
        "tipe": tipe,
        "mode": mode,
        "level": level,
        "benar": benar,
        "total": total,
        "skor": skor,
        "tanggal": selesai,
        "seed": q.get("seed") or "",
        "mulai": q.get("mulai") or selesai,
        "selesai": selesai,
    })
    progres = data["progress"].setdefault(mode, {"xp": 0})
    progres["xp"] += skor
    data.setdefault("papan", {})
    data["papan"][nama] = max(data["papan"].get(nama, 0), skor)
    posisi_sesudah = next((i + 1 for i, (n, _) in enumerate(papan_skor()) if n == nama), None)
    if posisi_sebelum and posisi_sesudah and posisi_sesudah < posisi_sebelum:
        _qori_catat_aktivitas_siswa(
            f"naik peringkat Leaderboard dari #{posisi_sebelum} ke #{posisi_sesudah}.",
            menu="Leaderboard",
            event_key=f"rank:{nama}:{posisi_sebelum}:{posisi_sesudah}:{selesai}",
            persist=False,
        )
    save_all_data()
    if tipe == "ujian":
        simpan_hasil_ujian(nama, mode, str(level), [], skor,
                           "Lulus" if skor >= BATAS_TUNTAS else "Belum lulus")
    else:
        simpan_hasil_game(nama, mode, level, benar, total, skor)
    naik = level_dari_xp(progres["xp"])[0] > level_dari_xp(xp_awal)[0]
    if st.session_state.get("user_role") == "Siswa":
        tujuan_notif = "Ujian" if tipe == "ujian" else "Nilai & Hasil"
        label_tipe = "Ujian" if tipe == "ujian" else "Game"
        _qori_catat_aktivitas_siswa(
            f"menyelesaikan {label_tipe} <b>{html.escape(str(mode))}</b> level {level}, "
            f"nilai <b>{skor}</b>, memperoleh {skor} poin.",
            menu=tujuan_notif,
            mode=mode,
            event_key=f"aktivitas:{len(data['hasil']) - 1}:{nama}:{selesai}:{skor}",
        )
        if naik:
            _qori_catat_aktivitas_siswa(
                f"naik level pada mode <b>{html.escape(str(mode))}</b>.",
                menu="Belajar & Game",
                mode=mode,
                event_key=f"naik-level:{nama}:{mode}:{progres['xp']}:{selesai}",
            )
    return skor, naik


def selesaikan_sesi():
    q = st.session_state.quiz
    n = len(q["soal"])
    skor, naik = simpan_hasil(
        q["tipe"], q["mode"], q["level"], q["benar"], n, q["xp_awal"]
    )
    q["skor"] = skor
    q["naik"] = naik
    q["finished"] = True
    st.rerun()


def opsi_aman(teks: str) -> str:
    return html.escape(str(teks))


def ada_arab(teks) -> bool:
    return any("\u0600" <= ch <= "\u06FF" for ch in str(teks))


def _selesaikan_waktu():
    q = st.session_state.quiz
    skor, naik = simpan_hasil(
        q["tipe"], q["mode"], q["level"], q["benar"], len(q["soal"]), q["xp_awal"]
    )
    q.update(skor=skor, naik=naik, finished=True, expired=True)
    st.rerun(scope="app")


@st.fragment(run_every=1.0)
def tampilkan_timer_ujian():
    q = st.session_state.get("quiz")
    if not q or q.get("tipe") != "ujian" or q.get("finished"):
        return
    batas = q.get("batas")
    if not batas:
        return
    sisa = max(0, min(BATAS_UJIAN, int((batas - datetime.now()).total_seconds())))
    st.progress(sisa / BATAS_UJIAN,
                text=f"⏱ Sisa waktu {sisa // 60:02d}:{sisa % 60:02d} dari 10 menit")
    if sisa <= 0:
        _selesaikan_waktu()


def render_quiz():
    q = st.session_state.quiz
    mode, level, tipe = q["mode"], q["level"], q["tipe"]
    soal_list = q["soal"]
    n = len(soal_list)

    if q["finished"]:
        skor = q["skor"]
        benar = q["benar"]
        lulus = skor >= BATAS_TUNTAS
        judul = "Masya Allah, luar biasa!" if skor >= 90 else (
            "Alhamdulillah, bagus!" if lulus else "Terus semangat berlatih!"
        )
        judul_sesi = (f"📝 {opsi_aman(q['judul'])}" if q.get("judul")
                      else f"{MODE_ICON[mode]} {tipe.title()} {mode} · Level {level}")
        st.markdown(f"""
        <div class="result-hero">
          <div class="result-title">{judul_sesi}</div>
          <div class="result-score">{skor}<span>/100</span></div>
          <div class="result-sub">{judul} Jawaban benar {benar} dari {n} soal.</div>
          <div>
            <span class="badge">{'✅ Tuntas' if lulus else '📈 Perlu latihan lagi'}</span>
            <span class="badge">🎯 Batas tuntas {BATAS_TUNTAS}</span>{'<span class="badge">🚀 Naik level!</span>' if q.get("naik") else ''}{'<span class="badge">⏱ Waktu habis</span>' if q.get("expired") else ''}
          </div>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        k1, k2, k3 = st.columns(3)
        if k1.button("🔁 Ulangi sesi", use_container_width=True, type="primary"):
            mulai_sesi(tipe, mode, level)
        if k2.button("📊 Lihat Nilai & Hasil", use_container_width=True):
            st.session_state.pop("quiz", None)
            st.session_state.menu = "Nilai & Hasil"
            st.rerun()
        if k3.button("🏠 Kembali ke Dashboard", use_container_width=True):
            st.session_state.pop("quiz", None)
            st.session_state.menu = "Dashboard"
            st.rerun()
        return

    soal = soal_list[q["idx"]]
    if tipe == "ujian":
        tampilkan_timer_ujian()
    st.progress(q["idx"] / n, text=f"Soal {q['idx'] + 1} dari {n}")
    badge_level(soal["level"])
    arab_html = f'<div class="quiz-arab">{soal["arab"]}</div>' if soal["arab"] else ""
    st.markdown(f"""
    <div class="chip-row">
      <span class="chip">{MODE_ICON[mode]} Mode {mode}</span>
      <span class="chip purple">Level {level}</span>
      <span class="chip green">Benar: {q['benar']}</span>
    </div>
    <div class="quiz-card">
      <div class="quiz-prompt">{opsi_aman(soal['prompt'])}</div>{arab_html}
    </div>
    """, unsafe_allow_html=True)

    radio_key = f"radio_{q['id']}_{q['idx']}"
    picked = q["picked"]
    if picked is None:
        pilihan = st.radio(
            "Pilih satu jawaban", soal["options"], index=None,
            key=radio_key, label_visibility="collapsed",
        )
        if st.button("Kirim jawaban", type="primary", use_container_width=True,
                     disabled=pilihan is None):
            q["picked"] = pilihan
            if pilihan == soal["answer"]:
                q["benar"] += 1
            st.rerun()
    else:
        if picked == soal["answer"]:
            st.success("✅ Jawaban benar!")
        else:
            st.error(f"❌ Belum tepat. Jawaban yang benar: {soal['answer']}")
        if soal["bahas"]:
            st.info(soal["bahas"])
        terakhir = q["idx"] == n - 1
        label = "Lihat hasil →" if terakhir else "Soal berikutnya →"
        if st.button(label, type="primary", use_container_width=True):
            if terakhir:
                selesaikan_sesi()
            else:
                q["idx"] += 1
                q["picked"] = None
                st.rerun()

    if st.button("✖ Batalkan sesi", use_container_width=True):
        st.session_state.pop("quiz", None)
        st.rerun()


def render_start_sesi(tipe: str, mode: str, level: int, jumlah: int,
                      label: str = None, key: str = None, dengan_catatan: bool = True):
    label = label or ("Mulai Game" if tipe == "game" else "Mulai Ujian")
    if st.button(f"▶ {label}", type="primary", use_container_width=True, key=key):
        mulai_sesi(tipe, mode, level)
    if not dengan_catatan:
        return
    if st.session_state.user_role == "Siswa":
        st.caption(f"Sesi ini terdiri dari {jumlah} soal. Hasil otomatis masuk ke Nilai & Hasil.")
    else:
        st.caption(f"Sesi ini terdiri dari {jumlah} soal. Mode coba Pengelola: "
                   "nilai tidak dimasukkan ke peringkat.")


LOGO_SVG = (
    '<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">'
    '<defs><linearGradient id="qg" x1="0" y1="0" x2="1" y2="1">'
    '<stop offset="0" stop-color="#1d7a55"/><stop offset="1" stop-color="#0a3a2b"/>'
    '</linearGradient></defs>'
    '<path d="M32 2 58 11v22c0 14-11 24-26 29C17 57 6 47 6 33V11Z" fill="url(#qg)" '
    'stroke="#c9a24a" stroke-width="2.4"/>'
    '<path d="M32 8 52 15v17c0 11-8 19-20 24C20 51 12 43 12 32V15Z" fill="none" '
    'stroke="#e8c877" stroke-width="1" opacity=".55"/>'
    '<path d="M40.5 15.5a9.5 9.5 0 1 0 0 15 11.5 11.5 0 1 1 0-15Z" fill="#f2d27c"/>'
    '<path d="M19 38.5c6-4 9.5-4 13-2.5 3.5-1.5 7-1.5 13 2.5v8c-6-3-9.5-3-13 .5'
    '-3.5-3.5-7-3.5-13-.5Z" fill="#f7f2df"/>'
    '<path d="M32 36v10.5" stroke="#0a3a2b" stroke-width="1.4"/>'
    '</svg>'
)
MOSQUE_SVG = (
    '<svg viewBox="0 0 280 72" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none">'
    '<g fill="#ffffff" opacity="0.12">'
    '<path d="M0 72V55h20V43h8v12h12V37c0-10 9-16 16-25 7 9 16 15 16 25v18h12v-9h6v9h20V34'
    'c0-12 11-19 20-28 9 9 20 16 20 28v20h14v-8h6v8h20V46c0-9 8-14 14-21 6 7 14 12 14 21v9h16v-6h6v6h18V72Z"/>'
    '<circle cx="52" cy="26" r="4"/><circle cx="142" cy="22" r="4"/><circle cx="232" cy="34" r="4"/>'
    '</g></svg>'
)
BELL_SVG = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" '
            'stroke-linecap="round" stroke-linejoin="round"><path d="M18 8a6 6 0 0 0-12 0'
            'c0 7-3 8-3 8h18s-3-1-3-8"/><path d="M13.7 21a2 2 0 0 1-3.4 0"/></svg>')
USER_SVG = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
            'stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="4"/>'
            '<path d="M4 21a8 8 0 0 1 16 0"/></svg>')

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
_sb_client, _sb_error = get_supabase_client()
menu_aktif = st.session_state.menu


def nav_button(label: str, key: str, target: str, sub_mode: str | None = None,
               icon: str | None = None, terkunci: bool = False):
    active = st.session_state.menu == target and not sub_mode
    if st.sidebar.button(label, key=key, use_container_width=True, icon=icon,
                         type="primary" if active else "secondary"):
        if terkunci:
            st.session_state.menu = "Terkunci"
            st.session_state.locked_mode = sub_mode
        else:
            st.session_state.menu = target
            if sub_mode:
                st.session_state.mode = sub_mode
                st.session_state.mini_mode = sub_mode
        st.session_state.pop("quiz", None)
        st.rerun()


with st.sidebar:
    st.markdown(
        '<div class="sb-brand">' + LOGO_SVG +
        '<h1>QORI AI</h1><p>'
        + T("Islamic Learning<br>Management System",
            "Islamic Learning<br>Management System",
            "نظام إدارة<br>التعلم الإسلامي")
        + '</p></div>',
        unsafe_allow_html=True,
    )
    _sb_nama = st.session_state.user_name or st.session_state.data["profil"]["nama"]
    _sb_peran = st.session_state.user_role or st.session_state.data["profil"]["peran"]
    _sb_level = level_pengelola() if st.session_state.get("user_role") == "Pengelola" else ""
    if _sb_level == "super_admin":
        _sb_peran = f"👑 Pengelola 1 - Super Admin | {_sb_nama} | Akses Penuh"
    elif _sb_level == "pengelola_2":
        _sb_peran = (f"🛡️ Pengelola 2 - Admin Terbatas | {_sb_nama} | "
                     "Butuh Izin Pengelola 1 untuk Mengubah")
    _sb_foto = (st.session_state.get("foto_profil") or {}).get(_sb_nama)
    if _sb_foto and _sb_foto.get("data"):
        if _sb_foto.get("path"):
            st.session_state["foto_profil_path"] = _sb_foto["path"]
        st.markdown(
            '<div class="sb-user"><img class="sb-avatar" alt="Foto Profil" src="'
            + foto_data_uri(_sb_foto) + '"/><div><div class="sb-nama">'
            + opsi_aman(_sb_nama) + '</div><div class="sb-peran">'
            + opsi_aman(_sb_peran) + '</div></div></div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="sb-user"><div class="sb-avatar-emoji">👨‍🏫</div><div>'
            '<div class="sb-nama">' + opsi_aman(_sb_nama) + '</div>'
            '<div class="sb-peran">' + opsi_aman(_sb_peran) + '</div></div></div>',
            unsafe_allow_html=True,
        )
    nav_button(T("Dashboard", "Dashboard", "لوحة التحكم"), "nav_dashboard", "Dashboard",
               icon=":material/home:")
    nav_button(T("Belajar & Game", "Learn & Games", "تعلم وألعاب") + "  ▾",
               "nav_belajar", "Belajar & Game",
               icon=":material/sports_esports:")
    for mode, slug, ikon_mode in (("Iqro'", "iqro", ":material/menu_book:"),
                                  ("Tahsin", "tahsin", ":material/mic:"),
                                  ("Tahfidz", "tahfidz", ":material/layers:")):
        kunci = mode_terkunci(mode)
        label_mode = T(mode, mode, {"Iqro'": "إقرأ", "Tahsin": "تحسين",
                                    "Tahfidz": "تحفيظ"}[mode])
        nav_button(f"🔒 {label_mode}" if kunci else label_mode, f"nav_mode_{slug}",
                   "Belajar & Game", mode, icon=ikon_mode, terkunci=kunci)
    nav_button(T("Ujian", "Exam", "اختبار"), "nav_ujian", "Ujian", icon=":material/quiz:")
    nav_button(T("Nilai & Hasil", "Scores & Results", "الدرجات والنتائج"),
               "nav_nilai", "Nilai & Hasil", icon=":material/bar_chart:")
    nav_button(T("Leaderboard", "Leaderboard", "لوحة المتصدرين"),
               "nav_leaderboard", "Leaderboard",
               icon=":material/emoji_events:")
    nav_button(T("Materi", "Materials", "المواد"), "nav_materi", "Materi",
               icon=":material/library_books:")
    nav_button(T("Al-Qur'an (Juz 30)", "Al-Qur'an (Juz 30)", "القرآن (الجزء ٣٠)"),
               "nav_quran", "Al-Qur'an (Juz 30)",
               icon=":material/auto_stories:")
    nav_button(T("AI Assistant", "AI Assistant", "مساعد الذكاء الاصطناعي"),
               "nav_ai", "AI Assistant", icon=":material/smart_toy:")
    nav_button(T("Data Siswa", "Student Data", "بيانات الطلاب"),
               "nav_siswa", "Data Siswa", icon=":material/group:")
    if _sb_level == "super_admin":
        _jml_izin = sum(1 for p in st.session_state.get("permintaan_izin", [])
                        if p.get("status") == "menunggu")
        nav_button("👑 " + T("Kelola Pengelola", "Manage Managers", "إدارة المديرين")
                   + (f" ({_jml_izin})" if _jml_izin else ""),
                   "nav_kelola_pengelola", "Kelola Pengelola",
                   icon=":material/admin_panel_settings:")
    if _sb_level != "pengelola_2":
        _label_set = (T("Pengaturan Aplikasi", "App Settings", "إعدادات التطبيق")
                      if _sb_level == "super_admin" else
                      T("Pengaturan", "Settings", "الإعدادات"))
        nav_button(_label_set,
                   "nav_pengaturan", "Pengaturan", icon=":material/settings:")
    if _sb_level == "pengelola_2":
        if _izin_aktif():
            _sisa_izin = _izin_saya_terakhir() or {}
            st.markdown(
                '<div class="sb-status ok"><span class="sb-dot ok"></span>'
                '✅ Izin edit aktif s.d. ' + opsi_aman(_batas_izin_teks(_sisa_izin))
                + '</div>', unsafe_allow_html=True)
        form_minta_izin("sidebar")

    st.markdown(
        '<div class="sb-status' + (' ok' if not _sb_error else '') + '">'
        '<span class="sb-dot' + (' ok' if not _sb_error else '') + '"></span>' +
        (T("Supabase Terhubung ✅", "Supabase Connected ✅", "تم الاتصال بـ Supabase ✅")
         if not _sb_error else
         T("Supabase belum terhubung", "Supabase not connected",
           "لم يتم الاتصال بـ Supabase")) + '</div>',
        unsafe_allow_html=True,
    )
    if st.button(T("Keluar", "Log out", "تسجيل الخروج"), key="logout",
                 use_container_width=True):
        st.session_state.user_name = ""
        st.session_state.user_role = ""
        st.session_state.pop("pengelola_level", None)
        st.session_state.pop("permintaan_izin", None)
        st.session_state.pop("quiz", None)
        st.session_state.pop("mini", None)
        st.session_state.pop("chat_ai", None)
        for _kunci_ai in ("ai_percakapan", "ai_chat_aktif", "ai_sudah_dimuat",
                          "ai_kuis", "ai_kuis_hasil", "ai_audio_otomatis",
                          "ai_autoplay_id", "ai_mic_hash", "ai_flash",
                          "ai_flash_error", "ai_prompt_awal"):
            st.session_state.pop(_kunci_ai, None)
        for _kunci_mat in ("_kurikulum", "mat_flash", "mat_balloons",
                           "mat_filter_kategori", "mat_cari", "mat_filter_status"):
            st.session_state.pop(_kunci_mat, None)
        st.session_state.pop("menu", None)
        st.session_state.pop("locked_mode", None)
        st.rerun()
    _terakhir_global = st.session_state.get("_qori_global_last_saved") or "Belum ada penyimpanan"
    st.caption("🕒 Terakhir disimpan: " + str(_terakhir_global) + " WIB")
    st.markdown('<div class="sb-mosque">' + MOSQUE_SVG + '</div>', unsafe_allow_html=True)

HERO_IMG = asset_b64("hero.jpg")
CARD_IMG = {
    "iqro": asset_b64("card-iqro.jpg"),
    "tahsin": asset_b64("card-tahsin.jpg"),
    "tahfidz": asset_b64("card-tahfidz.jpg"),
}
st.markdown(
    "<style>"
    f".hero{{background-image:url('{HERO_IMG}')}}"
    ".st-key-mode_iqro{background-color:#08a978;background-image:"
    "linear-gradient(90deg,#04503af7 0%,#04503ae0 55%,#04503a80 78%,#04503a10 100%),"
    f"url('{CARD_IMG['iqro']}')}}"
    ".st-key-mode_tahsin{background-color:#1677e8;background-image:"
    "linear-gradient(90deg,#073a7af7 0%,#073a7ae0 55%,#073a7a80 78%,#073a7a10 100%),"
    f"url('{CARD_IMG['tahsin']}')}}"
    ".st-key-mode_tahfidz{background-color:#843fe0;background-image:"
    "linear-gradient(90deg,#3c1475f7 0%,#3c1475e0 55%,#3c147580 78%,#3c147510 100%),"
    f"url('{CARD_IMG['tahfidz']}')}}"
    ".st-key-mode_iqro,.st-key-mode_tahsin,.st-key-mode_tahfidz{background-size:cover;"
    "background-position:right center;border-radius:18px;padding:20px 24px 18px;min-height:172px;"
    "box-shadow:0 12px 26px #153b6b26;transition:transform .2s, box-shadow .2s}"
    ".st-key-mode_iqro:hover,.st-key-mode_tahsin:hover,.st-key-mode_tahfidz:hover{"
    "transform:translateY(-3px);box-shadow:0 18px 34px #153b6b38}"
    "[data-testid='stMainBlockContainer'] [data-testid='stVerticalBlock'] > div:has(.st-key-mode_iqro),"
    "[data-testid='stMainBlockContainer'] [data-testid='stVerticalBlock'] > div:has(.st-key-panel_board),"
    "[data-testid='stMainBlockContainer'] [data-testid='stVerticalBlock'] > div:has(.st-key-panel_fitur){"
    "margin-top:8px !important;}"
    "[data-testid='stMarkdownContainer']:has(.hero){margin-bottom:0 !important;}"
    ".st-key-mode_iqro h3,.st-key-mode_tahsin h3,.st-key-mode_tahfidz h3{"
    "color:#fff !important;font-size:22px;margin:0 0 6px;font-weight:800}"
    ".st-key-mode_iqro p,.st-key-mode_tahsin p,.st-key-mode_tahfidz p{"
    "color:#eaf4ff !important;font-size:12.5px;line-height:1.55;max-width:300px;margin:0 0 10px}"
    ".mode-tag{display:inline-block;background:#ffffff26;border:1px solid #ffffff3d;"
    "border-radius:999px;padding:3px 10px;font-size:10.5px;font-weight:600;color:#f2f8ff;"
    "margin:0 0 11px}"
    ".st-key-mode_iqro [data-testid='stButton'] button,.st-key-mode_tahsin [data-testid='stButton'] button,"
    ".st-key-mode_tahfidz [data-testid='stButton'] button{background:#fff !important;border:0;"
    "border-radius:24px;color:#0f3a6b !important;font-size:12.5px;font-weight:700;padding:7px 20px;"
    "box-shadow:0 6px 14px #0003;width:auto;min-height:0}"
    ".st-key-mode_iqro [data-testid='stButton'] button p,.st-key-mode_tahsin [data-testid='stButton'] button p,"
    ".st-key-mode_tahfidz [data-testid='stButton'] button p{color:#0f3a6b !important;font-weight:700}"
    ".st-key-panel_board{background:#fff;border:1px solid #e6eefb;border-radius:16px;"
    "padding:18px 20px;box-shadow:0 8px 22px #163c700f;min-height:252px;height:100%}"
    ".panel{min-height:252px}"
    ".st-key-lihat_semua{display:flex;justify-content:flex-end}"
    ".st-key-lihat_semua button{background:transparent !important;border:0 !important;"
    "color:#1677e8 !important;font-size:12px !important;font-weight:700 !important;"
    "padding:0 !important;min-height:0}"
    ".st-key-lihat_semua button p{color:#1677e8 !important;font-size:12px !important;"
    "font-weight:700 !important}"
    "[data-testid='stSidebar'] .stButton{margin:0}"
    "[data-testid='stSidebar'] .stButton button{width:100%;justify-content:flex-start;text-align:left;"
    "background:transparent !important;border:0 !important;border-radius:11px;color:#d6e5ff !important;"
    "font-size:14px;font-weight:600;padding:6px 12px;position:relative;min-height:0;"
    "box-shadow:none}"
    "[data-testid='stSidebar'] .stButton button > div{justify-content:flex-start !important;"
    "width:100%}"
    "[data-testid='stSidebar'] .stButton button [data-testid='stIconMaterial']{"
    "font-size:19px;color:inherit !important}"
    "[data-testid='stSidebar'] .stButton button p{font-size:14px !important;font-weight:600 !important;"
    "color:#d6e5ff !important}"
    "[data-testid='stSidebar'] .stButton button:hover{background:#ffffff14 !important}"
    "[data-testid='stSidebar'] .stButton button:hover p{color:#fff !important}"
    "[data-testid='stSidebar'] .stButton button[kind='primary'],"
    "[data-testid='stSidebar'] [data-testid='stBaseButton-primary']{background:#1f6feb !important;"
    "box-shadow:0 8px 18px #1f6feb4d}"
    "[data-testid='stSidebar'] .stButton button[kind='primary'] p,"
    "[data-testid='stSidebar'] [data-testid='stBaseButton-primary'] p{color:#fff !important}"
    "[data-testid='stSidebar'] .st-key-nav_mode_iqro button,"
    "[data-testid='stSidebar'] .st-key-nav_mode_tahsin button,"
    "[data-testid='stSidebar'] .st-key-nav_mode_tahfidz button{padding:4px 10px 4px 34px !important;"
    "font-size:13px !important;font-weight:500 !important;color:#bcd2f5 !important;border-radius:9px !important}"
    "[data-testid='stSidebar'] .st-key-nav_mode_iqro button [data-testid='stIconMaterial'],"
    "[data-testid='stSidebar'] .st-key-nav_mode_tahsin button [data-testid='stIconMaterial'],"
    "[data-testid='stSidebar'] .st-key-nav_mode_tahfidz button [data-testid='stIconMaterial']{"
    "font-size:16px !important}"
    "[data-testid='stSidebar'] .st-key-nav_mode_iqro button p,"
    "[data-testid='stSidebar'] .st-key-nav_mode_tahsin button p,"
    "[data-testid='stSidebar'] .st-key-nav_mode_tahfidz button p{font-size:13px !important;"
    "font-weight:500 !important;color:#bcd2f5 !important}"
    "[data-testid='stSidebar'] .st-key-nav_mode_iqro button:hover p,"
    "[data-testid='stSidebar'] .st-key-nav_mode_tahsin button:hover p,"
    "[data-testid='stSidebar'] .st-key-nav_mode_tahfidz button:hover p{color:#fff !important}"
    "[data-testid='stSidebar'] .st-key-logout button{border:1px solid #ffffff24 !important;"
    "border-radius:10px;margin-top:8px;padding:8px !important;justify-content:center !important;"
    "text-align:center !important;font-size:11.5px !important;color:#d6e5ff !important}"
    "[data-testid='stSidebar'] .st-key-logout button p{font-size:11.5px !important;"
    "color:#d6e5ff !important;font-weight:600 !important}"
    "</style>",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Notifikasi
# ---------------------------------------------------------------------------
def daftar_notif(nama: str):
    mapa = st.session_state.setdefault("notif", {})
    clave = next((k for k in mapa if str(k).casefold() == str(nama).casefold()), nama)
    return mapa.setdefault(clave, [])


def tambah_notif(nama: str, kunci: str, teks: str, menu: str = "Dashboard"):
    dilihat = st.session_state.setdefault("notif_dilihat", {}).setdefault(nama, set())
    daftar = daftar_notif(nama)
    if kunci in dilihat or any(n.get("event_key") == kunci for n in daftar):
        return False
    dilihat.add(kunci)
    seq = st.session_state.get("notif_seq", 0) + 1
    st.session_state["notif_seq"] = seq
    daftar.insert(0, {
        "id": f"n{seq}",
        "event_key": kunci,
        "teks": teks,
        "waktu": datetime.now(ZoneInfo("Asia/Jakarta")).strftime("%d/%m/%Y %H:%M:%S WIB"),
        "dibaca": False,
        "menu": menu,
    })
    return True


def perbarui_notifikasi(nama: str, peran: str):
    berubah = False
    data = st.session_state.data
    hasil = data.get("hasil", [])
    if peran == "Pengelola":
        nama_pengelola = {rapikan_nama(n) for n in PENGELOLA}
        for i, h in enumerate(hasil):
            siswa = str(h.get("siswa") or "")
            if siswa in nama_pengelola:
                continue
            jenis = {"game": "Game", "materi": "Materi"}.get(h.get("tipe"), "Ujian")
            berubah |= tambah_notif(
                nama,
                f"aktivitas:{i}:{siswa}:{h.get('tanggal')}:{h.get('skor')}",
                f"🧑‍🎓 <b>{opsi_aman(siswa)}</b> selesai {jenis} "
                f"{opsi_aman(str(h.get('mode')))} · Nilai <b>{h.get('skor')}</b>",
                menu=("Belajar & Game" if h.get("tipe") == "game" else
                      "Materi" if h.get("tipe") == "materi" else "Ujian"),
            )
        for siswa in st.session_state.get("login_baru", []):
            berubah |= tambah_notif(nama, f"login:{siswa}",
                                    f"🆕 Siswa baru login pertama kali: <b>{opsi_aman(siswa)}</b>")
    else:
        for i, h in enumerate(hasil):
            if h.get("siswa") != nama:
                continue
            jenis = {"game": "Game", "materi": "Materi"}.get(h.get("tipe"), "Ujian")
            berubah |= tambah_notif(
                nama,
                f"nilai:{i}:{h.get('tanggal')}:{h.get('skor')}",
                f"📊 Nilai kamu sudah keluar: {jenis} "
                f"{opsi_aman(str(h.get('mode')))} · Nilai <b>{h.get('skor')}</b>",
                menu=("Belajar & Game" if h.get("tipe") == "game" else
                      "Materi" if h.get("tipe") == "materi" else "Ujian"),
            )
        for p in st.session_state.get("pengumuman", []):
            berubah |= tambah_notif(nama, f"pengumuman:{p['id']}",
                                    f"📢 Pengumuman baru dari Pengelola: {opsi_aman(p['teks'])}")
        posisi = next((i + 1 for i, (n, _) in enumerate(papan_skor()) if n == nama), None)
        if posisi:
            terakhir = st.session_state.setdefault("peringkat_terakhir", {})
            lama = terakhir.get(nama)
            terakhir[nama] = posisi
            if lama and lama != posisi:
                berubah |= tambah_notif(nama, f"peringkat:{lama}:{posisi}:{len(hasil)}",
                                        f"🏆 Peringkat Leaderboard kamu berubah: "
                                        f"#{lama} → #{posisi}", menu="Leaderboard")
    if berubah:
        save_all_data()


def render_panel_notif(nama: str, peran: str):
    notifs = daftar_notif(nama)
    belum = sum(1 for n in notifs if not n.get("dibaca", False))
    judul = f"🔔 {belum} Notifikasi Baru" if belum else "🔔 Notifikasi"
    st.markdown(f'<div class="notif-title">{judul}</div>', unsafe_allow_html=True)
    if not notifs:
        st.caption("Belum ada notifikasi.")
    for n in list(notifs):
        kiri, kanan = st.columns([7, 1], vertical_alignment="center", gap="small")
        kelas = "notif-baru" if not n.get("dibaca", False) else "notif-lama"
        teks_html = str(n.get("teks") or "Aktivitas baru")
        with kiri:
            st.markdown(
                f'<div class="notif-item {kelas}"><span class="notif-titik"></span>'
                f'<div>{teks_html}<div class="notif-waktu">{html.escape(str(n.get("waktu") or ""))}</div></div></div>',
                unsafe_allow_html=True,
            )
            teks_tombol = re.sub(r"<[^>]*>", "", html.unescape(teks_html))
            teks_tombol = re.sub(r"\s+", " ", teks_tombol).strip()
            if st.button(
                "Buka: " + (teks_tombol[:95] + ("…" if len(teks_tombol) > 95 else "")),
                key=f"buka_notif_{nama}_{n.get('id')}",
                use_container_width=True,
            ):
                n["dibaca"] = True
                tujuan = str(n.get("menu") or "Dashboard")
                menu_valid = {
                    "Dashboard", "Belajar & Game", "Ujian", "Nilai & Hasil",
                    "Leaderboard", "Materi", "Al-Qur'an (Juz 30)", "Data Siswa",
                    "AI Assistant", "Pengaturan", "Pengaturan Aplikasi",
                }
                st.session_state.menu = tujuan if tujuan in menu_valid else "Dashboard"
                if n.get("mode") in MODE_LIST:
                    st.session_state.mode = n["mode"]
                    st.session_state.mini_mode = n["mode"]
                save_all_data()
                st.rerun()
        with kanan:
            if st.button("🗑️", key=f"hapus_notif_{nama}_{n.get('id')}", help="Hapus notifikasi"):
                notifs.remove(n)
                save_all_data()
                st.rerun()
    if st.button("✅ Tandai Semua Sudah Dibaca", use_container_width=True,
                 disabled=belum == 0, key=f"baca_semua_{nama}"):
        for n in notifs:
            n["dibaca"] = True
        save_all_data()
        st.rerun()
    if peran == "Pengelola" and aku_super_admin():
        with st.expander("📢 Buat Pengumuman"):
            isi = st.text_input("Isi pengumuman", key=f"pengumuman_isi_{nama}")
            if st.button("Kirim Pengumuman", type="primary", key=f"kirim_pengumuman_{nama}"):
                if isi.strip():
                    pengumuman_id = f"p{int(datetime.now(ZoneInfo('Asia/Jakarta')).timestamp() * 1000)}"
                    st.session_state.setdefault("pengumuman", []).insert(0, {
                        "id": pengumuman_id,
                        "teks": isi.strip(),
                    })
                    _qori_tambah_notif_admin(
                        f"📣 Pengelola membuat pengumuman: <b>{html.escape(isi.strip())}</b>",
                        menu="Dashboard",
                        event_key=f"pengumuman-admin:{pengumuman_id}",
                    )
                    save_all_data()
                    st.rerun()
                else:
                    st.warning("Isi pengumuman tidak boleh kosong.")


# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
profil = st.session_state.data["profil"]
nama_tampil = st.session_state.user_name or profil["nama"]
peran_tampil = st.session_state.user_role or profil["peran"]
if peran_tampil == "Pengelola":
    _lvl_tampil = level_pengelola()
    if _lvl_tampil == "super_admin":
        peran_chip = "👑 Pengelola 1 · Super Admin"
    elif _lvl_tampil == "pengelola_2":
        peran_chip = "🛡️ Pengelola 2 · Admin Terbatas"
    else:
        peran_chip = peran_tampil
else:
    peran_chip = peran_tampil
foto_per_user = st.session_state.setdefault("foto_profil", {})
foto_aktif = foto_per_user.get(nama_tampil)
perbarui_notifikasi(nama_tampil, peran_tampil)
notif_belum = sum(1 for n in daftar_notif(nama_tampil) if not n["dibaca"])

st.markdown(
    "<style>"
    ".st-key-topbar_kiri .topbar{margin:0 2px;height:56px;display:flex;flex-direction:column;"
    "justify-content:center;align-items:flex-start;}"
    ".st-key-topbar_kanan{height:56px;min-height:56px !important;}"
    ".st-key-notif_bell{display:flex;justify-content:flex-end;}"
    ".st-key-notif_bell [data-testid='stPopover'] button{width:40px;min-height:40px;height:40px;"
    "padding:0;border-radius:50%;background:#fff;border:1px solid #e3ebf7;"
    "box-shadow:0 4px 12px #163c7012;position:relative;display:flex;align-items:center;"
    "justify-content:center;}"
    ".st-key-notif_bell [data-testid='stPopover'] button:hover{border-color:#cfe3ff;}"
    ".st-key-notif_bell [data-testid='stPopover'] button p{font-size:18px !important;"
    "line-height:1;}"
    ".notif-title{font-size:15px;font-weight:800;color:#0f2549;margin:2px 0 8px;}"
    ".notif-item{display:flex;gap:8px;padding:7px 9px;border-radius:10px;font-size:12.5px;"
    "line-height:1.45;color:#22314d;background:#f7faff;border:1px solid #e8f0fb;"
    "margin-bottom:6px;}"
    ".notif-item.notif-baru{background:#eef6ff;border-color:#cfe4ff;}"
    ".notif-titik{width:8px;height:8px;border-radius:50%;background:#c6d3e8;margin-top:5px;"
    "flex:none;}"
    ".notif-item.notif-baru .notif-titik{background:#1f6feb;}"
    ".notif-waktu{font-size:10.5px;color:#7a8cab;margin-top:2px;}"
    ".st-key-topbar_kanan{flex-wrap:nowrap !important;justify-content:flex-end !important;"
    "align-items:center !important;gap:10px !important;}"
    ".st-key-topbar_kanan > div{flex:0 0 auto !important;width:auto !important;"
    "min-width:0 !important;}"
    ".st-key-topbar_kanan .st-key-notif_bell,.st-key-topbar_kanan .st-key-user_chip{"
    "display:flex !important;align-items:center !important;flex:none !important;width:auto !important;}"
    ".st-key-topbar_kanan .st-key-user_chip [data-testid='stVerticalBlock']{gap:0 !important;}"
    ".st-key-user_chip [data-testid='stPopover'] button{width:40px;min-height:40px;height:40px;"
    "padding:0;border-radius:50%;border:2px solid #fff;"
    "background:linear-gradient(135deg,#5aa9f5,#0b4fa8);box-shadow:0 4px 12px #163c7012;"
    "display:flex;align-items:center;justify-content:center;}"
    ".st-key-user_chip [data-testid='stPopover'] button:hover{border-color:#cfe3ff;"
    "filter:brightness(1.05);}"
    ".st-key-user_chip [data-testid='stPopover'] button p{font-size:18px !important;"
    "line-height:1;color:#fff !important;}"
    ".st-key-topbar_kanan [data-testid='stMarkdownContainer']{margin-bottom:0 !important;}"
    ".chip-role{font-size:14px;font-weight:600;color:#173a6b;white-space:nowrap;"
    "margin:0;line-height:40px;display:flex;align-items:center;height:40px;}"
    ".chip-role .chev{font-size:11px;color:#5d7194;margin-left:6px;}"
    ".foto-menu-title{font-size:15px;font-weight:700;color:#0f2549;margin-bottom:4px;}"
    ".dash-greet{display:flex;align-items:center;gap:12px;}"
    "/* Header di HP: lonceng & profil pindah ke atas, sapaan ke bawah (tidak numpuk) */"
    "@media (max-width:768px){"
    "[data-testid='stHorizontalBlock']:has(.st-key-topbar_kiri){flex-direction:column !important;"
    "align-items:stretch !important;gap:4px !important;}"
    "[data-testid='stHorizontalBlock']:has(.st-key-topbar_kiri) "
    ">[data-testid='stColumn']{width:100% !important;flex:1 1 100% !important;"
    "max-width:100% !important;}"
    "[data-testid='stHorizontalBlock']:has(.st-key-topbar_kiri) "
    ">[data-testid='stColumn']:has(.st-key-topbar_kanan){order:-1 !important;}"
    ".st-key-topbar_kiri{height:auto !important;min-height:0 !important;}"
    ".st-key-topbar_kiri .topbar{height:auto !important;min-height:0 !important;"
    "justify-content:flex-start !important;margin:0 !important;}"
    ".st-key-topbar_kanan{height:auto !important;min-height:0 !important;"
    "flex-wrap:wrap !important;row-gap:6px !important;}"
    "}"
    "</style>",
    unsafe_allow_html=True,
)
if foto_aktif:
    st.markdown(
        "<style>"
        ".st-key-user_chip [data-testid='stPopover'] button{"
        f"background:#0b4fa8 url('{foto_data_uri(foto_aktif)}') center/cover no-repeat !important;"
        "}"
        ".st-key-user_chip [data-testid='stPopover'] button p{display:none !important;}"
        "</style>",
        unsafe_allow_html=True,
    )

# CSS paksa (menimpa gaya bawaan Streamlit): background abu-abu muda & tanpa jarak putih.
st.markdown(
    "<style>"
    "[data-testid='stAppViewContainer']{background-color:#E9EDF2 !important;}"
    "[data-testid='stAppViewBlockContainer']{background-color:#E9EDF2 !important;}"
    "header[data-testid='stHeader']{background:transparent !important;height:auto !important;"
    "pointer-events:none !important;}"
    "[data-testid='stToolbar']{background:transparent !important;pointer-events:none !important;}"
    ".main{background-color:#E9EDF2 !important;}"
    ".block-container,[data-testid='stMainBlockContainer']{"
    "padding-top:14px !important;padding-bottom:0 !important;"
    "padding-left:1.2rem !important;padding-right:1.2rem !important;"
    "max-width:100% !important;margin-top:0 !important;background-color:#E9EDF2 !important;}"
    "div[data-testid='stVerticalBlock'] > div{background-color:transparent;}"
    "html,body,[data-testid='stApp'],[data-testid='stMain']{background:#E9EDF2 !important;}"
    "[data-testid='stElementContainer']:has(style){display:none !important;"
    "height:0 !important;min-height:0 !important;padding:0 !important;margin:0 !important;}"
    ".topbar h1{margin-top:0 !important;padding-top:0 !important;}"
    ".st-key-panel_board,.st-key-panel_fitur{background:#fff !important;}"
    "</style>",
    unsafe_allow_html=True,
)
if notif_belum:
    lencana = str(notif_belum) if notif_belum < 10 else "9+"
    st.markdown(
        "<style>"
        ".st-key-notif_bell [data-testid='stPopover'] button::after{"
        f"content:'{lencana}';position:absolute;top:-3px;right:-3px;min-width:18px;height:18px;"
        "border-radius:9px;background:#ef4444;color:#fff;font-size:10.5px;font-weight:700;"
        "display:flex;align-items:center;justify-content:center;border:2px solid #fff;"
        "padding:0 3px;}"
        "</style>",
        unsafe_allow_html=True,
    )

menu = st.session_state.menu

# Catat kunjungan menu siswa hanya saat benar-benar berpindah menu/mode,
# bukan pada setiap rerun Streamlit.
if st.session_state.get("user_role") == "Siswa":
    mode_kunjungan = (st.session_state.get("mode") or "") if menu == "Belajar & Game" else ""
    tanda_menu = (str(menu), str(mode_kunjungan))
    if tanda_menu != st.session_state.get("_qori_last_activity_menu"):
        label_menu = str(menu)
        if mode_kunjungan:
            label_menu += f" · Mode {mode_kunjungan}"
        _qori_catat_aktivitas_siswa(
            f"membuka menu <b>{html.escape(label_menu)}</b>.",
            menu=("Belajar & Game" if menu == "Belajar & Game" else menu),
            mode=mode_kunjungan,
            event_key=f"menu:{st.session_state.get('user_name')}:{label_menu}:{datetime.now(ZoneInfo('Asia/Jakarta')).strftime('%Y%m%d%H%M%S%f')}",
        )
        st.session_state["_qori_last_activity_menu"] = tanda_menu

# Header hanya tampil di Dashboard.
if menu == "Dashboard":
    tb_kiri, tb_kanan = st.columns([5.6, 2.1], vertical_alignment="center", gap="small")
    with tb_kiri, st.container(key="topbar_kiri"):
        sapaan = T("Selamat Datang", "Welcome", "أهلاً وسهلاً")
        subjudul_dash = T(
            "Di QORI AI – Media Pembelajaran Al-Qur'an Berbasis Artificial Intelligence",
            "At QORI AI – AI-Based Qur'an Learning Media",
            "في QORI AI – وسائط تعلم القرآن بالذكاء الاصطناعي")
        st.markdown(
            '<div class="topbar"><div class="dash-greet"><div>'
            f'<h1>{sapaan}, {opsi_aman(nama_tampil)} 👋</h1>'
            f"<p>{subjudul_dash}</p>"
            '</div></div></div>',
            unsafe_allow_html=True,
        )
    with tb_kanan, st.container(key="topbar_kanan", horizontal=True,
                                vertical_alignment="center", gap="small"):
        with st.container(key="notif_bell"):
            with st.popover("🔔"):
                render_panel_notif(nama_tampil, peran_tampil)
        with st.container(key="user_chip"):
            with st.popover("👤"):
                st.markdown('<div class="foto-menu-title">👤 Foto Profil</div>',
                            unsafe_allow_html=True)
                if foto_aktif:
                    st.image(foto_aktif["data"], width=132)
                else:
                    st.caption("Belum ada foto profil. Silakan upload foto JPG/PNG.")
                unggah = st.file_uploader(
                    "Upload Foto Profil (JPG/PNG)", type=["jpg", "jpeg", "png"],
                    key=f"foto_upload_{nama_tampil}",
                )
                b1, b2 = st.columns(2)
                if b1.button("💾 Ganti Foto", type="primary", use_container_width=True,
                             disabled=unggah is None, key=f"foto_simpan_{nama_tampil}"):
                    foto_baru = _kompres_foto_upload(unggah)
                    foto_per_user[nama_tampil] = {
                        "data": foto_baru["data"], "mime": foto_baru["mime"],
                    }
                    kunci_header_foto = (
                        "foto_profil_pengelola" if peran_tampil == "Pengelola"
                        else f"foto_profil_siswa_{_foto_id_siswa(nama=nama_tampil)}")
                    foto_ok, foto_err = _simpan_foto_profil_permanen(
                        kunci_header_foto, foto_baru,
                        untuk_siswa=(peran_tampil == "Siswa"))
                    save_all_data()
                    if not foto_ok:
                        st.session_state["_foto_save_warning"] = foto_err
                    st.rerun()
                if b2.button("🗑️ Hapus Foto", use_container_width=True,
                             disabled=foto_aktif is None, key=f"foto_hapus_{nama_tampil}"):
                    foto_per_user.pop(nama_tampil, None)
                    _hapus_berkas_foto(nama_tampil)
                    save_all_data()
                    st.rerun()
        st.markdown(
            f'<div class="chip-role">{opsi_aman(peran_chip)}<span class="chev">▾</span></div>',
            unsafe_allow_html=True,
        )

# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------
def _dash_nama_kelas():
    return {rapikan_nama(str(d["nama"])).casefold() for d in LB_SISWA}


def _dash_hasil_kelas():
    nama = _dash_nama_kelas()
    return [h for h in st.session_state.data.get("hasil", []) or []
            if rapikan_nama(str(h.get("siswa") or "")).casefold() in nama]


def _dash_progress_kelas():
    nama = _dash_nama_kelas()
    level = {m: 0 for m in MODE_LIST}
    ref = {str(m["id"]): m for m in _semua_materi()}
    kur = _baca_json(KURIKULUM_FILE, {})
    for pemilik, ids in (kur.get("selesai") or {}).items():
        if rapikan_nama(str(pemilik)).casefold() not in nama:
            continue
        for mid in ids or []:
            mat = ref.get(str(mid))
            if not mat:
                continue
            mode = _mode_dari_kategori(str(mat.get("kategori") or ""))
            if mode not in level:
                continue
            try:
                level[mode] = max(level[mode], int(mat.get("lv") or 0))
            except (TypeError, ValueError):
                continue
    for h in _dash_hasil_kelas():
        if str(h.get("tipe")) != "materi":
            continue
        mode = _mode_dari_kategori(str(h.get("mode") or ""))
        if mode not in level:
            continue
        try:
            level[mode] = max(level[mode], int(h.get("level") or 0))
        except (TypeError, ValueError):
            continue
    return {m: max(0, min(MAX_LEVEL, lv)) for m, lv in level.items()}


def _dash_top_contoh(jumlah=3):
    return sorted(LB_SISWA, key=lambda d: -int(d.get("xp") or 0))[:jumlah]


def page_dashboard():
    data = st.session_state.data
    if (pesan := st.session_state.pop("dash_info", None)):
        st.success(pesan)
    pengelola = st.session_state.get("user_role") == "Pengelola"
    contoh_mode = _contoh_aktif()
    mode_teks = (T("Contoh", "Sample", "تجريبي") if contoh_mode
                 else T("Asli", "Real", "حقيقي"))
    banner_mode = (T(" · Mode: ", " · Mode: ", " · الوضع: ") + mode_teks
                   if pengelola else "")
    st.markdown(
        '<div style="border-radius:12px;padding:10px 16px;margin:0 0 12px;font-weight:800;'
        'font-size:13.5px;background:rgba(22,119,232,.10);border:1px solid rgba(22,119,232,.28);">'
        '📍 ' + T("Kelas 11 · 20 Siswa", "Class 11 · 20 Students",
                  "الفصل 11 · 20 طالبًا") + banner_mode + "</div>",
        unsafe_allow_html=True)

    if pengelola and not aku_super_admin():
        st.markdown(
            '<div style="border-radius:14px;padding:14px 18px;margin:0 0 14px;'
            'background:#fff7e6;border:2px solid #f0b400;color:#5c4400;font-weight:700;'
            'font-size:14px;line-height:1.55;">🛡️ '
            + T("Anda login sebagai Pengelola 2. Anda hanya bisa melihat data. Untuk "
                "mengubah data, minta izin ke Pengelola 1 (Kendar Sultoni).",
                "You are logged in as Manager 2. You can only view data. To change data, "
                "ask Manager 1 (Kendar Sultoni) for permission.",
                "أنت مسجل كمدير 2. يمكنك عرض البيانات فقط. لتغيير البيانات، اطلب الإذن من "
                "المدير 1 (Kendar Sultoni).")
            + '</div>', unsafe_allow_html=True)
        form_minta_izin("dashboard")

    hasil_kelas = _dash_hasil_kelas()
    game = [h for h in hasil_kelas if str(h.get("tipe")) == "game"]
    ujian = [h for h in hasil_kelas if str(h.get("tipe")) in ("ujian", "exam")]
    skor_semua = [int(h.get("skor") or 0) for h in hasil_kelas]
    rata = round(sum(skor_semua) / len(skor_semua)) if skor_semua else None
    tuntas = (round(sum(1 for s in skor_semua if s >= BATAS_TUNTAS) / len(skor_semua) * 100)
              if skor_semua else 0)
    hari_ini = datetime.now().date()
    aktif = len({rapikan_nama(str(h.get("siswa") or "")).casefold()
                 for h in hasil_kelas
                 if (_lb_parse_tanggal(h.get("tanggal")) or datetime.min).date() == hari_ini})

    hero_sub = T("Belajar Al-Qur'an Lebih Mudah, Interaktif,<br>dan Menyenangkan dengan AI",
                 "Learn the Qur'an Easier, Interactive,<br>and Fun with AI",
                 "تعلّم القرآن بسهولة وتفاعل<br>ومتعة مع الذكاء الاصطناعي")
    chip_iqro = T("Mengenal Huruf", "Recognize Letters", "تعلم الحروف")
    chip_tahsin = T("Memperbaiki Bacaan", "Improve Recitation", "تحسين التلاوة")
    chip_tahfidz = T("Menghafal Al-Qur'an", "Memorize the Qur'an", "حفظ القرآن")
    st.markdown(
        '<div class="hero"><div class="hero-content">'
        '<div class="hero-title">QORI <span>AI</span></div>'
        f'<div class="hero-sub">{hero_sub}</div>'
        '<div class="hero-chips">'
        '<div class="hero-chip"><span class="ico" style="background:#f7b733">📗</span>'
        f"<div><b>Iqro'</b><small>{chip_iqro}</small></div></div>"
        '<div class="hero-chip"><span class="ico" style="background:#57d3c8">🎙️</span>'
        f'<div><b>Tahsin</b><small>{chip_tahsin}</small></div></div>'
        '<div class="hero-chip"><span class="ico" style="background:#b18cf5">📚</span>'
        f"<div><b>Tahfidz</b><small>{chip_tahfidz}</small></div></div>"
        '</div></div></div>',
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3, gap="small")
    kartu = [
        (c1, "iqro", "iqro", T("Mode Iqro'", "Iqro' Mode", "وضع إقرأ"),
         T("Belajar membaca Al-Qur'an dari dasar (Iqro' 1–6)",
           "Learn to read the Qur'an from basics (Iqro' 1–6)",
           "تعلم قراءة القرآن من الأساس (إقرأ ١–٦)"),
         T("🔰 Pemula hingga mahir", "🔰 Beginner to advanced", "🔰 من المبتدئ إلى المتقدم")),
        (c2, "tahsin", "tahsin", T("Mode Tahsin", "Tahsin Mode", "وضع التحسين"),
         T("Memperbaiki bacaan sesuai ilmu tajwid",
           "Improve recitation according to tajwid rules",
           "تحسين التلاوة وفق أحكام التجويد"),
         T("🎯 Bacaan lebih tartil", "🎯 More accurate recitation", "🎯 تلاوة أكثر ترتيلاً")),
        (c3, "tahfidz", "tahfidz", T("Mode Tahfidz", "Tahfidz Mode", "وضع التحفيظ"),
         T("Menghafal dan menjaga hafalan Al-Qur'an",
           "Memorize and retain the Qur'an",
           "حفظ القرآن ومراجعته"),
         T("🌙 Muraja'ah terarah", "🌙 Guided muraja'ah", "🌙 مراجعة موجهة")),
    ]
    for kolom, cls, slug, judul, teks, tag in kartu:
        with kolom, st.container(key=f"mode_{cls}"):
            st.markdown(
                f'<h3>{judul}</h3><p>{teks}</p>',
                unsafe_allow_html=True,
            )
            if st.button(T("Mulai Belajar →", "Start Learning →", "ابدأ التعلم ←"),
                         key=f"to_{slug}"):
                mode_nama = MODE_SLUGS[slug]
                if mode_terkunci(mode_nama):
                    st.session_state.menu = "Terkunci"
                    st.session_state.locked_mode = mode_nama
                    st.rerun()
                xp = st.session_state.data["progress"].get(mode_nama, {"xp": 0})["xp"]
                level = level_dari_xp(xp)[0]
                st.session_state.mode = mode_nama
                st.session_state.menu = "Belajar & Game"
                mulai_sesi("game", mode_nama, level)
                st.rerun()

    p1, p2, p3 = st.columns([1.05, 1.05, 1], gap="small")
    with p1:
        progres = _dash_progress_kelas()
        baris = []
        kata_level = T("Level", "Level", "المستوى")
        for mode in MODE_LIST:
            lvl = int(progres.get(mode, 0) or 0)
            pct = round(lvl / MAX_LEVEL * 100) if MAX_LEVEL else 0
            warna = MODE_COLOR[mode] if pct > 0 else "#c3ced9"
            gaya_pct = ' style="color:#9aa7b8"' if pct == 0 else ""
            baris.append(
                f'<div class="p-row"><div class="p-ico" style="background:{MODE_COLOR[mode]}">'
                f'{MODE_ICON[mode]}</div>'
                f'<div class="p-body"><div class="p-top"><span>{mode}'
                f'<em class="lvl">{kata_level} {lvl} / {MAX_LEVEL}</em></span>'
                f'<span class="pct"{gaya_pct}>{pct}%</span></div>'
                f'<div class="track"><div class="fill" style="width:{pct}%;'
                f'background:{warna}"></div></div></div></div>'
            )
        st.markdown(
            '<div class="panel"><div class="panel-head"><h3>'
            + T("📊 Progress Belajar Kelas 11", "📊 Class 11 Learning Progress",
                "📊 تقدم الفصل 11 في التعلم")
            + '</h3></div>' + "".join(baris)
            + '<div style="font-size:11.5px;color:#8a97ab;margin-top:6px;line-height:1.5">'
            + T("Data akan bertambah otomatis setelah siswa menyelesaikan materi / game / ujian.",
                "Data updates automatically after students finish materials / games / exams.",
                "تتحدث البيانات تلقائيًا بعد إنهاء الطلاب للمواد / الألعاب / الاختبارات.")
            + '</div></div>',
            unsafe_allow_html=True,
        )
    with p2:
        kali = T("kali", "times", "مرات")
        rata_html = (str(rata) if rata is not None else
                     "-<small>" + T("Belum ada nilai", "No scores yet", "لا توجد درجات") + "</small>")
        kotak = [
            ("🎮", T("Game", "Games", "الألعاب"), f"{len(game)}<small>{kali}</small>", "#eaf8f1"),
            ("📝", T("Ujian", "Exam", "اختبار"), f"{len(ujian)}<small>{kali}</small>", "#ebf3ff"),
            ("🏆", T("Rata-rata Nilai", "Average Score", "متوسط الدرجات"), rata_html, "#fdf6e6"),
            ("✅", T("Ketuntasan", "Mastery", "الإتمام"), f"{tuntas}%", "#eaf8f1"),
            ("👥", T("Total Siswa Kelas 11", "Total Class 11 Students", "إجمالي طلاب الفصل 11"),
             f"{len(LB_SISWA)}<small>" + T("siswa", "students", "طالبًا") + "</small>", "#f2ecff"),
            ("🟢", T("Siswa Aktif Hari Ini", "Active Students Today", "الطلاب النشطون اليوم"),
             f"{aktif}<small>" + T("dari", "of", "من") + f" {len(LB_SISWA)}</small>", "#e8f6ff"),
        ]
        stat_html = "".join(
            f'<div class="stat" style="background:{bg}"><div class="stat-ico">{ico}</div>'
            f'<span>{label}</span><strong>{nilai}</strong></div>'
            for ico, label, nilai, bg in kotak
        )
        catatan_stat = ("" if hasil_kelas else
                        '<div style="font-size:11.5px;color:#8a97ab;margin-top:8px">'
                        + T("Belum ada aktivitas asli - mulai belajar dulu.",
                            "No real activity yet - start learning first.",
                            "لا يوجد نشاط حقيقي بعد - ابدأ التعلم أولًا.")
                        + '</div>')
        st.markdown(
            '<div class="panel"><div class="panel-head"><h3>'
            + T("📋 Statistik Aktivitas", "📋 Activity Statistics", "📋 إحصاءات النشاط")
            + '</h3></div>'
            f'<div class="stat-grid">{stat_html}</div>' + catatan_stat + '</div>',
            unsafe_allow_html=True,
        )
    with p3:
        ava = [
            "linear-gradient(135deg,#f6ad55,#dd6b20)",
            "linear-gradient(135deg,#63b3ed,#2b6cb0)",
            "linear-gradient(135deg,#68d391,#2f855a)",
            "linear-gradient(135deg,#b794f4,#6b46c1)",
            "linear-gradient(135deg,#f687b3,#b83280)",
        ]
        rows = []
        if contoh_mode:
            daftar_board = [(d["nama"], None) for d in _dash_top_contoh(3)]
        else:
            nama_kelas = _dash_nama_kelas()
            skor_game = {}
            for h in hasil_kelas:
                if str(h.get("tipe")) != "game":
                    continue
                nama_h = str(h.get("siswa") or "").strip()
                if rapikan_nama(nama_h).casefold() not in nama_kelas:
                    continue
                skor_game[nama_h] = max(skor_game.get(nama_h, 0), int(h.get("skor") or 0))
            daftar_board = sorted(skor_game.items(), key=lambda kv: (-kv[1], kv[0]))[:5]
        for i, (nama, skor) in enumerate(daftar_board):
            cls = " me" if nama == profil["nama"] else ""
            inisial = "".join(w[0] for w in nama.split()[:2]).upper()
            ava_html = (f'<span class="rank-ava" '
                        f'style="background:{ava[i % len(ava)]}">{inisial}</span>')
            nilai_kanan = (f'<span class="rank-score">{skor}</span>' if skor is not None
                           else '<span class="rank-score" style="font-size:10.5px;color:#9aa7b8">'
                                + T("Contoh", "Sample", "عينة") + '</span>')
            rows.append(
                f'<div class="rank{cls}"><span class="rank-badge r{i + 1}">{i + 1}</span>'
                f'{ava_html}'
                f'<span class="rank-name">{opsi_aman(nama)}</span>'
                f'{nilai_kanan}</div>'
            )
        rows_html = "".join(rows) or (
            '<div class="rank">'
            + T("Belum ada data - Siswa belum main game.",
                "No data yet - Students have not played games.",
                "لا توجد بيانات بعد - لم يلعب الطلاب الألعاب.")
            + '</div>')
        with st.container(key="panel_board"):
            h1, h2 = st.columns([1.6, 1])
            h1.markdown(
                '<div class="panel-head" style="margin-bottom:8px"><h3>'
                + T("🏆 Leaderboard (Game)", "🏆 Leaderboard (Games)",
                    "🏆 لوحة المتصدرين (الألعاب)")
                + '</h3></div>',
                unsafe_allow_html=True,
            )
            with h2:
                if st.button(T("Lihat Semua →", "See All →", "عرض الكل ←"),
                             key="lihat_semua"):
                    st.session_state.menu = "Leaderboard"
                    st.rerun()
            if pengelola:
                t1, t2 = st.columns(2)
                if t1.button(T("Mode Contoh", "Sample Mode", "الوضع التجريبي"),
                             key="dash_mode_contoh", use_container_width=True,
                             type="primary" if contoh_mode else "secondary",
                             disabled=contoh_mode or not _boleh_ubah()):
                    st.session_state["mode_pengelola"] = "Contoh"
                    st.session_state["nilai_mode"] = "contoh"
                    save_all_data()
                    st.rerun()
                if t2.button(T("Mode Asli", "Real Mode", "الوضع الحقيقي"),
                             key="dash_mode_asli", use_container_width=True,
                             type="primary" if not contoh_mode else "secondary",
                             disabled=not contoh_mode or not _boleh_ubah()):
                    st.session_state["mode_pengelola"] = "Asli"
                    st.session_state["nilai_mode"] = "asli"
                    save_all_data()
                    st.rerun()
            st.markdown(rows_html, unsafe_allow_html=True)
            if contoh_mode:
                st.caption(T("DATA CONTOH - Klik Mode Asli untuk melihat data asli (kosong).",
                             "SAMPLE DATA - Click Real Mode to see real data (empty).",
                             "بيانات تجريبية - اضغط الوضع الحقيقي لعرض البيانات الحقيقية (فارغة)."))

    f1, f2 = st.columns([1.75, 1], gap="small")
    with f1, st.container(key="panel_fitur"):
        st.markdown(
            '<div class="panel-head"><h3>'
            + T("🌟 Fitur Unggulan QORI AI", "🌟 QORI AI Key Features",
                "🌟 ميزات QORI AI البارزة")
            + '</h3></div>',
            unsafe_allow_html=True)
        kolom_fitur = st.columns(5, gap="small")
        fitur = [
            ("game", T("Game Interaktif", "Interactive Games", "ألعاب تفاعلية")),
            ("ujian", T("Ujian Online", "Online Exam", "اختبار إلكتروني")),
            ("nilai", T("Analisis Nilai", "Score Analysis", "تحليل الدرجات")),
            ("quran", T("Al-Qur'an Digital", "Digital Qur'an", "القرآن الرقمي")),
            ("ai", "AI Assistant"),
        ]
        for kolom, (slug, judul) in zip(kolom_fitur, fitur):
            with kolom:
                if st.button(judul, key=f"fitur_btn_{slug}", use_container_width=True):
                    if slug == "game":
                        mode_awal = (kelas_siswa()
                                     or st.session_state.get("mode", MODE_LIST[0]))
                        if mode_awal not in MODE_LIST:
                            mode_awal = MODE_LIST[0]
                        st.session_state.mode = mode_awal
                        st.session_state.mini_mode = mode_awal
                        st.session_state.menu = "Belajar & Game"
                    elif slug == "ujian":
                        st.session_state.menu = "Ujian"
                    elif slug == "nilai":
                        st.session_state.menu = "Nilai & Hasil"
                    elif slug == "quran":
                        st.session_state.menu = "Al-Qur'an (Juz 30)"
                    else:
                        st.session_state.menu = "AI Assistant"
                    st.session_state.pop("quiz", None)
                    st.rerun()
    with f2:
        terbaru = sorted(hasil_kelas,
                         key=lambda h: _lb_parse_tanggal(h.get("tanggal")) or datetime.min,
                         reverse=True)[:5]
        aktivitas = []
        for h in terbaru:
            jenis = {"game": T("Game", "Game", "لعبة"),
                     "materi": T("Materi", "Material", "مادة")}.get(
                         h["tipe"], T("Ujian", "Exam", "اختبار"))
            aktivitas.append(
                '<div class="act"><span class="act-check">✓</span>'
                f'<div class="act-body"><b>{opsi_aman(str(h.get("siswa") or "-"))}</b> · '
                + T("Selesai", "Completed", "أكملت") + f' {jenis} {opsi_aman(str(h.get("mode") or ""))} '
                + T("(Level", "(Level", "(المستوى") + f' {h.get("level")})'
                + T(" – Nilai", " – Score", " – الدرجة")
                + f' {h.get("skor")}</div>'
                f'<span class="act-time">{waktu_aktivitas(h.get("tanggal"))}</span></div>'
            )
        if terbaru:
            isi_akt = "".join(aktivitas)
        elif contoh_mode:
            contoh_rows = []
            for d in _dash_top_contoh(3):
                contoh_rows.append(
                    '<div class="act"><span class="act-check">✓</span>'
                    f'<div class="act-body"><b>{opsi_aman(d["nama"])}</b> · '
                    + T("Selesai Game", "Finished Game", "أكمل لعبة") + f' {opsi_aman(d["kategori"])}'
                    + T(" – Nilai", " – Score", " – الدرجة") + f' {int(d["nilai"])}</div>'
                    '<span class="act-time">' + T("Contoh", "Sample", "عينة") + '</span></div>'
                )
            isi_akt = ('<div style="font-size:12px;color:#8a6d1c;background:#fff4cc;'
                       'border:1px solid #f0d488;border-radius:10px;padding:8px 10px;'
                       'margin-bottom:8px;line-height:1.5">'
                       + T("Belum ada aktivitas asli. 3 aktivitas terakhir dalam Mode Contoh:",
                           "No real activity yet. The last 3 activities in Sample Mode:",
                           "لا يوجد نشاط حقيقي بعد. آخر 3 أنشطة في الوضع التجريبي:")
                       + '</div>') + "".join(contoh_rows)
        else:
            isi_akt = ('<div class="act">'
                       + T("Belum ada aktivitas asli - Mulai belajar dulu.",
                           "No real activity yet - Start learning first.",
                           "لا يوجد نشاط حقيقي بعد - ابدأ التعلم أولًا.")
                       + '</div>')
        st.markdown(
            '<div class="panel"><div class="panel-head"><h3>'
            + T("🕒 Aktivitas Terbaru", "🕒 Recent Activity", "🕒 النشاط الأخير")
            + '</h3></div>' + isi_akt + '</div>',
            unsafe_allow_html=True,
        )
        if not terbaru and contoh_mode:
            if aku_super_admin() and st.button("🗑️ " + T("Hapus Data Contoh", "Delete Sample Data",
                                    "حذف البيانات التجريبية"),
                         key="dash_hapus_contoh", use_container_width=True):
                _hapus_data_contoh()
                st.session_state["dash_info"] = T(
                    "Data contoh sudah dihapus. Dashboard sekarang memakai Mode Asli.",
                    "Sample data deleted. The Dashboard now uses Real Mode.",
                    "تم حذف البيانات التجريبية. تستخدم لوحة التحكم الآن الوضع الحقيقي.")
                st.rerun()
        elif not terbaru:
            if st.button("▶ " + T("Mulai Belajar", "Start Learning", "ابدأ التعلم"),
                         key="dash_mulai_belajar", use_container_width=True, type="primary"):
                mode_awal = (kelas_siswa() or st.session_state.get("mode", MODE_LIST[0]))
                if mode_awal not in MODE_LIST:
                    mode_awal = MODE_LIST[0]
                st.session_state.mode = mode_awal
                st.session_state.mini_mode = mode_awal
                st.session_state.menu = "Belajar & Game"
                st.rerun()

# ---------------------------------------------------------------------------
# Mini game (port dari versi 1.7)
# ---------------------------------------------------------------------------
MINI_CSS = """<style>
.mini-glyph{font-size:96px;text-align:right;direction:rtl;background:#e9f5ff;border:1px solid #d8e9fb;
  border-radius:20px;padding:10px 18px;color:#0f3a6b;margin:4px 0 10px;line-height:1.3}
.mini-kata{font-size:32px;text-align:right;direction:rtl;background:#f6f9ff;border:1px solid #e1ebfa;
  border-radius:16px;padding:16px 20px;color:#102448;margin:4px 0 6px;line-height:1.8}
.mini-label{font-size:13px;font-weight:800;color:#0f2549;margin:10px 0 6px;text-align:right}
.mini-opsi{border-radius:12px;padding:12px 8px;text-align:center;font-weight:700;
  border:1px solid #e1ebfa;background:#f6f9ff;color:#102448;line-height:1.6}
.mini-opsi.arab{text-align:right;direction:rtl}
.mini-opsi.benar{background:#e3f8ec;border-color:#08a979;color:#07734f}
.mini-opsi.salah{background:#fdeaea;border-color:#e5484d;color:#a42328}
.mini-kartu{background:#eef4fd;border:1px solid #dbe7f7;border-radius:12px;padding:14px 6px;
  text-align:center;font-weight:700;color:#102448;line-height:1.5;min-height:58px}
.mini-kartu.arab{text-align:right;direction:rtl;padding:14px 12px}
.mini-kartu.buka{background:#fff;border-color:#bcd4f5}
.mini-kartu.cocok{background:#e3f8ec;border-color:#08a979;color:#07734f}
[class*="st-key-mini_pz_"] button p,[class*="st-key-mini_pzu_"] button p,
[class*="st-key-mini_ahopsi_"] button p,[class*="st-key-mini_pl_"] button p,
[class*="st-key-mini_tangkap_"] button p{direction:rtl;text-align:right}
[class*="st-key-mini_ahopsi_"] button [data-testid="stMarkdownContainer"]{width:100%}
</style>"""


def simpan_game_cepat(mode: str, skor: int, benar: int = 0,
                      total: int = MINI_RONDE, level: int = 1):
    data = st.session_state.data
    total = max(1, int(total))
    benar = max(0, min(total, int(benar)))
    persen = round(benar / total * 100)
    nama = data["profil"]["nama"]
    tanggal_hasil = datetime.now().strftime("%Y-%m-%d %H:%M")
    posisi_sebelum = next((i + 1 for i, (n, _) in enumerate(papan_skor()) if n == nama), None)
    data["hasil"].append({
        "siswa": data["profil"]["nama"],
        "tipe": "game",
        "mode": mode,
        "level": int(level),
        "benar": benar,
        "total": total,
        "skor": persen,
        "tanggal": tanggal_hasil,
    })
    progres = data["progress"].setdefault(mode, {"xp": 0})
    progres["xp"] += int(skor)
    data.setdefault("papan", {})
    data["papan"][nama] = max(data["papan"].get(nama, 0), persen)
    posisi_sesudah = next((i + 1 for i, (n, _) in enumerate(papan_skor()) if n == nama), None)
    if posisi_sebelum and posisi_sesudah and posisi_sesudah < posisi_sebelum:
        _qori_catat_aktivitas_siswa(
            f"naik peringkat Leaderboard dari #{posisi_sebelum} ke #{posisi_sesudah}.",
            menu="Leaderboard",
            event_key=f"rank-game:{nama}:{posisi_sebelum}:{posisi_sesudah}:{datetime.now(ZoneInfo('Asia/Jakarta')).strftime('%Y%m%d%H%M%S%f')}",
            persist=False,
        )
    save_all_data()
    simpan_hasil_game(nama, mode, int(level), benar, total, persen)
    if st.session_state.get("user_role") == "Siswa":
        _qori_catat_aktivitas_siswa(
            f"menyelesaikan game <b>{html.escape(str(mode))}</b> level {int(level)}, "
            f"nilai <b>{persen}</b>, memperoleh {int(skor)} poin.",
            menu="Nilai & Hasil",
            mode=mode,
            event_key=f"aktivitas:{len(data['hasil']) - 1}:{nama}:{tanggal_hasil}:{persen}",
        )


def mini_reset(mode: str, game: str):
    st.session_state.mini = {
        "mode": mode, "game": game, "idx": 0, "skor": 0, "nyawa": MINI_NYAWA,
        "lvl": 1, "benar": 0, "streak_benar": 0, "streak_salah": 0,
        "done": False, "flash": None, "sel": None, "order": [],
        "opsi": None, "opsi_round": -1,
        "langkah": [], "langkah_round": -1,
        "puzzle": [], "puzzle_order": [], "pz_round": -1,
        "jawab": None, "ah_round": -1, "ah_opsi": [],
        "mem_deck": [], "mem_open": [], "mem_found": [], "mem_check": False,
        "menang": False,
    }


def mini_level(gs) -> int:
    if gs.get("game") == "Memory Ayat":
        ditemukan = len(gs.get("mem_found", []))
        dasar = 1 if ditemukan < 4 else (2 if ditemukan < 6 else 3)
    else:
        dasar = 1 if gs["idx"] < 3 else (2 if gs["idx"] < 7 else 3)
    gs["lvl"] = max(gs.get("lvl", 1), dasar)
    return gs["lvl"]


def mini_benar(gs):
    lvl = mini_level(gs)
    poin = MINI_POIN[lvl]
    gs["skor"] += poin
    gs["benar"] = gs.get("benar", 0) + 1
    gs["streak_benar"] = gs.get("streak_benar", 0) + 1
    gs["streak_salah"] = 0
    naik = False
    if gs["streak_benar"] >= 2 and gs["lvl"] < 3:
        gs["lvl"] += 1
        gs["streak_benar"] = 0
        naik = True
    return poin, naik


def mini_salah(gs, pesan: str = ""):
    gs["nyawa"] -= 1
    gs["streak_salah"] = gs.get("streak_salah", 0) + 1
    gs["streak_benar"] = 0
    saran = ("Coba lagi, kamu pasti bisa!" if gs["streak_salah"] >= 2
             else "Ayo coba lagi!")
    gs["flash"] = ("no", "💛 " + saran + (" " + pesan if pesan else ""))


def mini_jawab(gs, benar: bool, pesan: str = ""):
    if benar:
        poin, naik = mini_benar(gs)
        gs["flash"] = ("ok", f"⭐ MasyaAllah hebat! +{poin} poin"
                       + (" · naik level!" if naik else ""))
    else:
        mini_salah(gs, pesan)
    gs["idx"] += 1
    if gs["idx"] >= MINI_RONDE or gs["nyawa"] <= 0:
        gs["done"] = True
        simpan_game_cepat(gs["mode"], gs["skor"], gs["benar"], MINI_RONDE,
                          gs.get("lvl", 1))
    st.rerun()


def _mini_selesai(gs):
    gs["done"] = True
    if gs.get("game") == "Memory Ayat":
        simpan_game_cepat(gs["mode"], gs["skor"],
                          len(gs.get("mem_found", [])) // 2,
                          len(MEMORY_AYAT), gs.get("lvl", 1))
    else:
        simpan_game_cepat(gs["mode"], gs["skor"], gs["benar"], MINI_RONDE,
                          gs.get("lvl", 1))


def render_puzzle_ayat(gs, i: int):
    lvl = mini_level(gs)
    daftar = PUZZLE_AYAT[lvl]
    target = daftar[i % len(daftar)]
    if gs["pz_round"] != i:
        gs["pz_round"] = i
        gs["puzzle"] = []
        gs["puzzle_order"] = list(range(len(target)))
        random.shuffle(gs["puzzle_order"])
    st.subheader("🧩 Susun potongan ayat dengan urutan yang benar")
    sisa = [k for k in gs["puzzle_order"] if k not in gs["puzzle"]]
    if sisa:
        st.markdown('<div class="mini-label">Potongan ayat:</div>', unsafe_allow_html=True)
        kolom = st.columns(len(sisa))
        for k, c in zip(reversed(sisa), kolom):
            if c.button(target[k], key=f"mini_pz_{i}_{k}", use_container_width=True):
                gs["puzzle"].append(k)
                st.rerun()
    st.markdown('<div class="mini-label">Susunanmu:</div>', unsafe_allow_html=True)
    kolom = st.columns(len(target))
    for pos, k in enumerate(gs["puzzle"]):
        # RTL: kata pertama yang diklik tampil di kolom paling kanan
        if kolom[len(target) - 1 - pos].button(
                f"{target[k]}  ✕", key=f"mini_pzu_{i}_{k}", use_container_width=True):
            gs["puzzle"].remove(k)
            st.rerun()
    if not gs["puzzle"]:
        st.info("Belum ada potongan. Klik potongan di atas untuk menyusun.")
    lengkap = len(gs["puzzle"]) == len(target)
    if st.button("✅ Periksa Ayat", key=f"mini_puzzle_check_{i}", type="primary",
                 disabled=not lengkap, use_container_width=True):
        if gs["puzzle"] == list(range(len(target))):
            poin, naik = mini_benar(gs)
            gs["flash"] = ("ok", f"⭐ MasyaAllah, susunan benar! +{poin} poin"
                           + (" · naik level!" if naik else ""))
            gs["idx"] += 1
            gs["pz_round"] = -1
            gs["puzzle"] = []
            if gs["idx"] >= MINI_RONDE:
                _mini_selesai(gs)
        else:
            mini_salah(gs, "Susunan belum tepat.")
            if gs["nyawa"] <= 0:
                _mini_selesai(gs)
        st.rerun()


def render_ayat_hilang(gs, i: int):
    lvl = mini_level(gs)
    daftar = AYAT_HILANG[lvl]
    kalimat, jawab, opsi_asli = daftar[i % len(daftar)]
    if gs["ah_round"] != i:
        gs["ah_round"] = i
        gs["jawab"] = None
        gs["ah_opsi"] = list(opsi_asli)
        random.shuffle(gs["ah_opsi"])
    opsi = gs["ah_opsi"]
    st.markdown(
        f'<div class="mini-kata arab">{opsi_aman(kalimat.replace("...", "_____"))}</div>',
        unsafe_allow_html=True)
    st.write("Pilih kata yang hilang untuk melengkapi ayat.")
    if gs["jawab"] is None:
        kolom = st.columns(len(opsi))
        for j, opt in enumerate(opsi):
            if kolom[j].button(opt, key=f"mini_ahopsi_{i}_{j}", use_container_width=True):
                gs["jawab"] = j
                if opt == jawab:
                    poin, naik = mini_benar(gs)
                    gs["flash"] = ("ok", f"✅ Benar! +{poin} poin"
                                   + (" · naik level!" if naik else ""))
                else:
                    mini_salah(gs, f"Jawaban: {jawab}")
                if gs["nyawa"] <= 0:
                    _mini_selesai(gs)
                st.rerun()
    else:
        kolom = st.columns(len(opsi))
        for j, opt in enumerate(opsi):
            ar = " arab" if ada_arab(opt) else ""
            if opt == jawab:
                cls = "mini-opsi benar" + ar
            elif j == gs["jawab"]:
                cls = "mini-opsi salah" + ar
            else:
                cls = "mini-opsi" + ar
            kolom[j].markdown(f'<div class="{cls}">{opsi_aman(opt)}</div>',
                              unsafe_allow_html=True)
        if st.button("Lanjut Ronde Berikutnya", key=f"mini_ahlanjut_{i}",
                     type="primary"):
            gs["idx"] += 1
            gs["ah_round"] = -1
            if gs["idx"] >= MINI_RONDE:
                _mini_selesai(gs)
            st.rerun()


def render_memory_ayat(gs):
    if not gs["mem_deck"]:
        kartu = [(pair, teks) for pair, (ar, art) in enumerate(MEMORY_AYAT)
                 for teks in (ar, art)]
        random.shuffle(kartu)
        gs["mem_deck"] = kartu
        gs["mem_open"] = []
        gs["mem_found"] = []
    st.subheader("🃏 Memory Ayat: pasangkan tulisan Arab dengan artinya")
    st.caption(f"Pasangan: {len(gs['mem_found']) // 2}/{len(MEMORY_AYAT)}")
    memeriksa = gs.get("mem_check", False)
    for baris in range(2):
        kolom = st.columns(4)
        for pos_kolom, c in enumerate(kolom):
            pos = baris * 4 + pos_kolom
            _, teks = gs["mem_deck"][pos]
            cocok = pos in gs["mem_found"]
            terbuka = pos in gs["mem_open"]
            if cocok or terbuka:
                ar = " arab" if ada_arab(teks) else ""
                cls = ("mini-kartu cocok" if cocok else "mini-kartu buka") + ar
                c.markdown(f'<div class="{cls}">{opsi_aman(teks)}</div>',
                           unsafe_allow_html=True)
            elif memeriksa:
                c.markdown('<div class="mini-kartu">❓</div>', unsafe_allow_html=True)
            elif c.button("❓ Kartu", key=f"mini_mem_{pos}", use_container_width=True):
                gs["mem_open"].append(pos)
                if len(gs["mem_open"]) == 2:
                    gs["mem_check"] = True
                st.rerun()
    if memeriksa:
        time.sleep(1)
        p1, p2 = gs["mem_open"]
        if gs["mem_deck"][p1][0] == gs["mem_deck"][p2][0]:
            gs["mem_found"] += [p1, p2]
            poin, naik = mini_benar(gs)
            gs["flash"] = ("ok", f"⭐ Pasangan benar! +{poin} poin"
                           + (" · naik level!" if naik else ""))
            if len(gs["mem_found"]) == 2 * len(MEMORY_AYAT):
                gs["menang"] = True
                _mini_selesai(gs)
        else:
            mini_salah(gs, "Belum cocok.")
            if gs["nyawa"] <= 0:
                _mini_selesai(gs)
        gs["mem_open"] = []
        gs["mem_check"] = False
        st.rerun()
    if st.button("🔄 Main Lagi / Acak Kartu", key="mini_mem_ulang"):
        mini_reset(gs["mode"], gs["game"])
        st.rerun()


def render_mini_game():
    st.markdown(MINI_CSS, unsafe_allow_html=True)
    awal = st.session_state.get("mini_mode", st.session_state.get("mode", MODE_LIST[0]))
    if awal not in MODE_LIST:
        awal = MODE_LIST[0]
    kelas = kelas_siswa()
    label_mode = [f"🔒 {m}" if kelas is not None and m != kelas else m
                  for m in MODE_LIST]
    pilihan_mode = st.selectbox("Mode permainan", label_mode,
                                index=(label_mode.index(awal) if awal in label_mode
                                       else label_mode.index(kelas) if kelas in label_mode else 0),
                                key="mini_mode")
    mode = MODE_LIST[label_mode.index(pilihan_mode)]
    if mode_terkunci(mode):
        kartu_terkunci(mode, "kembali_dari_mini")
        return
    game = st.radio("Pilih permainan", GAMES_MINI[mode], horizontal=True,
                    key=f"mini_game_{mode}")
    if st.session_state.user_role == "Siswa":
        st.caption("Poin per jawaban benar: +10 (mudah), +15 (sedang), +20 (sulit) · "
                   "3 nyawa · 2 benar beruntun = level naik lebih cepat.")
    else:
        st.caption("Poin per jawaban benar: +10 (mudah), +15 (sedang), +20 (sulit) · "
                   "3 nyawa · Hasil akhir otomatis masuk ke Nilai & Hasil.")
    if st.button("▶ Mulai Mini Game - 10 Ronde", key="mini_start", type="primary",
                 use_container_width=True):
        mini_reset(mode, game)
        st.rerun()

    gs = st.session_state.get("mini")
    if not gs or gs.get("mode") != mode or gs.get("game") != game:
        mini_reset(mode, game)
        gs = st.session_state.mini
    for k, v in {"lvl": 1, "benar": 0, "streak_benar": 0, "streak_salah": 0,
                 "opsi": None, "opsi_round": -1, "opsi_pasang": [], "opsi_tangkap": [],
                 "opsi_tajwid": [], "opsi_mad": [], "langkah": [], "langkah_round": -1,
                 "puzzle": [], "puzzle_order": [], "pz_round": -1, "jawab": None,
                 "ah_round": -1, "ah_opsi": [], "mem_deck": [], "mem_open": [],
                 "mem_found": [], "mem_check": False, "menang": False}.items():
        gs.setdefault(k, v)

    if gs["done"]:
        if gs.get("menang"):
            st.success("🎉 Selamat! Kamu Menang!")
        st.success(f"Permainan selesai! Skor akhir {gs['skor']}")
        st.markdown("⭐" * max(1, min(5, round(gs["skor"] / 40))))
        if gs["nyawa"] <= 0:
            st.caption("Nyawa habis — jangan menyerah, ayo coba lagi!")
        m1, m2 = st.columns(2)
        if m1.button("🔁 Main Lagi", key="mini_again", use_container_width=True):
            mini_reset(mode, game)
            st.rerun()
        if m2.button("📊 Lihat Nilai & Hasil", key="mini_hasil", use_container_width=True):
            st.session_state.menu = "Nilai & Hasil"
            st.rerun()
        return

    flash = gs.pop("flash", None)
    if flash:
        (st.success if flash[0] == "ok" else st.warning)(flash[1])
    lvl = mini_level(gs)
    if game == "Memory Ayat":
        st.caption(f"⏱️ Sesi memory  ·  ⭐ Skor {gs['skor']}  ·  ❤️ Nyawa {gs['nyawa']}")
    else:
        st.caption(
            f"Ronde {gs['idx'] + 1}/{MINI_RONDE}  ·  ⭐ Skor {gs['skor']}  ·  ❤️ Nyawa {gs['nyawa']}"
        )
    badge_tier(lvl)
    i = gs["idx"]

    if mode == "Iqro'" and game == "Tebak Huruf":
        nama, glyph = HIJAIYAH[(i * 3 + 1) % len(HIJAIYAH)]
        if gs["opsi_round"] != i:
            gs["opsi_round"] = i
            opsi = [nama] + random.sample(
                [n for n, _ in HIJAIYAH if n != nama], 3)
            random.shuffle(opsi)
            gs["opsi"] = opsi
        opsi = gs["opsi"]
        st.markdown(f'<div class="mini-glyph arab">{glyph}</div>', unsafe_allow_html=True)
        st.caption("Pilih nama huruf hijaiyah di atas.")
        cols = st.columns(4)
        for j, opt in enumerate(opsi):
            if cols[j].button(opt, key=f"mini_huruf_{i}_{j}", use_container_width=True):
                mini_jawab(gs, opt == nama, f"Jawaban benar: {nama}.")

    elif mode == "Iqro'" and game == "Pasangkan Huruf":
        pasangan = [HIJAIYAH[(i * 3 + j) % len(HIJAIYAH)] for j in range(4)]
        if gs["opsi_round"] != -i:
            gs["opsi_round"] = -i
            gs["opsi_pasang"] = [n for n, _ in pasangan]
            random.shuffle(gs["opsi_pasang"])
        kanan = gs["opsi_pasang"]
        st.write("Pilih huruf di kiri, lalu pilih nama yang cocok di kanan.")
        kiri_kol, kanan_kol = st.columns(2)
        for j, (_, glyph) in enumerate(pasangan):
            if kiri_kol.button(glyph, key=f"mini_pl_{i}_{j}", use_container_width=True):
                gs["sel"] = glyph
                st.rerun()
        for j, nama_opsi in enumerate(kanan):
            if kanan_kol.button(nama_opsi, key=f"mini_pr_{i}_{j}", use_container_width=True):
                dipilih = gs.get("sel")
                target = next((n for n, g in pasangan if g == dipilih), None)
                gs["sel"] = None
                benar = bool(dipilih) and nama_opsi == target
                mini_jawab(gs, benar,
                           f"Pasangan yang tepat: {target}." if dipilih
                           else "Pilih huruf di kiri terlebih dahulu.")
        if gs.get("sel"):
            st.info(f"Huruf terpilih: {gs['sel']}")

    elif mode == "Iqro'":
        target_nama, target_glyph = HIJAIYAH[(i * 2 + 3) % len(HIJAIYAH)]
        if gs["opsi_round"] != 1000 + i:
            gs["opsi_round"] = 1000 + i
            opsi = [(target_nama, target_glyph)] + random.sample(
                [(n, g) for n, g in HIJAIYAH if n != target_nama], 3)
            random.shuffle(opsi)
            gs["opsi_tangkap"] = opsi
        opsi = gs["opsi_tangkap"]
        st.subheader(f"🎯 Tangkap huruf: {target_nama}")
        cols = st.columns(4)
        for j, (nama, glyph) in enumerate(opsi):
            if cols[j].button(glyph, key=f"mini_tangkap_{i}_{j}", use_container_width=True):
                mini_jawab(gs, nama == target_nama,
                           f"Targetnya {target_glyph} ({target_nama}).")

    elif mode == "Tahsin" and game == "Warna-Warni Tajwid":
        kata, jawab, opsi_asli, exp = TAJWID_Q[i % len(TAJWID_Q)]
        if gs["opsi_round"] != 2000 + i:
            gs["opsi_round"] = 2000 + i
            gs["opsi_tajwid"] = list(opsi_asli)
            random.shuffle(gs["opsi_tajwid"])
        st.markdown(f'<div class="mini-kata arab" style="color:#1684d8">{kata}</div>',
                    unsafe_allow_html=True)
        st.write("Pilih hukum tajwid yang sesuai dengan contoh di atas.")
        cols = st.columns(4)
        for j, opt in enumerate(gs["opsi_tajwid"]):
            if cols[j].button(opt, key=f"mini_tajwid_{i}_{j}", use_container_width=True):
                mini_jawab(gs, opt == jawab, f"{jawab}. {exp}")

    elif mode == "Tahsin" and game == "Tebak Panjang Mad":
        kata, jawab, exp = MAD_PANJANG[i % len(MAD_PANJANG)]
        if gs["opsi_round"] != 3000 + i:
            gs["opsi_round"] = 3000 + i
            gs["opsi_mad"] = ["Pendek (1 harakat)", "2 harakat", "4–6 harakat"]
            random.shuffle(gs["opsi_mad"])
        st.subheader("🌊 Tentukan panjang bacaan")
        st.markdown(f'<div class="mini-kata arab">{kata}</div>', unsafe_allow_html=True)
        cols = st.columns(3)
        for j, opt in enumerate(gs["opsi_mad"]):
            if cols[j].button(opt, key=f"mini_mad_{i}_{j}", use_container_width=True):
                mini_jawab(gs, opt == jawab, f"{jawab}. {exp}")

    elif mode == "Tahsin":
        urutan = ["Kenali huruf dan harakat", "Periksa huruf setelahnya",
                  "Tentukan hukum tajwid"]
        if gs["langkah_round"] != i:
            gs["langkah_round"] = i
            gs["langkah"] = list(urutan)
            random.shuffle(gs["langkah"])
        st.write("Susun langkah identifikasi tajwid dengan urutan yang benar.")
        for j, item in enumerate(gs["langkah"]):
            if item not in gs["order"] and st.button("＋ " + item, key=f"mini_urut_{i}_{j}"):
                gs["order"].append(item)
                st.rerun()
        st.info("Urutan pilihan: " + (" → ".join(gs["order"]) or "—"))
        if st.button("Periksa Susunan", key=f"mini_urut_check_{i}", type="primary"):
            benar = gs["order"] == urutan
            gs["order"] = []
            mini_jawab(gs, benar,
                       "Urutannya: kenali huruf → periksa huruf setelahnya → tentukan hukum.")

    elif game == "Puzzle Ayat":
        render_puzzle_ayat(gs, i)

    elif game == "Ayat Hilang":
        render_ayat_hilang(gs, i)

    else:
        render_memory_ayat(gs)


# ---------------------------------------------------------------------------
# Belajar & Game
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# Belajar & Game
# ---------------------------------------------------------------------------
BELAJAR_LEVEL = {
    "Iqro'": ["Mengenal Huruf Hijaiyah ا - ث", "Harakat (fathah, kasrah, dhammah)",
              "Tanwin", "Mad (panjang-pendek)", "Tajwid Dasar", "Baca Lancar"],
    "Tahsin": ["Makhraj Huruf", "Tajwid", "Nun Sukun", "Mim Sukun", "Mad",
               "Qalqalah & Waqaf"],
    "Tahfidz": ["Al-Fatihah", "Juz 30 Pendek", "Surah Pendek Pilihan",
                "Sambung Ayat", "Hafalan Lancar", "Muraja'ah Hafalan"],
}
BELAJAR_CONTOH = {
    "Iqro'": 'Contoh: Huruf <span class="arab">ا</span> dibaca ... '
             '(A) Alif &nbsp; (B) Ba &nbsp; (C) Ta',
    "Tahsin": 'Contoh: Nun sukun bertemu huruf ba dibaca ... '
              '(A) Iqlab &nbsp; (B) Idgham &nbsp; (C) Ikhfa',
    "Tahfidz": 'Contoh: «بِسْمِ اللَّهِ» adalah ayat ke-... dari Al-Fatihah '
               '(A) 1 &nbsp; (B) 2 &nbsp; (C) 7',
}

_CSS_BELAJAR = """<style>
.bl-chips{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin:2px 0 18px}
.bl-chip{display:inline-flex;align-items:center;gap:6px;background:#eef5ff;color:#12518f;
 border:1px solid #cfe2ff;border-radius:999px;padding:7px 14px;font-size:12.5px;font-weight:700}
.bl-info{background:linear-gradient(90deg,#eaf3ff,#e9faf4);border:1px solid #cfe2ff;
 border-radius:12px;padding:9px 15px;font-size:13px;font-weight:600;color:#1b3d63;margin:2px 0 14px}
.stTabs [data-baseweb='tab-list'] button{font-size:15px;font-weight:700;padding:12px 18px}
.bl-level{background:linear-gradient(135deg,#eaf3ff,#eefbf6);border:1px solid #cfe2ff;
 border-radius:14px;padding:12px 16px;margin-top:10px}
.bl-level b{font-size:15px;color:#0c2c52}
.bl-bar{height:9px;border-radius:999px;background:#dbe7f5;overflow:hidden;margin:9px 0 6px}
.bl-bar span{display:block;height:100%;border-radius:999px;
 background:linear-gradient(90deg,#1677e8,#12b8a6)}
.bl-level small{font-size:11.5px;color:#5b7290;font-weight:600}
.bl-desc{background:#fff;border:1px solid #e3edf9;border-radius:16px;padding:16px 18px;
 box-shadow:0 10px 26px #0c2c5210;margin:6px 0 16px}
.bl-desc .mode{font-size:13px;color:#4a617f;margin:0}
.bl-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:12px 0}
.bl-grid .cell{background:#f4f9ff;border:1px solid #e0ecfa;border-radius:12px;
 padding:10px 12px;text-align:center}
.bl-grid .cell span{font-size:20px}
.bl-grid .cell b{display:block;font-size:10.5px;text-transform:uppercase;letter-spacing:.4px;
 color:#6b819c;margin-top:2px}
.bl-grid .cell p{margin:3px 0 0;font-size:13.5px;font-weight:700;color:#0f2f57}
.bl-contoh{background:#f7f3e8;border:1px dashed #e3cf94;border-radius:10px;padding:9px 12px;
 font-size:12.5px;color:#6a5320}
.bl-contoh .arab{font-family:serif;font-size:18px;font-weight:700}
.st-key-mulai_game button,.st-key-mini_start button{height:60px;border-radius:14px;border:0;
 background:linear-gradient(135deg,#1e7cf0,#12b8a6) !important;color:#fff !important;
 font-size:18px;font-weight:800;
 box-shadow:0 16px 34px rgba(16,124,150,.35);animation:blGlow 2.4s ease-in-out infinite}
.st-key-mulai_game button:hover,.st-key-mini_start button:hover{
 background:linear-gradient(135deg,#3492ff,#26d4c0) !important;transform:translateY(-1px)}
.st-key-mulai_game button p,.st-key-mini_start button p{font-size:18px !important;
 font-weight:800 !important;color:#fff !important}
@keyframes blGlow{0%,100%{box-shadow:0 14px 30px rgba(16,124,150,.32)}
 50%{box-shadow:0 18px 42px rgba(18,184,166,.55)}}
.bl-warn{background:#fff8e1;border:1px solid #f0d488;border-left:4px solid #f0b400;
 border-radius:10px;padding:10px 14px;font-size:12.5px;font-weight:600;color:#6a5320;
 margin-top:10px;line-height:1.5}
.bl-ok{background:#e9faf1;border:1px solid #b7e6cf;border-left:4px solid #08a979;
 border-radius:10px;padding:10px 14px;font-size:12.5px;font-weight:600;color:#0c5a42;
 margin-top:10px;line-height:1.5}
.bl-score{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:12px}
.bl-score .cell{background:#f7fafd;border:1px solid #e3edf9;border-radius:12px;padding:11px 14px}
.bl-score .cell span{font-size:12px;color:#6b819c;font-weight:600;display:block}
.bl-score .cell b{font-size:17px;color:#0f2f57}
.bl-tips{display:flex;gap:9px;align-items:flex-start;background:#eef7ff;
 border:1px dashed #b9d6f5;border-radius:12px;padding:11px 14px;font-size:12.5px;
 color:#2a4d74;margin-top:16px;line-height:1.5}
@media(max-width:640px){.bl-grid{grid-template-columns:1fr}.bl-score{grid-template-columns:1fr}
 .st-key-mulai_game button,.st-key-mini_start button{font-size:15.5px;height:56px}}
</style>"""


def _belajar_skor():
    nama = rapikan_nama(str(st.session_state.get("user_name") or "")).casefold()
    nama_kelas = {rapikan_nama(d["nama"]).casefold() for d in LB_SISWA}
    skor_saya, skor_kelas = [], []
    for h in st.session_state.data.get("hasil", []) or []:
        if str(h.get("tipe")) != "game":
            continue
        siapa = rapikan_nama(str(h.get("siswa") or "")).casefold()
        if siapa not in nama_kelas:
            continue
        try:
            skor = int(h.get("skor") or 0)
        except (TypeError, ValueError):
            continue
        skor_kelas.append(skor)
        if siapa == nama:
            skor_saya.append((_lb_parse_tanggal(h.get("tanggal")) or datetime.min, skor))
    terakhir = max(skor_saya)[1] if skor_saya else None
    return terakhir, (max(skor_kelas) if skor_kelas else None)


def page_belajar():
    st.markdown(_CSS_BELAJAR, unsafe_allow_html=True)
    st.markdown(f"""
    <div class="hero-small">
      <h2>🎮 {T("Belajar & Game", "Learn & Games", "تعلم وألعاب")}</h2>
      <p>{T("Pilih Mode, Level, lalu Mulai. Nilai otomatis masuk ke Nilai & Hasil "
           "dan Leaderboard (khusus Siswa).",
           "Choose Mode, Level, then Start. Scores automatically go to Scores & Results "
           "and the Leaderboard (students only).",
           "اختر الوضع والمستوى ثم ابدأ. تُضاف الدرجات تلقائيًا إلى الدرجات والنتائج "
           "ولوحة المتصدرين (للطلاب فقط).")}</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(
        '<div class="bl-chips">'
        '<span class="bl-chip">📚 20 Soal per Sesi</span>'
        '<span class="bl-chip">🎮 Mini Game 10 Ronde</span>'
        '<span class="bl-chip">⏱️ Tanpa Batas Waktu / Bisa Diulang</span>'
        '</div>', unsafe_allow_html=True)
    if st.session_state.get("quiz") and st.session_state.quiz["tipe"] == "game":
        render_quiz()
        return
    tab_latihan, tab_mini = st.tabs([
        T("📝 Latihan Soal (20 Soal)", "📝 Question Practice (20 Qs)", "📝 تدريب الأسئلة (٢٠)"),
        T("🎮 Mini Game (10 Ronde)", "🎮 Mini Games (10 Rounds)", "🎮 ألعاب مصغرة (١٠)")])
    with tab_latihan:
        st.markdown(
            '<div class="bl-info">📝 Mode serius: 20 soal, nilai masuk rapor.</div>',
            unsafe_allow_html=True)
        st.markdown('<div class="section-title">'
                    + T("Pilih Sesi", "Choose Session", "اختر الجلسة")
                    + '</div>', unsafe_allow_html=True)
        k1, k2 = st.columns([1, 1.6])
        with k1:
            mode_terpilih = st.session_state.get("mode", MODE_LIST[0])
            if mode_terpilih not in MODE_LIST:
                mode_terpilih = MODE_LIST[0]
            kelas = kelas_siswa()
            ikon_mode = {"Iqro'": "📖", "Tahsin": "🎙️", "Tahfidz": "🧠"}
            label_mode = [(f"🔒 {ikon_mode[m]} {m}" if kelas is not None and m != kelas
                           else f"{ikon_mode[m]} {m}") for m in MODE_LIST]
            if kelas is not None and mode_terpilih != kelas:
                mode_terpilih = kelas
            indeks_mode = MODE_LIST.index(mode_terpilih)
            pilihan_mode = st.selectbox(T("Mode pembelajaran", "Learning mode", "وضع التعلم"),
                                        label_mode, index=indeks_mode)
            mode = MODE_LIST[label_mode.index(pilihan_mode)]
            if mode_terkunci(mode):
                kartu_terkunci(mode, "kembali_dari_belajar")
                return
            st.session_state.mode = mode
        with k2:
            level = st.select_slider(T("Tingkat", "Level", "المستوى"),
                                     options=list(range(1, MAX_LEVEL + 1)), value=1)
            label_level = BELAJAR_LEVEL[mode][level - 1]
            st.markdown(
                '<div class="bl-level"><b>Level ' + str(level) + ' - '
                + label_level + '</b>'
                '<div class="bl-bar"><span style="width:'
                + str(round(level / MAX_LEVEL * 100)) + '%"></span></div>'
                '<small>Level ' + str(level) + ' dari ' + str(MAX_LEVEL) + '</small></div>',
                unsafe_allow_html=True)
        st.markdown(
            '<div class="bl-desc"><p class="mode">' + MODE_DESKRIPSI[mode] + '</p>'
            '<div class="bl-grid">'
            '<div class="cell"><span>🎯</span><b>Target</b><p>' + label_level + '</p></div>'
            '<div class="cell"><span>📝</span><b>Jumlah</b><p>20 Soal</p></div>'
            '<div class="cell"><span>⭐</span><b>Poin Max</b><p>100</p></div>'
            '</div>'
            '<div class="bl-contoh">' + BELAJAR_CONTOH[mode] + '</div></div>',
            unsafe_allow_html=True)
        jumlah = 20
        render_start_sesi("game", mode, level, jumlah,
                          label=T("Mulai Latihan Soal - 20 Soal",
                                  "Start Question Practice - 20 Qs",
                                  "ابدأ تدريب الأسئلة - ٢٠ سؤالًا"),
                          key="mulai_game", dengan_catatan=False)
        if st.session_state.get("user_role") == "Pengelola":
            st.markdown(
                '<div class="bl-warn">⚠️ Sesi ini terdiri dari 20 soal. '
                'Mode coba Pengelola: nilai tidak dimasukkan ke peringkat.</div>',
                unsafe_allow_html=True)
        else:
            st.markdown(
                '<div class="bl-ok">✅ Nilai kamu akan otomatis masuk ke '
                'Nilai &amp; Hasil dan Leaderboard.</div>',
                unsafe_allow_html=True)
        skor_terakhir, skor_top = _belajar_skor()
        st.markdown(
            '<div class="bl-score">'
            '<div class="cell"><span>🏆 Skor Terakhir Kamu</span><b>'
            + (str(skor_terakhir) + ' / 100' if skor_terakhir is not None
               else '- / Belum pernah main')
            + '</b></div>'
            '<div class="cell"><span>🥇 Top Skor Kelas 11</span><b>'
            + (str(skor_top) if skor_top is not None else '-')
            + '</b></div></div>',
            unsafe_allow_html=True)
    with tab_mini:
        st.markdown(
            '<div class="bl-info">🎮 Mode santai: 10 ronde cepat, kumpulkan poin '
            'untuk naik leaderboard.</div>',
            unsafe_allow_html=True)
        render_mini_game()
    st.markdown(
        '<div class="bl-tips"><span>💡</span><span>Tips: Selesaikan Level 1 dulu sebelum '
        'pindah ke Level 2 agar progress naik.</span></div>',
        unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Ujian
# ---------------------------------------------------------------------------
UJIAN_MATERI = {
    "Iqro'": [f"Iqro' {i}" for i in range(1, 7)],
    "Tahsin": ["Makhraj", "Nun Sukun", "Mad", "Qalqalah", "Mim Sukun", "Waqaf"],
    "Tahfidz": ["Al-Fatihah", "An-Nas", "Al-Falaq", "Al-Ikhlas", "Al-Mulk"],
}
UJIAN_TAHSIN_LEVEL = {"Makhraj": (1,), "Nun Sukun": (3,), "Mad": (5,),
                      "Qalqalah": (6,), "Mim Sukun": (4,), "Waqaf": (6,)}
UJIAN_KATA_KUNCI = {"Qalqalah": "qalqalah", "Waqaf": "waqaf"}
UJIAN_SURAH_NO = {"Al-Fatihah": 1, "An-Nas": 114, "Al-Falaq": 113,
                  "Al-Ikhlas": 112, "Al-Mulk": 67}


def _ujian_pool(kategori, materi, rng=None):
    rng = rng or random
    if kategori == "Tahfidz":
        semua_jawaban = [t[2] for t in TAHFIDZ_SOAL]
        semua = []
        for _lvl, awal, jawab, surah, ayat in TAHFIDZ_SOAL:
            lain = rng.sample([j for j in semua_jawaban if j != jawab], 3)
            semua.append({"prompt": "Lanjutkan ayat berikut:", "answer": jawab,
                          "options": lain + [jawab], "arab": awal,
                          "bahas": f"QS. {surah}: {ayat}.", "awal": awal,
                          "surah": surah})
        utama = [x for x in semua if x["surah"] == materi]
    elif kategori == "Tahsin":
        semua = [{"prompt": q["prompt"], "answer": q["answer"],
                  "options": list(q["options"]), "arab": q.get("arab"),
                  "bahas": q.get("bahas") or "", "level": q["level"]}
                 for q in BANKS["Tahsin"]]
        levels = UJIAN_TAHSIN_LEVEL.get(materi, (1,))
        kata = UJIAN_KATA_KUNCI.get(materi)
        utama = [x for x in semua if x["level"] in levels
                 and (not kata or kata in (x["prompt"] + " " + x["bahas"]).lower())]
    else:
        try:
            lvl = int(str(materi).split()[-1])
        except (ValueError, IndexError):
            lvl = 1
        semua = [{"prompt": q["prompt"], "answer": q["answer"],
                  "options": list(q["options"]), "arab": q.get("arab"),
                  "bahas": q.get("bahas") or "", "level": q["level"]}
                 for q in BANKS["Iqro'"]]
        utama = [x for x in semua if x["level"] == lvl]
    rng.shuffle(utama)
    sisa = [x for x in semua if x not in utama]
    rng.shuffle(sisa)
    pool = utama + sisa
    return pool or semua


def _ujian_buat_tf(item, rng=None):
    rng = rng or random
    pilihan_salah = [o for o in item["options"] if o != item["answer"]]
    pakai_benar = rng.random() < 0.5 or not pilihan_salah
    nilai = item["answer"] if pakai_benar else rng.choice(pilihan_salah)
    if item.get("awal"):
        prompt = f"Lanjutan ayat «{item['awal']}» adalah «{nilai}»."
        arab = None
    else:
        prompt = f"{item['prompt']} Jawaban: {nilai}."
        arab = item.get("arab")
    return {"tipe": "tf", "prompt": prompt, "arab": arab,
            "options": ["Benar", "Salah"],
            "answer": "Benar" if pakai_benar else "Salah",
            "bahas": f"Jawaban yang benar: {item['answer']}. {item['bahas']}".strip()}


def _ujian_buat_audio(kategori, materi, n, rng=None):
    rng = rng or random
    soal = []
    if kategori == "Tahfidz":
        daftar = list(UJIAN_SURAH_NO)
        urut = [materi] + [s for s in daftar if s != materi]
        ekor = urut[1:]
        rng.shuffle(ekor)
        for surah in ([urut[0]] + ekor)[:n]:
            _nama, url = audio_qori(st.session_state.get("set_suara") or QORI_LIST[0],
                                    UJIAN_SURAH_NO[surah])
            lain = rng.sample([s for s in daftar if s != surah], 3)
            opsi = [surah] + lain
            rng.shuffle(opsi)
            soal.append({"tipe": "audio",
                         "prompt": "Dengarkan audio, surah apa yang dibaca?",
                         "arab": None, "options": opsi, "answer": surah,
                         "bahas": f"Audio yang diputar adalah surah {surah}.",
                         "audio_url": url, "audio_huruf": None, "audio_latin": ""})
    else:
        for name, glyph in rng.sample(HIJAIYAH, min(n, len(HIJAIYAH))):
            lain = rng.sample([g for _nm, g in HIJAIYAH if g != glyph], 3)
            opsi = [glyph] + lain
            rng.shuffle(opsi)
            soal.append({"tipe": "audio",
                         "prompt": "Dengarkan audio, pilih huruf yang dibaca.",
                         "arab": None, "options": opsi, "answer": glyph,
                         "bahas": f"Audio membunyikan huruf {name} ({glyph}).",
                         "audio_url": None, "audio_huruf": glyph + "\u064e",
                         "audio_latin": name})
    return soal


def _ujian_susun(kategori, materi, jumlah, rng=None):
    rng = rng or random
    pool = _ujian_pool(kategori, materi, rng)
    jumlah = max(1, int(jumlah))
    n_audio = max(1, jumlah // 5)
    n_tf = max(1, jumlah // 5)
    if kategori == "Tahfidz":
        n_audio = min(n_audio, len(UJIAN_SURAH_NO))
    n_mcq = max(0, jumlah - n_audio - n_tf)
    butuh = n_mcq + n_tf
    if len(pool) < butuh:
        pool = (pool * (butuh // max(1, len(pool)) + 1))[:butuh]
    soal = []
    for item in pool[:n_mcq]:
        salinan = {k: v for k, v in item.items() if k not in ("level",)}
        opsi = list(item["options"])
        rng.shuffle(opsi)
        salinan.update(tipe="mcq", options=opsi)
        soal.append(salinan)
    for item in pool[n_mcq:n_mcq + n_tf]:
        soal.append(_ujian_buat_tf(item, rng))
    soal += _ujian_buat_audio(kategori, materi, n_audio, rng)
    rng.shuffle(soal)
    return soal


def _ujian_mulai(siswa, kategori, materi, jumlah, menit, mode):
    sekarang = datetime.now()
    rng = _rng_sesi(siswa, kategori, materi)
    st.session_state["ujian"] = {
        "id": sekarang.strftime("%Y%m%d%H%M%S%f"),
        "siswa": siswa, "kategori": kategori, "materi": materi,
        "mode": mode, "jumlah": int(jumlah), "menit": int(menit),
        "seed": _kode_sesi(siswa, kategori, materi),
        "soal": _ujian_susun(kategori, materi, int(jumlah), rng),
        "idx": 0, "ragu": [False] * int(jumlah), "mulai": sekarang,
        "batas": sekarang + timedelta(minutes=int(menit)),
        "selesai": False, "tersimpan": False,
        "skor": 0, "benar": 0, "waktu": 0, "jawaban": [None] * int(jumlah),
    }
    st.session_state.pop("ujian_ai", None)
    st.rerun()


def _ujian_catat_jawaban(u_id, idx, kunci):
    u = st.session_state.get("ujian") or {}
    if u.get("id") != u_id:
        return
    jaw = list(u.get("jawaban") or [])
    total = len(u.get("soal") or [])
    while len(jaw) < total:
        jaw.append(None)
    jaw[idx] = st.session_state.get(kunci)
    u["jawaban"] = jaw


def _ujian_selesaikan(auto=False):
    u = st.session_state.get("ujian")
    if not u or u.get("selesai"):
        return
    total = len(u["soal"])
    jawaban = list(u.get("jawaban") or [])
    while len(jawaban) < total:
        jawaban.append(None)
    for i in range(total):
        kunci_i = f"ujian_pick_{u['id']}_{i}"
        if kunci_i in st.session_state:
            jawaban[i] = st.session_state.get(kunci_i)
    benar = sum(1 for q, p in zip(u["soal"], jawaban) if p == q["answer"])
    skor = round(benar / total * 100) if total else 0
    detik = max(0, min(int(u["menit"]) * 60,
                       int((datetime.now() - u["mulai"]).total_seconds())))
    u.update(selesai=True, auto=auto, jawaban=jawaban,
             benar=benar, skor=skor, waktu=detik)
    if u["mode"] == "asli" and not u.get("tersimpan"):
        data = st.session_state.data
        tanggal = datetime.now().strftime("%Y-%m-%d %H:%M")
        mulai_teks = (u["mulai"].strftime("%Y-%m-%d %H:%M")
                      if isinstance(u.get("mulai"), datetime)
                      else str(u.get("mulai") or tanggal))
        data.setdefault("hasil", []).append({
            "siswa": u["siswa"], "tipe": "ujian", "mode": u["kategori"],
            "level": u["materi"], "benar": benar, "total": total,
            "skor": skor, "tanggal": tanggal,
            "seed": u.get("seed") or "", "mulai": mulai_teks,
            "selesai": tanggal,
        })
        u["tanggal"] = tanggal
        kelas_peserta = ""
        for s in data.get("siswa", []) or []:
            if rapikan_nama(str(s.get("nama") or "")).lower() == u["siswa"].lower():
                kelas_peserta = str(s.get("kelas") or "")
                if u["kategori"] == "Tahfidz":
                    s["nilai_tahfidz"] = skor
                else:
                    s["nilai_tahsin"] = skor
                break
        papan = data.setdefault("papan", {})
        papan[u["siswa"]] = max(int(papan.get(u["siswa"]) or 0), skor)
        save_all_data()
        simpan_hasil_ujian(
            u["siswa"], u["kategori"], u["materi"],
            [{"soal": q.get("prompt", ""), "jawaban": p}
             for q, p in zip(u["soal"], jawaban)],
            skor, "Lulus" if skor >= BATAS_TUNTAS else "Belum lulus",
            kelas_peserta,
        )
        u["tersimpan"] = True
    st.rerun(scope="app")


@st.fragment(run_every=1.0)
def _ujian_timer():
    u = st.session_state.get("ujian")
    if not u or u.get("selesai"):
        return
    total = max(1, int(u["menit"]) * 60)
    sisa = max(0, int((u["batas"] - datetime.now()).total_seconds()))
    st.progress(min(1.0, sisa / total),
                text=f"⏱ {T('Sisa waktu', 'Time left', 'الوقت المتبقي')} "
                     f"{sisa // 60:02d}:{sisa % 60:02d} "
                     f"{T('dari', 'of', 'من')} {u['menit']} {T('menit', 'minutes', 'دقيقة')}")
    if sisa <= 0:
        _ujian_selesaikan(auto=True)


def _ujian_audio_huruf(glyph, latin):
    teks_ar = glyph + "\u064e"
    player = """<!doctype html><html><body style="margin:0;font-family:Inter,Arial,sans-serif;">
<button onclick="putar()" style="border:0;border-radius:10px;padding:10px 18px;
background:#1677e8;color:#fff;font-weight:700;font-size:15px;cursor:pointer;">
🔊 Putar Audio Huruf</button>
<span style="margin-left:10px;font-size:12px;color:#667;">
Klik untuk mendengarkan, lalu pilih hurufnya.</span>
<script>
function putar() {
  try {
    const vs = speechSynthesis.getVoices() || [];
    const arV = vs.find(v => v.lang && v.lang.startsWith('ar'));
    const u = new SpeechSynthesisUtterance(arV ? %s : %s);
    u.lang = arV ? 'ar-SA' : 'id-ID';
    u.rate = 0.75;
    speechSynthesis.cancel();
    speechSynthesis.speak(u);
  } catch (e) {}
}
</script></body></html>""" % (json.dumps(teks_ar), json.dumps(str(latin).lower()))
    components.html(player, height=64)


def _ujian_riwayat():
    recs = [h for h in (st.session_state.data.get("hasil") or [])
            if str(h.get("tipe")) in ("ujian", "exam")]
    st.markdown('<div class="section-title">🕘 '
                + T("Riwayat Ujian (5 Terakhir)", "Exam History (Last 5)",
                    "سجل الاختبارات (آخر 5)") + '</div>', unsafe_allow_html=True)
    if not recs:
        st.caption(T("Belum ada ujian yang dikerjakan.",
                     "No exams taken yet.", "لا توجد اختبارات بعد."))
        return
    recs.sort(key=_nilai_urut_waktu, reverse=True)
    baris = [{
        "Nama": str(h.get("siswa") or "-"),
        "Kategori": str(h.get("mode") or "-"),
        "Materi": str(h.get("level") or "-"),
        "Nilai": int(h.get("skor") or 0),
        "Status": "Lulus" if int(h.get("skor") or 0) >= BATAS_TUNTAS else "Remedial",
        "Tanggal": str(h.get("tanggal") or "-"),
    } for h in recs[:5]]
    st.dataframe(pd.DataFrame(baris), use_container_width=True, hide_index=True)


def _ujian_render_soal(u):
    soal = u["soal"][u["idx"]]
    n = len(u["soal"])
    _ujian_timer()
    st.markdown(
        '<div style="border-radius:12px;padding:10px 14px;margin:4px 0 10px;'
        'background:rgba(255,193,7,.14);border:1px solid rgba(255,193,7,.55);'
        'font-size:13.5px;font-weight:700;line-height:1.55;">'
        '⚠️ Soal dan jawaban diacak per siswa. Dilarang membuka tab lain / diskusi. '
        'Nilai otomatis masuk rapor.</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="chip-row">
      <span class="chip">👤 {opsi_aman(u['siswa'])}</span>
      <span class="chip purple">{MODE_ICON[u['kategori']]} {opsi_aman(u['kategori'])} ·
        {opsi_aman(u['materi'])}</span>
      <span class="chip {'green' if u['mode'] == 'asli' else ''}">
        {'🟢 Ujian Asli' if u['mode'] == 'asli' else '🟡 Mode Latihan'}</span>
      <span class="chip">🎯 KKM {BATAS_TUNTAS}</span>
    </div>
    """, unsafe_allow_html=True)

    soal_ke = u["idx"]
    jawaban_u = list(u.get("jawaban") or [])
    while len(jawaban_u) < n:
        jawaban_u.append(None)
    for mulai in range(0, n, 10):
        kolom = st.columns(min(10, n - mulai))
        for j, slot in enumerate(kolom):
            i = mulai + j
            status = "🟨" if u["ragu"][i] else ("🟩" if jawaban_u[i] else "⬜")
            if slot.button(f"{status}{i + 1}", key=f"ujian_nav_{u['id']}_{i}",
                           use_container_width=True,
                           type="primary" if i == soal_ke else "secondary"):
                u["idx"] = i
                st.rerun()

    st.progress((soal_ke + 1) / n,
                text=f"{T('Soal', 'Question', 'سؤال')} {soal_ke + 1} / {n}")
    arab_html = f'<div class="quiz-arab">{soal["arab"]}</div>' if soal.get("arab") else ""
    st.markdown(f"""
    <div class="quiz-card">
      <div class="quiz-prompt">{opsi_aman(soal['prompt'])}</div>{arab_html}
    </div>
    """, unsafe_allow_html=True)

    if soal["tipe"] == "audio":
        if soal.get("audio_url"):
            st.audio(soal["audio_url"], format="audio/mpeg")
            st.caption(T("Dengarkan potongan audio surah berikut.",
                         "Listen to the surah audio clip.",
                         "استمع إلى مقطع صوتي من السورة."))
        elif soal.get("audio_huruf"):
            _ujian_audio_huruf(soal["audio_huruf"], soal.get("audio_latin") or "")

    kunci = f"ujian_pick_{u['id']}_{soal_ke}"
    sekarang = jawaban_u[soal_ke]
    if sekarang not in soal["options"]:
        sekarang = None
    try:
        index_awal = soal["options"].index(sekarang) if sekarang is not None else None
    except ValueError:
        index_awal = None
    st.radio(T("Pilih jawaban", "Choose an answer", "اختر إجابة"),
             soal["options"], index=index_awal, key=kunci,
             on_change=_ujian_catat_jawaban, args=(u["id"], soal_ke, kunci),
             label_visibility="collapsed")

    terjawab = sum(1 for i in range(n)
                   if i < len(jawaban_u) and jawaban_u[i])
    st.caption(T(f"Terjawab {terjawab} dari {n} soal. Hijau = terjawab, "
                 "kuning = ragu-ragu, abu-abu = belum.",
                 f"Answered {terjawab} of {n}. Green = answered, yellow = unsure, "
                 "grey = unanswered.",
                 f"تمت الإجابة على {terjawab} من {n}. أخضر = أُجيب، أصفر = متردد، رمادي = لم يُجب."))

    b1, b2, b3, b4 = st.columns(4)
    if b1.button("← " + T("Sebelumnya", "Previous", "السابق"),
                 use_container_width=True, disabled=soal_ke == 0):
        u["idx"] = max(0, soal_ke - 1)
        st.rerun()
    label_ragu = ("🟡 " + T("Batal Ragu", "Unmark Unsure", "إلغاء التردد")
                  if u["ragu"][soal_ke]
                  else "🟡 " + T("Ragu-ragu", "Unsure", "متردد"))
    if b2.button(label_ragu, use_container_width=True):
        u["ragu"][soal_ke] = not u["ragu"][soal_ke]
        st.rerun()
    if b3.button(T("Selanjutnya", "Next", "التالي") + " →",
                 use_container_width=True, disabled=soal_ke >= n - 1):
        u["idx"] = min(n - 1, soal_ke + 1)
        st.rerun()
    if b4.button("📨 " + T("Kumpulkan", "Submit", "تسليم"), type="primary",
                 use_container_width=True):
        _ujian_selesaikan()


def _ujian_render_hasil(u):
    total = len(u["soal"])
    lulus = u["skor"] >= BATAS_TUNTAS
    tanggal = u.get("tanggal") or datetime.now().strftime("%Y-%m-%d %H:%M")
    menit, detik = divmod(int(u.get("waktu") or 0), 60)
    st.markdown(f"""
    <div class="result-hero">
      <div class="result-title">{opsi_aman(u['siswa'])} · {opsi_aman(u['kategori'])} ·
        {opsi_aman(u['materi'])}</div>
      <div class="result-score">{u['skor']}<span>/100</span></div>
      <div class="result-sub">{T('Benar', 'Correct', 'صحيح')} {u['benar']} / {total} ·
        {T('Waktu', 'Time', 'الوقت')} {menit:02d}:{detik:02d}</div>
      <div>
        <span class="badge">{'✅ LULUS' if lulus else '📈 REMEDIAL'}</span>
        <span class="badge">🎯 KKM {BATAS_TUNTAS}</span>
        {'<span class="badge">⏱ Waktu habis</span>' if u.get('auto') else ''}
        {'<span class="badge">🟡 Mode Latihan</span>' if u['mode'] == 'latihan' else ''}
      </div>
    </div>
    """, unsafe_allow_html=True)

    k1, k2, k3 = st.columns(3)
    k1.metric(T("Jumlah Benar", "Correct Answers", "الإجابات الصحيحة"),
              f"{u['benar']} / {total}")
    k2.metric(T("Waktu Dipakai", "Time Used", "الوقت المستغرق"),
              f"{menit:02d}:{detik:02d}")
    k3.metric(T("Status", "Status", "الحالة"), "LULUS" if lulus else "REMEDIAL")

    if u["mode"] == "asli" and u.get("tersimpan"):
        xp = u["benar"] * LB_XP["benar"] + (LB_XP["ujian"] if lulus else 0)
        st.success(T(f"Nilai {u['skor']} tersimpan ke Nilai & Hasil dan +{xp} XP "
                     "ke Leaderboard.",
                     f"Score {u['skor']} saved to Scores & Results and +{xp} XP "
                     "to the Leaderboard.",
                     f"تم حفظ الدرجة {u['skor']} وإضافة {xp} نقطة إلى لوحة المتصدرين."))
    elif u["mode"] == "latihan":
        st.warning("🟡 Mode Latihan - Nilai tidak disimpan")

    a1, a2, a3 = st.columns(3)
    if a1.button("🔁 " + T("Ulangi Ujian", "Retake Exam", "إعادة الاختبار"),
                 use_container_width=True, type="primary"):
        _ujian_mulai(u["siswa"], u["kategori"], u["materi"], u["jumlah"],
                     u["menit"], u["mode"])
    if a2.button("📊 " + T("Lihat Nilai & Hasil", "View Scores & Results",
                           "عرض الدرجات والنتائج"), use_container_width=True):
        st.session_state.pop("ujian", None)
        st.session_state.menu = "Nilai & Hasil"
        st.rerun()
    if a3.button("↩ " + T("Kembali", "Back", "رجوع"), use_container_width=True):
        st.session_state.pop("ujian", None)
        st.rerun()

    if lulus:
        isi = [[u["siswa"], u["kategori"], u["materi"], u["skor"], "LULUS", tanggal,
                "Ujian Asli" if u["mode"] == "asli" else "Latihan"]]
        st.download_button(
            "📄 " + T("Download Sertifikat PDF", "Download Certificate PDF",
                      "تنزيل شهادة PDF"),
            data=_pdf_bytes("SERTIFIKAT LULUS UJIAN - QORI AI",
                            ["Nama", "Kategori", "Materi", "Nilai", "Status", "Tanggal",
                             "Mode"],
                            isi),
            file_name="sertifikat_" + _slug_nama(u["siswa"]) + ".pdf",
            mime="application/pdf")
        if u["mode"] == "latihan":
            st.caption(T("Sertifikat latihan tidak tercatat di Nilai & Hasil.",
                         "Practice certificates are not recorded in Scores & Results.",
                         "شهادات التدريب لا تُسجَّل في الدرجات والنتائج."))

    st.markdown('<div class="section-title">🧾 '
                + T("Pembahasan Soal", "Question Review", "مراجعة الأسئلة")
                + '</div>', unsafe_allow_html=True)
    ai_map = st.session_state.setdefault("ujian_ai", {})
    for i, soal in enumerate(u["soal"]):
        jawab = u["jawaban"][i] if i < len(u["jawaban"]) else None
        benar_soal = jawab == soal["answer"]
        with st.expander(("✅ " if benar_soal else "❌ ")
                         + f"{T('Soal', 'Question', 'سؤال')} {i + 1}"):
            st.markdown(f"**{opsi_aman(soal['prompt'])}**")
            if soal.get("arab"):
                st.markdown(f'<div class="quiz-arab">{soal["arab"]}</div>',
                            unsafe_allow_html=True)
            st.markdown(f"- {T('Jawabanmu', 'Your answer', 'إجابتك')}: **"
                        f"{opsi_aman(str(jawab or '-'))}**")
            st.markdown(f"- {T('Jawaban benar', 'Correct answer', 'الإجابة الصحيحة')}: "
                        f"**{opsi_aman(str(soal['answer']))}**")
            if soal.get("bahas"):
                st.info(soal["bahas"])
            if not benar_soal:
                if st.button("🤖 " + T("Tanya AI Kenapa Salah?",
                                       "Ask AI Why It's Wrong?",
                                       "اسأل الذكاء الاصطناعي عن الخطأ"),
                             key=f"ujian_ai_btn_{u['id']}_{i}"):
                    prompt = (f"Siswa menjawab '{jawab}' padahal jawaban benar "
                              f"'{soal['answer']}' untuk soal: {soal['prompt']} "
                              f"{('Ayat: ' + str(soal['arab'])) if soal.get('arab') else ''}. "
                              f"Penjelasan: {soal.get('bahas') or '-'}. Jelaskan singkat "
                              "kenapa jawaban siswa salah dan bagaimana cara mengingat "
                              "jawaban yang benar.")
                    with st.spinner(T("QORI AI sedang menyiapkan jawaban...",
                                      "QORI AI is preparing an answer...",
                                      "QORI AI يجهّز الإجابة...")):
                        jawaban_ai = jawab_openai(prompt, "Ramah")
                    ai_map[i] = jawaban_ai or (
                        (soal.get("bahas") or "") + "\n\n" + T(
                            "Tips: baca ulang materi ini dan ulangi soal serupa.",
                            "Tip: review this material and retry similar questions.",
                            "نصيحة: راجع هذه المادة وأعد الأسئلة المشابهة."))
                    st.rerun()
                if i in ai_map:
                    st.info(ai_map[i])

    _ujian_riwayat()


def page_ujian():
    st.markdown(f"""
    <div class="hero-small">
      <h2>📝 {T("Ujian Online", "Online Exam", "اختبار إلكتروني")}</h2>
      <p>{T("Pilih siswa, materi, dan level. Soal diacak dengan 3 tipe: pilihan ganda, "
           "benar/salah, dan tebak audio. KKM 75.",
           "Choose a student, material, and level. Questions are randomized with 3 types: "
           "multiple choice, true/false, and audio. Passing score 75.",
           "اختر الطالب والمادة والمستوى. تُخلط الأسئلة بثلاثة أنواع: اختيار من متعدد، "
           "صواب/خطأ، وصوتي. درجة النجاح 75.")}</p>
    </div>
    """, unsafe_allow_html=True)

    ujian = st.session_state.get("ujian")
    if ujian:
        if ujian.get("selesai"):
            _ujian_render_hasil(ujian)
        else:
            _ujian_render_soal(ujian)
        return

    st.markdown('<div class="section-title">⚙️ '
                + T("Pengaturan Ujian", "Exam Settings", "إعدادات الاختبار")
                + '</div>', unsafe_allow_html=True)

    nama_saya = str(st.session_state.get("user_name") or "")
    siswa_terkunci = None
    if st.session_state.user_role == "Siswa" and nama_saya:
        siswa_terkunci = next((d["nama"] for d in LB_SISWA
                               if d["nama"].lower() == nama_saya.lower()), None)

    kiri, kanan = st.columns([1.4, 1])
    with kiri:
        if siswa_terkunci:
            st.text_input(T("Siswa", "Student", "الطالب"), siswa_terkunci,
                          disabled=True)
            siswa_pilih = siswa_terkunci
        else:
            kosong = "— " + T("Pilih siswa", "Select student", "اختر الطالب") + " —"
            pilihan_siswa = st.selectbox(
                T("Siswa (wajib)", "Student (required)", "الطالب (مطلوب)"),
                [kosong] + [d["nama"] for d in LB_SISWA], key="ujian_pilih_siswa")
            siswa_pilih = None if pilihan_siswa == kosong else pilihan_siswa
        kategori = st.selectbox(T("Kategori", "Category", "الفئة"), MODE_LIST,
                                key="ujian_kategori")
        materi = st.selectbox(T("Materi / Level", "Material / Level", "المادة / المستوى"),
                              UJIAN_MATERI[kategori], key=f"ujian_materi_{kategori}")
        c1, c2 = st.columns(2)
        jumlah = c1.selectbox(T("Jumlah Soal", "Number of Questions", "عدد الأسئلة"),
                              [5, 10, 20], index=1,
                              format_func=lambda n: T(f"{n} soal", f"{n} questions",
                                                      f"{n} سؤالًا"),
                              key="ujian_jumlah")
        menit = c2.selectbox(T("Waktu", "Duration", "المدة"), [5, 10, 20], index=2,
                             format_func=lambda n: T(f"{n} menit", f"{n} minutes",
                                                     f"{n} دقيقة"),
                             key="ujian_menit")
        _batasi_ujian_asli = aku_pengelola() and not _boleh_ubah()
        if _batasi_ujian_asli and st.session_state.get("ujian_mode_pilih") == "Ujian Asli":
            st.session_state["ujian_mode_pilih"] = "Latihan"
        mode_pilih = st.radio(
            T("Mode", "Mode", "الوضع"),
            ["Latihan"] if _batasi_ujian_asli else ["Latihan", "Ujian Asli"],
            index=0, horizontal=True, key="ujian_mode_pilih")
        if _batasi_ujian_asli:
            st.warning(PESAN_AKSES_DITOLAK
                       + " Mode Ujian Asli dinonaktifkan untuk Pengelola 2.")
            form_minta_izin("ujian")
        if mode_pilih == "Latihan":
            st.caption("🟡 " + T("Mode Latihan — nilai tidak disimpan. Cocok untuk coba-coba.",
                                 "Practice mode — scores are not saved. Great for trying out.",
                                 "وضع التدريب — لا تُحفظ الدرجات. مناسب للتجربة."))
        else:
            st.caption("🟢 " + T("Mode Ujian Asli — nilai otomatis tersimpan ke Nilai & Hasil "
                                 "dan XP Leaderboard.",
                                 "Real exam mode — scores are automatically saved to Scores & "
                                 "Results and Leaderboard XP.",
                                 "وضع الاختبار الحقيقي — تُحفظ الدرجات تلقائيًا."))

    with kanan:
        st.markdown(
            '<div style="border-radius:14px;padding:16px 18px;background:rgba(22,119,232,.08);'
            'border:1px solid rgba(22,119,232,.28);font-size:14px;line-height:1.8;">'
            '<b>📋 ' + T("Aturan Ujian", "Exam Rules", "قواعد الاختبار") + '</b><br>'
            f'🎯 KKM: <b>{BATAS_TUNTAS}</b><br>'
            '🔀 ' + T("Soal & jawaban diacak per siswa", "Questions and answers shuffled per student",
                      "تُخلط الأسئلة والأجوبة لكل طالب") + '<br>'
            '⏱ ' + T("Timer berjalan, otomatis kumpul saat habis",
                     "Timer runs; auto-submit when time is up",
                     "يعمل المؤقت ويُسلَّم تلقائيًا عند الانتهاء") + '<br>'
            '1️⃣ ' + T("1x kesempatan per sesi", "1 attempt per session",
                      "محاولة واحدة لكل جلسة") + '<br>'
            '🚫 ' + T("Tetap di tab ujian, jangan buka tab lain",
                     "Stay on the exam tab; do not open other tabs",
                     "ابقَ في تبويب الاختبار ولا تفتح تبويبات أخرى") + '<br>'
            '💾 ' + T("Mode Ujian Asli: nilai otomatis tersimpan",
                      "Real mode: scores are saved automatically",
                      "الوضع الحقيقي: تُحفظ الدرجات تلقائيًا") + '</div>',
            unsafe_allow_html=True)
        st.write("")
        if st.button("▶ " + T("Mulai Ujian", "Start Exam", "ابدأ الاختبار"),
                     type="primary", use_container_width=True,
                     disabled=not siswa_pilih):
            _ujian_mulai(siswa_pilih, kategori, materi, jumlah, menit,
                         "asli" if mode_pilih == "Ujian Asli" else "latihan")
        if not siswa_pilih:
            st.caption(T("Pilih siswa dulu agar nilai tidak nyasar.",
                         "Select a student first so the score goes to the right person.",
                         "اختر الطالب أولًا حتى تُنسب الدرجة لصاحبها."))

    _ujian_riwayat()

# ---------------------------------------------------------------------------
# Nilai & Hasil
# ---------------------------------------------------------------------------
def _nilai_dari_h(h):
    try:
        if h.get("skor") is not None:
            return int(h.get("skor") or 0)
    except (TypeError, ValueError):
        pass
    benar = int(h.get("benar") or 0)
    total = int(h.get("total") or 0)
    return round(benar / total * 100) if total > 0 else 0


def _nilai_hasil_nama(nama):
    kunci = str(nama or "").strip().lower()
    return [h for h in st.session_state.data.get("hasil", []) or []
            if str(h.get("siswa") or "").strip().lower() == kunci]


def _contoh_aktif():
    """Mode Contoh hanya berlaku untuk Pengelola; Siswa selalu Mode Asli."""
    if st.session_state.get("user_role") != "Pengelola":
        return False
    return str(st.session_state.get("mode_pengelola") or "Contoh").lower() != "asli"


def _hapus_data_contoh():
    data = st.session_state.data
    for s in data.get("siswa", []) or []:
        nama_s = rapikan_nama(str(s.get("nama") or ""))
        riw = _nilai_hasil_nama(nama_s)
        ada_tahfidz = any(str(h.get("tipe")) == "manual"
                          and str(h.get("mode")) == "Tahfidz" for h in riw)
        ada_tahsin = any(str(h.get("tipe")) == "manual"
                         and str(h.get("mode")) in ("Tahsin", "Iqro'") for h in riw)
        if not ada_tahfidz:
            s["nilai_tahfidz"] = 0
        if not ada_tahsin:
            s["nilai_tahsin"] = 0
        s.pop("nilai_iqro", None)
    st.session_state["nilai_mode"] = "asli"
    st.session_state["mode_pengelola"] = "Asli"
    save_all_data()


def _nilai_urut_waktu(h):
    return _lb_parse_tanggal(h.get("tanggal")) or datetime.min


def _nilai_mode(nama, mode):
    recs = [h for h in _nilai_hasil_nama(nama) if str(h.get("mode")) == mode]
    if not recs:
        return None
    recs.sort(key=_nilai_urut_waktu)
    return _nilai_dari_h(recs[-1])


def _nilai_predikat(rata):
    if rata is None:
        return "-"
    if rata >= 90:
        return "A"
    if rata >= 80:
        return "B"
    if rata >= 70:
        return "C"
    return "Remedial"


def _nilai_status(rata):
    if rata is None:
        return "-"
    return "Lulus" if rata >= 70 else "Remedial"


def _nilai_sumber(h):
    if not h:
        return "-"
    return "Input Guru" if str(h.get("tipe")) == "manual" else "Dari Kuis"


def _waktu_sesi_teks(h):
    if not h:
        return "-"
    mulai = str(h.get("mulai") or "").strip()
    selesai = str(h.get("selesai") or h.get("tanggal") or "").strip()
    if not mulai:
        return "-"
    return f"{mulai[:16]} - {selesai[:16] or '-'}"


def _nilai_rows_20(contoh=None):
    if contoh is None:
        contoh = _contoh_aktif()
    rows = []
    for d in LB_SISWA:
        iqro = _nilai_mode(d["nama"], "Iqro'")
        tahsin = _nilai_mode(d["nama"], "Tahsin")
        tahfidz = _nilai_mode(d["nama"], "Tahfidz")
        riwayat = sorted(_nilai_hasil_nama(d["nama"]), key=_nilai_urut_waktu)
        terakhir = riwayat[-1] if riwayat else None
        sumber = _nilai_sumber(terakhir)
        if not riwayat and contoh:
            if d["kategori"] == "Iqro' Dasar":
                iqro = d["nilai"]
            elif d["kategori"] == "Tahfidz":
                tahfidz = d["nilai"]
            else:
                tahsin = d["nilai"]
            sumber = T("Contoh", "Sample", "عينة")
        ada = [v for v in (iqro, tahsin, tahfidz) if v is not None]
        rata = round(sum(ada) / len(ada)) if ada else None
        rows.append({
            "nama": d["nama"], "status": d["status"], "kategori": d["kategori"],
            "iqro": iqro, "tahsin": tahsin, "tahfidz": tahfidz,
            "ujian": _nilai_dari_h(terakhir) if terakhir else None,
            "tanggal": str((terakhir or {}).get("tanggal") or "")[:16] or "-",
            "sumber": sumber,
            "seed": str((terakhir or {}).get("seed") or "").strip() or "-",
            "waktu": _waktu_sesi_teks(terakhir),
            "sampel": bool(not riwayat and contoh),
            "rata": rata, "predikat": _nilai_predikat(rata),
            "lulus": _nilai_status(rata),
            "riwayat": riwayat,
        })
    return rows


_NILAI_TAG = {
    "Iqro'": ["Makhraj huruf", "Harakat (fathah/kasrah/dhammah)"],
    "Tahsin": ["Makhraj huruf", "Mad (panjang-pendek)"],
    "Tahfidz": ["Kelancaran hafalan", "Qalqalah & tajwid"],
}


def _nilai_analisis(row):
    skor = [("Iqro'", row["iqro"]), ("Tahsin", row["tahsin"]), ("Tahfidz", row["tahfidz"])]
    lemah = [(m, s) for m, s in skor if s is not None and s < 80]
    if not lemah:
        if row["rata"] is None:
            return [], T("Belum ada nilai. Ajak siswa mengerjakan kuis atau input nilai ujian manual.",
                         "No scores yet. Have the student take a quiz or enter a manual exam score.",
                         "لا توجد درجات بعد. اطلب من الطالب أداء اختبار أو أدخل درجة اختبار يدوية.")
        return [], T(f"Semua nilai sudah baik (rata-rata {row['rata']}). Pertahankan latihan rutin "
                     "dan naikkan target ke level berikutnya.",
                     f"All scores look good (average {row['rata']}). Keep up the routine practice "
                     "and aim for the next level.",
                     f"جميع الدرجات جيدة (المتوسط {row['rata']}). حافظ على التدريب المنتظم "
                     "وارفع الهدف إلى المستوى التالي.")
    mode, nilai = min(lemah, key=lambda x: x[1])
    if mode == "Tahsin" and nilai < 70:
        saran = T(f"Makhraj huruf ع masih lemah (nilai Tahsin {nilai}). Ulangi latihan makhraj "
                  "terutama huruf ع, ح, خ, lalu rapikan panjang-pendek (mad).",
                  f"The makhraj of ع is still weak (Tahsin score {nilai}). Repeat makhraj drills "
                  "especially for ع, ح, خ, then fix the lengths (mad).",
                  f"مخرج حرف ع لا يزال ضعيفًا (درجة التحسين {nilai}). أعد تدريبات المخارج "
                  "خاصة ع، ح، خ ثم اضبط المدود.")
    else:
        saran = T(f"Nilai {mode} {nilai} masih perlu perbaikan. Fokus pada "
                  + " dan ".join(_NILAI_TAG[mode]) + " lewat latihan bertahap setiap hari.",
                  f"The {mode} score of {nilai} needs improvement. Focus on "
                  + " and ".join(_NILAI_TAG[mode]) + " with short daily practice.",
                  f"درجة {mode} ({nilai}) تحتاج إلى تحسين. ركّز على "
                  + " و ".join(_NILAI_TAG[mode]) + " بتدريب يومي قصير.")
    return _NILAI_TAG[mode], saran


def _nilai_render_detail(row, terbuka=False):
    with st.expander("🔍 " + T("Detail", "Details", "التفاصيل") + f" — {row['nama']}",
                     expanded=terbuka):
        r1, r2, r3 = st.columns(3)
        r1.markdown(f"**{T('Kategori', 'Category', 'الفئة')}:** {opsi_aman(row['kategori'])}")
        r2.markdown(f"**{T('Status', 'Status', 'الحالة')}:** {opsi_aman(row['status'])}")
        r3.markdown(f"**{T('Rata-rata', 'Average', 'المتوسط')}:** "
                    f"{row['rata'] if row['rata'] is not None else '-'}"
                    + (f" ({row['predikat']})" if row["rata"] is not None else ""))
        terakhir = row["riwayat"][-1] if row["riwayat"] else None
        sumber = _nilai_sumber(terakhir) if terakhir else row.get("sumber", "-")
        st.markdown(f"**{T('Sumber Nilai', 'Score Source', 'مصدر الدرجة')}:** {opsi_aman(sumber)}"
                    + (f" · {T('Tanggal Ujian', 'Exam Date', 'تاريخ الاختبار')}: "
                       f"{opsi_aman(str(terakhir.get('tanggal'))[:16])}" if terakhir else ""))
        st.markdown("**📜 " + T("Riwayat Kuis", "Quiz History", "سجل الاختبارات") + "**")
        if not row["riwayat"]:
            st.caption(T("Belum ada riwayat kuis untuk siswa ini.",
                         "No quiz history for this student yet.",
                         "لا يوجد سجل اختبارات لهذا الطالب بعد."))
        else:
            for h in list(reversed(row["riwayat"]))[:10]:
                manual = str(h.get("tipe")) == "manual"
                jenis = T("Input Manual", "Manual Entry", "إدخال يدوي") if manual else str(h.get("mode") or "-")
                level = "-" if manual else str(h.get("level") or "-")
                benar = int(h.get("benar") or 0)
                total = int(h.get("total") or 0)
                benar_teks = f"{benar}/{total}" if total else "-"
                seed_h = str(h.get("seed") or "").strip()
                seed_teks = (f" · 🔑 {opsi_aman(seed_h)}"
                             if seed_h and st.session_state.user_role == "Pengelola" else "")
                st.markdown(
                    f"<div class='nilai-meta'>• {opsi_aman(str(h.get('tanggal') or '-'))} · "
                    f"{opsi_aman(jenis)} · Level {opsi_aman(level)} · "
                    f"<b>{_nilai_dari_h(h)}</b> ({benar_teks}){seed_teks}</div>",
                    unsafe_allow_html=True)
            if len(row["riwayat"]) > 10:
                st.caption(T(f"Menampilkan 10 dari {len(row['riwayat'])} riwayat terakhir.",
                             f"Showing the latest 10 of {len(row['riwayat'])} records.",
                             f"عرض آخر 10 من {len(row['riwayat'])} سجلات."))
        tags, saran = _nilai_analisis(row)
        k1, k2 = st.columns(2)
        k1.markdown("**⚠️ " + T("Kekurangan", "Weaknesses", "نقاط الضعف") + "**")
        if tags:
            k1.markdown("\n".join(f"- {t}" for t in tags))
        else:
            k1.markdown("- " + T("Tidak ada kekurangan menonjol.", "No major weaknesses.",
                                 "لا توجد نقاط ضعف بارزة."))
        k2.markdown("**🤖 " + T("Saran Perbaikan dari AI", "AI Improvement Tips",
                                "نصائح التحسين من الذكاء الاصطناعي") + "**")
        k2.info(saran)
        if row.get("sampel"):
            k2.caption(T("Catatan: angka ini masih DATA CONTOH, bukan nilai ujian asli.",
                         "Note: these numbers are SAMPLE DATA, not real exam scores.",
                         "ملاحظة: هذه الأرقام بيانات تجريبية وليست درجات اختبار حقيقية."))
        if st.button("🏆 " + T("Lihat di Leaderboard", "View on Leaderboard", "عرض في لوحة المتصدرين"),
                     key="d_lb_" + _slug_nama(row["nama"])):
            st.session_state.menu = "Leaderboard"
            st.rerun()


def page_nilai():
    st.markdown(f"""
    <div class="hero-small">
      <h2>📊 {T("Nilai & Hasil", "Scores & Results", "الدرجات والنتائج")}</h2>
      <p>{T("Raport Kelas 11: nilai, predikat, tren, dan saran perbaikan per siswa.",
           "Class 11 report: scores, grades, trends, and improvement tips per student.",
           "تقرير الفصل 11: الدرجات والتقديرات والاتجاهات ونصائح التحسين لكل طالب.")}</p>
    </div>
    """, unsafe_allow_html=True)
    if (pesan_nilai := st.session_state.pop("nilai_info", None)):
        st.success(pesan_nilai)
    data = st.session_state.data
    pengelola = st.session_state.user_role == "Pengelola"
    guru = st.session_state.user_role in ("Pengelola", "Guru")
    contoh_mode = _contoh_aktif()
    pengelola_nilai = st.session_state.user_role == "Pengelola"
    boleh_ubah = _boleh_ubah()

    st.markdown(
        '<div style="border-radius:14px;padding:12px 18px;margin:0 0 14px;font-weight:800;'
        'font-size:14.5px;background:rgba(22,119,232,.10);border:1px solid rgba(22,119,232,.28);">'
        '📍 ' + T("Kelas 11 - 20 Siswa - Tahun Ajaran 2026/2027",
                   "Class 11 - 20 Students - Academic Year 2026/2027",
                   "الفصل 11 - 20 طالبًا - العام الدراسي 2026/2027") + "</div>",
        unsafe_allow_html=True)

    rows = _nilai_rows_20()
    nama_saya = st.session_state.user_name or data["profil"]["nama"]
    if not guru:
        rows = [r for r in rows if r["nama"].lower() == str(nama_saya).lower()]

    hasil_semua = data.get("hasil", []) or []
    ada_rata = [r["rata"] for r in rows if r["rata"] is not None]
    rata_kelas = round(sum(ada_rata) / len(ada_rata)) if ada_rata else 0
    tertinggi = max(ada_rata) if ada_rata else 0
    siswa_ujian = len({str(h.get("siswa") or "").strip().lower()
                       for h in hasil_semua if str(h.get("siswa") or "").strip()})
    m1, m2, m3, m4 = st.columns(4)
    m1.metric(T("Rata-rata Kelas 11", "Class 11 Average", "متوسط الفصل 11"), rata_kelas)
    m2.metric(T("Nilai Tertinggi", "Highest Score", "أعلى درجة"), tertinggi)
    m3.metric(T("Total Ujian Dikerjakan", "Exams Completed", "إجمالي الاختبارات"),
              len(hasil_semua))
    m4.metric(T("Siswa Sudah Ujian", "Students Tested", "الطلاب الذين اختُبروا"),
              f"{siswa_ujian} / {len(LB_SISWA)}")

    kiri, kanan = st.columns([2, 1])
    with kiri:
        st.markdown('<div class="section-title">📈 '
                    + T("Perkembangan Nilai Kelas 11 per Minggu", "Weekly Score Trend",
                        "تطور الدرجات الأسبوعي") + '</div>', unsafe_allow_html=True)
        tren_rows = []
        for h in hasil_semua:
            dt = _lb_parse_tanggal(h.get("tanggal"))
            if dt is None:
                continue
            tren_rows.append({"Minggu": dt - timedelta(days=dt.weekday()),
                              "Nilai": _nilai_dari_h(h)})
        if tren_rows:
            df_tren = (pd.DataFrame(tren_rows).groupby("Minggu")["Nilai"].mean().round(1)
                       .reset_index().sort_values("Minggu"))
            df_tren["Minggu"] = df_tren["Minggu"].dt.strftime("%d/%m")
            st.line_chart(df_tren.set_index("Minggu")["Nilai"], height=250, color="#08a979")
        else:
            st.info(T("Belum ada nilai asli. Silakan mulai Ujian / Kuis dulu.",
                      "No real scores yet. Start an Exam / Quiz first.",
                      "لا توجد درجات حقيقية بعد. ابدأ اختبارًا / مسابقة أولًا."))
    with kanan:
        st.markdown('<div class="section-title">📊 '
                    + T("Rata-rata per Kategori", "Average per Category",
                        "المتوسط حسب الفئة") + '</div>', unsafe_allow_html=True)
        kat_avg = {}
        for k in LB_KATEGORI_SISWA:
            nilai_k = [r["rata"] for r in rows if r["kategori"] == k and r["rata"] is not None]
            kat_avg[k] = round(sum(nilai_k) / len(nilai_k)) if nilai_k else 0
        if any(r["rata"] is not None for r in rows):
            st.bar_chart(pd.Series(kat_avg), height=250, color="#1677e8")
            if contoh_mode:
                st.caption(T("⚠️ Grafik memakai data contoh/simulasi, bukan nilai asli.",
                             "⚠️ Chart uses sample/simulated data, not real scores.",
                             "⚠️ يستخدم المخطط بيانات تجريبية وليست درجات حقيقية."))
        else:
            st.info(T("Belum ada nilai asli. Silakan mulai Ujian / Kuis dulu.",
                      "No real scores yet. Start an Exam / Quiz first.",
                      "لا توجد درجات حقيقية بعد. ابدأ اختبارًا / مسابقة أولًا."))

    if pengelola_nilai and contoh_mode:
        st.markdown(
            '<div style="border-radius:14px;padding:14px 18px;margin:4px 0 10px;'
            'background:#fff4cc;border:2px solid #f0b400;color:#5c4400;font-weight:700;'
            'font-size:14.5px;line-height:1.55;">⚠️ '
            + T('DATA CONTOH / SIMULASI - Anak-anak belum uji coba. Nilai ini hanya untuk '
                'contoh tampilan. Klik tombol "Hapus Data Contoh & Mulai Dari Nol" untuk '
                'mengosongkan.',
                'SAMPLE / SIMULATED DATA - Students have not taken the tests yet. These scores '
                'are for display only. Click "Delete Sample Data & Start From Zero" to clear them.',
                'بيانات تجريبية / محاكاة - لم يخضع الطلاب للاختبارات بعد. هذه الدرجات للعرض '
                'فقط. اضغط زر الحذف لتفريغها.')
            + '</div>', unsafe_allow_html=True)
    elif pengelola_nilai:
        st.markdown(
            '<div style="border-radius:14px;padding:12px 18px;margin:4px 0 10px;'
            'background:rgba(8,169,121,.10);border:1px solid rgba(8,169,121,.35);'
            'font-weight:700;font-size:14px;">✅ '
            + T("Mode Asli: tabel hanya berisi nilai dari Kuis/Ujian siswa atau Input Nilai "
                "Manual (Guru). Tidak ada nilai contoh.",
                "Real mode: the table only shows scores from student Quizzes/Exams or Manual "
                "Entry (Teacher). No sample scores.",
                "الوضع الحقيقي: يعرض الجدول فقط درجات الاختبارات أو الإدخال اليدوي. لا درجات تجريبية.")
            + '</div>', unsafe_allow_html=True)

    if pengelola_nilai and not aku_super_admin():
        if not _izin_aktif():
            st.warning(PESAN_AKSES_DITOLAK)
        form_minta_izin("nilai")

    if pengelola_nilai:
        b_hapus, b_mode = st.columns([2.4, 1.4])
        if b_hapus.button("🗑️ " + T("Hapus Data Contoh & Mulai Dari Nol",
                                     "Delete Sample Data & Start From Zero",
                                     "حذف البيانات التجريبية والبدء من الصفر"),
                          key="btn_hapus_contoh", use_container_width=True,
                          disabled=not boleh_ubah):
            _hapus_data_contoh()
            st.session_state["nilai_info"] = T(
                "Data contoh sudah dihapus. Tabel sekarang hanya menampilkan nilai asli; "
                "nilai akan terisi otomatis setelah siswa mengerjakan ujian.",
                "Sample data deleted. The table now only shows real scores; scores fill in "
                "automatically after students take an exam.",
                "تم حذف البيانات التجريبية. يعرض الجدول الآن الدرجات الحقيقية فقط.")
            st.rerun()
        if b_mode.button("🔄 " + T("Mode: Contoh / Asli", "Mode: Sample / Real",
                                   "الوضع: تجريبي / حقيقي"),
                         key="btn_mode_nilai", use_container_width=True,
                         disabled=not boleh_ubah):
            barumu = "asli" if contoh_mode else "contoh"
            st.session_state["nilai_mode"] = barumu
            st.session_state["mode_pengelola"] = "Asli" if barumu == "asli" else "Contoh"
            save_all_data()
            st.rerun()
        st.caption(T("Mode aktif: ", "Active mode: ", "الوضع النشط: ")
                   + (T("Contoh (simulasi)", "Sample (simulated)", "تجريبي (محاكاة)")
                      if contoh_mode else T("Asli", "Real", "حقيقي")))
    if not hasil_semua:
        st.info(T("Belum ada nilai asli. Silakan mulai Ujian / Kuis dulu.",
                  "No real scores yet. Start an Exam / Quiz first.",
                  "لا توجد درجات حقيقية بعد. ابدأ اختبارًا / مسابقة أولًا."))

    st.markdown('<div class="section-title">📋 '
                + T("Tabel Nilai 20 Siswa Kelas 11", "Class 11 Score Table",
                    "جدول درجات الفصل 11") + '</div>', unsafe_allow_html=True)
    semua = "Semua"
    f1, f2, f3, f4 = st.columns([1.2, 1.1, 1.1, 1.6])
    filter_kat = f1.selectbox(T("Kategori", "Category", "الفئة"),
                              [semua] + LB_KATEGORI_SISWA,
                              format_func=lambda k: T("Semua Kategori", "All Categories", "كل الفئات")
                              if k == semua else k, key="nilai_filter_kat")
    filter_status = f2.selectbox(T("Status", "Status", "الحالة"),
                                 [semua] + LB_STATUS_SISWA,
                                 format_func=lambda k: T("Semua Status", "All Statuses", "كل الحالات")
                                 if k == semua else k, key="nilai_filter_status")
    filter_pred = f3.selectbox(T("Predikat", "Grade", "التقدير"),
                               [semua, "A", "B", "C", "Remedial"],
                               format_func=lambda k: T("Semua Predikat", "All Grades", "كل التقديرات")
                               if k == semua else k, key="nilai_filter_predikat")
    cari = f4.text_input(T("🔍 Cari Nama", "🔍 Search Name", "🔍 بحث بالاسم"),
                         placeholder=T("Ketik nama siswa...", "Type student name...",
                                       "اكتب اسم الطالب..."),
                         key="nilai_cari")

    tampil = [r for r in rows
              if (filter_kat == semua or r["kategori"] == filter_kat)
              and (filter_status == semua or r["status"] == filter_status)
              and (filter_pred == semua or r["predikat"] == filter_pred)
              and (not cari.strip() or cari.strip().lower() in r["nama"].lower())]

    kolom_ekspor = ["No", "Nama Lengkap", "Status", "Kategori", "Nilai Iqro'",
                    "Nilai Tahsin", "Nilai Tahfidz", "Nilai Ujian Terakhir", "Sumber Nilai",
                    "Rata-rata", "Predikat", "Lulus / Remedial", "Tanggal Ujian"]
    if pengelola:
        kolom_ekspor += ["Seed / Kode Sesi", "Waktu Mulai - Waktu Selesai"]
    isi_ekspor = [[i, r["nama"], r["status"], r["kategori"],
                   r["iqro"] if r["iqro"] is not None else "-",
                   r["tahsin"] if r["tahsin"] is not None else "-",
                   r["tahfidz"] if r["tahfidz"] is not None else "-",
                   r["ujian"] if r["ujian"] is not None else "Belum Ujian",
                   r["sumber"],
                   r["rata"] if r["rata"] is not None else "-",
                   r["predikat"], r["lulus"], r["tanggal"]]
                  + ([r.get("seed", "-"), r.get("waktu", "-")] if pengelola else [])
                  for i, r in enumerate(tampil, start=1)]
    if pengelola:
        st.caption("🔑 Seed / Kode Sesi membuktikan setiap siswa mendapat paket soal "
                   "yang diacak berbeda (contoh: FRISCHA-2611-TAHSIN-L1).")
    kol_dl, kol_reset = st.columns([3, 1.4])
    with kol_dl:
        d1, d2 = st.columns(2)
        d1.download_button("📥 " + T("Download Excel", "Download Excel", "تنزيل Excel"),
                           data=_xlsx_bytes(kolom_ekspor, isi_ekspor),
                           file_name="nilai_kelas11_qori_ai.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                           use_container_width=True)
        d2.download_button("📄 " + T("Download PDF Raport Kelas 11", "Download Class 11 Report PDF",
                                     "تنزيل تقرير PDF"),
                           data=_pdf_bytes("Raport Kelas 11 QORI AI", kolom_ekspor, isi_ekspor,
                                           landscape=True,
                                           footer=(f"Dibuat oleh: {nama_saya} (Pengelola)"
                                                   if pengelola else None)),
                           file_name="raport_kelas11_qori_ai.pdf", mime="application/pdf",
                           use_container_width=True)
    with kol_reset:
        if pengelola:
            if st.button("🔄 " + T("Reset Semua Nilai", "Reset All Scores", "إعادة تعيين كل الدرجات"),
                         key="btn_reset_nilai", use_container_width=True,
                         disabled=not boleh_ubah):
                st.session_state["aksi_reset"] = True
                st.rerun()
    if boleh_ubah and st.session_state.get("aksi_reset"):
        st.warning(T("Yakin mau hapus semua nilai? Data tidak bisa dikembalikan.",
                     "Are you sure you want to delete all scores? This cannot be undone.",
                     "هل أنت متأكد من حذف كل الدرجات؟ لا يمكن التراجع."))
        k_ya, k_batal, _ = st.columns([1, 1, 3])
        if k_ya.button(T("Ya", "Yes", "نعم"), key="btn_reset_ya", use_container_width=True):
            data["hasil"] = []
            data["papan"] = {}
            for kunci in ("aksi_reset", "aksi_edit_idx", "aksi_hapus_idx"):
                st.session_state.pop(kunci, None)
            save_all_data()
            st.session_state["nilai_info"] = T("Semua nilai berhasil direset.",
                                               "All scores were reset.", "تمت إعادة تعيين كل الدرجات.")
            st.rerun()
        if k_batal.button(T("Batal", "Cancel", "إلغاء"), key="btn_reset_batal",
                          use_container_width=True):
            st.session_state.pop("aksi_reset", None)
            st.rerun()

    if guru:
        with st.expander("➕ " + T("Input Nilai Manual (Guru)", "Manual Score Entry (Teacher)",
                                 "إدخال درجة يدوية (المعلم)")):
            with st.form("form_nilai_manual"):
                m_nama = st.selectbox(T("Nama Siswa", "Student Name", "اسم الطالب"),
                                      [d["nama"] for d in LB_SISWA], key="nilai_manual_nama")
                m1, m2, m3 = st.columns(3)
                m_kat = m1.selectbox(T("Kategori", "Category", "الفئة"), LB_KATEGORI_SISWA,
                                     key="nilai_manual_kat")
                m_nilai = m2.number_input(T("Nilai", "Score", "الدرجة"), 0, 100, 80, step=1,
                                          key="nilai_manual_skor")
                m_tgl = m3.date_input(T("Tanggal Ujian", "Exam Date", "تاريخ الاختبار"),
                                      value=datetime.now().date(), key="nilai_manual_tgl")
                simpan_manual = st.form_submit_button(
                    "💾 " + T("Simpan Nilai", "Save Score", "حفظ الدرجة"),
                    type="primary", use_container_width=True,
                    disabled=not (boleh_ubah or st.session_state.user_role == "Guru"))
            if simpan_manual:
                mode_manual = "Iqro'" if m_kat == "Iqro' Dasar" else m_kat
                data.setdefault("hasil", []).append({
                    "siswa": m_nama, "tipe": "manual", "mode": mode_manual,
                    "level": "-", "benar": 0, "total": 0, "skor": int(m_nilai),
                    "tanggal": m_tgl.strftime("%Y-%m-%d") + " " + datetime.now().strftime("%H:%M"),
                })
                for s in data.get("siswa", []) or []:
                    if rapikan_nama(str(s.get("nama") or "")).lower() == m_nama.lower():
                        if mode_manual == "Tahfidz":
                            s["nilai_tahfidz"] = int(m_nilai)
                        else:
                            s["nilai_tahsin"] = int(m_nilai)
                        break
                papan = data.setdefault("papan", {})
                papan[m_nama] = max(int(papan.get(m_nama) or 0), int(m_nilai))
                save_all_data()
                st.session_state["nilai_info"] = T(
                    f"Nilai {m_nama} ({m_kat}) berhasil disimpan dan masuk Leaderboard.",
                    f"Score for {m_nama} ({m_kat}) saved and synced to the Leaderboard.",
                    f"تم حفظ درجة {m_nama} ({m_kat}) ومزامنتها مع لوحة المتصدرين.")
                st.rerun()

    st.caption(T("Klik baris tabel untuk membuka detail siswa di bawah.",
                 "Click a table row to open the student details below.",
                 "انقر على صف في الجدول لفتح تفاصيل الطالب أدناه."))
    if not tampil:
        st.info(T("Belum ada siswa yang cocok dengan filter ini.",
                  "No students match this filter.", "لا يوجد طلاب مطابقون لهذه التصفية."))
        terpilih = []
    else:
        baris_tabel = [{
            "No": i,
            "Nama Lengkap": r["nama"],
            "Status": r["status"],
            "Kategori": r["kategori"],
            "Nilai Iqro'": str(r["iqro"]) if r["iqro"] is not None else "-",
            "Nilai Tahsin": str(r["tahsin"]) if r["tahsin"] is not None else "-",
            "Nilai Tahfidz": str(r["tahfidz"]) if r["tahfidz"] is not None else "-",
            "Nilai Ujian Terakhir": str(r["ujian"]) if r["ujian"] is not None else "Belum Ujian",
            "Sumber Nilai": r["sumber"],
            "Rata-rata": str(r["rata"]) if r["rata"] is not None else "-",
            "Predikat": r["predikat"],
            "Lulus / Remedial": r["lulus"],
            "Tanggal Ujian": r["tanggal"],
            **({"Seed / Kode Sesi": r.get("seed", "-"),
                "Waktu Mulai - Waktu Selesai": r.get("waktu", "-")} if pengelola else {}),
        } for i, r in enumerate(tampil, start=1)]
        df_nilai = pd.DataFrame(baris_tabel)
        tabel_nilai = st.dataframe(
            df_nilai, use_container_width=True, hide_index=True, height=520,
            on_select="rerun", selection_mode="single-row", key="tabel_nilai",
            column_config={
                "No": st.column_config.NumberColumn("No", width="small"),
                "Nama Lengkap": st.column_config.TextColumn("Nama Lengkap", width=260),
            })
        try:
            terpilih = list(tabel_nilai.selection.rows)
        except Exception:
            terpilih = []

    for i, r in enumerate(tampil):
        _nilai_render_detail(r, terbuka=(i in terpilih))

# ---------------------------------------------------------------------------
# Leaderboard
# ---------------------------------------------------------------------------
LB_XP = {"materi": 10, "benar": 20, "hafalan": 50, "hadir": 5, "ujian": 50}
LB_SISWA = [
    {"nama": "FRISCHA BUNGA LESTARI", "jk": "Perempuan", "status": "Non Santri",
     "kategori": "Tahsin", "xp": 1180, "nilai": 92, "hafalan": 12, "materi": 15,
     "badge": "🌟 Juara Tajwid"},
    {"nama": "ZALFATUSSYIFA RAMADANTI", "jk": "Perempuan", "status": "Non Santri",
     "kategori": "Tahfidz", "xp": 1140, "nilai": 90, "hafalan": 22, "materi": 14,
     "badge": "📖 Bintang Tahfidz"},
    {"nama": "ZAIN RAHMANITA", "jk": "Perempuan", "status": "Non Santri",
     "kategori": "Tahfidz", "xp": 1110, "nilai": 89, "hafalan": 20, "materi": 14,
     "badge": "📖 Bintang Tahfidz"},
    {"nama": "YUSUF IMAM MA'RUF", "jk": "Laki-laki", "status": "Non Santri",
     "kategori": "Tahfidz", "xp": 1080, "nilai": 88, "hafalan": 18, "materi": 13,
     "badge": "🔥 Rajin 7 Hari"},
    {"nama": "RAIHAN", "jk": "Laki-laki", "status": "Santri",
     "kategori": "Tahsin", "xp": 1050, "nilai": 87, "hafalan": 10, "materi": 12,
     "badge": "🔥 Rajin 7 Hari"},
    {"nama": "FEBRIANSYAH RACHMAT HIDAYAT", "jk": "Laki-laki", "status": "Santri",
     "kategori": "Tahfidz", "xp": 1020, "nilai": 86, "hafalan": 19, "materi": 12,
     "badge": "📖 Bintang Tahfidz"},
    {"nama": "ANGGA FADILLAH", "jk": "Laki-laki", "status": "Non Santri",
     "kategori": "Tahsin", "xp": 990, "nilai": 85, "hafalan": 9, "materi": 11,
     "badge": ""},
    {"nama": "MUHAMMAD HAFIDZ", "jk": "Laki-laki", "status": "Non Santri",
     "kategori": "Tahfidz", "xp": 960, "nilai": 84, "hafalan": 16, "materi": 11,
     "badge": ""},
    {"nama": "ANDY RAMADANI ABDULLAH", "jk": "Laki-laki", "status": "Non Santri",
     "kategori": "Tahsin", "xp": 930, "nilai": 83, "hafalan": 8, "materi": 10,
     "badge": ""},
    {"nama": "ANGGI RATU MAHADEWI", "jk": "Perempuan", "status": "Non Santri",
     "kategori": "Tahfidz", "xp": 900, "nilai": 84, "hafalan": 15, "materi": 10,
     "badge": ""},
    {"nama": "RIZQI RAMADHANY", "jk": "Laki-laki", "status": "Santri",
     "kategori": "Tahfidz", "xp": 870, "nilai": 82, "hafalan": 14, "materi": 9,
     "badge": ""},
    {"nama": "KAWILUJEUNGAN RASYIDA RAIHANUN", "jk": "Perempuan", "status": "Santri",
     "kategori": "Tahfidz", "xp": 840, "nilai": 81, "hafalan": 13, "materi": 9,
     "badge": ""},
    {"nama": "MIFTAHUL JANNAH", "jk": "Perempuan", "status": "Santri",
     "kategori": "Tahfidz", "xp": 810, "nilai": 80, "hafalan": 12, "materi": 8,
     "badge": ""},
    {"nama": "MUHAMAD AZHAM FATAHILAH", "jk": "Laki-laki", "status": "Santri",
     "kategori": "Tahfidz", "xp": 780, "nilai": 79, "hafalan": 11, "materi": 8,
     "badge": ""},
    {"nama": "ROSMALATI KHOLISHA", "jk": "Perempuan", "status": "Santri",
     "kategori": "Tahfidz", "xp": 750, "nilai": 78, "hafalan": 10, "materi": 7,
     "badge": ""},
    {"nama": "M. ARIF ZAKARIYA", "jk": "Laki-laki", "status": "Santri",
     "kategori": "Tahfidz", "xp": 720, "nilai": 77, "hafalan": 9, "materi": 7,
     "badge": ""},
    {"nama": "MOCHAMMAD ALKAHFI MUBAROK", "jk": "Laki-laki", "status": "Non Santri",
     "kategori": "Tahfidz", "xp": 690, "nilai": 76, "hafalan": 8, "materi": 6,
     "badge": ""},
    {"nama": "MUHAMAD HARTANTO", "jk": "Laki-laki", "status": "Non Santri",
     "kategori": "Iqro' Dasar", "xp": 660, "nilai": 75, "hafalan": 3, "materi": 6,
     "badge": "⭐ Naik Daun"},
    {"nama": "IMAM MANSYUR IBNU HULKARIM", "jk": "Laki-laki", "status": "Non Santri",
     "kategori": "Tahfidz", "xp": 630, "nilai": 74, "hafalan": 7, "materi": 5,
     "badge": ""},
    {"nama": "DAFFAN OKTAFFIL HIDAYAT", "jk": "Laki-laki", "status": "Non Santri",
     "kategori": "Iqro' Dasar", "xp": 600, "nilai": 73, "hafalan": 2, "materi": 4,
     "badge": "⭐ Naik Daun"},
]
LB_KATEGORI_SISWA = ["Tahsin", "Tahfidz", "Iqro' Dasar"]
LB_STATUS_SISWA = ["Santri", "Non Santri"]
LB_PERIODE = {
    "minggu": ("Minggu Ini", "This Week", "هذا الأسبوع"),
    "bulan": ("Bulan Ini", "This Month", "هذا الشهر"),
    "semua": ("Semua Waktu", "All Time", "كل الأوقات"),
}
_LB_MEDAL = ["🥇", "🥈", "🥉"]


def _seed_kelas11(data):
    isi = _baca_json(LEADERBOARD_FILE, {})
    if int(isi.get("seed_kelas11") or 0) >= 1:
        return
    lama = {rapikan_nama(str(s.get("nama") or "")).lower(): s
            for s in data.get("siswa", []) or []}
    baru = []
    for d in LB_SISWA:
        rec = dict(lama.get(d["nama"].lower(), {}))
        program = "Iqro'" if d["kategori"] == "Iqro' Dasar" else d["kategori"]
        rec.update({
            "nama": d["nama"], "kelas": "Kelas 11", "program": program,
            "jenis_kelamin": d["jk"], "status_santri": d["status"],
            "jumlah_hafalan": str(d["hafalan"]),
            "nilai_tahsin": d["nilai"] if program in ("Tahsin", "Iqro'") else int(rec.get("nilai_tahsin") or 0),
            "nilai_tahfidz": d["nilai"] if program == "Tahfidz" else int(rec.get("nilai_tahfidz") or 0),
        })
        baru.append(rec)
    data["siswa"] = baru
    users = _baca_json(USERS_FILE, {})
    users["siswa"] = baru
    users.setdefault("versi", 1)
    _tulis_json(USERS_FILE, users)
    if not isinstance(isi, dict):
        isi = {}
    isi.setdefault("versi", 1)
    isi.setdefault("reset_at", "")
    isi.setdefault("baseline", {})
    isi.setdefault("hall_of_fame", [])
    isi["seed_kelas11"] = 1
    _tulis_json(LEADERBOARD_FILE, isi)


_seed_kelas11(st.session_state.data)

_CSS_LEADERBOARD = """
<style>
.lb-podium{display:grid;grid-template-columns:1.1fr 1fr 1fr;gap:14px;align-items:end;margin:10px 0 18px}
.lb-pcard{border-radius:18px;padding:18px 14px 16px;text-align:center;color:#3b2a00;
  background:linear-gradient(180deg,#fff8e1,#ffe9a8);border:1px solid #f0d175;
  box-shadow:0 10px 24px #00000014}
.lb-pcard.first{padding-top:10px;transform:translateY(-8px);box-shadow:0 14px 30px #b8860b33}
.lb-pcard.silver{background:linear-gradient(180deg,#f7f9fc,#e2e8f3);border-color:#c9d4e5;color:#2a3b55}
.lb-pcard.bronze{background:linear-gradient(180deg,#fff3e8,#f3d9c4);border-color:#e3bfa0;color:#4a2f1b}
.lb-medal{font-size:26px;line-height:1.1}
.lb-crown{font-size:26px;line-height:1}
.lb-pava{width:76px;height:76px;border-radius:50%;margin:8px auto 6px;display:flex;align-items:center;
  justify-content:center;font-weight:800;font-size:22px;background:#fff center/cover no-repeat;
  border:3px solid #fff;box-shadow:0 4px 12px #00000026;color:#0b4fa8}
.lb-pcard.first .lb-pava{width:92px;height:92px;font-size:26px}
.lb-pname{font-weight:800;font-size:15px;line-height:1.25}
.lb-pmeta{font-size:11.5px;opacity:.75;margin-top:2px}
.lb-pxp{font-weight:900;font-size:17px;margin-top:6px}
.lb-pmetric{font-size:11.5px;font-weight:700;opacity:.85}
.lb-pbadge{display:inline-block;font-size:10.5px;background:#ffffffb0;border-radius:999px;
  padding:3px 9px;margin:6px 2px 0;color:#3b2a00;font-weight:700}
.lb-me{background:linear-gradient(90deg,#0b4fa8,#18a8d8);color:#fff;border-radius:14px;
  padding:14px 18px;font-size:13.5px;font-weight:600;margin:4px 0 16px;box-shadow:0 8px 20px #0b4fa833}
.lb-me b{font-size:15.5px}
.lb-head{border-radius:14px;padding:12px 18px;margin:0 0 14px;font-weight:800;font-size:14.5px;
  color:color-mix(in srgb,var(--text-color) 92%,transparent);
  background:color-mix(in srgb,var(--primary-color) 10%,var(--secondary-background-color));
  border:1px solid color-mix(in srgb,var(--primary-color) 28%,transparent)}
.lb-table-scroll{overflow-x:auto;border-radius:14px;border:1px solid color-mix(in srgb,var(--text-color) 12%,transparent);
  background:color-mix(in srgb,var(--secondary-background-color) 55%,transparent);margin-top:4px}
.lb-table{width:100%;border-collapse:collapse;font-size:12.5px;color:var(--text-color)}
.lb-table th{text-align:left;font-size:10px;text-transform:uppercase;letter-spacing:.4px;opacity:.55;
  padding:9px 8px;border-bottom:1px solid color-mix(in srgb,var(--text-color) 14%,transparent);white-space:nowrap}
.lb-table td{padding:8px;border-bottom:1px solid color-mix(in srgb,var(--text-color) 8%,transparent);
  vertical-align:middle;white-space:nowrap}
.lb-table tr:last-child td{border-bottom:0}
.lb-table tr.me td{background:color-mix(in srgb,var(--primary-color) 12%,transparent)}
.lb-rk{font-weight:800;font-size:13px}
.lb-ava{width:28px;height:28px;border-radius:50%;display:inline-flex;align-items:center;
  justify-content:center;font-weight:800;font-size:11px;color:#fff;
  background:linear-gradient(135deg,#63b3ed,#2b6cb0) center/cover no-repeat;vertical-align:middle}
.lb-nm{font-weight:700}
.lb-sub{font-size:10px;opacity:.6}
.lb-bdg{display:inline-block;font-size:10px;font-weight:700;border-radius:999px;padding:2px 7px;
  margin:1px 2px 1px 0;background:color-mix(in srgb,var(--primary-color) 14%,transparent)}
.lb-delta.up{color:#08a979;font-weight:800}
.lb-delta.down{color:#e5484d;font-weight:800}
.lb-delta.same{opacity:.45}
.lb-hof-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px}
.lb-hof-card{border-radius:14px;padding:13px 15px;border:1px solid color-mix(in srgb,var(--text-color) 12%,transparent);
  background:color-mix(in srgb,var(--secondary-background-color) 65%,transparent);font-size:12.5px;color:var(--text-color)}
.lb-hof-title{font-weight:800;font-size:12.5px;margin-bottom:6px}
.lb-hof-line{display:flex;justify-content:space-between;gap:8px;padding:2px 0}
@media(max-width:760px){.lb-podium{grid-template-columns:1fr}.lb-pcard.first{transform:none}}
</style>
"""


def _lb_parse_tanggal(teks):
    for fmt in ("%Y-%m-%d %H:%M", "%d/%m/%Y %H:%M", "%Y-%m-%d"):
        try:
            return datetime.strptime(str(teks or "").strip(), fmt)
        except ValueError:
            continue
    return None


def _lb_state():
    isi = _baca_json(LEADERBOARD_FILE, {})
    baseline = isi.get("baseline") if isinstance(isi.get("baseline"), dict) else {}
    hall = [e for e in (isi.get("hall_of_fame") or []) if isinstance(e, dict)]
    return {"versi": 1, "reset_at": str(isi.get("reset_at") or ""),
            "baseline": baseline, "hall_of_fame": hall,
            "seed_kelas11": int(isi.get("seed_kelas11") or 0)}


def _lb_simpan(state):
    _tulis_json(LEADERBOARD_FILE, state)


def _lb_hasil_dalam(mulai=None, sampai=None):
    keluar = []
    for h in st.session_state.data.get("hasil", []) or []:
        dt = _lb_parse_tanggal(h.get("tanggal"))
        if dt is None:
            continue
        if mulai is not None and dt < mulai:
            continue
        if sampai is not None and dt >= sampai:
            continue
        keluar.append(h)
    return keluar


def _lb_rows(state, mulai=None, sampai=None, demo=True):
    agr = {}
    for h in _lb_hasil_dalam(mulai, sampai):
        nama = str(h.get("siswa") or "").strip().lower()
        if not nama:
            continue
        a = agr.setdefault(nama, {"benar": 0, "hafalan": 0, "nilai": [], "ujian": 0})
        a["benar"] += max(0, int(h.get("benar") or 0))
        skor = int(h.get("skor") or 0)
        manual = str(h.get("tipe")) == "manual"
        ujian_asli = str(h.get("tipe")) == "ujian"
        if (str(h.get("mode")) == "Tahfidz" and not manual and not ujian_asli
                and skor >= 60):
            a["hafalan"] += 1
        if manual and skor >= 70:
            a["ujian"] += 1
        if ujian_asli and skor >= BATAS_TUNTAS:
            a["ujian"] += 1
        if 0 <= skor <= 100:
            a["nilai"].append(skor)
    kur = _baca_json(KURIKULUM_FILE, {})
    selesai_map = kur.get("selesai") if isinstance(kur.get("selesai"), dict) else {}
    selesai_lower = {str(k).strip().lower(): v for k, v in selesai_map.items()}
    siswa_map = {str(s.get("nama") or "").strip().lower(): s
                 for s in st.session_state.data.get("siswa", []) or []}
    baseline = state.get("baseline") or {}
    rows = []
    for d in LB_SISWA:
        kunci = d["nama"].lower()
        rec = siswa_map.get(kunci, {})
        a = agr.get(kunci, {"benar": 0, "hafalan": 0, "nilai": [], "ujian": 0})
        materi_kur = len({str(i) for i in (selesai_lower.get(kunci) or [])})
        try:
            hafalan_field = max(0, int(float(str(rec.get("jumlah_hafalan") or 0))))
        except (TypeError, ValueError):
            hafalan_field = 0
        try:
            hadir = max(0, int(rec.get("hadir") or 0))
        except (TypeError, ValueError):
            hadir = 0
        try:
            nilai_field = int(float(rec.get("nilai_tahsin") or rec.get("nilai_tahfidz") or 0))
        except (TypeError, ValueError):
            nilai_field = 0
        nilai_list = [v for v in a["nilai"] if 0 <= v <= 100]
        if demo:
            materi = max(d["materi"], materi_kur)
            hafalan = max(d["hafalan"], hafalan_field, a["hafalan"])
            nilai = (round(sum(nilai_list) / len(nilai_list)) if nilai_list
                     else max(d["nilai"], nilai_field))
            badge = d["badge"]
            xp = (d["xp"] + a["benar"] * LB_XP["benar"]
                  + max(0, materi - d["materi"]) * LB_XP["materi"]
                  + max(0, hafalan - d["hafalan"]) * LB_XP["hafalan"]
                  + hadir * LB_XP["hadir"]
                  + a["ujian"] * LB_XP["ujian"])
        else:
            materi = materi_kur
            hafalan = a["hafalan"]
            nilai = round(sum(nilai_list) / len(nilai_list)) if nilai_list else 0
            badge = ""
            xp = (a["benar"] * LB_XP["benar"] + materi * LB_XP["materi"]
                  + hafalan * LB_XP["hafalan"] + hadir * LB_XP["hadir"]
                  + a["ujian"] * LB_XP["ujian"])
            if not (a["benar"] or nilai_list or materi_kur or hadir or a["ujian"]
                    or a["hafalan"]):
                continue
        b = baseline.get(d["nama"]) if isinstance(baseline.get(d["nama"]), dict) else {}
        try:
            xp = max(0, xp - int(b.get("xp") or 0))
        except (TypeError, ValueError):
            pass
        rows.append({
            "nama": d["nama"], "jk": d["jk"], "status": d["status"],
            "kategori": d["kategori"], "xp": xp, "nilai": nilai,
            "hafalan": hafalan, "materi": materi, "hadir": hadir,
            "badge": badge, "benar": a["benar"],
            "raw": {"materi": materi, "benar": a["benar"],
                    "hafalan": hafalan, "hadir": hadir, "ujian": a["ujian"]},
        })
    return rows


def _lb_avatar(nama, cls="lb-ava"):
    inisial = "".join(w[0] for w in str(nama).split()[:2]).upper() or "?"
    return f'<span class="{cls}">{opsi_aman(inisial)}</span>'


def _lb_podium_html(rows):
    kartu = []
    for i, r in enumerate(rows[:3]):
        badge = (f'<span class="lb-pbadge">{opsi_aman(r["badge"])}</span>'
                 if r["badge"] else "")
        kelas_css = ["first", "silver", "bronze"][i]
        mahkota = '<div class="lb-crown">👑</div>' if i == 0 else ""
        kartu.append(
            f'<div class="lb-pcard {kelas_css}">{mahkota}'
            f'<div class="lb-medal">{_LB_MEDAL[i]}</div>'
            f'{_lb_avatar(r["nama"], "lb-pava")}'
            f'<div class="lb-pname">{opsi_aman(r["nama"])}</div>'
            f'<div class="lb-pmeta">{opsi_aman(r["kategori"])} · {opsi_aman(r["status"])}</div>'
            f'<div class="lb-pxp">{r["xp"]} XP</div>'
            f'<div class="lb-pmetric">⭐ {T("Nilai", "Score", "الدرجة")} {r["nilai"]} · '
            f'📖 {r["hafalan"]} {T("Hafalan", "Memorized", "حفظ")}</div>'
            f'<div>{badge}</div></div>')
    return '<div class="lb-podium">' + "".join(kartu) + "</div>"


def _lb_tabel_html(rows, pos_lalu, nama_saya):
    urut = sorted(rows, key=lambda r: (-r["xp"], r["nama"].lower()))
    kepala = [
        T("Peringkat", "Rank", "الترتيب"), T("Nama Lengkap", "Full Name", "الاسم الكامل"),
        T("Jenis Kelamin", "Gender", "الجنس"), T("Status", "Status", "الحالة"),
        T("Kategori", "Category", "الفئة"), "Total XP",
        T("Nilai Rata-rata", "Average Score", "متوسط الدرجة"),
        T("Jumlah Hafalan", "Memorized", "عدد المحفوظ"),
        T("Materi Selesai", "Materials Done", "المواد المكتملة"),
        T("Badge", "Badge", "الشارة"), T("Naik/Turun", "Change", "الصعود/الهبوط"),
    ]
    baris = []
    for i, r in enumerate(urut):
        pos = i + 1
        posisi = _LB_MEDAL[i] if i < 3 else f'<span class="lb-rk">{pos}</span>'
        if r["nama"] in pos_lalu:
            beda = pos_lalu[r["nama"]] - pos
            if beda > 0:
                delta = f'<span class="lb-delta up">⬆️ {beda}</span>'
            elif beda < 0:
                delta = f'<span class="lb-delta down">⬇️ {abs(beda)}</span>'
            else:
                delta = '<span class="lb-delta same">—</span>'
        else:
            delta = '<span class="lb-delta same">—</span>'
        badge = (f'<span class="lb-bdg">{opsi_aman(r["badge"])}</span>'
                 if r["badge"] else "—")
        cls = ' class="me"' if r["nama"].lower() == nama_saya.lower() else ""
        baris.append(
            f'<tr{cls}><td>{posisi}</td>'
            f'<td><span class="lb-nm">{opsi_aman(r["nama"])}</span>'
            f'{" <span class=lb-sub>(" + T("Kamu", "You", "أنت") + ")</span>" if cls else ""}</td>'
            f'<td>{opsi_aman(r["jk"])}</td><td>{opsi_aman(r["status"])}</td>'
            f'<td>{opsi_aman(r["kategori"])}</td>'
            f'<td><b>{r["xp"]}</b></td><td>{r["nilai"]}</td><td>{r["hafalan"]}</td>'
            f'<td>{r["materi"]}</td><td>{badge}</td><td>{delta}</td></tr>')
    return ('<div class="lb-table-scroll"><table class="lb-table"><thead><tr>'
            + "".join(f"<th>{h}</th>" for h in kepala)
            + "</tr></thead><tbody>" + "".join(baris) + "</tbody></table></div>")


def page_leaderboard():
    st.markdown(f"""
    <div class="hero-small">
      <h2>🏆 {T("Leaderboard", "Leaderboard", "لوحة المتصدرين")}</h2>
      <p>{T("Peringkat 20 siswa Kelas 11 berdasarkan XP, hafalan, dan nilai.",
           "Ranking of 20 Class 11 students by XP, memorization, and scores.",
           "ترتيب 20 طالبًا من الفصل 11 حسب النقاط والحفظ والدرجات.")}</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(_CSS_LEADERBOARD, unsafe_allow_html=True)
    if st.session_state.get("lb_info"):
        st.success(st.session_state.pop("lb_info"))
    st.markdown(
        '<div class="lb-head">📍 ' + T(
            "Kelas 11 - 20 Siswa - Tahun Ajaran 2026/2027",
            "Class 11 - 20 Students - Academic Year 2026/2027",
            "الفصل 11 - 20 طالبًا - العام الدراسي 2026/2027")
        + "</div>", unsafe_allow_html=True)

    state = _lb_state()
    pengelola_lb = st.session_state.get("user_role") == "Pengelola"
    demo_lb = _contoh_aktif()
    if pengelola_lb:
        mc1, mc2, _mc = st.columns([1, 1, 2])
        if mc1.button(T("Mode Contoh", "Sample Mode", "الوضع التجريبي"),
                      key="lb_mode_contoh", use_container_width=True,
                      type="primary" if demo_lb else "secondary",
                      disabled=demo_lb or not _boleh_ubah()):
            st.session_state["mode_pengelola"] = "Contoh"
            st.session_state["nilai_mode"] = "contoh"
            save_all_data()
            st.rerun()
        if mc2.button(T("Mode Asli", "Real Mode", "الوضع الحقيقي"),
                      key="lb_mode_asli", use_container_width=True,
                      type="primary" if not demo_lb else "secondary",
                      disabled=not demo_lb or not _boleh_ubah()):
            st.session_state["mode_pengelola"] = "Asli"
            st.session_state["nilai_mode"] = "asli"
            save_all_data()
            st.rerun()
        if demo_lb:
            st.caption(T("DATA CONTOH - Klik Mode Asli untuk melihat data asli (kosong).",
                         "SAMPLE DATA - Click Real Mode to see real data (empty).",
                         "بيانات تجريبية - اضغط الوضع الحقيقي لعرض البيانات الحقيقية (فارغة)."))
    reset_dt = _lb_parse_tanggal(state.get("reset_at"))
    label_periode = {k: T(*v) for k, v in LB_PERIODE.items()}
    f1, f2, f3 = st.columns(3)
    with f1:
        kategori = st.selectbox(
            T("Kategori", "Category", "الفئة"), ["Semua"] + LB_KATEGORI_SISWA,
            format_func=lambda k: T("Semua Kategori", "All Categories", "كل الفئات")
            if k == "Semua" else k, key="lb_kategori")
    with f2:
        status = st.selectbox(
            T("Status", "Status", "الحالة"), ["Semua"] + LB_STATUS_SISWA,
            format_func=lambda k: T("Semua Status", "All Statuses", "كل الحالات")
            if k == "Semua" else k, key="lb_status")
    with f3:
        periode = st.selectbox(T("Periode", "Period", "الفترة"), list(LB_PERIODE),
                               format_func=lambda p: label_periode[p], key="lb_periode")

    sekarang = datetime.now()
    if periode == "minggu":
        mulai = (sekarang - timedelta(days=6)).replace(hour=0, minute=0, second=0, microsecond=0)
    elif periode == "bulan":
        mulai = sekarang.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    else:
        mulai = reset_dt
    if reset_dt and (mulai is None or reset_dt > mulai):
        mulai = reset_dt
    rows = _lb_rows(state, mulai, demo=demo_lb)
    if periode == "minggu":
        m2 = (sekarang - timedelta(days=13)).replace(hour=0, minute=0, second=0, microsecond=0)
        s2 = (sekarang - timedelta(days=7)).replace(hour=0, minute=0, second=0, microsecond=0)
    elif periode == "bulan":
        awal_bulan = sekarang.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        m2 = (awal_bulan - timedelta(days=1)).replace(day=1)
        s2 = awal_bulan
    else:
        m2 = s2 = None
    if m2 is not None:
        if reset_dt and reset_dt > m2:
            m2 = reset_dt
        rows_lalu = _lb_rows(state, m2, s2, demo=demo_lb) if s2 > m2 else []
    else:
        rows_lalu = []

    tampil = [r for r in rows
              if (kategori == "Semua" or r["kategori"] == kategori)
              and (status == "Semua" or r["status"] == status)]
    urut = sorted(tampil, key=lambda r: (-r["xp"], r["nama"].lower()))
    if not pengelola_lb:
        nama_login_lb = rapikan_nama(st.session_state.get("user_name") or "")
        urut = [r for r in urut if rapikan_nama(r["nama"]) == nama_login_lb]
        tampil = [r for r in tampil if rapikan_nama(r["nama"]) == nama_login_lb]
    lalu = [r for r in rows_lalu
            if (kategori == "Semua" or r["kategori"] == kategori)
            and (status == "Semua" or r["status"] == status)]
    pos_lalu = {r["nama"]: i + 1
                for i, r in enumerate(sorted(lalu, key=lambda r: (-r["xp"], r["nama"].lower())))}

    st.caption(T("XP otomatis: Materi Selesai +10 · Kuis Benar +20 · Hafalan/Ujian Lulus +50 · Hadir +5.",
                 "Automatic XP: Material Done +10 · Correct Quiz +20 · Memorization/Exam Passed +50 · Attendance +5.",
                 "النقاط التلقائية: مادة مكتملة +10 · إجابة صحيحة +20 · حفظ/اختبار ناجح +50 · حضور +5."))

    if not urut:
        if not pengelola_lb:
            st.info(T("Belum ada data - Siswa belum main game.",
                      "No data yet - Student has not played games.",
                      "لا توجد بيانات بعد - لم يلعب الطالب الألعاب."))
        else:
            st.info(T("Belum ada siswa yang cocok dengan filter ini.",
                      "No students match this filter.", "لا يوجد طلاب مطابقون لهذه التصفية."))
    else:
        st.markdown(_lb_podium_html(urut), unsafe_allow_html=True)

    nama_saya = st.session_state.get("user_name") or st.session_state.data["profil"].get("nama", "")
    pos_saya = next((i + 1 for i, r in enumerate(urut)
                     if r["nama"].lower() == nama_saya.lower()), None)
    if pos_saya:
        r_saya = urut[pos_saya - 1]
        total = len(urut)
        if pos_saya == 1:
            teks = T(
                f"📍 Posisi Kamu: Peringkat #1 dari {total} siswa · Total XP kamu {r_saya['xp']} XP. Kamu di puncak! 👑",
                f"📍 Your Position: Rank #1 of {total} students · Your total XP is {r_saya['xp']} XP. You are on top! 👑",
                f"📍 موقفك: المرتبة #1 من {total} طالبًا · مجموع نقاطك {r_saya['xp']} XP. أنت في القمة! 👑")
        else:
            atas = urut[pos_saya - 2]
            gap = f'{atas["xp"] - r_saya["xp"]} XP'
            teks = T(
                f"📍 Posisi Kamu: Peringkat #{pos_saya} dari {total} siswa · Total XP kamu {r_saya['xp']} · "
                f"Kurang {gap} lagi untuk naik ke #{pos_saya - 1}!",
                f"📍 Your Position: Rank #{pos_saya} of {total} students · Your total XP is {r_saya['xp']} · "
                f"{gap} more to move up to #{pos_saya - 1}!",
                f"📍 موقفك: المرتبة #{pos_saya} من {total} طالبًا · مجموع نقاطك {r_saya['xp']} · "
                f"تحتاج {gap} للصعود إلى #{pos_saya - 1}!")
        st.markdown(f'<div class="lb-me">{teks}</div>', unsafe_allow_html=True)

    if urut:
        st.markdown(_lb_tabel_html(tampil, pos_lalu, nama_saya), unsafe_allow_html=True)

    st.markdown("### 🏛️ " + T("Hall of Fame", "Hall of Fame", "قاعة المشاهير"))
    hall = state.get("hall_of_fame") or []
    if hall:
        kartu = []
        for e in list(reversed(hall))[:4]:
            juara = e.get("juara") or []
            baris = "".join(
                f'<div class="lb-hof-line"><span>{_LB_MEDAL[i]} {opsi_aman(str(j.get("nama") or ""))}</span>'
                f'<b>{int(j.get("xp") or 0)} XP</b></div>'
                for i, j in enumerate(juara[:3]))
            kartu.append(f'<div class="lb-hof-card"><div class="lb-hof-title">'
                         f'🏆 {T("Musim", "Season", "موسم")} {opsi_aman(str(e.get("bulan") or ""))}</div>'
                         f'{baris}</div>')
        st.markdown('<div class="lb-hof-grid">' + "".join(kartu) + "</div>",
                    unsafe_allow_html=True)
    else:
        st.caption(T("Belum ada pemenang musim sebelumnya. Juara akan muncul di sini setelah Reset Musim.",
                     "No previous season winners yet. Champions will appear here after a Season Reset.",
                     "لا يوجد فائزون في المواسم السابقة بعد. سيظهر الأبطال هنا بعد إعادة تعيين الموسم."))

    if _boleh_ubah() or st.session_state.user_role == "Guru":
        if st.button("🔄 " + T("Reset Musim", "Reset Season", "إعادة تعيين الموسم"),
                     key="lb_reset"):
            st.session_state["lb_konfirmasi"] = True
            st.rerun()
        if st.session_state.get("lb_konfirmasi"):
            st.warning(T("Reset Musim akan mengarsipkan 3 juara teratas ke Hall of Fame dan memulai hitungan XP baru.",
                         "Season Reset archives the top 3 into the Hall of Fame and starts a new XP count.",
                         "إعادة تعيين الموسم تؤرشف أفضل 3 في قاعة المشاهير وتبدأ حساب نقاط جديد."))
            k1, k2, _ = st.columns([1, 1, 3])
            if k1.button(T("Ya", "Yes", "نعم"), key="lb_reset_ya"):
                if not _lb_hasil_dalam(reset_dt):
                    st.error(T("Belum ada aktivitas baru untuk diarsipkan.",
                               "There is no new activity to archive yet.",
                               "لا يوجد نشاط جديد للأرشفة بعد."))
                else:
                    rows_now = _lb_rows(state, demo=demo_lb)
                    urut_now = sorted(rows_now, key=lambda r: (-r["xp"], r["nama"].lower()))
                    juara = [{"nama": r["nama"], "xp": r["xp"],
                              "kategori": r["kategori"]} for r in urut_now[:3]]
                    hall.append({"bulan": sekarang.strftime("%m/%Y"),
                                 "waktu": sekarang.strftime("%d/%m/%Y %H:%M"),
                                 "juara": juara})
                    state = {"versi": 1,
                             "reset_at": sekarang.strftime("%Y-%m-%d %H:%M"),
                             "baseline": {r["nama"]: {"xp": r["xp"], "raw": dict(r["raw"])}
                                          for r in rows_now},
                             "hall_of_fame": hall,
                             "seed_kelas11": state.get("seed_kelas11", 1)}
                    _lb_simpan(state)
                    st.session_state.pop("lb_konfirmasi", None)
                    st.session_state["lb_info"] = T(
                        "Musim baru dimulai. Juara musim ini sudah masuk Hall of Fame.",
                        "A new season has started. This season's champions are in the Hall of Fame.",
                        "بدأ موسم جديد. أبطال هذا الموسم في قاعة المشاهير.")
                    st.rerun()
            if k2.button(T("Batal", "Cancel", "إلغاء"), key="lb_reset_batal"):
                st.session_state.pop("lb_konfirmasi", None)
                st.rerun()
        st.caption(T("Semua perubahan tersimpan otomatis.",
                     "All changes are saved automatically.",
                     "تُحفظ جميع التغييرات تلقائيًا."))

# ---------------------------------------------------------------------------
# Materi
# ---------------------------------------------------------------------------
def _muat_kurikulum():
    if "_kurikulum" in st.session_state:
        return
    isi = _baca_json(KURIKULUM_FILE, {})
    selesai = {str(k): [str(i) for i in v]
               for k, v in (isi.get("selesai") or {}).items() if isinstance(v, list)}
    dipelajari = {str(k): [str(i) for i in v]
                  for k, v in (isi.get("dipelajari") or {}).items() if isinstance(v, list)}
    kustom = []
    for m in isi.get("kustom") or []:
        if isinstance(m, dict) and m.get("id"):
            m = dict(m)
            m["kustom"] = True
            m.setdefault("kategori", "Iqro'")
            m.setdefault("berkas", [])
            kustom.append(m)
    st.session_state["_kurikulum"] = {
        "selesai": selesai, "dipelajari": dipelajari, "kustom": kustom,
    }


def _simpan_kurikulum():
    mem = st.session_state["_kurikulum"]
    disk = _baca_json(KURIKULUM_FILE, {})
    selesai = {str(k): list(v) for k, v in (disk.get("selesai") or {}).items()
               if isinstance(v, list)}
    dipelajari = {str(k): list(v) for k, v in (disk.get("dipelajari") or {}).items()
                  if isinstance(v, list)}
    nama = st.session_state.get("user_name") or ""
    if nama:
        selesai[nama] = list(mem["selesai"].get(nama, []))
        dipelajari[nama] = list(mem["dipelajari"].get(nama, []))
    ids = {m.get("id") for m in mem["kustom"]}
    kustom = list(mem["kustom"]) + [
        m for m in (disk.get("kustom") or [])
        if isinstance(m, dict) and m.get("id") and m.get("id") not in ids]
    isi = {"versi": 1, "selesai": selesai, "dipelajari": dipelajari, "kustom": kustom}
    _tulis_json(KURIKULUM_FILE, isi)
    mem["selesai"] = {k: list(v) for k, v in selesai.items() if v}
    mem["dipelajari"] = {k: list(v) for k, v in dipelajari.items() if v}
    mem["kustom"] = kustom


def _semua_materi():
    _muat_kurikulum()
    return list(st.session_state["_kurikulum"]["kustom"]) + list(DAFTAR_MATERI)


def _materi_by_id(materi_id: str):
    for m in _semua_materi():
        if str(m.get("id")) == str(materi_id):
            return m
    return None


def _progres_materi():
    nama = st.session_state.get("user_name") or ""
    k = st.session_state["_kurikulum"]
    return set(k["selesai"].get(nama, [])), set(k["dipelajari"].get(nama, []))


def _mode_dari_kategori(kategori: str):
    return {"Iqro'": "Iqro'", "Tajwid": "Tahsin", "Tahfidz": "Tahfidz"}.get(kategori)


def _alasan_terkunci(mat, selesai):
    mode_kat = _mode_dari_kategori(mat.get("kategori"))
    kelas = kelas_siswa()
    if kelas is not None and mode_kat and mode_kat != kelas:
        return T(f"Materi ini khusus siswa Kelas {mode_kat}. Hubungi Pengelola "
                 "bila ingin pindah kelas.",
                 f"This material is for Class {mode_kat} students only. "
                 "Contact the Administrator to change class.",
                 f"هذه المادة مخصصة لطلاب فصل {mode_kat} فقط. تواصل مع المشرف "
                 "لتغيير الفصل.")
    if str(mat.get("id", "")).startswith("iqro") and not mat.get("kustom"):
        urut = [m["id"] for m in DAFTAR_MATERI if m.get("kategori") == "Iqro'"]
        if mat["id"] in urut:
            pos = urut.index(mat["id"])
            if pos > 0 and urut[pos - 1] not in selesai:
                return T(f"Selesaikan Iqro' Level {pos} dulu untuk membuka level ini.",
                         f"Finish Iqro' Level {pos} first to unlock this level.",
                         f"أكمل إقرأ المستوى {pos} أولاً لفتح هذا المستوى.")
    return None


def _tandai_dipelajari(materi_id: str):
    nama = st.session_state.get("user_name") or ""
    k = st.session_state["_kurikulum"]
    daftar = k["dipelajari"].setdefault(nama, [])
    if materi_id not in daftar:
        daftar.append(materi_id)
        _simpan_kurikulum()


def _selesaikan_materi(mat):
    nama = st.session_state.get("user_name") or ""
    k = st.session_state["_kurikulum"]
    selesai = k["selesai"].setdefault(nama, [])
    if mat["id"] not in selesai:
        selesai.append(mat["id"])
    dipelajari = k["dipelajari"].setdefault(nama, [])
    if mat["id"] in dipelajari:
        dipelajari.remove(mat["id"])
    if st.session_state.user_role == "Siswa":
        st.session_state.data.setdefault("hasil", []).append({
            "siswa": nama or st.session_state.data["profil"]["nama"],
            "tipe": "materi",
            "mode": mat.get("kategori") or "Iqro'",
            "level": int(mat.get("lv") or 1),
            "benar": 5,
            "total": 5,
            "skor": 100,
            "tanggal": datetime.now().strftime("%Y-%m-%d %H:%M"),
        })
        save_all_data()
    _simpan_kurikulum()
    st.session_state["mat_flash"] = T(
        f"Selamat! Materi “{mat['judul']}” selesai. Level berikutnya terbuka.",
        f"Well done! “{mat['judul']}” completed. The next level is unlocked.",
        f"أحسنت! أكملت “{mat['judul']}”. تم فتح المستوى التالي.")
    st.session_state["mat_balloons"] = True


def _ulangi_materi(mat):
    nama = st.session_state.get("user_name") or ""
    k = st.session_state["_kurikulum"]
    selesai = k["selesai"].setdefault(nama, [])
    if mat["id"] in selesai:
        selesai.remove(mat["id"])
    _tandai_dipelajari(mat["id"])
    _simpan_kurikulum()
    st.session_state["mat_flash"] = T(
        f"“{mat['judul']}” dibuka lagi sebagai Sedang Dipelajari.",
        f"“{mat['judul']}” reopened as In Progress.",
        f"أُعيد فتح “{mat['judul']}” كقيد الدراسة.")


def _berkas_materi(mat, jenis: str):
    for b in mat.get("berkas") or []:
        nama = str(b.get("rel") or "").lower()
        if nama.endswith(jenis):
            path = ASSETS / b["rel"]
            if path.exists():
                return path
    return None


def _kuis_dari_materi(mat):
    isi = " ".join(str(mat.get(k) or "") for k in
                   ("judul", "deskripsi", "arti", "contoh", "tips"))
    kuis = _buat_kuis(T(f"Kuis materi {mat['judul']}",
                        f"Quiz on {mat['judul']}",
                        f"اختبار مادة {mat['judul']}"), isi)
    soal = []
    for s in kuis.get("soal", []):
        if not s.get("options"):
            continue
        soal.append({
            "prompt": s["q"], "options": list(s["options"]), "answer": s["answer"],
            "bahas": s.get("bahas", ""), "arab": s.get("arab") or "",
            "level": max(1, min(MAX_LEVEL, int(mat.get("lv") or 1))),
        })
    return soal


def _mulai_kuis_materi(mat):
    soal = _kuis_dari_materi(mat)
    if not soal:
        return False
    mode_q = _mode_dari_kategori(mat.get("kategori")) or "Iqro'"
    level_q = int(mat.get("lv") or 1)
    peserta = _nama_peserta()
    rng = _rng_sesi(peserta, mode_q, level_q)
    soal = [acak_pilihan(s, rng) for s in soal]
    rng.shuffle(soal)
    xp_awal = st.session_state.data["progress"].get(mode_q, {"xp": 0}).get("xp", 0)
    st.session_state.quiz = {
        "id": datetime.now().strftime("%H%M%S%f"),
        "acak_id": rng.randint(1, 99999),
        "tipe": "ujian",
        "mode": mode_q,
        "level": level_q,
        "judul": mat["judul"],
        "peserta": peserta,
        "seed": _kode_sesi(peserta, mode_q, level_q),
        "mulai": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "selesai": None,
        "soal": soal,
        "idx": 0,
        "benar": 0,
        "picked": None,
        "finished": False,
        "xp_awal": xp_awal,
        "naik": False,
        "skor": 0,
        "batas": datetime.now() + timedelta(seconds=BATAS_UJIAN),
        "expired": False,
    }
    st.session_state.menu = "Ujian"
    return True


def _latih_materi(mat):
    mode = _mode_dari_kategori(mat.get("kategori"))
    st.session_state.menu = "Belajar & Game"
    if mode:
        mulai_sesi("game", mode, max(1, min(MAX_LEVEL, int(mat.get("lv") or 1))))


def _tanya_ai_materi(mat):
    st.session_state["ai_prompt_awal"] = T(
        f"Jelaskan tentang materi {mat['judul']} ini",
        f"Explain this material: {mat['judul']}",
        f"اشرح لي هذه المادة: {mat['judul']}")
    st.session_state.menu = "AI Assistant"


def _simpan_upload_materi(daftar):
    hasil = []
    if not daftar:
        return hasil
    MATERI_ASSET_DIR.mkdir(parents=True, exist_ok=True)
    for berkas in daftar:
        ext = Path(berkas.name).suffix.lower()
        slug = _slug_nama(Path(berkas.name).stem)[:40]
        nama_file = f"{datetime.now():%Y%m%d%H%M%S}_{slug}{ext}"
        (MATERI_ASSET_DIR / nama_file).write_bytes(berkas.getbuffer())
        hasil.append({"nama": berkas.name, "rel": f"materi/{nama_file}"})
    return hasil


def _tambah_materi_guru():
    label_kat = {k: _bahasa_nama_kategori(k) for k in KATEGORI_MATERI}
    with st.expander("➕ " + T("Tambah Materi Baru (Guru)",
                              "Add New Material (Teacher)",
                              "إضافة مادة جديدة (المعلم)")):
        with st.form("form_materi_baru", clear_on_submit=True):
            judul = st.text_input(T("Judul materi", "Material title", "عنوان المادة"))
            k1, k2, k3 = st.columns(3)
            kategori = k1.selectbox(
                T("Kategori", "Category", "الفئة"), KATEGORI_MATERI,
                format_func=lambda k: label_kat[k])
            level = k2.selectbox(T("Level", "Level", "المستوى"), TINGKAT_MATERI)
            durasi = k3.number_input(T("Durasi (menit)", "Duration (minutes)",
                                       "المدة (دقيقة)"),
                                     min_value=5, max_value=180, value=15, step=5)
            deskripsi = st.text_area(T("Deskripsi", "Description", "الوصف"), height=70)
            arab = st.text_area(T("Huruf / Ayat Arab", "Arabic letters / verse",
                                  "الحروف / الآية"), height=70)
            l1, l2 = st.columns(2)
            latin = l1.text_input(T("Latin", "Latin", "اللاتينية"))
            arti = l2.text_input(T("Arti", "Meaning", "المعنى"))
            contoh = st.text_input(T("Contoh kata", "Example", "مثال"))
            video = st.text_input(T("Link video YouTube (opsional)",
                                    "YouTube video link (optional)",
                                    "رابط فيديو يوتيوب (اختياري)"))
            tips = st.text_area(T("Tips guru", "Teacher tips", "نصائح المعلم"), height=70)
            unggah = st.file_uploader(
                T("Upload PDF / Gambar / Audio (bisa lebih dari satu)",
                  "Upload PDF / Image / Audio (multiple allowed)",
                  "رفع PDF / صورة / صوت (يمكن تعدد الملفات)"),
                type=["pdf", "png", "jpg", "jpeg", "mp3", "wav"], accept_multiple_files=True)
            simpan = st.form_submit_button(
                "💾 " + T("Simpan Materi", "Save Material", "حفظ المادة"),
                type="primary", use_container_width=True)
        if simpan:
            if not judul.strip():
                st.error(T("Judul materi wajib diisi.", "Material title is required.",
                           "عنوان المادة مطلوب."))
                return
            berkas = _simpan_upload_materi(unggah)
            mat = {
                "id": "kustom_" + datetime.now().strftime("%Y%m%d%H%M%S%f"),
                "kategori": kategori, "judul": judul.strip(),
                "deskripsi": deskripsi.strip(), "durasi": int(durasi),
                "level": level, "lv": 1, "huruf": arab.strip(),
                "latin": latin.strip(), "arti": arti.strip(),
                "contoh": contoh.strip(), "video": video.strip(),
                "makhraj": "", "tips": tips.strip(), "surah": None,
                "kustom": True, "berkas": berkas,
            }
            st.session_state["_kurikulum"]["kustom"].insert(0, mat)
            _simpan_kurikulum()
            st.session_state["mat_flash"] = T(
                f"Materi baru “{mat['judul']}” berhasil disimpan.",
                f"New material “{mat['judul']}” saved successfully.",
                f"تم حفظ المادة الجديدة “{mat['judul']}”.")
            st.session_state["mat_balloons"] = True
            st.rerun()


def _kartu_materi(mat, status, selesai):
    mid = mat["id"]
    kat = _bahasa_nama_kategori(mat.get("kategori") or "")
    label_status = {
        "belum": T("Belum Mulai", "Not Started", "لم يبدأ"),
        "sedang": T("Sedang Dipelajari", "In Progress", "قيد الدراسة"),
        "selesai": T("Selesai ✅", "Completed ✅", "مكتمل ✅"),
    }[status]
    warna_status = {"belum": "", "sedang": "kuning", "selesai": "hijau"}[status]
    st.markdown(
        '<div class="mk-chips">'
        f'<span class="mk-chip">{opsi_aman(kat)}</span>'
        f'<span class="mk-chip">{T("Level", "Level", "المستوى")}: '
        f'{opsi_aman(str(mat.get("level") or "-"))}</span>'
        f'<span class="mk-chip">⏱️ {int(mat.get("durasi") or 0)} '
        f'{T("menit", "min", "دقيقة")}</span>'
        f'<span class="mk-chip {warna_status}">{label_status}</span>'
        '</div>', unsafe_allow_html=True)
    st.progress({"belum": 0.0, "sedang": 0.5, "selesai": 1.0}[status],
                text=T("Status: ", "Status: ", "الحالة: ") + label_status)
    if mat.get("deskripsi"):
        st.markdown(f"*{opsi_aman(mat['deskripsi'])}*")
    if mat.get("huruf"):
        st.markdown(f'<div class="mk-arab" dir="rtl">{opsi_aman(mat["huruf"])}</div>',
                    unsafe_allow_html=True)
    if mat.get("latin"):
        st.markdown(f'<div class="mk-latin"><b>{T("Latin", "Latin", "اللاتينية")}:</b> '
                    f'{opsi_aman(mat["latin"])}</div>', unsafe_allow_html=True)
    if mat.get("arti"):
        st.markdown(f'<div class="mk-arti"><b>{T("Arti", "Meaning", "المعنى")}:</b> '
                    f'{opsi_aman(mat["arti"])}</div>', unsafe_allow_html=True)
    if mat.get("contoh"):
        st.markdown(f'<div class="mk-box mk-kuning">💡 <b>'
                    f'{T("Contoh Kata", "Example", "مثال")}:</b> '
                    f'{opsi_aman(mat["contoh"])}</div>', unsafe_allow_html=True)
    if mat.get("makhraj") and mat.get("kategori") == "Tajwid":
        st.markdown(f'<div class="mk-box mk-biru">🦷 <b>{T("Makhraj", "Makhraj", "المخرج")}:</b> '
                    f'{opsi_aman(mat["makhraj"])}</div>' + _makhraj_svg(),
                    unsafe_allow_html=True)
    gambar = _berkas_materi(mat, (".png", ".jpg", ".jpeg"))
    if gambar is not None:
        st.image(str(gambar), caption=T("Gambar Makhraj / Materi",
                                        "Makhraj / material image",
                                        "صورة المخرج / المادة"))
    if mat.get("tips"):
        st.markdown(f'<div class="mk-box mk-hijau">🧑‍🏫 <b>{T("Tips Guru", "Teacher Tips",
                                                                  "نصائح المعلم")}:</b> '
                    f'{opsi_aman(mat["tips"])}</div>', unsafe_allow_html=True)
    if mat.get("video"):
        st.markdown(f"**🎬 {T('Video Cara Pengucapan', 'Pronunciation Video',
                              'فيديو النطق')}**")
        st.video(mat["video"])
    for i, b in enumerate(mat.get("berkas") or []):
        path = ASSETS / str(b.get("rel") or "")
        if not path.exists():
            continue
        nama = str(b.get("nama") or path.name)
        if path.suffix.lower() == ".pdf":
            try:
                st.download_button("📄 " + nama, path.read_bytes(), file_name=nama,
                                   mime="application/pdf",
                                   key=f"mk_file_{mid}_{i}")
            except Exception:
                st.caption("📄 " + nama)
        elif path.suffix.lower() in (".mp3", ".wav"):
            st.audio(str(path))
            st.caption("🎧 " + nama)

    st.write("")
    b1, b2, b3 = st.columns(3)
    with b1:
        if st.button("🔊 " + T("Dengarkan", "Listen", "استمع"),
                     key=f"mk_dengar_{mid}", use_container_width=True):
            _tandai_dipelajari(mid)
            surah = mat.get("surah")
            if surah:
                nama_qori, url = audio_qori(qori_terpilih(), int(surah))
                st.audio(url, autoplay=True)
                st.caption("🎧 " + nama_qori + " · " + T(
                    "Sesuai Pengaturan > Suara Qori",
                    "From Settings > Qori Voice",
                    "حسب الإعدادات > صوت القارئ"))
            else:
                audio_berkas = _berkas_materi(mat, (".mp3", ".wav"))
                if audio_berkas is not None:
                    st.audio(str(audio_berkas), autoplay=True)
                else:
                    teks = " . ".join(filter(None, [
                        str(mat.get("huruf") or ""), str(mat.get("latin") or ""),
                        str(mat.get("arti") or ""), str(mat.get("contoh") or "")]))
                    audio = _tts_google(_bersihkan_tts(teks), _bahasa_tts(teks)) if teks else b""
                    if audio:
                        st.audio(audio, format="audio/mpeg", autoplay=True)
                        st.caption(T("Dibacakan dengan TTS. Murottal surah memakai "
                                     "Qori pilihan di Pengaturan.",
                                     "Read with TTS. Surah recitation uses the Qori "
                                     "selected in Settings.",
                                     "قُرئ بصوت اصطناعي. تلاوة السور تستخدم القارئ "
                                     "المختار في الإعدادات."))
                    else:
                        st.warning(T("Audio belum bisa dimuat. Periksa koneksi internet.",
                                     "Audio could not be loaded. Check your connection.",
                                     "تعذر تحميل الصوت. تحقق من الاتصال."))
    with b2:
        if st.button("✍️ " + T("Latih Level Ini", "Practice This Level",
                              "تدرب على هذا المستوى"),
                     key=f"mk_latih_{mid}", use_container_width=True):
            _tandai_dipelajari(mid)
            _latih_materi(mat)
    with b3:
        if st.button("📝 " + T("Kuis Level Ini", "Quiz This Level",
                              "اختبار هذا المستوى"),
                     key=f"mk_kuis_{mid}", use_container_width=True):
            _tandai_dipelajari(mid)
            if _mulai_kuis_materi(mat):
                st.rerun()
            else:
                st.warning(T("Soal kuis belum bisa disusun. Coba lagi.",
                             "Quiz questions could not be created. Try again.",
                             "تعذر إعداد أسئلة الاختبار. حاول مرة أخرى."))
    b4, b5 = st.columns(2)
    with b4:
        if st.button("❓ " + T("Tanya AI tentang materi ini",
                              "Ask AI about this material",
                              "اسأل الذكاء الاصطناعي عن هذه المادة"),
                     key=f"mk_ai_{mid}", use_container_width=True):
            _tandai_dipelajari(mid)
            _tanya_ai_materi(mat)
            st.rerun()
    with b5:
        if status == "selesai":
            if st.button("🔁 " + T("Sudah Selesai · Ulangi Lagi",
                                  "Completed · Review Again",
                                  "مكتمل · أعد الدراسة"),
                         key=f"mk_ulang_{mid}", use_container_width=True):
                _ulangi_materi(mat)
                st.rerun()
        else:
            if st.button("✅ " + T("Tandai Selesai", "Mark as Completed",
                                  "ضع علامة مكتمل"),
                         key=f"mk_selesai_{mid}", type="primary",
                         use_container_width=True):
                _selesaikan_materi(mat)
                st.rerun()


def page_materi():
    st.markdown(f"""
    <div class="hero-small">
      <h2>📚 {T("Materi Pembelajaran", "Learning Materials", "المواد التعليمية")}</h2>
      <p>{T("Jelajahi materi Iqro', Tajwid & Tahfidz",
           "Explore Iqro, Tajweed & Tahfidz materials",
           "استكشف مواد إقرأ والتجويد والتحفيظ")}</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(_CSS_MATERI, unsafe_allow_html=True)
    if st.session_state.get("mat_flash"):
        st.success(st.session_state.pop("mat_flash"))
    if st.session_state.pop("mat_balloons", False):
        st.balloons()

    semua = _semua_materi()
    selesai, dipelajari = _progres_materi()
    total = len(semua)
    jumlah = sum(1 for m in semua if m["id"] in selesai)
    persen = round(jumlah / total * 100) if total else 0
    st.progress(jumlah / total if total else 0.0,
                text=f"{jumlah}/{total} · {persen}%")
    st.markdown("**✅ " + T(
        f"Kamu sudah menyelesaikan {jumlah} dari {total} Materi · {persen}%",
        f"You have completed {jumlah} of {total} materials · {persen}%",
        f"أكملت {jumlah} من {total} مواد · {persen}%") + "**")

    f1, f2, f3 = st.columns([1.6, 2, 1.4])
    label_kat = {"Semua": T("Semua", "All", "الكل")}
    label_kat.update({k: _bahasa_nama_kategori(k) for k in KATEGORI_MATERI})
    with f1:
        kategori = st.selectbox(
            T("Kategori materi", "Material category", "فئة المادة"),
            ["Semua"] + KATEGORI_MATERI, format_func=lambda k: label_kat[k],
            key="mat_filter_kategori")
    with f2:
        cari = st.text_input(T("🔍 Cari Materi...", "🔍 Search Materials...",
                               "🔍 ابحث في المواد..."), key="mat_cari")
    label_status = {
        "Semua": T("Semua Status", "All Status", "كل الحالات"),
        "belum": T("Belum Mulai", "Not Started", "لم يبدأ"),
        "sedang": T("Sedang Dipelajari", "In Progress", "قيد الدراسة"),
        "selesai": T("Selesai ✅", "Completed ✅", "مكتمل ✅"),
    }
    with f3:
        status_filter = st.selectbox(
            T("Status", "Status", "الحالة"), list(label_status),
            format_func=lambda s: label_status[s], key="mat_filter_status")

    tampil = []
    for mat in semua:
        if kategori != "Semua" and mat.get("kategori") != kategori:
            continue
        teks = " ".join(str(mat.get(k) or "") for k in ("judul", "deskripsi", "arti"))
        if cari and cari.lower() not in teks.lower():
            continue
        status = ("selesai" if mat["id"] in selesai else
                  "sedang" if mat["id"] in dipelajari else "belum")
        if status_filter != "Semua" and status != status_filter:
            continue
        tampil.append((mat, status))
    st.caption(T(f"Menampilkan {len(tampil)} materi.",
                 f"Showing {len(tampil)} materials.",
                 f"عرض {len(tampil)} مادة."))
    if not tampil:
        st.info(T("Tidak ada materi yang cocok dengan filter. Coba kata kunci lain.",
                  "No materials match the filter. Try another keyword.",
                  "لا توجد مواد مطابقة للتصفية. جرّب كلمة أخرى."))

    for mat, status in tampil:
        alasan = _alasan_terkunci(mat, selesai)
        if alasan:
            judul = "🔒 " + mat["judul"]
        elif status == "selesai":
            judul = "✅ " + mat["judul"]
        else:
            judul = ("📖 " if status == "sedang" else "") + mat["judul"]
        judul += f"  ·  ⏱️ {int(mat.get('durasi') or 0)} " + T("menit", "min", "دقيقة")
        with st.expander(judul):
            if alasan:
                st.info(alasan)
                continue
            _kartu_materi(mat, status, selesai)

    catatan = [(mode, lvl, MATERI[mode][lvl]) for mode in MODE_LIST
               for lvl in range(1, MAX_LEVEL + 1)
               if "QORI AI" in str(MATERI[mode].get(lvl, ""))]
    if catatan:
        with st.expander("📥 " + T("Catatan Materi dari QORI AI",
                                   "Materials Saved from QORI AI",
                                   "مواد محفوظة من QORI AI")):
            for mode, lvl, isi in catatan:
                st.markdown(f"**{MODE_ICON[mode]} {mode} · Level {lvl}**")
                st.markdown(f'<div class="materi-box">{isi}</div>', unsafe_allow_html=True)

    if st.session_state.user_role in ("Pengelola", "Guru"):
        _tambah_materi_guru()
    if st.session_state.user_role == "Siswa":
        st.caption(T("Tandai Selesai pada materi akan menambahkan catatan ke Nilai & Hasil.",
                     "Marking a material as completed adds a record to Scores & Results.",
                     "وضع علامة مكتمل يضيف سجلًا إلى الدرجات والنتائج."))

# ---------------------------------------------------------------------------
# Al-Qur'an Juz 30
# ---------------------------------------------------------------------------
@st.cache_data(ttl=86400, show_spinner=False)
def ambil_surah(nomor: int):
    try:
        req = Request(
            f"https://equran.id/api/v2/surat/{nomor}",
            headers={"User-Agent": "QORI-AI/1.0"},
        )
        with urlopen(req, timeout=8) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
        if payload.get("code") == 200:
            return payload["data"]
    except Exception:
        return None
    return None


def page_quran():
    st.markdown(f"""
    <div class="hero-small">
      <h2>📖 {T("Al-Qur'an Digital – Juz 30", "Digital Qur'an – Juz 30", "القرآن الرقمي – الجزء ٣٠")}</h2>
      <p>{T("37 surah Juz 30 lengkap dengan teks Arab, terjemahan, dan audio murottal.",
           "All 37 surahs of Juz 30 with Arabic text, translation, and murottal audio.",
           "٣٧ سورة من الجزء ٣٠ مع النص العربي والترجمة والتلاوة الصوتية.")}</p>
    </div>
    """, unsafe_allow_html=True)
    kata_ayat = T("ayat", "verses", "آية")
    opsi = [f"{no} · {nama} ({ayat} {kata_ayat})" for no, nama, ayat, _ in SURAH_JUZ30]
    pilihan = st.selectbox(T("Pilih surah", "Choose surah", "اختر السورة"), opsi,
                           key="quran_surah_terakhir")
    nomor = int(pilihan.split("·")[0].strip())
    nama, jumlah, arti = SURAH_INFO[nomor]
    st.markdown(f"""
    <div class="meta-card">
      <b style="font-size:18px;color:#102448">{nama}</b>
      <span class="small-muted"> · {arti} · {jumlah} ayat · Juz 30</span>
    </div>
    """, unsafe_allow_html=True)

    data = ambil_surah(nomor)
    sumber = "equran.id"
    if not data:
        lokal = FALLBACK_SURAH.get(nomor)
        if not lokal:
            st.warning("Teks surah belum tersedia offline dan koneksi internet tidak aktif. Coba muat ulang.")
            return
        data = {
            "ayat": [
                {"nomorAyat": i + 1, "teksArab": arab, "teksIndonesia": terjemah, "teksLatin": ""}
                for i, (arab, terjemah) in enumerate(lokal)
            ]
        }
        sumber = "data lokal"

    pilihan_qori = qori_terpilih()
    nama_qori, url_audio = audio_qori(pilihan_qori, nomor)
    st.markdown(
        "🎙️ *" + T("Qori Aktif:", "Active Qori:", "القارئ النشط:")
        + f"* {nama_qori} | "
        + T("Sesuai Pengaturan > Suara Qori | ",
            "From Settings > Qori Voice | ",
            "حسب الإعدادات > صوت القارئ | ")
        + T("[Ganti di Pengaturan]", "[Change in Settings]", "[التغيير في الإعدادات]")
    )
    st.audio(url_audio)
    tampil_latin = st.toggle(
        T("Tampilkan transliterasi latin", "Show Latin transliteration",
          "عرض النقل الصوتي اللاتيني"),
        value=False)

    ayat_html = []
    for ayah in data["ayat"]:
        latin = ayah.get("teksLatin", "")
        latin_html = f'<div class="ayah-latin">{opsi_aman(latin)}</div>' if (tampil_latin and latin) else ""
        ayat_html.append(
            f'<div class="ayah">'
            f'<span class="ayah-no">{ayah["nomorAyat"]}</span>'
            f'<div class="ayah-arab">{ayah["teksArab"]}</div>'
            f'<p class="ayah-terjemah">{opsi_aman(ayah.get("teksIndonesia", ""))}</p>{latin_html}'
            f'</div>'
        )
    st.markdown(
        f'<div class="meta-card">{"".join(ayat_html)}</div>',
        unsafe_allow_html=True,
    )
    st.caption(f"Sumber teks: {sumber}. Terjemahan: Kementerian Agama RI.")

# ---------------------------------------------------------------------------
# Data Siswa
# ---------------------------------------------------------------------------
SISWA_PEREMPUAN_AWAL = {
    "FRISCHA BUNGA LESTARI",
    "ZALFATUSSYIFA RAMADANTI",
    "ZAIN RAHMANITA",
    "ANGGI RATU MAHADEWI",
    "KAWILUJEUNGAN RASYIDA RAIHANUN",
    "MIFTAHUL JANNAH",
    "ROSMALATI KHOLISHA",
}


def jenis_kelamin_tampil(row):
    nilai = str(row.get("jenis_kelamin") or "").strip()
    if nilai in ("Laki-laki", "Perempuan"):
        return nilai
    nama = str(row.get("nama") or "").strip().upper()
    return "Perempuan" if nama in SISWA_PEREMPUAN_AWAL else "Laki-laki"



SISWA_STATUS_OPSI = ["Aktif", "Tidak Aktif", "Lulus", "Pindah"]
SISWA_LEVEL_OPSI = ["Jilid 1", "Jilid 2", "Jilid 3", "Jilid 4", "Jilid 5",
                    "Jilid 6", "Al-Qur'an"]
SISWA_EKSTRA_DEFAULT = {
    "nis": "", "tanggal_lahir": "", "no_hp_ortu": "", "alamat": "",
    "level_iqro": "", "surah_terakhir": "", "jumlah_hafalan": "",
    "nilai_tahsin": 0, "nilai_tahfidz": 0,
    "hadir": 0, "izin": 0, "alpa": 0,
    "status_siswa": "Aktif", "status_santri": "", "guru_pembimbing": "", "tanggal_masuk": "",
    "catatan_guru": "", "foto": "",
}


def _tanggal_ke_teks(nilai) -> str:
    try:
        return nilai.strftime("%Y-%m-%d")
    except Exception:
        return ""


def _tanggal_obj(nilai):
    try:
        return datetime.strptime(str(nilai or "").strip(), "%Y-%m-%d").date()
    except Exception:
        return None


def _umur_siswa(nilai) -> str:
    lahir = _tanggal_obj(nilai)
    if lahir is None:
        return ""
    hari = datetime.now().date()
    return str(hari.year - lahir.year
               - ((hari.month, hari.day) < (lahir.month, lahir.day)))


def _lengkapi_siswa():
    siswa = st.session_state.data.setdefault("siswa", [])
    berubah = False
    for s in siswa:
        for kunci, nilai in SISWA_EKSTRA_DEFAULT.items():
            if kunci not in s:
                s[kunci] = nilai
                berubah = True
        if not s.get("jenis_kelamin"):
            s["jenis_kelamin"] = jenis_kelamin_tampil(s)
            berubah = True
    if berubah:
        save_all_data()
    return siswa


def _foto_data_uri_dari_nilai(nilai) -> str:
    """Normalisasi foto dari data URI, bytes, atau path lama menjadi data URI."""
    if isinstance(nilai, dict):
        data = nilai.get("data")
        mime = nilai.get("mime") or "image/jpeg"
        if isinstance(data, str) and data.startswith("data:"):
            return data
        if isinstance(data, str):
            try:
                base64.b64decode(data, validate=False)
                return f"data:{mime};base64,{data}"
            except Exception:
                return ""
        if isinstance(data, (bytes, bytearray)):
            return f"data:{mime};base64," + base64.b64encode(bytes(data)).decode("ascii")
        return ""
    rel = str(nilai or "").strip()
    if rel.startswith("data:image/"):
        return rel
    if rel:
        path = ASSETS / rel
        try:
            if path.exists():
                mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
                return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode("ascii")
        except Exception:
            pass
    return ""


def _foto_siswa_uri(rel) -> str:
    return _foto_data_uri_dari_nilai(rel)


def _kompres_foto_upload(berkas, batas_byte: int = 300 * 1024) -> dict:
    """Resize maksimal 300x300 dan kompres JPEG sampai ukuran <= 300 KB."""
    if berkas is None:
        return {}
    import io as _io
    try:
        from PIL import Image, ImageOps
        gambar = Image.open(_io.BytesIO(berkas.getvalue()))
        gambar = ImageOps.exif_transpose(gambar).convert("RGB")
        gambar.thumbnail((300, 300), getattr(Image, "Resampling", Image).LANCZOS)
        kualitas = 88
        hasil = _io.BytesIO()
        gambar.save(hasil, format="JPEG", quality=kualitas, optimize=True)
        while hasil.tell() > batas_byte and kualitas > 35:
            kualitas -= 7
            hasil = _io.BytesIO()
            gambar.save(hasil, format="JPEG", quality=kualitas, optimize=True)
        if hasil.tell() > batas_byte:
            raise ValueError("Foto tidak dapat dikompres hingga maksimal 300 KB.")
        data = hasil.getvalue()
        return {"data": data, "mime": "image/jpeg",
                "data_uri": "data:image/jpeg;base64," + base64.b64encode(data).decode("ascii")}
    except ImportError as exc:
        raise RuntimeError("Paket Pillow diperlukan untuk kompresi foto profil.") from exc


def _simpan_foto_siswa(nama: str, berkas) -> str:
    """Simpan foto siswa sebagai data URI agar ikut tersimpan di JSON dan Supabase."""
    if berkas is None:
        return ""
    hasil = _kompres_foto_upload(berkas)
    return hasil["data_uri"]


def _foto_id_siswa(record=None, nama=None) -> str:
    record = record or {}
    if not record and nama:
        target = rapikan_nama(str(nama)).casefold()
        record = next((x for x in st.session_state.data.get("siswa", [])
                       if rapikan_nama(str(x.get("nama") or "")).casefold() == target), {})
    identitas = (record.get("id") or record.get("nis") or record.get("nisn")
                 or record.get("nama") or nama or "siswa")
    return re.sub(r"[^A-Za-z0-9_-]+", "_", str(identitas).strip())


def _app_settings_merge(user_id: str, perubahan: dict) -> tuple[bool, str | None]:
    """Tandai perubahan foto di state; snapshot global menyimpannya pada akhir rerun."""
    backup = st.session_state.setdefault("foto_profil_backup", {})
    for key, value in (perubahan or {}).items():
        if not str(key).startswith("foto_profil_"):
            continue
        if value:
            backup[str(key)] = value
        else:
            backup.pop(str(key), None)
    return True, None

def _user_settings_id() -> str:
    role = str(st.session_state.get("user_role") or "pengguna").strip().casefold()
    nama = str(st.session_state.get("user_name") or "anonim").strip().casefold()
    return f"{role}:{nama}"


def _simpan_foto_profil_permanen(kunci: str, foto: dict, *, untuk_siswa: bool = False) -> tuple[bool, str | None]:
    """Simpan foto terkompresi ke state; autosave global menulisnya ke Supabase saat rerun."""
    if not foto or not foto.get("data"):
        return False, "Data foto kosong."
    data_uri = foto.get("data_uri") or (
        "data:" + str(foto.get("mime") or "image/jpeg") + ";base64," +
        base64.b64encode(foto["data"]).decode("ascii"))
    st.session_state.setdefault("foto_profil_backup", {})[kunci] = data_uri
    return True, None

def _muat_foto_profil_supabase():
    """Tampilkan foto dari snapshot global; fallback baca foto lama untuk migrasi tanpa mengubah jam."""
    marker = _user_settings_id()
    if st.session_state.get("_foto_supabase_loaded_for") == marker:
        return
    st.session_state["_foto_supabase_loaded_for"] = marker
    backup = st.session_state.setdefault("foto_profil_backup", {})
    # Snapshot global biasanya sudah memulihkan backup foto ke Session State.
    if not backup:
        client, _error = get_supabase_client()
        if client is not None:
            user_ids = [marker, "pengelola:kendar sultoni"]
            try:
                for uid in dict.fromkeys(user_ids):
                    hasil = (client.table("app_settings").select("settings")
                             .eq("user_id", uid).limit(1).execute())
                    rows = getattr(hasil, "data", None) or []
                    if rows and isinstance(rows[0].get("settings"), dict):
                        for key, value in rows[0]["settings"].items():
                            if str(key).startswith("foto_profil_") and isinstance(value, str) and value.startswith("data:image/"):
                                backup.setdefault(key, value)
            except Exception as exc:
                st.session_state["_foto_supabase_load_error"] = str(exc)
    for key, value in backup.items():
        if not isinstance(value, str) or not value.startswith("data:image/"):
            continue
        try:
            raw = base64.b64decode(value.split(",", 1)[1])
        except Exception:
            continue
        if key == "foto_profil_pengelola" and st.session_state.get("user_role") == "Pengelola":
            nama = st.session_state.get("user_name") or "Kendar Sultoni"
            st.session_state.setdefault("foto_profil", {})[nama] = {"data": raw, "mime": "image/jpeg"}
        elif key.startswith("foto_profil_siswa_"):
            sid = key[len("foto_profil_siswa_"):]
            for siswa_rec in st.session_state.data.get("siswa", []):
                if _foto_id_siswa(siswa_rec) == sid:
                    siswa_rec["foto"] = value
                    break
            if st.session_state.get("user_role") == "Siswa":
                nama_login = rapikan_nama(str(st.session_state.get("user_name") or "")).casefold()
                rec = next((x for x in st.session_state.data.get("siswa", [])
                            if rapikan_nama(str(x.get("nama") or "")).casefold() == nama_login), None)
                if rec and _foto_id_siswa(rec) == sid:
                    st.session_state.setdefault("foto_profil", {})[st.session_state.user_name] = {"data": raw, "mime": "image/jpeg"}
    # Hydrasi foto dari baris lama bukan perubahan pengguna; jangan ubah timestamp.
    if "_qori_buat_snapshot" in globals():
        st.session_state["_qori_global_signature"] = _qori_signature_snapshot(_qori_buat_snapshot())

def _hapus_foto_siswa(rel):
    rel = str(rel or "").strip()
    if not rel:
        return
    try:
        (ASSETS / rel).unlink(missing_ok=True)
    except Exception:
        pass


def _simpan_siswa_lokal(record, before_nama=None):
    siswa = st.session_state.data.setdefault("siswa", [])
    kunci = rapikan_nama(str(before_nama or record.get("nama") or "")).lower()
    for s in siswa:
        if rapikan_nama(str(s.get("nama") or "")).lower() == kunci:
            s.update(record)
            break
    else:
        siswa.append(dict(record))
    save_all_data()


def _hapus_siswa_lokal(nama):
    kunci = rapikan_nama(str(nama or "")).lower()
    siswa = st.session_state.data.setdefault("siswa", [])
    st.session_state.data["siswa"] = [
        s for s in siswa
        if rapikan_nama(str(s.get("nama") or "")).lower() != kunci
    ]
    save_all_data()


def _nis_bentrok(nis, kecuali_nama=None) -> bool:
    nis = str(nis or "").strip().lower()
    if not nis:
        return False
    kunci = rapikan_nama(str(kecuali_nama or "")).lower()
    for s in st.session_state.data.get("siswa", []):
        if rapikan_nama(str(s.get("nama") or "")).lower() == kunci:
            continue
        if str(s.get("nis") or "").strip().lower() == nis:
            return True
    return False


def _validasi_siswa(record, kecuali_nama=None):
    if not str(record.get("nama") or "").strip():
        return T("Nama lengkap wajib diisi.", "Full name is required.",
                 "الاسم الكامل مطلوب.")
    if not str(record.get("nis") or "").strip():
        return T("NIS / NISN wajib diisi.", "NIS / NISN is required.",
                 "الرقم الوطني مطلوب.")
    if _nis_bentrok(record.get("nis"), kecuali_nama):
        return T("NIS / NISN sudah dipakai siswa lain.",
                 "This NIS / NISN is already used by another student.",
                 "الرقم الوطني مستخدم لطالب آخر.")
    for kunci, label in (("tanggal_lahir", T("Tanggal lahir", "Date of birth",
                                             "تاريخ الميلاد")),
                         ("tanggal_masuk", T("Tanggal masuk", "Entry date",
                                             "تاريخ الالتحاق"))):
        if record.get(kunci) and _tanggal_obj(record[kunci]) is None:
            return (label + T(" harus berformat YYYY-MM-DD.",
                              " must use YYYY-MM-DD format.",
                              " يجب أن يكون بصيغة YYYY-MM-DD."))
    return None


def _rekam_dari_isian(isian, foto=""):
    return {
        "nama": rapikan_nama(str(isian.get("nama") or "").strip()),
        "nis": str(isian.get("nis") or "").strip(),
        "jenis_kelamin": isian.get("jenis_kelamin") or "Laki-laki",
        "kelas": str(isian.get("kelas") or "").strip(),
        "program": str(isian.get("program") or MODE_LIST[0]),
        "tanggal_lahir": str(isian.get("tanggal_lahir") or "").strip(),
        "no_hp_ortu": str(isian.get("no_hp_ortu") or "").strip(),
        "alamat": str(isian.get("alamat") or "").strip(),
        "level_iqro": str(isian.get("level_iqro") or "").strip(),
        "surah_terakhir": str(isian.get("surah_terakhir") or "").strip(),
        "jumlah_hafalan": str(isian.get("jumlah_hafalan") or "").strip(),
        "nilai_tahsin": int(isian.get("nilai_tahsin") or 0),
        "nilai_tahfidz": int(isian.get("nilai_tahfidz") or 0),
        "hadir": int(isian.get("hadir") or 0),
        "izin": int(isian.get("izin") or 0),
        "alpa": int(isian.get("alpa") or 0),
        "status_siswa": isian.get("status_siswa") or SISWA_STATUS_OPSI[0],
        "guru_pembimbing": str(isian.get("guru_pembimbing") or "").strip(),
        "tanggal_masuk": str(isian.get("tanggal_masuk") or "").strip(),
        "catatan_guru": str(isian.get("catatan_guru") or "").strip(),
        "foto": foto,
    }


def _xlsx_bytes(header, rows) -> bytes:
    import io as _io
    import zipfile
    from xml.sax.saxutils import escape

    def kolom(i):
        hasil = ""
        i += 1
        while i:
            i, sisa = divmod(i - 1, 26)
            hasil = chr(65 + sisa) + hasil
        return hasil

    def sel(r, c, nilai):
        ref = f"{kolom(c)}{r}"
        if isinstance(nilai, (int, float)) and not isinstance(nilai, bool):
            return f'<c r="{ref}"><v>{nilai}</v></c>'
        teks = escape(str("" if nilai is None else nilai))
        return f'<c r="{ref}" t="inlineStr"><is><t xml:space="preserve">{teks}</t></is></c>'

    semua = [list(header)] + [list(r) for r in rows]
    baris_xml = []
    for r, baris in enumerate(semua, start=1):
        baris_xml.append(f'<row r="{r}">'
                         + "".join(sel(r, c, v) for c, v in enumerate(baris))
                         + "</row>")
    sheet = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        "<sheetData>" + "".join(baris_xml) + "</sheetData></worksheet>"
    )
    content_types = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
        '<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>'
        "</Types>"
    )
    rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
        "</Relationships>"
    )
    workbook = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        '<sheets><sheet name="Data Siswa" sheetId="1" r:id="rId1"/></sheets></workbook>'
    )
    wb_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>'
        '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
        "</Relationships>"
    )
    styles = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        '<fonts count="1"><font><sz val="11"/><name val="Calibri"/></font></fonts>'
        '<fills count="1"><fill><patternFill patternType="none"/></fill></fills>'
        '<borders count="1"><border/></borders><cellStyleXfs count="1"><xf/></cellStyleXfs>'
        '<cellXfs count="1"><xf/></cellXfs></styleSheet>'
    )
    buffer = _io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types)
        z.writestr("_rels/.rels", rels)
        z.writestr("xl/workbook.xml", workbook)
        z.writestr("xl/_rels/workbook.xml.rels", wb_rels)
        z.writestr("xl/styles.xml", styles)
        z.writestr("xl/worksheets/sheet1.xml", sheet)
    return buffer.getvalue()


def _pdf_bytes(judul, header, rows, landscape=False, footer=None) -> bytes:
    def bersih(nilai):
        teks = str("" if nilai is None else nilai)
        teks = teks.encode("latin-1", "replace").decode("latin-1")
        return teks.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")

    if landscape:
        lebar = (4, 26, 9, 9, 5, 6, 6, 7, 9, 5, 7, 9, 11)
        lebar_hal, tinggi_hal = 842, 595
        x_teks, y_judul, y_tabel, per_halaman = 24, 560, 538, 40
    else:
        lebar = (4, 24, 10, 8, 9, 9, 6, 7, 10)
        lebar_hal, tinggi_hal = 595, 842
        x_teks, y_judul, y_tabel, per_halaman = 40, 805, 782, 46

    def baris_teks(kolom):
        potong = [str(v if v is not None else "")[:w].ljust(w)
                  for v, w in zip(list(kolom) + [""] * len(lebar), lebar)]
        return " ".join(potong)

    semua = [baris_teks(header)] + [baris_teks(r) for r in rows]
    halaman = [semua[i:i + per_halaman]
               for i in range(0, len(semua), per_halaman)] or [semua]

    objek = []
    for idx, daftar in enumerate(halaman):
        nomor_hal = 4 + 2 * idx
        nomor_isi = 5 + 2 * idx
        isi = ["BT", "/F1 9 Tf", f"{x_teks} {y_judul} Td",
               f"({bersih(judul)} - {idx + 1}/{len(halaman)}) Tj", "ET",
               "BT", "/F1 7.2 Tf", f"{x_teks} {y_tabel} Td", "11.5 TL"]
        for teks in daftar:
            isi.append(f"({bersih(teks)}) Tj")
            isi.append("T*")
        isi.append("ET")
        if footer:
            isi += ["BT", "/F1 8 Tf", f"{x_teks} 30 Td",
                    f"({bersih(footer)}) Tj", "ET"]
        aliran = "\n".join(isi).encode("latin-1")
        objek.append((nomor_hal,
                      f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {lebar_hal} {tinggi_hal}] "
                      f"/Resources << /Font << /F1 3 0 R >> >> "
                      f"/Contents {nomor_isi} 0 R >>".encode("latin-1")))
        objek.append((nomor_isi,
                      b"<< /Length " + str(len(aliran)).encode("latin-1")
                      + b" >>\nstream\n" + aliran + b"\nendstream"))
    kids = " ".join(f"{4 + 2 * i} 0 R" for i in range(len(halaman)))
    objek.extend([
        (1, b"<< /Type /Catalog /Pages 2 0 R >>"),
        (2, f"<< /Type /Pages /Kids [{kids}] /Count {len(halaman)} >>".encode("latin-1")),
        (3, b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica "
            b"/Encoding /WinAnsiEncoding >>"),
    ])
    objek.sort(key=lambda x: x[0])
    keluaran = bytearray(b"%PDF-1.4\n")
    posisi = {}
    for nomor, isi in objek:
        posisi[nomor] = len(keluaran)
        keluaran += f"{nomor} 0 obj\n".encode("latin-1") + isi + b"\nendobj\n"
    xref = len(keluaran)
    total = max(posisi) + 1
    keluaran += f"xref\n0 {total}\n".encode("latin-1")
    keluaran += b"0000000000 65535 f \n"
    for i in range(1, total):
        keluaran += f"{posisi.get(i, 0):010d} 00000 n \n".encode("latin-1")
    keluaran += (f"trailer\n<< /Size {total} /Root 1 0 R >>\n"
                 f"startxref\n{xref}\n%%EOF").encode("latin-1")
    return bytes(keluaran)


def _render_isian_siswa(prefix: str, rec: dict) -> dict:
    c1, c2, c3 = st.columns(3)
    nama = c1.text_input(T("Nama lengkap *", "Full name *", "الاسم الكامل *"),
                         value=str(rec.get("nama") or ""), key=f"{prefix}_nama")
    nis = c2.text_input(T("NIS / NISN *", "NIS / NISN *", "الرقم الوطني *"),
                        value=str(rec.get("nis") or ""), key=f"{prefix}_nis")
    kelas = c3.text_input(T("Kelas", "Class", "الفصل"),
                          value=str(rec.get("kelas") or ""), key=f"{prefix}_kelas")
    jk_opsi = ["Laki-laki", "Perempuan"]
    jk_nilai = str(rec.get("jenis_kelamin") or "Laki-laki")
    jk = c1.selectbox(T("Jenis kelamin", "Gender", "الجنس"), jk_opsi,
                      index=jk_opsi.index(jk_nilai) if jk_nilai in jk_opsi else 0,
                      key=f"{prefix}_jk")
    program_nilai = str(rec.get("program") or MODE_LIST[0])
    program = c2.selectbox(T("Program", "Program", "البرنامج"), MODE_LIST,
                           index=MODE_LIST.index(program_nilai)
                           if program_nilai in MODE_LIST else 0,
                           key=f"{prefix}_program")
    status_nilai = str(rec.get("status_siswa") or SISWA_STATUS_OPSI[0])
    status = c3.selectbox(T("Status", "Status", "الحالة"), SISWA_STATUS_OPSI,
                          index=SISWA_STATUS_OPSI.index(status_nilai)
                          if status_nilai in SISWA_STATUS_OPSI else 0,
                          key=f"{prefix}_status")
    santri_nilai = str(rec.get("status_santri") or "")
    santri = c3.selectbox(T("Santri / Non Santri", "Resident / Non-Resident", "ساكن / غير ساكن"),
                          LB_STATUS_SISWA,
                          index=LB_STATUS_SISWA.index(santri_nilai)
                          if santri_nilai in LB_STATUS_SISWA else 1,
                          key=f"{prefix}_santri")
    tanggal_lahir = c1.text_input(T("Tanggal lahir (YYYY-MM-DD)",
                                    "Date of birth (YYYY-MM-DD)",
                                    "تاريخ الميلاد (YYYY-MM-DD)"),
                                  value=str(rec.get("tanggal_lahir") or ""),
                                  key=f"{prefix}_lahir")
    hp = c2.text_input(T("No. HP Orang Tua / Wali", "Parent / Guardian Phone",
                         "هاتف ولي الأمر"),
                       value=str(rec.get("no_hp_ortu") or ""), key=f"{prefix}_hp")
    alamat = c3.text_input(T("Alamat singkat", "Short address", "العنوان المختصر"),
                           value=str(rec.get("alamat") or ""), key=f"{prefix}_alamat")
    level_nilai = str(rec.get("level_iqro") or "")
    level = c1.selectbox(T("Level Iqro'", "Iqro' Level", "مستوى إقرأ"),
                         SISWA_LEVEL_OPSI,
                         index=SISWA_LEVEL_OPSI.index(level_nilai)
                         if level_nilai in SISWA_LEVEL_OPSI else 0,
                         key=f"{prefix}_level")
    surah = c2.text_input(T("Surah terakhir dihafal", "Last memorized surah",
                            "آخر سورة محفوظة"),
                          value=str(rec.get("surah_terakhir") or ""),
                          key=f"{prefix}_surah")
    jumlah = c3.text_input(T("Jumlah hafalan", "Memorization amount", "مقدار الحفظ"),
                           value=str(rec.get("jumlah_hafalan") or ""),
                           placeholder=T("Misal: 5 Surah / 1 Juz",
                                         "e.g. 5 Surahs / 1 Juz",
                                         "مثال: 5 سور / جزء واحد"),
                           key=f"{prefix}_jumlah")
    tahsin = c1.number_input(T("Nilai Tahsin terakhir", "Latest Tahsin score",
                               "آخر درجة تحسين"), 0, 100,
                             int(rec.get("nilai_tahsin") or 0), key=f"{prefix}_tahsin")
    tahfidz = c2.number_input(T("Nilai Tahfidz terakhir", "Latest Tahfidz score",
                                "آخر درجة تحفيظ"), 0, 100,
                              int(rec.get("nilai_tahfidz") or 0), key=f"{prefix}_tahfidz")
    guru = c3.text_input(T("Guru pembimbing", "Mentor teacher", "المعلم المشرف"),
                         value=str(rec.get("guru_pembimbing") or ""), key=f"{prefix}_guru")
    h1, h2, h3 = st.columns(3)
    hadir = h1.number_input(T("Hadir (x)", "Present (x)", "حاضر (x)"), 0, 999,
                            int(rec.get("hadir") or 0), key=f"{prefix}_hadir")
    izin = h2.number_input(T("Izin (x)", "Excused (x)", "إذن (x)"), 0, 999,
                           int(rec.get("izin") or 0), key=f"{prefix}_izin")
    alpa = h3.number_input(T("Alpa (x)", "Absent (x)", "غائب (x)"), 0, 999,
                           int(rec.get("alpa") or 0), key=f"{prefix}_alpa")
    masuk = st.text_input(T("Tanggal masuk (YYYY-MM-DD)", "Entry date (YYYY-MM-DD)",
                            "تاريخ الالتحاق (YYYY-MM-DD)"),
                          value=str(rec.get("tanggal_masuk") or ""), key=f"{prefix}_masuk")
    catatan = st.text_area(T("Catatan guru", "Teacher notes", "ملاحظات المعلم"),
                           value=str(rec.get("catatan_guru") or ""), key=f"{prefix}_catatan")
    foto = st.file_uploader(T("Foto siswa (JPG/PNG)", "Student photo (JPG/PNG)",
                              "صورة الطالب (JPG/PNG)"),
                            type=["jpg", "jpeg", "png"], key=f"{prefix}_foto")
    return {
        "nama": nama, "nis": nis, "kelas": kelas, "jenis_kelamin": jk,
        "program": program, "status_siswa": status, "status_santri": santri,
        "tanggal_lahir": tanggal_lahir, "no_hp_ortu": hp, "alamat": alamat,
        "level_iqro": level, "surah_terakhir": surah, "jumlah_hafalan": jumlah,
        "nilai_tahsin": tahsin, "nilai_tahfidz": tahfidz,
        "hadir": hadir, "izin": izin, "alpa": alpa,
        "guru_pembimbing": guru, "tanggal_masuk": masuk,
        "catatan_guru": catatan, "_foto_baru": foto,
    }


def page_siswa():
    st.markdown(f"""
    <div class="hero-small">
      <h2>👥 {T("Data Siswa", "Student Data", "بيانات الطلاب")}</h2>
      <p>{T("Kelola data, progress ngaji, nilai, kehadiran, dan hafalan siswa.",
           "Manage student data, recitation progress, scores, attendance, and memorization.",
           "إدارة بيانات الطلاب وتقدم التلاوة والدرجات والحضور والحفظ.")}</p>
    </div>
    """, unsafe_allow_html=True)
    pesan_ok = st.session_state.pop("_siswa_pesan", None)
    if pesan_ok:
        st.success(pesan_ok)
    pesan_warn = st.session_state.pop("_siswa_warn", None)
    if pesan_warn:
        st.warning(pesan_warn)

    pengelola = st.session_state.user_role == "Pengelola"
    boleh_ubah = _boleh_ubah()
    if pengelola and not boleh_ubah:
        st.warning(PESAN_AKSES_DITOLAK)
        form_minta_izin("siswa")
    supa_rows, sb_error = load_students_supabase()
    if sb_error is None:
        st.success(T(f"Terhubung ke Supabase · {len(supa_rows)} siswa terdaftar",
                     f"Connected to Supabase · {len(supa_rows)} students registered",
                     f"متصل بـ Supabase · {len(supa_rows)} طالبًا مسجلًا"))
        if st.session_state.pop("siswa_seeded", None):
            st.success(T("20 siswa berhasil dimasukkan",
                         "20 students inserted successfully",
                         "تم إدخال 20 طالبًا بنجاح"))
        if supa_rows:
            lokal = {
                rapikan_nama(str(s.get("nama") or "")).lower(): s
                for s in st.session_state.data.get("siswa", [])
            }
            ubah = False
            for row in supa_rows:
                kunci = rapikan_nama(str(row.get("nama") or "")).lower()
                program = str(row.get("program") or "").strip()
                if not kunci or program not in MODE_LIST:
                    continue
                dasar = {
                    "jenis_kelamin": str(row.get("jenis_kelamin") or "").strip(),
                    "program": program,
                    "kelas": str(row.get("kelas") or "").strip(),
                }
                rec = lokal.get(kunci)
                if rec is None:
                    st.session_state.data["siswa"].append({
                        "nama": str(row.get("nama") or "").strip(), **dasar,
                    })
                    ubah = True
                else:
                    for kunci_bidang, nilai in dasar.items():
                        if nilai and str(rec.get(kunci_bidang) or "") != nilai:
                            rec[kunci_bidang] = nilai
                            ubah = True
            if ubah:
                save_all_data()
        else:
            st.info(T("Belum ada data siswa di tabel Supabase.",
                          "No student data in the Supabase table yet.",
                          "لا توجد بيانات طلاب في جدول Supabase بعد."))
            if pengelola and st.button(T("📥 Masukkan 20 Data Awal",
                                             "📥 Insert 20 Initial Records",
                                             "📥 إدخال 20 سجلًا أوليًا"),
                                           type="primary", key="seed_siswa",
                                           disabled=not boleh_ubah):
                client, sb_err = get_supabase_client()
                if sb_err:
                    st.error(sb_err)
                else:
                    try:
                        cek = client.table("siswa").select("id").limit(1).execute().data or []
                    except Exception as exc:
                        cek = None
                        st.error(T("Gagal memeriksa isi tabel: ", "Failed to check table contents: ",
                                       "فشل فحص محتويات الجدول: ") + str(exc))
                    if cek == []:
                        records = [
                            {"nama": s.get("nama", ""),
                             "program": s.get("program", "Iqro'"),
                             "kelas": s.get("kelas", "")}
                            for s in st.session_state.data["siswa"]
                        ]
                        try:
                            client.table("siswa").insert(records).execute()
                            load_students_supabase.clear()
                            st.session_state["siswa_seeded"] = True
                            st.rerun()
                        except Exception as exc:
                            st.error(T("Gagal memasukkan data awal: ", "Failed to insert initial data: ",
                                           "فشل إدخال البيانات الأولية: ") + str(exc))
                    elif cek:
                        st.warning(T("Tabel siswa sudah berisi data. Tidak ada data yang dimasukkan.",
                                     "The student table already contains data. Nothing was inserted.",
                                     "جدول الطلاب يحتوي على بيانات بالفعل. لم يتم إدخال أي شيء."))
        if st.button(T("🔄 Muat ulang dari Supabase", "🔄 Reload from Supabase",
                       "🔄 إعادة التحميل من Supabase")):
            load_students_supabase.clear()
            st.rerun()
        st.caption(T("Sumber data: tabel public.siswa di Supabase.",
                     "Data source: public.siswa table in Supabase.",
                     "مصدر البيانات: جدول public.siswa في Supabase."))
    elif "belum dikonfigurasi" in str(sb_error) or "belum terpasang" in str(sb_error):
        st.caption(T("Supabase belum aktif — menampilkan data siswa lokal.",
                     "Supabase is inactive — showing local student data.",
                     "Supabase غير مفعّل — يتم عرض بيانات الطلاب المحلية."))
    else:
        st.warning(sb_error)

    siswa = _lengkapi_siswa()

    H = {
        "no": T("No", "No", "رقم"),
        "foto": T("Foto", "Photo", "الصورة"),
        "nama": T("Nama", "Name", "الاسم"),
        "nis": T("NIS / NISN", "NIS / NISN", "الرقم الوطني"),
        "lahir": T("Tanggal Lahir", "Date of Birth", "تاريخ الميلاد"),
        "umur": T("Umur", "Age", "العمر"),
        "kelas": T("Kelas", "Class", "الفصل"),
        "jk": T("Jenis Kelamin", "Gender", "الجنس"),
        "santri": T("Status Santri", "Resident Status", "حالة السكن"),
        "program": T("Program", "Program", "البرنامج"),
        "hp": T("No. HP Orang Tua", "Parent Phone", "هاتف ولي الأمر"),
        "alamat": T("Alamat", "Address", "العنوان"),
        "level": T("Level Iqro'", "Iqro' Level", "مستوى إقرأ"),
        "surah": T("Surah Terakhir", "Last Surah", "آخر سورة"),
        "hafalan": T("Jumlah Hafalan", "Memorization", "مقدار الحفظ"),
        "tahsin": T("Nilai Tahsin", "Tahsin Score", "درجة التحسين"),
        "tahfidz": T("Nilai Tahfidz", "Tahfidz Score", "درجة التحفيظ"),
        "hadir": T("Hadir", "Present", "حاضر"),
        "izin": T("Izin", "Excused", "إذن"),
        "alpa": T("Alpa", "Absent", "غائب"),
        "kehadiran": T("Kehadiran", "Attendance", "الحضور"),
        "status": T("Status", "Status", "الحالة"),
        "guru": T("Guru Pembimbing", "Mentor Teacher", "المعلم المشرف"),
        "masuk": T("Tanggal Masuk", "Entry Date", "تاريخ الالتحاق"),
        "catatan": T("Catatan Guru", "Teacher Notes", "ملاحظات المعلم"),
    }

    total = len(siswa)
    aktif = sum(1 for s in siswa if str(s.get("status_siswa") or "Aktif") == "Aktif")
    nilai_tahsin = [int(s.get("nilai_tahsin") or 0) for s in siswa]
    nilai_tahfidz = [int(s.get("nilai_tahfidz") or 0) for s in siswa]
    rata_tahsin = round(sum(nilai_tahsin) / total) if total else 0
    rata_tahfidz = round(sum(nilai_tahfidz) / total) if total else 0
    m1, m2, m3, m4 = st.columns(4)
    m1.metric(T("Total Siswa", "Total Students", "إجمالي الطلاب"), total)
    m2.metric(T("Status Aktif", "Active", "نشط"), aktif)
    m3.metric(T("Rata-rata Tahsin", "Avg. Tahsin", "متوسط التحسين"), rata_tahsin)
    m4.metric(T("Rata-rata Tahfidz", "Avg. Tahfidz", "متوسط التحفيظ"), rata_tahfidz)

    kelas_opsi = [T("Semua Kelas", "All Classes", "كل الفصول")] + sorted({
        str(s.get("kelas") or "").strip() for s in siswa
        if str(s.get("kelas") or "").strip()
    })
    program_opsi = [T("Semua Program", "All Programs", "كل البرامج")] + list(MODE_LIST)
    status_opsi = [T("Semua Status", "All Statuses", "كل الحالات")] + SISWA_STATUS_OPSI
    santri_opsi = [T("Semua Santri", "All Resident Status", "كل حالات السكن")] + LB_STATUS_SISWA
    f1, f2, f3, f4, f5 = st.columns([2, 1.1, 1.1, 1.1, 1.1])
    cari = f1.text_input(T("🔍 Cari Nama / NIS", "🔍 Search Name / NIS",
                           "🔍 بحث بالاسم / الرقم"),
                         placeholder=T("Ketik nama atau NIS...", "Type name or NIS...",
                                       "اكتب الاسم أو الرقم..."))
    filter_kelas = f2.selectbox(T("Filter Kelas", "Filter Class", "تصفية الفصل"),
                                kelas_opsi, key="filter_kelas_siswa")
    filter_program = f3.selectbox(T("Filter Program", "Filter Program", "تصفية البرنامج"),
                                  program_opsi, key="filter_program_siswa")
    filter_status = f4.selectbox(T("Filter Status", "Filter Status", "تصفية الحالة"),
                                 status_opsi, key="filter_status_siswa")
    filter_santri = f5.selectbox(T("Filter Santri", "Filter Resident", "تصفية السكن"),
                                 santri_opsi, key="filter_santri_siswa")

    semua_kelas = T("Semua Kelas", "All Classes", "كل الفصول")
    semua_program = T("Semua Program", "All Programs", "كل البرامج")
    semua_status = T("Semua Status", "All Statuses", "كل الحالات")
    semua_santri = T("Semua Santri", "All Resident Status", "كل حالات السكن")

    def kehadiran_teks(s):
        return (f"{H['hadir']} {int(s.get('hadir') or 0)}x / "
                f"{H['izin']} {int(s.get('izin') or 0)}x / "
                f"{H['alpa']} {int(s.get('alpa') or 0)}x")

    tersaring = []
    for s in siswa:
        nama_s = str(s.get("nama") or "")
        nis_s = str(s.get("nis") or "")
        if cari and cari.strip().lower() not in (nama_s + " " + nis_s).lower():
            continue
        if filter_kelas != semua_kelas and str(s.get("kelas") or "") != filter_kelas:
            continue
        if filter_program != semua_program and str(s.get("program") or "") != filter_program:
            continue
        if (filter_status != semua_status
                and str(s.get("status_siswa") or "Aktif") != filter_status):
            continue
        if filter_santri != semua_santri and str(s.get("status_santri") or "") != filter_santri:
            continue
        tersaring.append(s)

    baris_tabel = []
    for nomor, s in enumerate(tersaring, start=1):
        baris_tabel.append({
            H["no"]: nomor,
            H["foto"]: _foto_siswa_uri(s.get("foto")),
            H["nama"]: str(s.get("nama") or ""),
            H["nis"]: str(s.get("nis") or "-"),
            H["lahir"]: str(s.get("tanggal_lahir") or "-"),
            H["umur"]: _umur_siswa(s.get("tanggal_lahir")) or "-",
            H["kelas"]: str(s.get("kelas") or "-"),
            H["jk"]: jenis_kelamin_tampil(s),
            H["santri"]: str(s.get("status_santri") or "-"),
            H["program"]: str(s.get("program") or ""),
            H["hp"]: str(s.get("no_hp_ortu") or "-"),
            H["alamat"]: str(s.get("alamat") or "-"),
            H["level"]: str(s.get("level_iqro") or "-"),
            H["surah"]: str(s.get("surah_terakhir") or "-"),
            H["hafalan"]: str(s.get("jumlah_hafalan") or "-"),
            H["tahsin"]: int(s.get("nilai_tahsin") or 0),
            H["tahfidz"]: int(s.get("nilai_tahfidz") or 0),
            H["kehadiran"]: kehadiran_teks(s),
            H["status"]: str(s.get("status_siswa") or "Aktif"),
            H["guru"]: str(s.get("guru_pembimbing") or "-"),
            H["masuk"]: str(s.get("tanggal_masuk") or "-"),
            H["catatan"]: str(s.get("catatan_guru") or "-"),
        })

    df_tampil = pd.DataFrame(baris_tabel)
    if df_tampil.empty:
        st.info(T("Belum ada siswa yang cocok dengan filter.",
                  "No students match the filters.",
                  "لا يوجد طلاب يطابقون عوامل التصفية."))
        pilih_baris = []
        tabel = None
    else:
        tabel = st.dataframe(
            df_tampil, use_container_width=True, hide_index=True, height=460,
            on_select="rerun", selection_mode="single-row", key="tabel_siswa",
            column_config={
                H["foto"]: st.column_config.ImageColumn(H["foto"], width="small"),
                H["tahsin"]: st.column_config.NumberColumn(H["tahsin"], format="%d"),
                H["tahfidz"]: st.column_config.NumberColumn(H["tahfidz"], format="%d"),
                H["no"]: st.column_config.NumberColumn(H["no"], width="small"),
            },
        )
        st.caption(T("Klik salah satu baris untuk melihat detail lengkap + grafik progress.",
                     "Click any row to see full details + progress chart.",
                     "انقر على أي صف لعرض التفاصيل الكاملة + مخطط التقدم."))
        try:
            pilih_baris = list(tabel.selection.rows)
        except Exception:
            pilih_baris = []

    kolom_excel = [H["no"], H["nama"], H["nis"], H["kelas"], H["jk"], H["santri"],
                   H["program"],
                   H["lahir"], H["umur"], H["hp"], H["alamat"], H["level"],
                   H["surah"], H["hafalan"], H["tahsin"], H["tahfidz"],
                   H["kehadiran"], H["status"], H["guru"], H["masuk"], H["catatan"]]
    isi_excel = [[nomor, str(s.get("nama") or ""), str(s.get("nis") or ""),
                  str(s.get("kelas") or ""), jenis_kelamin_tampil(s),
                  str(s.get("status_santri") or ""),
                  str(s.get("program") or ""), str(s.get("tanggal_lahir") or ""),
                  _umur_siswa(s.get("tanggal_lahir")), str(s.get("no_hp_ortu") or ""),
                  str(s.get("alamat") or ""), str(s.get("level_iqro") or ""),
                  str(s.get("surah_terakhir") or ""), str(s.get("jumlah_hafalan") or ""),
                  int(s.get("nilai_tahsin") or 0), int(s.get("nilai_tahfidz") or 0),
                  kehadiran_teks(s), str(s.get("status_siswa") or "Aktif"),
                  str(s.get("guru_pembimbing") or ""), str(s.get("tanggal_masuk") or ""),
                  str(s.get("catatan_guru") or "")]
                 for nomor, s in enumerate(tersaring, start=1)]
    if BAHASA_ARAB:
        kepala_pdf = ["No", "Name", "NIS", "Class", "Program", "Tahsin", "Tahfidz", "Status"]
    else:
        kepala_pdf = [H["no"], H["nama"], H["nis"], H["kelas"], H["program"],
                      H["tahsin"], H["tahfidz"], H["status"]]
    kepala_pdf = kepala_pdf[:4] + ["Santri"] + kepala_pdf[4:]
    isi_pdf = [[nomor, str(s.get("nama") or ""), str(s.get("nis") or ""),
                str(s.get("kelas") or ""), str(s.get("status_santri") or ""),
                str(s.get("program") or ""),
                int(s.get("nilai_tahsin") or 0), int(s.get("nilai_tahfidz") or 0),
                str(s.get("status_siswa") or "Aktif")]
               for nomor, s in enumerate(tersaring, start=1)]
    e1, e2 = st.columns(2)
    e1.download_button(
        T("📊 Export Excel (.xlsx)", "📊 Export Excel (.xlsx)",
          "📊 تصدير Excel (.xlsx)"),
        data=_xlsx_bytes(kolom_excel, isi_excel),
        file_name="data_siswa_qori_ai.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
    )
    e2.download_button(
        T("📄 Export PDF", "📄 Export PDF", "📄 تصدير PDF"),
        data=_pdf_bytes(T("Data Siswa QORI AI", "QORI AI Student Data",
                          "بيانات طلاب QORI AI"),
                        kepala_pdf, isi_pdf),
        file_name="data_siswa_qori_ai.pdf", mime="application/pdf",
        use_container_width=True,
    )

    if pilih_baris and tersaring and pilih_baris[0] < len(tersaring):
        s = tersaring[pilih_baris[0]]
        st.divider()
        st.subheader("🔎 " + T("Detail Siswa", "Student Details", "تفاصيل الطالب")
                     + f": {s.get('nama', '')}")
        d1, d2 = st.columns([1, 3])
        with d1:
            uri = _foto_siswa_uri(s.get("foto"))
            if uri:
                st.image(uri, width=150,
                         caption=T("Foto Siswa", "Student Photo", "صورة الطالب"))
            else:
                st.markdown(
                    "<div style='width:150px;height:150px;background:#E0E7FF;"
                    "border-radius:16px;display:flex;align-items:center;"
                    "justify-content:center;font-size:48px;'>👨‍🎓</div>",
                    unsafe_allow_html=True)
        with d2:
            info1, info2 = st.columns(2)
            info1.write(f"**{H['nis']}:** {s.get('nis') or '-'}")
            info1.write(f"**{H['kelas']}:** {s.get('kelas') or '-'}")
            info1.write(f"**{H['santri']}:** {s.get('status_santri') or '-'}")
            info1.write(f"**{H['lahir']}:** {s.get('tanggal_lahir') or '-'} "
                        f"({_umur_siswa(s.get('tanggal_lahir')) or '-'} "
                        f"{T('tahun', 'years', 'سنة')})")
            info1.write(f"**{H['hp']}:** {s.get('no_hp_ortu') or '-'}")
            info1.write(f"**{H['alamat']}:** {s.get('alamat') or '-'}")
            info2.write(f"**{H['level']}:** {s.get('level_iqro') or '-'}")
            info2.write(f"**{H['surah']}:** {s.get('surah_terakhir') or '-'}")
            info2.write(f"**{H['hafalan']}:** {s.get('jumlah_hafalan') or '-'}")
            info2.write(f"**{H['guru']}:** {s.get('guru_pembimbing') or '-'}")
            info2.write(f"**{H['masuk']}:** {s.get('tanggal_masuk') or '-'}")
        st.write(f"**{H['kehadiran']}:** {kehadiran_teks(s)} | "
                 f"**{H['status']}:** {s.get('status_siswa') or 'Aktif'}")
        grafik = pd.DataFrame(
            {"Nilai": [int(s.get("nilai_tahsin") or 0),
                       int(s.get("nilai_tahfidz") or 0)]},
            index=["Tahsin", "Tahfidz"],
        )
        st.markdown(f"**📈 {T('Grafik Progress', 'Progress Chart', 'مخطط التقدم')}**")
        st.bar_chart(grafik, height=240)
        st.caption(f"{H['catatan']}: {s.get('catatan_guru') or '-'}")
        if pengelola:
            b1, b2 = st.columns(2)
            if b1.button(T("✏️ Edit Siswa Ini", "✏️ Edit This Student",
                           "✏️ تعديل هذا الطالب"),
                         key="detail_edit_siswa", use_container_width=True,
                         disabled=not boleh_ubah):
                st.session_state["siswa_edit"] = str(s.get("nama") or "")
                st.session_state.pop("siswa_hapus", None)
                st.rerun()
            if b2.button(T("🗑️ Hapus Siswa Ini", "🗑️ Delete This Student",
                           "🗑️ حذف هذا الطالب"),
                         key="detail_hapus_siswa", use_container_width=True,
                         disabled=not boleh_ubah):
                st.session_state["siswa_hapus"] = str(s.get("nama") or "")
                st.session_state.pop("siswa_edit", None)
                st.rerun()

    if pengelola:
        with st.expander(T("➕ Tambah Data Siswa", "➕ Add Student Data",
                           "➕ إضافة بيانات طالب")):
            with st.form("form_tambah_siswa_v2", clear_on_submit=True):
                baru = _render_isian_siswa("tambah", {})
                simpan_baru = st.form_submit_button(
                    T("Simpan Data Siswa", "Save Student Data", "حفظ بيانات الطالب"),
                    type="primary", disabled=not boleh_ubah)
            if simpan_baru and boleh_ubah:
                pesan = _validasi_siswa(baru)
                if pesan:
                    st.error(pesan)
                else:
                    berkas = baru.pop("_foto_baru", None)
                    foto_rel = _simpan_foto_siswa(baru.get("nama"), berkas)
                    rekam = _rekam_dari_isian(baru, foto=foto_rel)
                    if rekam.get("foto"):
                        sid_foto = _foto_id_siswa(rekam)
                        foto_bytes = base64.b64decode(rekam["foto"].split(",", 1)[1])
                        foto_ok, foto_err = _simpan_foto_profil_permanen(
                            f"foto_profil_siswa_{sid_foto}",
                            {"data": foto_bytes, "mime": "image/jpeg", "data_uri": rekam["foto"]},
                            untuk_siswa=True)
                        if not foto_ok:
                            st.session_state["_siswa_warn"] = "Foto tersimpan lokal, tetapi gagal ke Supabase: " + str(foto_err)
                    ok = True
                    if sb_error is None:
                        ok, err = save_student_supabase({
                            "nama": rekam["nama"],
                            "jenis_kelamin": rekam["jenis_kelamin"],
                            "status": "Santri",
                            "program": rekam["program"],
                            "kelas": rekam["kelas"],
                        })
                        if not ok:
                            st.session_state["_siswa_warn"] = (
                                T("Data tersimpan lokal, tetapi gagal ke Supabase: ",
                                  "Saved locally, but failed to sync to Supabase: ",
                                  "تم الحفظ محليًا، لكن تعذرت المزامنة إلى Supabase: ")
                                + str(err))
                    _simpan_siswa_lokal(rekam)
                    st.session_state["_siswa_pesan"] = (
                        T("✅ Data siswa berhasil ditambahkan.",
                          "✅ Student data added successfully.",
                          "✅ تمت إضافة بيانات الطالب بنجاح.") + f" {rekam['nama']}")
                    st.rerun()

        with st.expander(T("✏️ Kelola Data Siswa (Edit / Hapus)",
                           "✏️ Manage Students (Edit / Delete)",
                           "✏️ إدارة الطلاب (تعديل / حذف)")):
            if not siswa:
                st.info(T("Belum ada data siswa.", "No student data yet.",
                          "لا توجد بيانات طلاب بعد."))
            else:
                nama_opsi = [str(s.get("nama") or "") for s in siswa]
                target_awal = (st.session_state.get("siswa_edit")
                               or st.session_state.get("siswa_hapus"))
                indeks_awal = (nama_opsi.index(target_awal)
                               if target_awal in nama_opsi else 0)
                pilih = st.selectbox(
                    T("Pilih siswa", "Choose student", "اختر الطالب"),
                    nama_opsi, index=indeks_awal, key="pilih_kelola_siswa")
                k1, k2 = st.columns(2)
                if k1.button(T("✏️ Edit Data Ini", "✏️ Edit This Data",
                               "✏️ تعديل هذه البيانات"),
                             key="kelola_edit_siswa", use_container_width=True,
                             disabled=not boleh_ubah):
                    st.session_state["siswa_edit"] = pilih
                    st.session_state.pop("siswa_hapus", None)
                    st.rerun()
                if k2.button(T("🗑️ Hapus Data Ini", "🗑️ Delete This Data",
                               "🗑️ حذف هذه البيانات"),
                             key="kelola_hapus_siswa", use_container_width=True,
                             disabled=not boleh_ubah):
                    st.session_state["siswa_hapus"] = pilih
                    st.session_state.pop("siswa_edit", None)
                    st.rerun()

                target_edit = st.session_state.get("siswa_edit")
                rec_edit = next((s for s in siswa
                                 if rapikan_nama(str(s.get("nama") or "")).lower()
                                 == rapikan_nama(str(target_edit or "")).lower()), None)
                if rec_edit and boleh_ubah:
                    st.markdown(f"#### ✏️ {T('Edit', 'Edit', 'تعديل')}: "
                                f"{rec_edit.get('nama', '')}")
                    with st.form("form_edit_siswa_v2"):
                        isian_edit = _render_isian_siswa("edit", rec_edit)
                        simpan_edit = st.form_submit_button(
                            T("Simpan Perubahan", "Save Changes", "حفظ التغييرات"),
                            type="primary")
                    batal = st.button(T("Batal Edit", "Cancel Edit", "إلغاء التعديل"),
                                      key="batal_edit_siswa")
                    if batal:
                        st.session_state.pop("siswa_edit", None)
                        st.rerun()
                    if simpan_edit:
                        nama_lama = str(rec_edit.get("nama") or "")
                        pesan = _validasi_siswa(isian_edit, kecuali_nama=nama_lama)
                        if pesan:
                            st.error(pesan)
                        else:
                            berkas = isian_edit.pop("_foto_baru", None)
                            foto_rel = (rec_edit.get("foto") or "")
                            if berkas is not None:
                                foto_lama = rec_edit.get("foto") or ""
                                foto_rel = _simpan_foto_siswa(
                                    isian_edit.get("nama"), berkas)
                                if foto_lama and foto_lama != foto_rel:
                                    _hapus_foto_siswa(foto_lama)
                            rekam = _rekam_dari_isian(isian_edit, foto=foto_rel)
                            if berkas is not None and rekam.get("foto"):
                                sid_foto = _foto_id_siswa(rekam)
                                foto_bytes = base64.b64decode(rekam["foto"].split(",", 1)[1])
                                foto_ok, foto_err = _simpan_foto_profil_permanen(
                                    f"foto_profil_siswa_{sid_foto}",
                                    {"data": foto_bytes, "mime": "image/jpeg", "data_uri": rekam["foto"]},
                                    untuk_siswa=True)
                                if not foto_ok:
                                    st.session_state["_siswa_warn"] = "Foto tersimpan lokal, tetapi gagal ke Supabase: " + str(foto_err)
                            if sb_error is None:
                                sid = next(
                                    (r.get("id") for r in supa_rows
                                     if rapikan_nama(str(r.get("nama") or "")).lower()
                                     == rapikan_nama(nama_lama).lower()), None)
                                if sid is not None:
                                    ok, err = save_student_supabase({
                                        "nama": rekam["nama"],
                                        "jenis_kelamin": rekam["jenis_kelamin"],
                                        "status": "Santri",
                                        "program": rekam["program"],
                                        "kelas": rekam["kelas"],
                                    }, student_id=sid)
                                    if not ok:
                                        st.session_state["_siswa_warn"] = (
                                            T("Perubahan tersimpan lokal, tetapi gagal ke Supabase: ",
                                              "Changes saved locally, but failed to sync to Supabase: ",
                                              "تم حفظ التغييرات محليًا، لكن تعذرت المزامنة إلى Supabase: ")
                                            + str(err))
                            _simpan_siswa_lokal(rekam, before_nama=nama_lama)
                            st.session_state.pop("siswa_edit", None)
                            st.session_state["_siswa_pesan"] = (
                                T("✅ Data siswa berhasil diperbarui.",
                                  "✅ Student data updated successfully.",
                                  "✅ تم تحديث بيانات الطالب بنجاح.")
                                + f" {rekam['nama']}")
                            st.rerun()

                target_hapus = st.session_state.get("siswa_hapus")
                rec_hapus = next((s for s in siswa
                                  if rapikan_nama(str(s.get("nama") or "")).lower()
                                  == rapikan_nama(str(target_hapus or "")).lower()), None)
                if rec_hapus and boleh_ubah:
                    st.warning(T("Yakin hapus data siswa ", "Delete student data ",
                                 "حذف بيانات الطالب ")
                               + f"**{rec_hapus.get('nama', '')}**? "
                               + T("Tindakan ini tidak bisa dibatalkan.",
                                   "This action cannot be undone.",
                                   "لا يمكن التراجع عن هذا الإجراء."))
                    key_yakin = "yakin_hapus_" + _slug_nama(rec_hapus.get("nama"))
                    yakin = st.checkbox(
                        T("Saya yakin ingin menghapus siswa ini",
                          "I am sure I want to delete this student",
                          "أنا متأكد من حذف هذا الطالب"),
                        key=key_yakin)
                    h1, h2 = st.columns(2)
                    if h1.button(T("Ya, Hapus", "Yes, Delete", "نعم، احذف"),
                                 type="primary", disabled=not yakin,
                                 key="konfirmasi_hapus_ya"):
                        if sb_error is None:
                            sid = next(
                                (r.get("id") for r in supa_rows
                                 if rapikan_nama(str(r.get("nama") or "")).lower()
                                 == rapikan_nama(str(rec_hapus.get("nama") or "")).lower()),
                                None)
                            if sid is not None:
                                delete_student_supabase(sid)
                        _hapus_foto_siswa(rec_hapus.get("foto"))
                        nama_hapus = str(rec_hapus.get("nama") or "")
                        _hapus_siswa_lokal(nama_hapus)
                        st.session_state.pop("siswa_hapus", None)
                        st.session_state["_siswa_pesan"] = (
                            T("🗑️ Data siswa dihapus:", "🗑️ Student data deleted:",
                              "🗑️ تم حذف بيانات الطالب:") + f" {nama_hapus}")
                        st.rerun()
                    if h2.button(T("Batal", "Cancel", "إلغاء"),
                                 key="konfirmasi_hapus_batal"):
                        st.session_state.pop("siswa_hapus", None)
                        st.rerun()
    elif not pengelola:
        st.info(T("Mode Siswa: Anda hanya dapat melihat data. Pengubahan data "
                  "hanya tersedia untuk Pengelola.",
                  "Student mode: you can only view data. Editing is available "
                  "to the Manager only.",
                  "وضع الطالب: يمكنك عرض البيانات فقط. التعديل متاح للمدير فقط."))

# ---------------------------------------------------------------------------
# Pengaturan
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# Kelola Pengelola
# ---------------------------------------------------------------------------
def page_kelola_pengelola():
    if not aku_super_admin():
        st.error(PESAN_AKSES_DITOLAK)
        return
    st.markdown(f"""
    <div class="hero-small">
      <h2>👑 {T("Kelola Pengelola", "Manage Managers", "إدارة المديرين")}</h2>
      <p>{T("Khusus Pengelola 1 (Kendar Sultoni): kelola akun pengelola, password, "
           "dan permintaan izin.",
           "Manager 1 (Kendar Sultoni) only: manage manager accounts, passwords, "
           "and permission requests.",
           "خاص بالمدير 1 (Kendar Sultoni): إدارة حسابات المديرين وكلمات المرور "
           "وطلبات الإذن.")}</p>
    </div>
    """, unsafe_allow_html=True)
    if (pesan := st.session_state.pop("_kelola_pesan", None)):
        st.success(pesan)
    if (pesan_err := st.session_state.pop("_kelola_error", None)):
        st.error(pesan_err)

    daftar = _muat_permintaan_izin()
    belum = [p for p in daftar if p.get("status") == "menunggu"]
    disetujui = [p for p in daftar if p.get("status") == "disetujui"]
    k1, k2, k3 = st.columns(3)
    k1.metric(T("Total Pengelola", "Total Managers", "إجمالي المديرين"), len(PENGELOLA))
    k2.metric(T("Minta Izin Menunggu", "Pending Requests", "طلبات معلقة"), len(belum))
    k3.metric(T("Izin Sedang Aktif", "Active Permissions", "أذونات نشطة"), len(disetujui))

    st.markdown('<div class="section-title">👥 '
                + T("Daftar Pengelola", "Manager List", "قائمة المديرين")
                + '</div>', unsafe_allow_html=True)
    urut = sorted(PENGELOLA, key=lambda u: (u not in SUPER_ADMIN, u))
    for uname in urut:
        super_admin = uname in SUPER_ADMIN
        label = ("👑 Pengelola 1 - Super Admin | Akses Penuh" if super_admin
                 else "🛡️ Pengelola 2 - Admin Terbatas | Butuh Izin Pengelola 1")
        warna = "#fff7e6" if super_admin else "#eef6ff"
        garis = "#f0b400" if super_admin else "#cfe4ff"
        st.markdown(
            f'<div style="border-radius:12px;padding:10px 14px;margin-bottom:8px;'
            f'background:{warna};border:1px solid {garis};font-size:14px;">'
            f'<b>{opsi_aman(rapikan_nama(uname))}</b><br>'
            f'<span style="font-size:12px;color:#5d7194;">{label} · '
            + T("Password: •••••• (bisa diubah di bawah)", "Password: •••••• (change below)",
                "كلمة المرور: •••••• (تُغيَّر أدناه)")
            + '</span></div>', unsafe_allow_html=True)

    tab_izin, tab_tambah, tab_pass, tab_hapus = st.tabs([
        f"📩 {T('Permintaan Izin', 'Permission Requests', 'طلبات الإذن')}"
        + (f" ({len(belum)})" if belum else ""),
        "➕ " + T("Tambah Pengelola", "Add Manager", "إضافة مدير"),
        "🔑 " + T("Ubah Password", "Change Password", "تغيير كلمة المرور"),
        "🗑️ " + T("Hapus Pengelola", "Remove Manager", "حذف مدير"),
    ])

    with tab_izin:
        if not daftar:
            st.info(T("Belum ada permintaan izin.",
                      "No permission requests yet.",
                      "لا توجد طلبات إذن بعد."))
        for p in daftar:
            status = str(p.get("status") or "menunggu")
            if status == "menunggu":
                warna_badge, badge = "#fff4cc", "⏳ Menunggu"
            elif status == "disetujui":
                warna_badge = "#dcfce7"
                try:
                    _masih_aktif = (datetime.fromisoformat(str(p.get("berlaku_hingga")))
                                    > datetime.now())
                except (TypeError, ValueError):
                    _masih_aktif = False
                badge = (f"✅ Disetujui s.d. {_batas_izin_teks(p)}"
                         if _masih_aktif else f"⌛ Kedaluwarsa ({_batas_izin_teks(p)})")
            elif status == "ditolak":
                warna_badge, badge = "#fee2e2", "❌ Ditolak"
            else:
                warna_badge, badge = "#e5e7eb", status
            st.markdown(
                f'<div style="border-radius:12px;padding:12px 14px;margin-bottom:10px;'
                f'background:#fff;border:1px solid #e3ebf7;">'
                f'<b>{opsi_aman(str(p.get("nama") or p.get("username") or "-"))}</b> · '
                f'<span style="font-size:11.5px;color:#5d7194;">'
                f'{opsi_aman(str(p.get("waktu") or "-"))}</span><br>'
                f'<span style="font-size:13px;">'
                + T("Mau ubah: ", "Wants to change: ", "يريد تغيير: ")
                + f'<b>{opsi_aman(str(p.get("aksi") or "-"))}</b></span><br>'
                f'<span style="font-size:12.5px;color:#5d7194;">'
                + T("Alasan: ", "Reason: ", "السبب: ")
                + f'{opsi_aman(str(p.get("alasan") or "-"))}</span><br>'
                f'<span style="display:inline-block;margin-top:6px;padding:3px 9px;'
                f'border-radius:999px;background:{warna_badge};font-size:11.5px;'
                f'font-weight:700;">{badge}</span></div>',
                unsafe_allow_html=True)
            if status == "menunggu":
                s1, s2 = st.columns(2)
                pid = str(p.get("id") or "")
                if s1.button("✅ " + T("Setujui", "Approve", "موافقة"),
                             key=f"setujui_izin_{pid}", type="primary",
                             use_container_width=True):
                    p["status"] = "disetujui"
                    p["berlaku_hingga"] = (
                        datetime.now() + timedelta(days=1)).isoformat(timespec="seconds")
                    p["disetujui_pada"] = datetime.now().strftime("%d/%m/%Y %H:%M")
                    _simpan_permintaan_izin(daftar)
                    st.session_state["_kelola_pesan"] = (
                        "✅ Izin disetujui untuk "
                        + str(p.get("nama") or p.get("username") or "")
                        + " selama 1 hari (s.d. " + _batas_izin_teks(p) + ").")
                    st.rerun()
                if s2.button("❌ " + T("Tolak", "Reject", "رفض"),
                             key=f"tolak_izin_{pid}", use_container_width=True):
                    p["status"] = "ditolak"
                    p["berlaku_hingga"] = ""
                    _simpan_permintaan_izin(daftar)
                    st.session_state["_kelola_pesan"] = (
                        "Permintaan izin dari "
                        + str(p.get("nama") or p.get("username") or "")
                        + " ditolak.")
                    st.rerun()

    with tab_tambah:
        with st.form("form_tambah_pengelola", clear_on_submit=True):
            uname_baru = st.text_input(
                T("Username (nama lengkap, huruf kecil)",
                  "Username (full name, lowercase)", "اسم المستخدم (الاسم الكامل)"),
                key="kelola_tambah_uname")
            pass_baru = st.text_input(T("Password", "Password", "كلمة المرور"),
                                      type="password", key="kelola_tambah_pass")
            tambah = st.form_submit_button(
                "➕ " + T("Tambah sebagai Pengelola 2", "Add as Manager 2",
                          "إضافة كمدير 2"),
                type="primary", key="kelola_tambah_btn")
        if tambah:
            un = " ".join(uname_baru.strip().lower().split())
            if not un or not pass_baru.strip():
                st.error(T("Username dan password wajib diisi.",
                           "Username and password are required.",
                           "اسم المستخدم وكلمة المرور مطلوبان."))
            elif un in PENGELOLA:
                st.warning(T("Username itu sudah terdaftar sebagai Pengelola.",
                             "That username is already registered as a Manager.",
                             "اسم المستخدم مسجل بالفعل كمدير."))
            elif un in SISWA_LOGIN:
                st.warning(T("Username itu dipakai akun Siswa. Pakai nama lain.",
                             "That username belongs to a Student account. Use another name.",
                             "اسم المستخدم هذا لحساب طالب. استخدم اسمًا آخر."))
            else:
                PENGELOLA[un] = pass_baru.strip()
                save_all_data()
                st.session_state["_kelola_pesan"] = (
                    "✅ Pengelola 2 baru ditambahkan: " + rapikan_nama(un)
                    + " (Admin Terbatas).")
                st.rerun()
        st.caption(T("Pengelola baru otomatis masuk level Pengelola 2 (hanya lihat, "
                     "butuh izin untuk mengubah).",
                     "New managers are automatically Manager 2 (view only, needs "
                     "permission to change).",
                     "المديرون الجدد تلقائيًا من المستوى 2 (عرض فقط، يحتاجون إذنًا للتغيير)."))

    with tab_pass:
        pilihan_pass = sorted(PENGELOLA, key=lambda u: (u not in SUPER_ADMIN, u))
        with st.form("form_ganti_password_pengelola", clear_on_submit=True):
            target_pass = st.selectbox(
                T("Pilih pengelola", "Choose manager", "اختر المدير"),
                pilihan_pass, format_func=rapikan_nama, key="kelola_pass_target")
            pass_anyar = st.text_input(T("Password baru", "New password", "كلمة مرور جديدة"),
                                       type="password", key="kelola_pass_baru")
            ganti = st.form_submit_button(
                "🔑 " + T("Simpan Password Baru", "Save New Password",
                          "حفظ كلمة المرور الجديدة"),
                type="primary", key="kelola_pass_btn")
        if ganti:
            if not pass_anyar.strip():
                st.error(T("Password baru tidak boleh kosong.",
                           "New password cannot be empty.",
                           "كلمة المرور الجديدة لا يمكن أن تكون فارغة."))
            else:
                PENGELOLA[target_pass] = pass_anyar.strip()
                save_all_data()
                st.session_state["_kelola_pesan"] = (
                    "✅ Password " + rapikan_nama(target_pass) + " berhasil diubah.")
                st.rerun()
        st.caption(T("Password tidak pernah ditampilkan di layar.",
                     "Passwords are never displayed on screen.",
                     "لا تُعرض كلمات المرور على الشاشة أبدًا."))

    with tab_hapus:
        calon_hapus = [u for u in sorted(PENGELOLA) if u not in SUPER_ADMIN]
        if not calon_hapus:
            st.info(T("Tidak ada Pengelola 2 yang bisa dihapus.",
                      "No Manager 2 accounts to remove.",
                      "لا يوجد مدير 2 للحذف."))
        else:
            target_hapus = st.selectbox(
                T("Pilih pengelola yang dihapus", "Choose manager to remove",
                  "اختر المدير للحذف"),
                calon_hapus, format_func=rapikan_nama, key="kelola_hapus_target")
            yakin = st.checkbox(
                T("Saya yakin menghapus akun pengelola ini",
                  "I am sure I want to remove this manager account",
                  "أنا متأكد من حذف حساب المدير هذا"),
                key="kelola_hapus_yakin")
            if st.button("🗑️ " + T("Hapus Pengelola", "Remove Manager", "حذف المدير"),
                         type="primary", disabled=not yakin,
                         key="kelola_hapus_btn"):
                PENGELOLA.pop(target_hapus, None)
                save_all_data()
                st.session_state["_kelola_pesan"] = (
                    "🗑️ Akun pengelola dihapus: " + rapikan_nama(target_hapus))
                st.rerun()
        st.caption(T("Pengelola 1 (Kendar Sultoni) tidak bisa dihapus.",
                     "Manager 1 (Kendar Sultoni) cannot be removed.",
                     "لا يمكن حذف المدير 1 (Kendar Sultoni)."))


def page_pengaturan():
    if st.session_state.user_role == "Pengelola" and not aku_super_admin():
        st.error(PESAN_AKSES_DITOLAK)
        return
    st.markdown(f"## ⚙️ {T('Pengaturan', 'Settings', 'الإعدادات')}")
    st.markdown(
        "<p style='color:#6B7280; margin-top:-10px;'>"
        + T("Atur QORI AI sesuai gaya belajarmu. Semua tersimpan otomatis.",
            "Customize QORI AI to your learning style. Everything saves automatically.",
            "خصّص QORI AI حسب أسلوب تعلمك. يتم الحفظ تلقائيًا.")
        + "</p>",
        unsafe_allow_html=True,
    )
    st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)

    simpan_cfg = st.session_state.setdefault("pengaturan_tersimpan", {})
    defaults = {
        "set_nama": "Kendar Sultoni", "set_lembaga": "TPQ Nurul Ilmi", "set_email": "kendar@gmail.com",
        "set_mode": "Tahsin", "set_iqro": "Iqro' 3", "set_target": 30,
        "set_huruf": "Sedang", "set_suara": QORI_LIST[0], "set_kecepatan": "Normal (1x)",
        "set_autoplay": True, "set_tajwid": True,
        "set_reminder": True, "set_jam": "19:00", "set_notif_leader": True,
        "tema_aplikasi": "Terang", "bahasa_aplikasi": "Bahasa Indonesia",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = simpan_cfg.get(k, v)
    if "set_jam_input" not in st.session_state and "set_jam_input" in simpan_cfg:
        st.session_state["set_jam_input"] = simpan_cfg["set_jam_input"]
    if st.session_state.get("set_suara") not in QORI_LIST:
        st.session_state["set_suara"] = qori_terpilih()

    with st.expander(T("👤 A. Profil Saya", "👤 A. My Profile", "👤 أ. ملفي الشخصي"),
                     expanded=True):
        foto_map = st.session_state.setdefault("foto_profil", {})
        foto_saya = foto_map.get(nama_tampil)
        c1, c2 = st.columns([1, 2])
        with c1:
            if foto_saya and foto_saya.get("data"):
                st.image(foto_saya["data"], width=120,
                         caption=T("Foto Profil Kamu", "Your Profile Photo",
                                   "صورة ملفك الشخصي"))
            else:
                st.markdown(
                    "<div style='width:120px;height:120px;background:#E0E7FF;border-radius:50%;"
                    "display:flex;align-items:center;justify-content:center;font-size:48px;'>"
                    "👨‍🏫</div>",
                    unsafe_allow_html=True,
                )
                st.caption(T("Belum ada foto profil.", "No profile photo yet.",
                             "لا توجد صورة ملف شخصي بعد."))
            foto_baru = st.file_uploader(
                T("Upload Foto Profil Baru (JPG/PNG)",
                  "Upload New Profile Photo (JPG/PNG)",
                  "رفع صورة ملف شخصي جديدة (JPG/PNG)"),
                type=["jpg", "jpeg", "png"], key="up_foto",
            )
            if foto_baru is not None:
                if foto_baru.size > 200 * 1024 * 1024:
                    st.error(T("Ukuran foto maksimal 200MB.",
                               "Photo size must be at most 200MB.",
                               "الحجم الأقصى للصورة 200 ميجابايت."))
                elif hashlib.sha256(foto_baru.getvalue()).hexdigest() != st.session_state.get(
                        f"_foto_upload_hash_{_slug_nama(nama_tampil)}"):
                    try:
                        foto_kompres = _kompres_foto_upload(foto_baru)
                        foto_map[nama_tampil] = {
                            "data": foto_kompres["data"], "mime": foto_kompres["mime"]}
                        st.session_state[f"_foto_upload_hash_{_slug_nama(nama_tampil)}"] = hashlib.sha256(
                            foto_baru.getvalue()).hexdigest()
                        foto_ok, foto_err = _simpan_foto_profil_permanen(
                            "foto_profil_pengelola" if peran_tampil == "Pengelola"
                            else f"foto_profil_siswa_{_foto_id_siswa(nama=nama_tampil)}",
                            foto_kompres,
                            untuk_siswa=(peran_tampil == "Siswa"))
                        st.session_state["_foto_ok"] = bool(foto_ok)
                        if not foto_ok:
                            st.session_state["_foto_save_warning"] = foto_err
                        save_all_data()
                        st.rerun()
                    except Exception as exc:
                        st.error(f"Gagal memproses foto: {exc}")
            if st.session_state.get("_foto_save_warning"):
                st.warning("Foto tersimpan di sesi/JSON, tetapi Supabase belum berhasil: " + str(st.session_state.pop("_foto_save_warning")))
            if st.session_state.pop("_foto_ok", False):
                st.success(T("✅ Foto berhasil disimpan! Tidak akan hilang lagi walau pindah halaman.",
                             "✅ Photo saved! It will stay even when you switch pages.",
                             "✅ تم حفظ الصورة! لن تختفي عند تغيير الصفحة."))
            if foto_saya and st.button(
                    T("🗑️ Hapus Foto Profil", "🗑️ Delete Profile Photo",
                      "🗑️ حذف صورة الملف"),
                    key="hapus_foto_pengaturan", use_container_width=True):
                foto_map.pop(nama_tampil, None)
                st.session_state.pop(f"_foto_upload_hash_{_slug_nama(nama_tampil)}", None)
                _hapus_berkas_foto(nama_tampil)
                kunci_foto = ("foto_profil_pengelola" if peran_tampil == "Pengelola"
                              else f"foto_profil_siswa_{_foto_id_siswa(nama=nama_tampil)}")
                st.session_state.get("foto_profil_backup", {}).pop(kunci_foto, None)
                _app_settings_merge(GLOBAL_SETTINGS_USER_ID, {kunci_foto: ""})
                st.session_state["foto_profil_path"] = None
                save_all_data()
                st.rerun()
        with c2:
            st.text_input(T("Nama Tampilan", "Display Name", "اسم العرض"), key="set_nama",
                          on_change=autosave_pengaturan)
            st.text_input(T("Nama Lembaga / TPQ / Sekolah", "Institution / TPQ / School Name",
                            "اسم المؤسسة / دار القرآن / المدرسة"), key="set_lembaga",
                          on_change=autosave_pengaturan)
            st.text_input(T("Username", "Username", "اسم المستخدم"), key="set_email",
                          on_change=autosave_pengaturan)
            st.text_input(T("Ganti Password", "Change Password", "تغيير كلمة المرور"),
                          type="password",
                          placeholder=T("Isi jika mau ganti", "Fill to change",
                                        "املأه إذا أردت التغيير"), key="set_pass")
        st.success(T("Halo, ", "Hello, ", "مرحبًا، ")
                   + f"{st.session_state['set_nama']} - {st.session_state['set_lembaga']}")

    with st.expander(T("📚 B. Preferensi Belajar", "📚 B. Learning Preferences",
                       "📚 ب. تفضيلات التعلم")):
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox(T("Mode Default Saat Buka Aplikasi", "Default Mode on App Start",
                           "الوضع الافتراضي عند فتح التطبيق"),
                         ["Iqro'", "Tahsin", "Tahfidz", "Belajar & Game"], key="set_mode",
                         on_change=autosave_pengaturan)
            st.selectbox(T("Level Iqro' Saat Ini", "Current Iqro' Level", "مستوى إقرأ الحالي"),
                         ["Iqro' 1", "Iqro' 2", "Iqro' 3", "Iqro' 4", "Iqro' 5",
                          "Iqro' 6", "Al-Qur'an"], key="set_iqro",
                         on_change=autosave_pengaturan)
        with col2:
            st.slider(T("Target Belajar Harian (menit)", "Daily Learning Target (minutes)",
                        "هدف التعلم اليومي (دقائق)"), 5, 60, key="set_target",
                      on_change=autosave_pengaturan)
            st.selectbox(T("Ukuran Huruf Al-Qur'an", "Qur'an Font Size", "حجم خط القرآن"),
                         ["Kecil", "Sedang", "Besar", "Sangat Besar"], key="set_huruf",
                         on_change=autosave_pengaturan)
        st.info(
            T("Mode favoritmu: ", "Your favorite mode: ", "وضعك المفضل: ")
            + f"{st.session_state['set_mode']} | "
            + T("Target: ", "Target: ", "الهدف: ")
            + f"{st.session_state['set_target']} "
            + T("menit/hari", "minutes/day", "دقيقة/يوم")
            + " | "
            + T("Huruf: ", "Font: ", "الخط: ")
            + f"{st.session_state['set_huruf']}"
        )

    with st.expander(T("🎙️ C. Suara & AI Assistant", "🎙️ C. Voice & AI Assistant",
                       "🎙️ ج. الصوت ومساعد الذكاء الاصطناعي")):
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox(T("Pilih Suara Qori Laki-laki - Pembaca Al-Qur'an Dunia",
                           "Choose Male Qori Voice - World Qur'an Reciters",
                           "اختر صوت قارئ - قرّاء القرآن العالميون"),
                         QORI_LIST, key="set_suara", on_change=autosave_pengaturan)
            st.selectbox(T("Kecepatan Baca", "Reading Speed", "سرعة القراءة"),
                         ["Lambat (0.75x)", "Normal (1x)", "Cepat (1.25x)"], key="set_kecepatan",
                         on_change=autosave_pengaturan)
        with col2:
            st.toggle(T("Auto-play Audio Saat Buka Materi", "Auto-play Audio on Material Open",
                        "التشغيل التلقائي للصوت عند فتح المادة"), key="set_autoplay",
                      on_change=autosave_pengaturan)
            st.toggle(T("Tampilkan Warna Tajwid (Merah/Hijau)", "Show Tajwid Colors (Red/Green)",
                        "إظهار ألوان التجويد (أحمر/أخضر)"), key="set_tajwid",
                      on_change=autosave_pengaturan)
        st.caption(T("Suara Qori laki-laki asli dari seluruh dunia. Suara ini yang akan "
                     "membacakan ayat saat belajar Tahsin / Tahfidz / Iqro'.",
                     "Authentic male Qori voices from around the world. This voice recites "
                     "verses while learning Tahsin / Tahfidz / Iqro'.",
                     "أصوات قرّاء أصيلة من جميع أنحاء العالم. هذا الصوت يتلو الآيات أثناء "
                     "تعلم التحسين / التحفيظ / إقرأ."))
        nama_tes, url_tes = audio_qori(st.session_state["set_suara"], 1)
        st.caption(T("🎙️ Sekarang memutar: ", "🎙️ Now playing: ", "🎙️ يُشغَّل الآن: ")
                   + f"{nama_tes} - Al-Fatihah")
        if st.button(T("▶️ Tes Suara Qori - Putar Al-Fatihah",
                       "▶️ Test Qori Voice - Play Al-Fatihah",
                       "▶️ اختبار صوت القارئ - تشغيل الفاتحة")):
            st.audio(url_tes)

    with st.expander(T("🔔 D. Notifikasi & Pengingat", "🔔 D. Notifications & Reminders",
                       "🔔 د. الإشعارات والتذكيرات")):
        st.toggle(T("Aktifkan Pengingat Belajar Harian", "Enable Daily Learning Reminder",
                    "تفعيل تذكير التعلم اليومي"), key="set_reminder",
                  on_change=autosave_pengaturan)
        if st.session_state["set_reminder"]:
            st.time_input(T("Jam Pengingat", "Reminder Time", "وقت التذكير"),
                          value=None, key="set_jam_input",
                          on_change=autosave_pengaturan)
            st.markdown(
                T("⏰ Kamu akan diingatkan setiap hari jam ", "⏰ You will be reminded daily at ",
                  "⏰ سيتم تذكيرك يوميًا الساعة ")
                + f"*{st.session_state.get('set_jam_input', '19:00')}* "
                + T("untuk belajar.", "to study.", "للدراسة.")
            )
        st.toggle(T("Notifikasi Leaderboard (Ada yang menyalip poinmu)",
                    "Leaderboard Notification (Someone passed your score)",
                    "إشعار لوحة المتصدرين (تجاوز أحدهم نقاطك)"), key="set_notif_leader",
                  on_change=autosave_pengaturan)

    with st.expander(T("🎨 E. Tampilan & Bahasa", "🎨 E. Appearance & Language",
                       "🎨 هـ. المظهر واللغة")):
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox(
                T("Tema Aplikasi", "App Theme", "مظهر التطبيق"),
                ["Terang", "Gelap"], key="tema_aplikasi",
                on_change=autosave_pengaturan,
                format_func=lambda v: T(
                    {"Terang": "Terang", "Gelap": "Gelap"}[v],
                    {"Terang": "Light", "Gelap": "Dark"}[v],
                    {"Terang": "فاتح", "Gelap": "داكن"}[v]),
            )
        with col2:
            st.selectbox(T("Bahasa", "Language", "اللغة"),
                         ["Bahasa Indonesia", "English", "العربية (Arab)"],
                         key="bahasa_aplikasi", on_change=autosave_pengaturan)
        st.session_state["_tampilan_aktif"] = {
            "tema": st.session_state["tema_aplikasi"],
            "bahasa": st.session_state["bahasa_aplikasi"],
        }
        simpan_cfg["tema_aplikasi"] = st.session_state["tema_aplikasi"]
        simpan_cfg["bahasa_aplikasi"] = st.session_state["bahasa_aplikasi"]
        st.caption(T("Tema dan bahasa langsung berlaku ke seluruh aplikasi.",
                     "Theme and language apply instantly across the whole app.",
                     "يُطبَّق المظهر واللغة فورًا على التطبيق بأكمله."))

    with st.expander(T("💾 F. Data & Aplikasi", "💾 F. Data & Application",
                       "💾 و. البيانات والتطبيق")):
        terakhir_global = st.session_state.get("_qori_global_last_saved") or "Belum ada penyimpanan"
        if st.session_state.get("_qori_global_save_error"):
            st.warning("⚠️ Ada perubahan belum tersimpan: " + str(st.session_state.get("_qori_global_save_error")))
        else:
            st.success(T("✅ Tersimpan Otomatis - Terakhir disimpan: ",
                         "✅ Autosaved - Last saved: ",
                         "✅ محفوظ تلقائيًا - آخر حفظ: ") + f"{terakhir_global} WIB")
        st.caption(T("Autosave tetap aktif. Tombol di bawah menyimpan seluruh isi 14 menu "
                     "QORI AI sekaligus, bukan hanya pengaturan halaman ini.",
                     "Autosave remains active. The button below saves all contents of all 14 "
                     "QORI AI menus, not only this settings page.",
                     "يظل الحفظ التلقائي فعالاً. الزر أدناه يحفظ جميع محتويات القوائم الـ14 "
                     "في QORI AI، وليس إعدادات هذه الصفحة فقط."))
        st.markdown(T("*Lokasi Penyimpanan:* Supabase + Session + File JSON (Aman)",
                      "*Storage Location:* Supabase + Session + JSON File (Secure)",
                      "*موقع التخزين:* Supabase + الجلسة + ملف JSON (آمن)"))
        st.markdown(T("*Versi:* QORI AI v1.0 | *Dibuat oleh:* Kendar Sultoni",
                      "*Version:* QORI AI v1.0 | *Created by:* Kendar Sultoni",
                      "*الإصدار:* QORI AI v1.0 | *أنشأه:* Kendar Sultoni"))
        # Tiga kotak sejajar: satu-satunya tombol simpan, unduh JSON, dan reset.
        st.markdown("""
        <style>
        .st-key-qori_simpan_global_pengaturan button,
        .st-key-qori_download_global_json button,
        .st-key-qori_reset_global_data button {
            background: #ffffff !important;
            color: #111111 !important;
            border: 1px solid #222222 !important;
            border-radius: 8px !important;
            box-shadow: none !important;
            font-weight: 600 !important;
            min-height: 44px !important;
        }
        .st-key-qori_simpan_global_pengaturan button:hover,
        .st-key-qori_download_global_json button:hover,
        .st-key-qori_reset_global_data button:hover {
            background: #f5f5f5 !important;
            color: #111111 !important;
            border-color: #111111 !important;
        }
        </style>
        """, unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("✅ Simpan Semua Pengaturan", key="qori_simpan_global_pengaturan",
                         use_container_width=True, type="secondary"):
                _qori_ok, _qori_detail = _qori_simpan_snapshot_global(
                    alasan="simpan_manual_dari_pengaturan", manual=True)
                if _qori_ok:
                    st.session_state["_qori_global_refresh_after_autosave"] = True
                    st.success("✅ Semua isi 14 menu QORI AI berhasil disimpan. "
                               f"Terakhir disimpan: {_qori_detail} WIB")
                else:
                    st.error("Gagal menyimpan seluruh data QORI AI: " + str(_qori_detail))
        with c2:
            _qori_export_snapshot = _qori_buat_snapshot()
            _qori_export_snapshot["terakhir_disimpan"] = (
                st.session_state.get("_qori_global_last_saved") or "")
            st.download_button(
                T("⬇️ Unduh Data (JSON)", "⬇️ Download Data (JSON)",
                  "⬇️ تنزيل البيانات (JSON)"),
                data=json.dumps(_qori_export_snapshot, ensure_ascii=False, indent=2,
                                default=str).encode("utf-8"),
                file_name="qori_ai_backup_global.json", mime="application/json",
                key="qori_download_global_json", use_container_width=True,
            )
        with c3:
            if st.button(T("🔄 Reset Semua Data", "🔄 Reset All Data",
                           "🔄 إعادة تعيين كل البيانات"),
                         key="qori_reset_global_data", use_container_width=True):
                st.session_state["confirm_reset"] = True
        if st.session_state.get("confirm_reset"):
            st.error(T("Yakin hapus semua data? Tindakan ini tidak bisa dibatalkan.",
                       "Delete all data? This action cannot be undone.",
                       "حذف كل البيانات؟ لا يمكن التراجع عن هذا الإجراء."))
            cc1, cc2 = st.columns(2)
            with cc1:
                if st.button(T("Ya, Hapus Semua", "Yes, Delete All", "نعم، احذف الكل"),
                             type="primary"):
                    try:
                        AUTOSAVE_FILE.unlink(missing_ok=True)
                    except Exception:
                        pass
                    for k in list(st.session_state.keys()):
                        if k.startswith("set_"):
                            del st.session_state[k]
                    for k in ("data_tersimpan", "_sig_autosave", "_tampilan_aktif",
                              "tema_aplikasi", "bahasa_aplikasi"):
                        st.session_state.pop(k, None)
                    simpan_cfg.clear()
                    st.session_state["confirm_reset"] = False
                    st.rerun()
            with cc2:
                if st.button(T("Batal", "Cancel", "إلغاء")):
                    st.session_state["confirm_reset"] = False
                    st.rerun()

    for k in defaults:
        if k in st.session_state:
            simpan_cfg[k] = st.session_state[k]
    if "set_jam_input" in st.session_state:
        simpan_cfg["set_jam_input"] = st.session_state["set_jam_input"]


# ---------------------------------------------------------------------------
# AI Assistant
# ---------------------------------------------------------------------------
KATEGORI_AI = {
    "Tajwid": [
        ("Apa itu qalqalah?", "What is qalqalah?", "ما هي القلقلة؟"),
        ("Jelaskan mad thabi'i", "Explain mad thabi'i", "اشرح المد الطبيعي"),
        ("Hukum nun sukun dan tanwin?", "The rules of nun sukun and tanwin?",
         "ما أحكام النون الساكنة والتنوين؟"),
    ],
    "Tahfidz": [
        ("Tips menjaga hafalan?", "Tips for maintaining memorization?",
         "نصائح للحفاظ على الحفظ؟"),
        ("Buatkan jadwal hafal 1 Juz dalam 30 hari",
         "Make a 30-day plan to memorize 1 Juz",
         "ضع جدولًا لحفظ جزء واحد في ٣٠ يومًا"),
    ],
    "Arti Ayat": [
        ("Berapa ayat Surah An-Nas?", "How many verses are in Surah An-Nas?",
         "كم عدد آيات سورة الناس؟"),
        ("Arti Al-Fatihah ayat 1?", "The meaning of Al-Fatihah verse 1?",
         "ما معنى الآية الأولى من الفاتحة؟"),
    ],
    "Fiqih": [
        ("Cara wudhu yang benar?", "How to perform wudhu correctly?",
         "كيف يكون الوضوء الصحيح؟"),
        ("Apa itu tajwid?", "What is tajwid?", "ما هو التجويد؟"),
    ],
}

MODE_AI = {
    "Ramah": ("🟢 Ramah", "🟢 Friendly", "🟢 لطيف"),
    "Tegas": ("🟠 Tegas", "🟠 Firm", "🟠 حازم"),
    "Ustadz": ("🕌 Ustadz", "🕌 Ustadz", "🕌 أستاذ"),
}

AYAT_AI = {
    1: {
        "nama": "Al-Fatihah", "ayat": 7,
        "baris": [
            ("بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ",
             "Bismillāhir-raḥmānir-raḥīm",
             "Dengan nama Allah Yang Maha Pengasih, Maha Penyayang."),
        ],
    },
    108: {
        "nama": "Al-Kautsar", "ayat": 3,
        "baris": [
            ("إِنَّا أَعْطَيْنَاكَ الْكَوْثَرَ", "Innā a'ṭainākal-kauṡar",
             "Sungguh, Kami telah memberimu (Muhammad) nikmat yang banyak."),
            ("فَصَلِّ لِرَبِّكَ وَانْحَرْ", "Faṣalli lirabbika wanḥar",
             "Maka laksanakanlah salat karena Tuhanmu, dan berkurbanlah."),
            ("إِنَّ شَانِئَكَ هُوَ الْأَبْتَرُ", "Inna syāni'aka huwal-abtar",
             "Sungguh, orang yang membencimu dialah yang terputus."),
        ],
    },
    112: {
        "nama": "Al-Ikhlas", "ayat": 4,
        "baris": [
            ("قُلْ هُوَ اللَّهُ أَحَدٌ", "Qul huwallāhu aḥad",
             "Katakanlah, “Dialah Allah, Yang Maha Esa.”"),
            ("اللَّهُ الصَّمَدُ", "Allāhuṣ-ṣamad",
             "Allah tempat meminta segala sesuatu."),
            ("لَمْ يَلِدْ وَلَمْ يُولَدْ", "Lam yalid wa lam yūlad",
             "(Allah) tidak beranak dan tidak pula diperanakkan."),
            ("وَلَمْ يَكُن لَّهُ كُفُوًا أَحَدٌ", "Wa lam yakul lahū kufuwan aḥad",
             "Dan tidak ada sesuatu yang setara dengan Dia."),
        ],
    },
    114: {
        "nama": "An-Nas", "ayat": 6,
        "baris": [
            ("قُلْ أَعُوذُ بِرَبِّ النَّاسِ", "Qul a'ūżu birabbin-nās",
             "Katakanlah, “Aku berlindung kepada Tuhannya manusia,"),
            ("مَلِكِ النَّاسِ", "Malikin-nās", "Raja manusia,"),
            ("إِلَٰهِ النَّاسِ", "Ilāhin-nās", "Sembahan manusia,"),
            ("مِن شَرِّ الْوَسْوَاسِ الْخَنَّاسِ", "Min syarril-waswāsil-khannās",
             "dari (kejahatan) bisikan setan yang bersembunyi,"),
            ("الَّذِي يُوَسْوِسُ فِي صُدُورِ النَّاسِ", "Allażī yuwaswisu fī ṣudūrin-nās",
             "yang membisikkan (kejahatan) ke dalam dada manusia,"),
            ("مِنَ الْجِنَّةِ وَالنَّاسِ", "Minal-jinnati wan-nās",
             "dari (golongan) jin dan manusia."),
        ],
    },
}

TOPIK_AI = [
    ("Qalqalah", ["qalqalah", "qolqolah"]),
    ("Mad", ["mad "]),
    ("Nun & Tanwin", ["nun sukun", "tanwin"]),
    ("Tajwid", ["tajwid"]),
    ("Makhraj", ["makhraj", "makhorij"]),
    ("Hafalan", ["hafal", "tahfidz", "tahfiz"]),
    ("Wudhu", ["wudhu", "wudu"]),
    ("Arti Ayat", ["arti", "ayat", "surah"]),
]


SYSTEM_PROMPT_AI = (
    "Kamu adalah QORI AI, asisten AI yang ramah, sopan, islami, dan pintar. "
    "Kamu bisa menjawab SEMUA pertanyaan apa saja: pelajaran sekolah, matematika, "
    "bahasa, sains, teknologi, umum, agama, kehidupan sehari-hari, dan lain-lain. "
    "Jawab dengan bahasa Indonesia yang mudah dipahami anak & pemula, jelas, dan lengkap. "
    "Kalau pertanyaannya tentang Al-Qur'an / tajwid, jawab lebih detail dan dengan contoh. "
    "Jangan mengarang ayat, hadis, nomor ayat, atau hukum agama; jika tidak yakin, "
    "sarankan memeriksa mushaf/guru."
)


def jawab_ai(teks: str) -> str:
    t = teks.lower()
    if any(k in t for k in ["salam", "assalam", "halo", "hai"]):
        return ("Wa'alaikumussalam warahmatullah! 🌙 Saya QORI AI Assistant. "
                "Silakan tanyakan apa saja — tajwid, pelajaran sekolah, atau tips menghafal.")
    if "terima kasih" in t or "makasih" in t:
        return "Sama-sama, semoga Allah mudahkan belajar kita. 🤲"
    if "nun sukun" in t or "tanwin" in t:
        return ("Hukum nun sukun dan tanwin ada empat: **izhar** (dibaca jelas), "
                "**idgham** (dilebur), **iqlab** (berubah menjadi bunyi mim), dan "
                "**ikhfa** (dibaca samar disertai dengung).")
    if "qalqalah" in t:
        return ("Qalqalah adalah pantulan suara pada huruf ق ط ب ج د ketika sukun. "
                "Lima hurufnya sering diingat dengan ungkapan **قُطْبُ جَدٍّ**.")
    if "ikhfa" in t:
        return ("Ikhfa adalah membaca nun sukun atau tanwin secara samar disertai dengung "
                "ketika bertemu salah satu dari 15 huruf ikhfa, seperti ت ث ج د ذ ز س ش ص ض ط ظ ف ق ك.")
    if "idgham" in t:
        return ("Idgham berarti meleburkan bunyi nun sukun/tanwin ke huruf berikutnya. "
                "Hurufnya ي ر م ل و ن. Jika bertemu ي ن م و dibaca dengan dengung (bighunnah).")
    if "iqlab" in t:
        return "Iqlab terjadi ketika nun sukun atau tanwin bertemu huruf ب, dibaca menjadi bunyi mim disertai dengung."
    if "izhar" in t:
        return ("Izhar halqi adalah membaca nun sukun/tanwin dengan jelas ketika bertemu salah satu "
                "huruf tenggorokan: ء ه ع ح غ خ.")
    if "mad" in t:
        return ("Mad thabi'i dibaca panjang 2 harakat ketika ada fathah + alif, kasrah + ya, "
                "atau dhammah + wau. Mad wajib muttashil (bertemu hamzah satu kata) dibaca 4–5 harakat, "
                "sedangkan mad jaiz munfashil dibaca 2, 4, atau 5 harakat.")
    if "an-nas" in t or "annas" in t:
        return "Surah An-Nas terdiri dari 6 ayat dan merupakan surah terakhir dalam Al-Qur'an (surah ke-114)."
    if "al-ikhlas" in t or "alikhlas" in t:
        return "Surah Al-Ikhlas terdiri dari 4 ayat dan menegaskan keesaan Allah (tauhid)."
    if "al-falaq" in t or "alfalaq" in t:
        return "Surah Al-Falaq terdiri dari 5 ayat dan berisi permohonan perlindungan dari segala kejahatan."
    if "al-kautsar" in t or "alkautsar" in t:
        return "Surah Al-Kautsar terdiri dari 3 ayat, surah terpendek dalam Al-Qur'an."
    if "an-naba" in t or "annaba" in t:
        return "Surah An-Naba' terdiri dari 40 ayat dan menjadi surah pertama dalam Juz 30."
    if "fatihah" in t:
        return ("Al-Fatihah terdiri dari 7 ayat dan dibaca pada setiap rakaat shalat. "
                "Ayat pertama berbunyi بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ.")
    if "wudhu" in t:
        return ("Wudhu adalah bersuci dengan air sebelum shalat. Rukunnya: niat, membasuh wajah, "
                "membasuh kedua tangan hingga siku, mengusap kepala, membasuh kedua kaki hingga "
                "mata kaki, dan tertib.")
    if "shalat" in t or "salat" in t:
        return ("Shalat wajib ada lima waktu: Subuh, Dzuhur, Ashar, Maghrib, dan Isya. "
                "Shalat diawali takbir dan diakhiri salam, dengan membaca Al-Fatihah pada setiap rakaat.")
    if "puasa" in t:
        return ("Puasa Ramadan wajib bagi muslim yang mampu, dilaksanakan dari terbit fajar hingga "
                "terbenam matahari, disertai niat dan menahan diri dari makan, minum, serta hal yang membatalkan.")
    if "zakat" in t:
        return ("Zakat adalah harta tertentu yang wajib dikeluarkan bagi yang memenuhi syarat, "
                "misalnya zakat fitrah di bulan Ramadan dan zakat mal atas harta yang mencapai nisab.")
    if "doa" in t:
        return ("Doa adalah permohonan kepada Allah. Kita boleh berdoa dengan bahasa sendiri, "
                "memulai dengan memuji Allah dan bershalawat, lalu menyampaikan kebutuhan dengan penuh harap.")
    if "hadis" in t or "hadits" in t:
        return ("Hadis adalah perkataan, perbuatan, atau persetujuan Nabi Muhammad ﷺ yang menjadi "
                "sumber ajaran Islam setelah Al-Qur'an. Untuk rujukan hadis, sebaiknya periksa kitab "
                "hadis terpercaya bersama guru.")
    if "rukun islam" in t:
        return ("Rukun Islam ada lima: syahadat, shalat, zakat, puasa Ramadan, dan haji bagi yang mampu.")
    if "islam" in t:
        return ("Islam adalah agama yang mengajarkan tauhid (mengesakan Allah), dengan Al-Qur'an "
                "sebagai kitab suci dan Sunnah Nabi Muhammad ﷺ sebagai teladan. Ajarannya mencakup "
                "akidah, ibadah, akhlak, dan muamalah.")
    if "hafal" in t or "tahfidz" in t:
        return ("Tips menjaga hafalan: (1) muraja'ah rutin setiap hari, (2) setor hafalan ke guru, "
                "(3) ulangi ayat sebelum tidur dan setelah shalat, (4) gunakan satu mushaf yang sama, "
                "(5) pahami maknanya agar lebih melekat.")
    if "iqro" in t:
        return ("Iqro' adalah metode belajar membaca Al-Qur'an bertahap, mulai dari huruf hijaiyah "
                "berharakat hingga bacaan panjang-pendek dan tajwid dasar pada tingkat 1–6.")
    if "makhraj" in t:
        return ("Makharijul huruf adalah tempat keluarnya huruf: rongga mulut (جوف), tenggorokan (حلق), "
                "lidah (لسان), dua bibir (شفتان), dan rongga hidung (خيشوم) untuk dengung.")
    if "tajwid" in t:
        return ("Tajwid adalah ilmu untuk membaca Al-Qur'an dengan benar, dengan memperhatikan "
                "makhraj huruf, sifat huruf, panjang-pendek, serta hukum bacaan.")
    if "fotosintesis" in t:
        return ("Fotosintesis adalah proses tumbuhan membuat makanan dengan bantuan cahaya matahari. "
                "Tumbuhan menggunakan air dari akar dan karbon dioksida dari udara, lalu menghasilkan "
                "gula sebagai makanan serta oksigen.")
    if "pantun" in t:
        return ("Contoh pantun:\n\n"
                "Pergi ke taman memetik melati,  \nHarumnya semerbak di pagi hari.  \n"
                "Rajin belajar sepenuh hati,  \nAgar tercapai cita-cita nanti.")
    if "mie goreng" in t or "mi goreng" in t:
        return ("Cara sederhana membuat mi goreng: rebus mi hingga matang lalu tiriskan. "
                "Tumis bawang putih dan telur, masukkan sayuran serta mi, tambahkan kecap dan bumbu "
                "secukupnya, aduk rata, lalu sajikan.")
    return ("OpenAI belum tersambung, jadi jawaban bawaan QORI AI masih terbatas. "
            "Tambahkan OPENAI_API_KEY yang valid pada file .env untuk mendapatkan jawaban umum "
            "dari GPT-4o-mini.")


def _chat_ai_baru(judul: str = "") -> dict:
    sekarang = datetime.now()
    return {
        "id": sekarang.strftime("%Y%m%d%H%M%S%f"),
        "judul": judul,
        "waktu": sekarang.strftime("%d/%m/%Y %H:%M"),
        "mode": "Ramah",
        "pesan": [],
    }


def _muat_chat_ai():
    if st.session_state.get("ai_sudah_dimuat"):
        return
    mentah = _baca_json(CHAT_AI_FILE, {})
    daftar = []
    for c in (mentah.get("percakapan") or []) if isinstance(mentah, dict) else []:
        if not isinstance(c, dict):
            continue
        pesan = []
        for i, m in enumerate(c.get("pesan") or []):
            if isinstance(m, (list, tuple)) and len(m) == 2:
                m = {"peran": m[0], "isi": m[1]}
            if not isinstance(m, dict) or not str(m.get("isi") or "").strip():
                continue
            pesan.append({
                "id": str(m.get("id") or f"{c.get('id', 'x')}-{i}"),
                "peran": m.get("peran") if m.get("peran") in ("user", "assistant") else "assistant",
                "isi": str(m.get("isi")),
                "waktu": str(m.get("waktu") or ""),
                "audio": str(m.get("audio") or ""),
                "audio_nama": str(m.get("audio_nama") or ""),
            })
        daftar.append({
            "id": str(c.get("id") or datetime.now().strftime("%Y%m%d%H%M%S%f")),
            "judul": str(c.get("judul") or ""),
            "waktu": str(c.get("waktu") or ""),
            "mode": c.get("mode") if c.get("mode") in MODE_AI else "Ramah",
            "pesan": pesan,
        })
    if not daftar:
        daftar = [_chat_ai_baru()]
    aktif = str(mentah.get("aktif") or "") if isinstance(mentah, dict) else ""
    if aktif not in {c["id"] for c in daftar}:
        aktif = daftar[-1]["id"]
    st.session_state.ai_percakapan = daftar
    st.session_state.ai_chat_aktif = aktif
    st.session_state.ai_sudah_dimuat = True


def _gabung_percakapan(lama, baru):
    peta = {}
    for c in list(lama or []) + list(baru or []):
        if not isinstance(c, dict) or not c.get("id"):
            continue
        if c["id"] not in peta:
            peta[c["id"]] = {
                **c,
                "pesan": [dict(m) for m in c.get("pesan", []) if isinstance(m, dict)],
            }
            continue
        target = peta[c["id"]]
        for kunci in ("judul", "waktu", "mode"):
            if c.get(kunci):
                target[kunci] = c[kunci]
        pesan = {m.get("id"): m for m in target["pesan"]}
        for m in c.get("pesan", []):
            if isinstance(m, dict) and m.get("id"):
                pesan[m["id"]] = m
        target["pesan"] = sorted(pesan.values(), key=lambda m: str(m.get("id", "")))
    return sorted(peta.values(), key=lambda c: str(c.get("id", "")))


def _simpan_chat_ai(gabung: bool = True):
    if "ai_percakapan" not in st.session_state:
        return
    daftar = st.session_state.ai_percakapan
    if gabung:
        disk = _baca_json(CHAT_AI_FILE, {})
        if isinstance(disk, dict) and disk.get("percakapan"):
            daftar = _gabung_percakapan(disk.get("percakapan"), daftar)
            st.session_state.ai_percakapan = daftar
    try:
        _tulis_json(CHAT_AI_FILE, {
            "versi": 1,
            "aktif": st.session_state.get("ai_chat_aktif"),
            "diperbarui": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "percakapan": daftar,
        })
    except Exception:
        st.session_state.ai_flash_error = T(
            "Riwayat chat gagal disimpan ke disk.",
            "Chat history could not be saved to disk.",
            "تعذر حفظ سجل الدردشة على القرص.")


def _chat_aktif() -> dict:
    _muat_chat_ai()
    daftar = st.session_state.ai_percakapan
    aktif = st.session_state.get("ai_chat_aktif")
    for c in daftar:
        if c["id"] == aktif:
            return c
    if not daftar:
        daftar.append(_chat_ai_baru())
    st.session_state.ai_chat_aktif = daftar[-1]["id"]
    return daftar[-1]


def _chat_tambah(peran: str, isi: str, audio: str = "", audio_nama: str = "") -> dict:
    c = _chat_aktif()
    sekarang = datetime.now()
    pesan = {
        "id": sekarang.strftime("%Y%m%d%H%M%S%f") + str(len(c["pesan"])),
        "peran": peran,
        "isi": isi,
        "waktu": sekarang.strftime("%d/%m/%Y %H:%M"),
        "audio": audio,
        "audio_nama": audio_nama,
    }
    c["pesan"].append(pesan)
    c["waktu"] = pesan["waktu"]
    if peran == "user" and not c["judul"]:
        judul = re.sub(r"\s+", " ", re.sub(r"[*_`#>|]", "", isi)).strip()
        c["judul"] = (judul[:46] + "…") if len(judul) > 46 else judul
    _simpan_chat_ai()
    if peran == "user" and st.session_state.get("user_role") == "Siswa":
        _qori_catat_aktivitas_siswa(
            "mengirim pesan ke AI Assistant.",
            menu="AI Assistant",
            event_key=f"chat:{st.session_state.get('user_name')}:{pesan['id']}",
        )
    return pesan


def _chat_hapus_semua():
    st.session_state.ai_percakapan = [_chat_ai_baru()]
    st.session_state.ai_chat_aktif = st.session_state.ai_percakapan[0]["id"]
    st.session_state.pop("ai_kuis", None)
    st.session_state.pop("ai_kuis_hasil", None)
    _simpan_chat_ai(gabung=False)


def _statistik_topik_ai():
    teks = []
    for c in st.session_state.get("ai_percakapan", []):
        for m in c.get("pesan", []):
            if m.get("peran") == "user":
                teks.append(m.get("isi", "").lower())
    hasil = []
    for nama, kunci in TOPIK_AI:
        jumlah = sum(1 for t in teks if any(k in t for k in kunci))
        if jumlah:
            hasil.append((nama, jumlah))
    return sorted(hasil, key=lambda x: (-x[1], x[0]))


def _deteksi_surah(teks: str):
    t = re.sub(r"[^a-z0-9]", "", teks.lower())
    kandidat = []
    for nomor, nama, ayat, _ in SURAH_JUZ30:
        pola = re.sub(r"[^a-z0-9]", "", nama.lower())
        if pola and pola in t:
            kandidat.append((len(pola), nomor, nama, ayat))
    if "fatihah" in t:
        kandidat.append((7, 1, "Al-Fatihah", 7))
    for arab, nomor, nama, ayat in (
        ("الناس", 114, "An-Nas", 6), ("الفاتحة", 1, "Al-Fatihah", 7),
        ("الإخلاص", 112, "Al-Ikhlas", 4), ("الكوثر", 108, "Al-Kautsar", 3),
    ):
        if arab in teks:
            kandidat.append((len(arab), nomor, nama, ayat))
    if not kandidat:
        return None
    return max(kandidat)[1:]


def _baris_ayat_md(baris, nomor_awal: int = 1) -> str:
    potong = []
    for i, (arab, latin, arti) in enumerate(baris, nomor_awal):
        potong.append(
            f"**{i}.**\n\n#### {arab}\n\n"
            f"**Latin:** {latin}  \n**Arti:** {arti}"
        )
    return "\n\n".join(potong)


def _jawab_ayat_ai(nomor: int) -> str:
    info = AYAT_AI.get(nomor)
    nama, jumlah = (info["nama"], info["ayat"]) if info else (
        SURAH_INFO.get(nomor, ("Surah", 0))[0], SURAH_INFO.get(nomor, ("Surah", 0))[1])
    if nomor == 114:
        isi = T(f"Surah **{nama}** terdiri dari **{jumlah} ayat** dan merupakan surah terakhir (ke-114) dalam Al-Qur'an.",
                f"Surah **{nama}** has **{jumlah} verses** and is the last surah (114th) in the Qur'an.",
                f"سورة **{nama}** تتكون من **{jumlah} آيات** وهي آخر سورة في القرآن (١١٤).")
    elif nomor == 1:
        isi = T(f"Surah **{nama}** terdiri dari **{jumlah} ayat** dan dibaca pada setiap rakaat shalat.",
                f"Surah **{nama}** has **{jumlah} verses** and is recited in every unit of prayer.",
                f"سورة **{nama}** تتكون من **{jumlah} آيات** وتُقرأ في كل ركعة من الصلاة.")
    elif nomor == 112:
        isi = T(f"Surah **{nama}** terdiri dari **{jumlah} ayat** dan menegaskan keesaan Allah (tauhid).",
                f"Surah **{nama}** has **{jumlah} verses** and affirms the oneness of Allah (tawhid).",
                f"سورة **{nama}** تتكون من **{jumlah} آيات** وتؤكد توحيد الله.")
    else:
        isi = T(f"Surah **{nama}** terdiri dari **{jumlah} ayat**.",
                f"Surah **{nama}** has **{jumlah} verses**.",
                f"سورة **{nama}** تتكون من **{jumlah} آيات**.")
    if info:
        contoh = AYAT_AI[nomor]["baris"][:1]
        isi += "\n\n" + T("Contoh ayat (Arab, Latin, Arti):", "Sample verse (Arabic, Latin, meaning):",
                          "مثال على الآية (عربي، لاتيني، معنى):") + "\n\n" + _baris_ayat_md(contoh)
    return isi


def _jawab_bacakan(nomor: int, nama: str, jumlah: int) -> str:
    nama_qori, sumber = audio_qori(qori_terpilih(), nomor)
    st.session_state.ai_audio_otomatis = {
        "src": sumber, "nama": nama_qori, "surah": nama,
    }
    info = AYAT_AI.get(nomor)
    baris = []
    if info:
        baris = info["baris"]
    else:
        data = ambil_surah(nomor)
        for a in (data.get("ayat") or [])[:10] if data else []:
            arab = str(a.get("teksArab") or "").strip()
            latin = str(a.get("teksLatin") or "").strip()
            arti = str(a.get("teksIndonesia") or "").strip()
            if arab:
                baris.append((arab, latin or "-", arti or "-"))
        if not baris:
            for arab, arti in FALLBACK_SURAH.get(nomor, []):
                baris.append((arab, "-", arti))
    kepala = T(
        f"**Murottal {nama}** ({jumlah} ayat) — diputar dengan suara **{nama_qori}**.",
        f"**{nama} recitation** ({jumlah} verses) — played in **{nama_qori}**'s voice.",
        f"**تلاوة سورة {nama}** ({jumlah} آيات) — بصوت **{nama_qori}**.")
    if baris:
        isi = kepala + "\n\n" + _baris_ayat_md(baris)
        if len(baris) < jumlah:
            isi += "\n\n_" + T(
                "Ditampilkan sebagian ayat; audio memutar surah lengkap.",
                "Only part of the verses are shown; the audio plays the full surah.",
                "تُعرض بعض الآيات فقط؛ الصوت يشغّل السورة كاملة.") + "_"
        return isi
    return kepala + "\n\n" + T(
        "Teks ayat tidak dapat dimuat sekarang, tetapi audio murottal tetap bisa diputar.",
        "The verse text could not be loaded, but the recitation audio can still play.",
        "تعذر تحميل نص الآيات، لكن يمكن تشغيل التلاوة.")


def _rentang_juz30(mulai: int, selesai: int) -> str:
    pos = 0
    bagian = []
    for _, nama, jumlah, _ in SURAH_JUZ30:
        awal, akhir = pos + 1, pos + jumlah
        lo, hi = max(mulai, awal), min(selesai, akhir)
        if lo <= hi:
            a, b = lo - pos, hi - pos
            bagian.append(f"{nama} {a}" if a == b else f"{nama} {a}–{b}")
        pos = akhir
    return ", ".join(bagian) or "-"


def _jadwal_hafalan_30() -> str:
    total = sum(jumlah for _, _, jumlah, _ in SURAH_JUZ30)
    baris = [
        T("### 📅 Jadwal Hafalan 1 Juz (Juz 30) — 30 Hari",
          "### 📅 30-Day Plan to Memorize 1 Juz (Juz 30)",
          "### 📅 جدول حفظ جزء واحد (الجزء ٣٠) — ٣٠ يومًا"),
        "",
        T("| Hari | Target Hafalan | Muraja'ah |", "| Day | Memorization target | Review |",
          "| اليوم | هدف الحفظ | المراجعة |"),
        "|---|---|---|",
    ]
    sebelumnya = 0
    for hari in range(1, 31):
        batas = total if hari == 30 else round(total * hari / 30)
        target = _rentang_juz30(sebelumnya + 1, batas)
        if hari == 1:
            ulang = T("Ulangi target hari ini 3×", "Repeat today's target 3×",
                      "كرر هدف اليوم ٣ مرات")
        else:
            ulang = T(f"Ulangi hari {hari - 1}", f"Review day {hari - 1}",
                      f"راجع يوم {hari - 1}")
        if hari in (7, 14, 21, 28):
            pekan = hari // 7
            ulang += " + " + T(f"setor pekan {pekan} ke guru",
                               f"recite week {pekan} to your teacher",
                               f"اعرض أسبوع {pekan} على المعلم")
        if hari == 30:
            ulang = T("Setoran penuh Juz 30 ke guru", "Full Juz 30 recitation to your teacher",
                      "تسميع الجزء ٣٠ كاملًا أمام المعلم")
        baris.append(f"| {hari} | {target} | {ulang} |")
        sebelumnya = batas
    baris += [
        "",
        "**" + T("Tips:", "Tips:", "نصائح:") + "**",
        "- " + T("Baca target baru 5–10× sebelum dihafal.",
                "Read the new target 5–10× before memorizing.",
                "اقرأ الهدف الجديد ٥–١٠ مرات قبل الحفظ."),
        "- " + T("Muraja'ah sebelum tidur dan setelah shalat.",
                "Review before sleeping and after prayer.",
                "راجع قبل النوم وبعد الصلاة."),
        "- " + T("Gunakan satu mushaf yang sama agar posisi ayat mudah diingat.",
                "Use the same mushaf so verse positions are easy to remember.",
                "استخدم نفس المصحف لسهولة تذكر مواضع الآيات."),
    ]
    return "\n".join(baris)


def _bersihkan_tts(teks: str) -> str:
    t = re.sub(r"```.*?```", " ", teks, flags=re.S)
    t = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", t)
    t = re.sub(r"https?://\S+", " ", t)
    t = re.sub(r"[*_#>`~|]+", " ", t)
    t = re.sub(r"\s+", " ", t)
    return t.strip()[:800]


def _bahasa_tts(teks: str) -> str:
    arab = len(re.findall(r"[\u0600-\u06FF]", teks))
    huruf = len(re.findall(r"[A-Za-z\u0600-\u06FF]", teks))
    if huruf and arab / huruf > 0.35:
        return "ar"
    return {"Indonesia": "id", "English": "en", "Arab": "ar"}.get(bahasa, "id")


@st.cache_data(ttl=3600, show_spinner=False)
def _tts_google(teks: str, kode_bahasa: str) -> bytes:
    data = b""
    for i in range(0, min(len(teks), 800), 160):
        potong = teks[i:i + 160]
        url = ("https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob"
               f"&tl={kode_bahasa}&q={quote(potong)}")
        try:
            req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urlopen(req, timeout=15) as resp:
                data += resp.read()
        except Exception:
            continue
    return data


def _transkrip_audio(berkas, kode_bahasa: str = "id"):
    client = get_openai_client()
    if client is None:
        return None, T(
            "Fitur suara membutuhkan OPENAI_API_KEY yang valid pada file .env.",
            "Voice features require a valid OPENAI_API_KEY in the .env file.",
            "تتطلب ميزات الصوت مفتاح OPENAI_API_KEY صالحًا في ملف .env.")
    isi = berkas.getvalue() if hasattr(berkas, "getvalue") else b""
    if not isi:
        return None, T("Rekaman audio kosong.", "The audio recording is empty.",
                       "التسجيل الصوتي فارغ.")
    nama = getattr(berkas, "name", None) or "rekaman.wav"
    mime = getattr(berkas, "type", None) or "audio/wav"
    try:
        with st.spinner(T("Mengubah suara menjadi teks...", "Transcribing speech...",
                          "جارٍ تحويل الصوت إلى نص...")):
            hasil = client.audio.transcriptions.create(
                model="whisper-1", file=(nama, isi, mime), language=kode_bahasa)
        teks = (getattr(hasil, "text", "") or "").strip()
        if not teks:
            return None, T("Suara belum terdeteksi dengan jelas. Coba rekam lagi.",
                           "Speech was not detected clearly. Please record again.",
                           "لم يتم التعرف على الصوت بوضوح. أعد التسجيل.")
        return teks, None
    except Exception:
        return None, T("Maaf, transkripsi audio gagal. Coba lagi sebentar.",
                       "Sorry, audio transcription failed. Please try again.",
                       "عذرًا، فشل تحويل الصوت. حاول مرة أخرى.")


def _normal_arab(teks: str) -> str:
    t = re.sub(r"[\u0610-\u061A\u064B-\u065F\u0670\u06D6-\u06ED]", "", teks)
    t = re.sub(r"[^\u0621-\u063A\u0641-\u064A\s]", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def _analisis_bacaan(berkas, nomor: int):
    info = SURAH_INFO.get(nomor)
    if not info:
        return None, T("Surah target tidak dikenal.", "Unknown target surah.",
                       "السورة المستهدفة غير معروفة.")
    nama, jumlah = info[0], info[1]
    data = ambil_surah(nomor)
    referensi = "\n".join(
        str(a.get("teksArab") or "") for a in (data.get("ayat") or [])) if data else ""
    if not referensi:
        info_lokal = AYAT_AI.get(nomor)
        if info_lokal:
            referensi = "\n".join(b[0] for b in info_lokal["baris"])
        else:
            referensi = "\n".join(a for a, _ in FALLBACK_SURAH.get(nomor, []))
    if not referensi:
        return None, T("Referensi ayat gagal dimuat. Periksa koneksi internet.",
                       "The verse reference could not be loaded. Check your internet connection.",
                       "تعذر تحميل مرجع الآيات. تحقق من اتصال الإنترنت.")

    isi = berkas.getvalue() if hasattr(berkas, "getvalue") else b""
    if not isi:
        return None, T("Berkas audio kosong.", "The audio file is empty.",
                       "ملف الصوت فارغ.")
    ext = Path(getattr(berkas, "name", "") or "audio.wav").suffix.lower().lstrip(".")
    if ext not in ("mp3", "wav"):
        ext = "wav"
    client = get_openai_client()
    skor = None
    ringkas = ""
    koreksi = []
    sumber = ""
    transkrip = ""

    if client is not None:
        try:
            b64 = base64.b64encode(isi).decode()
            with st.spinner(T("Menilai bacaan...", "Evaluating recitation...",
                              "جارٍ تقييم التلاوة...")):
                resp = client.chat.completions.create(
                    model="gpt-4o-audio-preview",
                    modalities=["text"],
                    messages=[{"role": "user", "content": [
                        {"type": "text", "text": (
                            f"Nilai bacaan Al-Qur'an surah {nama} berikut. "
                            "Balas dengan format: NILAI: <angka 0-100>; RINGKASAN: <2 kalimat>; "
                            "KOREKSI: <3 poin makhraj/tajwid yang perlu diperbaiki>. "
                            "Gunakan bahasa Indonesia yang mudah dipahami anak. "
                            "Jika audio bukan bacaan Al-Qur'an, katakan dengan jujur.")},
                        {"type": "input_audio", "input_audio": {"data": b64, "format": ext}},
                    ]}],
                    temperature=0.2,
                    max_tokens=350,
                )
            teks = (resp.choices[0].message.content or "").strip()
            cocok = re.search(r"NILAI\s*[:=]\s*(\d{1,3})", teks, re.I)
            if cocok:
                skor = max(0, min(100, int(cocok.group(1))))
            ringkas = re.sub(r"NILAI\s*[:=]\s*\d{1,3}", "", teks, flags=re.I).strip()
            sumber = T("Penilaian audio AI", "AI audio assessment", "تقييم صوتي بالذكاء الاصطناعي")
        except Exception:
            skor = None

    if skor is None:
        transkrip, galat = _transkrip_audio(berkas, "ar")
        if not transkrip:
            return None, galat
        rasio = difflib.SequenceMatcher(
            None, _normal_arab(transkrip), _normal_arab(referensi), autojunk=False).ratio()
        skor = max(40, min(98, round(50 + 48 * rasio)))
        sulit = [("ع", "'ain"), ("ح", "ha"), ("ق", "qaf"), ("ص", "shad"),
                 ("ض", "dhad"), ("ط", "tha"), ("ظ", "zha"), ("غ", "ghain"),
                 ("خ", "kha")]
        kurang = [f"huruf {nama_huruf} ({huruf})" for huruf, nama_huruf in sulit
                  if huruf in referensi and huruf not in transkrip][:3]
        if kurang:
            koreksi = [T("Perjelas makhraj ", "Clarify the makhraj of ",
                         "وضح مخرج ") + k for k in kurang]
        else:
            koreksi = [T("Jaga panjang-pendek mad dan dengung (ghunnah).",
                         "Keep the mad lengths and ghunnah consistent.",
                         "حافظ على مقادير المد والغنة."),
                       T("Ulangi ayat yang terlewat agar urutan hafalan rapi.",
                         "Repeat missed verses so the memorization order stays neat.",
                         "أعد الآيات الفائتة ليبقى ترتيب الحفظ منتظمًا.")]
        ringkas = T(
            f"Perkiraan awal dari transkripsi: {len(transkrip.split())} kata terbaca. "
            "Penilaian ini belum menggantikan telinga guru tahsin.",
            f"Initial estimate from transcription: {len(transkrip.split())} words detected. "
            "This assessment does not replace a tahsin teacher's ear.",
            f"تقدير أولي من النص: {len(transkrip.split())} كلمة. "
            "هذا التقييم لا يغني عن أذن معلم التحسين.")
        sumber = T("Perkiraan dari transkripsi", "Estimate from transcription",
                   "تقدير من النص المكتوب")

    judul = T(f"### 📊 Hasil Cek Bacaan — {nama}",
              f"### 📊 Recitation Check — {nama}",
              f"### 📊 نتيجة فحص التلاوة — {nama}")
    bagian = [judul, "", f"**{T('Nilai Tahsin', 'Tahsin score', 'درجة التحسين')}: {skor}/100**",
              "", ringkas]
    if koreksi:
        bagian += ["", f"**{T('Koreksi makhraj', 'Makhraj corrections', 'تصحيح المخارج')}:**"]
        bagian += [f"- {k}" for k in koreksi]
    if transkrip:
        bagian += ["", f"**{T('Transkrip pendengaran', 'Transcript', 'النص المسموع')}:** "
                       f"_{transkrip[:400]}_"]
    if sumber:
        bagian += ["", f"_{sumber} · {datetime.now().strftime('%d/%m/%Y %H:%M')}_"]
    return "\n".join(bagian), None


def _gaya_jawaban(jawaban: str, mode: str) -> str:
    if mode == "Tegas":
        return (T("**Mode Tegas — siap ujian.**", "**Firm mode — exam ready.**",
                  "**الوضع الحازم — استعداد للاختبار.**")
                + "\n\n" + jawaban + "\n\n> " + T(
                    "Catatan ujian: baca sekali lagi, lalu ulangi tanpa melihat.",
                    "Exam note: read once more, then repeat without looking.",
                    "ملاحظة الاختبار: اقرأ مرة أخرى ثم أعد دون النظر."))
    if mode == "Ustadz":
        return ("بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ\n\n" + jawaban + "\n\n_" + T(
            "Wallāhu a'lam bish-shawāb. Semoga Allah memberkahi ilmu kita.",
            "Wallāhu a'lam bish-shawāb. May Allah bless our knowledge.",
            "والله أعلم بالصواب. نسأل الله البركة في العلم.") + "_")
    return (T("Hai sahabat QORI! 😊", "Hi QORI friend! 😊", "مرحبًا يا صديق QORI! 😊")
            + "\n\n" + jawaban + "\n\n" + T(
                "Terus semangat belajar ya! 🌟", "Keep up the learning spirit! 🌟",
                "واصل حماسك في التعلم! 🌟"))


def _jawab_khusus(prompt: str):
    t = prompt.lower()
    if (("jadwal" in t or "plan" in t or "schedule" in t or "جدول" in t)
            and ("hafal" in t or "tahfidz" in t or "tahfiz" in t
                 or "memor" in t or "حفظ" in t)):
        return _jadwal_hafalan_30()
    surah = _deteksi_surah(t)
    if surah:
        nomor, nama, jumlah = surah
        if any(k in t for k in ["bacakan", "putar", "murottal", "dengarkan", "play",
                                "recite", "listen", "اقرأ"]):
            return _jawab_bacakan(nomor, nama, jumlah)
        if any(k in t for k in ["berapa ayat", "arti", "terjemah", "makna", "ayat 1",
                                "how many", "verse", "meaning", "translation",
                                "عدد آيات", "معنى"]):
            return _jawab_ayat_ai(nomor)
    return None


def _prompt_sebelum(pesan, indeks: int) -> str:
    for i in range(indeks - 1, -1, -1):
        if pesan[i].get("peran") == "user":
            return pesan[i].get("isi", "")
    return ""


def _kuis_lokal(prompt: str, jawaban: str) -> list:
    semua = []
    for bank in BANKS.values():
        if not isinstance(bank, list):
            continue
        for s in bank:
            if isinstance(s, dict) and s.get("options") and s.get("answer") in s["options"]:
                semua.append(s)
    stop = {"yang", "dengan", "dalam", "untuk", "adalah", "pada", "dari", "atau",
            "this", "that", "dengan", "kamu", "kita", "akan", "agar", "juga"}
    kunci = [k for k in re.findall(r"[a-zA-Z']{4,}", (prompt + " " + jawaban).lower())
             if k not in stop][:25]
    cocok, terpakai = [], set()
    for s in semua:
        teks = (s.get("prompt", "") + " " + s.get("bahas", "")).lower()
        if any(k in teks for k in kunci) and s["prompt"] not in terpakai:
            cocok.append(s)
            terpakai.add(s["prompt"])
    rng = random.Random(len(prompt) * 31 + len(jawaban))
    rng.shuffle(cocok)
    pilih = cocok[:5]
    if len(pilih) < 5:
        sisa = [s for s in semua if s["prompt"] not in terpakai]
        rng.shuffle(sisa)
        pilih += sisa[:5 - len(pilih)]
    return [{
        "q": s["prompt"], "options": list(s["options"]), "answer": s["answer"],
        "bahas": s.get("bahas", ""), "arab": s.get("arab") or "",
    } for s in pilih]


def _buat_kuis(prompt: str, jawaban: str) -> dict:
    soal = []
    client = get_openai_client()
    if client is not None:
        try:
            with st.spinner(T("Menyusun 5 soal kuis...", "Creating 5 quiz questions...",
                              "جارٍ إعداد ٥ أسئلة...")):
                resp = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": (
                            "Kamu pembuat soal untuk anak belajar Al-Qur'an. Balas HANYA JSON array "
                            "berisi tepat 5 objek: {\"q\": \"soal\", \"options\": [4 pilihan], "
                            "\"answer\": indeks jawaban benar 0-3, \"bahas\": \"penjelasan singkat\"}. "
                            f"Gunakan bahasa {bahasa}.")},
                        {"role": "user", "content": (
                            f"Pertanyaan siswa: {prompt[:600]}\n\nMateri jawaban:\n"
                            f"{jawaban[:2500]}")},
                    ],
                    temperature=0.5,
                    max_tokens=900,
                )
            mentah = (resp.choices[0].message.content or "").strip()
            cocok = re.search(r"\[.*\]", mentah, re.S)
            data = json.loads(cocok.group(0)) if cocok else []
            for item in data[:5]:
                opsi = [str(o) for o in (item.get("options") or [])][:4]
                if not item.get("q") or len(opsi) < 2:
                    continue
                idx = item.get("answer", 0)
                if isinstance(idx, str):
                    idx = opsi.index(idx) if idx in opsi else 0
                idx = max(0, min(len(opsi) - 1, int(idx)))
                soal.append({"q": str(item["q"]), "options": opsi,
                             "answer": opsi[idx], "bahas": str(item.get("bahas", "")),
                             "arab": ""})
        except Exception:
            soal = []
    if len(soal) < 5:
        lokal = _kuis_lokal(prompt, jawaban)
        ada = {s["q"] for s in soal}
        soal += [s for s in lokal if s["q"] not in ada]
    return {
        "id": datetime.now().strftime("%H%M%S%f"),
        "topik": (prompt[:52] + "…") if len(prompt) > 52 else (prompt or "QORI AI"),
        "soal": soal[:5],
    }


def _markdown_ke_html(teks: str) -> str:
    aman = html.escape(teks)
    aman = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", aman, flags=re.S)
    aman = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<i>\1</i>", aman)
    aman = re.sub(r"_(.+?)_", r"<i>\1</i>", aman)
    aman = re.sub(r"^#{1,6}\s*(.+)$", r"<b>\1</b>", aman, flags=re.M)
    aman = re.sub(r"^>\s*(.+)$", r"<i>\1</i>", aman, flags=re.M)
    aman = re.sub(r"^-\s+", "• ", aman, flags=re.M)
    return aman.replace("\n", "<br>")


def _simpan_ke_materi(teks: str, mode_materi: str, level: int):
    isi = _markdown_ke_html(teks)
    blok = ("<div class=\"materi-box\"><b>🤖 QORI AI · "
            + datetime.now().strftime("%d/%m/%Y %H:%M") + "</b><br>" + isi + "</div>")
    lama = MATERI.get(mode_materi, {}).get(int(level), "")
    MATERI[mode_materi][int(level)] = (lama + "<br><br>" + blok) if lama else blok
    _tulis_semua(st.session_state.data)


def jawab_openai(prompt: str, mode: str = "Ramah"):
    client = get_openai_client()
    if client is None:
        return None
    gaya = {
        "Ramah": "Gunakan gaya ramah untuk anak: sapaan hangat, bahasa sederhana, beri semangat.",
        "Tegas": ("Gunakan gaya tegas seperti penguji: langsung ke inti, poin-poin ringkas, "
                  "tandai kesalahan umum, tanpa basa-basi."),
        "Ustadz": ("Gunakan gaya ustadz yang tenang dan berwibawa: awali bismillah, beri nasihat "
                   "singkat, dan akhiri dengan doa ringan."),
    }.get(mode, "Gunakan gaya ramah untuk anak.")
    bahasa_inst = {
        "Indonesia": "Jawab sepenuhnya dalam bahasa Indonesia.",
        "English": "Answer fully in English; keep Arabic verses with Latin transliteration and meaning.",
        "Arab": "أجب باللغة العربية الفصحى المبسطة، مع الحفاظ على الآيات.",
    }.get(bahasa, "Jawab dalam bahasa Indonesia.")
    try:
        riwayat = [
            {"role": m.get("peran") if m.get("peran") in ("user", "assistant") else "user",
             "content": m.get("isi", "")}
            for m in _chat_aktif().get("pesan", [])[-8:]
        ]
        with st.spinner(T("QORI AI sedang menyiapkan jawaban...",
                          "QORI AI is preparing an answer...",
                          "QORI AI يجهّز الإجابة...")):
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": (
                        f"{SYSTEM_PROMPT_AI}\n\n{gaya}\n"
                        f"ATURAN BAHASA (WAJIB, utamakan ini): {bahasa_inst} "
                        "Abaikan instruksi bahasa lain di atas bila bertentangan.")},
                    *riwayat,
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
                max_tokens=600,
            )
        return completion.choices[0].message.content or None
    except Exception:
        return None


def jawab_ai_terpadu(prompt: str, mode: str = "Ramah") -> str:
    khusus = _jawab_khusus(prompt)
    if khusus:
        return khusus
    jawaban = jawab_openai(prompt, mode)
    if jawaban:
        return jawaban
    jawaban = _gaya_jawaban(jawab_ai(prompt), mode)
    if OPENAI_API_KEY and OpenAI is not None:
        jawaban += "\n\n_" + T(
            "Koneksi OpenAI gagal — menampilkan jawaban bawaan QORI AI.",
            "OpenAI connection failed — showing QORI AI's built-in answer.",
            "فشل الاتصال بـ OpenAI — يتم عرض إجابة QORI AI المدمجة.") + "_"
    return jawaban


def _ai_proses(prompt: str):
    c = _chat_aktif()
    mode = c.get("mode", "Ramah")
    st.session_state.pop("ai_audio_otomatis", None)
    jawaban = jawab_ai_terpadu(prompt, mode)
    audio = st.session_state.pop("ai_audio_otomatis", None) or {}
    _chat_tambah("user", prompt)
    pesan = _chat_tambah(
        "assistant", jawaban, audio.get("src", ""),
        f"{audio.get('nama', '')} · {audio.get('surah', '')}".strip(" ·"))
    if audio:
        st.session_state.ai_autoplay_id = pesan["id"]
    st.session_state.pop("ai_kuis", None)
    st.session_state.pop("ai_kuis_hasil", None)


def page_ai_assistant():
    st.markdown(f"""
    <div class="hero-small">
      <h2>🤖 QORI AI Assistant</h2>
      <p>{T("Asisten AI serbaguna untuk belajar, berkarya, dan bertanya.",
           "A versatile AI assistant to learn, create, and ask questions.",
           "مساعد ذكاء اصطناعي متعدد الاستخدامات للتعلم والإبداع والاستفسار.")}</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <style>
    .stChatMessage{background:var(--secondary-background-color);color:var(--text-color);
      border:1px solid color-mix(in srgb, var(--text-color) 16%, transparent);
      border-radius:16px;padding:6px 14px}
    .stChatMessage p,.stChatMessage li{color:var(--text-color)}
    .stChatMessage h4{color:var(--text-color);line-height:2}
    </style>
    """, unsafe_allow_html=True)
    _muat_chat_ai()
    _awal = st.session_state.pop("ai_prompt_awal", None)
    if _awal:
        _ai_proses(_awal)
        st.rerun()
    c = _chat_aktif()
    pesan = c["pesan"]
    if st.session_state.get("ai_flash"):
        st.success(st.session_state.pop("ai_flash"))
    if st.session_state.get("ai_flash_error"):
        st.error(st.session_state.pop("ai_flash_error"))

    kol_riwayat, kol_utama = st.columns([1, 2.7], gap="large")

    with kol_riwayat:
        st.markdown("#### 🕘 " + T("Riwayat Chat", "Chat History", "سجل الدردشة"))
        with st.container(height=280):
            for cc in reversed(st.session_state.ai_percakapan):
                judul = cc["judul"] or T("Chat Baru", "New chat", "دردشة جديدة")
                aktif = cc["id"] == c["id"]
                if st.button(
                    ("● " if aktif else "💬 ") + judul[:36],
                    key=f"ai_buka_{cc['id']}", use_container_width=True,
                    type="primary" if aktif else "secondary",
                    help=f"{cc['waktu']} · {len(cc['pesan'])} " + T("pesan", "messages", "رسالة"),
                ):
                    st.session_state.ai_chat_aktif = cc["id"]
                    st.session_state.pop("ai_kuis", None)
                    st.session_state.pop("ai_kuis_hasil", None)
                    st.rerun()
        st.markdown("#### 🔥 " + T("Pertanyaan Sering Ditanyakan",
                                   "Frequently Asked Questions",
                                   "الأسئلة المتكررة"))
        topik = _statistik_topik_ai()
        if topik:
            st.caption(T(f"Siswa paling sering bertanya tentang {topik[0][0]}.",
                         f"Students ask most often about {topik[0][0]}.",
                         f"الطلاب يسألون غالبًا عن {topik[0][0]}."))
            for nama, jumlah in topik[:5]:
                st.markdown(f"- **{nama}** — {jumlah}×")
        else:
            st.caption(T("Belum ada pertanyaan siswa yang tercatat.",
                         "No student questions recorded yet.",
                         "لا توجد أسئلة طلاب مسجلة بعد."))

    with kol_utama:
        kiri, kanan = st.columns([2, 1.6], vertical_alignment="center")
        with kiri:
            st.markdown("### 💬 " + T("Percakapan", "Conversation", "المحادثة"))
        with kanan:
            b1, b2 = st.columns(2)
            with b1:
                if st.button("➕ " + T("Chat Baru", "New Chat", "دردشة جديدة"),
                             key="ai_chat_baru", use_container_width=True):
                    if pesan:
                        baru = _chat_ai_baru()
                        st.session_state.ai_percakapan.append(baru)
                        st.session_state.ai_chat_aktif = baru["id"]
                        _simpan_chat_ai()
                    else:
                        st.session_state.ai_flash = T(
                            "Chat ini masih kosong. Silakan mulai bertanya.",
                            "This chat is still empty. Start asking a question.",
                            "هذه الدردشة فارغة. ابدأ بسؤال.")
                    st.rerun()
            with b2:
                with st.popover("🗑️ " + T("Hapus Riwayat", "Clear History", "حذف السجل"),
                                use_container_width=True):
                    st.caption(T("Semua percakapan akan dihapus dari perangkat ini.",
                                 "All conversations will be deleted from this device.",
                                 "ستُحذف جميع المحادثات من هذا الجهاز."))
                    yakin = st.checkbox(T("Saya yakin ingin menghapus semua riwayat.",
                                          "I am sure I want to delete all history.",
                                          "أنا متأكد من حذف كل السجل."),
                                        key="ai_yakin_hapus")
                    if st.button(T("Hapus Semua", "Delete All", "حذف الكل"),
                                 key="ai_hapus_semua", disabled=not yakin):
                        _chat_hapus_semua()
                        st.session_state.ai_flash = T(
                            "Riwayat chat berhasil dihapus.",
                            "Chat history has been deleted.",
                            "تم حذف سجل الدردشة.")
                        st.rerun()

        mode_pilih = st.segmented_control(
            T("Pilih Mode Jawaban", "Answer Mode", "وضع الإجابة"),
            options=list(MODE_AI), default=c.get("mode", "Ramah"),
            format_func=lambda m: T(*MODE_AI[m]), key=f"ai_mode_{c['id']}")
        if mode_pilih and mode_pilih != c.get("mode"):
            c["mode"] = mode_pilih
            _simpan_chat_ai()

        if not pesan:
            st.markdown("**" + T("💡 Pilih kategori, lalu klik pertanyaan",
                                  "💡 Choose a category, then click a question",
                                  "💡 اختر فئة ثم اضغط على سؤال") + "**")
            label_kat = {
                "Tajwid": T("Tajwid", "Tajweed", "التجويد"),
                "Tahfidz": T("Tahfidz", "Memorization", "التحفيظ"),
                "Arti Ayat": T("Arti Ayat", "Verse Meaning", "معاني الآيات"),
                "Fiqih": T("Fiqih", "Fiqh", "الفقه"),
            }
            kategori = st.segmented_control(
                T("Kategori", "Category", "الفئة"), options=list(KATEGORI_AI),
                default="Tajwid", format_func=lambda k: label_kat[k],
                key="ai_kategori") or "Tajwid"
            for i, (id_q, en_q, ar_q) in enumerate(KATEGORI_AI[kategori]):
                if st.button(T(id_q, en_q, ar_q), key=f"ai_saran_{kategori}_{i}",
                             use_container_width=True):
                    _ai_proses(id_q)
                    st.rerun()

        def aksi_jawaban(m, idx):
            k1, k2, k3 = st.columns(3)
            with k1:
                if st.button("🔊 " + T("Putar", "Play", "تشغيل"),
                             key=f"ai_tts_{c['id']}_{idx}", use_container_width=True,
                             help=T("Putar jawaban dengan suara Qori pilihan",
                                    "Play the answer in the selected Qori's voice",
                                    "شغّل الإجابة بصوت القارئ المختار")):
                    if m.get("audio"):
                        st.audio(m["audio"], format="audio/mpeg", autoplay=True)
                        st.caption(("🎧 " + m.get("audio_nama", "")).strip(" ·"))
                    else:
                        teks = _bersihkan_tts(m["isi"])
                        audio = _tts_google(teks, _bahasa_tts(m["isi"])) if teks else b""
                        if audio:
                            st.audio(audio, format="audio/mpeg", autoplay=True)
                            st.caption(T(
                                "Dibacakan dengan TTS. Suara Qori pilihan dipakai untuk murottal surah.",
                                "Read aloud with TTS. The selected Qori's voice is used for surah recitation.",
                                "تُقرأ بصوت اصطناعي. يُستخدم صوت القارئ المختار لتلاوة السور."))
                        else:
                            st.warning(T("Audio belum bisa dimuat. Periksa koneksi internet.",
                                         "Audio could not be loaded. Check your internet connection.",
                                         "تعذر تحميل الصوت. تحقق من اتصال الإنترنت."))
            with k2:
                with st.popover("📚 " + T("Materi", "Material", "المادة"),
                                use_container_width=True):
                    mode_materi = st.selectbox(
                        T("Kategori materi", "Material category", "فئة المادة"),
                        MODE_LIST, key=f"ai_sm_mode_{c['id']}_{idx}")
                    level_materi = st.selectbox(
                        T("Level", "Level", "المستوى"), list(range(1, MAX_LEVEL + 1)),
                        key=f"ai_sm_level_{c['id']}_{idx}")
                    if st.button(T("Simpan ke Materi", "Save to Material", "حفظ في المادة"),
                                 key=f"ai_sm_btn_{c['id']}_{idx}", type="primary",
                                 disabled=aku_pengelola() and not _boleh_ubah()):
                        _simpan_ke_materi(m["isi"], mode_materi, level_materi)
                        st.session_state.ai_flash = T(
                            f"Jawaban disimpan ke Materi {mode_materi} level {level_materi}.",
                            f"Answer saved to {mode_materi} material level {level_materi}.",
                            f"تم حفظ الإجابة في مادة {mode_materi} المستوى {level_materi}.")
                        st.rerun()
            with k3:
                if st.button("📝 " + T("Kuis", "Quiz", "اختبار"),
                             key=f"ai_kuis_btn_{c['id']}_{idx}", use_container_width=True,
                             help=T("Buatkan kuis 5 soal dari jawaban ini",
                                    "Create a 5-question quiz from this answer",
                                    "أنشئ اختبارًا من ٥ أسئلة من هذه الإجابة")):
                    st.session_state.ai_kuis = _buat_kuis(
                        _prompt_sebelum(pesan, idx), m["isi"])
                    st.session_state.pop("ai_kuis_hasil", None)
                    st.rerun()

        for idx, m in enumerate(pesan):
            with st.chat_message(m["peran"]):
                st.markdown(m["isi"])
                if m["peran"] == "assistant":
                    if m.get("audio"):
                        putar = st.session_state.get("ai_autoplay_id") == m["id"]
                        st.audio(m["audio"], format="audio/mpeg", autoplay=putar)
                        if putar:
                            st.session_state.ai_autoplay_id = ""
                        st.caption("🎧 " + m.get("audio_nama", ""))
                    aksi_jawaban(m, idx)

        kuis = st.session_state.get("ai_kuis")
        if kuis:
            with st.expander("📝 " + T("Kuis 5 Soal", "5-Question Quiz", "اختبار ٥ أسئلة")
                             + f" — {kuis['topik']}", expanded=True):
                for i, soal in enumerate(kuis.get("soal", [])):
                    st.markdown(f"**{i + 1}. {soal['q']}**")
                    if soal.get("arab"):
                        st.markdown(f"#### {soal['arab']}")
                    st.radio(
                        T("Pilih jawaban", "Choose an answer", "اختر إجابة"),
                        soal["options"], index=None, label_visibility="collapsed",
                        key=f"ai_kuis_{kuis['id']}_{i}")
                if st.button(T("✅ Periksa Jawaban", "✅ Check Answers", "✅ تحقق من الإجابات"),
                             key=f"ai_kuis_periksa_{kuis['id']}"):
                    benar = 0
                    for i, soal in enumerate(kuis.get("soal", [])):
                        if st.session_state.get(f"ai_kuis_{kuis['id']}_{i}") == soal["answer"]:
                            benar += 1
                    st.session_state.ai_kuis_hasil = benar
                if st.session_state.get("ai_kuis_hasil") is not None:
                    hasil = st.session_state.ai_kuis_hasil
                    st.success(T(f"Skor kamu: {hasil}/5. Terus berlatih!",
                                 f"Your score: {hasil}/5. Keep practicing!",
                                 f"درجتك: {hasil}/5. واصل التدريب!"))
                    for i, soal in enumerate(kuis.get("soal", [])):
                        st.markdown(f"{i + 1}. **{soal['answer']}** — {soal.get('bahas', '')}")
                if st.button(T("Tutup Kuis", "Close Quiz", "إغلاق الاختبار"),
                             key=f"ai_kuis_tutup_{kuis['id']}"):
                    st.session_state.pop("ai_kuis", None)
                    st.session_state.pop("ai_kuis_hasil", None)
                    st.rerun()

        with st.expander("🎙️ " + T("Upload Audio Bacaan — Koreksi Tajwid",
                                    "Upload Recitation — Tajwid Check",
                                    "رفع تلاوة — تصحيح التجويد")):
            st.caption(T(
                "Unggah rekaman mp3/wav, pilih surah, lalu QORI AI memberi nilai Tahsin "
                "dan koreksi makhraj.",
                "Upload an mp3/wav recording, choose a surah, and QORI AI will give a Tahsin "
                "score and makhraj corrections.",
                "ارفع تسجيلًا بصيغة mp3/wav، اختر السورة، وسيعطيك QORI AI درجة التحسين وتصحيح المخارج."))
            kol_s, kol_f = st.columns([1, 1.6])
            with kol_s:
                nomor_target = st.selectbox(
                    T("Surah target", "Target surah", "السورة المستهدفة"),
                    options=[n for n, _, _, _ in SURAH_JUZ30],
                    format_func=lambda n: f"{SURAH_INFO[n][0]} ({SURAH_INFO[n][1]} ayat)",
                    key="ai_cek_surah")
            with kol_f:
                berkas_bacaan = st.file_uploader(
                    T("Rekaman bacaan (mp3/wav)", "Recitation file (mp3/wav)",
                      "ملف التلاوة (mp3/wav)"),
                    type=["mp3", "wav"], key="ai_cek_berkas")
            if berkas_bacaan is not None:
                st.audio(berkas_bacaan)
            if st.button("📊 " + T("Nilai Bacaan", "Score Recitation", "قيّم التلاوة"),
                         key="ai_cek_mulai", type="primary",
                         disabled=berkas_bacaan is None):
                hasil, galat = _analisis_bacaan(berkas_bacaan, nomor_target)
                if galat:
                    st.session_state.ai_flash_error = galat
                else:
                    _chat_tambah("user", "🎙️ " + T(
                        f"Cek bacaan Surah {SURAH_INFO[nomor_target][0]}",
                        f"Recitation check for Surah {SURAH_INFO[nomor_target][0]}",
                        f"فحص تلاوة سورة {SURAH_INFO[nomor_target][0]}"))
                    _chat_tambah("assistant", hasil)
                    st.session_state.ai_flash = T(
                        "Hasil penilaian bacaan sudah masuk ke riwayat chat.",
                        "The recitation result has been added to chat history.",
                        "تمت إضافة نتيجة التلاوة إلى سجل الدردشة.")
                st.rerun()

        kol_mic, kol_info = st.columns([1.15, 2.4], vertical_alignment="center")
        with kol_mic:
            with st.popover("🎤 " + T("Suara ke Teks", "Speech to Text", "الصوت إلى نص"),
                            use_container_width=True):
                st.caption(T("Rekam pertanyaanmu, lalu otomatis dikirim ke QORI AI.",
                             "Record your question; it will be sent to QORI AI automatically.",
                             "سجّل سؤالك وسيُرسل تلقائيًا إلى QORI AI."))
                rekaman = st.audio_input(
                    T("Rekam pertanyaan", "Record your question", "سجّل سؤالك"),
                    key="ai_mic")
                if rekaman is not None:
                    cap = hashlib.md5(rekaman.getvalue()).hexdigest()
                    if cap != st.session_state.get("ai_mic_hash"):
                        st.session_state.ai_mic_hash = cap
                        teks_suara, galat_suara = _transkrip_audio(rekaman, "id")
                        if teks_suara:
                            _ai_proses(teks_suara)
                            st.session_state.ai_flash = T(
                                "Pertanyaan suara berhasil diubah menjadi teks.",
                                "Your spoken question was converted to text.",
                                "تم تحويل سؤالك الصوتي إلى نص.")
                        else:
                            st.session_state.ai_flash_error = galat_suara
                        st.rerun()
        with kol_info:
            st.caption(T(
                "Tombol 🔊 Putar, 📚 Simpan ke Materi, dan 📝 Kuis ada di bawah setiap jawaban AI.",
                "The 🔊 Play, 📚 Save to Material, and 📝 Quiz buttons appear under every AI answer.",
                "تظهر أزرار 🔊 التشغيل و📚 الحفظ في المادة و📝 الاختبار أسفل كل إجابة."))

        prompt = st.chat_input(T("Tanyakan apa saja kepada QORI AI...",
                                 "Ask QORI AI anything...",
                                 "اسأل QORI AI عن أي شيء..."))
        if prompt:
            _ai_proses(prompt)
            st.rerun()


# ---------------------------------------------------------------------------
# AUTOSAVE PRA-RENDER
# Widget state Streamlit sudah diperbarui sebelum script rerun dimulai.
# Simpan di sini agar perubahan tetap tersimpan walau halaman melakukan st.rerun()/st.stop().
# ---------------------------------------------------------------------------
_qori_pantau_perubahan_global()

# ---------------------------------------------------------------------------
# Router
# ---------------------------------------------------------------------------
if menu == "Dashboard":
    page_dashboard()
elif menu == "Belajar & Game":
    page_belajar()
elif menu == "Terkunci":
    page_terkunci()
elif menu == "Ujian":
    page_ujian()
elif menu == "Nilai & Hasil":
    page_nilai()
elif menu == "Leaderboard":
    page_leaderboard()
elif menu == "Materi":
    page_materi()
elif menu == "Al-Qur'an (Juz 30)":
    page_quran()
elif menu == "AI Assistant":
    page_ai_assistant()
elif menu == "Data Siswa":
    page_siswa()
elif menu == "Kelola Pengelola":
    page_kelola_pengelola()
elif menu == "Pengaturan":
    page_pengaturan()

# Autosave global untuk perubahan pada semua menu yang tercermin di state/berkas.
_qori_pantau_perubahan_global()
if st.session_state.pop("_qori_global_refresh_after_autosave", False):
    st.rerun()
_qori_waktu_tampil = st.session_state.get("_qori_global_last_saved") or "Belum ada penyimpanan"
st.caption("🕒 Terakhir disimpan: " + str(_qori_waktu_tampil) + " WIB")
if st.session_state.get("_qori_global_save_error"):
    st.warning("⚠️ Sinkronisasi global belum berhasil: " + str(st.session_state.get("_qori_global_save_error")))

st.markdown("""
<div style="text-align:center;color:#8291aa;font-size:11px;padding:24px 0 5px">
  © 2026 QORI AI · Islamic Learning Management System · Belajar Al-Qur'an dengan lebih interaktif
</div>
""", unsafe_allow_html=True)
