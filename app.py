import streamlit as st

st.set_page_config(page_title="QORI AI - MA Al-Barokah", page_icon="📖")
st.title("📖 QORI AI - MA Al-Barokah Kelas 11")
st.write("Belajar Sesuai Kelasmu: Iqro / Tahsin / Tahfidz")

DAFTAR_SISWA = {
    "TRISCHA BUNGA LESTARI": "Tahsin",
    "ZALFATOSYIFA RAMADHANI": "Tahfidz",
    "ZAIN RAHMANITA": "Tahfidz",
    "YUSUF IMAM MA'MUN": "Tahfidz",
    "RAIHAN": "Tahsin",
    "FEBRIANSYAH RACHMAT HIDAYAT": "Tahfidz",
    "ANGGA FADILLAH": "Tahsin",
    "MUHAMMAD HAFIDZ": "Tahfidz",
    "ANDY RAMADANI ABDULLAH": "Tahsin",
    "ANGGI RATU MAHARANI": "Tahfidz",
    "RIZQI RAMADHANI": "Tahfidz",
    "KAMILATUSSYIFA RASYIDA RAHMAHUN": "Tahfidz",
    "MUTIARA JANNAH": "Tahfidz",
    "MUHAMMAD AZHAR SATRIA": "Tahfidz",
    "ROSMALATI KHOIRUNNISA": "Tahfidz",
    "M. ARIF ZAKARIYA": "Tahfidz",
    "MUHAMMAD ALKAFI I MUBAROK": "Tahfidz",
    "MAHFUD HARTANTO": "Iqro",
    "IMAM MANSYUR IBNU HILMAN": "Tahfidz",
    "DAFFA OKTAFIL HIDAYAT": "Iqro",
}

nama = st.text_input("Siapa nama kamu?", placeholder="Contoh: MAHFUD HARTANTO").strip().upper()
salam = st.text_input("Ketik salam dulu:", placeholder="Assalamualaikum")

if salam and "salam" not in salam.lower():
    st.warning("Yuk ucap salam dulu 🙏 Ketik: Assalamualaikum")
    st.stop()
if not nama:
    st.info("Isi nama kamu dulu ya!")
    st.stop()
if salam:
    st.success(f"Waalaikumsalam {nama}! Selamat belajar! 💪")

if nama in DAFTAR_SISWA:
    mode = DAFTAR_SISWA[nama]
    if mode == "Iqro":
        st.info(f"Halo {nama}, kelas kamu: **📖 IQRO**. Fokus belajar Iqro ya! Kamu belum bisa nanya Tahsin / Tahfidz.")
    elif mode == "Tahsin":
        st.info(f"Halo {nama}, kelas kamu: **✨ TAHSIN**. Fokus perbaiki bacaan Tajwid ya!")
    else:
        st.info(f"Halo {nama}, kelas kamu: **🤲 TAHFIDZ**. Fokus menghafal ya!")
else:
    mode = st.selectbox("Mau belajar apa?", ["Iqro", "Tahsin", "Tahfidz"])

pertanyaan = st.text_input("Tulis yang mau ditanya:", placeholder="Tanya sesuai kelasmu ya...")

# ===== KATA KUNCI PEMISAH =====
KATA_TAHSIN = ["nun mati", "nun sukun", "mim mati", "mad ", "mad thobi", "mad wajib", "mad jaiz", "mad lazim", "mad arid", "mad lin", "mad iwad", "mad badal", "qolqolah", "qalqalah", "ghunnah", "dengung", "tafkhim", "tarqiq", "makhroj", "makhraj", "sifat huruf", "izhar", "ikhfa", "iqlab", "idgham", "lam syamsiyah", "lam qomariyah", "waqof", "tajwid", "tahsin"]
KATA_TAHFIDZ = ["cara hafal", "cara menghafal", "metode hafal", "murojaah", "murajaah", "juz 30", "juz amma", "al-fatihah", "fatihah", "al-ikhlas", "ikhlas", "an-nas", "al-falaq", "falaq", "al-kautsar", "kautsar", "al-ashr", "an-nashr", "nashr", "al-qadr", "qadr", "setor hafalan", "jadwal hafalan", "jadwal tahfidz", "lupa", "susah hafal", "tahfidz", "hafal", "menghafal", "surah pendek"]
KATA_IQRO = ["iqro", "hijaiyah", "fathah", "kasroh", "dhommah", "harokat", "tanwin", "sukun", "tasydid"]

