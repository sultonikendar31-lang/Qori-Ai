import random
from datetime import datetime

import streamlit as st


SOAL_IQRO = [
    # --- IQRO 1: Huruf Hijaiyah ---
    {"soal": "[Iqro 1] Huruf apa ini? **ب**", "pilihan": ["Ba", "Ta", "Tsa", "Jim"], "jawaban": "Ba"},
    {"soal": "[Iqro 1] Huruf apa ini? **ت**", "pilihan": ["Ba", "Ta", "Tsa", "Ha"], "jawaban": "Ta"},
    {"soal": "[Iqro 1] Huruf apa ini? **ث**", "pilihan": ["Tsa", "Jim", "Ha", "Kha"], "jawaban": "Tsa"},
    {"soal": "[Iqro 1] Huruf apa ini? **ج**", "pilihan": ["Ha", "Jim", "Kha", "Dal"], "jawaban": "Jim"},
    {"soal": "[Iqro 1] Huruf apa ini? **ح**", "pilihan": ["Jim", "Ha", "Kha", "Ain"], "jawaban": "Ha"},
    {"soal": "[Iqro 1] Huruf apa ini? **خ**", "pilihan": ["Ha", "Jim", "Kha", "Dal"], "jawaban": "Kha"},
    {"soal": "[Iqro 1] Huruf apa ini? **ع**", "pilihan": ["Ain", "Ghain", "Fa", "Qof"], "jawaban": "Ain"},
    {"soal": "[Iqro 1] Huruf apa ini? **غ**", "pilihan": ["Ain", "Ghain", "Fa", "Qof"], "jawaban": "Ghain"},
    {"soal": "[Iqro 1] Huruf apa ini? **ق**", "pilihan": ["Fa", "Qof", "Kaf", "Lam"], "jawaban": "Qof"},
    {"soal": "[Iqro 1] Huruf apa ini? **ي**", "pilihan": ["Ya", "Nun", "Wawu", "Ha"], "jawaban": "Ya"},

    # --- IQRO 2: Fathah (A) ---
    {"soal": "[Iqro 2] Huruf **بَ** dibaca?", "pilihan": ["Ba", "Bi", "Bu", "Ban"], "jawaban": "Ba"},
    {"soal": "[Iqro 2] Huruf **تَ** dibaca?", "pilihan": ["Ta", "Ti", "Tu", "Tan"], "jawaban": "Ta"},
    {"soal": "[Iqro 2] Kata **كَتَبَ** dibaca?", "pilihan": ["Kataba", "Kutiba", "Kitaba", "Katuba"], "jawaban": "Kataba"},
    {"soal": "[Iqro 2] Kata **فَعَلَ** dibaca?", "pilihan": ["Fa'ala", "Fu'ila", "Fi'ala", "Fa'ula"], "jawaban": "Fa'ala"},
    {"soal": "[Iqro 2] Fathah bunyinya condong ke?", "pilihan": ["A", "I", "U", "E"], "jawaban": "A"},

    # --- IQRO 3: Kasrah (I) & Dhommah (U) ---
    {"soal": "[Iqro 3] Huruf **بِ** dibaca?", "pilihan": ["Bi", "Ba", "Bu", "Ban"], "jawaban": "Bi"},
    {"soal": "[Iqro 3] Huruf **بُ** dibaca?", "pilihan": ["Bu", "Ba", "Bi", "Ban"], "jawaban": "Bu"},
    {"soal": "[Iqro 3] Kata **كُتِبَ** dibaca?", "pilihan": ["Kutiba", "Kataba", "Kitaba", "Kutuba"], "jawaban": "Kutiba"},
    {"soal": "[Iqro 3] Kasrah bunyinya?", "pilihan": ["I", "A", "U", "O"], "jawaban": "I"},
    {"soal": "[Iqro 3] Dhommah bunyinya?", "pilihan": ["U", "A", "I", "E"], "jawaban": "U"},

    # --- IQRO 4: Tanwin & Nun Sukun ---
    {"soal": "[Iqro 4] Tanwin Fathah **بً** dibaca?", "pilihan": ["Ban", "Ba", "Bi", "Bu"], "jawaban": "Ban"},
    {"soal": "[Iqro 4] Tanwin Kasrah **بٍ** dibaca?", "pilihan": ["Bin", "Ban", "Bun", "Ba"], "jawaban": "Bin"},
    {"soal": "[Iqro 4] Tanwin Dhommah **بٌ** dibaca?", "pilihan": ["Bun", "Ban", "Bin", "Ba"], "jawaban": "Bun"},
    {"soal": "[Iqro 4] Kata **مِنْ** ada hukum apa?", "pilihan": ["Nun Sukun", "Mad", "Qolqolah", "Iqlab"], "jawaban": "Nun Sukun"},
    {"soal": "[Iqro 4] Kata **عَنْ** dibaca?", "pilihan": ["'An", "'A", "'In", "'Un"], "jawaban": "'An"},

    # --- IQRO 5: Mad, Tasydid, Qolqolah ---
    {"soal": "[Iqro 5] Huruf **بَا** dibaca panjang berapa?", "pilihan": ["2 harakat", "4 harakat", "6 harakat", "1 harakat"], "jawaban": "2 harakat"},
    {"soal": "[Iqro 5] Tanda tasydid ( ّ ) artinya?", "pilihan": ["Huruf dibaca double / ditekan", "Huruf dibaca panjang", "Huruf dibaca samar", "Huruf dibaca dengung"], "jawaban": "Huruf dibaca double / ditekan"},
    {"soal": "[Iqro 5] Huruf Qolqolah ada berapa?", "pilihan": ["5", "4", "6", "3"], "jawaban": "5"},
    {"soal": "[Iqro 5] Huruf Qolqolah adalah?", "pilihan": ["ق - ط - ب - ج - د", "ا - و - ي", "ن - م", "خ - غ"], "jawaban": "ق - ط - ب - ج - د"},
    {"soal": "[Iqro 5] Kata **قُلْ** huruf Qolqolah-nya?", "pilihan": ["Qof", "Lam", "Kaf", "Dal"], "jawaban": "Qof"},

    # --- IQRO 6: Waqof, Idgham, Ikhfa ---
    {"soal": "[Iqro 6] Tanda waqof **م** artinya?", "pilihan": ["Wajib berhenti", "Boleh berhenti", "Lanjut", "Ulang"], "jawaban": "Wajib berhenti"},
    {"soal": "[Iqro 6] Tanda waqof **ج** artinya?", "pilihan": ["Boleh berhenti / lanjut", "Wajib berhenti", "Harus lanjut", "Ulang"], "jawaban": "Boleh berhenti / lanjut"},
    {"soal": "[Iqro 6] Tanda waqof **لا** artinya?", "pilihan": ["Dilarang berhenti", "Wajib berhenti", "Boleh berhenti", "Ulang"], "jawaban": "Dilarang berhenti"},
    {"soal": "[Iqro 6] Mad Wajib Muttasil panjangnya?", "pilihan": ["4-5 harakat", "2 harakat", "6 harakat", "1 harakat"], "jawaban": "4-5 harakat"},
    {"soal": "[Iqro 6] Mad Lazim panjangnya?", "pilihan": ["6 harakat", "2 harakat", "4 harakat", "1 harakat"], "jawaban": "6 harakat"},
]
SOAL_TAHSIN = [
    {"soal": "[Tahsin] Nun Sukun bertemu Ba (مِنْ بَعْدِ) hukumnya?", "pilihan": ["Iqlab", "Idgham", "Ikhfa", "Idzhar"], "jawaban": "Iqlab"},
    {"soal": "[Tahsin] Nun Sukun bertemu Ya (مَنْ يَعْمَلْ) hukumnya?", "pilihan": ["Idgham Bighunnah", "Iqlab", "Ikhfa", "Idzhar"], "jawaban": "Idgham Bighunnah"},
    {"soal": "[Tahsin] Nun Sukun bertemu Ro (مِنْ رَبِّهِمْ) hukumnya?", "pilihan": ["Idgham Bilaghunnah", "Idgham Bighunnah", "Ikhfa", "Idzhar"], "jawaban": "Idgham Bilaghunnah"},
    {"soal": "[Tahsin] Nun Sukun bertemu Lam (مِنْ لَدُنْهُ) hukumnya?", "pilihan": ["Idgham Bilaghunnah", "Ikhfa", "Idzhar", "Iqlab"], "jawaban": "Idgham Bilaghunnah"},
    {"soal": "[Tahsin] Nun Sukun bertemu Ha (مِنْهَا) hukumnya?", "pilihan": ["Idzhar Halqi", "Ikhfa", "Idgham", "Iqlab"], "jawaban": "Idzhar Halqi"},
    {"soal": "[Tahsin] Huruf Idzhar Halqi ada berapa?", "pilihan": ["6", "5", "4", "15"], "jawaban": "6"},
    {"soal": "[Tahsin] Huruf Idzhar Halqi adalah?", "pilihan": ["ا - ه - ع - ح - غ - خ", "ي - ن - م - و", "ق - ط - ب - ج - د", "ب - ج - د"], "jawaban": "ا - ه - ع - ح - غ - خ"},
    {"soal": "[Tahsin] Huruf Ikhfa ada berapa?", "pilihan": ["15", "6", "4", "5"], "jawaban": "15"},
    {"soal": "[Tahsin] Tanwin bertemu Jim hukumnya?", "pilihan": ["Ikhfa", "Idzhar", "Iqlab", "Idgham"], "jawaban": "Ikhfa"},
    {"soal": "[Tahsin] Mim Sukun bertemu Ba (هُمْ بِهِ) hukumnya?", "pilihan": ["Ikhfa Syafawi", "Idgham Mimi", "Idzhar Syafawi", "Iqlab"], "jawaban": "Ikhfa Syafawi"},
    {"soal": "[Tahsin] Mim Sukun bertemu Mim hukumnya?", "pilihan": ["Idgham Mimi", "Ikhfa Syafawi", "Idzhar Syafawi", "Iqlab"], "jawaban": "Idgham Mimi"},
    {"soal": "[Tahsin] Mim Sukun bertemu selain Ba & Mim hukumnya?", "pilihan": ["Idzhar Syafawi", "Ikhfa Syafawi", "Idgham Mimi", "Iqlab"], "jawaban": "Idzhar Syafawi"},
    {"soal": "[Tahsin] Mad Thabi'i panjangnya?", "pilihan": ["2 harakat", "6 harakat", "4 harakat", "1 harakat"], "jawaban": "2 harakat"},
    {"soal": "[Tahsin] Mad Wajib Muttasil contohnya?", "pilihan": ["جَاءَ", "قَالَ", "كَانَ", "مِنْ"], "jawaban": "جَاءَ"},
    {"soal": "[Tahsin] Mad Jaiz Munfasil terjadi jika?", "pilihan": ["Mad di akhir kata, Hamzah di awal kata berikutnya", "Mad & Hamzah satu kata", "Mad bertemu sukun", "Mad bertemu tasydid"], "jawaban": "Mad di akhir kata, Hamzah di awal kata berikutnya"},
    {"soal": "[Tahsin] Lam Jalalah dibaca Tafkhim jika sebelumnya?", "pilihan": ["Fathah / Dhommah", "Kasrah", "Sukun", "Tanwin"], "jawaban": "Fathah / Dhommah"},
    {"soal": "[Tahsin] Lam Jalalah dibaca Tarqiq jika sebelumnya?", "pilihan": ["Kasrah", "Fathah", "Dhommah", "Sukun"], "jawaban": "Kasrah"},
    {"soal": "[Tahsin] Qolqolah Kubro terjadi saat?", "pilihan": ["Huruf Qolqolah sukun di akhir & waqof", "Huruf Qolqolah di tengah", "Huruf Qolqolah berharakat", "Huruf Qolqolah tasydid"], "jawaban": "Huruf Qolqolah sukun di akhir & waqof"},
    {"soal": "[Tahsin] Qolqolah Sughro terjadi saat?", "pilihan": ["Huruf Qolqolah sukun di tengah kata", "Huruf Qolqolah di akhir & waqof", "Huruf Qolqolah berharakat", "Huruf Qolqolah tasydid"], "jawaban": "Huruf Qolqolah sukun di tengah kata"},
    {"soal": "[Tahsin] Ghunnah artinya?", "pilihan": ["Dengung", "Samar", "Jelas", "Memantul"], "jawaban": "Dengung"},
    {"soal": "[Tahsin] Ghunnah pada Nun & Mim bertasydid dibaca?", "pilihan": ["2 harakat dengung", "1 harakat", "6 harakat", "Tanpa dengung"], "jawaban": "2 harakat dengung"},
    {"soal": "[Tahsin] Hukum Alif Lam Syamsiyah, Lam-nya?", "pilihan": ["Tidak dibaca (dilebur)", "Dibaca jelas", "Dibaca dengung", "Dibaca memantul"], "jawaban": "Tidak dibaca (dilebur)"},
    {"soal": "[Tahsin] Contoh Alif Lam Qomariyah?", "pilihan": ["الْقَمَرُ", "الشَّمْسُ", "الرَّحْمَنُ", "النَّاسُ"], "jawaban": "الْقَمَرُ"},
    {"soal": "[Tahsin] Contoh Alif Lam Syamsiyah?", "pilihan": ["الشَّمْسُ", "الْقَمَرُ", "الْكِتَابُ", "الْحَمْدُ"], "jawaban": "الشَّمْسُ"},
    {"soal": "[Tahsin] Hukum bacaan Ra (ر) dibaca Tafkhim jika?", "pilihan": ["Berharakat Fathah / Dhommah", "Berharakat Kasrah", "Sukun setelah Kasrah", "Semua benar"], "jawaban": "Berharakat Fathah / Dhommah"},
]
SOAL_TAHFIDZ = [
    {"soal": "[Juz 30 - An-Naba] Lanjutkan: عَمَّ يَتَسَاءَلُونَ ...", "pilihan": ["عَنِ النَّبَإِ الْعَظِيمِ", "وَالنَّازِعَاتِ", "وَالسَّمَاءِ", "وَالشَّمْسِ"], "jawaban": "عَنِ النَّبَإِ الْعَظِيمِ"},
    {"soal": "[Juz 30 - An-Nazi'at] Lanjutkan: وَالنَّازِعَاتِ ...", "pilihan": ["غَرْقًا", "نَشْطًا", "سَبْحًا", "أَمْرًا"], "jawaban": "غَرْقًا"},
    {"soal": "[Juz 30 - 'Abasa] Lanjutkan: عَبَسَ وَتَوَلَّى ...", "pilihan": ["أَنْ جَاءَهُ الْأَعْمَى", "وَالنَّازِعَاتِ", "وَالشَّمْسِ", "وَاللَّيْلِ"], "jawaban": "أَنْ جَاءَهُ الْأَعْمَى"},
    {"soal": "[Juz 30 - At-Takwir] Lanjutkan: إِذَا الشَّمْسُ ...", "pilihan": ["كُوِّرَتْ", "انْفَطَرَتْ", "انْشَقَّتْ", "طُمِسَتْ"], "jawaban": "كُوِّرَتْ"},
    {"soal": "[Juz 30 - Al-Infithar] Lanjutkan: إِذَا السَّمَاءُ ...", "pilihan": ["انْفَطَرَتْ", "كُوِّرَتْ", "انْشَقَّتْ", "زُلْزِلَتْ"], "jawaban": "انْفَطَرَتْ"},
    {"soal": "[Juz 30 - Al-Muthaffifin] Lanjutkan: وَيْلٌ لِلْمُطَفِّفِينَ ...", "pilihan": ["الَّذِينَ إِذَا اكْتَالُوا", "إِذَا الشَّمْسُ", "وَالسَّمَاءِ", "وَالطَّارِقِ"], "jawaban": "الَّذِينَ إِذَا اكْتَالُوا"},
    {"soal": "[Juz 30 - Al-Insyiqaq] Lanjutkan: إِذَا السَّمَاءُ ...", "pilihan": ["انْشَقَّتْ", "كُوِّرَتْ", "انْفَطَرَتْ", "زُلْزِلَتْ"], "jawaban": "انْشَقَّتْ"},
    {"soal": "[Juz 30 - Al-Buruj] Lanjutkan: وَالسَّمَاءِ ذَاتِ ...", "pilihan": ["الْبُرُوجِ", "الطَّارِقِ", "الشَّمْسِ", "اللَّيْلِ"], "jawaban": "الْبُرُوجِ"},
    {"soal": "[Juz 30 - Ath-Thariq] Lanjutkan: وَالسَّمَاءِ وَالطَّارِقِ ...", "pilihan": ["وَمَا أَدْرَاكَ مَا الطَّارِقُ", "وَالنَّجْمِ", "وَالْفَجْرِ", "وَالضُّحَى"], "jawaban": "وَمَا أَدْرَاكَ مَا الطَّارِقُ"},
    {"soal": "[Juz 30 - Al-A'la] Lanjutkan: سَبِّحِ اسْمَ رَبِّكَ ...", "pilihan": ["الْأَعْلَى", "الْعَظِيمِ", "الْكَرِيمِ", "الْحَمِيدِ"], "jawaban": "الْأَعْلَى"},
    {"soal": "[Juz 30 - Al-Ghasyiyah] Lanjutkan: هَلْ أَتَاكَ حَدِيثُ ...", "pilihan": ["الْغَاشِيَةِ", "الطَّارِقِ", "الْفَجْرِ", "اللَّيْلِ"], "jawaban": "الْغَاشِيَةِ"},
    {"soal": "[Juz 30 - Al-Fajr] Lanjutkan: وَالْفَجْرِ ...", "pilihan": ["وَلَيَالٍ عَشْرٍ", "وَالشَّمْسِ", "وَالضُّحَى", "وَاللَّيْلِ"], "jawaban": "وَلَيَالٍ عَشْرٍ"},
    {"soal": "[Juz 30 - Al-Balad] Lanjutkan: لَا أُقْسِمُ بِهَٰذَا ...", "pilihan": ["الْبَلَدِ", "الْفَجْرِ", "الشَّمْسِ", "اللَّيْلِ"], "jawaban": "الْبَلَدِ"},
    {"soal": "[Juz 30 - Asy-Syams] Lanjutkan: وَالشَّمْسِ وَضُحَاهَا ...", "pilihan": ["وَالْقَمَرِ إِذَا تَلَاهَا", "وَاللَّيْلِ", "وَالنَّهَارِ", "وَالْفَجْرِ"], "jawaban": "وَالْقَمَرِ إِذَا تَلَاهَا"},
    {"soal": "[Juz 30 - Al-Lail] Lanjutkan: وَاللَّيْلِ إِذَا ...", "pilihan": ["يَغْشَى", "تَجَلَّى", "سَجَى", "ضُحَى"], "jawaban": "يَغْشَى"},
    {"soal": "[Juz 30 - Adh-Dhuha] Lanjutkan: وَالضُّحَى ...", "pilihan": ["وَاللَّيْلِ إِذَا سَجَى", "وَالشَّمْسِ", "وَالْفَجْرِ", "وَالْعَصْرِ"], "jawaban": "وَاللَّيْلِ إِذَا سَجَى"},
    {"soal": "[Juz 30 - Asy-Syarh] Lanjutkan: أَلَمْ نَشْرَحْ لَكَ ...", "pilihan": ["صَدْرَكَ", "قَلْبَكَ", "عَيْنَكَ", "أَمْرَكَ"], "jawaban": "صَدْرَكَ"},
    {"soal": "[Juz 30 - At-Tin] Lanjutkan: وَالتِّينِ وَالزَّيْتُونِ ...", "pilihan": ["وَطُورِ سِينِينَ", "وَالْعَصْرِ", "وَالشَّمْسِ", "وَاللَّيْلِ"], "jawaban": "وَطُورِ سِينِينَ"},
    {"soal": "[Juz 30 - Al-'Alaq] Lanjutkan: اقْرَأْ بِاسْمِ رَبِّكَ الَّذِي ...", "pilihan": ["خَلَقَ", "أَنْزَلَ", "أَرْسَلَ", "جَعَلَ"], "jawaban": "خَلَقَ"},
    {"soal": "[Juz 30 - Al-Qadr] Lanjutkan: إِنَّا أَنْزَلْنَاهُ فِي لَيْلَةِ ...", "pilihan": ["الْقَدْرِ", "الْجُمُعَةِ", "الْفَجْرِ", "النَّصْرِ"], "jawaban": "الْقَدْرِ"},
    {"soal": "[Juz 30 - Al-Bayyinah] Lanjutkan: لَمْ يَكُنِ الَّذِينَ كَفَرُوا ...", "pilihan": ["مِنْ أَهْلِ الْكِتَابِ", "مِنَ الْمُشْرِكِينَ", "مِنَ الْمُنَافِقِينَ", "مِنَ الْكَافِرِينَ"], "jawaban": "مِنْ أَهْلِ الْكِتَابِ"},
    {"soal": "[Juz 30 - Az-Zalzalah] Lanjutkan: إِذَا زُلْزِلَتِ الْأَرْضُ ...", "pilihan": ["زِلْزَالَهَا", "انْشِقَاقَهَا", "انْفِطَارَهَا", "دَكًّا"], "jawaban": "زِلْزَالَهَا"},
    {"soal": "[Juz 30 - Al-'Adiyat] Lanjutkan: وَالْعَادِيَاتِ ...", "pilihan": ["ضَبْحًا", "قَدْحًا", "صُبْحًا", "نَقْعًا"], "jawaban": "ضَبْحًا"},
    {"soal": "[Juz 30 - Al-Qari'ah] Lanjutkan: الْقَارِعَةُ ...", "pilihan": ["مَا الْقَارِعَةُ", "مَا الْحَاقَّةُ", "مَا سَقَرُ", "مَا الْعَادِيَاتُ"], "jawaban": "مَا الْقَارِعَةُ"},
    {"soal": "[Juz 30 - At-Takatsur] Lanjutkan: أَلْهَاكُمُ ...", "pilihan": ["التَّكَاثُرُ", "التَّفَاخُرُ", "التَّنَافُسُ", "التَّكَابُرُ"], "jawaban": "التَّكَاثُرُ"},
    {"soal": "[Juz 30 - Al-'Ashr] Lanjutkan: وَالْعَصْرِ إِنَّ الْإِنْسَانَ ...", "pilihan": ["لَفِي خُسْرٍ", "فِي جَنَّةٍ", "لَا يَمُوتُ", "فِي نَعِيمٍ"], "jawaban": "لَفِي خُسْرٍ"},
    {"soal": "[Juz 30 - Al-Humazah] Lanjutkan: وَيْلٌ لِكُلِّ ...", "pilihan": ["هُمَزَةٍ لُمَزَةٍ", "مُطَفِّفٍ", "كَافِرٍ", "مُنَافِقٍ"], "jawaban": "هُمَزَةٍ لُمَزَةٍ"},
    {"soal": "[Juz 30 - Al-Fil] Lanjutkan: أَلَمْ تَرَ كَيْفَ فَعَلَ رَبُّكَ بِأَصْحَابِ ...", "pilihan": ["الْفِيلِ", "الْأُخْدُودِ", "الْكَهْفِ", "الرَّسِّ"], "jawaban": "الْفِيلِ"},
    {"soal": "[Juz 30 - Quraisy] Lanjutkan: لِإِيلَافِ ...", "pilihan": ["قُرَيْشٍ", "الْفِيلِ", "الْعَرَبِ", "مَكَّةَ"], "jawaban": "قُرَيْشٍ"},
    {"soal": "[Juz 30 - Al-Ma'un] Lanjutkan: أَرَأَيْتَ الَّذِي يُكَذِّبُ ...", "pilihan": ["بِالدِّينِ", "بِالْحَقِّ", "بِالْيَوْمِ", "بِالنَّارِ"], "jawaban": "بِالدِّينِ"},
    {"soal": "[Juz 30 - Al-Kautsar] Lanjutkan: إِنَّا أَعْطَيْنَاكَ ...", "pilihan": ["الْكَوْثَرَ", "الْفَلَقَ", "النَّاسَ", "الْعَصْرَ"], "jawaban": "الْكَوْثَرَ"},
    {"soal": "[Juz 30 - Al-Kafirun] Lanjutkan: قُلْ يَا أَيُّهَا ...", "pilihan": ["الْكَافِرُونَ", "الْمُؤْمِنُونَ", "الْمُشْرِكُونَ", "الْمُنَافِقُونَ"], "jawaban": "الْكَافِرُونَ"},
    {"soal": "[Juz 30 - An-Nashr] Lanjutkan: إِذَا جَاءَ نَصْرُ اللَّهِ ...", "pilihan": ["وَالْفَتْحُ", "وَالْعَصْرُ", "وَالْكَوْثَرُ", "وَالنَّاسُ"], "jawaban": "وَالْفَتْحُ"},
    {"soal": "[Juz 30 - Al-Lahab] Lanjutkan: تَبَّتْ يَدَا أَبِي لَهَبٍ ...", "pilihan": ["وَتَبَّ", "وَمَا أَدْرَاكَ", "فِي جِيدِهَا", "سَيَصْلَى"], "jawaban": "وَتَبَّ"},
    {"soal": "[Juz 30 - Al-Ikhlas] Lanjutkan: قُلْ هُوَ اللَّهُ ...", "pilihan": ["أَحَدٌ", "الصَّمَدُ", "لَمْ يَلِدْ", "كُفُوًا"], "jawaban": "أَحَدٌ"},
    {"soal": "[Juz 30 - Al-Falaq] Lanjutkan: قُلْ أَعُوذُ بِرَبِّ ...", "pilihan": ["الْفَلَقِ", "النَّاسِ", "الْعَالَمِينَ", "الْفَاتِحَةِ"], "jawaban": "الْفَلَقِ"},
    {"soal": "[Juz 30 - An-Nas] Lanjutkan: قُلْ أَعُوذُ بِرَبِّ ...", "pilihan": ["النَّاسِ", "الْفَلَقِ", "الْعَالَمِينَ", "الْفَاتِحَةِ"], "jawaban": "النَّاسِ"},
    {"soal": "[Juz 30] Surat pertama di Juz 30 adalah?", "pilihan": ["An-Naba", "Al-Fatihah", "Al-Baqarah", "Yasin"], "jawaban": "An-Naba"},
    {"soal": "[Juz 30] Surat terakhir di Juz 30 adalah?", "pilihan": ["An-Nas", "Al-Falaq", "Al-Ikhlas", "Al-Lahab"], "jawaban": "An-Nas"},
    {"soal": "[Juz 30 - Al-Fatihah] الْحَمْدُ لِلَّهِ رَبِّ ...", "pilihan": ["الْعَالَمِينَ", "الرَّحِيمِ", "مَالِكِ يَوْمِ الدِّينِ", "اهْدِنَا"], "jawaban": "الْعَالَمِينَ"},
]


