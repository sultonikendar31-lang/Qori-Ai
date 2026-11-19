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
DB = os.environ.get("QORI_DB_PATH", "qori_ai.db")
def db():
    c = sqlite3.connect(DB, check_same_thread=False, timeout=30)
    c.execute("PRAGMA journal_mode=WAL")
    c.execute("PRAGMA foreign_keys=ON")
    c.execute("CREATE TABLE IF NOT EXISTS hasil (nama TEXT PRIMARY KEY, nilai INTEGER, ulang INTEGER)")
    c.execute("CREATE TABLE IF NOT EXISTS aktivitas (id INTEGER PRIMARY KEY AUTOINCREMENT, nama TEXT, kelas TEXT, aktivitas TEXT, jam TEXT, lama TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS saran (id INTEGER PRIMARY KEY AUTOINCREMENT, pengirim TEXT, label TEXT, role TEXT, jenis TEXT, isi TEXT, jam TEXT, balasan TEXT, pembalas TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS ujian_sesi (nama TEXT PRIMARY KEY, mulai REAL NOT NULL, seed INTEGER NOT NULL)")
    c.execute("""CREATE TABLE IF NOT EXISTS game_scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama TEXT NOT NULL, kelas TEXT NOT NULL, game TEXT NOT NULL,
        skor INTEGER NOT NULL, jam TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS game_attempts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        attempt_id TEXT NOT NULL UNIQUE,
        nama TEXT NOT NULL, kelas TEXT NOT NULL, game TEXT NOT NULL,
        level INTEGER NOT NULL, skor INTEGER NOT NULL,
        benar INTEGER NOT NULL, total_soal INTEGER NOT NULL,
        jam TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS setoran (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pengirim TEXT, label TEXT, kategori TEXT, judul TEXT, keterangan TEXT,
        foto BLOB, foto_nama TEXT, audio BLOB, audio_nama TEXT,
        jam TEXT, koreksi TEXT, pembalas TEXT, nilai_setoran TEXT
    )""")
    c.commit()
    return c
CONN = db()
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
def hapus_hasil_satu(nama):
    CONN.execute("DELETE FROM hasil WHERE nama=?", (nama,))
    CONN.execute("DELETE FROM ujian_sesi WHERE nama=?", (nama,))
    CONN.commit()
def reset_semua_hasil():
    CONN.execute("DELETE FROM hasil")
    CONN.execute("DELETE FROM ujian_sesi")
    CONN.commit()
def get_aktivitas():
    return [{"nama":r[0],"kelas":r[1],"aktivitas":r[2],"jam":r[3],"lama":r[4]} for r in CONN.execute("SELECT nama,kelas,aktivitas,jam,lama FROM aktivitas ORDER BY id DESC")]
def tambah_aktivitas(nama, kelas, aktivitas, jam, lama):
    CONN.execute("INSERT INTO aktivitas(nama,kelas,aktivitas,jam,lama) VALUES(?,?,?,?,?)", (nama, kelas, aktivitas, jam, lama))
    CONN.commit()
def hapus_riwayat_satu(nama):
    CONN.execute("DELETE FROM aktivitas WHERE nama=?", (nama,))
    CONN.commit()
def reset_semua_riwayat():
    CONN.execute("DELETE FROM aktivitas")
    CONN.commit()

def simpan_skor_game(nama, kelas, game, skor):
    CONN.execute(
        "INSERT INTO game_scores(nama,kelas,game,skor,jam) VALUES(?,?,?,?,datetime('now','localtime'))",
        (nama, kelas, game, skor)
    )
    CONN.commit()

def get_leaderboard():
    rows = CONN.execute("""
        SELECT nama, kelas, SUM(skor), COUNT(*), GROUP_CONCAT(game, ', ')
        FROM game_scores GROUP BY nama, kelas
        ORDER BY SUM(skor) DESC, COUNT(*) DESC, nama ASC
    """).fetchall()
    return [{"nama":r[0],"kelas":r[1],"total":r[2],"jumlah_main":r[3],"game":r[4] or "-"} for r in rows]

def reset_leaderboard():
    CONN.execute("DELETE FROM game_scores")
    CONN.execute("DELETE FROM game_attempts")
    CONN.commit()