def jawab_iqro(t, n):
    if t == "iqro" or t == "materi iqro" or "apa itu iqro" in t:
        return f"**MATERI IQRO LENGKAP, {n}! 📖**\n\n**IQRO 1 - Kenalan Huruf:** A BA TA TSA... sampai YA tanpa harokat.\n**IQRO 2 - Fathah (A):** بَ = BA, كَتَبَ = KATABA.\n**IQRO 3 - Kasroh (I) & Dhommah (U):** بِ = BI, بُ = BU.\n**IQRO 4 - Tanwin & Sukun:** كِتَابًا = KITAABAN, مِنْ = MIN.\n**IQRO 5 - Tasydid & Mad Dasar:** إِنَّ = INNA, قَا = QOO.\n**IQRO 6 - Gabungan:** Udah mirip Al-Quran!\n\n**Ketik: Iqro 1 / Iqro 2 / Iqro 3 / Iqro 4 / Iqro 5 / Iqro 6**"
    if "iqro 1" in t:
        return f"**IQRO 1 - HURUF HIJAIYAH, {n}**\n\nا ب ت ث ج ح خ د ذ ر ز س ش ص ض ط ظ ع غ ف ق ك ل م ن و هـ ء ي\n\nDibaca: A BA TA TSA JA HA KHO DA DZA RO ZA SA SYA SHO DHO THO ZHO 'A GHO FA QO KA LA MA NA WA HA A YA\n\n**Sering ketuker:** Ba-Ta-Tsa, Jim-Ha-Kho, Sin-Syin, Shod-Dhod, Tho-Zho, Ain-Ghoin, Fa-Qof.\n\n**Latihan:** Baca 1 halaman 5x sampai hafal!"
    if "iqro 2" in t:
        return f"**IQRO 2 - FATHAH (A), {n}**\n\nFathah di atas = A. بَ = BA, تَ = TA, كَتَبَ = KA-TA-BA, دَرَسَ = DA-RO-SA\n\n**Aturan:** Fathah dibaca PENDEK 1 ketukan, jangan dipanjangin jadi BAAA!"
    if "iqro 3" in t:
        return f"**IQRO 3 - KASROH (I) & DHOMMAH (U), {n}**\n\nKasroh di bawah = I, Dhommah di atas = U.\nبَ = BA, بِ = BI, بُ = BU. كُتِبَ = KU-TI-BA\n\n**Tips:** Lihat tandanya dulu sebelum baca!"
    if "iqro 4" in t:
        return f"**IQRO 4 - TANWIN & SUKUN, {n}**\n\n**Tanwin:** AN IN UN. كِتَابًا = KITAABAN, كِتَابٍ = KITAABIN, كِتَابٌ = KITAABUN\n**Sukun:** huruf mati. مِنْ = MIN, قُلْ = QUL, لَمْ = LAM\n\n**Salah:** MIN dibaca MINA itu salah!"
    if "iqro 5" in t:
        return f"**IQRO 5 - TASYDID & MAD DASAR, {n}**\n\n**Tasydid (ّ) = ditekan:** إِنَّ = INNA, مُحَمَّدٌ = MUHAMMADUN\n**Mad = panjang 2 harakat:** قَا = QOO, فِيْ = FII, نُوْرٌ = NUURUN\n\n**Beda:** Tasydid ditekan, Mad dipanjangin!"
    if "iqro 6" in t:
        return f"**IQRO 6 - UDAH MIRIP AL-QURAN, {n}!**\n\nGabungan semua yang udah kamu pelajari: Fathah, Kasroh, Dhommah, Tanwin, Sukun, Tasydid, Mad.\n\nKalau lulus ini, kamu NAIK KELAS ke Tahsin! Semangat!"
    if "hijaiyah" in t:
        return f"**Huruf Hijaiyah 28 huruf, {n}!**\n\nا ب ت ث ج ح خ د ذ ر ز س ش ص ض ط ظ ع غ ف ق ك ل م ن و هـ ء ي\n\nDibaca: A BA TA TSA JA HA KHO DA DZA RO ZA SA SYA SHO DHO THO ZHO 'A GHO FA QO KA LA MA NA WA HA A YA\n\n**Sering ketuker:** ح vs هـ, ع vs ا, ق vs ك"
    if "fathah" in t or "harokat" in t:
        return f"**Harokat, {n}:** Fathah (َ) = A, Kasroh (ِ) = I, Dhommah (ُ) = U, Sukun (ْ) = mati, Tasydid (ّ) = dobel, Tanwin (ً ٍ ٌ) = AN IN UN\n\nContoh: بَ = BA, بِ = BI, بُ = BU"
    if "tanwin" in t:
        return f"**Tanwin, {n} (Iqro 4):** Fathatain = AN, Kasrotain = IN, Dhommatain = UN. Contoh: كِتَابًا = KITAABAN, كِتَابٌ = KITAABUN"
    if "sukun" in t:
        return f"**Sukun (ْ) = huruf mati, {n} (Iqro 4).** Dibaca pendek & jelas. Contoh: مِنْ = MIN, قُلْ = QUL"
    if "tasydid" in t:
        return f"**Tasydid (ّ) = dobel / ditekan, {n} (Iqro 5).** Contoh: إِنَّ = INNA, مُحَمَّدٌ = MUHAMMADUN"
    return f"**Semangat Iqro, {n}! 📖**\n\nKamu nanya: '{t}'\n\n**Kamu kelas IQRO, ketik ini aja:**\n- Iqro (lihat semua materi)\n- Iqro 1 / Iqro 2 / Iqro 3 / Iqro 4 / Iqro 5 / Iqro 6\n- Huruf Hijaiyah / Fathah / Tanwin / Sukun / Tasydid"