# ======================================================
# FUNGSI PENYIMPANAN HASIL GAME
# ======================================================
def simpan_hasil_game(supabase, nama, mode, poin, benar, salah):
    """Simpan satu hasil ketika siswa berhasil mencapai FINISH."""
    try:
        supabase.table("hasil_game").insert({
            "nama": str(nama),
            "mode": str(mode),
            "poin": int(poin),
            "benar": int(benar),
            "salah": int(salah),
            "tanggal": datetime.now().strftime("%Y-%m-%d %H:%M"),
        }).execute()
        return True
    except Exception as e:
        # Kegagalan pencatatan nilai tidak boleh mematikan game.
        print(f"Gagal simpan hasil game: {e}")
        return False


def _game_key(nama_siswa, item):
    """Gunakan state terpisah untuk setiap siswa."""
    identitas = str(nama_siswa or "siswa").strip().lower().replace(" ", "_")
    return f"qori_game_{identitas}_{item}"


def _game_get(nama_siswa, item, default):
    key = _game_key(nama_siswa, item)
    if key not in st.session_state:
        st.session_state[key] = default
    return st.session_state[key]


def _game_set(nama_siswa, item, value):
    st.session_state[_game_key(nama_siswa, item)] = value


def _reset_game(nama_siswa):
    nilai_awal = {
        "posisi": 0,
        "poin": 0,
        "benar": 0,
        "salah": 0,
        "soal_aktif": None,
        "dadu": 0,
        "selesai": False,
        "mode_aktif": None,
    }
    for item, value in nilai_awal.items():
        _game_set(nama_siswa, item, value)