def simpan_hasil_game(attempt_id, nama, kelas, game, level, skor, total_soal=25):
    """Simpan satu hasil akhir sesi game; attempt_id mencegah duplikasi saat rerun."""
    benar = int(skor // 10)
    CONN.execute(
        """INSERT OR IGNORE INTO game_attempts
        (attempt_id,nama,kelas,game,level,skor,benar,total_soal,jam)
        VALUES(?,?,?,?,?,?,?,?,datetime('now','localtime'))""",
        (attempt_id, nama, kelas, game, int(level), int(skor), benar, int(total_soal))
    )
    CONN.commit()

def get_rekap_nilai_game(nama_game):
    """Nilai terbaik dan jumlah percobaan per siswa pada setiap level game."""
    rows = CONN.execute(
        """SELECT nama, kelas, level, MAX(skor), COUNT(*), MAX(jam)
        FROM game_attempts WHERE game=?
        GROUP BY nama, kelas, level
        ORDER BY nama COLLATE NOCASE, level""",
        (nama_game,)
    ).fetchall()
    hasil = {}
    for nama, kelas, level, skor, jumlah, jam in rows:
        hasil.setdefault(nama, {"kelas": kelas, "level": {}})
        hasil[nama]["level"][int(level)] = {
            "skor": int(skor), "percobaan": int(jumlah), "jam": jam
        }
    return hasil

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
def tambah_setoran(pengirim, label, kategori, judul, keterangan, foto_bytes, foto_nama, audio_bytes, audio_nama, jam):
    CONN.execute("INSERT INTO setoran(pengirim,label,kategori,judul,keterangan,foto,foto_nama,audio,audio_nama,jam,koreksi,pembalas,nilai_setoran) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (pengirim, label, kategori, judul, keterangan, foto_bytes, foto_nama, audio_bytes, audio_nama, jam, "", "", ""))
    CONN.commit()
def get_setoran():
    rows = CONN.execute("SELECT id,pengirim,label,kategori,judul,keterangan,foto,foto_nama,audio,audio_nama,jam,koreksi,pembalas,nilai_setoran FROM setoran ORDER BY id DESC").fetchall()
    out = []
    for r in rows:
        out.append({"id":r[0],"pengirim":r[1],"label":r[2],"kategori":r[3],"judul":r[4],"keterangan":r[5] or "","foto":r[6],"foto_nama":r[7] or "","audio":r[8],"audio_nama":r[9] or "","jam":r[10],"koreksi":r[11] or "","pembalas":r[12] or "","nilai":r[13] or ""})
    return out
def koreksi_setoran(sid, koreksi, pembalas, nilai_setoran):
    CONN.execute("UPDATE setoran SET koreksi=?, pembalas=?, nilai_setoran=? WHERE id=?", (koreksi, pembalas, nilai_setoran, sid))
    CONN.commit()
def hapus_setoran(sid):
    CONN.execute("DELETE FROM setoran WHERE id=?", (sid,))
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
    "KENDAR SULTONI": "Mahasiswa",
}
NAMA_LENGKAP_TIM = {
    "MUHAMAD RAIS": "Bapak Muhamad Rais, S.Pd.I",
    "MUHAMAD SIDDIQ ASYHARI": "Dr. Muhamad Siddiq Asyhari, M.Pd",
    "SYAMSUL HADI": "Bapak Syamsul Hadi, S.Pd.I",
    "KENDAR SULTONI": "Kendar Sultoni",
}
JUZ30_SURAH = [
    "Surah An-Naba (78)", "Surah An-Nazi'at (79)", "Surah 'Abasa (80)",
    "Surah At-Takwir (81)", "Surah Al-Infitar (82)", "Surah Al-Mutaffifin (83)",
    "Surah Al-Insyiqaq (84)", "Surah Al-Buruj (85)", "Surah At-Tariq (86)",
    "Surah Al-A'la (87)", "Surah Al-Ghasyiyah (88)", "Surah Al-Fajr (89)",
    "Surah Al-Balad (90)", "Surah Asy-Syams (91)", "Surah Al-Lail (92)",
    "Surah Ad-Dhuha (93)", "Surah Asy-Syarh (94)", "Surah At-Tin (95)",
    "Surah Al-'Alaq (96)", "Surah Al-Qadr (97)", "Surah Al-Bayyinah (98)",
    "Surah Az-Zalzalah (99)", "Surah Al-'Adiyat (100)", "Surah Al-Qari'ah (101)",
    "Surah At-Takasur (102)", "Surah Al-'Asr (103)", "Surah Al-Humazah (104)",
    "Surah Al-Fil (105)", "Surah Quraisy (106)", "Surah Al-Ma'un (107)",
    "Surah Al-Kautsar (108)", "Surah Al-Kafirun (109)", "Surah An-Nasr (110)",
    "Surah Al-Lahab (111)", "Surah Al-Ikhlas (112)", "Surah Al-Falaq (113)",
    "Surah An-Nas (114)",
]
# ===== ISI BACAAN JUZ 30 - ARAB + LATIN + ARTI (UNTUK TAHSIN & TAHFIDZ) =====
JUZ30_BACA = {
    "Surah An-Naba (78)": {"ayat": "40 ayat", "arab": "عَمَّ يَتَسَاءَلُونَ (1) عَنِ النَّبَإِ الْعَظِيمِ (2) الَّذِي هُمْ فِيهِ مُخْتَلِفُونَ (3) كَلَّا سَيَعْلَمُونَ (4) ثُمَّ كَلَّا سَيَعْلَمُونَ (5) ... lanjutkan sampai ayat 40 di mushaf ya!", "latin": "Amma yatasaa-aluun. 'Anin naba-il 'azhiim. Alladzii hum fiihi mukhtalifuun. Kallaa saya'lamuun. Tsumma kallaa saya'lamuun...", "arti": "Tentang apakah mereka saling bertanya-tanya? Tentang berita yang besar, yang mereka perselisihkan. Sekali-kali tidak, kelak mereka akan mengetahui."},
    "Surah An-Nazi'at (79)": {"ayat": "46 ayat", "arab": "وَالنَّازِعَاتِ غَرْقًا (1) وَالنَّاشِطَاتِ نَشْطًا (2) وَالسَّابِحَاتِ سَبْحًا (3) فَالسَّابِقَاتِ سَبْقًا (4) فَالْمُدَبِّرَاتِ أَمْرًا (5) ... lanjutkan di mushaf!", "latin": "Wan naazi'aati gharqaa. Wan naasyithaati nasythaa. Was saabihhaati sabhaa. Fas saabiquaati sabqaa. Fal mudabbiraati amraa...", "arti": "Demi (malaikat) yang mencabut nyawa dengan keras, yang mencabut dengan lemah lembut, yang turun dari langit dengan cepat..."},
    "Surah 'Abasa (80)": {"ayat": "42 ayat", "arab": "عَبَسَ وَتَوَلَّىٰ (1) أَنْ جَاءَهُ الْأَعْمَىٰ (2) وَمَا يُدْرِيكَ لَعَلَّهُ يَزَّكَّىٰ (3) أَوْ يَذَّكَّرُ فَتَنْفَعَهُ الذِّكْرَىٰ (4) ... lanjutkan di mushaf!", "latin": "'Abasa wa tawallaa. An jaa-ahul a'maa. Wa maa yudriika la'allahu yazzakkaa. Au yadzdzakkaru fatanfa'ahudz dzikraa...", "arti": "Dia bermuka masam dan berpaling, karena telah datang seorang buta kepadanya. Tahukah kamu, barangkali ia ingin membersihkan dirinya."},
    "Surah At-Takwir (81)": {"ayat": "29 ayat", "arab": "إِذَا الشَّمْسُ كُوِّرَتْ (1) وَإِذَا النُّجُومُ انْكَدَرَتْ (2) وَإِذَا الْجِبَالُ سُيِّرَتْ (3) وَإِذَا الْعِشَارُ عُطِّلَتْ (4) ... lanjutkan di mushaf!", "latin": "Idzasy syamsu kuwwirat. Wa idzan nujuumu-nkadarat. Wa idzal jibaalu suyyirat. Wa idzal 'isyaaru 'uththilat...", "arti": "Apabila matahari digulung, dan apabila bintang-bintang berjatuhan, dan apabila gunung-gunung dihancurkan..."},
    "Surah Al-Infitar (82)": {"ayat": "19 ayat", "arab": "إِذَا السَّمَاءُ انْفَطَرَتْ (1) وَإِذَا الْكَوَاكِبُ انْتَثَرَتْ (2) وَإِذَا الْبِحَارُ فُجِّرَتْ (3) وَإِذَا الْقُبُورُ بُعْثِرَتْ (4) ... lanjutkan di mushaf!", "latin": "Idzas samaa-u-nfatharat. Wa idzal kawaakibu-ntatsarat. Wa idzal bihaaru fujjirat. Wa idzal qubuuru bu'tsirat...", "arti": "Apabila langit terbelah, dan apabila bintang-bintang jatuh berserakan, dan apabila lautan dijadikan meluap..."},
    "Surah Al-Mutaffifin (83)": {"ayat": "36 ayat", "arab": "وَيْلٌ لِلْمُطَفِّفِينَ (1) الَّذِينَ إِذَا اكْتَالُوا عَلَى النَّاسِ يَسْتَوْفُونَ (2) وَإِذَا كَالُوهُمْ أَوْ وَزَنُوهُمْ يُخْسِرُونَ (3) ... lanjutkan di mushaf!", "latin": "Wailul lil muthaffifiin. Alladziina idzaktaaluu 'alan naasi yastaufuun. Wa idzaa kaaluuhum au wazanuuhum yukhsiruun...", "arti": "Celakalah orang-orang yang curang, yang apabila menerima takaran dari orang lain mereka minta dipenuhi, dan apabila mereka menakar untuk orang lain, mereka mengurangi."},
    "Surah Al-Insyiqaq (84)": {"ayat": "25 ayat", "arab": "إِذَا السَّمَاءُ انْشَقَّتْ (1) وَأَذِنَتْ لِرَبِّهَا وَحُقَّتْ (2) وَإِذَا الْأَرْضُ مُدَّتْ (3) وَأَلْقَتْ مَا فِيهَا وَتَخَلَّتْ (4) ... lanjutkan di mushaf!", "latin": "Idzas samaa-u-nsyaqqat. Wa adzinat lirabbihaa wa huqqat. Wa idzal ardhu muddat. Wa alqat maa fiihaa wa takhallat...", "arti": "Apabila langit terbelah, dan patuh kepada Tuhannya, dan sudah semestinya langit itu patuh, dan apabila bumi diratakan..."},
    "Surah Al-Buruj (85)": {"ayat": "22 ayat", "arab": "وَالسَّمَاءِ ذَاتِ الْبُرُوجِ (1) وَالْيَوْمِ الْمَوْعُودِ (2) وَشَاهِدٍ وَمَشْهُودٍ (3) قُتِلَ أَصْحَابُ الْأُخْدُودِ (4) ... lanjutkan di mushaf!", "latin": "Was samaa-i dzaatil buruuj. Wal yaumil mau'uud. Wa syaahidin wa masyhuud. Qutila ash-haabul ukhduud...", "arti": "Demi langit yang mempunyai gugusan bintang, dan hari yang dijanjikan, dan yang menyaksikan dan yang disaksikan. Binasa dan terlaknatlah orang-orang yang membuat parit."},
    "Surah At-Tariq (86)": {"ayat": "17 ayat", "arab": "وَالسَّمَاءِ وَالطَّارِقِ (1) وَمَا أَدْرَاكَ مَا الطَّارِقُ (2) النَّجْمُ الثَّاقِبُ (3) إِنْ كُلُّ نَفْسٍ لَمَّا عَلَيْهَا حَافِظٌ (4) ... lanjutkan di mushaf!", "latin": "Was samaa-i wath thaariq. Wa maa adraaka math thaariq. An najmu-ts tsaaqib. In kullu nafsil lammaa 'alaihaa haafizh...", "arti": "Demi langit dan yang datang pada malam hari. Tahukah kamu apakah yang datang pada malam hari itu? Yaitu bintang yang cahayanya menembus. Tidak ada satu jiwa pun melainkan ada penjaganya."},
    "Surah Al-A'la (87)": {"ayat": "19 ayat", "arab": "سَبِّحِ اسْمَ رَبِّكَ الْأَعْلَى (1) الَّذِي خَلَقَ فَسَوَّىٰ (2) وَالَّذِي قَدَّرَ فَهَدَىٰ (3) وَالَّذِي أَخْرَجَ الْمَرْعَىٰ (4) فَجَعَلَهُ غُثَاءً أَحْوَىٰ (5) سَنُقْرِئُكَ فَلَا تَنْسَىٰ (6) إِلَّا مَا شَاءَ اللَّهُ ۚ إِنَّهُ يَعْلَمُ الْجَهْرَ وَمَا يَخْفَىٰ (7) وَنُيَسِّرُكَ لِلْيُسْرَىٰ (8) فَذَكِّرْ إِنْ نَفَعَتِ الذِّكْرَىٰ (9) سَيَذَّكَّرُ مَنْ يَخْشَىٰ (10) وَيَتَجَنَّبُهَا الْأَشْقَى (11) الَّذِي يَصْلَى النَّارَ الْكُبْرَىٰ (12) ثُمَّ لَا يَمُوتُ فِيهَا وَلَا يَحْيَىٰ (13) قَدْ أَفْلَحَ مَنْ تَزَكَّىٰ (14) وَذَكَرَ اسْمَ رَبِّهِ فَصَلَّىٰ (15) بَلْ تُؤْثِرُونَ الْحَيَاةَ الدُّنْيَا (16) وَالْآخِرَةُ خَيْرٌ وَأَبْقَىٰ (17) إِنَّ هَٰذَا لَفِي الصُّحُفِ الْأُولَىٰ (18) صُحُفِ إِبْرَاهِيمَ وَمُوسَىٰ (19)", "latin": "Sabbihisma rabbikal a'laa. Alladzii khalaqa fasawwaa. Walladzii qaddara fahadaa. Walladzii akhrajal mar'aa. Faja'alahu ghutsaa-an ahwaa. Sanuqri-uka falaa tansaa. Illaa maa syaa-allaah. Innahu ya'lamul jahra wa maa yakhfaa. Wa nuyassiruka lilyusraa. Fadzakkir in nafa'atidz dzikraa. Sayadzdzakkaru man yakhsyaa. Wa yatajannabuhal asyqaa. Alladzii yashlan naaral kubraa. Tsumma laa yamuutu fiihaa wa laa yahyaa. Qad aflaha man tazakkaa. Wa dzakara-sma rabbihi fashallaa. Bal tu'tsiruunal hayaatad dunyaa. Wal aakhiratu khairun wa abqaa. Inna haadzaa lafis shuhufil uulaa. Shuhufi ibraahiima wa muusaa.", "arti": "Sucikanlah nama Tuhanmu Yang Maha Tinggi. Yang menciptakan, lalu menyempurnakan. Yang menentukan kadar, lalu memberi petunjuk."},
    "Surah Al-Ghasyiyah (88)": {"ayat": "26 ayat", "arab": "هَلْ أَتَاكَ حَدِيثُ الْغَاشِيَةِ (1) وُجُوهٌ يَوْمَئِذٍ خَاشِعَةٌ (2) عَامِلَةٌ نَاصِبَةٌ (3) تَصْلَىٰ نَارًا حَامِيَةً (4) تُسْقَىٰ مِنْ عَيْنٍ آنِيَةٍ (5) ... lanjutkan di mushaf!", "latin": "Hal ataaka hadiitsul ghaasyiyah. Wujuuhun yauma-idzin khaasyi'ah. 'Aamilatun naashibah. Tashlaa naaran haamiyah. Tusqaa min 'ainin aaniyah...", "arti": "Sudah datangkah kepadamu berita tentang hari pembalasan? Banyak muka pada hari itu tunduk terhina, bekerja keras lagi kepayahan, memasuki api yang sangat panas."},
    "Surah Al-Fajr (89)": {"ayat": "30 ayat", "arab": "وَالْفَجْرِ (1) وَلَيَالٍ عَشْرٍ (2) وَالشَّفْعِ وَالْوَتْرِ (3) وَاللَّيْلِ إِذَا يَسْرِ (4) هَلْ فِي ذَٰلِكَ قَسَمٌ لِذِي حِجْرٍ (5) ... lanjutkan di mushaf!", "latin": "Wal fajr. Wa layaalin 'asyr. Wasy syaf'i wal watr. Wal laili idzaa yasr. Hal fii dzaalika qasamul lidzii hijr...", "arti": "Demi fajar, dan malam yang sepuluh, dan yang genap dan yang ganjil, dan malam bila berlalu. Pada yang demikian itu terdapat sumpah bagi orang yang berakal."},
    "Surah Al-Balad (90)": {"ayat": "20 ayat", "arab": "لَا أُقْسِمُ بِهَٰذَا الْبَلَدِ (1) وَأَنْتَ حِلٌّ بِهَٰذَا الْبَلَدِ (2) وَوَالِدٍ وَمَا وَلَدَ (3) لَقَدْ خَلَقْنَا الْإِنْسَانَ فِي كَبَدٍ (4) ... lanjutkan di mushaf!", "latin": "Laa uqsimu bihaadzal balad. Wa anta hillum bihaadzal balad. Wa waalidin wa maa walad. Laqad khalaqnal insaana fii kabad...", "arti": "Aku benar-benar bersumpah dengan kota ini (Mekah), dan kamu bertempat di kota ini, dan demi bapak dan anaknya. Sesungguhnya Kami telah menciptakan manusia berada dalam susah payah."},
    "Surah Asy-Syams (91)": {"ayat": "15 ayat", "arab": "وَالشَّمْسِ وَضُحَاهَا (1) وَالْقَمَرِ إِذَا تَلَاهَا (2) وَالنَّهَارِ إِذَا جَلَّاهَا (3) وَاللَّيْلِ إِذَا يَغْشَاهَا (4) وَالسَّمَاءِ وَمَا بَنَاهَا (5) وَالْأَرْضِ وَمَا طَحَاهَا (6) وَنَفْسٍ وَمَا سَوَّاهَا (7) فَأَلْهَمَهَا فُجُورَهَا وَتَقْوَاهَا (8) قَدْ أَفْلَحَ مَنْ زَكَّاهَا (9) وَقَدْ خَابَ مَنْ دَسَّاهَا (10) كَذَّبَتْ ثَمُودُ بِطَغْوَاهَا (11) إِذِ انْبَعَثَ أَشْقَاهَا (12) فَقَالَ لَهُمْ رَسُولُ اللَّهِ نَاقَةَ اللَّهِ وَسُقْيَاهَا (13) فَكَذَّبُوهُ فَعَقَرُوهَا فَدَمْدَمَ عَلَيْهِمْ رَبُّهُمْ بِذَنْبِهِمْ فَسَوَّاهَا (14) وَلَا يَخَافُ عُقْبَاهَا (15)", "latin": "Wasy syamsi wa dhuhaahaa. Wal qamari idzaa talaahaa. Wan nahaari idzaa jallaahaa. Wal laili idzaa yaghsyaahaa. Was samaa-i wa maa banaahaa. Wal ardhi wa maa thahaahaa. Wa nafsiw wa maa sawwaahaa. Fa-alhamahaa fujuurahaa wa taqwaahaa. Qad aflaha man zakkaahaa. Wa qad khaaba man dassaahaa. Kadzdzabat tsamuudu bithaghwaahaa. Idzi-nba'atsa asyqaahaa. Faqaala lahum rasuulullaahi naaqatallaahi wa suqyaahaa. Fakadzdzabuuhu fa'aqaruuhaa fadamdama 'alaihim rabbuhum bidzanbihim fasawwaahaa. Wa laa yakhaafu 'uqbaahaa.", "arti": "Demi matahari dan cahayanya di pagi hari, dan bulan apabila mengiringinya, dan siang apabila menampakkannya..."},
    "Surah Al-Lail (92)": {"ayat": "21 ayat", "arab": "وَاللَّيْلِ إِذَا يَغْشَىٰ (1) وَالنَّهَارِ إِذَا تَجَلَّىٰ (2) وَمَا خَلَقَ الذَّكَرَ وَالْأُنْثَىٰ (3) إِنَّ سَعْيَكُمْ لَشَتَّىٰ (4) ... lanjutkan di mushaf!", "latin": "Wal laili idzaa yaghsyaa. Wan nahaari idzaa tajallaa. Wa maa khalaqadz dzakara wal untsaa. Inna sa'yakum lasyattaa...", "arti": "Demi malam apabila menutupi, dan siang apabila terang benderang, dan penciptaan laki-laki dan perempuan. Sesungguhnya usaha kamu memang berbeda-beda."},
    "Surah Ad-Dhuha (93)": {"ayat": "11 ayat", "arab": "وَالضُّحَىٰ (1) وَاللَّيْلِ إِذَا سَجَىٰ (2) مَا وَدَّعَكَ رَبُّكَ وَمَا قَلَىٰ (3) وَلَلْآخِرَةُ خَيْرٌ لَكَ مِنَ الْأُولَىٰ (4) وَلَسَوْفَ يُعْطِيكَ رَبُّكَ فَتَرْضَىٰ (5) أَلَمْ يَجِدْكَ يَتِيمًا فَآوَىٰ (6) وَوَجَدَكَ ضَالًّا فَهَدَىٰ (7) وَوَجَدَكَ عَائِلًا فَأَغْنَىٰ (8) فَأَمَّا الْيَتِيمَ فَلَا تَقْهَرْ (9) وَأَمَّا السَّائِلَ فَلَا تَنْهَرْ (10) وَأَمَّا بِنِعْمَةِ رَبِّكَ فَحَدِّثْ (11)", "latin": "Wadh dhuhaa. Wal laili idzaa sajaa. Maa wadda'aka rabbuka wa maa qalaa. Walal aakhiratu khairul laka minal uulaa. Wa lasaufa yu'thiika rabbuka fatardhaa. Alam yajidka yatiiman fa-aawaa. Wa wajadaka dhaallan fahadaa. Wa wajadaka 'aa-ilan fa-aghnaa. Fa-ammal yatiima falaa taqhar. Wa ammas saa-ila falaa tanhar. Wa ammaa bini'mati rabbika fahaddits.", "arti": "Demi waktu matahari sepenggalahan naik, dan demi malam apabila telah sunyi. Tuhanmu tiada meninggalkan kamu dan tiada (pula) benci kepadamu."},
    "Surah Asy-Syarh (94)": {"ayat": "8 ayat", "arab": "أَلَمْ نَشْرَحْ لَكَ صَدْرَكَ (1) وَوَضَعْنَا عَنْكَ وِزْرَكَ (2) الَّذِي أَنْقَضَ ظَهْرَكَ (3) وَرَفَعْنَا لَكَ ذِكْرَكَ (4) فَإِنَّ مَعَ الْعُسْرِ يُسْرًا (5) إِنَّ مَعَ الْعُسْرِ يُسْرًا (6) فَإِذَا فَرَغْتَ فَانْصَبْ (7) وَإِلَىٰ رَبِّكَ فَارْغَبْ (8)", "latin": "Alam nasyrah laka shadrak. Wa wadha'naa 'anka wizrak. Alladzii anqadha zhahrak. Wa rafa'naa laka dzikrak. Fa-inna ma'al 'usri yusraa. Inna ma'al 'usri yusraa. Fa-idzaa faraghta fanshab. Wa ilaa rabbika farghab.", "arti": "Bukankah Kami telah melapangkan untukmu dadamu? Dan Kami telah menghilangkan daripadamu bebanmu. Sesungguhnya sesudah kesulitan itu ada kemudahan."},
    "Surah At-Tin (95)": {"ayat": "8 ayat", "arab": "وَالتِّينِ وَالزَّيْتُونِ (1) وَطُورِ سِينِينَ (2) وَهَٰذَا الْبَلَدِ الْأَمِينِ (3) لَقَدْ خَلَقْنَا الْإِنْسَانَ فِي أَحْسَنِ تَقْوِيمٍ (4) ثُمَّ رَدَدْنَاهُ أَسْفَلَ سَافِلِينَ (5) إِلَّا الَّذِينَ آمَنُوا وَعَمِلُوا الصَّالِحَاتِ فَلَهُمْ أَجْرٌ غَيْرُ مَمْنُونٍ (6) فَمَا يُكَذِّبُكَ بَعْدُ بِالدِّينِ (7) أَلَيْسَ اللَّهُ بِأَحْكَمِ الْحَاكِمِينَ (8)", "latin": "Wattiini waz zaituun. Wa thuuri siiniin. Wa haadzal baladil amiin. Laqad khalaqnal insaana fii ahsani taqwiim. Tsumma radadnaahu asfala saafiliin. Illal ladziina aamanuu wa 'amilush shaalihaati falahum ajrun ghairu mamnuun. Famaa yukadzdzibuka ba'du biddiin. Alaisallaahu bi-ahkamil haakimiin.", "arti": "Demi buah tin dan buah zaitun, dan demi bukit Sinai, dan demi kota ini yang aman. Sesungguhnya Kami telah menciptakan manusia dalam bentuk yang sebaik-baiknya."},
    "Surah Al-'Alaq (96)": {"ayat": "19 ayat", "arab": "اقْرَأْ بِاسْمِ رَبِّكَ الَّذِي خَلَقَ (1) خَلَقَ الْإِنْسَانَ مِنْ عَلَقٍ (2) اقْرَأْ وَرَبُّكَ الْأَكْرَمُ (3) الَّذِي عَلَّمَ بِالْقَلَمِ (4) عَلَّمَ الْإِنْسَانَ مَا لَمْ يَعْلَمْ (5) ... lanjutkan ayat 6-19 di mushaf!", "latin": "Iqra' bismi rabbikal ladzii khalaq. Khalaqal insaana min 'alaq. Iqra' wa rabbukal akram. Alladzii 'allama bil qalam. 'Allamal insaana maa lam ya'lam...", "arti": "Bacalah dengan menyebut nama Tuhanmu Yang menciptakan. Dia telah menciptakan manusia dari segumpal darah. Bacalah, dan Tuhanmulah Yang Maha Pemurah."},
    "Surah Al-Qadr (97)": {"ayat": "5 ayat", "arab": "إِنَّا أَنْزَلْنَاهُ فِي لَيْلَةِ الْقَدْرِ (1) وَمَا أَدْرَاكَ مَا لَيْلَةُ الْقَدْرِ (2) لَيْلَةُ الْقَدْرِ خَيْرٌ مِنْ أَلْفِ شَهْرٍ (3) تَنَزَّلُ الْمَلَائِكَةُ وَالرُّوحُ فِيهَا بِإِذْنِ رَبِّهِمْ مِنْ كُلِّ أَمْرٍ (4) سَلَامٌ هِيَ حَتَّىٰ مَطْلَعِ الْفَجْرِ (5)", "latin": "Innaa anzalnaahu fii lailatil qadr. Wa maa adraaka maa lailatul qadr. Lailatul qadri khairum min alfi syahr. Tanazzalul malaa-ikatu war ruuhu fiihaa bi-idzni rabbihim min kulli amr. Salaamun hiya hattaa mathla'il fajr.", "arti": "Sesungguhnya Kami telah menurunkannya (Al-Qur'an) pada malam kemuliaan. Dan tahukah kamu apakah malam kemuliaan itu? Malam kemuliaan itu lebih baik dari seribu bulan."},
    "Surah Al-Bayyinah (98)": {"ayat": "8 ayat", "arab": "لَمْ يَكُنِ الَّذِينَ كَفَرُوا مِنْ أَهْلِ الْكِتَابِ وَالْمُشْرِكِينَ مُنْفَكِّينَ حَتَّىٰ تَأْتِيَهُمُ الْبَيِّنَةُ (1) رَسُولٌ مِنَ اللَّهِ يَتْلُو صُحُفًا مُطَهَّرَةً (2) فِيهَا كُتُبٌ قَيِّمَةٌ (3) وَمَا تَفَرَّقَ الَّذِينَ أُوتُوا الْكِتَابَ إِلَّا مِنْ بَعْدِ مَا جَاءَتْهُمُ الْبَيِّنَةُ (4) وَمَا أُمِرُوا إِلَّا لِيَعْبُدُوا اللَّهَ مُخْلِصِينَ لَهُ الدِّينَ حُنَفَاءَ وَيُقِيمُوا الصَّلَاةَ وَيُؤْتُوا الزَّكَاةَ ۚ وَذَٰلِكَ دِينُ الْقَيِّمَةِ (5) إِنَّ الَّذِينَ كَفَرُوا مِنْ أَهْلِ الْكِتَابِ وَالْمُشْرِكِينَ فِي نَارِ جَهَنَّمَ خَالِدِينَ فِيهَا ۚ أُولَٰئِكَ هُمْ شَرُّ الْبَرِيَّةِ (6) إِنَّ الَّذِينَ آمَنُوا وَعَمِلُوا الصَّالِحَاتِ أُولَٰئِكَ هُمْ خَيْرُ الْبَرِيَّةِ (7) جَزَاؤُهُمْ عِنْدَ رَبِّهِمْ جَنَّاتُ عَدْنٍ تَجْرِي مِنْ تَحْتِهَا الْأَنْهَارُ خَالِدِينَ فِيهَا أَبَدًا ۖ رَضِيَ اللَّهُ عَنْهُمْ وَرَضُوا عَنْهُ ۚ ذَٰلِكَ لِمَنْ خَشِيَ رَبَّهُ (8)", "latin": "Lam yakunil ladziina kafaruu min ahlil kitaabi wal musyrikiina munfakkiina hattaa ta'tiyahumul bayyinah. Rasuulum minallaahi yatluu shuhufam muthahharah. Fiihaa kutubun qayyimah. Wa maa tafarraqal ladziina uutul kitaaba illaa mim ba'di maa jaa-at-humul bayyinah. Wa maa umiruu illaa liya'budullaaha mukhlishiina lahud diina hunafaa-a wa yuqiimush shalaata wa yu-tuz zakaah. Wa dzaalika diinul qayyimah. Innal ladziina kafaruu min ahlil kitaabi wal musyrikiina fii naari jahannama khaalidiina fiihaa. Ulaa-ika hum syarrul bariyyah. Innal ladziina aamanuu wa 'amilush shaalihaati ulaa-ika hum khairul bariyyah. Jazaa-uhum 'inda rabbihim jannaatu 'adnin tajrii min tahtihal anhaaru khaalidiina fiihaa abadaa. Radhiyallaahu 'anhum wa radhuu 'anh. Dzaalika liman khasyiya rabbah.", "arti": "Orang-orang kafir dari Ahli Kitab dan orang-orang musyrik tidak akan meninggalkan agama mereka sampai datang kepada mereka bukti yang nyata."},
    "Surah Az-Zalzalah (99)": {"ayat": "8 ayat", "arab": "إِذَا زُلْزِلَتِ الْأَرْضُ زِلْزَالَهَا (1) وَأَخْرَجَتِ الْأَرْضُ أَثْقَالَهَا (2) وَقَالَ الْإِنْسَانُ مَا لَهَا (3) يَوْمَئِذٍ تُحَدِّثُ أَخْبَارَهَا (4) بِأَنَّ رَبَّكَ أَوْحَىٰ لَهَا (5) يَوْمَئِذٍ يَصْدُرُ النَّاسُ أَشْتَاتًا لِيُرَوْا أَعْمَالَهُمْ (6) فَمَنْ يَعْمَلْ مِثْقَالَ ذَرَّةٍ خَيْرًا يَرَهُ (7) وَمَنْ يَعْمَلْ مِثْقَالَ ذَرَّةٍ شَرًّا يَرَهُ (8)", "latin": "Idzaa zulzilatil ardhu zilzaalahaa. Wa akhrajatil ardhu atsqoolahaa. Wa qaalal insaanu maa lahaa. Yauma-idzin tuhadditsu akhbaarahaa. Bi-anna rabbaka auhaa lahaa. Yauma-idzin yashdurun naasu asytaatal liyurau a'maalahum. Faman ya'mal mitsqaala dzarratin khairay yarah. Wa man ya'mal mitsqaala dzarratin syarray yarah.", "arti": "Apabila bumi digoncangkan dengan goncangan yang dahsyat, dan bumi telah mengeluarkan beban-beban beratnya, dan manusia bertanya: Mengapa bumi jadi begini?"},
    "Surah Al-'Adiyat (100)": {"ayat": "11 ayat", "arab": "وَالْعَادِيَاتِ ضَبْحًا (1) فَالْمُورِيَاتِ قَدْحًا (2) فَالْمُغِيرَاتِ صُبْحًا (3) فَأَثَرْنَ بِهِ نَقْعًا (4) فَوَسَطْنَ بِهِ جَمْعًا (5) إِنَّ الْإِنْسَانَ لِرَبِّهِ لَكَنُودٌ (6) وَإِنَّهُ عَلَىٰ ذَٰلِكَ لَشَهِيدٌ (7) وَإِنَّهُ لِحُبِّ الْخَيْرِ لَشَدِيدٌ (8) أَفَلَا يَعْلَمُ إِذَا بُعْثِرَ مَا فِي الْقُبُورِ (9) وَحُصِّلَ مَا فِي الصُّدُورِ (10) إِنَّ رَبَّهُمْ بِهِمْ يَوْمَئِذٍ لَخَبِيرٌ (11)", "latin": "Wal 'aadiyaati dhabhaa. Fal muuriyaati qadhaa. Fal mughiiraati shubhaa. Fa-atsarna bihii naq'aa. Fa-wasathna bihii jam'aa. Innal insaana lirabbihii lakanuud. Wa innahuu 'alaa dzaalika lasyahiid. Wa innahuu lihubbil khairi lasyadiid. Afalaa ya'lamu idzaa bu'tsira maa fil qubuur. Wa hushshila maa fish shuduur. Inna rabbahum bihim yauma-idzil lakhbiir.", "arti": "Demi kuda perang yang berlari kencang dengan terengah-engah, dan kuda yang mencetuskan api dengan pukulan kuku kakinya..."},
    "Surah Al-Qari'ah (101)": {"ayat": "11 ayat", "arab": "الْقَارِعَةُ (1) مَا الْقَارِعَةُ (2) وَمَا أَدْرَاكَ مَا الْقَارِعَةُ (3) يَوْمَ يَكُونُ النَّاسُ كَالْفَرَاشِ الْمَبْثُوثِ (4) وَتَكُونُ الْجِبَالُ كَالْعِهْنِ الْمَنْفُوشِ (5) فَأَمَّا مَنْ ثَقُلَتْ مَوَازِينُهُ (6) فَهُوَ فِي عِيشَةٍ رَاضِيَةٍ (7) وَأَمَّا مَنْ خَفَّتْ مَوَازِينُهُ (8) فَأُمُّهُ هَاوِيَةٌ (9) وَمَا أَدْرَاكَ مَا هِيَهْ (10) نَارٌ حَامِيَةٌ (11)", "latin": "Al qaari'ah. Mal qaari'ah. Wa maa adraaka mal qaari'ah. Yauma yakuunun naasu kal faraasyil mabtsuuts. Wa takuunul jibaalu kal 'ihnil manfuusy. Fa-ammaa man tsaqulat mawaaziinuh. Fahuwa fii 'iisyatir raadhiyah. Wa ammaa man khaffat mawaaziinuh. Fa-ummuhuu haawiyah. Wa maa adraaka maa hiyah. Naarun haamiyah.", "arti": "Hari Kiamat. Apakah hari Kiamat itu? Dan tahukah kamu apakah hari Kiamat itu? Pada hari itu manusia seperti anai-anai yang bertebaran."},
    "Surah At-Takasur (102)": {"ayat": "8 ayat", "arab": "أَلْهَاكُمُ التَّكَاثُرُ (1) حَتَّىٰ زُرْتُمُ الْمَقَابِرَ (2) كَلَّا سَوْفَ تَعْلَمُونَ (3) ثُمَّ كَلَّا سَوْفَ تَعْلَمُونَ (4) كَلَّا لَوْ تَعْلَمُونَ عِلْمَ الْيَقِينِ (5) لَتَرَوُنَّ الْجَحِيمَ (6) ثُمَّ لَتَرَوُنَّهَا عَيْنَ الْيَقِينِ (7) ثُمَّ لَتُسْأَلُنَّ يَوْمَئِذٍ عَنِ النَّعِيمِ (8)", "latin": "Alhaakumut takaa-tsur. Hattaa zurtumul maqaabir. Kallaa saufa ta'lamuun. Tsumma kallaa saufa ta'lamuun. Kallaa lau ta'lamuuna 'ilmal yaqiin. Latarawunnal jahiim. Tsumma latarawunnahaa 'ainal yaqiin. Tsumma latus-alunna yauma-idzin 'anin na'iim.", "arti": "Bermegah-megahan telah melalaikan kamu, sampai kamu masuk ke dalam kubur. Janganlah begitu, kelak kamu akan mengetahui."},
    "Surah Al-'Asr (103)": {"ayat": "3 ayat", "arab": "وَالْعَصْرِ (1) إِنَّ الْإِنْسَانَ لَفِي خُسْرٍ (2) إِلَّا الَّذِينَ آمَنُوا وَعَمِلُوا الصَّالِحَاتِ وَتَوَاصَوْا بِالْحَقِّ وَتَوَاصَوْا بِالصَّبْرِ (3)", "latin": "Wal 'ashr. Innal insaana lafii khusr. Illal ladziina aamanuu wa 'amilush shaalihaati wa tawaashau bil haqqi wa tawaashau bish shabr.", "arti": "Demi masa. Sesungguhnya manusia itu benar-benar dalam kerugian, kecuali orang-orang yang beriman dan mengerjakan amal saleh dan saling menasihati supaya menaati kebenaran dan saling menasihati supaya menetapi kesabaran."},
    "Surah Al-Humazah (104)": {"ayat": "9 ayat", "arab": "وَيْلٌ لِكُلِّ هُمَزَةٍ لُمَزَةٍ (1) الَّذِي جَمَعَ مَالًا وَعَدَّدَهُ (2) يَحْسَبُ أَنَّ مَالَهُ أَخْلَدَهُ (3) كَلَّا ۖ لَيُنْبَذَنَّ فِي الْحُطَمَةِ (4) وَمَا أَدْرَاكَ مَا الْحُطَمَةُ (5) نَارُ اللَّهِ الْمُوقَدَةُ (6) الَّتِي تَطَّلِعُ عَلَى الْأَفْئِدَةِ (7) إِنَّهَا عَلَيْهِمْ مُؤْصَدَةٌ (8) فِي عَمَدٍ مُمَدَّدَةٍ (9)", "latin": "Wailul likulli humazatil lumazah. Alladzii jama'a maalan wa 'addadah. Yahsabu anna maalahuu akhladah. Kallaa layunbadzanna fil huthamah. Wa maa adraaka mal huthamah. Naarullaahil muuqadah. Allatii taththali'u 'alal af-idah. Innahaa 'alaihim mu'shadah. Fii 'amadim mumaddadah.", "arti": "Kecelakaanlah bagi setiap pengumpat lagi pencela, yang mengumpulkan harta dan menghitung-hitung. Dia mengira bahwa hartanya itu dapat mengekalkannya."},
    "Surah Al-Fil (105)": {"ayat": "5 ayat", "arab": "أَلَمْ تَرَ كَيْفَ فَعَلَ رَبُّكَ بِأَصْحَابِ الْفِيلِ (1) أَلَمْ يَجْعَلْ كَيْدَهُمْ فِي تَضْلِيلٍ (2) وَأَرْسَلَ عَلَيْهِمْ طَيْرًا أَبَابِيلَ (3) تَرْمِيهِمْ بِحِجَارَةٍ مِنْ سِجِّيلٍ (4) فَجَعَلَهُمْ كَعَصْفٍ مَأْكُولٍ (5)", "latin": "Alam tara kaifa fa'ala rabbuka bi-ash-haabil fiil. Alam yaj'al kaidahum fii tadhliil. Wa arsala 'alaihim thairan abaabiil. Tarmiihim bihijaaratim min sijjiil. Faja'alahum ka'ashfim ma'kuul.", "arti": "Apakah kamu tidak memperhatikan bagaimana Tuhanmu telah bertindak terhadap tentara bergajah? Bukankah Dia telah menjadikan tipu daya mereka itu sia-sia?"},
    "Surah Quraisy (106)": {"ayat": "4 ayat", "arab": "لِإِيلَافِ قُرَيْشٍ (1) إِيلَافِهِمْ رِحْلَةَ الشِّتَاءِ وَالصَّيْفِ (2) فَلْيَعْبُدُوا رَبَّ هَٰذَا الْبَيْتِ (3) الَّذِي أَطْعَمَهُمْ مِنْ جُوعٍ وَآمَنَهُمْ مِنْ خَوْفٍ (4)", "latin": "Li-iilaafi quraisy. Iilaafihim rihlatasy syitaa-i wash shaif. Falya'buduu rabba haadzal bait. Alladzii ath'amahum min juu'in wa aamanahum min khauf.", "arti": "Karena kebiasaan orang-orang Quraisy, yaitu kebiasaan mereka bepergian pada musim dingin dan musim panas. Maka hendaklah mereka menyembah Tuhan Pemilik rumah ini (Ka'bah)."},
    "Surah Al-Ma'un (107)": {"ayat": "7 ayat", "arab": "أَرَأَيْتَ الَّذِي يُكَذِّبُ بِالدِّينِ (1) فَذَٰلِكَ الَّذِي يَدُعُّ الْيَتِيمَ (2) وَلَا يَحُضُّ عَلَىٰ طَعَامِ الْمِسْكِينِ (3) فَوَيْلٌ لِلْمُصَلِّينَ (4) الَّذِينَ هُمْ عَنْ صَلَاتِهِمْ سَاهُونَ (5) الَّذِينَ هُمْ يُرَاءُونَ (6) وَيَمْنَعُونَ الْمَاعُونَ (7)", "latin": "Ara-aital ladzii yukadzdzibu biddiin. Fadzaalikal ladzii yadu'ul yatiim. Wa laa yahudhdhu 'alaa tha'aamil miskiin. Fawailul lil mushalliin. Alladziina hum 'an shalaatihim saahuun. Alladziina hum yuraa-uun. Wa yamna'uunal maa'uun.", "arti": "Tahukah kamu orang yang mendustakan agama? Itulah orang yang menghardik anak yatim, dan tidak menganjurkan memberi makan orang miskin."},
    "Surah Al-Kautsar (108)": {"ayat": "3 ayat", "arab": "إِنَّا أَعْطَيْنَاكَ الْكَوْثَرَ (1) فَصَلِّ لِرَبِّكَ وَانْحَرْ (2) إِنَّ شَانِئَكَ هُوَ الْأَبْتَرُ (3)", "latin": "Innaa a'thainaakal kautsar. Fashalli lirabbika wanhar. Inna syaani-aka huwal abtar.", "arti": "Sesungguhnya Kami telah memberikan kepadamu nikmat yang banyak. Maka dirikanlah shalat karena Tuhanmu, dan berkorbanlah. Sesungguhnya orang-orang yang membenci kamu dialah yang terputus."},
    "Surah Al-Kafirun (109)": {"ayat": "6 ayat", "arab": "قُلْ يَا أَيُّهَا الْكَافِرُونَ (1) لَا أَعْبُدُ مَا تَعْبُدُونَ (2) وَلَا أَنْتُمْ عَابِدُونَ مَا أَعْبُدُ (3) وَلَا أَنَا عَابِدٌ مَا عَبَدْتُمْ (4) وَلَا أَنْتُمْ عَابِدُونَ مَا أَعْبُدُ (5) لَكُمْ دِينُكُمْ وَلِيَ دِينِ (6)", "latin": "Qul yaa ayyuhal kaafiruun. Laa a'budu maa ta'buduun. Wa laa antum 'aabiduuna maa a'bud. Wa laa ana 'aabidum maa 'abattum. Wa laa antum 'aabiduuna maa a'bud. Lakum diinukum wa liya diin.", "arti": "Katakanlah: Hai orang-orang kafir, aku tidak akan menyembah apa yang kamu sembah. Dan kamu bukan penyembah Tuhan yang aku sembah."},
    "Surah An-Nasr (110)": {"ayat": "3 ayat", "arab": "إِذَا جَاءَ نَصْرُ اللَّهِ وَالْفَتْحُ (1) وَرَأَيْتَ النَّاسَ يَدْخُلُونَ فِي دِينِ اللَّهِ أَفْوَاجًا (2) فَسَبِّحْ بِحَمْدِ رَبِّكَ وَاسْتَغْفِرْهُ ۚ إِنَّهُ كَانَ تَوَّابًا (3)", "latin": "Idzaa jaa-a nashrullaahi wal fath. Wa ra-aitan naasa yadkhuluuna fii diinillaahi afwaajaa. Fasabbih bihamdi rabbika wastaghfirh. Innahuu kaana tawwaabaa.", "arti": "Apabila telah datang pertolongan Allah dan kemenangan, dan kamu lihat manusia masuk agama Allah dengan berbondong-bondong, maka bertasbihlah dengan memuji Tuhanmu dan mohonlah ampun kepada-Nya."},
    "Surah Al-Lahab (111)": {"ayat": "5 ayat", "arab": "تَبَّتْ يَدَا أَبِي لَهَبٍ وَتَبَّ (1) مَا أَغْنَىٰ عَنْهُ مَالُهُ وَمَا كَسَبَ (2) سَيَصْلَىٰ نَارًا ذَاتَ لَهَبٍ (3) وَامْرَأَتُهُ حَمَّالَةَ الْحَطَبِ (4) فِي جِيدِهَا حَبْلٌ مِنْ مَسَدٍ (5)", "latin": "Tabbat yadaa abii lahabin wa tabb. Maa aghnaa 'anhu maaluhuu wa maa kasab. Sayashlaa naaran dzaata lahab. Wamra-atuhuu hammaalatal hathab. Fii jiidihaa hablum mim masad.", "arti": "Binasalah kedua tangan Abu Lahab dan sesungguhnya dia akan binasa. Tidaklah berfaedah baginya harta bendanya dan apa yang ia usahakan."},
    "Surah Al-Ikhlas (112)": {"ayat": "4 ayat", "arab": "قُلْ هُوَ اللَّهُ أَحَدٌ (1) اللَّهُ الصَّمَدُ (2) لَمْ يَلِدْ وَلَمْ يُولَدْ (3) وَلَمْ يَكُنْ لَهُ كُفُوًا أَحَدٌ (4)", "latin": "Qul huwallaahu ahad. Allaahush shamad. Lam yalid wa lam yuulad. Wa lam yakul lahuu kufuwan ahad.", "arti": "Katakanlah: Dialah Allah, Yang Maha Esa. Allah adalah Tuhan yang bergantung kepada-Nya segala sesuatu. Dia tiada beranak dan tidak pula diperanakkan. Dan tidak ada seorang pun yang setara dengan Dia."},
    "Surah Al-Falaq (113)": {"ayat": "5 ayat", "arab": "قُلْ أَعُوذُ بِرَبِّ الْفَلَقِ (1) مِنْ شَرِّ مَا خَلَقَ (2) وَمِنْ شَرِّ غَاسِقٍ إِذَا وَقَبَ (3) وَمِنْ شَرِّ النَّفَّاثَاتِ فِي الْعُقَدِ (4) وَمِنْ شَرِّ حَاسِدٍ إِذَا حَسَدَ (5)", "latin": "Qul a'uudzu birabbil falaq. Min syarri maa khalaq. Wa min syarri ghaasiqin idzaa waqab. Wa min syarrin naffaatsaati fil 'uqad. Wa min syarri haasidin idzaa hasad.", "arti": "Katakanlah: Aku berlindung kepada Tuhan Yang Menguasai subuh, dari kejahatan makhluk-Nya, dan dari kejahatan malam apabila telah gelap gulita."},
    "Surah An-Nas (114)": {"ayat": "6 ayat", "arab": "قُلْ أَعُوذُ بِرَبِّ النَّاسِ (1) مَلِكِ النَّاسِ (2) إِلَٰهِ النَّاسِ (3) مِنْ شَرِّ الْوَسْوَاسِ الْخَنَّاسِ (4) الَّذِي يُوَسْوِسُ فِي صُدُورِ النَّاسِ (5) مِنَ الْجِنَّةِ وَالنَّاسِ (6)", "latin": "Qul a'uudzu birabbin naas. Malikin naas. Ilaahin naas. Min syarril waswaasil khannaas. Alladzii yuwaswisu fii shuduurin naas. Minal jinnati wan naas.", "arti": "Katakanlah: Aku berlindung kepada Tuhan manusia. Raja manusia. Sembahan manusia. Dari kejahatan bisikan syaitan yang biasa bersembunyi."},
}
# ===== ISI IQRO 1-6 =====
IQRO_BACA = {
    "Iqro 1": {"judul": "Iqro 1 - Mengenal Huruf Hijaiyah", "materi": "Huruf Hijaiyah (dari kanan ke kiri):\nا - Alif | ب - Ba | ت - Ta | ث - Tsa | ج - Jim | ح - Ha | خ - Kho | د - Dal | ذ - Dzal | ر - Ro | ز - Za | س - Sin | ش - Syin | ص - Shod | ض - Dhod | ط - Tho | ظ - Zho | ع - 'Ain | غ - Ghoin | ف - Fa | ق - Qof | ك - Kaf | ل - Lam | م - Mim | ن - Nun | و - Wau | ه - Ha | ء - Hamzah | ي - Ya\n\nCara baca: Sebutkan nama hurufnya satu-satu, pelan-pelan.\nContoh: ا ب ت - dibaca Alif, Ba, Ta\nContoh: ج ح خ - dibaca Jim, Ha, Kho\nLatihan: ا - ب - ت - ث - ج - ح - خ"},
    "Iqro 2": {"judul": "Iqro 2 - Harakat Fathah (A)", "materi": "Fathah = garis di atas huruf, dibaca A.\n\nأَ - A | بَ - Ba | تَ - Ta | ثَ - Tsa | جَ - Ja | حَ - Ha | خَ - Kho\n\nContoh kata:\nبَ تَ - Ba Ta\nجَ حَ - Ja Ha\nكَ تَ بَ - Ka Ta Ba\nدَ رَ سَ - Da Ra Sa\n\nLatihan baca: بَ - تَ - ثَ - جَ - حَ - خَ - دَ"},
    "Iqro 3": {"judul": "Iqro 3 - Kasrah (I) & Dhammah (U)", "materi": "Kasrah = garis di bawah huruf, dibaca I.\nDhammah = seperti angka 9 kecil di atas, dibaca U.\n\nبِ - Bi | تُ - Tu | ثِ - Tsi | جُ - Ju | حِ - Hi | خُ - Khu\n\nContoh:\nبِ - تِ - ثِ (Bi, Ti, Tsi)\nبُ - تُ - ثُ (Bu, Tu, Tsu)\n\nLatihan campur:\nبَ بِ بُ - Ba Bi Bu\nتَ تِ تُ - Ta Ti Tu\nكَ كِ كُ - Ka Ki Ku"},
    "Iqro 4": {"judul": "Iqro 4 - Tanwin & Panjang (Mad)", "materi": "Tanwin = 2 garis, dibaca An / In / Un.\nMad = dibaca panjang 2 ketukan.\n\nبًا - Ban | بٍ - Bin | بٌ - Bun\n\nMad Thabi'i:\nبَا - Baa (panjang) | بِي - Bii | بُو - Buu\n\nContoh:\nكِتَابٌ - Kitaabun (Kitab)\nرَسُولٌ - Rosuulun\nقَالَ - Qoola (dia berkata)\n\nLatihan: بَا - بِي - بُو | كَا - كِي - كُو"},
    "Iqro 5": {"judul": "Iqro 5 - Sukun, Tasydid & Qalqalah", "materi": "Sukun = huruf mati, tidak ada bunyi vokal.\nTasydid = huruf dibaca rangkap / ditekan.\n\nContoh Sukun:\nاَبْ - Ab | اَتْ - At | اَنْ - An\n\nContoh Tasydid:\nرَبَّ - Robba | اِنَّ - Inna | مُحَمَّدٌ - Muhammadun\n\nQalqalah (memantul): ق ط ب ج د\nContoh: اَقْ - Aq | اَطْ - Ath | اَبْ - Ab\n\nLatihan: مَنْ - Min | قَدْ - Qod | رَبِّ - Robbi"},
    "Iqro 6": {"judul": "Iqro 6 - Waqaf, Idgham & Siap Baca Al-Qur'an", "materi": "Waqaf = berhenti. Ibtida = mulai lagi.\nIdgham = melebur 2 huruf jadi 1.\n\nContoh Idgham:\nمِنْ رَبِّ - Mir Robbi (nun bertemu ro)\nمَنْ يَقُولُ - May Yaquulu\n\nWaqaf:\nTanda مـ = harus berhenti\nTanda ج = boleh berhenti / lanjut\nTanda لا = jangan berhenti\n\nLatihan baca surat pendek:\nبِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ - Bismillaahirrohmaanirrohiim\n\nKalau sudah lancar Iqro 6, lanjut ke Tahsin & Tahfidz Juz 30!"},
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

for k, v in [("login_nama",None),("login_role",None),("login_jabatan",None),("kategori_pilih",None),("messages",[]),("siswa_pilih",None),("seed_acak",1),("soal_acak",None),("kunci_acak",None),("kat_acak",None),("waktu_mulai",None),("waktu_habis",False),("ujian_selesai",False),("hasil_ujian",None),("lihat_nilai",False),("lihat_riwayat",False),("lihat_saran",False),("lihat_setoran",False),("lihat_baca",False),("lihat_video",True),("waktu_login",None),("sudah_catat_masuk",False),("jawaban_tersimpan",{}),("login_error",""),("login_error_time",0),("game",None),("game_question",None),("game_feedback",""),("game_question_no",0)]:
    if k not in st.session_state:
        st.session_state[k] = v

DURASI_UJIAN = 10*60
KKM = 75
prompt_awal = None
SYSTEM_PROMPT_KUNCI = "Kamu adalah QORI AI, guru yang ramah dan pintar untuk anak Madrasah Aliyah Al-Barokah. Kamu BEBAS menjawab pertanyaan apa saja: Iqro, Tahsin, Tahfidz, pelajaran sekolah, agama, umum. Jawab Bahasa Indonesia mudah, sopan, islami. Kalau menyebut huruf hijaiyah, WAJIB format: 1. Alif (ا) - dibaca \"A\"."

# ===== CEK PASSWORD =====
def cek_password(nama, password_input):
    pw_dict = st.secrets.get("USER_PASSWORDS", {})
    stored = pw_dict.get(nama) if hasattr(pw_dict, "get") else None
    if stored:
        if str(stored).startswith("pbkdf2_sha256$"):
            try:
                _, salt, digest = str(stored).split("$", 2)
                calculated = hashlib.pbkdf2_hmac("sha256", password_input.encode(), bytes.fromhex(salt), 300_000).hex()
                return hmac.compare_digest(calculated, digest)
            except (ValueError, TypeError):
                return False
        calculated = hashlib.sha256(password_input.encode()).hexdigest()
        return hmac.compare_digest(calculated, str(stored))
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
            <div style='background-color: rgba(0,0,0,0.55); padding:10px 14px; border-radius:10px; text-align:center; min-width:160px;'><p style='color:#F9D423; font-weight:bold; margin:0; font-size:15px;'>Kendar Sultoni</p><p style='color:white; margin:2px 0 0 0; font-size:13px;'>Mahasiswa</p></div>
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
    if st.session_state.get("login_error"):
        sisa = 5 - (time.time() - st.session_state["login_error_time"])
        if sisa > 0:
            st.error(st.session_state["login_error"])
            if st_autorefresh:
                st_autorefresh(interval=1000, key="cek_error_hilang")
            else:
                time.sleep(5)
                st.session_state["login_error"] = ""
                st.session_state["login_error_time"] = 0
                st.rerun()
        else:
            st.session_state["login_error"] = ""
            st.session_state["login_error_time"] = 0
            st.rerun()
    nama_input = st.text_input("✍️ Nama Lengkap:", placeholder="Tulis nama lengkapmu...", key="input_nama_login")
    pw_input = st.text_input("🔑 Password:", type="password", placeholder="Masukkan passwordmu...", key="input_pw_login")
    if st.button("🚪 Masuk ke QORI AI", use_container_width=True):
        nama_bersih = nama_input.strip().upper()
        if not nama_bersih or not pw_input:
            st.session_state["login_error"] = "⚠️ Nama & Password harus diisi!"
            st.session_state["login_error_time"] = time.time()
            st.rerun()
        elif nama_bersih in TIM_PENYUSUN or nama_bersih in DATA_SISWA:
            if not cek_password(nama_bersih, pw_input):
                st.session_state["login_error"] = "❌ Password salah! Tanya ke guru / tim kalau lupa."
                st.session_state["login_error_time"] = time.time()
                st.rerun()
            else:
                st.session_state["login_error"] = ""
                st.session_state["login_nama"] = nama_bersih
                if nama_bersih in TIM_PENYUSUN:
                    st.session_state["login_role"] = "tim"
                    st.session_state["login_jabatan"] = TIM_PENYUSUN[nama_bersih]
                    tampil = NAMA_LENGKAP_TIM.get(nama_bersih, nama_bersih)
                else:
                    st.session_state["login_role"] = "siswa"
                    st.session_state["login_jabatan"] = f"Siswa {DATA_SISWA[nama_bersih]['kategori']}"
                    tampil = nama_bersih
                # Reset sesi game saat akun berganti agar soal/skor akun sebelumnya
                # tidak terbawa ke akun berikutnya, termasuk akun dengan kategori sama.
                for k_game, v_game in [
                    ("game", None), ("game_question", None), ("game_questions", []),
                    ("game_index", 0), ("game_feedback", ""),
                    ("game_session_score", 0), ("game_session_key", None),
                    ("game_attempt_id", None),
                ]:
                    st.session_state[k_game] = v_game
                st.session_state["waktu_login"] = time.time()
                st.session_state["sudah_catat_masuk"] = False
                st.success(f"✅ Selamat datang, {tampil}")
                time.sleep(0.5)
                st.rerun()
        else:
            st.session_state["login_error"] = "❌ Nama tidak ditemukan! Cek lagi ejaannya, atau tanya ke guru."
            st.session_state["login_error_time"] = time.time()
            st.rerun()
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

# ===== MENU GAME QORI AI BERDASARKAN KATEGORI SISWA =====
st.markdown("### 🎮 Game QORI AI")
role_login = st.session_state.get("login_role")
nama_login = st.session_state.get("login_nama")
kategori_login = DATA_SISWA.get(nama_login, {}).get("kategori") if role_login == "siswa" else None

# PEMBATASAN TAMPILAN GAME:
# - Siswa Iqro hanya melihat Game Iqro'.
# - Siswa Tahsin hanya melihat Game Tahsin.
# - Siswa Tahfidz hanya melihat Game Tahfidz.
# - Siswa tidak melihat tombol game kategori lain.
# - Aturan ini khusus siswa; akun TIM tetap dapat melihat ketiga game.
if role_login == "siswa":
    game_diizinkan = {
        "Iqro": [("iqro", "🔤 Game Iqro'")],
        "Tahsin": [("tahsin", "📖 Game Tahsin")],
        "Tahfidz": [("tahfidz", "🧠 Game Tahfidz")],
    }.get(kategori_login, [])
    if not game_diizinkan:
        st.warning("Kategori akun siswa belum terdaftar. Silakan hubungi tim QORI AI.")
    else:
        game_key, game_label = game_diizinkan[0]
        st.caption(f"Akses siswa dibatasi: hanya **Game {kategori_login}** yang ditampilkan untuk akun kamu.")
        if st.button(game_label, use_container_width=True):
            st.session_state["game"] = game_key
            st.session_state["game_question"] = None
            st.session_state["game_feedback"] = ""
            st.rerun()
elif role_login == "tim":
    game_col1, game_col2, game_col3 = st.columns(3)
    with game_col1:
        if st.button("🔤 Game Iqro'", use_container_width=True):
            st.session_state["game"] = "iqro"
            st.session_state["game_question"] = None
            st.session_state["game_feedback"] = ""
            st.rerun()
    with game_col2:
        if st.button("📖 Game Tahsin", use_container_width=True):
            st.session_state["game"] = "tahsin"
            st.session_state["game_question"] = None
            st.session_state["game_feedback"] = ""
            st.rerun()
    with game_col3:
        if st.button("🧠 Game Tahfidz", use_container_width=True):
            st.session_state["game"] = "tahfidz"
            st.session_state["game_question"] = None
            st.session_state["game_feedback"] = ""
            st.rerun()

# ===== HALAMAN GAME QORI AI: 25 SOAL PER PERMAINAN =====
if st.session_state.get("game"):
    game_key = st.session_state["game"]
    kategori_game = {"iqro": "Iqro", "tahsin": "Tahsin", "tahfidz": "Tahfidz"}

    # Validasi akses kategori siswa setiap kali halaman game dirender.
    if st.session_state.get("login_role") == "siswa":
        kategori_akun = DATA_SISWA.get(st.session_state.get("login_nama"), {}).get("kategori")
        if kategori_game.get(game_key) != kategori_akun:
            st.session_state["game"] = None
            st.session_state["game_question"] = None
            st.session_state["game_questions"] = []
            st.session_state["game_index"] = 0
            st.session_state["game_feedback"] = ""
            st.warning("Akses ditolak. Game ini tidak sesuai dengan kategori akun siswa kamu.")
            st.stop()

    # Enam tingkat kesulitan tersedia untuk setiap kategori game.
    LEVEL_GAME = {
        1: ("Pemula", "Paling mudah: pengenalan dasar dengan 3 pilihan."),
        2: ("Dasar", "Mulai mengenali variasi dan tanda baca dengan 3 pilihan."),
        3: ("Menengah Awal", "Soal lebih menantang dengan 4 pilihan."),
        4: ("Menengah", "Membedakan materi yang mirip dengan 4 pilihan."),
        5: ("Lanjutan", "Pengecoh lebih beragam dengan 5 pilihan."),
        6: ("Mahir", "Tantangan tertinggi dengan konteks lebih sedikit dan hingga 6 pilihan."),
    }
    pilihan_level = [f"Level {i} – {LEVEL_GAME[i][0]}" for i in range(1, 7)]
    level_label = st.selectbox(
        "Pilih tingkat kesulitan",
        pilihan_level,
        index=0,
        key=f"pilih_level_{game_key}"
    )
    level_game = int(level_label.split()[1])
    st.caption(LEVEL_GAME[level_game][1])
    opsi_level_info = {1: 3, 2: 3, 3: 4, 4: 4, 5: 5, 6: 6}
    st.info(f"🎯 Level {level_game} – {LEVEL_GAME[level_game][0]} | 25 soal | hingga {opsi_level_info[level_game]} pilihan jawaban")

    if game_key == "iqro":
        st.markdown("## 🔤 Game Iqro' - Tebak Huruf Hijaiyah")
        bank_huruf = [
            ("ا","Alif"),("ب","Ba"),("ت","Ta"),("ث","Tsa"),("ج","Jim"),
            ("ح","Ha"),("خ","Kho"),("د","Dal"),("ذ","Dzal"),("ر","Ro"),
            ("ز","Za"),("س","Sin"),("ش","Syin"),("ص","Shod"),("ض","Dhod"),
            ("ط","Tho"),("ظ","Zho"),("ع","Ain"),("غ","Ghoin"),("ف","Fa"),
            ("ق","Qof"),("ك","Kaf"),("ل","Lam"),("م","Mim"),("ن","Nun"),
            ("و","Wau"),("ه","Ha"),("ء","Hamzah"),("ي","Ya")
        ]
        bank = [(huruf, nama, random.sample([x[1] for x in bank_huruf if x[1] != nama], 2) + [nama]) for huruf, nama in bank_huruf]
        judul_game = "Game Iqro'"

    elif game_key == "tahsin":
        st.markdown("## 📖 Game Tahsin - Tebak Hukum Tajwid")
        bank = [
            ("مِنْ شَرِّ", "Ikhfa", ["Ikhfa", "Izhar", "Iqlab"]),
            ("مِنْ بَعْدِ", "Iqlab", ["Iqlab", "Ikhfa", "Idgham"]),
            ("مَنْ آمَنَ", "Izhar", ["Izhar", "Ikhfa", "Iqlab"]),
            ("مِنْ رَبِّهِمْ", "Idgham Bilaghunnah", ["Idgham Bilaghunnah", "Idgham Bighunnah", "Ikhfa"]),
            ("مَنْ يَعْمَلْ", "Idgham Bighunnah", ["Idgham Bighunnah", "Izhar", "Iqlab"]),
            ("مِنْ مَالٍ", "Idgham Bighunnah", ["Ikhfa", "Idgham Bighunnah", "Izhar"]),
            ("مِنْ نِعْمَةٍ", "Idgham Bighunnah", ["Iqlab", "Idgham Bighunnah", "Izhar"]),
            ("مِنْ هَادٍ", "Izhar", ["Izhar", "Ikhfa", "Idgham"]),
            ("مِنْ عِلْمٍ", "Izhar", ["Iqlab", "Izhar", "Ikhfa"]),
            ("مِنْ خَيْرٍ", "Izhar", ["Idgham", "Ikhfa", "Izhar"]),
            ("مِنْ غِلٍّ", "Izhar", ["Izhar", "Iqlab", "Idgham"]),
            ("مِنْ حَكِيمٍ", "Izhar", ["Ikhfa", "Izhar", "Idgham"]),
            ("سَمِيعٌ بَصِيرٌ", "Iqlab", ["Idgham", "Iqlab", "Ikhfa"]),
            ("عَلِيمٌ قَدِيرٌ", "Ikhfa", ["Izhar", "Ikhfa", "Iqlab"]),
            ("غَفُورٌ رَحِيمٌ", "Idgham Bilaghunnah", ["Idgham Bilaghunnah", "Ikhfa", "Iqlab"]),
            ("هُدًى لِلْمُتَّقِينَ", "Idgham Bilaghunnah", ["Izhar", "Idgham Bilaghunnah", "Iqlab"]),
            ("وُجُوهٌ يَوْمَئِذٍ", "Idgham Bighunnah", ["Idgham Bighunnah", "Izhar", "Ikhfa"]),
            ("قَوْمًا ظَالِمِينَ", "Ikhfa", ["Iqlab", "Ikhfa", "Izhar"]),
            ("أَنْفُسَكُمْ", "Ikhfa", ["Ikhfa", "Izhar", "Idgham"]),
            ("أَنْبِئْهُمْ", "Iqlab", ["Iqlab", "Ikhfa", "Izhar"]),
            ("مِنْ دُونِ", "Ikhfa", ["Izhar", "Ikhfa", "Iqlab"]),
            ("مِنْ تَحْتِهَا", "Ikhfa", ["Idgham", "Ikhfa", "Izhar"]),
            ("مِنْ صَلْصَالٍ", "Ikhfa", ["Iqlab", "Izhar", "Ikhfa"]),
            ("مِنْ ذَكَرٍ", "Ikhfa", ["Ikhfa", "Idgham", "Izhar"]),
            ("مِنْ جُوعٍ", "Ikhfa", ["Izhar", "Iqlab", "Ikhfa"]),
        ]
        judul_game = "Game Tahsin"

    else:
        st.markdown("## 🧠 Game Tahfidz - Sambung Ayat")
        bank = [
            ("قُلْ هُوَ اللَّهُ أَحَدٌ", "اللَّهُ الصَّمَدُ", ["اللَّهُ الصَّمَدُ", "لَمْ يَلِدْ", "وَلَمْ يُولَدْ"]),
            ("اللَّهُ الصَّمَدُ", "لَمْ يَلِدْ وَلَمْ يُولَدْ", ["لَمْ يَلِدْ وَلَمْ يُولَدْ", "وَلَمْ يَكُنْ لَهُ", "قُلْ هُوَ اللَّهُ"]),
            ("لَمْ يَلِدْ وَلَمْ يُولَدْ", "وَلَمْ يَكُنْ لَهُ كُفُوًا أَحَدٌ", ["وَلَمْ يَكُنْ لَهُ كُفُوًا أَحَدٌ", "اللَّهُ الصَّمَدُ", "قُلْ أَعُوذُ بِرَبِّ الْفَلَقِ"]),
            ("قُلْ أَعُوذُ بِرَبِّ الْفَلَقِ", "مِنْ شَرِّ مَا خَلَقَ", ["مِنْ شَرِّ مَا خَلَقَ", "وَمِنْ شَرِّ غَاسِقٍ", "مِنَ الْجِنَّةِ وَالنَّاسِ"]),
            ("مِنْ شَرِّ مَا خَلَقَ", "وَمِنْ شَرِّ غَاسِقٍ إِذَا وَقَبَ", ["وَمِنْ شَرِّ غَاسِقٍ إِذَا وَقَبَ", "قُلْ أَعُوذُ بِرَبِّ النَّاسِ", "وَمِنْ شَرِّ حَاسِدٍ"]),
            ("قُلْ أَعُوذُ بِرَبِّ النَّاسِ", "مَلِكِ النَّاسِ", ["مَلِكِ النَّاسِ", "إِلَٰهِ النَّاسِ", "مِنْ شَرِّ الْوَسْوَاسِ"]),
            ("مَلِكِ النَّاسِ", "إِلَٰهِ النَّاسِ", ["إِلَٰهِ النَّاسِ", "مِنَ الْجِنَّةِ وَالنَّاسِ", "قُلْ أَعُوذُ بِرَبِّ الْفَلَقِ"]),
            ("وَالْعَصْرِ", "إِنَّ الْإِنْسَانَ لَفِي خُسْرٍ", ["إِنَّ الْإِنْسَانَ لَفِي خُسْرٍ", "إِلَّا الَّذِينَ آمَنُوا", "وَتَوَاصَوْا بِالصَّبْرِ"]),
            ("إِنَّ الْإِنْسَانَ لَفِي خُسْرٍ", "إِلَّا الَّذِينَ آمَنُوا وَعَمِلُوا الصَّالِحَاتِ", ["إِلَّا الَّذِينَ آمَنُوا وَعَمِلُوا الصَّالِحَاتِ", "وَالْعَصْرِ", "وَتَوَاصَوْا بِالْحَقِّ"]),
            ("إِلَّا الَّذِينَ آمَنُوا وَعَمِلُوا الصَّالِحَاتِ", "وَتَوَاصَوْا بِالْحَقِّ وَتَوَاصَوْا بِالصَّبْرِ", ["وَتَوَاصَوْا بِالْحَقِّ وَتَوَاصَوْا بِالصَّبْرِ", "إِنَّ الْإِنْسَانَ لَفِي خُسْرٍ", "وَالْعَصْرِ"]),
            ("إِنَّا أَعْطَيْنَاكَ الْكَوْثَرَ", "فَصَلِّ لِرَبِّكَ وَانْحَرْ", ["فَصَلِّ لِرَبِّكَ وَانْحَرْ", "إِنَّ شَانِئَكَ هُوَ الْأَبْتَرُ", "قُلْ هُوَ اللَّهُ أَحَدٌ"]),
            ("فَصَلِّ لِرَبِّكَ وَانْحَرْ", "إِنَّ شَانِئَكَ هُوَ الْأَبْتَرُ", ["إِنَّ شَانِئَكَ هُوَ الْأَبْتَرُ", "إِنَّا أَعْطَيْنَاكَ الْكَوْثَرَ", "وَالْعَصْرِ"]),
            ("أَلْهَاكُمُ التَّكَاثُرُ", "حَتَّىٰ زُرْتُمُ الْمَقَابِرَ", ["حَتَّىٰ زُرْتُمُ الْمَقَابِرَ", "كَلَّا سَوْفَ تَعْلَمُونَ", "لَتَرَوُنَّ الْجَحِيمَ"]),
            ("حَتَّىٰ زُرْتُمُ الْمَقَابِرَ", "كَلَّا سَوْفَ تَعْلَمُونَ", ["كَلَّا سَوْفَ تَعْلَمُونَ", "أَلْهَاكُمُ التَّكَاثُرُ", "ثُمَّ لَتُسْأَلُنَّ"]),
            ("قُلْ يَا أَيُّهَا الْكَافِرُونَ", "لَا أَعْبُدُ مَا تَعْبُدُونَ", ["لَا أَعْبُدُ مَا تَعْبُدُونَ", "وَلَا أَنَا عَابِدٌ", "لَكُمْ دِينُكُمْ"]),
            ("لَا أَعْبُدُ مَا تَعْبُدُونَ", "وَلَا أَنْتُمْ عَابِدُونَ مَا أَعْبُدُ", ["وَلَا أَنْتُمْ عَابِدُونَ مَا أَعْبُدُ", "لَكُمْ دِينُكُمْ", "قُلْ يَا أَيُّهَا الْكَافِرُونَ"]),
            ("لَكُمْ دِينُكُمْ", "وَلِيَ دِينِ", ["وَلِيَ دِينِ", "لَا أَعْبُدُ مَا تَعْبُدُونَ", "وَلَا أَنَا عَابِدٌ"]),
            ("إِذَا جَاءَ نَصْرُ اللَّهِ وَالْفَتْحُ", "وَرَأَيْتَ النَّاسَ يَدْخُلُونَ فِي دِينِ اللَّهِ أَفْوَاجًا", ["وَرَأَيْتَ النَّاسَ يَدْخُلُونَ فِي دِينِ اللَّهِ أَفْوَاجًا", "فَسَبِّحْ بِحَمْدِ رَبِّكَ", "إِنَّا أَعْطَيْنَاكَ الْكَوْثَرَ"]),
            ("وَرَأَيْتَ النَّاسَ يَدْخُلُونَ فِي دِينِ اللَّهِ أَفْوَاجًا", "فَسَبِّحْ بِحَمْدِ رَبِّكَ وَاسْتَغْفِرْهُ", ["فَسَبِّحْ بِحَمْدِ رَبِّكَ وَاسْتَغْفِرْهُ", "إِذَا جَاءَ نَصْرُ اللَّهِ", "وَالْعَصْرِ"]),
            ("تَبَّتْ يَدَا أَبِي لَهَبٍ وَتَبَّ", "مَا أَغْنَىٰ عَنْهُ مَالُهُ وَمَا كَسَبَ", ["مَا أَغْنَىٰ عَنْهُ مَالُهُ وَمَا كَسَبَ", "سَيَصْلَىٰ نَارًا ذَاتَ لَهَبٍ", "فِي جِيدِهَا حَبْلٌ"]),
            ("مَا أَغْنَىٰ عَنْهُ مَالُهُ وَمَا كَسَبَ", "سَيَصْلَىٰ نَارًا ذَاتَ لَهَبٍ", ["سَيَصْلَىٰ نَارًا ذَاتَ لَهَبٍ", "تَبَّتْ يَدَا أَبِي لَهَبٍ", "وَامْرَأَتُهُ حَمَّالَةَ الْحَطَبِ"]),
            ("وَالشَّمْسِ وَضُحَاهَا", "وَالْقَمَرِ إِذَا تَلَاهَا", ["وَالْقَمَرِ إِذَا تَلَاهَا", "وَالنَّهَارِ إِذَا جَلَّاهَا", "وَاللَّيْلِ إِذَا يَغْشَاهَا"]),
            ("وَالْقَمَرِ إِذَا تَلَاهَا", "وَالنَّهَارِ إِذَا جَلَّاهَا", ["وَالنَّهَارِ إِذَا جَلَّاهَا", "وَالشَّمْسِ وَضُحَاهَا", "وَالسَّمَاءِ وَمَا بَنَاهَا"]),
            ("وَالضُّحَىٰ", "وَاللَّيْلِ إِذَا سَجَىٰ", ["وَاللَّيْلِ إِذَا سَجَىٰ", "مَا وَدَّعَكَ رَبُّكَ", "وَلَلْآخِرَةُ خَيْرٌ"]),
            ("أَلَمْ نَشْرَحْ لَكَ صَدْرَكَ", "وَوَضَعْنَا عَنْكَ وِزْرَكَ", ["وَوَضَعْنَا عَنْكَ وِزْرَكَ", "الَّذِي أَنْقَضَ ظَهْرَكَ", "وَرَفَعْنَا لَكَ ذِكْرَكَ"]),
        ]
        judul_game = "Game Tahfidz"

    # Sesuaikan tantangan dengan level: semakin tinggi level, semakin banyak
    # pilihan jawaban. Pada Tahfidz, petunjuk ayat dipersingkat pada level tinggi.
    jumlah_soal = 25
    jumlah_opsi_per_level = {1: 3, 2: 3, 3: 4, 4: 4, 5: 5, 6: 6}
    jumlah_opsi = jumlah_opsi_per_level[level_game]
    semua_jawaban = list(dict.fromkeys(item[1] for item in bank))
    bank_level = []
    for prompt_asli, jawaban_asli, opsi_asli in bank:
        prompt_level = prompt_asli
        if game_key == "iqro" and level_game >= 2:
            tanda = {2: "َ", 3: "ِ", 4: "ُ", 5: "ْ", 6: "ّ"}.get(level_game, "")
            prompt_level = prompt_asli + tanda
        elif game_key == "tahfidz" and level_game >= 2:
            kata = prompt_asli.split()
            jumlah_kata = {2: 5, 3: 4, 4: 3, 5: 2, 6: 1}[level_game]
            prompt_level = " ".join(kata[-jumlah_kata:])

        kandidat = list(dict.fromkeys([jawaban_asli] + list(opsi_asli) + semua_jawaban))
        pengecoh = [x for x in kandidat if x != jawaban_asli]
        random.shuffle(pengecoh)
        opsi_level = [jawaban_asli] + pengecoh[:max(0, jumlah_opsi - 1)]
        random.shuffle(opsi_level)
        bank_level.append((prompt_level, jawaban_asli, opsi_level))

    judul_game_level = f"{judul_game} - Level {level_game}"
    session_key_baru = f"{game_key}_level_{level_game}"
    if st.session_state.get("game_session_key") != session_key_baru:
        st.session_state["game_session_key"] = session_key_baru
        st.session_state["game_questions"] = random.sample(bank_level, jumlah_soal)
        st.session_state["game_index"] = 0
        st.session_state["game_question"] = None
        st.session_state["game_feedback"] = ""
        st.session_state["game_session_score"] = 0
        st.session_state["game_attempt_id"] = f"{time.time_ns()}-{random.randint(1000,9999)}"

    indeks = st.session_state.get("game_index", 0)
    if indeks >= jumlah_soal:
        # Simpan nilai akhir satu kali untuk rekap khusus Tim.
        if st.session_state.get("login_role") == "siswa":
            nama_hasil = st.session_state.get("login_nama", "")
            kelas_hasil = DATA_SISWA.get(nama_hasil, {}).get("kategori", "-")
            if kelas_hasil == kategori_game.get(game_key):
                simpan_hasil_game(
                    st.session_state.get("game_attempt_id", str(time.time_ns())),
                    nama_hasil, kelas_hasil, judul_game, level_game,
                    st.session_state.get("game_session_score", 0), jumlah_soal
                )
        st.success("🎉 MasyaAllah! Kamu telah menyelesaikan 25 soal.")
        st.metric("Skor sesi ini", st.session_state.get("game_session_score", 0))
        st.write("Skor maksimal: 250 poin.")
        if st.button("🔁 Main Lagi (25 Soal Baru)", use_container_width=True):
            st.session_state["game_questions"] = random.sample(bank_level, jumlah_soal)
            st.session_state["game_index"] = 0
            st.session_state["game_question"] = None
            st.session_state["game_feedback"] = ""
            st.session_state["game_session_score"] = 0
            st.session_state["game_attempt_id"] = f"{time.time_ns()}-{random.randint(1000,9999)}"
            st.rerun()
        if st.button("❌ Tutup Game", use_container_width=True):
            st.session_state["game"] = None
            st.session_state["game_session_key"] = None
            st.session_state["game_question"] = None
            st.rerun()
        st.stop()

    if st.session_state.get("game_question") is None:
        item = st.session_state["game_questions"][indeks]
        prompt_game, jawaban_benar, pilihan_asli = item
        pilihan_game = list(pilihan_asli)
        random.shuffle(pilihan_game)
        st.session_state["game_question"] = {"prompt": prompt_game, "answer": jawaban_benar, "options": pilihan_game}

    q = st.session_state["game_question"]
    st.progress(indeks / jumlah_soal, text=f"Soal {indeks + 1} dari {jumlah_soal}")
    if game_key == "iqro":
        st.markdown(f"<div style='background:white;color:#111;padding:28px;border-radius:15px;text-align:center;font-size:100px;'>{q['prompt']}</div>", unsafe_allow_html=True)
        st.write("Apa nama huruf hijaiyah di atas?")
    else:
        st.markdown(f"<div style='background:white;color:#111;padding:22px;border-radius:15px;text-align:center;font-size:34px;direction:rtl;'>{q['prompt']}{' ... ؟' if game_key == 'tahfidz' else ''}</div>", unsafe_allow_html=True)
        st.write("Apa hukum tajwid dari lafaz di atas?" if game_key == "tahsin" else "Apa lanjutan ayat yang benar?")

    if st.session_state.get("game_feedback"):
        st.info(st.session_state["game_feedback"])

    for idx, opsi_jawaban in enumerate(q["options"]):
        if st.button(opsi_jawaban, key=f"game_{game_key}_{indeks}_{idx}", use_container_width=True):
            if opsi_jawaban == q["answer"]:
                st.session_state["game_session_score"] += 10
                nama_login = st.session_state.get("login_nama") or "Pengguna"
                if st.session_state.get("login_role") == "siswa":
                    kelas_login = DATA_SISWA.get(nama_login, {}).get("kategori", "-")
                    if kelas_login == kategori_game.get(game_key):
                        simpan_skor_game(nama_login, kelas_login, judul_game_level, 10)
                st.session_state["game_feedback"] = "✅ Benar! MasyaAllah, kamu mendapat 10 poin."
            else:
                st.session_state["game_feedback"] = f"❌ Belum tepat. Jawaban yang benar: {q['answer']}. Soal berikutnya akan ditampilkan."

            # Setiap jawaban hanya boleh satu kali. Benar atau salah, langsung lanjut.
            st.session_state["game_index"] += 1
            st.session_state["game_question"] = None
            st.rerun()

    st.metric("⭐ Skor sesi ini", st.session_state.get("game_session_score", 0))
    st.caption("Setiap soal hanya dijawab satu kali. Jawaban benar mendapat 10 poin; jika salah, skor tidak bertambah dan permainan langsung lanjut ke soal berikutnya.")
    if st.button("❌ Tutup Game", use_container_width=True):
        st.session_state["game"] = None
        st.session_state["game_session_key"] = None
        st.session_state["game_question"] = None
        st.session_state["game_questions"] = []
        st.session_state["game_index"] = 0
        st.session_state["game_feedback"] = ""
        st.rerun()
    st.stop()

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
        st.session_state["lihat_setoran"] = False
        st.session_state["lihat_baca"] = False
        st.session_state["sudah_catat_masuk"] = False
        st.session_state["waktu_login"] = None
        # Tutup dan bersihkan sesi game ketika keluar/ganti akun.
        st.session_state["game"] = None
        st.session_state["game_question"] = None
        st.session_state["game_questions"] = []
        st.session_state["game_index"] = 0
        st.session_state["game_feedback"] = ""
        st.session_state["game_session_score"] = 0
        st.session_state["game_session_key"] = None
        st.session_state["game_attempt_id"] = None
        st.session_state["lihat_video"] = True
        st.session_state["login_error"] = ""
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
            st.session_state["siswa_pilih"]=item; st.session_state["seed_acak"]+=1; st.session_state["soal_acak"]=None; st.session_state["waktu_mulai"]=time.time(); simpan_sesi_ujian(item, st.session_state["waktu_mulai"], st.session_state["seed_acak"]); st.session_state["waktu_habis"]=False; st.session_state["ujian_selesai"]=False; st.session_state["hasil_ujian"]=None; st.session_state["lihat_nilai"]=False; st.session_state["lihat_riwayat"]=False; st.session_state["lihat_saran"]=False; st.session_state["lihat_setoran"]=False; st.session_state["lihat_baca"]=False; st.session_state["jawaban_tersimpan"]={}
            catat_aktivitas(f"Mulai Ujian - {kategori}")
            st.rerun()

# ===== MENU UTAMA =====
if st.session_state["siswa_pilih"] is None and not st.session_state["lihat_nilai"]:
    c1,c2,c3,c4 = st.columns(4)
    with c1: klik_iqro = st.button("📖 Iqro", use_container_width=True)
    with c2: klik_tahsin = st.button("📗 Tahsin", use_container_width=True)
    with c3: klik_tahfidz = st.button("⭐ Tahfidz", use_container_width=True)
    with c4: klik_nilai = st.button("📊 Daftar Hasil Nilai", use_container_width=True)
    if klik_iqro: st.session_state["kategori_pilih"] = None if st.session_state["kategori_pilih"]=="Iqro" else "Iqro"; st.session_state["lihat_nilai"]=False; st.session_state["lihat_riwayat"]=False; st.session_state["lihat_saran"]=False; st.session_state["lihat_setoran"]=False; st.session_state["lihat_baca"]=False; catat_aktivitas("Buka Kelas Iqro")
    if klik_tahsin: st.session_state["kategori_pilih"] = None if st.session_state["kategori_pilih"]=="Tahsin" else "Tahsin"; st.session_state["lihat_nilai"]=False; st.session_state["lihat_riwayat"]=False; st.session_state["lihat_saran"]=False; st.session_state["lihat_setoran"]=False; st.session_state["lihat_baca"]=False; catat_aktivitas("Buka Kelas Tahsin")
    if klik_tahfidz: st.session_state["kategori_pilih"] = None if st.session_state["kategori_pilih"]=="Tahfidz" else "Tahfidz"; st.session_state["lihat_nilai"]=False; st.session_state["lihat_riwayat"]=False; st.session_state["lihat_saran"]=False; st.session_state["lihat_setoran"]=False; st.session_state["lihat_baca"]=False; catat_aktivitas("Buka Kelas Tahfidz")
    if klik_nilai: st.session_state["lihat_nilai"]=True; st.session_state["kategori_pilih"]=None; st.session_state["lihat_riwayat"]=False; st.session_state["lihat_saran"]=False; st.session_state["lihat_setoran"]=False; st.session_state["lihat_baca"]=False; catat_aktivitas("Buka Daftar Hasil Nilai")
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
        st.session_state["lihat_riwayat"]=True; st.session_state["kategori_pilih"]=None; st.session_state["lihat_nilai"]=False; st.session_state["lihat_saran"]=False; st.session_state["lihat_setoran"]=False; st.session_state["lihat_baca"]=False; st.rerun()
if st.session_state["siswa_pilih"] is None:
    if st.button("📖 Baca Juz 30 & Iqro 1-6 (Langsung Baca Di Sini)", use_container_width=True):
        st.session_state["lihat_baca"]=True; st.session_state["kategori_pilih"]=None; st.session_state["lihat_nilai"]=False; st.session_state["lihat_riwayat"]=False; st.session_state["lihat_saran"]=False; st.session_state["lihat_setoran"]=False; catat_aktivitas("Buka Baca Juz 30 & Iqro"); st.rerun()
if st.session_state["siswa_pilih"] is None:
    jml_baru = len([s for s in get_saran() if not s["balasan"]]) if st.session_state["login_role"]=="tim" else len([s for s in get_saran() if s["pengirim"]==st.session_state["login_nama"] and s["balasan"]])
    label_saran = f"💬 Kotak Saran / Kritik / Keluhan ({jml_baru} Baru)" if jml_baru>0 else "💬 Kotak Saran / Kritik / Keluhan"
    if st.button(label_saran, use_container_width=True):
        st.session_state["lihat_saran"]=True; st.session_state["kategori_pilih"]=None; st.session_state["lihat_nilai"]=False; st.session_state["lihat_riwayat"]=False; st.session_state["lihat_setoran"]=False; st.session_state["lihat_baca"]=False; catat_aktivitas("Buka Kotak Saran"); st.rerun()
if st.session_state["siswa_pilih"] is None:
    jml_setoran_baru = len([s for s in get_setoran() if not s["koreksi"]]) if st.session_state["login_role"]=="tim" else len([s for s in get_setoran() if s["pengirim"]==st.session_state["login_nama"] and s["koreksi"]])
    label_setoran = f"🎙️ Setoran Suara / Koreksi Bacaan ({jml_setoran_baru} Baru)" if jml_setoran_baru>0 else "🎙️ Setoran Suara / Koreksi Bacaan (Foto + Suara)"
    if st.button(label_setoran, use_container_width=True):
        st.session_state["lihat_setoran"]=True; st.session_state["kategori_pilih"]=None; st.session_state["lihat_nilai"]=False; st.session_state["lihat_riwayat"]=False; st.session_state["lihat_saran"]=False; st.session_state["lihat_baca"]=False; catat_aktivitas("Buka Setoran Suara"); st.rerun()

# ===== BACA JUZ 30 & IQRO 1-6 =====
if st.session_state.get("lihat_baca") and st.session_state["siswa_pilih"] is None:
    st.markdown("<div style='background-color: rgba(20,50,35,0.95); padding:18px; border-radius:15px; text-align:center; border:2px solid #F9D423;'><h2 style='color:#F9D423; margin:0;'>📖 Baca Juz 30 & Iqro 1-6</h2><p style='color:white;'>Baca dulu di sini, baru Setoran Suara</p></div>", unsafe_allow_html=True)
    st.write("")
    # Otomatis arahkan sesuai kelas siswa
    if st.session_state["login_role"]=="siswa":
        kat_siswa = DATA_SISWA.get(st.session_state["login_nama"],{}).get("kategori","Tahsin")
        default_tab = "Iqro 1-6" if kat_siswa=="Iqro" else "Juz 30 (Tahsin & Tahfidz)"
    else:
        default_tab = "Juz 30 (Tahsin & Tahfidz)"
    tab_pilih = st.radio("Pilih Bacaan:", ["Juz 30 (Tahsin & Tahfidz)", "Iqro 1-6"], index=0 if default_tab.startswith("Juz") else 1, horizontal=True, key="tab_baca")
    if tab_pilih == "Juz 30 (Tahsin & Tahfidz)":
        st.markdown("<p style='color:white; font-weight:bold;'>Pilih Surat Juz 30:</p>", unsafe_allow_html=True)
        surat_baca = st.selectbox("Surat:", JUZ30_SURAH, key="surat_baca")
        isi = JUZ30_BACA.get(surat_baca, {})
        st.markdown(f"<div style='background-color: rgba(0,0,0,0.75); padding:18px; border-radius:15px; text-align:center;'><h3 style='color:#F9D423; margin:0;'>{surat_baca} - {isi.get('ayat','')}</h3><p style='color:white; font-size:26px; line-height:2.2; direction:rtl; text-align:right; margin:15px 0 0 0;'>{isi.get('arab','')}</p></div>", unsafe_allow_html=True)
        st.write("")
        st.markdown(f"<div style='background-color: rgba(255,255,255,0.12); padding:14px; border-radius:12px;'><p style='color:#F9D423; font-weight:bold; margin:0;'>Latin (Cara Baca):</p><p style='color:white;'>{isi.get('latin','')}</p><p style='color:#F9D423; font-weight:bold; margin:10px 0 0 0;'>Artinya:</p><p style='color:white;'>{isi.get('arti','')}</p></div>", unsafe_allow_html=True)
        st.info("Untuk surat yang panjang (An-Naba sampai Al-Fajr dll), di atas ditampilkan awal suratnya. Lanjutkan baca lengkapnya di mushaf / Iqro, lalu Setoran Suara.")
        if st.button("🎙️ Langsung Setoran Surat Ini", use_container_width=True):
            st.session_state["lihat_baca"]=False; st.session_state["lihat_setoran"]=True; st.rerun()
    else:
        st.markdown("<p style='color:white; font-weight:bold;'>Pilih Iqro:</p>", unsafe_allow_html=True)
        iqro_pilih = st.selectbox("Iqro:", list(IQRO_BACA.keys()), key="iqro_baca")
        isi_iqro = IQRO_BACA[iqro_pilih]
        st.markdown(f"<div style='background-color: rgba(0,0,0,0.75); padding:18px; border-radius:15px;'><h3 style='color:#F9D423; text-align:center; margin:0;'>{isi_iqro['judul']}</h3><p style='color:white; font-size:19px; line-height:2.0; white-space:pre-line; margin:12px 0 0 0;'>{isi_iqro['materi']}</p></div>", unsafe_allow_html=True)
        st.info("Baca pelan-pelan, perhatikan harakatnya. Kalau sudah lancar, langsung Setoran Suara.")
        if st.button("🎙️ Langsung Setoran Iqro Ini", use_container_width=True):
            st.session_state["lihat_baca"]=False; st.session_state["lihat_setoran"]=True; st.rerun()
    st.write("")
    if st.button("⬅️ Tutup Bacaan", use_container_width=True):
        st.session_state["lihat_baca"]=False; st.rerun()
    st.stop()

# ===== SETORAN SUARA - HANYA UPLOAD =====
if st.session_state.get("lihat_setoran") and st.session_state["siswa_pilih"] is None:
    st.markdown("<div style='background-color: rgba(20,50,35,0.95); padding:18px; border-radius:15px; text-align:center; border:2px solid #F9D423;'><h2 style='color:#F9D423; margin:0;'>🎙️ Setoran Suara / Koreksi Bacaan</h2><p style='color:white;'>Iqro | Tahsin | Tahfidz - Pilih Surat Juz 30 + Upload Foto + Upload Suara</p></div>", unsafe_allow_html=True)
    st.write("")
    st.markdown("<p style='color:white; font-weight:bold; font-size:17px;'>📤 Kirim Setoran Baru:</p>", unsafe_allow_html=True)
    if st.session_state["login_role"]=="siswa":
        kat_default = DATA_SISWA.get(st.session_state["login_nama"],{}).get("kategori","Tahsin")
        idx_kat = ["Iqro","Tahsin","Tahfidz"].index(kat_default) if kat_default in ["Iqro","Tahsin","Tahfidz"] else 1
    else:
        idx_kat = 1
    kat_setoran = st.selectbox("Kategori Setoran:", ["Iqro","Tahsin","Tahfidz"], index=idx_kat, key="kat_setoran")
    surat_juz30 = st.selectbox("📖 Pilih Surat Juz 30 (kalau setoran Tahfidz / Tahsin):", ["-- Ketik Sendiri / Bukan Juz 30 --"] + JUZ30_SURAH, key="surat_juz30")
    if surat_juz30 != "-- Ketik Sendiri / Bukan Juz 30 --":
        st.info(f"Surat dipilih: **{surat_juz30}** — tinggal isi ayatnya di bawah kalau perlu.")
    judul_setoran = st.text_input("Materi / Ayat / Judul Setoran:", placeholder="Contoh: Ayat 1-4 | Iqro 2 Hal. 5 | Atau kosongkan kalau sudah pilih surat di atas", key="judul_setoran")
    ket_setoran = st.text_area("Keterangan (opsional):", placeholder="Contoh: Mohon dikoreksi makhraj huruf... / Ayat 1-4...", height=70, key="ket_setoran")
    foto_up = st.file_uploader("📷 Upload Foto (halaman Iqro / tulisan / mushaf):", type=["jpg","jpeg","png","webp"], key="foto_setoran")
    st.markdown("<div style='background-color: rgba(249,212,35,0.15); border:1.5px solid #F9D423; padding:12px; border-radius:12px;'><p style='color:#F9D423; font-weight:bold; margin:0;'>🎤 Cara Kirim Suara di HP:</p><p style='color:white; margin:5px 0 0 0;'>1. Rekam dulu pakai <b>Perekam HP</b> atau <b>Voice Note WA</b><br>2. Terus Upload file-nya di bawah ini<br>❌ Jangan pencet mic Google yang di atas layar!</p></div>", unsafe_allow_html=True)
    st.write("")
    audio_file = st.file_uploader("📤 Upload File Suara Di Sini (WA / Perekam HP):", type=["mp3","wav","m4a","ogg","webm","opus","aac"], key="audio_file_setoran")
    if audio_file:
        st.success(f"✅ Suara terpilih: {audio_file.name} - Coba putar dulu sebelum kirim, pastikan ada suaranya!")
        st.audio(audio_file)
    if st.button("📩 Kirim Setoran ke Tim", use_container_width=True):
        if surat_juz30 != "-- Ketik Sendiri / Bukan Juz 30 --":
            if judul_setoran.strip():
                judul_final = f"{surat_juz30} - {judul_setoran.strip()}"
            else:
                judul_final = surat_juz30
        else:
            judul_final = judul_setoran.strip()
        if not judul_final:
            st.warning("⚠️ Pilih dulu Surat Juz 30 di atas, atau isi Materi / Judul Setorannya!")
        elif not audio_file:
            st.warning("⚠️ Suaranya belum ada! Rekam di WA / Perekam HP dulu, terus Upload di atas.")
        else:
            if st.session_state["login_role"]=="siswa":
                label = f"{st.session_state['login_nama']} | Kelas: {DATA_SISWA.get(st.session_state['login_nama'],{}).get('kategori','-')}"
            else:
                label = f"{NAMA_LENGKAP_TIM.get(st.session_state['login_nama'], st.session_state['login_nama'])} | {TIM_PENYUSUN.get(st.session_state['login_nama'],'Tim')}"
            foto_bytes = foto_up.getvalue() if foto_up else None
            foto_nama = foto_up.name if foto_up else ""
            audio_bytes = audio_file.getvalue(); audio_nama = audio_file.name
            tambah_setoran(st.session_state["login_nama"], label, kat_setoran, judul_final, ket_setoran.strip(), foto_bytes, foto_nama, audio_bytes, audio_nama, time.strftime("%d/%m/%Y %H:%M", time.localtime(time.time())))
            catat_aktivitas(f"Kirim Setoran {kat_setoran} - {judul_final[:30]}")
            st.success("✅ Setoran terkirim! Tim akan mendengarkan & mengoreksi.")
            time.sleep(0.5); st.rerun()
    st.write("")
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<p style='color:white; font-weight:bold; font-size:17px;'>📋 Daftar Setoran:</p>", unsafe_allow_html=True)
    filter_kat = st.selectbox("Filter:", ["Semua","Iqro","Tahsin","Tahfidz"], key="filter_setoran")
    semua_setoran = get_setoran()
    if st.session_state["login_role"]=="siswa":
        daftar_setoran = [s for s in semua_setoran if s["pengirim"]==st.session_state["login_nama"]]
    else:
        daftar_setoran = semua_setoran
    if filter_kat != "Semua":
        daftar_setoran = [s for s in daftar_setoran if s["kategori"]==filter_kat]
    if not daftar_setoran:
        st.info("Belum ada setoran.")
    else:
        for s in daftar_setoran:
            st.markdown(f"<div style='background-color: rgba(255,255,255,0.12); border:1.5px solid rgba(255,255,255,0.5); padding:14px; border-radius:12px;'><p style='color:#F9D423; font-weight:bold; margin:0;'>[{html.escape(str(s['kategori']))}] {html.escape(str(s['judul']))} - {html.escape(str(s['label']))}</p><p style='color:#AAAAAA; font-size:12px;'>{html.escape(str(s['jam']))} | File: {html.escape(str(s['audio_nama']))} | {'✅ Sudah Dikoreksi' if s['koreksi'] else '⏳ Menunggu Koreksi'}</p><p style='color:white;'>{html.escape(str(s['keterangan']))}</p></div>", unsafe_allow_html=True)
            if s["foto"]:
                try: st.image(io.BytesIO(s["foto"]), caption=f"📷 Foto - {s['judul']}", use_container_width=True)
                except: st.warning("Foto tidak bisa ditampilkan.")
            if s["audio"]:
                st.markdown("<p style='color:#F9D423; font-weight:bold; margin:5px 0 2px 0;'>🔊 Dengarkan Suara Siswa (Tim pencet Play):</p>", unsafe_allow_html=True)
                st.audio(io.BytesIO(s["audio"]))
            if s["koreksi"]:
                st.markdown(f"<div style='background-color: rgba(20,50,35,0.9); border:1.5px solid #F9D423; padding:12px; border-radius:12px; margin:5px 0 12px 0;'><p style='color:#F9D423; font-weight:bold; margin:0;'>✍️ Koreksi dari {html.escape(str(s['pembalas']))} | Nilai Setoran: {html.escape(str(s['nilai']))}</p><p style='color:white;'>{html.escape(str(s['koreksi']))}</p></div>", unsafe_allow_html=True)
            if st.session_state["login_role"]=="tim":
                koreksi_txt = st.text_area(f"Tulis Koreksi untuk {s['label']} - {s['judul']}:", value=s["koreksi"], key=f"koreksi_{s['id']}", height=100, placeholder="Contoh: Makhraj huruf ح kurang jelas, ulangi... Tajwid idgham sudah bagus...")
                nilai_txt = st.text_input("Nilai Setoran (0-100, kosongkan kalau belum dinilai):", value=s["nilai"], key=f"nilai_{s['id']}", placeholder="Contoh: 85")
                ck1, ck2 = st.columns(2)
                with ck1:
                    if st.button("✅ Kirim / Update Koreksi", key=f"kirim_koreksi_{s['id']}", use_container_width=True):
                        if not koreksi_txt.strip():
                            st.warning("⚠️ Koreksinya masih kosong!")
                        else:
                            koreksi_setoran(s['id'], koreksi_txt.strip(), f"{NAMA_LENGKAP_TIM.get(st.session_state['login_nama'], st.session_state['login_nama'])} | {TIM_PENYUSUN.get(st.session_state['login_nama'],'Tim')}", nilai_txt.strip())
                            st.success("✅ Koreksi terkirim, siswa bisa langsung lihat!")
                            time.sleep(0.5); st.rerun()
                with ck2:
                    if st.button("🗑️ Hapus Setoran", key=f"hapus_setoran_{s['id']}", use_container_width=True):
                        hapus_setoran(s['id']); st.rerun()
            st.write("")
    st.write("")
    if st.button("⬅️ Tutup Setoran Suara", use_container_width=True):
        st.session_state["lihat_setoran"]=False; st.rerun()
    st.stop()

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

    st.markdown("### 🏆 Leaderboard Game QORI AI")
    leaderboard = get_leaderboard()
    if not leaderboard:
        st.info("Belum ada siswa yang bermain game.")
    else:
        rows_lb = ""
        for peringkat, data_lb in enumerate(leaderboard[:10], 1):
            medal = "🥇" if peringkat == 1 else "🥈" if peringkat == 2 else "🥉" if peringkat == 3 else str(peringkat)
            rows_lb += (
                f"<tr><td style='padding:10px;text-align:center;color:white;'>{medal}</td>"
                f"<td style='padding:10px;color:white;font-weight:bold;'>{html.escape(str(data_lb['nama']))}</td>"
                f"<td style='padding:10px;text-align:center;color:white;'>{html.escape(str(data_lb['kelas']))}</td>"
                f"<td style='padding:10px;text-align:center;color:white;'>{html.escape(str(data_lb['game']))}</td>"
                f"<td style='padding:10px;text-align:center;color:#F9D423;font-weight:bold;'>{data_lb['total']}</td>"
                f"<td style='padding:10px;text-align:center;color:white;'>{data_lb['jumlah_main']}</td></tr>"
            )
        st.markdown(
            f"<div style='background-color:rgba(0,0,0,0.75);padding:15px;border-radius:15px;overflow-x:auto;'>"
            f"<table style='width:100%;'><tr style='background-color:#F9D423;'>"
            f"<th style='padding:10px;color:#000;'>Rank</th><th style='padding:10px;color:#000;'>Nama</th>"
            f"<th style='padding:10px;color:#000;'>Kelas</th><th style='padding:10px;color:#000;'>Game</th>"
            f"<th style='padding:10px;color:#000;'>Total Skor</th><th style='padding:10px;color:#000;'>Jumlah Main</th>"
            f"</tr>{rows_lb}</table></div>", unsafe_allow_html=True
        )
    # Rekap nilai per siswa, per game, dan per level hanya dapat dilihat Tim.
    if st.session_state.get("login_role") == "tim":
        st.markdown("### 📊 Daftar Nilai Game Siswa – Level 1 sampai 6")
        st.caption("Menampilkan nilai terbaik dari setiap level yang telah diselesaikan. Tanda — berarti siswa belum menyelesaikan level tersebut. Data ini khusus Tim.")
        konfigurasi_rekap = [
            ("Game Iqro'", "Iqro", "🔤 Nilai Game Iqro'"),
            ("Game Tahsin", "Tahsin", "📖 Nilai Game Tahsin"),
            ("Game Tahfidz", "Tahfidz", "🧠 Nilai Game Tahfidz"),
        ]
        for nama_game_rekap, kategori_rekap, judul_rekap in konfigurasi_rekap:
            st.markdown(f"#### {judul_rekap}")
            rekap = get_rekap_nilai_game(nama_game_rekap)
            siswa_kategori = [n for n, d in DATA_SISWA.items() if d.get("kategori") == kategori_rekap]
            if not siswa_kategori:
                st.info("Belum ada data siswa untuk kategori ini.")
                continue
            rows_rekap = ""
            for no, nama_siswa in enumerate(siswa_kategori, 1):
                data_siswa = rekap.get(nama_siswa, {"kelas": kategori_rekap, "level": {}})
                cells = ""
                total_terbaik = 0
                for lev in range(1, 7):
                    info_level = data_siswa["level"].get(lev)
                    if info_level:
                        nilai_level = info_level["skor"]
                        total_terbaik += nilai_level
                        isi_nilai = f"{nilai_level}/250<br><small>{info_level['percobaan']}x main</small>"
                    else:
                        isi_nilai = "—"
                    cells += f"<td style='padding:8px;text-align:center;color:white;'>{isi_nilai}</td>"
                rows_rekap += (
                    f"<tr><td style='padding:8px;text-align:center;color:white;'>{no}</td>"
                    f"<td style='padding:8px;color:white;font-weight:bold;'>{html.escape(nama_siswa)}</td>"
                    f"{cells}<td style='padding:8px;text-align:center;color:#F9D423;font-weight:bold;'>{total_terbaik}</td></tr>"
                )
            st.markdown(
                "<div style='background:rgba(0,0,0,.78);padding:12px;border-radius:12px;overflow-x:auto;'>"
                "<table style='width:100%;border-collapse:collapse;min-width:850px;'>"
                "<tr style='background:#F9D423;color:#000;'><th>No</th><th>Nama Siswa</th>"
                "<th>Level 1</th><th>Level 2</th><th>Level 3</th><th>Level 4</th>"
                "<th>Level 5</th><th>Level 6</th><th>Akumulasi Nilai Terbaik</th></tr>"
                f"{rows_rekap}</table></div>", unsafe_allow_html=True
            )

    if st.session_state["login_role"] == "tim":
        if st.button("🔄 Reset Leaderboard Game (Khusus Tim)"):
            reset_leaderboard()
            st.success("Leaderboard game berhasil direset.")
            st.rerun()

    if st.session_state["login_role"] == "tim":
        st.write("")
        st.markdown("<div style='background-color: rgba(120,20,20,0.9); padding:18px; border-radius:15px; text-align:center; border:2px solid #FF5252;'><h3 style='color:#FFFFFF; margin:0;'>🔄 Reset Riwayat (Khusus Tim)</h3><p style='color:white; font-size:13px; margin:6px 0 0 0;'>Hati-hati! Riwayat yang sudah dihapus tidak bisa dikembalikan.</p></div>", unsafe_allow_html=True)
        st.write("")
        st.markdown("<p style='color:white; font-weight:bold;'>Reset 1 siswa saja:</p>", unsafe_allow_html=True)
        nama_reset_riw = st.selectbox("Pilih siswa yang riwayatnya mau dihapus:", ["-- Pilih Siswa --"] + list(DATA_SISWA.keys()), key="pilih_reset_riwayat_satu")
        if st.button("🗑️ Hapus Riwayat Siswa Ini", use_container_width=True):
            if nama_reset_riw == "-- Pilih Siswa --":
                st.warning("⚠️ Pilih dulu siswanya!")
            else:
                hapus_riwayat_satu(nama_reset_riw)
                st.success(f"✅ Riwayat {nama_reset_riw} sudah dihapus!")
                time.sleep(0.5)
                st.rerun()
        st.write("")
        st.markdown("<p style='color:white; font-weight:bold;'>Reset SEMUA riwayat jadi kosong:</p>", unsafe_allow_html=True)
        konfirmasi_riw = st.text_input("Ketik RESET untuk konfirmasi (huruf besar semua):", placeholder="Ketik RESET di sini...", key="konfirmasi_reset_riwayat")
        if st.button("🗑️ Hapus SEMUA Riwayat", use_container_width=True):
            if konfirmasi_riw.strip() != "RESET":
                st.warning("⚠️ Ketik dulu RESET dengan huruf besar semua biar tidak kepencet tidak sengaja!")
            else:
                reset_semua_riwayat()
                st.success("✅ Semua riwayat sudah dihapus! Tabel jadi kosong.")
                time.sleep(0.5)
                st.rerun()
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
    if st.session_state["login_role"] == "tim":
        st.write("")
        st.markdown("<div style='background-color: rgba(120,20,20,0.9); padding:18px; border-radius:15px; text-align:center; border:2px solid #FF5252;'><h3 style='color:#FFFFFF; margin:0;'>🔄 Reset Nilai (Khusus Tim)</h3><p style='color:white; font-size:13px; margin:6px 0 0 0;'>Hati-hati! Nilai yang sudah direset tidak bisa dikembalikan.</p></div>", unsafe_allow_html=True)
        st.write("")
        st.markdown("<p style='color:white; font-weight:bold;'>Reset 1 siswa saja:</p>", unsafe_allow_html=True)
        nama_reset = st.selectbox("Pilih siswa yang nilainya mau dihapus:", ["-- Pilih Siswa --"] + list(DATA_SISWA.keys()), key="pilih_reset_satu")
        if st.button("🗑️ Hapus Nilai Siswa Ini", use_container_width=True):
            if nama_reset == "-- Pilih Siswa --":
                st.warning("⚠️ Pilih dulu siswanya!")
            elif nama_reset not in hasil:
                st.warning(f"⚠️ {nama_reset} belum punya nilai, jadi tidak ada yang dihapus.")
            else:
                hapus_hasil_satu(nama_reset)
                st.success(f"✅ Nilai {nama_reset} sudah dihapus! Sekarang jadi Belum Mengerjakan lagi.")
                time.sleep(0.5)
                st.rerun()
        st.write("")
        st.markdown("<p style='color:white; font-weight:bold;'>Reset SEMUA siswa jadi Belum Mengerjakan:</p>", unsafe_allow_html=True)
        konfirmasi = st.text_input("Ketik RESET untuk konfirmasi (huruf besar semua):", placeholder="Ketik RESET di sini...", key="konfirmasi_reset_all")
        if st.button("🗑️ Reset SEMUA Nilai Jadi Kosong", use_container_width=True):
            if konfirmasi.strip() != "RESET":
                st.warning("⚠️ Ketik dulu RESET dengan huruf besar semua biar tidak kepencet tidak sengaja!")
            else:
                reset_semua_hasil()
                st.success("✅ Semua nilai sudah direset! Semua siswa kembali jadi Belum Mengerjakan.")
                time.sleep(0.5)
                st.rerun()
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