def jawab_tahsin(t, n):
    if t == "tahsin" or t == "materi tahsin" or "apa itu tahsin" in t or t == "tajwid":
        return f"**MATERI TAHSIN LENGKAP, {n}! ✨**\n\n**1. Makhroj & Sifat Huruf** - Ketik: Makhroj\n**2. Nun Mati & Tanwin (5 hukum)** - Ketik: Nun mati\n**3. Mim Mati (3 hukum)** - Ketik: Mim mati\n**4. Mad (9 macam)** - Ketik: Mad\n**5. Qolqolah** - Ketik: Qolqolah\n**6. Ghunnah** - Ketik: Ghunnah\n**7. Tafkhim & Tarqiq** - Ketik: Tafkhim\n**8. Lam Syamsiyah & Qomariyah** - Ketik: Lam Syamsiyah\n**9. Waqof & Ibtida** - Ketik: Waqof\n**10. Idgham** - Ketik: Idgham"
    if "makhroj" in t or "makhraj" in t:
        return f"**MAKHROJ, {n}.**\n\n1. Jauf - ا و ي\n2. Halq - ء هـ ع ح غ خ\n3. Lisan - ق ك ج ش ي ض ل ن ر ط د ت ص ز س ظ ذ ث\n4. Syafatain - ف ب م و\n5. Khoisyum - Ghunnah\n\n**Sering salah:** ح vs هـ, ع vs ا, ق vs ك"
    if "sifat huruf" in t or t == "sifat":
        return f"**SIFAT HURUF, {n}.**\n\n- Hams: ف ح ث هـ ش خ ص س ك ت\n- Isti'la (tebal): خ ص ض غ ط ق ظ\n- Qolqolah (mantul): ق ط ب ج د\n- Ghunnah (dengung): ن م"
    if "nun mati" in t or "nun sukun" in t:
        if "ba" in t:
            return f"**IQLAB, {n}!** Nun mati ketemu **Ba**. Jadi Mim + dengung 2 harakat.\n\nContoh: مِنْ بَعْدِ = **MIM BA'DI**, سَمِيعٌ بَصِيرٌ = **SAMII'UM BASHIIR**"
        if "ya" in t or "waw" in t or "wau" in t or "mim" in t or "nun" in t:
            return f"**IDGHAM BIGUNNAH, {n}!** Nun mati ketemu **ي ن م و**. Dilebur + dengung.\n\nContoh: مَنْ يَعْمَلْ = **MAYYA'MAL**, مِنْ نُورٍ = **MINNUUR**"
        if "lam" in t or "ra" in t or "ro" in t:
            return f"**IDGHAM BILAGUNNAH, {n}!** Nun mati ketemu **ل ر**. Dilebur TANPA dengung.\n\nContoh: مِنْ رَبِّهِمْ = **MIRROBBIHIM**"
        return f"**HUKUM NUN MATI LENGKAP, {n}:**\n\n1. Izhar (ء هـ ع ح غ خ) -> JELAS. Contoh: مِنْ أَهْلِ = MIN AHLI\n2. Idgham Bigunnah (ي ن م و) -> lebur + dengung. Contoh: MAYYA'MAL\n3. Idgham Bilagunnah (ل ر) -> lebur tanpa dengung. Contoh: MIRROBBIHIM\n4. Iqlab (ب) -> jadi MIM. Contoh: MIM BA'DI\n5. Ikhfa (15 huruf) -> SAMAR. Contoh: MINGKUM"
    if "iqlab" in t:
        return f"**IQLAB, {n}!** Nun mati ketemu Ba. Jadi Mim + dengung. Contoh: مِنْ بَعْدِ = MIM BA'DI"
    if "izhar" in t:
        return f"**IZHAR - JELAS, {n}.** Nun mati ketemu ء هـ ع ح غ خ. Contoh: مِنْ أَهْلِ = MIN AHLI, مِنْ خَيْرٍ = MIN KHOIR"
    if "ikhfa" in t and "syafawi" not in t:
        return f"**IKHFA - SAMAR, {n}.** Nun mati ketemu 15 huruf: ت ث ج د ذ ز س ش ص ض ط ظ ف ق ك. Contoh: مِنْكُمْ = MINGKUM, أَنْتُمْ = ANGTUM"
    if "mim mati" in t:
        if "ba" in t:
            return f"**IKHFA SYAFAWI, {n}!** Mim mati ketemu Ba. Samar + dengung. Contoh: هُمْ بِهِ = HUMM BIHI"
        if "mim" in t:
            return f"**IDGHAM MIMI, {n}!** Mim mati ketemu Mim. Dilebur + dengung. Contoh: لَهُمْ مَا = LAHUMMAA"
        return f"**HUKUM MIM MATI, {n}:**\n\n1. Ikhfa Syafawi (ب) -> samar + dengung. Contoh: HUMM BIHI\n2. Idgham Mimi (م) -> lebur + dengung. Contoh: LAHUMMAA\n3. Izhar Syafawi (selain ب م) -> JELAS. Contoh: 'ALAIHIM GHOIRI"
    if "mad thobi" in t or "mad asli" in t:
        return f"**MAD THOBI'I, {n}.** Panjang 2 harakat. قَا = QOO, قِيْ = QII, قُوْ = QUU. Contoh: قَالَ = QOOLA"
    if "mad wajib" in t:
        return f"**MAD WAJIB MUTTASHIL, {n}.** Mad + Hamzah 1 kata, 4-5 harakat. Contoh: جَاءَ = JAAAAA'A"
    if "mad jaiz" in t or "mad munfasil" in t:
        return f"**MAD JAIZ MUNFASHIL, {n}.** Mad + Hamzah beda kata, 2/4/5 harakat. Contoh: إِنَّا أَعْطَيْنَاكَ = INNAAAA A'THOINAAK"
    if "mad lazim" in t:
        return f"**MAD LAZIM, {n}.** Mad + Tasydid/Sukun, 6 harakat. Contoh: وَلَا الضَّالِّينَ = WALADHOOOOLLLIIN"
    if "mad arid" in t:
        return f"**MAD ARIDH LISSUKUN, {n}.** Mad + Waqof, 2/4/6 harakat. Contoh: الْعَالَمِينَ -> 'AALAMIIN"
    if "mad lin" in t:
        return f"**MAD LIN, {n}.** Waw/Ya sukun + Waqof, 2/4/6 harakat. Contoh: قُرَيْشٍ -> QUROIIISY"
    if "mad iwad" in t:
        return f"**MAD IWADH, {n}.** Tanwin Fathah diwaqofkan jadi Mad 2 harakat. Contoh: عَلِيمًا -> 'ALIIMAA"
    if "mad badal" in t:
        return f"**MAD BADAL, {n}.** Hamzah + Mad, 2 harakat. Contoh: آمَنَ = AAMANA"
    if "mad" in t:
        return f"**MAD LENGKAP, {n}:** Thobi'i (2), Wajib (4-5), Jaiz (2/4/5), Lazim (6), Aridh (2/4/6), Lin (2/4/6), Iwadh (2), Badal (2), Tamkin (2)\n\nKetik: Mad Thobi'i / Mad Wajib / Mad Lazim"
    if "qolqolah" in t or "qalqalah" in t:
        return f"**QOLQOLAH, {n}.** Hurufnya **QUTHBU JADIN** = ق ط ب ج د\n\n- Sugro (tengah): يَجْعَلُ = YAJ'AL\n- Kubro (akhir): أَحَدٌ = AHAD\n- Akbar (Tasydid diwaqofkan): الْحَقُّ = AL-HAQQ"
    if "ghunnah" in t or "dengung" in t:
        return f"**GHUNNAH = DENGUNG, {n}.** Dari hidung, 2 harakat.\n\nWajib di: Nun Tasydid (INNA), Mim Tasydid (TSUMMA), Idgham Bigunnah, Iqlab, Ikhfa."
    if "tafkhim" in t or "tarqiq" in t:
        return f"**TAFKHIM & TARQIQ, {n}.**\n\n- Tafkhim = TEBAL: خ ص ض غ ط ق ظ\n- Tarqiq = TIPIS: selain itu\n- Lam Jalalah: Tebal kalau sebelumnya Fathah/Dhommah (ROSUULULLOOH), tipis kalau Kasroh (BISMILLAAH)"
    if "lam syamsiyah" in t or "lam qomariyah" in t or "lam" in t:
        return f"**LAM TA'RIF, {n}.**\n\n- Syamsiyah (Lam HILANG): الشَّمْسُ = ASY-SYAMSU\n- Qomariyah (Lam JELAS): الْقَمَرُ = AL-QOMARU"
    if "waqof" in t or "berhenti" in t:
        return f"**WAQOF, {n}.**\n\n- م = WAJIB berhenti\n- لا = DILARANG berhenti\n- ج = BOLEH berhenti\n- صلى / قلى = lanjut lebih baik\n\nCara berhenti: huruf terakhir jadi Sukun, Tanwin Fathah jadi Mad Iwadh, Ta Marbuthoh jadi Ha."
    if "idgham" in t:
        return f"**IDGHAM = MELEBUR, {n}.**\n\nBigunnah (ي ن م و), Bilagunnah (ل ر), Mimi (م), Mutamatsilain, Mutajanisain, Mutaqaribain."
    return f"**Semangat Tahsin, {n}! ✨**\n\nKamu nanya: '{t}'\n\n**Kamu kelas TAHSIN, ketik ini aja:**\n- Tahsin (lihat semua materi)\n- Nun mati / Mim mati / Mad / Qolqolah\n- Makhroj / Ghunnah / Tafkhim / Waqof"

