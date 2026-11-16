import streamlit as st

st.set_page_config(page_title="QORI AI - MA Al-Barokah", page_icon="📖")
st.title("📖 QORI AI - MA Al-Barokah Kelas 11")
st.write("Asisten Pengajian Digital: Iqro, Tahsin, Tahfidz")

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
    "MAHFUD HARTANTO": "Iqro Dasar",
    "IMAM MANSYUR IBNU HILMAN": "Tahfidz",
    "DAFFA OKTAFIL HIDAYAT": "Iqro",
}

nama = st.text_input("Siapa nama kamu?", placeholder="Contoh: RAIHAN").strip().upper()
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
    st.info(f"Halo {nama}, mode kamu: **{mode}**")
else:
    mode = st.selectbox("Mau belajar apa?", ["Iqro", "Tahsin", "Tahfidz"])

pertanyaan = st.text_input("Tulis yang mau ditanya / dikoreksi:", placeholder="Contoh: Apa itu mad thobi'i? / Nun mati ketemu ba / Cara hafal Al-Fatihah")

def jawab_qori(tanya, mode):
    t = tanya.lower().strip()
    n = nama

    # ============ IQRO ============
    if "hijaiyah" in t or "huruf hijaiyah" in t:
        return f"**Huruf Hijaiyah ada 28 huruf, {n}!**\n\nا ب ت ث ج ح خ د ذ ر ز س ش ص ض ط ظ ع غ ف ق ك ل م ن و هـ ء ي\n\n**Yang sering ketuker:**\n- ح (Ha pedas, tenggorokan) beda sama هـ (Ha biasa)\n- ع (Ain, tenggorokan) beda sama ا (Alif)\n- ق (Qof, pangkal lidah) beda sama ك (Kaf)\n- س (Sin) beda sama ص (Shod, tebal)\n- ت (Ta) beda sama ط (Tho, tebal)\n\n**Latihan:** Sebutin 3x dari Alif sampai Ya pelan-pelan!"
    if "iqro 1" in t or "iqro satu" in t or "iqro jilid 1" in t:
        return f"**Iqro 1 itu dasar banget, {n}.**\n\nIsinya: Kenalan huruf Hijaiyah dari Alif sampai Ya, tanpa harokat, dibaca **A BA TA TSA...**\n\n**Target:** Kamu harus hafal bentuk & nama hurufnya, jangan sampai ketuker Ba sama Ta, Jim sama Kha.\n\n**Tips:** Baca 1 halaman 5x, kalau udah lancar baru lanjut!"
    if "iqro 2" in t or "iqro dua" in t:
        return f"**Iqro 2 = Harokat Fathah, {n}.**\n\nFathah itu garis miring di atas huruf, dibaca **A**.\n\nContoh: بَ = BA, تَ = TA, كَ = KA\n\nGabung: كَتَبَ = KA-TA-BA, دَرَسَ = DA-RO-SA\n\n**Hati-hati:** Jangan dibaca panjang! Fathah cuma 1 ketukan, bukan 2."
    if "iqro 3" in t or "iqro tiga" in t:
        return f"**Iqro 3 = Kasroh & Dhommah, {n}.**\n\n- Kasroh (di bawah) dibaca **I**: بِ = BI, مِ = MI\n- Dhommah (waw kecil di atas) dibaca **U**: بُ = BU, مُ = MU\n\nGabung: كُتِبَ = KU-TI-BA\n\n**Latihan:** Bedain BA - BI - BU, jangan sampai kebalik!"
    if "iqro 4" in t or "iqro empat" in t:
        return f"**Iqro 4 = Tanwin & Sukun, {n}.**\n\n- Tanwin: Fathatain (ً) = AN, Kasrotain (ٍ) = IN, Dhommatain (ٌ) = UN. Contoh: كِتَابًا = KITAABAN\n- Sukun (ْ) = huruf mati, dibaca pendek & jelas. Contoh: مِنْ = MIN, قُلْ = QUL\n\nIni yang paling sering salah, pelan-pelan aja!"
    if "iqro 5" in t or "iqro lima" in t:
        return f"**Iqro 5 = Tasydid & Mad, {n}.**\n\n- Tasydid (ّ) = huruf dobel / ditekan. Contoh: إِنَّ = INNA (Nun-nya ditekan + dengung)\n- Mad Thobi'i = dibaca panjang 2 harakat. Contoh: قَا = QOO, فِيْ = FII\n\n**Kunci:** Tasydid itu ditekan, Mad itu dipanjangin. Beda ya!"
    if "iqro 6" in t or "iqro enam" in t:
        return f"**Iqro 6 = Udah mirip Al-Quran, {n}!**\n\nIsinya: Gabungan semua hukum: Ikhfa, Idgham, Iqlab, Qolqolah, Mad panjang, Waqof.\n\nKalau udah lulus Iqro 6, kamu udah SIAP baca Al-Quran langsung. Tinggal perbaiki Tahsin-nya!"
    if "fathah" in t or "harokat" in t:
        return f"**Harokat itu tanda baca, {n}.**\n\n- Fathah ( َ ) = A\n- Kasroh ( ِ ) = I\n- Dhommah ( ُ ) = U\n- Sukun ( ْ ) = mati\n- Tasydid ( ّ ) = dobel / ditekan\n- Tanwin ( ً ٍ ٌ ) = AN IN UN\n\nContoh: بَ = BA, بِ = BI, بُ = BU, بْ = B (mati), بَّ = BBA"
    if "tanwin" in t:
        return f"**Tanwin itu Nun mati yang tersembunyi, {n}.**\n\n- Fathatain (ً) = AN : كِتَابًا = KITAABAN\n- Kasrotain (ٍ) = IN : كِتَابٍ = KITAABIN\n- Dhommatain (ٌ) = UN : كِتَابٌ = KITAABUN\n\nTanwin juga ikut hukum Nun Mati! Kalau ketemu Ba jadi Iqlab, ketemu Ya jadi Idgham, dll."
    if "sukun" in t or "huruf mati" in t:
        return f"**Sukun (ْ) artinya huruf mati / tidak berharokat, {n}.**\n\nCara bacanya: dibaca pendek, jelas, tidak dipanjangin.\n\nContoh: مِنْ = MIN, لَمْ = LAM, قُلْ = QUL\n\n**Kesalahan umum:** Sukun dibaca jadi berharokat, contoh MIN dibaca MINA. Itu salah ya!"
    if "tasydid" in t or "syaddah" in t:
        return f"**Tasydid (ّ) artinya huruf dobel, {n}.**\n\nCara bacanya: ditekan + ditahan sebentar.\n\nContoh:\n- إِنَّ = INNA (bukan INA)\n- مُحَمَّدٌ = MUHAMMADUN\n- إِيَّاكَ = IYYAAKA\n\nKalau ada Tasydid + Nun / Mim, wajib dengung 2 harakat. Itu namanya Ghunnah Musyaddadah."

    # ============ TAHSIN - NUN MATI ============
    if ("nun mati" in t or "nun sukun" in t or "tanwin" in t) and "ba" in t or "iqlab" in t:
        return f"**Ini IQLAB, {n}!**\n\nNun mati / tanwin ketemu huruf **Ba (ب)**.\n\n**Cara bacanya:** Nun berubah jadi bunyi **Mim**, dengung 2 harakat, bibir agak merapat.\n\n**Contoh:**\n- مِنْ بَعْدِ = **MIM BA'DI**\n- سَمِيعٌ بَصِيرٌ = **SAMII'UM BASHIIR**\n\nCoba ulangi 3x: MIM BA'DI!"
    if "nun mati" in t and ("ya" in t or "waw" in t or "wau" in t or "mim" in t or "nun" in t):
        return f"**Ini IDGHAM BIGUNNAH, {n}!**\n\nNun mati ketemu **Ya, Nun, Mim, Waw (ي ن م و) - disingkat YANMU**.\n\n**Cara bacanya:** Nun dilebur ke huruf depannya, dengung 2 harakat.\n\n**Contoh:**\n- مَنْ يَعْمَلْ = **MAYYA'MAL**\n- مِنْ نُورٍ = **MINNUUR**\n- مِنْ مَالٍ = **MIMMAAL**\n- مِنْ وَالٍ = **MIWWAAL**"
    if "nun mati" in t and ("lam" in t or "ra" in t or "ro" in t):
        return f"**Ini IDGHAM BILAGUNNAH, {n}!**\n\nNun mati ketemu **Lam (ل) atau Ra (ر)**.\n\n**Cara bacanya:** Nun hilang, langsung masuk ke Lam/Ra, **TANPA dengung**.\n\n**Contoh:**\n- مِنْ رَبِّهِمْ = **MIRROBBIHIM**\n- مِنْ لَدُنْهُ = **MILLADUNHU**"
    if "izhar" in t:
        return f"**IZHAR itu dibaca JELAS, {n}.**\n\nNun mati ketemu 6 huruf Izhar: **Hamzah, Ha, Ain, Ha, Ghoin, Kha (ء هـ ع ح غ خ)**\n\n**Cara bacanya:** Nun dibaca jelas, TIDAK dengung, TIDAK samar.\n\n**Contoh:**\n- مِنْ أَهْلِ = **MIN AHLI** (jelas)\n- مِنْ خَيْرٍ = **MIN KHOIR**"
    if "ikhfa" in t and "syafawi" not in t:
        return f"**IKHFA itu dibaca SAMAR, {n}.**\n\nNun mati ketemu 15 huruf Ikhfa: Ta, Tsa, Jim, Dal, Dzal, Zai, Sin, Syin, Shod, Dhod, Tho, Zho, Fa, Qof, Kaf.\n\n**Cara bacanya:** Antara jelas dan dengung, samar + dengung 2 harakat.\n\n**Contoh:**\n- مِنْكُمْ = **MINGKUM**\n- أَنْتُمْ = **ANGTUM**\n- مِنْ شَرِّ = **MINGSYARRI**"
    if "nun mati" in t:
        return f"**Hukum Nun Mati ada 4, {n}. Ingat ini:**\n\n1. **Izhar** - ketemu ء هـ ع ح غ خ -> dibaca JELAS\n2. **Idgham Bigunnah** - ketemu ي ن م و -> dilebur + DENGUNG\n3. **Idgham Bilagunnah** - ketemu ل ر -> dilebur TANPA dengung\n4. **Iqlab** - ketemu ب -> berubah jadi MIM + dengung\n5. **Ikhfa** - ketemu 15 huruf sisanya -> SAMAR + dengung\n\nKamu tadi nanya ketemu huruf apa? Ketik lengkap, contoh: 'Nun mati ketemu kaf'"

    # ============ MIM MATI ============
    if "mim mati" in t and "ba" in t or "ikhfa syafawi" in t:
        return f"**Ini IKHFA SYAFAWI, {n}!**\n\nMim mati ketemu **Ba (ب)**.\n\n**Cara bacanya:** Samar + dengung 2 harakat, bibir tidak rapat penuh.\n\n**Contoh:** هُمْ بِهِ = **HUMM BIHI**, تَرْمِيهِمْ بِحِجَارَةٍ = **TARMIHIM BIHIJAAROH**"
    if "mim mati" in t and "mim" in t or "idgham mislain" in t or "idgham mimi" in t:
        return f"**Ini IDGHAM MISLAIN / IDGHAM MIMI, {n}!**\n\nMim mati ketemu **Mim (م)**.\n\n**Cara bacanya:** Mim pertama dilebur, dengung 2 harakat.\n\n**Contoh:** لَهُمْ مَا = **LAHUMMAA**"
    if "mim mati" in t:
        return f"**Hukum Mim Mati ada 3, {n}:**\n\n1. **Ikhfa Syafawi** - ketemu Ba -> samar + dengung\n2. **Idgham Mimi** - ketemu Mim -> dilebur + dengung\n3. **Izhar Syafawi** - ketemu huruf selain Ba & Mim -> dibaca JELAS\n\nContoh Izhar Syafawi: عَلَيْهِمْ غَيْرِ = **'ALAIHIM GHOIRI** (Mim jelas)"
    if "izhar syafawi" in t:
        return f"**IZHAR SYAFAWI, {n}:** Mim mati ketemu huruf selain Ba & Mim, dibaca JELAS.\n\nContoh: لَهُمْ قُلُوبٌ = **LAHUM QULUUB**"

    # ============ MAD ============
    if "mad thobi" in t or "mad asli" in t or "mad tobii" in t:
        return f"**MAD THOBI'I / MAD ASLI, {n}.**\n\nMad paling dasar, dibaca panjang **2 harakat**.\n\n**Rumusnya:**\n- Fathah + Alif = AA : قَا = QOO\n- Kasroh + Ya sukun = II : قِيْ = QII\n- Dhommah + Waw sukun = UU : قُوْ = QUU\n\nContoh: قَالَ = **QOOLA**, فِيْ = **FII**"
    if "mad wajib" in t:
        return f"**MAD WAJIB MUTTASHIL, {n}.**\n\nMad Thobi'i ketemu Hamzah dalam **1 kata**, dibaca panjang **4-5 harakat**.\n\n**Contoh:** جَاءَ = **JAAAAA'A**, السَّمَاءِ = **ASSAMAAAAA'I**"
    if "mad jaiz" in t or "mad munfasil" in t:
        return f"**MAD JAIZ MUNFASHIL, {n}.**\n\nMad Thobi'i ketemu Hamzah tapi **beda kata**, dibaca panjang **2, 4, atau 5 harakat**.\n\n**Contoh:** إِنَّا أَعْطَيْنَاكَ = **INNAAAA A'THOINAAK**"
    if "mad lazim" in t:
        return f"**MAD LAZIM, {n}.**\n\nMad ketemu Sukun asli / Tasydid, dibaca panjang **6 harakat**. Paling panjang!\n\n**Contoh:** وَلَا الضَّالِّينَ = **WALADHOOOOLLLIIN** (Lam Tasydid, 6 harakat)"
    if "mad arid" in t or "mad aridh" in t:
        return f"**MAD ARIDH LISSUKUN, {n}.**\n\nMad ketemu huruf yang disukun karena Waqof (berhenti), dibaca **2, 4, atau 6 harakat**.\n\n**Contoh:** Kalau berhenti di الْعَالَمِينَ dibaca **'AALAMIIN** (bisa 2, 4, atau 6, pilih yang konsisten)"
    if "mad" in t:
        return f"**MAD itu artinya PANJANG, {n}.**\n\nMacam-macam Mad:\n1. **Mad Thobi'i** - 2 harakat (dasar)\n2. **Mad Wajib Muttashil** - 4-5 harakat (Mad + Hamzah 1 kata)\n3. **Mad Jaiz Munfashil** - 2/4/5 harakat (Mad + Hamzah beda kata)\n4. **Mad Lazim** - 6 harakat (Mad + Tasydid / Sukun)\n5. **Mad Aridh Lissukun** - 2/4/6 harakat (Mad + Waqof)\n6. **Mad Lin** - 2/4/6 (Waw/Ya sukun + Waqof)\n\nKamu mau nanya Mad yang mana? Ketik: 'Mad Thobi'i' atau 'Mad Wajib'"

    # ============ LAINNYA TAHSIN ============
    if "qolqolah" in t or "qalqalah" in t:
        return f"**QOLQOLAH itu huruf yang MEMANTUL, {n}.**\n\nHurufnya 5, dihafal **QUTHBU JADIN (قطب جد)** = Qof, Tho, Ba, Jim, Dal.\n\n**2 Jenis:**\n- **Qolqolah Sugro** (di tengah): يَجْعَلُ = **YAJ'AL** (Jim mantul kecil)\n- **Qolqolah Kubro** (di akhir / waqof): أَحَدٌ = **AHAD** (Dal mantul besar)\n\n**Kesalahan umum:** Mantulnya jadi ditambah huruf E, contoh AHAD dibaca AHADE. Itu salah!"
    if "ghunnah" in t or "dengung" in t:
        return f"**GHUNNAH itu DENGUNG, {n}.**\n\nKeluar dari hidung, ditahan **2 harakat**.\n\n**Wajib dengung di:**\n- Nun Tasydid: إِنَّ = **INNA**\n- Mim Tasydid: ثُمَّ = **TSUMMA**\n- Idgham Bigunnah, Iqlab, Ikhfa\n\n**Tips:** Pencet hidung pas baca, kalau getar berarti udah bener dengungnya!"
    if "tafkhim" in t or "tarqiq" in t or "huruf tebal" in t or "lam jalalah" in t or "allah" in t:
        return f"**TAFKHIM & TARQIQ, {n}.**\n\n- **Tafkhim** = dibaca TEBAL. Hurufnya: خ ص ض غ ط ق ظ (KHOSHODHOGHTHOQODZHO)\n- **Tarqiq** = dibaca TIPIS. Selain huruf tebal.\n\n**Lam Jalalah (lafadz Allah):**\n- Tebal kalau sebelumnya Fathah/Dhommah: رَسُولُ اللهِ = **ROSUULULLOOH**\n- Tipis kalau sebelumnya Kasroh: بِسْمِ اللهِ = **BISMILLAAH**\n\n**Ra:** Tebal kalau Fathah/Dhommah (رَبِّ = **ROBBI**), tipis kalau Kasroh (رِزْقٍ = **RIZQ**)"
    if "waqof" in t or "waqf" in t or "berhenti" in t:
        return f"**WAQOF itu BERHENTI, {n}.**\n\nTandanya:\n- م (Mim kecil) = WAJIB berhenti\n- لا = DILARANG berhenti\n- ج = BOLEH berhenti / lanjut, berhenti lebih baik\n- صلى / قلى = Boleh berhenti, lanjut lebih baik\n- ∴ ∴ (3 titik) = Berhenti di salah satu aja\n\n**Aturan:** Kalau berhenti, huruf terakhir jadi Sukun. Contoh: الْمُفْلِحُونَ kalau waqof dibaca **AL-MUFLIHUUN** (Nun-nya jadi sukun)."
    if "makhroj" in t or "makhraj" in t:
        return f"**MAKHROJ itu TEMPAT KELUAR HURUF, {n}.**\n\n5 Tempat utama:\n1. **Jauf (rongga mulut)** - huruf Mad: ا و ي\n2. **Halq (tenggorokan)** - ء هـ ع ح غ خ\n3. **Lisan (lidah)** - ق ك ج ش ي ض ل ن ر ط د ت ص ز س ظ ذ ث\n4. **Syafatain (bibir)** - ف ب م و\n5. **Khoisyum (hidung)** - Ghunnah / dengung\n\n**Yang paling sering salah:** ح vs هـ, ع vs ا, ق vs ك. Latihan di depan kaca ya!"
    if "tahsin" in t:
        return f"**TAHSIN itu MEMPERBAGUS BACAAN, {n}.**\n\nBukan cuma bener hurufnya, tapi juga:\n1. Makhroj-nya pas\n2. Hukum Tajwid-nya bener (Nun Mati, Mim Mati, Mad, Qolqolah)\n3. Panjang pendeknya pas\n4. Waqof-nya bener\n\n**Coba ketik yang mau kamu perbaiki, contoh:**\n- Nun mati ketemu ba\n- Mad Thobi'i\n- Qolqolah\n- Makhroj"

    # ============ TAHFIDZ ============
    if "cara hafal" in t or "cara menghafal" in t or "metode hafal" in t or "tips hafal" in t:
        return f"**Cara Menghafal yang Paling Nempel, {n}: Metode 3-3-3**\n\n1. **Baca 3x sambil lihat** - baca ayatnya 3x, pahami artinya\n2. **Tutup, baca 3x tanpa lihat** - kalau salah, lihat lagi 1x, tutup lagi\n3. **Ulangi 3x di waktu beda** - pagi, siang, malam sebelum tidur\n\n**Rahasia penghafal Quran:**\n- Jangan pindah ayat sebelum ayat ini bener-bener lancar\n- 1 hari 1 ayat tapi nempel, lebih baik dari 1 halaman tapi lupa besok\n- Murojaah itu WAJIB, hafalan tanpa murojaah = hilang!"
    if "murojaah" in t or "murajaah" in t or "lupa" in t:
        return f"**Murojaah itu MENGULANG HAFALAN, {n}.**\n\n**Jadwal yang bagus:**\n- **Pagi:** Hafalan baru (otak masih fresh)\n- **Siang:** Ulangi hafalan pagi\n- **Malam sebelum tidur:** Ulangi semua hafalan hari ini + kemarin\n- **Jumat:** Murojaah semua hafalan seminggu\n\n**Kalau sering lupa:** Berarti murojaahnya kurang. Bukan karena kamu bodoh! Semua penghafal Quran juga sering lupa, makanya mereka murojaah terus.\n\n**Tips:** Setor ke temen / ke Ustadz, biar ada yang ngingetin kalau salah."
    if "al-fatihah" in t or "al fatihah" in t or "fatihah" in t:
        return f"**Surah Al-Fatihah (7 ayat), {n}. Wajib hafal!**\n\n1. بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ\n2. الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ\n3. الرَّحْمَٰنِ الرَّحِيمِ\n4. مَالِكِ يَوْمِ الدِّينِ\n5. إِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ\n6. اهْدِنَا الصِّرَاطَ الْمُسْتَقِيمَ\n7. صِرَاطَ الَّذِينَ أَنْعَمْتَ عَلَيْهِمْ غَيْرِ الْمَغْضُوبِ عَلَيْهِمْ وَلَا الضَّالِّينَ\n\n**Cara hafal:** Potong jadi 3 bagian. Ayat 1-2 dulu, lancar baru 3-4, baru 5-7. Jangan langsung 7 ayat sekaligus!"
    if "al-ikhlas" in t or "al ikhlas" in t or "ikhlas" in t:
        return f"**Surah Al-Ikhlas (4 ayat), {n}.**\n\n1. قُلْ هُوَ اللَّهُ أَحَدٌ - QUL HUWALLAAHU AHAD\n2. اللَّهُ الصَّمَدُ - ALLAAHUSH SHOMAD\n3. لَمْ يَلِدْ وَلَمْ يُولَدْ - LAM YALID WALAM YUULAD\n4. وَلَمْ يَكُنْ لَهُ كُفُوًا أَحَدٌ - WALAM YAKUL LAHUU KUFUWAN AHAD\n\n**Artinya:** Tentang ke-Esaan Allah. Pahalanya sama kayak sepertiga Al-Quran lho!"
    if "an-nas" in t or "an nas" in t:
        return f"**Surah An-Nas (6 ayat), {n}.**\n\nقُلْ أَعُوذُ بِرَبِّ النَّاسِ - مَلِكِ النَّاسِ - إِلَٰهِ النَّاسِ - مِنْ شَرِّ الْوَسْوَاسِ الْخَنَّاسِ - الَّذِي يُوَسْوِسُ فِي صُدُورِ النَّاسِ - مِنَ الْجِنَّةِ وَالنَّاسِ\n\n**Tips hafal:** Ini surah terakhir, sering dibaca sebelum tidur. Baca 3x tiap malam, seminggu pasti hafal!"
    if "al-falaq" in t or "al falaq" in t or "falaq" in t:
        return f"**Surah Al-Falaq (5 ayat), {n}.**\n\nقُلْ أَعُوذُ بِرَبِّ الْفَلَقِ - مِنْ شَرِّ مَا خَلَقَ - وَمِنْ شَرِّ غَاسِقٍ إِذَا وَقَبَ - وَمِنْ شَرِّ النَّفَّاثَاتِ فِي الْعُقَدِ - وَمِنْ شَرِّ حَاسِدٍ إِذَا حَسَدَ\n\nPasangan An-Nas, dibaca bareng sebelum tidur. Semangat!"
    if "juz 30" in t or "juz amma" in t or "surah pendek" in t:
        return f"**Juz 30 / Juz Amma ada 37 surah, {n}. Urutan dari yang paling gampang dihafal:**\n\n1. Al-Ikhlas, Al-Falaq, An-Nas (4-6 ayat)\n2. Al-Kautsar, Al-Ashr, An-Nashr (3 ayat)\n3. Al-Fatihah (7 ayat)\n4. Al-Qadr, Al-Zalzalah, Al-Adiyat\n5. Baru lanjut ke yang lebih panjang kayak An-Naba, Abasa\n\n**Saran:** Mulai dari yang paling pendek dulu biar semangat, jangan langsung An-Naba!"
    if "tahfidz" in t or "hafal" in t or "menghafal" in t:
        return f"**TAHFIDZ itu MENGHAFAL AL-QURAN, {n}.**\n\n**3 Kunci Sukses Tahfidz:**\n1. **Niat lurus** - karena Allah, bukan karena mau dipuji\n2. **Konsisten** - 1 ayat tiap hari lebih baik dari 1 juz sebulan sekali\n3. **Murojaah** - hafalan yang gak diulang = hilang\n\n**Coba ketik yang mau kamu hafal, contoh:**\n- Al-Fatihah\n- Al-Ikhlas\n- An-Nas\n- Cara hafal\n- Murojaah"

    # ============ JAWABAN UMUM ============
    if mode == "Iqro" or "iqro" in mode.lower():
        return f"**Semangat Iqro, {n}!**\n\nKamu nanya: '{tanya}'\n\n**Coba ketik salah satu ini:**\n- Huruf Hijaiyah\n- Iqro 1 / Iqro 2 / Iqro 3 / Iqro 4 / Iqro 5 / Iqro 6\n- Fathah / Tanwin / Sukun / Tasydid"
    if mode == "Tahsin" or "tahsin" in mode.lower():
        return f"**Semangat Tahsin, {n}!**\n\nKamu nanya: '{tanya}'\n\n**Coba ketik yang lengkap ya, contoh:**\n- Nun mati ketemu ba / ya / lam\n- Mim mati ketemu ba\n- Mad Thobi'i / Mad Wajib / Mad Lazim\n- Qolqolah / Ghunnah / Makhroj / Waqof / Izhar / Ikhfa"
    return f"**Semangat {n}!**\n\nKamu nanya: '{tanya}' di mode {mode}.\n\n**Coba ketik contoh ini biar aku jawab lengkap:**\n- Huruf Hijaiyah\n- Nun mati ketemu ba\n- Mad Thobi'i\n- Qolqolah\n- Cara hafal\n- Al-Fatihah / Al-Ikhlas / An-Nas"

if st.button("Tanya Qori AI"):
    if not pertanyaan:
        st.warning("Tulis dulu pertanyaannya ya!")
    else:
        st.info(jawab_qori(pertanyaan, mode))
st.write("---")
st.write("Semoga bermanfaat. Wassalamualaikum warahmatullahi wabarakatuh")