# ======================================================
# SISWA: BERMAIN GAME QORI
# ======================================================
def tampilkan_game_qori(supabase, nama_siswa):
    st.markdown("### 🎲 Game Petualangan QORI")
    st.write(
        f"Halo **{nama_siswa}**, pilih materi, kocok dadu, "
        "jawab tantangan, dan capai kotak FINISH!"
    )

    pilihan_mode = [
        "📖 Iqro 1-6",
        "🎙️ Tahsin - Tajwid Lengkap",
        "🧠 Tahfidz - Juz 30 Full",
    ]
    mode = st.selectbox(
        "Pilih Materi:",
        pilihan_mode,
        key=_game_key(nama_siswa, "pilih_mode"),
    )

    mode_sebelumnya = _game_get(nama_siswa, "mode_aktif", None)
    if mode_sebelumnya is None:
        _game_set(nama_siswa, "mode_aktif", mode)
    elif mode_sebelumnya != mode:
        # Setiap pergantian materi memulai permainan baru agar soal/nilai
        # dari materi sebelumnya tidak tercampur.
        _reset_game(nama_siswa)
        _game_set(nama_siswa, "mode_aktif", mode)
        st.rerun()

    posisi = _game_get(nama_siswa, "posisi", 0)
    poin = _game_get(nama_siswa, "poin", 0)
    benar = _game_get(nama_siswa, "benar", 0)
    salah = _game_get(nama_siswa, "salah", 0)
    dadu = _game_get(nama_siswa, "dadu", 0)
    selesai = _game_get(nama_siswa, "selesai", False)

    kolom1, kolom2, kolom3 = st.columns(3)
    kolom1.metric("📍 Posisi", f"{posisi} / 30")
    kolom2.metric("⭐ Poin", poin)
    kolom3.metric("🎲 Dadu", dadu or "-")
    st.progress(min(max(posisi / 30, 0.0), 1.0))

    papan = ""
    for nomor in range(1, 31):
        if nomor == posisi:
            papan += " 🧕 "
        elif nomor % 5 == 0:
            papan += " ❓ "
        elif nomor % 7 == 0:
            papan += " 🧩 "
        else:
            papan += f" {nomor} "
        if nomor % 6 == 0:
            papan += "\n"

    st.text(papan)
    st.caption("🧕 = Posisi siswa | ❓ = Kotak soal | 🧩 = Kotak tantangan")

    if selesai:
        st.balloons()
        st.success(
            f"🎉 MASYAALLAH! {nama_siswa} mencapai FINISH! "
            f"Poin: {poin} | Benar: {benar} | Salah: {salah}"
        )
        if st.button("Main Lagi", key=_game_key(nama_siswa, "main_lagi")):
            _reset_game(nama_siswa)
            _game_set(nama_siswa, "mode_aktif", mode)
            st.rerun()
        return

    if st.button(
        "🎲 KOCOK DADU!",
        use_container_width=True,
        key=_game_key(nama_siswa, "kocok_dadu"),
    ):
        hasil_dadu = random.randint(1, 6)
        posisi_baru = posisi + hasil_dadu
        _game_set(nama_siswa, "dadu", hasil_dadu)

        if posisi_baru >= 30:
            posisi_baru = 30
            poin_baru = poin + 50
            _game_set(nama_siswa, "posisi", posisi_baru)
            _game_set(nama_siswa, "poin", poin_baru)
            _game_set(nama_siswa, "selesai", True)
            simpan_hasil_game(
                supabase,
                nama_siswa,
                mode,
                poin_baru,
                benar,
                salah,
            )
            st.rerun()

        _game_set(nama_siswa, "posisi", posisi_baru)

        if posisi_baru % 5 == 0 or posisi_baru % 7 == 0:
            if mode.startswith("📖 Iqro"):
                bank_soal = SOAL_IQRO
            elif mode.startswith("🎙️ Tahsin"):
                bank_soal = SOAL_TAHSIN
            else:
                bank_soal = SOAL_TAHFIDZ

            _game_set(nama_siswa, "soal_aktif", random.choice(bank_soal))
        else:
            _game_set(nama_siswa, "soal_aktif", None)
            st.info(
                f"Berjalan {hasil_dadu} langkah ke kotak {posisi_baru}. "
                "Kotak aman, silakan kocok dadu lagi."
            )
        st.rerun()

    soal = _game_get(nama_siswa, "soal_aktif", None)
    if soal:
        st.markdown("---")
        st.markdown(f"### ❓ Tantangan Kotak {posisi}")
        st.markdown(f"**{soal['soal']}**")
        jawaban = st.radio(
            "Pilih jawaban:",
            soal["pilihan"],
            key=_game_key(nama_siswa, f"pilihan_{posisi}_{dadu}"),
        )
        if st.button(
            "Jawab!",
            key=_game_key(nama_siswa, f"tombol_jawab_{posisi}_{dadu}"),
        ):
            if jawaban == soal["jawaban"]:
                _game_set(nama_siswa, "poin", _game_get(nama_siswa, "poin", 0) + 10)
                _game_set(nama_siswa, "benar", _game_get(nama_siswa, "benar", 0) + 1)
                _game_set(
                    nama_siswa,
                    "posisi",
                    min(30, _game_get(nama_siswa, "posisi", 0) + 2),
                )
                st.success("✅ BENAR! Maju 2 langkah dan mendapat 10 poin!")
            else:
                _game_set(nama_siswa, "salah", _game_get(nama_siswa, "salah", 0) + 1)
                _game_set(
                    nama_siswa,
                    "poin",
                    max(0, _game_get(nama_siswa, "poin", 0) - 5),
                )
                _game_set(
                    nama_siswa,
                    "posisi",
                    max(0, _game_get(nama_siswa, "posisi", 0) - 2),
                )
                st.error(f"❌ Jawaban yang benar: {soal['jawaban']}. Mundur 2 langkah.")

            _game_set(nama_siswa, "soal_aktif", None)
            st.rerun()

    if st.button(
        "🔄 Ulang dari Awal",
        key=_game_key(nama_siswa, "ulang_dari_awal"),
    ):
        _reset_game(nama_siswa)
        _game_set(nama_siswa, "mode_aktif", mode)
        st.rerun()


# ======================================================
# TIM: HANYA MELIHAT HASIL GAME SISWA
# ======================================================
def tampilkan_hasil_game(supabase):
    st.markdown("### 📊 Hasil Game QORI - Siswa")
    st.write("Akun Tim hanya dapat melihat hasil permainan siswa.")

    try:
        rows = (
            supabase.table("hasil_game")
            .select("*")
            .order("id", desc=True)
            .execute()
            .data
            or []
        )
    except Exception as e:
        st.warning(
            "Tabel hasil_game belum tersedia atau tidak dapat dibaca. "
            f"Periksa tabel dan izin Supabase. Detail: {e}"
        )
        return

    if not rows:
        st.info("Belum ada siswa yang menyelesaikan permainan.")
        return

    for row in rows:
        st.markdown(
            f"**{row.get('nama', '-')}** | {row.get('mode', '-')} | "
            f"⭐ {row.get('poin', 0)} Poin | "
            f"✅ {row.get('benar', 0)} Benar | "
            f"❌ {row.get('salah', 0)} Salah | "
            f"{row.get('tanggal', '')}"
        )
        st.divider()