def jawab_tahfidz(t, n):
    if t == "tahfidz" or t == "materi tahfidz" or "apa itu tahfidz" in t:
        return f"**MATERI TAHFIDZ LENGKAP, {n}! 🤲**\n\n**1. Cara Menghafal (7 Metode)** - Ketik: Cara hafal\n**2. Murojaah (Biar Gak Lupa)** - Ketik: Murojaah\n**3. Jadwal Hafalan Harian** - Ketik: Jadwal hafalan\n**4. Juz 30 / Juz Amma (37 Surah)** - Ketik: Juz 30\n**5. Surah-surah Pendek** - Ketik nama surahnya!\n**6. Kalau Sering Lupa** - Ketik: Lupa\n**7. Cara Setor Hafalan** - Ketik: Setor hafalan\n**8. Niat & Adab** - Ketik: Adab Tahfidz"
    if "adab tahfidz" in t or "niat" in t:
        return f"**NIAT & ADAB TAHFIDZ, {n}.**\n\n**Niat:** Karena Allah, bukan karena mau dipuji.\n\n**Adab:**\n1. Wudhu dulu\n2. Duduk sopan\n3. Baca Ta'awudz dulu\n4. Jangan sambil main HP\n5. Doa: 'Allahumma yassir, Ya Allah mudahkan'"
    if "cara hafal" in t or "cara menghafal" in t or "metode hafal" in t or "tips hafal" in t or "cara cepat hafal" in t:
        return f"**7 CARA MENGHAFAL AL-QURAN, {n}.**\n\n**1. METODE 3-3-3 (Paling Ampuh)**\nBaca 3x sambil lihat, tutup baca 3x tanpa lihat, ulangi di 3 waktu: pagi, siang, malam.\n\n**2. METODE 1 AYAT 1 HARI**\n1 hari 1 ayat tapi nempel, lebih baik dari 1 halaman tapi besok lupa!\n\n**3. METODE POTONG AYAT**\nAyat panjang dipotong jadi 3 bagian. Hafal potong 1, baru potong 2, baru sambung semua.\n\n**4. METODE TULIS**\nTulis ayatnya 3x sambil dibaca keras-keras. Tangan + mulut + mata = 3x nempel!\n\n**5. METODE DENGAR**\nDengerin murottal 1 ayat diulang 10x, sambil ikutin.\n\n**6. METODE SAMBUNG**\nHafal ayat 1, hafal ayat 2, sambung 1+2, hafal ayat 3, sambung 1+2+3.\n\n**7. METODE TEMAN**\nSetor berdua. Kamu setor ke dia, dia setor ke kamu.\n\n**Ketik: Murojaah buat cara biar gak lupa!**"
    if "murojaah" in t or "murajaah" in t:
        return f"**MUROJAAH - BIAR GAK LUPA, {n}!**\n\n**Jadwal Harian:**\n- Pagi (Subuh): Hafalan BARU\n- Siang (Dzuhur): Ulangi hafalan pagi 3x\n- Sore (Ashar): Ulangi hafalan kemarin\n- Malam: Ulangi SEMUA hafalan hari ini + kemarin\n\n**Jadwal Mingguan:**\n- Senin-Jumat: Hafalan baru + murojaah\n- Sabtu: Murojaah seminggu (tidak nambah baru)\n- Ahad: Murojaah sebulan / setor ke Ustadz\n\n**3 Jenis:** Murojaah Dekat (hari ini), Murojaah Jauh (lama), Murojaah Sholat (baca hafalan di sholat - paling nempel!)"
    if "jadwal hafalan" in t or "jadwal tahfidz" in t or "jadwal" in t:
        return f"**JADWAL HAFALAN HARIAN, {n}.**\n\n- 04.30: Bangun, Subuh, hafalan baru 1-3 ayat (15 menit aja!)\n- 12.30: Setelah Dzuhur, ulang hafalan pagi 3x\n- 20.00: Setelah Isya, murojaah + setor ke orang tua / teman\n- Sabtu: Murojaah seminggu\n- Ahad: Libur hafalan baru, murojaah santai\n\n**Target:** Pemula 1 ayat/hari, Menengah 3 ayat/hari, Mahir 1 halaman/hari"
    if "lupa" in t or "susah hafal" in t or "sulit hafal" in t:
        return f"**KALAU SERING LUPA, {n}. Jangan nyerah!**\n\n**Penyebab 90% lupa:** Kurang murojaah, bukan karena bodoh!\n\n**Solusi:**\n- Kurangi target: 1 ayat aja per hari\n- Jauhin HP pas menghafal (15 menit aja!)\n- Murojaah di sholat\n- Tidur cukup\n\nSemua penghafal Quran pernah lupa. Bedanya, yang sukses itu yang MAU ngulang lagi!"
    if "setor hafalan" in t or "setoran" in t or "cara setor" in t:
        return f"**CARA SETOR HAFALAN, {n}.**\n\n**Sebelum setor:** Murojaah dulu 3x sendiri.\n**Pas setor:** Baca Ta'awudz + Basmalah, suara jelas, jangan terlalu cepat. Kalau lupa, bilang: 'Maaf Ustadz, boleh diingatkan?'\n**Setelah setor:** Catat yang salah, ulang lagi 5x. Jangan nambah baru kalau masih banyak salah."
    if "juz 30" in t or "juz amma" in t or "surah pendek" in t or "daftar surah" in t:
        return f"**JUZ 30 / JUZ AMMA - 37 SURAH, {n}.**\n\n**LEVEL 1 - PALING GAMPANG:**\nAl-Kautsar, Al-Ashr, An-Nashr, Al-Ikhlas, Al-Falaq, An-Nas, Al-Masad, Al-Fil\n\n**LEVEL 2 - MUDAH:**\nAl-Fatihah, Al-Qadr, Az-Zalzalah, Al-Adiyat, Al-Qori'ah, At-Takatsur, Al-Humazah, Quraisy\n\n**LEVEL 3 - MENENGAH:**\nAl-Bayyinah, Al-Lail, Asy-Syams, Adh-Dhuha, Asy-Syarh, At-Tin, Al-'Alaq, Al-Ghosyiyah\n\n**LEVEL 4 - PANJANG:**\nAl-Fajr, Al-Balad, Al-Infithor, Al-Muthaffifin, At-Takwir, Abasa, An-Nazi'at, An-Naba\n\n**Mulai dari Level 1 dulu biar semangat! Ketik nama surahnya!**"
    if "al-fatihah" in t or "fatihah" in t:
        return f"**Surah Al-Fatihah (7 ayat), {n}.**\n\n1. بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ\n2. الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ\n3. الرَّحْمَٰنِ الرَّحِيمِ\n4. مَالِكِ يَوْمِ الدِّينِ\n5. إِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ\n6. اهْدِنَا الصِّرَاطَ الْمُسْتَقِيمَ\n7. صِرَاطَ الَّذِينَ أَنْعَمْتَ عَلَيْهِمْ غَيْرِ الْمَغْضُوبِ عَلَيْهِمْ وَلَا الضَّالِّينَ\n\n**Cara hafal:** Potong jadi 3 bagian. Ayat 1-2 dulu, baru 3-4, baru 5-7!"
    if "al-ikhlas" in t or "ikhlas" in t:
        return f"**Surah Al-Ikhlas (4 ayat), {n}.**\n\n1. قُلْ هُوَ اللَّهُ أَحَدٌ\n2. اللَّهُ الصَّمَدُ\n3. لَمْ يَلِدْ وَلَمْ يُولَدْ\n4. وَلَمْ يَكُنْ لَهُ كُفُوًا أَحَدٌ\n\n**Pahalanya sama kayak sepertiga Al-Quran!**"
    if "an-nas" in t or "an nas" in t:
        return f"**Surah An-Nas (6 ayat), {n}.**\n\nقُلْ أَعُوذُ بِرَبِّ النَّاسِ - مَلِكِ النَّاسِ - إِلَٰهِ النَّاسِ - مِنْ شَرِّ الْوَسْوَاسِ الْخَنَّاسِ - الَّذِي يُوَسْوِسُ فِي صُدُورِ النَّاسِ - مِنَ الْجِنَّةِ وَالنَّاسِ"
    if "al-falaq" in t or "falaq" in t:
        return f"**Surah Al-Falaq (5 ayat), {n}.**\n\nقُلْ أَعُوذُ بِرَبِّ الْفَلَقِ - مِنْ شَرِّ مَا خَلَقَ - وَمِنْ شَرِّ غَاسِقٍ إِذَا وَقَبَ - وَمِنْ شَرِّ النَّفَّاثَاتِ فِي الْعُقَدِ - وَمِنْ شَرِّ حَاسِدٍ إِذَا حَسَدَ"
    if "al-kautsar" in t or "kautsar" in t:
        return f"**Surah Al-Kautsar (3 ayat), {n}.**\n\n1. إِنَّا أَعْطَيْنَاكَ الْكَوْثَرَ\n2. فَصَلِّ لِرَبِّكَ وَانْحَرْ\n3. إِنَّ شَانِئَكَ هُوَ الْأَبْتَرُ"
    if "al-ashr" in t or "ashr" in t:
        return f"**Surah Al-Ashr (3 ayat), {n}.**\n\n1. وَالْعَصْرِ\n2. إِنَّ الْإِنْسَانَ لَفِي خُسْرٍ\n3. إِلَّا الَّذِينَ آمَنُوا وَعَمِلُوا الصَّالِحَاتِ وَتَوَاصَوْا بِالْحَقِّ وَتَوَاصَوْا بِالصَّبْرِ"
    if "an-nashr" in t or "nashr" in t:
        return f"**Surah An-Nashr (3 ayat), {n}.**\n\n1. إِذَا جَاءَ نَصْرُ اللَّهِ وَالْفَتْحُ\n2. وَرَأَيْتَ النَّاسَ يَدْخُلُونَ فِي دِينِ اللَّهِ أَفْوَاجًا\n3. فَسَبِّحْ بِحَمْدِ رَبِّكَ وَاسْتَغْفِرْهُ ۚ إِنَّهُ كَانَ تَوَّابًا"
    if "al-qadr" in t or "qadr" in t:
        return f"**Surah Al-Qadr (5 ayat), {n}.**\n\n1. إِنَّا أَنْزَلْنَاهُ فِي لَيْلَةِ الْقَدْرِ\n2. وَمَا أَدْرَاكَ مَا لَيْلَةُ الْقَدْرِ\n3. لَيْلَةُ الْقَدْرِ خَيْرٌ مِنْ أَلْفِ شَهْرٍ\n4. تَنَزَّلُ الْمَلَائِكَةُ وَالرُّوحُ فِيهَا بِإِذْنِ رَبِّهِمْ مِنْ كُلِّ أَمْرٍ\n5. سَلَامٌ هِيَ حَتَّىٰ مَطْلَعِ الْفَجْرِ"
    return f"**Semangat Tahfidz, {n}! 🤲**\n\nKamu nanya: '{t}'\n\n**Kamu kelas TAHFIDZ, ketik ini aja:**\n- Tahfidz (lihat semua materi)\n- Cara hafal / Murojaah / Jadwal hafalan\n- Juz 30 / Al-Fatihah / Al-Ikhlas / An-Nas"

def jawab_qori(tanya, mode):
    t = tanya.lower().strip()
    n = nama
    # ===== PEMISAH TOTAL =====
    if mode == "Iqro":
        # Kalau nanya Tahsin / Tahfidz, tolak!
        if any(k in t for k in KATA_TAHSIN if k not in ["tanwin", "sukun", "tasydid", "mad "]):
            return f"⛔ **Maaf {n}, kamu kelas IQRO!**\n\nKamu nanya: '{tanya}' itu materi **TAHSIN**.\n\nKamu belum boleh belajar Tahsin dulu. Fokus Iqro dulu sampai lulus Iqro 6, baru naik ke Tahsin ya!\n\n**Ketik yang boleh buat kamu:**\n- Iqro / Iqro 1 / Iqro 2 / Iqro 3 / Iqro 4 / Iqro 5 / Iqro 6\n- Huruf Hijaiyah / Fathah / Tanwin / Sukun / Tasydid"
        if any(k in t for k in KATA_TAHFIDZ if k not in ["hafal"]):
            return f"⛔ **Maaf {n}, kamu kelas IQRO!**\n\nKamu nanya: '{tanya}' itu materi **TAHFIDZ**.\n\nKamu belum boleh menghafal dulu. Fokus Iqro dulu sampai bisa baca dengan lancar, baru naik ke Tahsin & Tahfidz ya!\n\n**Ketik yang boleh buat kamu:** Iqro / Iqro 1 / Iqro 2 / Iqro 3 / Iqro 4 / Iqro 5 / Iqro 6"
        return jawab_iqro(t, n)
    if mode == "Tahsin":
        if any(k in t for k in KATA_IQRO):
            # Iqro 1-6 masih boleh dibahas sedikit sebagai pengingat, tapi arahkan ke Tahsin
            if "iqro" in t and t not in ["iqro", "iqro 1", "iqro 2", "iqro 3", "iqro 4", "iqro 5", "iqro 6"]:
                pass
            if t in ["iqro", "iqro 1", "iqro 2", "iqro 3", "iqro 4", "iqro 5", "iqro 6", "hijaiyah", "fathah"]:
                return f"⛔ **Maaf {n}, kamu kelas TAHSIN!**\n\nKamu udah lulus Iqro, sekarang fokus **TAHSIN** ya! Jangan balik ke Iqro lagi.\n\n**Kamu nanya:** '{tanya}' itu materi Iqro.\n\n**Ketik yang boleh buat kamu:**\n- Tahsin (lihat semua materi Tahsin)\n- Nun mati / Mim mati / Mad / Qolqolah / Makhroj / Waqof"
        if any(k in t for k in KATA_TAHFIDZ):
            return f"⛔ **Maaf {n}, kamu kelas TAHSIN!**\n\nKamu nanya: '{tanya}' itu materi **TAHFIDZ**.\n\nKamu fokus perbaiki bacaan dulu (Tahsin). Kalau bacaanmu udah bagus, baru kamu boleh naik ke Tahfidz ya! Kalau hafal tapi bacaannya masih salah, hafalannya jadi salah juga.\n\n**Ketik yang boleh buat kamu:**\n- Tahsin (lihat semua materi)\n- Nun mati / Mim mati / Mad / Qolqolah / Makhroj / Waqof"
        return jawab_tahsin(t, n)
    if mode == "Tahfidz":
        if any(k in t for k in KATA_IQRO):
            return f"⛔ **Maaf {n}, kamu kelas TAHFIDZ!**\n\nKamu nanya: '{tanya}' itu materi **IQRO**.\n\nKamu udah lulus Iqro & Tahsin, sekarang fokus **MENGHAFAL** aja ya! Jangan balik ke Iqro lagi.\n\n**Ketik yang boleh buat kamu:**\n- Tahfidz (lihat semua materi)\n- Cara hafal / Murojaah / Juz 30 / Al-Fatihah"
        if any(k in t for k in KATA_TAHSIN):
            return f"⛔ **Maaf {n}, kamu kelas TAHFIDZ!**\n\nKamu nanya: '{tanya}' itu materi **TAHSIN**.\n\nKamu fokus **MENGHAFAL** aja ya! Tajwid-mu udah bagus, tinggal hafalin & murojaah terus.\n\n**Kalau bacaannya ada yang ragu pas menghafal, tanya ke Ustadz langsung ya, jangan di sini.**\n\n**Ketik yang boleh buat kamu:**\n- Tahfidz (lihat semua materi)\n- Cara hafal / Murojaah / Juz 30 / Al-Fatihah"
        return jawab_tahfidz(t, n)
    return f"Semangat {n}! Ketik sesuai kelasmu ya!"

if st.button("Tanya Qori AI"):
    if not pertanyaan:
        st.warning("Tulis dulu pertanyaannya ya!")
    else:
        st.info(jawab_qori(pertanyaan, mode))
st.write("---")
st.write("Semoga bermanfaat. Wassalamualaikum warahmatullahi wabarakatuh")
