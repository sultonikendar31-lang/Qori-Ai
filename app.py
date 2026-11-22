import streamlit as st

# ===== DATA LENGKAP JUZ 30 (SURAH 78-114) =====
# Sumber teks ayat: data yang diberikan pengguna.
BASMALAH = "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ"

# Setiap surah = 1 string, ayat dipisah dengan \n
AYAT_JUZ30 = {
"78. An-Naba'": """عَمَّ يَتَسَاءَلُونَ
عَنِ النَّبَإِ الْعَظِيمِ
الَّذِي هُمْ فِيهِ مُخْتَلِفُونَ
كَلَّا سَيَعْلَمُونَ
ثُمَّ كَلَّا سَيَعْلَمُونَ
أَلَمْ نَجْعَلِ الْأَرْضَ مِهَادًا
وَالْجِبَالَ أَوْتَادًا
وَخَلَقْنَاكُمْ أَزْوَاجًا
وَجَعَلْنَا نَوْمَكُمْ سُبَاتًا
وَجَعَلْنَا اللَّيْلَ لِبَاسًا
وَجَعَلْنَا النَّهَارَ مَعَاشًا
وَبَنَيْنَا فَوْقَكُمْ سَبْعًا شِدَادًا
وَجَعَلْنَا سِرَاجًا وَهَّاجًا
وَأَنْزَلْنَا مِنَ الْمُعْصِرَاتِ مَاءً ثَجَّاجًا
لِنُخْرِجَ بِهِ حَبًّا وَنَبَاتًا
وَجَنَّاتٍ أَلْفَافًا
إِنَّ يَوْمَ الْفَصْلِ كَانَ مِيقَاتًا
يَوْمَ يُنْفَخُ فِي الصُّورِ فَتَأْتُونَ أَفْوَاجًا
وَفُتِحَتِ السَّمَاءُ فَكَانَتْ أَبْوَابًا
وَسُيِّرَتِ الْجِبَالُ فَكَانَتْ سَرَابًا
إِنَّ جَهَنَّمَ كَانَتْ مِرْصَادًا
لِلطَّاغِينَ مَآبًا
لَابِثِينَ فِيهَا أَحْقَابًا
لَا يَذُوقُونَ فِيهَا بَرْدًا وَلَا شَرَابًا
إِلَّا حَمِيمًا وَغَسَّاقًا
جَزَاءً وِفَاقًا
إِنَّهُمْ كَانُوا لَا يَرْجُونَ حِسَابًا
وَكَذَّبُوا بِآيَاتِنَا كِذَّابًا
وَكُلَّ شَيْءٍ أَحْصَيْنَاهُ كِتَابًا
فَذُوقُوا فَلَنْ نَزِيدَكُمْ إِلَّا عَذَابًا
إِنَّ لِلْمُتَّقِينَ مَفَازًا
حَدَائِقَ وَأَعْنَابًا
وَكَوَاعِبَ أَتْرَابًا
وَكَأْسًا دِهَاقًا
لَا يَسْمَعُونَ فِيهَا لَغْوًا وَلَا كِذَّابًا
جَزَاءً مِنْ رَبِّكَ عَطَاءً حِسَابًا
رَبِّ السَّمَاوَاتِ وَالْأَرْضِ وَمَا بَيْنَهُمَا الرَّحْمَٰنِ ۖ لَا يَمْلِكُونَ مِنْهُ خِطَابًا
يَوْمَ يَقُومُ الرُّوحُ وَالْمَلَائِكَةُ صَفًّا ۖ لَا يَتَكَلَّمُونَ إِلَّا مَنْ أَذِنَ لَهُ الرَّحْمَٰنُ وَقَالَ صَوَابًا
ذَٰلِكَ الْيَوْمُ الْحَقُّ ۖ فَمَنْ شَاءَ اتَّخَذَ إِلَىٰ رَبِّهِ مَآبًا
إِنَّا أَنْذَرْنَاكُمْ عَذَابًا قَرِيبًا يَوْمَ يَنْظُرُ الْمَرْءُ مَا قَدَّمَتْ يَدَاهُ وَيَقُولُ الْكَافِرُ يَا لَيْتَنِي كُنْتُ تُرَابًا""",
"79. An-Nazi'at": """وَالنَّازِعَاتِ غَرْقًا
وَالنَّاشِطَاتِ نَشْطًا
وَالسَّابِحَاتِ سَبْحًا
فَالسَّابِقَاتِ سَبْقًا
فَالْمُدَبِّرَاتِ أَمْرًا
يَوْمَ تَرْجُفُ الرَّاجِفَةُ
تَتْبَعُهَا الرَّادِفَةُ
قُلُوبٌ يَوْمَئِذٍ وَاجِفَةٌ
أَبْصَارُهَا خَاشِعَةٌ
يَقُولُونَ أَإِنَّا لَمَرْدُودُونَ فِي الْحَافِرَةِ
أَإِذَا كُنَّا عِظَامًا نَخِرَةً
قَالُوا تِلْكَ إِذًا كَرَّةٌ خَاسِرَةٌ
فَإِنَّمَا هِيَ زَجْرَةٌ وَاحِدَةٌ
فَإِذَا هُمْ بِالسَّاهِرَةِ
هَلْ أَتَاكَ حَدِيثُ مُوسَىٰ
إِذْ نَادَاهُ رَبُّهُ بِالْوَادِ الْمُقَدَّسِ طُوًى
اذْهَبْ إِلَىٰ فِرْعَوْنَ إِنَّهُ طَغَىٰ
فَقُلْ هَلْ لَكَ إِلَىٰ أَنْ تَزَكَّىٰ
وَأَهْدِيَكَ إِلَىٰ رَبِّكَ فَتَخْشَىٰ
فَأَرَاهُ الْآيَةَ الْكُبْرَىٰ
فَكَذَّبَ وَعَصَىٰ
ثُمَّ أَدْبَرَ يَسْعَىٰ
فَحَشَرَ فَنَادَىٰ
فَقَالَ أَنَا رَبُّكُمُ الْأَعْلَىٰ
فَأَخَذَهُ اللَّهُ نَكَالَ الْآخِرَةِ وَالْأُولَىٰ
إِنَّ فِي ذَٰلِكَ لَعِبْرَةً لِمَنْ يَخْشَىٰ
أَأَنْتُمْ أَشَدُّ خَلْقًا أَمِ السَّمَاءُ ۚ بَنَاهَا
رَفَعَ سَمْكَهَا فَسَوَّاهَا
وَأَغْطَشَ لَيْلَهَا وَأَخْرَجَ ضُحَاهَا
وَالْأَرْضَ بَعْدَ ذَٰلِكَ دَحَاهَا
أَخْرَجَ مِنْهَا مَاءَهَا وَمَرْعَاهَا
وَالْجِبَالَ أَرْسَاهَا
مَتَاعًا لَكُمْ وَلِأَنْعَامِكُمْ
فَإِذَا جَاءَتِ الطَّامَّةُ الْكُبْرَىٰ
يَوْمَ يَتَذَكَّرُ الْإِنْسَانُ مَا سَعَىٰ
وَبُرِّزَتِ الْجَحِيمُ لِمَنْ يَرَىٰ
فَأَمَّا مَنْ طَغَىٰ
وَآثَرَ الْحَيَاةَ الدُّنْيَا
فَإِنَّ الْجَحِيمَ هِيَ الْمَأْوَىٰ
وَأَمَّا مَنْ خَافَ مَقَامَ رَبِّهِ وَنَهَى النَّفْسَ عَنِ الْهَوَىٰ
فَإِنَّ الْجَنَّةَ هِيَ الْمَأْوَىٰ
يَسْأَلُونَكَ عَنِ السَّاعَةِ أَيَّانَ مُرْسَاهَا
فِيمَ أَنْتَ مِنْ ذِكْرَاهَا
إِلَىٰ رَبِّكَ مُنْتَهَاهَا
إِنَّمَا أَنْتَ مُنْذِرُ مَنْ يَخْشَاهَا
كَأَنَّهُمْ يَوْمَ يَرَوْنَهَا لَمْ يَلْبَثُوا إِلَّا عَشِيَّةً أَوْ ضُحَاهَا""",
"80. 'Abasa": """عَبَسَ وَتَوَلَّىٰ
أَنْ جَاءَهُ الْأَعْمَىٰ
وَمَا يُدْرِيكَ لَعَلَّهُ يَزَّكَّىٰ
أَوْ يَذَّكَّرُ فَتَنْفَعَهُ الذِّكْرَىٰ
أَمَّا مَنِ اسْتَغْنَىٰ
فَأَنْتَ لَهُ تَصَدَّىٰ
وَمَا عَلَيْكَ أَلَّا يَزَّكَّىٰ
وَأَمَّا مَنْ جَاءَكَ يَسْعَىٰ
وَهُوَ يَخْشَىٰ
فَأَنْتَ عَنْهُ تَلَهَّىٰ
كَلَّا إِنَّهَا تَذْكِرَةٌ
فَمَنْ شَاءَ ذَكَرَهُ
فِي صُحُفٍ مُكَرَّمَةٍ
مَرْفُوعَةٍ مُطَهَّرَةٍ
بِأَيْدِي سَفَرَةٍ
كِرَامٍ بَرَرَةٍ
قُتِلَ الْإِنْسَانُ مَا أَكْفَرَهُ
مِنْ أَيِّ شَيْءٍ خَلَقَهُ
مِنْ نُطْفَةٍ خَلَقَهُ فَقَدَّرَهُ
ثُمَّ السَّبِيلَ يَسَّرَهُ
ثُمَّ أَمَاتَهُ فَأَقْبَرَهُ
ثُمَّ إِذَا شَاءَ أَنْشَرَهُ
كَلَّا لَمَّا يَقْضِ مَا أَمَرَهُ
فَلْيَنْظُرِ الْإِنْسَانُ إِلَىٰ طَعَامِهِ
أَنَّا صَبَبْنَا الْمَاءَ صَبًّا
ثُمَّ شَقَقْنَا الْأَرْضَ شَقًّا
فَأَنْبَتْنَا فِيهَا حَبًّا
وَعِنَبًا وَقَضْبًا
وَزَيْتُونًا وَنَخْلًا
وَحَدَائِقَ غُلْبًا
وَفَاكِهَةً وَأَبًّا
مَتَاعًا لَكُمْ وَلِأَنْعَامِكُمْ
فَإِذَا جَاءَتِ الصَّاخَّةُ
يَوْمَ يَفِرُّ الْمَرْءُ مِنْ أَخِيهِ
وَأُمِّهِ وَأَبِيهِ
وَصَاحِبَتِهِ وَبَنِيهِ
لِكُلِّ امْرِئٍ مِنْهُمْ يَوْمَئِذٍ شَأْنٌ يُغْنِيهِ
وُجُوهٌ يَوْمَئِذٍ مُسْفِرَةٌ
ضَاحِكَةٌ مُسْتَبْشِرَةٌ
وَوُجُوهٌ يَوْمَئِذٍ عَلَيْهَا غَبَرَةٌ
تَرْهَقُهَا قَتَرَةٌ
أُولَٰئِكَ هُمُ الْكَفَرَةُ الْفَجَرَةُ""",
"81. At-Takwir": """إِذَا الشَّمْسُ كُوِّرَتْ
وَإِذَا النُّجُومُ انْكَدَرَتْ
وَإِذَا الْجِبَالُ سُيِّرَتْ
وَإِذَا الْعِشَارُ عُطِّلَتْ
وَإِذَا الْوُحُوشُ حُشِرَتْ
وَإِذَا الْبِحَارُ سُجِّرَتْ
وَإِذَا النُّفُوسُ زُوِّجَتْ
وَإِذَا الْمَوْءُودَةُ سُئِلَتْ
بِأَيِّ ذَنْبٍ قُتِلَتْ
وَإِذَا الصُّحُفُ نُشِرَتْ
وَإِذَا السَّمَاءُ كُشِطَتْ
وَإِذَا الْجَحِيمُ سُعِّرَتْ
وَإِذَا الْجَنَّةُ أُزْلِفَتْ
عَلِمَتْ نَفْسٌ مَا أَحْضَرَتْ
فَلَا أُقْسِمُ بِالْخُنَّسِ
الْجَوَارِ الْكُنَّسِ
وَاللَّيْلِ إِذَا عَسْعَسَ
وَالصُّبْحِ إِذَا تَنَفَّسَ
إِنَّهُ لَقَوْلُ رَسُولٍ كَرِيمٍ
ذِي قُوَّةٍ عِنْدَ ذِي الْعَرْشِ مَكِينٍ
مُطَاعٍ ثَمَّ أَمِينٍ
وَمَا صَاحِبُكُمْ بِمَجْنُونٍ
وَلَقَدْ رَآهُ بِالْأُفُقِ الْمُبِينِ
وَمَا هُوَ عَلَى الْغَيْبِ بِضَنِينٍ
وَمَا هُوَ بِقَوْلِ شَيْطَانٍ رَجِيمٍ
فَأَيْنَ تَذْهَبُونَ
إِنْ هُوَ إِلَّا ذِكْرٌ لِلْعَالَمِينَ
لِمَنْ شَاءَ مِنْكُمْ أَنْ يَسْتَقِيمَ
وَمَا تَشَاءُونَ إِلَّا أَنْ يَشَاءَ اللَّهُ رَبُّ الْعَالَمِينَ""",
"82. Al-Infitar": """إِذَا السَّمَاءُ انْفَطَرَتْ
وَإِذَا الْكَوَاكِبُ انْتَثَرَتْ
وَإِذَا الْبِحَارُ فُجِّرَتْ
وَإِذَا الْقُبُورُ بُعْثِرَتْ
عَلِمَتْ نَفْسٌ مَا قَدَّمَتْ وَأَخَّرَتْ
يَا أَيُّهَا الْإِنْسَانُ مَا غَرَّكَ بِرَبِّكَ الْكَرِيمِ
الَّذِي خَلَقَكَ فَسَوَّاكَ فَعَدَلَكَ
فِي أَيِّ صُورَةٍ مَا شَاءَ رَكَّبَكَ
كَلَّا بَلْ تُكَذِّبُونَ بِالدِّينِ
وَإِنَّ عَلَيْكُمْ لَحَافِظِينَ
كِرَامًا كَاتِبِينَ
يَعْلَمُونَ مَا تَفْعَلُونَ
إِنَّ الْأَبْرَارَ لَفِي نَعِيمٍ
وَإِنَّ الْفُجَّارَ لَفِي جَحِيمٍ
يَصْلَوْنَهَا يَوْمَ الدِّينِ
وَمَا هُمْ عَنْهَا بِغَائِبِينَ
وَمَا أَدْرَاكَ مَا يَوْمُ الدِّينِ
ثُمَّ مَا أَدْرَاكَ مَا يَوْمُ الدِّينِ
يَوْمَ لَا تَمْلِكُ نَفْسٌ لِنَفْسٍ شَيْئًا ۖ وَالْأَمْرُ يَوْمَئِذٍ لِلَّهِ""",
"83. Al-Mutaffifin": """وَيْلٌ لِلْمُطَفِّفِينَ
الَّذِينَ إِذَا اكْتَالُوا عَلَى النَّاسِ يَسْتَوْفُونَ
وَإِذَا كَالُوهُمْ أَوْ وَزَنُوهُمْ يُخْسِرُونَ
أَلَا يَظُنُّ أُولَٰئِكَ أَنَّهُمْ مَبْعُوثُونَ
لِيَوْمٍ عَظِيمٍ
يَوْمَ يَقُومُ النَّاسُ لِرَبِّ الْعَالَمِينَ
كَلَّا إِنَّ كِتَابَ الْفُجَّارِ لَفِي سِجِّينٍ
وَمَا أَدْرَاكَ مَا سِجِّينٌ
كِتَابٌ مَرْقُومٌ
وَيْلٌ يَوْمَئِذٍ لِلْمُكَذِّبِينَ
الَّذِينَ يُكَذِّبُونَ بِيَوْمِ الدِّينِ
وَمَا يُكَذِّبُ بِهِ إِلَّا كُلُّ مُعْتَدٍ أَثِيمٍ
إِذَا تُتْلَىٰ عَلَيْهِ آيَاتُنَا قَالَ أَسَاطِيرُ الْأَوَّلِينَ
كَلَّا ۖ بَلْ ۜ رَانَ عَلَىٰ قُلُوبِهِمْ مَا كَانُوا يَكْسِبُونَ
كَلَّا إِنَّهُمْ عَنْ رَبِّهِمْ يَوْمَئِذٍ لَمَحْجُوبُونَ
ثُمَّ إِنَّهُمْ لَصَالُو الْجَحِيمِ
ثُمَّ يُقَالُ هَٰذَا الَّذِي كُنْتُمْ بِهِ تُكَذِّبُونَ
كَلَّا إِنَّ كِتَابَ الْأَبْرَارِ لَفِي عِلِّيِّينَ
وَمَا أَدْرَاكَ مَا عِلِّيُّونَ
كِتَابٌ مَرْقُومٌ
يَشْهَدُهُ الْمُقَرَّبُونَ
إِنَّ الْأَبْرَارَ لَفِي نَعِيمٍ
عَلَى الْأَرَائِكِ يَنْظُرُونَ
تَعْرِفُ فِي وُجُوهِهِمْ نَضْرَةَ النَّعِيمِ
يُسْقَوْنَ مِنْ رَحِيقٍ مَخْتُومٍ
خِتَامُهُ مِسْكٌ ۚ وَفِي ذَٰلِكَ فَلْيَتَنَافَسِ الْمُتَنَافِسُونَ
وَمِزَاجُهُ مِنْ تَسْنِيمٍ
عَيْنًا يَشْرَبُ بِهَا الْمُقَرَّبُونَ
إِنَّ الَّذِينَ أَجْرَمُوا كَانُوا مِنَ الَّذِينَ آمَنُوا يَضْحَكُونَ
وَإِذَا مَرُّوا بِهِمْ يَتَغَامَزُونَ
وَإِذَا انْقَلَبُوا إِلَىٰ أَهْلِهِمُ انْقَلَبُوا فَكِهِينَ
وَإِذَا رَأَوْهُمْ قَالُوا إِنَّ هَٰؤُلَاءِ لَضَالُّونَ
وَمَا أُرْسِلُوا عَلَيْهِمْ حَافِظِينَ
فَالْيَوْمَ الَّذِينَ آمَنُوا مِنَ الْكُفَّارِ يَضْحَكُونَ
عَلَى الْأَرَائِكِ يَنْظُرُونَ
هَلْ ثُوِّبَ الْكُفَّارُ مَا كَانُوا يَفْعَلُونَ""",
"84. Al-Insyiqaq": """إِذَا السَّمَاءُ انْشَقَّتْ
وَأَذِنَتْ لِرَبِّهَا وَحُقَّتْ
وَإِذَا الْأَرْضُ مُدَّتْ
وَأَلْقَتْ مَا فِيهَا وَتَخَلَّتْ
وَأَذِنَتْ لِرَبِّهَا وَحُقَّتْ
يَا أَيُّهَا الْإِنْسَانُ إِنَّكَ كَادِحٌ إِلَىٰ رَبِّكَ كَدْحًا فَمُلَاقِيهِ
فَأَمَّا مَنْ أُوتِيَ كِتَابَهُ بِيَمِينِهِ
فَسَوْفَ يُحَاسَبُ حِسَابًا يَسِيرًا
وَيَنْقَلِبُ إِلَىٰ أَهْلِهِ مَسْرُورًا
وَأَمَّا مَنْ أُوتِيَ كِتَابَهُ وَرَاءَ ظَهْرِهِ
فَسَوْفَ يَدْعُو ثُبُورًا
وَيَصْلَىٰ سَعِيرًا
إِنَّهُ كَانَ فِي أَهْلِهِ مَسْرُورًا
إِنَّهُ ظَنَّ أَنْ لَنْ يَحُورَ
بَلَىٰ إِنَّ رَبَّهُ كَانَ بِهِ بَصِيرًا
فَلَا أُقْسِمُ بِالشَّفَقِ
وَاللَّيْلِ وَمَا وَسَقَ
وَالْقَمَرِ إِذَا اتَّسَقَ
لَتَرْكَبُنَّ طَبَقًا عَنْ طَبَقٍ
فَمَا لَهُمْ لَا يُؤْمِنُونَ
وَإِذَا قُرِئَ عَلَيْهِمُ الْقُرْآنُ لَا يَسْجُدُونَ
بَلِ الَّذِينَ كَفَرُوا يُكَذِّبُونَ
وَاللَّهُ أَعْلَمُ بِمَا يُوعُونَ
فَبَشِّرْهُمْ بِعَذَابٍ أَلِيمٍ
إِلَّا الَّذِينَ آمَنُوا وَعَمِلُوا الصَّالِحَاتِ لَهُمْ أَجْرٌ غَيْرُ مَمْنُونٍ""",
"85. Al-Buruj": """وَالسَّمَاءِ ذَاتِ الْبُرُوجِ
وَالْيَوْمِ الْمَوْعُودِ
وَشَاهِدٍ وَمَشْهُودٍ
قُتِلَ أَصْحَابُ الْأُخْدُودِ
النَّارِ ذَاتِ الْوَقُودِ
إِذْ هُمْ عَلَيْهَا قُعُودٌ
وَهُمْ عَلَىٰ مَا يَفْعَلُونَ بِالْمُؤْمِنِينَ شُهُودٌ
وَمَا نَقَمُوا مِنْهُمْ إِلَّا أَنْ يُؤْمِنُوا بِاللَّهِ الْعَزِيزِ الْحَمِيدِ
الَّذِي لَهُ مُلْكُ السَّمَاوَاتِ وَالْأَرْضِ ۚ وَاللَّهُ عَلَىٰ كُلِّ شَيْءٍ شَهِيدٌ
إِنَّ الَّذِينَ فَتَنُوا الْمُؤْمِنِينَ وَالْمُؤْمِنَاتِ ثُمَّ لَمْ يَتُوبُوا فَلَهُمْ عَذَابُ جَهَنَّمَ وَلَهُمْ عَذَابُ الْحَرِيقِ
إِنَّ الَّذِينَ آمَنُوا وَعَمِلُوا الصَّالِحَاتِ لَهُمْ جَنَّاتٌ تَجْرِي مِنْ تَحْتِهَا الْأَنْهَارُ ۚ ذَٰلِكَ الْفَوْزُ الْكَبِيرُ
إِنَّ بَطْشَ رَبِّكَ لَشَدِيدٌ
إِنَّهُ هُوَ يُبْدِئُ وَيُعِيدُ
وَهُوَ الْغَفُورُ الْوَدُودُ
ذُو الْعَرْشِ الْمَجِيدُ
فَعَّالٌ لِمَا يُرِيدُ
هَلْ أَتَاكَ حَدِيثُ الْجُنُودِ
فِرْعَوْنَ وَثَمُودَ
بَلِ الَّذِينَ كَفَرُوا فِي تَكْذِيبٍ
وَاللَّهُ مِنْ وَرَائِهِمْ مُحِيطٌ
بَلْ هُوَ قُرْآنٌ مَجِيدٌ
فِي لَوْحٍ مَحْفُوظٍ""",
"86. At-Tariq": """وَالسَّمَاءِ وَالطَّارِقِ
وَمَا أَدْرَاكَ مَا الطَّارِقُ
النَّجْمُ الثَّاقِبُ
إِنْ كُلُّ نَفْسٍ لَمَّا عَلَيْهَا حَافِظٌ
فَلْيَنْظُرِ الْإِنْسَانُ مِمَّ خُلِقَ
خُلِقَ مِنْ مَاءٍ دَافِقٍ
يَخْرُجُ مِنْ بَيْنِ الصُّلْبِ وَالتَّرَائِبِ
إِنَّهُ عَلَىٰ رَجْعِهِ لَقَادِرٌ
يَوْمَ تُبْلَى السَّرَائِرُ
فَمَا لَهُ مِنْ قُوَّةٍ وَلَا نَاصِرٍ
وَالسَّمَاءِ ذَاتِ الرَّجْعِ
وَالْأَرْضِ ذَاتِ الصَّدْعِ
إِنَّهُ لَقَوْلٌ فَصْلٌ
وَمَا هُوَ بِالْهَزْلِ
إِنَّهُمْ يَكِيدُونَ كَيْدًا
وَأَكِيدُ كَيْدًا
فَمَهِّلِ الْكَافِرِينَ أَمْهِلْهُمْ رُوَيْدًا""",
"87. Al-A'la": """سَبِّحِ اسْمَ رَبِّكَ الْأَعْلَى
الَّذِي خَلَقَ فَسَوَّىٰ
وَالَّذِي قَدَّرَ فَهَدَىٰ
وَالَّذِي أَخْرَجَ الْمَرْعَىٰ
فَجَعَلَهُ غُثَاءً أَحْوَىٰ
سَنُقْرِئُكَ فَلَا تَنْسَىٰ
إِلَّا مَا شَاءَ اللَّهُ ۚ إِنَّهُ يَعْلَمُ الْجَهْرَ وَمَا يَخْفَىٰ
وَنُيَسِّرُكَ لِلْيُسْرَىٰ
فَذَكِّرْ إِنْ نَفَعَتِ الذِّكْرَىٰ
سَيَذَّكَّرُ مَنْ يَخْشَىٰ
وَيَتَجَنَّبُهَا الْأَشْقَى
الَّذِي يَصْلَى النَّارَ الْكُبْرَىٰ
ثُمَّ لَا يَمُوتُ فِيهَا وَلَا يَحْيَىٰ
قَدْ أَفْلَحَ مَنْ تَزَكَّىٰ
وَذَكَرَ اسْمَ رَبِّهِ فَصَلَّىٰ
بَلْ تُؤْثِرُونَ الْحَيَاةَ الدُّنْيَا
وَالْآخِرَةُ خَيْرٌ وَأَبْقَىٰ
إِنَّ هَٰذَا لَفِي الصُّحُفِ الْأُولَىٰ
صُحُفِ إِبْرَاهِيمَ وَمُوسَىٰ""",
"88. Al-Ghasyiyah": """هَلْ أَتَاكَ حَدِيثُ الْغَاشِيَةِ
وُجُوهٌ يَوْمَئِذٍ خَاشِعَةٌ
عَامِلَةٌ نَاصِبَةٌ
تَصْلَىٰ نَارًا حَامِيَةً
تُسْقَىٰ مِنْ عَيْنٍ آنِيَةٍ
لَيْسَ لَهُمْ طَعَامٌ إِلَّا مِنْ ضَرِيعٍ
لَا يُسْمِنُ وَلَا يُغْنِي مِنْ جُوعٍ
وُجُوهٌ يَوْمَئِذٍ نَاعِمَةٌ
لِسَعْيِهَا رَاضِيَةٌ
فِي جَنَّةٍ عَالِيَةٍ
لَا تَسْمَعُ فِيهَا لَاغِيَةً
فِيهَا عَيْنٌ جَارِيَةٌ
فِيهَا سُرُرٌ مَرْفُوعَةٌ
وَأَكْوَابٌ مَوْضُوعَةٌ
وَنَمَارِقُ مَصْفُوفَةٌ
وَزَرَابِيُّ مَبْثُوثَةٌ
أَفَلَا يَنْظُرُونَ إِلَى الْإِبِلِ كَيْفَ خُلِقَتْ
وَإِلَى السَّمَاءِ كَيْفَ رُفِعَتْ
وَإِلَى الْجِبَالِ كَيْفَ نُصِبَتْ
وَإِلَى الْأَرْضِ كَيْفَ سُطِحَتْ
فَذَكِّرْ إِنَّمَا أَنْتَ مُذَكِّرٌ
لَسْتَ عَلَيْهِمْ بِمُصَيْطِرٍ
إِلَّا مَنْ تَوَلَّىٰ وَكَفَرَ
فَيُعَذِّبُهُ اللَّهُ الْعَذَابَ الْأَكْبَرَ
إِنَّ إِلَيْنَا إِيَابَهُمْ
ثُمَّ إِنَّ عَلَيْنَا حِسَابَهُمْ""",
"89. Al-Fajr": """وَالْفَجْرِ
وَلَيَالٍ عَشْرٍ
وَالشَّفْعِ وَالْوَتْرِ
وَاللَّيْلِ إِذَا يَسْرِ
هَلْ فِي ذَٰلِكَ قَسَمٌ لِذِي حِجْرٍ
أَلَمْ تَرَ كَيْفَ فَعَلَ رَبُّكَ بِعَادٍ
إِرَمَ ذَاتِ الْعِمَادِ
الَّتِي لَمْ يُخْلَقْ مِثْلُهَا فِي الْبِلَادِ
وَثَمُودَ الَّذِينَ جَابُوا الصَّخْرَ بِالْوَادِ
وَفِرْعَوْنَ ذِي الْأَوْتَادِ
الَّذِينَ طَغَوْا فِي الْبِلَادِ
فَأَكْثَرُوا فِيهَا الْفَسَادَ
فَصَبَّ عَلَيْهِمْ رَبُّكَ سَوْطَ عَذَابٍ
إِنَّ رَبَّكَ لَبِالْمِرْصَادِ
فَأَمَّا الْإِنْسَانُ إِذَا مَا ابْتَلَاهُ رَبُّهُ فَأَكْرَمَهُ وَنَعَّمَهُ فَيَقُولُ رَبِّي أَكْرَمَنِ
وَأَمَّا إِذَا مَا ابْتَلَاهُ فَقَدَرَ عَلَيْهِ رِزْقَهُ فَيَقُولُ رَبِّي أَهَانَنِ
كَلَّا ۖ بَلْ لَا تُكْرِمُونَ الْيَتِيمَ
وَلَا تَحَاضُّونَ عَلَىٰ طَعَامِ الْمِسْكِينِ
وَتَأْكُلُونَ التُّرَاثَ أَكْلًا لَمًّا
وَتُحِبُّونَ الْمَالَ حُبًّا جَمًّا
كَلَّا إِذَا دُكَّتِ الْأَرْضُ دَكًّا دَكًّا
وَجَاءَ رَبُّكَ وَالْمَلَكُ صَفًّا صَفًّا
وَجِيءَ يَوْمَئِذٍ بِجَهَنَّمَ ۚ يَوْمَئِذٍ يَتَذَكَّرُ الْإِنْسَانُ وَأَنَّىٰ لَهُ الذِّكْرَىٰ
يَقُولُ يَا لَيْتَنِي قَدَّمْتُ لِحَيَاتِي
فَيَوْمَئِذٍ لَا يُعَذِّبُ عَذَابَهُ أَحَدٌ
وَلَا يُوثِقُ وَثَاقَهُ أَحَدٌ
يَا أَيَّتُهَا النَّفْسُ الْمُطْمَئِنَّةُ
ارْجِعِي إِلَىٰ رَبِّكِ رَاضِيَةً مَرْضِيَّةً
فَادْخُلِي فِي عِبَادِي
وَادْخُلِي جَنَّتِي""",
"90. Al-Balad": """لَا أُقْسِمُ بِهَٰذَا الْبَلَدِ
وَأَنْتَ حِلٌّ بِهَٰذَا الْبَلَدِ
وَوَالِدٍ وَمَا وَلَدَ
لَقَدْ خَلَقْنَا الْإِنْسَانَ فِي كَبَدٍ
أَيَحْسَبُ أَنْ لَنْ يَقْدِرَ عَلَيْهِ أَحَدٌ
يَقُولُ أَهْلَكْتُ مَالًا لُبَدًا
أَيَحْسَبُ أَنْ لَمْ يَرَهُ أَحَدٌ
أَلَمْ نَجْعَلْ لَهُ عَيْنَيْنِ
وَلِسَانًا وَشَفَتَيْنِ
وَهَدَيْنَاهُ النَّجْدَيْنِ
فَلَا اقْتَحَمَ الْعَقَبَةَ
وَمَا أَدْرَاكَ مَا الْعَقَبَةُ
فَكُّ رَقَبَةٍ
أَوْ إِطْعَامٌ فِي يَوْمٍ ذِي مَسْغَبَةٍ
يَتِيمًا ذَا مَقْرَبَةٍ
أَوْ مِسْكِينًا ذَا مَتْرَبَةٍ
ثُمَّ كَانَ مِنَ الَّذِينَ آمَنُوا وَتَوَاصَوْا بِالصَّبْرِ وَتَوَاصَوْا بِالْمَرْحَمَةِ
أُولَٰئِكَ أَصْحَابُ الْمَيْمَنَةِ
وَالَّذِينَ كَفَرُوا بِآيَاتِنَا هُمْ أَصْحَابُ الْمَشْأَمَةِ
عَلَيْهِمْ نَارٌ مُؤْصَدَةٌ""",
"91. Asy-Syams": """وَالشَّمْسِ وَضُحَاهَا
وَالْقَمَرِ إِذَا تَلَاهَا
وَالنَّهَارِ إِذَا جَلَّاهَا
وَاللَّيْلِ إِذَا يَغْشَاهَا
وَالسَّمَاءِ وَمَا بَنَاهَا
وَالْأَرْضِ وَمَا طَحَاهَا
وَنَفْسٍ وَمَا سَوَّاهَا
فَأَلْهَمَهَا فُجُورَهَا وَتَقْوَاهَا
قَدْ أَفْلَحَ مَنْ زَكَّاهَا
وَقَدْ خَابَ مَنْ دَسَّاهَا
كَذَّبَتْ ثَمُودُ بِطَغْوَاهَا
إِذِ انْبَعَثَ أَشْقَاهَا
فَقَالَ لَهُمْ رَسُولُ اللَّهِ نَاقَةَ اللَّهِ وَسُقْيَاهَا
فَكَذَّبُوهُ فَعَقَرُوهَا فَدَمْدَمَ عَلَيْهِمْ رَبُّهُمْ بِذَنْبِهِمْ فَسَوَّاهَا
وَلَا يَخَافُ عُقْبَاهَا""",
"92. Al-Lail": """وَاللَّيْلِ إِذَا يَغْشَىٰ
وَالنَّهَارِ إِذَا تَجَلَّىٰ
وَمَا خَلَقَ الذَّكَرَ وَالْأُنْثَىٰ
إِنَّ سَعْيَكُمْ لَشَتَّىٰ
فَأَمَّا مَنْ أَعْطَىٰ وَاتَّقَىٰ
وَصَدَّقَ بِالْحُسْنَىٰ
فَسَنُيَسِّرُهُ لِلْيُسْرَىٰ
وَأَمَّا مَنْ بَخِلَ وَاسْتَغْنَىٰ
وَكَذَّبَ بِالْحُسْنَىٰ
فَسَنُيَسِّرُهُ لِلْعُسْرَىٰ
وَمَا يُغْنِي عَنْهُ مَالُهُ إِذَا تَرَدَّىٰ
إِنَّ عَلَيْنَا لَلْهُدَىٰ
وَإِنَّ لَنَا لَلْآخِرَةَ وَالْأُولَىٰ
فَأَنْذَرْتُكُمْ نَارًا تَلَظَّىٰ
لَا يَصْلَاهَا إِلَّا الْأَشْقَى
الَّذِي كَذَّبَ وَتَوَلَّىٰ
وَسَيُجَنَّبُهَا الْأَتْقَى
الَّذِي يُؤْتِي مَالَهُ يَتَزَكَّىٰ
وَمَا لِأَحَدٍ عِنْدَهُ مِنْ نِعْمَةٍ تُجْزَىٰ
إِلَّا ابْتِغَاءَ وَجْهِ رَبِّهِ الْأَعْلَىٰ
وَلَسَوْفَ يَرْضَىٰ""",
"93. Ad-Dhuha": """وَالضُّحَىٰ
وَاللَّيْلِ إِذَا سَجَىٰ
مَا وَدَّعَكَ رَبُّكَ وَمَا قَلَىٰ
وَلَلْآخِرَةُ خَيْرٌ لَكَ مِنَ الْأُولَىٰ
وَلَسَوْفَ يُعْطِيكَ رَبُّكَ فَتَرْضَىٰ
أَلَمْ يَجِدْكَ يَتِيمًا فَآوَىٰ
وَوَجَدَكَ ضَالًّا فَهَدَىٰ
وَوَجَدَكَ عَائِلًا فَأَغْنَىٰ
فَأَمَّا الْيَتِيمَ فَلَا تَقْهَرْ
وَأَمَّا السَّائِلَ فَلَا تَنْهَرْ
وَأَمَّا بِنِعْمَةِ رَبِّكَ فَحَدِّثْ""",
"94. Asy-Syarh": """أَلَمْ نَشْرَحْ لَكَ صَدْرَكَ
وَوَضَعْنَا عَنْكَ وِزْرَكَ
الَّذِي أَنْقَضَ ظَهْرَكَ
وَرَفَعْنَا لَكَ ذِكْرَكَ
فَإِنَّ مَعَ الْعُسْرِ يُسْرًا
إِنَّ مَعَ الْعُسْرِ يُسْرًا
فَإِذَا فَرَغْتَ فَانْصَبْ
وَإِلَىٰ رَبِّكَ فَارْغَبْ""",
"95. At-Tin": """وَالتِّينِ وَالزَّيْتُونِ
وَطُورِ سِينِينَ
وَهَٰذَا الْبَلَدِ الْأَمِينِ
لَقَدْ خَلَقْنَا الْإِنْسَانَ فِي أَحْسَنِ تَقْوِيمٍ
ثُمَّ رَدَدْنَاهُ أَسْفَلَ سَافِلِينَ
إِلَّا الَّذِينَ آمَنُوا وَعَمِلُوا الصَّالِحَاتِ فَلَهُمْ أَجْرٌ غَيْرُ مَمْنُونٍ
فَمَا يُكَذِّبُكَ بَعْدُ بِالدِّينِ
أَلَيْسَ اللَّهُ بِأَحْكَمِ الْحَاكِمِينَ""",
"96. Al-'Alaq": """اقْرَأْ بِاسْمِ رَبِّكَ الَّذِي خَلَقَ
خَلَقَ الْإِنْسَانَ مِنْ عَلَقٍ
اقْرَأْ وَرَبُّكَ الْأَكْرَمُ
الَّذِي عَلَّمَ بِالْقَلَمِ
عَلَّمَ الْإِنْسَانَ مَا لَمْ يَعْلَمْ
كَلَّا إِنَّ الْإِنْسَانَ لَيَطْغَىٰ
أَنْ رَآهُ اسْتَغْنَىٰ
إِنَّ إِلَىٰ رَبِّكَ الرُّجْعَىٰ
أَرَأَيْتَ الَّذِي يَنْهَىٰ
عَبْدًا إِذَا صَلَّىٰ
أَرَأَيْتَ إِنْ كَانَ عَلَى الْهُدَىٰ
أَوْ أَمَرَ بِالتَّقْوَىٰ
أَرَأَيْتَ إِنْ كَذَّبَ وَتَوَلَّىٰ
أَلَمْ يَعْلَمْ بِأَنَّ اللَّهَ يَرَىٰ
كَلَّا لَئِنْ لَمْ يَنْتَهِ لَنَسْفَعًا بِالنَّاصِيَةِ
نَاصِيَةٍ كَاذِبَةٍ خَاطِئَةٍ
فَلْيَدْعُ نَادِيَهُ
سَنَدْعُ الزَّبَانِيَةَ
كَلَّا لَا تُطِعْهُ وَاسْجُدْ وَاقْتَرِبْ""",
"97. Al-Qadr": """إِنَّا أَنْزَلْنَاهُ فِي لَيْلَةِ الْقَدْرِ
وَمَا أَدْرَاكَ مَا لَيْلَةُ الْقَدْرِ
لَيْلَةُ الْقَدْرِ خَيْرٌ مِنْ أَلْفِ شَهْرٍ
تَنَزَّلُ الْمَلَائِكَةُ وَالرُّوحُ فِيهَا بِإِذْنِ رَبِّهِمْ مِنْ كُلِّ أَمْرٍ
سَلَامٌ هِيَ حَتَّىٰ مَطْلَعِ الْفَجْرِ""",
"98. Al-Bayyinah": """لَمْ يَكُنِ الَّذِينَ كَفَرُوا مِنْ أَهْلِ الْكِتَابِ وَالْمُشْرِكِينَ مُنْفَكِّينَ حَتَّىٰ تَأْتِيَهُمُ الْبَيِّنَةُ
رَسُولٌ مِنَ اللَّهِ يَتْلُو صُحُفًا مُطَهَّرَةً
فِيهَا كُتُبٌ قَيِّمَةٌ
وَمَا تَفَرَّقَ الَّذِينَ أُوتُوا الْكِتَابَ إِلَّا مِنْ بَعْدِ مَا جَاءَتْهُمُ الْبَيِّنَةُ
وَمَا أُمِرُوا إِلَّا لِيَعْبُدُوا اللَّهَ مُخْلِصِينَ لَهُ الدِّينَ حُنَفَاءَ وَيُقِيمُوا الصَّلَاةَ وَيُؤْتُوا الزَّكَاةَ ۚ وَذَٰلِكَ دِينُ الْقَيِّمَةِ
إِنَّ الَّذِينَ كَفَرُوا مِنْ أَهْلِ الْكِتَابِ وَالْمُشْرِكِينَ فِي نَارِ جَهَنَّمَ خَالِدِينَ فِيهَا ۚ أُولَٰئِكَ هُمْ شَرُّ الْبَرِيَّةِ
إِنَّ الَّذِينَ آمَنُوا وَعَمِلُوا الصَّالِحَاتِ أُولَٰئِكَ هُمْ خَيْرُ الْبَرِيَّةِ
جَزَاؤُهُمْ عِنْدَ رَبِّهِمْ جَنَّاتُ عَدْنٍ تَجْرِي مِنْ تَحْتِهَا الْأَنْهَارُ خَالِدِينَ فِيهَا أَبَدًا ۖ رَضِيَ اللَّهُ عَنْهُمْ وَرَضُوا عَنْهُ ۚ ذَٰلِكَ لِمَنْ خَشِيَ رَبَّهُ""",
"99. Az-Zalzalah": """إِذَا زُلْزِلَتِ الْأَرْضُ زِلْزَالَهَا
وَأَخْرَجَتِ الْأَرْضُ أَثْقَالَهَا
وَقَالَ الْإِنْسَانُ مَا لَهَا
يَوْمَئِذٍ تُحَدِّثُ أَخْبَارَهَا
بِأَنَّ رَبَّكَ أَوْحَىٰ لَهَا
يَوْمَئِذٍ يَصْدُرُ النَّاسُ أَشْتَاتًا لِيُرَوْا أَعْمَالَهُمْ
فَمَنْ يَعْمَلْ مِثْقَالَ ذَرَّةٍ خَيْرًا يَرَهُ
وَمَنْ يَعْمَلْ مِثْقَالَ ذَرَّةٍ شَرًّا يَرَهُ""",
"100. Al-'Adiyat": """وَالْعَادِيَاتِ ضَبْحًا
فَالْمُورِيَاتِ قَدْحًا
فَالْمُغِيرَاتِ صُبْحًا
فَأَثَرْنَ بِهِ نَقْعًا
فَوَسَطْنَ بِهِ جَمْعًا
إِنَّ الْإِنْسَانَ لِرَبِّهِ لَكَنُودٌ
وَإِنَّهُ عَلَىٰ ذَٰلِكَ لَشَهِيدٌ
وَإِنَّهُ لِحُبِّ الْخَيْرِ لَشَدِيدٌ
أَفَلَا يَعْلَمُ إِذَا بُعْثِرَ مَا فِي الْقُبُورِ
وَحُصِّلَ مَا فِي الصُّدُورِ
إِنَّ رَبَّهُمْ بِهِمْ يَوْمَئِذٍ لَخَبِيرٌ""",
"101. Al-Qari'ah": """الْقَارِعَةُ
مَا الْقَارِعَةُ
وَمَا أَدْرَاكَ مَا الْقَارِعَةُ
يَوْمَ يَكُونُ النَّاسُ كَالْفَرَاشِ الْمَبْثُوثِ
وَتَكُونُ الْجِبَالُ كَالْعِهْنِ الْمَنْفُوشِ
فَأَمَّا مَنْ ثَقُلَتْ مَوَازِينُهُ
فَهُوَ فِي عِيشَةٍ رَاضِيَةٍ
وَأَمَّا مَنْ خَفَّتْ مَوَازِينُهُ
فَأُمُّهُ هَاوِيَةٌ
وَمَا أَدْرَاكَ مَا هِيَهْ
نَارٌ حَامِيَةٌ""",
"102. At-Takatsur": """أَلْهَاكُمُ التَّكَاثُرُ
حَتَّىٰ زُرْتُمُ الْمَقَابِرَ
كَلَّا سَوْفَ تَعْلَمُونَ
ثُمَّ كَلَّا سَوْفَ تَعْلَمُونَ
كَلَّا لَوْ تَعْلَمُونَ عِلْمَ الْيَقِينِ
لَتَرَوُنَّ الْجَحِيمَ
ثُمَّ لَتَرَوُنَّهَا عَيْنَ الْيَقِينِ
ثُمَّ لَتُسْأَلُنَّ يَوْمَئِذٍ عَنِ النَّعِيمِ""",
"103. Al-'Asr": """وَالْعَصْرِ
إِنَّ الْإِنْسَانَ لَفِي خُسْرٍ
إِلَّا الَّذِينَ آمَنُوا وَعَمِلُوا الصَّالِحَاتِ وَتَوَاصَوْا بِالْحَقِّ وَتَوَاصَوْا بِالصَّبْرِ""",
"104. Al-Humazah": """وَيْلٌ لِكُلِّ هُمَزَةٍ لُمَزَةٍ
الَّذِي جَمَعَ مَالًا وَعَدَّدَهُ
يَحْسَبُ أَنَّ مَالَهُ أَخْلَدَهُ
كَلَّا ۖ لَيُنْبَذَنَّ فِي الْحُطَمَةِ
وَمَا أَدْرَاكَ مَا الْحُطَمَةُ
نَارُ اللَّهِ الْمُوقَدَةُ
الَّتِي تَطَّلِعُ عَلَى الْأَفْئِدَةِ
إِنَّهَا عَلَيْهِمْ مُؤْصَدَةٌ
فِي عَمَدٍ مُمَدَّدَةٍ""",
"105. Al-Fil": """أَلَمْ تَرَ كَيْفَ فَعَلَ رَبُّكَ بِأَصْحَابِ الْفِيلِ
أَلَمْ يَجْعَلْ كَيْدَهُمْ فِي تَضْلِيلٍ
وَأَرْسَلَ عَلَيْهِمْ طَيْرًا أَبَابِيلَ
تَرْمِيهِمْ بِحِجَارَةٍ مِنْ سِجِّيلٍ
فَجَعَلَهُمْ كَعَصْفٍ مَأْكُولٍ""",
"106. Quraisy": """لِإِيلَافِ قُرَيْشٍ
إِيلَافِهِمْ رِحْلَةَ الشِّتَاءِ وَالصَّيْفِ
فَلْيَعْبُدُوا رَبَّ هَٰذَا الْبَيْتِ
الَّذِي أَطْعَمَهُمْ مِنْ جُوعٍ وَآمَنَهُمْ مِنْ خَوْفٍ""",
"107. Al-Ma'un": """أَرَأَيْتَ الَّذِي يُكَذِّبُ بِالدِّينِ
فَذَٰلِكَ الَّذِي يَدُعُّ الْيَتِيمَ
وَلَا يَحُضُّ عَلَىٰ طَعَامِ الْمِسْكِينِ
فَوَيْلٌ لِلْمُصَلِّينَ
الَّذِينَ هُمْ عَنْ صَلَاتِهِمْ سَاهُونَ
الَّذِينَ هُمْ يُرَاءُونَ
وَيَمْنَعُونَ الْمَاعُونَ""",
"108. Al-Kautsar": """إِنَّا أَعْطَيْنَاكَ الْكَوْثَرَ
فَصَلِّ لِرَبِّكَ وَانْحَرْ
إِنَّ شَانِئَكَ هُوَ الْأَبْتَرُ""",
"109. Al-Kafirun": """قُلْ يَا أَيُّهَا الْكَافِرُونَ
لَا أَعْبُدُ مَا تَعْبُدُونَ
وَلَا أَنْتُمْ عَابِدُونَ مَا أَعْبُدُ
وَلَا أَنَا عَابِدٌ مَا عَبَدْتُمْ
وَلَا أَنْتُمْ عَابِدُونَ مَا أَعْبُدُ
لَكُمْ دِينُكُمْ وَلِيَ دِينِ""",
"110. An-Nasr": """إِذَا جَاءَ نَصْرُ اللَّهِ وَالْفَتْحُ
وَرَأَيْتَ النَّاسَ يَدْخُلُونَ فِي دِينِ اللَّهِ أَفْوَاجًا
فَسَبِّحْ بِحَمْدِ رَبِّكَ وَاسْتَغْفِرْهُ ۚ إِنَّهُ كَانَ تَوَّابًا""",
"111. Al-Lahab": """تَبَّتْ يَدَا أَبِي لَهَبٍ وَتَبَّ
مَا أَغْنَىٰ عَنْهُ مَالُهُ وَمَا كَسَبَ
سَيَصْلَىٰ نَارًا ذَاتَ لَهَبٍ
وَامْرَأَتُهُ حَمَّالَةَ الْحَطَبِ
فِي جِيدِهَا حَبْلٌ مِنْ مَسَدٍ""",
"112. Al-Ikhlas": """قُلْ هُوَ اللَّهُ أَحَدٌ
اللَّهُ الصَّمَدُ
لَمْ يَلِدْ وَلَمْ يُولَدْ
وَلَمْ يَكُنْ لَهُ كُفُوًا أَحَدٌ""",
"113. Al-Falaq": """قُلْ أَعُوذُ بِرَبِّ الْفَلَقِ
مِنْ شَرِّ مَا خَلَقَ
وَمِنْ شَرِّ غَاسِقٍ إِذَا وَقَبَ
وَمِنْ شَرِّ النَّفَّاثَاتِ فِي الْعُقَدِ
وَمِنْ شَرِّ حَاسِدٍ إِذَا حَسَدَ""",
"114. An-Nas": """قُلْ أَعُوذُ بِرَبِّ النَّاسِ
مَلِكِ النَّاسِ
إِلَٰهِ النَّاسِ
مِنْ شَرِّ الْوَسْوَاسِ الْخَنَّاسِ
الَّذِي يُوَسْوِسُ فِي صُدُورِ النَّاسِ
مِنَ الْجِنَّةِ وَالنَّاسِ""",
}

from supabase import create_client

# Kredensial Supabase disimpan di Streamlit Cloud > App settings > Secrets.
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


# === FUNGSI SIMPAN KE SUPABASE ===
def simpan_siswa(nama, kelas, nis):
    return supabase.table("siswa").insert({"nama": nama, "kelas": kelas, "nis": nis}).execute()

def simpan_hasil_ujian(nama_siswa, kelas, materi, skor, jawaban=None):
    return supabase.table("hasil_ujian").insert({"nama_siswa": nama_siswa, "kelas": kelas, "materi": materi, "skor": skor, "jawaban": jawaban}).execute()

def simpan_aktivitas(nama_siswa, aktivitas):
    return supabase.table("riwayat_aktivitas").insert({"nama_siswa": nama_siswa, "aktivitas": aktivitas}).execute()

def simpan_nilai(nama_siswa, materi, nilai):
    return supabase.table("nilai_pembelajaran").insert({"nama_siswa": nama_siswa, "materi": materi, "nilai": nilai}).execute()

def simpan_bukti(nama_siswa, nama_file, link_file):
    return supabase.table("bukti_tugas").insert({"nama_siswa": nama_siswa, "nama_file": nama_file, "link_file": link_file}).execute()


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
import json
import re
import sqlite3
import pandas as pd
from urllib.request import Request, urlopen
from openai import OpenAI
try:
    from streamlit_autorefresh import st_autorefresh
except:
    st_autorefresh = None

st.set_page_config(page_title="QORI AI", page_icon="🕌", layout="wide")

# ===== WARNA TULISAN PUTIH TANPA MENGUBAH BENTUK KOTAK =====
st.markdown("""
<style>
h1, h2, h3, h4, p, span, label {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)


# ===== WARNA ANGKA DAN KARTU METRIK DASHBOARD =====
st.markdown("""
<style>
/* Angka metrik menjadi putih pekat */
[data-testid="stMetricValue"] {
    color: white !important;
    -webkit-text-fill-color: white !important;
    text-shadow: 2px 2px 4px black;
}
/* Label metrik menjadi putih pekat */
[data-testid="stMetricLabel"] {
    color: white !important;
    -webkit-text-fill-color: white !important;
}
/* Latar gelap transparan agar angka terbaca di atas foto */
[data-testid="stMetric"] {
    background-color: rgba(0, 0, 0, 0.6);
    padding: 10px;
    border-radius: 15px;
}
</style>
""", unsafe_allow_html=True)

# ===== PERBAIKI WARNA TULISAN DI KOTAK UPLOAD =====
st.markdown("""
<style>
[data-testid="stFileUploader"] {
    background-color: #FFFFFF !important;
    border: 2px solid #1A5C2A !important;
    border-radius: 12px !important;
    padding: 12px !important;
}
[data-testid="stFileUploader"] * { color: #000000 !important; }
[data-testid="stFileUploader"] small {
    color: #333333 !important;
    font-size: 14px !important;
}
[data-testid="stFileUploader"] button {
    background-color: #1A5C2A !important;
    color: #FFFFFF !important;
    border: none !important;
    font-weight: bold !important;
    font-size: 16px !important;
    padding: 8px 20px !important;
}
[data-testid="stFileUploaderDropzone"] {
    background-color: #FFFFFF !important;
    color: #000000 !important;
}
[data-testid="stFileUploaderDropzone"] span { color: #000000 !important; }
[data-testid="stAlert"] {
    background-color: #FFFFFF !important;
    border: 2px solid #1A5C2A !important;
    color: #000000 !important;
}
[data-testid="stAlert"] * {
    color: #000000 !important;
    font-weight: 900 !important;
}
/* Paksa warna teks pada kotak Mode Tahsin, terlepas dari tema Streamlit */
.qori-mode-tahsin,
.qori-mode-tahsin * {
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
    font-weight: 900 !important;
}
.qori-mode-tahsin {
    background: #FFFFFF !important;
    border: 3px solid #1A5C2A !important;
}
.qori-mode-tahsin p::selection {
    color: #000000 !important;
    background: #FFE082 !important;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=86400, show_spinner=False)
def ambil_ayat_surat_quran(nomor_surat):
    """Ambil teks Arab lengkap satu surat dari API Al-Quran Cloud dan cache 24 jam."""
    url = f"https://api.alquran.cloud/v1/surah/{int(nomor_surat)}"
    request = Request(url, headers={"User-Agent": "QORI-AI/1.0"})
    with urlopen(request, timeout=15) as response:
        payload = json.loads(response.read().decode("utf-8"))
    if payload.get("code") != 200 or not payload.get("data", {}).get("ayahs"):
        raise ValueError("Data ayat tidak tersedia dari layanan Al-Quran.")
    return payload["data"]["ayahs"]

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

def hapus_nilai_game_satu(nama):
    """Hapus seluruh nilai/percobaan game milik satu siswa dari database."""
    CONN.execute("DELETE FROM game_attempts WHERE nama=?", (nama,))
    CONN.execute("DELETE FROM game_scores WHERE nama=?", (nama,))
    CONN.commit()

def reset_semua_nilai_game():
    """Hapus seluruh nilai game dari database."""
    CONN.execute("DELETE FROM game_attempts")
    CONN.execute("DELETE FROM game_scores")
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
    "MUHAMAD SIDDIQ ASYHARI": "Dosen Pengampu",
    "SYAMSUL HADI": "Kepala MA Al-Barokah",
    "MUHAMAD RAIS": "Guru Pamong",
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
    "KAWILUJEUNGAN RASYIDA RAIHANUN": {"kategori": "Tahfidz", "level": "Tahfidz", "jk": "Perempuan"},
    "MIFTAHUL JANNAH": {"kategori": "Tahfidz", "level": "Tahfidz", "jk": "Perempuan"},
    "MUHAMAD AZHAM FATAHILAH": {"kategori": "Tahfidz", "level": "Tahfidz", "jk": "Laki-laki"},
    "ROSMALATI KHOLISHA": {"kategori": "Tahfidz", "level": "Tahfidz", "jk": "Perempuan"},
    "M. ARIF ZAKARIYA": {"kategori": "Tahfidz", "level": "Tahfidz", "jk": "Laki-laki"},
    "MOCHAMMAD ALKAHFI MUBAROK": {"kategori": "Tahfidz", "level": "Tahfidz", "jk": "Laki-laki"},
    "IMAM MANSYUR IBNU HULKARIM": {"kategori": "Tahfidz", "level": "Tahfidz", "jk": "Laki-laki"},
}

for k, v in [("login_nama",None),("login_role",None),("login_jabatan",None),("program",None),("kategori_pilih",None),("messages",[]),("siswa_pilih",None),("seed_acak",1),("soal_acak",None),("kunci_acak",None),("kat_acak",None),("waktu_mulai",None),("waktu_habis",False),("ujian_selesai",False),("hasil_ujian",None),("lihat_nilai",False),("lihat_nilai_game",False),("lihat_riwayat",False),("lihat_saran",False),("lihat_setoran",False),("lihat_baca",False),("lihat_video",True),("waktu_login",None),("sudah_catat_masuk",False),("jawaban_tersimpan",{}),("login_error",""),("login_error_time",0),("preview_tim_ujian",False),("preview_kategori_ujian",None),("game",None),("game_question",None),("game_feedback",""),("game_question_no",0)]:
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
    """Menampilkan tim penyusun dengan ukuran kotak mengikuti panjang nama."""
    st.markdown(
        "<h3 style='text-align:center;'>⭐ Tim Penyusun QORI AI</h3>",
        unsafe_allow_html=True
    )

    st.markdown("""
    <style>
    .kotak-tim {
        text-align: center;
        background-color: rgba(0,0,0,0.35);
        padding: 12px 16px;
        border-radius: 15px;
        border: 1.5px solid rgba(255,255,255,0.7);
        width: fit-content;
        max-width: 100%;
        margin: 0 auto;
        min-height: 78px;
        box-sizing: border-box;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .block-container p.nama-tim {
        color: white !important;
        font-weight: 900;
        margin: 0;
        white-space: nowrap;
        font-size: 15px;
        text-shadow: 1px 1px 3px black;
    }
    .block-container p.jabatan-tim {
        color: white !important;
        font-weight: 700;
        margin: 4px 0 0 0;
        font-size: 13px;
        text-shadow: 1px 1px 3px black;
    }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class='kotak-tim'>
            <p class='nama-tim'>Dr. Muhamad Siddiq Asyhari, M.Pd</p>
            <p class='jabatan-tim'>Dosen Pengampu</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='kotak-tim'>
            <p class='nama-tim'>Bapak Syamsul Hadi, S.Pd.I</p>
            <p class='jabatan-tim'>Kepala MA Al-Barokah</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class='kotak-tim'>
            <p class='nama-tim'>Bapak Muhamad Rais, S.Pd.I</p>
            <p class='jabatan-tim'>Guru Pamong</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        st.markdown("""
        <div class='kotak-tim'>
            <p class='nama-tim'>Kendar Sultoni</p>
            <p class='jabatan-tim'>Mahasiswa</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(
        "<div style='text-align:center; font-size:12px; margin-top:10px;'>"
        "QORI AI - Madrasah Aliyah Al-Barokah | "
        "Media Belajar Iqro, Tahsin &amp; Tahfidz"
        "</div>",
        unsafe_allow_html=True
    )

bg = get_base64("background.jpeg")
if bg:
    st.markdown(f"""<style>.stApp {{ background-image: url("data:image/jpeg;base64,{bg}") !important; background-size: cover !important; background-position: center !important; background-attachment: fixed !important; }} .stApp::before {{ content:""; position:fixed; top:0; left:0; right:0; bottom:0; background: rgba(0,0,0,0.55); z-index:0; pointer-events:none; }} .block-container {{ position:relative; z-index:1; padding-top:20px !important; max-width:900px !important; }} .block-container p, .block-container span, .block-container label, .block-container h2 {{ color:white !important; }} div[data-testid="stButton"] > button {{ background-color: rgba(255,255,255,0.25) !important; color:white !important; border:1.5px solid rgba(255,255,255,0.8) !important; font-weight:bold !important; font-size:17px !important; border-radius:12px !important; }} [data-testid="stChatMessage"] {{ background-color: rgba(10,35,25,0.97) !important; border:2px solid #F9D423 !important; border-radius:14px !important; }} [data-testid="stChatMessage"] p {{ color:#FFF !important; font-size:20px !important; line-height:2.0 !important; }} [data-testid="stAlert"] {{ background-color: #FFD6D6 !important; }} [data-testid="stAlert"] p, [data-testid="stAlert"] span, [data-testid="stAlert"] div {{ color: #000000 !important; }} </style>""", unsafe_allow_html=True)


# ===== PERBAIKAN LATAR CHAT DAN METRIK AGAR TIDAK TRANSPARAN =====
st.markdown("""
<style>
[data-testid="stChatMessage"] {
    background-color: #1A1A1A !important;
    border: 1px solid #C9A227 !important;
    border-radius: 15px !important;
}
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li,
[data-testid="stChatMessage"] span {
    color: white !important;
    opacity: 1 !important;
}
[data-testid="stMetric"] {
    background-color: #1A1A1A !important;
}
</style>
""", unsafe_allow_html=True)


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
                    st.session_state["program"] = "Tim"
                    st.session_state["kelas"] = "Tim"
                    tampil = NAMA_LENGKAP_TIM.get(nama_bersih, nama_bersih)
                else:
                    st.session_state["login_role"] = "siswa"
                    # Ambil program dari Supabase (tabel siswa, kolom nama dan program).
                    # Jika data belum ada/kosong atau koneksi gagal, gunakan kategori lokal
                    # agar siswa tetap bisa masuk tanpa mengubah password lama.
                    program_db = None
                    try:
                        hasil_siswa = (
                            supabase.table("siswa")
                            .select("program")
                            .eq("nama", nama_bersih)
                            .limit(1)
                            .execute()
                        )
                        cek = hasil_siswa.data or []
                        if cek:
                            program_db = cek[0].get("program")
                    except Exception as e:
                        st.warning(f"Program belum dapat dibaca dari Supabase; menggunakan data akun lokal. ({e})")
                    program_lokal = DATA_SISWA[nama_bersih].get(
                        "program", DATA_SISWA[nama_bersih].get("kategori", "Tahsin")
                    )
                    program_final = str(program_db or program_lokal or "Tahsin").strip().title()
                    if program_final not in ["Iqro", "Tahsin", "Tahfidz"]:
                        program_final = str(program_lokal or "Tahsin").strip().title()
                    st.session_state["program"] = program_final
                    # Kelas otomatis mengikuti program siswa dari Supabase.
                    st.session_state["kelas"] = program_final
                    st.session_state["login_jabatan"] = f"Siswa {program_final}"
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

# ===== PROGRAM AKUN =====
# Program siswa dibaca saat login dari Supabase kolom siswa.program.
# Jangan timpa lagi dengan kategori lokal di setiap rerun Streamlit.
# Tim tetap mendapat akses ke seluruh program.
if st.session_state.get("login_role") == "tim":
    st.session_state["program"] = "Tim"

program_saya = st.session_state.get("program", "Tahsin")
if not st.session_state.get("kelas"):
    st.session_state["kelas"] = program_saya

# ===== BANNER SELAMAT DATANG =====
if st.session_state["login_role"] == "siswa":
    kelas_login = DATA_SISWA.get(st.session_state["login_nama"], {}).get("kategori", "")
    teks_selamat = f"👤 Selamat datang, {st.session_state['login_nama']} | Kelas: {kelas_login}"
else:
    jabatan_tim = TIM_PENYUSUN.get(st.session_state["login_nama"], st.session_state.get("login_jabatan", ""))
    nama_tim = NAMA_LENGKAP_TIM.get(st.session_state["login_nama"], st.session_state["login_nama"])
    teks_selamat = f"👤 Selamat datang, {nama_tim} | {jabatan_tim}"
st.markdown(f"<div style='background-color: rgba(0,0,0,0.6); padding:10px; border-radius:10px; text-align:center; margin-top:10px;'><b style='color:white;'>{teks_selamat}</b></div>", unsafe_allow_html=True)

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
    # Untuk siswa, level dibuka berurutan: level berikutnya baru tersedia
    # setelah level sebelumnya selesai. Level yang sudah selesai tetap dapat diulang.
    if st.session_state.get("login_role") == "siswa":
        nama_progres = st.session_state.get("login_nama", "")
        kategori_progres = DATA_SISWA.get(nama_progres, {}).get("kategori", "")
        nama_game_progres = {"iqro": "Game Iqro'", "tahsin": "Game Tahsin", "tahfidz": "Game Tahfidz"}.get(game_key)
        level_tersimpan = set()
        if nama_game_progres and kategori_progres:
            level_tersimpan = {
                int(row[0]) for row in CONN.execute(
                    "SELECT DISTINCT level FROM game_attempts WHERE nama=? AND game=?",
                    (nama_progres, nama_game_progres)
                ).fetchall()
            }
        level_berikutnya = next((i for i in range(1, 7) if i not in level_tersimpan), 6)
        level_maksimal_dibuka = 6 if len(level_tersimpan) == 6 else level_berikutnya
        level_tersedia = [i for i in range(1, level_maksimal_dibuka + 1)]
        st.caption(f"Progres kamu: {len(level_tersimpan)} dari 6 tingkatan selesai. Selesaikan secara berurutan.")
    else:
        level_tersedia = list(range(1, 7))

    pilihan_level = [f"Level {i} – {LEVEL_GAME[i][0]}" for i in level_tersedia]
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
    if st.session_state.get("login_role") == "tim":
        st.info("👁️ Mode Preview Tim: soal dan pilihan jawaban sama seperti yang dilihat siswa. Skor hanya untuk pengecekan dan tidak disimpan ke nilai siswa.")

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
        if st.session_state.get("login_role") == "tim":
            st.success("✅ Preview 25 soal selesai. Nilai tidak disimpan ke Daftar Hasil Nilai siswa.")
        else:
            st.success("🎉 MasyaAllah! Kamu telah menyelesaikan 25 soal.")
        st.metric("Skor sesi ini", st.session_state.get("game_session_score", 0))
        st.write("Skor maksimal: 250 poin.")
        if st.session_state.get("login_role") == "siswa":
            st.success(f"Nilai kamu untuk sesi ini: {st.session_state.get('game_session_score', 0)} / 250")
            if st.button("📋 Lihat Nilai Saya", use_container_width=True, key="lihat_nilai_saya_setelah_game"):
                st.session_state["lihat_nilai_game"] = True
                st.session_state["game"] = None
                st.session_state["game_question"] = None
                st.rerun()
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
        st.session_state["program"] = None
        st.session_state["siswa_pilih"] = None
        st.session_state["preview_tim_ujian"] = False
        st.session_state["preview_kategori_ujian"] = None
        st.session_state["kategori_pilih"] = None
        st.session_state["lihat_nilai"] = False
        st.session_state["lihat_nilai_game"] = False
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


# PROGRAM GATE: PANEL GURU TAHSIN UNTUK TIM
if program_saya == "Tim":
    # ===== PENILAIAN GURU - BACA QUR'AN =====
    if st.session_state.get("login_role") == "tim" and st.session_state.get("siswa_pilih") is None:
        st.divider()
        st.header("👨‍🏫 Penilaian Bacaan Al-Qur'an")

        try:
            data_bacaan = (
                supabase.table("bacaan_quran")
                .select("*")
                .eq("status", "menunggu")
                .order("created_at", desc=True)
                .execute()
                .data
            )

            if not data_bacaan:
                st.info("Belum ada bacaan yang menunggu dinilai.")
            else:
                for row in data_bacaan:
                    with st.expander(
                        f"📌 {row.get('nama_siswa', '-')} - {row.get('kelas', '-')} - {row.get('surah', '-')}"
                    ):
                        st.write(f"**Ayat:** {row.get('ayat_text', '-')}")
                        st.write(f"Tanggal: {row.get('created_at', '-')}")
                        if row.get("audio_url"):
                            st.audio(row["audio_url"])

                        st.subheader("Rubrik Penilaian (1-4)")
                        st.caption("1=Kurang, 2=Cukup, 3=Baik, 4=Sangat Baik")
                        c1, c2, c3 = st.columns(3)
                        row_id = row.get("id")
                        with c1:
                            makhraj = st.number_input("1. Makhrajul Huruf", 1, 4, 3, key=f"makhraj_{row_id}")
                            sifat = st.number_input("2. Sifat Huruf", 1, 4, 3, key=f"sifat_{row_id}")
                        with c2:
                            tajwid = st.number_input("3. Hukum Tajwid", 1, 4, 3, key=f"tajwid_{row_id}")
                            harakat = st.number_input("4. Ketepatan Harakat", 1, 4, 3, key=f"harakat_{row_id}")
                        with c3:
                            lancar = st.number_input("5. Kelancaran", 1, 4, 3, key=f"lancar_{row_id}")
                            mad = st.number_input("6. Panjang Pendek (Mad)", 1, 4, 3, key=f"mad_{row_id}")

                        catatan = st.text_area(
                            "Catatan Guru",
                            key=f"catatan_{row_id}",
                            placeholder="Contoh: Huruf 'ain masih kurang jelas, mad thabi'i kurang panjang...",
                        )
                        total = round(
                            ((makhraj + sifat + tajwid + harakat + lancar + mad) / 24) * 100
                        )
                        st.metric("Total Nilai (otomatis)", f"{total} / 100")

                        if st.button("💾 Simpan Nilai", key=f"simpan_nilai_bacaan_{row_id}"):
                            supabase.table("nilai_bacaan").insert({
                                "bacaan_id": row_id,
                                "makhraj": makhraj,
                                "sifat_huruf": sifat,
                                "tajwid": tajwid,
                                "harakat": harakat,
                                "kelancaran": lancar,
                                "mad": mad,
                                "total_nilai": total,
                                "catatan_guru": catatan,
                            }).execute()
                            supabase.table("bacaan_quran").update(
                                {"status": "dinilai"}
                            ).eq("id", row_id).execute()
                            st.success("Nilai tersimpan!")
                            st.rerun()
        except Exception as e:
            st.error(f"Gagal ambil data penilaian bacaan: {e}")

# PROGRAM GATE: PANEL GURU TAHFIDZ UNTUK TIM
if program_saya == "Tim":
    # ===== MENU TAHFIDZ: PENILAIAN GURU / PENGUJI =====
    if st.session_state.get("login_role") == "tim" and st.session_state.get("siswa_pilih") is None:
        st.divider()
        st.header("📖 Penilaian Tahfidz Al-Qur'an")
        st.info("Penilaian dilakukan oleh guru/penguji. AI hanya dapat membantu transkrip awal.")

        st.subheader("1. Setoran yang Menunggu Penilaian")
        try:
            data_menunggu_tahfidz = (
                supabase.table("nilai_tahfidz")
                .select("*")
                .eq("status", "menunggu")
                .order("created_at", desc=True)
                .execute()
                .data
            )
        except Exception as e:
            st.error(f"Gagal mengambil data setoran tahfidz: {e}")
            data_menunggu_tahfidz = []

        if not data_menunggu_tahfidz:
            st.success("Tidak ada setoran tahfidz yang menunggu dinilai.")
        else:
            for row_tahfidz in data_menunggu_tahfidz:
                id_tahfidz = row_tahfidz.get("id")
                with st.expander(
                    f"{row_tahfidz.get('nama_siswa', '-')} - {row_tahfidz.get('surah', '-')} "
                    f"(Ayat {row_tahfidz.get('ayat_mulai', '-')}–{row_tahfidz.get('ayat_sampai', '-')})"
                ):
                    st.write(f"**Kelas:** {row_tahfidz.get('kelas', '-')}")
                    if row_tahfidz.get("audio_url"):
                        st.audio(row_tahfidz["audio_url"])

                    st.markdown("**Beri skor 1–4 untuk tiap aspek:**")
                    st.caption("1 = Kurang | 2 = Cukup | 3 = Baik | 4 = Sangat Baik")
                    k_tahfidz = str(id_tahfidz)
                    c1, c2, c3 = st.columns(3)
                    with c1:
                        kelancaran = st.selectbox("1. Kelancaran Hafalan", [1, 2, 3, 4], key=f"kel_tahfidz_{k_tahfidz}")
                        lafaz = st.selectbox("2. Ketepatan Lafaz Ayat", [1, 2, 3, 4], key=f"laf_tahfidz_{k_tahfidz}")
                    with c2:
                        urutan = st.selectbox("3. Ketepatan Urutan Ayat", [1, 2, 3, 4], key=f"urt_tahfidz_{k_tahfidz}")
                        makhraj = st.selectbox("4. Makharijul Huruf", [1, 2, 3, 4], key=f"mak_tahfidz_{k_tahfidz}")
                    with c3:
                        tajwid = st.selectbox("5. Penerapan Tajwid", [1, 2, 3, 4], key=f"taj_tahfidz_{k_tahfidz}")
                        pertahankan = st.selectbox("6. Mempertahankan Hafalan", [1, 2, 3, 4], key=f"per_tahfidz_{k_tahfidz}")

                    catatan_tahfidz = st.text_area(
                        "Catatan Guru",
                        key=f"cat_tahfidz_{k_tahfidz}",
                        placeholder="Contoh: Makhraj huruf 'ain masih kurang jelas di ayat 3...",
                    )

                    if st.button("💾 Simpan Nilai Tahfidz", key=f"simpan_tahfidz_{k_tahfidz}"):
                        try:
                            total_tahfidz = (
                                kelancaran + lafaz + urutan + makhraj + tajwid + pertahankan
                            )
                            nilai_tahfidz = round((total_tahfidz / 24) * 100, 1)

                            if nilai_tahfidz >= 90:
                                predikat_tahfidz = "Mumtaz (Istimewa)"
                            elif nilai_tahfidz >= 80:
                                predikat_tahfidz = "Jayyid Jiddan (Sangat Baik)"
                            elif nilai_tahfidz >= 70:
                                predikat_tahfidz = "Jayyid (Baik)"
                            elif nilai_tahfidz >= 60:
                                predikat_tahfidz = "Maqbul (Cukup)"
                            else:
                                predikat_tahfidz = "Perlu Bimbingan / Mengulang"

                            supabase.table("nilai_tahfidz").update({
                                "kelancaran": kelancaran,
                                "lafaz_ayat": lafaz,
                                "urutan_ayat": urutan,
                                "makhraj": makhraj,
                                "tajwid": tajwid,
                                "mempertahankan_hafalan": pertahankan,
                                "total_skor": total_tahfidz,
                                "nilai_akhir": nilai_tahfidz,
                                "predikat": predikat_tahfidz,
                                "catatan_guru": catatan_tahfidz,
                                "dinilai_oleh": st.session_state.get("login_nama"),
                                "status": "dinilai",
                            }).eq("id", id_tahfidz).execute()

                            st.success(f"Tersimpan! Nilai: {nilai_tahfidz} - {predikat_tahfidz}")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Gagal menyimpan nilai tahfidz: {e}")

        st.subheader("2. Riwayat Nilai Tahfidz")
        try:
            riwayat_nilai_tahfidz = (
                supabase.table("nilai_tahfidz")
                .select("*")
                .eq("status", "dinilai")
                .order("created_at", desc=True)
                .limit(30)
                .execute()
                .data
            )
            if riwayat_nilai_tahfidz:
                for r_tahfidz in riwayat_nilai_tahfidz:
                    st.write(
                        f"**{r_tahfidz.get('nama_siswa', '-')}** | "
                        f"{r_tahfidz.get('surah', '-')} | "
                        f"Nilai: **{r_tahfidz.get('nilai_akhir', '-')}** "
                        f"({r_tahfidz.get('predikat', '-')}) | "
                        f"Catatan: {r_tahfidz.get('catatan_guru') or '-'}"
                    )
            else:
                st.info("Belum ada nilai tahfidz.")
        except Exception as e:
            st.error(f"Gagal mengambil riwayat nilai tahfidz: {e}")

# ===== MENU GAME QORI AI: KHUSUS SISWA =====
# Akun TIM tidak menampilkan baris Game QORI AI di bagian atas.
# TIM menggunakan menu kategori di Menu Utama bagian bawah.
role_login = st.session_state.get("login_role")
nama_login = st.session_state.get("login_nama", "")

# DATA_SISWA menjadi sumber kategori utama untuk seluruh akun siswa.
kategori_saya = DATA_SISWA.get(nama_login, {}).get("kategori") if role_login == "siswa" else None
if role_login == "siswa" and not st.session_state.get("lihat_nilai_game", False) and not st.session_state.get("lihat_nilai", False):
    st.markdown("### 🎮 Game QORI AI")
    st.session_state["kategori_saya"] = kategori_saya

    game_per_kategori = {
        "Iqro": ("iqro", "🔤 Game Iqro'", "📖 Iqro"),
        "Tahsin": ("tahsin", "📖 Game Tahsin", "📗 Tahsin"),
        "Tahfidz": ("tahfidz", "🧠 Game Tahfidz", "⭐ Tahfidz"),
    }
    konfigurasi_siswa = game_per_kategori.get(kategori_saya)

    if not konfigurasi_siswa:
        st.warning("Kategori akun siswa belum terdaftar. Silakan hubungi Tim QORI AI.")
    else:
        game_key_siswa, label_game_siswa, label_kategori_siswa = konfigurasi_siswa
        st.caption(f"Akses siswa dibatasi: hanya **Game {kategori_saya}** yang ditampilkan untuk akun kamu.")

        # Siswa hanya melihat game kategorinya sendiri dan daftar nilainya sendiri.
        tombol_game, tombol_nilai_game = st.columns(2)
        with tombol_game:
            if st.button(label_game_siswa, use_container_width=True, key="tombol_game_siswa_kategori"):
                st.session_state["game"] = game_key_siswa
                st.session_state["game_session_key"] = None
                st.session_state["game_index"] = 0
                st.session_state["game_question"] = None
                st.session_state["game_feedback"] = ""
                st.session_state["lihat_nilai_game"] = False
                st.session_state["lihat_nilai"] = False
                st.rerun()
        with tombol_nilai_game:
            if st.button("📋 Daftar Hasil Nilai Game", use_container_width=True, key="tombol_nilai_game_siswa"):
                st.session_state["lihat_nilai_game"] = True
                st.session_state["lihat_nilai"] = False
                st.session_state["kategori_pilih"] = None
                st.session_state["game"] = None
                st.session_state["game_question"] = None
                st.session_state["game_feedback"] = ""
                st.rerun()

# ===== DAFTAR HASIL NILAI GAME: REKAP PER LEVEL 1-6 =====
if st.session_state.get("lihat_nilai_game", False):
    role_nilai = st.session_state.get("login_role")
    nama_akun_nilai = st.session_state.get("login_nama", "")
    if role_nilai == "tim" or (role_nilai == "siswa" and nama_akun_nilai in DATA_SISWA):
        st.markdown("### 📋 Daftar Hasil Nilai Game")
        st.caption("Nilai setiap tingkatan tersimpan setelah siswa menyelesaikan 25 soal. Total merupakan penjumlahan nilai terbaik Level 1–6.")
        st.markdown("**KKM Game: 75** — nilai setiap tingkatan **di bawah 75 berwarna merah** (belum mencapai KKM), sedangkan nilai **75 ke atas berwarna hijau** (mencapai KKM).")

        konfigurasi_game = {
            "Iqro": "Game Iqro'",
            "Tahsin": "Game Tahsin",
            "Tahfidz": "Game Tahfidz",
        }
        rekap_game = {
            kategori: get_rekap_nilai_game(nama_game)
            for kategori, nama_game in konfigurasi_game.items()
        }

        if role_nilai == "tim":
            daftar_nilai_tampil = list(DATA_SISWA.items())
            st.caption("Mode Tim: menampilkan seluruh siswa dari kategori Iqro, Tahsin, dan Tahfidz.")
        else:
            # Siswa hanya dapat membaca rekam nilai milik akun yang sedang login.
            daftar_nilai_tampil = [(nama_akun_nilai, DATA_SISWA[nama_akun_nilai])]
            st.caption("Mode Siswa: hanya menampilkan nilai milik akun kamu sendiri.")

        # Filter daftar nilai game (khusus Tim); siswa tetap hanya melihat datanya sendiri.
        if role_nilai == "tim":
            kolom_cari_game, kolom_filter_game = st.columns(2)
            with kolom_cari_game:
                cari_nama_game = st.text_input("🔍 Cari Nama Siswa", key="cari_nama_daftar_game")
            with kolom_filter_game:
                pilih_kategori_game = st.selectbox(
                    "Filter Game",
                    ["Semua", "Game Iqro", "Game Tahsin", "Game Tahfidz"],
                    key="filter_kategori_daftar_game",
                )
            kategori_filter_map = {
                "Game Iqro": "Iqro",
                "Game Tahsin": "Tahsin",
                "Game Tahfidz": "Tahfidz",
            }
            if cari_nama_game.strip():
                daftar_nilai_tampil = [
                    item for item in daftar_nilai_tampil
                    if cari_nama_game.strip().casefold() in item[0].casefold()
                ]
            if pilih_kategori_game != "Semua":
                kategori_dicari = kategori_filter_map[pilih_kategori_game]
                daftar_nilai_tampil = [
                    item for item in daftar_nilai_tampil
                    if item[1].get("kategori") == kategori_dicari
                ]

        total_siswa_nilai = len(daftar_nilai_tampil)
        jumlah_belum = 0
        jumlah_tuntas = 0
        jumlah_belum_tuntas = 0
        data_tabel_nilai = []
        rows_nilai = ""

        for nomor, (nama_siswa, identitas) in enumerate(daftar_nilai_tampil, 1):
            kategori = identitas.get("kategori", "-")
            jenis_kelamin = identitas.get("jk", "-")
            hasil_siswa = rekap_game.get(kategori, {}).get(nama_siswa, {"level": {}})
            level_selesai = hasil_siswa.get("level", {})

            nilai_per_level = {}
            total_nilai = 0
            for level_nomor in range(1, 7):
                info_level = level_selesai.get(level_nomor)
                if info_level:
                    nilai_level = int(info_level.get("skor", 0))
                    nilai_per_level[level_nomor] = nilai_level
                    total_nilai += nilai_level
                else:
                    nilai_per_level[level_nomor] = "-"

            jumlah_level_selesai = sum(1 for v in nilai_per_level.values() if isinstance(v, int))
            if jumlah_level_selesai == 0:
                nilai_tampil = "-"
                keterangan = "⏳ Belum Mengerjakan"
                jumlah_belum += 1
            elif jumlah_level_selesai == 6:
                nilai_tampil = str(total_nilai)
                keterangan = "✅ Tuntas 6/6 Tingkatan"
                jumlah_tuntas += 1
            else:
                nilai_tampil = str(total_nilai)
                keterangan = f"🟡 Sudah {jumlah_level_selesai}/6 Tingkatan"
                jumlah_belum_tuntas += 1

            data_baris = {
                "No": nomor,
                "Nama": nama_siswa,
                "JK": jenis_kelamin,
                "Kategori": kategori,
                **{f"Level {i}": nilai_per_level[i] for i in range(1, 7)},
                "Total": nilai_tampil,
                "Ket": keterangan,
            }
            data_tabel_nilai.append(data_baris)

            sel_level = "".join(
                f"<td style='padding:9px;text-align:center;font-weight:bold;color:{('#FF5252' if nilai_per_level[i] < KKM else '#69F0AE') if isinstance(nilai_per_level[i], int) else '#BDBDBD'};border:1px solid #555;'>{nilai_per_level[i]}</td>"
                for i in range(1, 7)
            )
            rows_nilai += (
                f"<tr><td style='padding:9px;text-align:center;color:white;border:1px solid #555;'>{nomor}</td>"
                f"<td style='padding:9px;color:white;font-weight:bold;border:1px solid #555;'>{html.escape(nama_siswa)}</td>"
                f"<td style='padding:9px;text-align:center;color:white;border:1px solid #555;'>{html.escape(jenis_kelamin)}</td>"
                f"<td style='padding:9px;text-align:center;color:white;border:1px solid #555;'>{html.escape(kategori)}</td>"
                f"{sel_level}"
                f"<td style='padding:9px;text-align:center;color:#F9D423;font-weight:bold;border:1px solid #555;'>{nilai_tampil}</td>"
                f"<td style='padding:9px;text-align:center;color:white;border:1px solid #555;'>{keterangan}</td></tr>"
            )

        if role_nilai == "tim":
            st.markdown(
                f"<div style='text-align:center;font-weight:bold;font-size:16px;color:white;margin:8px 0 14px 0;'>"
                f"Total: {total_siswa_nilai} &nbsp;|&nbsp; ⏳ Belum: {jumlah_belum} &nbsp;|&nbsp; "
                f"✅ Tuntas 6/6: {jumlah_tuntas} &nbsp;|&nbsp; 🟡 Proses: {jumlah_belum_tuntas}</div>",
                unsafe_allow_html=True,
            )
        else:
            data_saya = data_tabel_nilai[0]
            level_saya_selesai = sum(1 for i in range(1, 7) if isinstance(data_saya[f"Level {i}"], int))
            st.markdown(
                f"<div style='text-align:center;font-weight:bold;font-size:18px;color:white;margin:8px 0 14px 0;'>"
                f"Total Nilai: {data_saya['Total']} &nbsp;|&nbsp; Sudah: {level_saya_selesai}/6 Tingkatan</div>",
                unsafe_allow_html=True,
            )

        st.markdown(
            "<div style='background-color:rgba(0,0,0,0.85);padding:0;border-radius:10px;overflow-x:auto;'>"
            "<table style='width:100%;border-collapse:collapse;min-width:1100px;'>"
            "<thead><tr style='background-color:#F9D423;'>"
            "<th style='padding:9px;color:#000;'>No</th><th style='padding:9px;color:#000;text-align:left;'>Nama</th>"
            "<th style='padding:9px;color:#000;'>JK</th><th style='padding:9px;color:#000;'>Kategori</th>"
            "<th style='padding:9px;color:#000;'>Tingkatan 1</th><th style='padding:9px;color:#000;'>Tingkatan 2</th>"
            "<th style='padding:9px;color:#000;'>Tingkatan 3</th><th style='padding:9px;color:#000;'>Tingkatan 4</th>"
            "<th style='padding:9px;color:#000;'>Tingkatan 5</th><th style='padding:9px;color:#000;'>Tingkatan 6</th>"
            "<th style='padding:9px;color:#000;'>Total</th><th style='padding:9px;color:#000;'>Ket</th>"
            f"</tr></thead><tbody>{rows_nilai}</tbody></table></div>",
            unsafe_allow_html=True,
        )
        st.caption("Keterangan warna: merah = nilai di bawah KKM 75; hijau = nilai 75 atau lebih; abu-abu = belum dikerjakan.")

        # Ekspor seluruh daftar nilai hanya tersedia bagi Tim.
        # Format XLSX menghindari masalah pemisah kolom CSV dan asosiasi aplikasi Word.
        if role_nilai == "tim":
            kolom_nilai_excel = [
                "No", "Nama", "JK", "Kategori", "Level 1", "Level 2",
                "Level 3", "Level 4", "Level 5", "Level 6", "Total", "Ket"
            ]
            df_tampil = pd.DataFrame(data_tabel_nilai, columns=kolom_nilai_excel)
            buffer_excel = io.BytesIO()
            with pd.ExcelWriter(buffer_excel, engine="openpyxl") as writer_excel:
                df_tampil.to_excel(writer_excel, index=False, sheet_name="Nilai Game")

            # Kotak 1 - Keterangan unduhan Game.
            st.markdown(
                "<p style='text-align:center; font-weight:bold;'>"
                "📥 Download Daftar Hasil Nilai Game (Excel)</p>",
                unsafe_allow_html=True,
            )

            # Kotak 2 - Tombol unduhan Game di tengah.
            col_game_kiri, col_game_tengah, col_game_kanan = st.columns([1, 1, 1])
            with col_game_tengah:
                st.download_button(
                    "⬇️ Download",
                    data=buffer_excel.getvalue(),
                    file_name="daftar_hasil_nilai_game_qori_ai.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True,
                    key="download_daftar_hasil_nilai_game_tim",
                )

            st.divider()
            st.markdown("## 🔄 Reset Nilai Game (Khusus Tim)")
            st.warning("Hati-hati! Nilai dan riwayat percobaan game yang direset tidak bisa dikembalikan.")

            st.markdown("**Reset nilai satu siswa:**")
            nama_reset_game = st.selectbox(
                "Pilih siswa yang nilainya mau dihapus:",
                ["-- Pilih Siswa --"] + sorted(DATA_SISWA.keys(), key=str.casefold),
                key="pilih_reset_satu_game",
            )
            if st.button("🗑️ Hapus Nilai Game Siswa Ini", use_container_width=True, key="hapus_nilai_game_satu"):
                if nama_reset_game == "-- Pilih Siswa --":
                    st.warning("Pilih dulu siswanya!")
                else:
                    hapus_nilai_game_satu(nama_reset_game)
                    st.success(f"Nilai Game {nama_reset_game} berhasil dihapus.")
                    time.sleep(0.5)
                    st.rerun()

            st.markdown("**Reset semua nilai game:**")
            konfirmasi_reset_game = st.text_input(
                "Ketik RESET untuk konfirmasi (huruf besar semua):",
                placeholder="Ketik RESET di sini...",
                key="konfirmasi_reset_semua_game",
            )
            if st.button("🗑️ Reset SEMUA Nilai Game", use_container_width=True, key="reset_semua_nilai_game"):
                if konfirmasi_reset_game.strip() != "RESET":
                    st.warning("Ketik RESET dengan huruf besar semua untuk melanjutkan.")
                else:
                    reset_semua_nilai_game()
                    st.success("Semua nilai game berhasil direset.")
                    time.sleep(0.5)
                    st.rerun()

        if st.button("❌ Tutup Daftar Nilai", key="tutup_daftar_nilai_game"):
            st.session_state["lihat_nilai_game"] = False
            st.rerun()

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
    """Siswa memulai ujian atas namanya sendiri; Tim hanya mendapat satu tombol preview."""
    role = st.session_state.get("login_role")

    if role == "siswa":
        nama_siswa = st.session_state.get("login_nama", "")
        if DATA_SISWA.get(nama_siswa, {}).get("kategori") != kategori:
            st.warning("Akses dibatasi: kategori ujian tidak sesuai dengan akun siswa.")
            return
        label = f"▶️ Mulai Ujian - {nama_siswa}"
        key_tombol = f"mulai_ujian_siswa_{kategori}_{nama_siswa}"
    elif role == "tim":
        # Tim tidak memilih nama siswa. Satu tombol membuka soal kategori terpilih.
        label = f"▶️ Mulai Ujian - Preview Tim ({kategori})"
        key_tombol = f"mulai_ujian_preview_tim_{kategori}"
    else:
        return

    if st.button(label, use_container_width=True, key=key_tombol):
        st.session_state["seed_acak"] += 1
        st.session_state["soal_acak"] = None
        st.session_state["kunci_acak"] = None
        st.session_state["kat_acak"] = None
        st.session_state["waktu_mulai"] = time.time()
        st.session_state["waktu_habis"] = False
        st.session_state["ujian_selesai"] = False
        st.session_state["hasil_ujian"] = None
        st.session_state["lihat_nilai"] = False
        st.session_state["lihat_riwayat"] = False
        st.session_state["lihat_saran"] = False
        st.session_state["lihat_setoran"] = False
        st.session_state["lihat_baca"] = False
        st.session_state["jawaban_tersimpan"] = {}

        if role == "tim":
            # Identitas sementara hanya untuk mengaktifkan layar ujian.
            # Tidak dibuat sesi SQLite dan tidak menyimpan nilai siswa.
            st.session_state["preview_tim_ujian"] = True
            st.session_state["preview_kategori_ujian"] = kategori
            st.session_state["siswa_pilih"] = f"__PREVIEW_TIM_{kategori.upper()}__"
            catat_aktivitas(f"Preview Ujian {kategori} oleh Tim")
        else:
            st.session_state["preview_tim_ujian"] = False
            st.session_state["preview_kategori_ujian"] = None
            st.session_state["siswa_pilih"] = st.session_state["login_nama"]
            simpan_sesi_ujian(st.session_state["siswa_pilih"], st.session_state["waktu_mulai"], st.session_state["seed_acak"])
            catat_aktivitas(f"Mulai Ujian - {kategori}")
        st.rerun()

# ===== MENU UTAMA: TIM SEMUA KATEGORI, SISWA SESUAI KATEGORI AKUN =====
if st.session_state["siswa_pilih"] is None and not st.session_state["lihat_nilai"] and not st.session_state.get("lihat_nilai_game", False):
    role_menu = st.session_state.get("login_role")
    nama_menu = st.session_state.get("login_nama", "")
    kategori_menu_siswa = DATA_SISWA.get(nama_menu, {}).get("kategori")

    if role_menu == "tim":
        # TIM memiliki dua menu yang berbeda:
        # Baris 1 = Game edukatif (bank soal game: huruf, tajwid, sambung ayat).
        # Baris 2 = Ujian akademik (bank soal ujian) dan daftar hasil nilai.
        st.markdown("### 🎮 Soal Game")
        g1, g2, g3, g4 = st.columns(4)
        with g1:
            klik_game_iqro = st.button(
                "🎮 Game Iqro", use_container_width=True, key="tim_game_iqro"
            )
        with g2:
            klik_game_tahsin = st.button(
                "🎮 Game Tahsin", use_container_width=True, key="tim_game_tahsin"
            )
        with g3:
            klik_game_tahfidz = st.button(
                "🎮 Game Tahfidz", use_container_width=True, key="tim_game_tahfidz"
            )
        with g4:
            klik_nilai_game = st.button(
                "📋 Daftar Hasil Nilai Game", use_container_width=True, key="tim_nilai_game"
            )

        game_tim_dipilih = (
            "iqro" if klik_game_iqro else
            "tahsin" if klik_game_tahsin else
            "tahfidz" if klik_game_tahfidz else None
        )
        if game_tim_dipilih:
            # Game memakai mesin dan bank soal game yang sama dengan siswa.
            # Role Tim otomatis menjadi preview; skor tidak disimpan ke nilai siswa.
            st.session_state["game"] = game_tim_dipilih
            st.session_state["game_session_key"] = None
            st.session_state["game_question"] = None
            st.session_state["game_questions"] = []
            st.session_state["game_index"] = 0
            st.session_state["game_feedback"] = ""
            st.session_state["game_session_score"] = 0
            st.session_state["kategori_pilih"] = None
            st.session_state["lihat_nilai_game"] = False
            st.session_state["lihat_nilai"] = False
            st.session_state["lihat_riwayat"] = False
            st.session_state["lihat_saran"] = False
            st.session_state["lihat_setoran"] = False
            st.session_state["lihat_baca"] = False
            st.rerun()

        if klik_nilai_game:
            st.session_state["lihat_nilai_game"] = True
            st.session_state["lihat_nilai"] = False
            st.session_state["game"] = None
            st.session_state["game_session_key"] = None
            st.session_state["kategori_pilih"] = None
            st.session_state["lihat_riwayat"] = False
            st.session_state["lihat_saran"] = False
            st.session_state["lihat_setoran"] = False
            st.session_state["lihat_baca"] = False
            catat_aktivitas("Buka Daftar Hasil Nilai Game")
            st.rerun()

        st.markdown("### 📝 Soal Ujian")
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            klik_iqro = st.button("📖 Iqro", use_container_width=True, key="menu_utama_iqro_tim")
        with m2:
            klik_tahsin = st.button("📗 Tahsin", use_container_width=True, key="menu_utama_tahsin_tim")
        with m3:
            klik_tahfidz = st.button("⭐ Tahfidz", use_container_width=True, key="menu_utama_tahfidz_tim")
        with m4:
            klik_nilai = st.button("📋 Daftar Hasil Nilai Ujian", use_container_width=True, key="menu_utama_nilai_tim")

        kategori_tim_dipilih = (
            "Iqro" if klik_iqro else
            "Tahsin" if klik_tahsin else
            "Tahfidz" if klik_tahfidz else None
        )
        if kategori_tim_dipilih:
            st.session_state["kategori_pilih"] = kategori_tim_dipilih
            st.session_state["game"] = None
            st.session_state["game_session_key"] = None
            st.session_state["lihat_nilai_game"] = False
            st.session_state["lihat_nilai"] = False
            st.session_state["lihat_riwayat"] = False
            st.session_state["lihat_saran"] = False
            st.session_state["lihat_setoran"] = False
            st.session_state["lihat_baca"] = False

        if klik_nilai:
            st.session_state["lihat_nilai"] = True
            st.session_state["lihat_nilai_game"] = False
            st.session_state["game"] = None
            st.session_state["game_session_key"] = None
            st.session_state["kategori_pilih"] = None
            st.session_state["lihat_riwayat"] = False
            st.session_state["lihat_saran"] = False
            st.session_state["lihat_setoran"] = False
            st.session_state["lihat_baca"] = False
            catat_aktivitas("Buka Daftar Hasil Nilai Ujian")
            st.rerun()

    else:
        # SISWA hanya melihat tombol kategori miliknya + Daftar Hasil Nilai.
        konfigurasi_menu = {
            "Iqro": ("📖 Iqro", "Iqro"),
            "Tahsin": ("📗 Tahsin", "Tahsin"),
            "Tahfidz": ("⭐ Tahfidz", "Tahfidz"),
        }
        if kategori_menu_siswa not in konfigurasi_menu:
            st.warning("Kategori akun belum terdaftar. Silakan hubungi Tim QORI AI.")
            klik_kategori_siswa = False
            klik_nilai = False
        else:
            label_menu_siswa, kategori_pilih_siswa = konfigurasi_menu[kategori_menu_siswa]
            s1, s2 = st.columns(2)
            with s1:
                klik_kategori_siswa = st.button(
                    label_menu_siswa,
                    use_container_width=True,
                    key="menu_utama_kategori_siswa",
                )
            with s2:
                klik_nilai = st.button(
                    "📋 Daftar Hasil Nilai Ujian",
                    use_container_width=True,
                    key="menu_utama_nilai_ujian_siswa",
                )

            if klik_kategori_siswa:
                st.session_state["kategori_pilih"] = (
                    None if st.session_state["kategori_pilih"] == kategori_pilih_siswa else kategori_pilih_siswa
                )
                st.session_state["lihat_nilai"] = False
                st.session_state["lihat_riwayat"] = False
                st.session_state["lihat_saran"] = False
                st.session_state["lihat_setoran"] = False
                st.session_state["lihat_baca"] = False
                catat_aktivitas(f"Buka Kelas {kategori_pilih_siswa}")

        if klik_nilai:
            st.session_state["lihat_nilai"] = True
            st.session_state["lihat_nilai_game"] = False
            st.session_state["game"] = None
            st.session_state["kategori_pilih"] = None
            st.session_state["lihat_riwayat"] = False
            st.session_state["lihat_saran"] = False
            st.session_state["lihat_setoran"] = False
            st.session_state["lihat_baca"] = False
            catat_aktivitas("Buka Daftar Hasil Nilai Ujian")

    # Siswa hanya dapat membuka kategori sendiri. Tim melihat satu tombol preview,
    # bukan daftar nama siswa.
    if st.session_state.get("kategori_pilih"):
        kategori_aktif = st.session_state["kategori_pilih"]
        if role_menu == "siswa" and kategori_aktif != kategori_menu_siswa:
            st.session_state["kategori_pilih"] = None
            st.warning("Akses dibatasi: kamu hanya dapat membuka kategori kelasmu sendiri.")
        else:
            tampilkan_daftar(kategori_aktif)

# PROGRAM GATE: HALAMAN SETOR TAHFIDZ UNTUK SISWA TAHFIDZ
if st.session_state.get("login_role") == "siswa" and program_saya == "Tahfidz" and st.session_state.get("siswa_pilih") is None:
    # ===== MENU TAHFIDZ: SETOR HAFALAN SISWA =====
    if st.session_state.get("login_role") == "siswa" and st.session_state.get("siswa_pilih") is None:
        st.divider()
        st.header("📖 Penilaian Tahfidz Al-Qur'an")
        st.info("Setoran dinilai oleh guru/penguji. AI tidak menetapkan nilai hafalan.")

        # ===== TAHFIDZ: TAMPILAN AYAT + BASMALAH + NEXT KHUSUS TAHFIDZ =====
        st.write("Setor hafalan kamu. Baca Basmalah terlebih dahulu, lalu coba hafalkan ayat yang ditampilkan.")
        surah_tahfidz = st.selectbox(
            "Pilih Surah (Juz 30) - Tahfidz",
            list(AYAT_JUZ30.keys()),
            key="surah_tahfidz",
        )

        if st.session_state.get("surah_aktif_tahfidz") != surah_tahfidz:
            st.session_state.surah_aktif_tahfidz = surah_tahfidz
            st.session_state.halaman_ayat_tahfidz = 0

        ayat_full_tahfidz = AYAT_JUZ30.get(surah_tahfidz, "")
        ayat_tahfidz = ""
        if ayat_full_tahfidz:
            baris_tahfidz = ayat_full_tahfidz.split("\n")
            PER_HALAMAN_TAHFIDZ = 5
            total_hal_tahfidz = (len(baris_tahfidz) + PER_HALAMAN_TAHFIDZ - 1) // PER_HALAMAN_TAHFIDZ
            hal_tahfidz = st.session_state.get("halaman_ayat_tahfidz", 0)
            hal_tahfidz = max(0, min(hal_tahfidz, total_hal_tahfidz - 1))
            mulai_tahfidz = hal_tahfidz * PER_HALAMAN_TAHFIDZ
            potongan_tahfidz = baris_tahfidz[mulai_tahfidz:mulai_tahfidz + PER_HALAMAN_TAHFIDZ]

            basmalah_html_tahfidz = (
                f"<div style='text-align:center; font-size:30px; margin-bottom:12px;'>{BASMALAH}</div>"
                if hal_tahfidz == 0 else ""
            )
            st.markdown(f"""
            <div style="background:white; color:#111; padding:20px; border-radius:12px;
                        text-align:right; font-size:28px; line-height:2.2; direction:rtl;">
                {basmalah_html_tahfidz}
                {'<br>'.join(potongan_tahfidz)}
            </div>
            <p style="text-align:center; color:grey;">Halaman {hal_tahfidz+1} dari {total_hal_tahfidz} •
            Ayat/baris {mulai_tahfidz+1} - {min(mulai_tahfidz+PER_HALAMAN_TAHFIDZ, len(baris_tahfidz))}</p>
            """, unsafe_allow_html=True)

            kolom_prev_tahfidz, kolom_kosong_tahfidz, kolom_next_tahfidz = st.columns([1, 1, 1])
            with kolom_prev_tahfidz:
                if st.button("⬅️ Sebelumnya", key="prev_tahfidz", disabled=(hal_tahfidz == 0)):
                    st.session_state.halaman_ayat_tahfidz = hal_tahfidz - 1
                    st.rerun()
            with kolom_next_tahfidz:
                if st.button("Selanjutnya ➡️", key="next_tahfidz", disabled=(hal_tahfidz >= total_hal_tahfidz - 1)):
                    st.session_state.halaman_ayat_tahfidz = hal_tahfidz + 1
                    st.rerun()

            ayat_tahfidz = "\n".join(potongan_tahfidz)
        else:
            ayat_tahfidz = st.text_area("Ayat Tahfidz", key="ayat_tahfidz_manual")

        with st.expander("1. Siswa: Setor Hafalan", expanded=False):
            with st.form("form_setor_tahfidz"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"Surah yang disetorkan: **{surah_tahfidz}**")
                    ayat_mulai = st.text_input("Dari Ayat", placeholder="Contoh: 1", key="ayat_mulai_tahfidz")
                with col2:
                    kelas_tahfidz = st.session_state.get("kelas", program_saya)
                    ayat_sampai = st.text_input("Sampai Ayat", placeholder="Contoh: 7", key="ayat_sampai_tahfidz")

                audio_tahfidz = st.file_uploader(
                    "Upload Rekaman Hafalan (mp3/wav/m4a)",
                    type=["mp3", "wav", "m4a"],
                    key="file_setor_tahfidz",
                )
                setor_tahfidz = st.form_submit_button("📤 Kirim Setoran")

            if setor_tahfidz:
                nama_login_tahfidz = st.session_state.get("login_nama", "")
                if not nama_login_tahfidz:
                    st.error("Nama akun siswa tidak ditemukan. Silakan masuk kembali.")
                elif not ayat_mulai.strip() or not ayat_sampai.strip():
                    st.error("Lengkapi ayat mulai dan ayat sampai.")
                elif audio_tahfidz is None:
                    st.error("Upload dulu rekaman hafalannya.")
                else:
                    try:
                        import uuid
                        ekstensi = audio_tahfidz.name.rsplit(".", 1)[-1].lower()
                        file_name = f"tahfidz_{uuid.uuid4().hex}.{ekstensi}"
                        tipe_konten = audio_tahfidz.type or {
                            "mp3": "audio/mpeg",
                            "wav": "audio/wav",
                            "m4a": "audio/mp4",
                        }.get(ekstensi, "application/octet-stream")

                        supabase.storage.from_("audio-bacaan").upload(
                            file_name,
                            audio_tahfidz.getvalue(),
                            {"content-type": tipe_konten, "upsert": "false"},
                        )
                        audio_url_tahfidz = supabase.storage.from_("audio-bacaan").get_public_url(file_name)

                        supabase.table("nilai_tahfidz").insert({
                            "nama_siswa": nama_login_tahfidz,
                            "kelas": kelas_tahfidz,
                            "surah": surah_tahfidz,
                            "ayat_mulai": ayat_mulai.strip(),
                            "ayat_sampai": ayat_sampai.strip(),
                            "audio_url": audio_url_tahfidz,
                            "status": "menunggu",
                        }).execute()
                        st.success("✅ Setoran terkirim! Menunggu penilaian guru.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Gagal mengirim setoran tahfidz: {e}")

        # Riwayat siswa hanya menampilkan setoran milik akun yang sedang masuk.
        st.subheader("2. Riwayat Setoran dan Nilai Tahfidz Saya")
        try:
            riwayat_siswa_tahfidz = (
                supabase.table("nilai_tahfidz")
                .select("*")
                .eq("nama_siswa", st.session_state.get("login_nama", ""))
                .order("created_at", desc=True)
                .limit(30)
                .execute()
                .data
            )
            if not riwayat_siswa_tahfidz:
                st.info("Belum ada riwayat setoran tahfidz.")
            else:
                for riwayat_row in riwayat_siswa_tahfidz:
                    label_riwayat = (
                        f"{riwayat_row.get('surah', '-')} | "
                        f"Ayat {riwayat_row.get('ayat_mulai', '-')}–{riwayat_row.get('ayat_sampai', '-')} | "
                        f"{riwayat_row.get('status', 'menunggu').capitalize()}"
                    )
                    with st.expander(label_riwayat):
                        st.write(f"Status: **{riwayat_row.get('status', 'menunggu')}**")
                        if riwayat_row.get("audio_url"):
                            st.audio(riwayat_row["audio_url"])
                        if riwayat_row.get("nilai_akhir") is not None:
                            st.metric("Nilai Akhir", riwayat_row.get("nilai_akhir"))
                            st.write(f"Predikat: **{riwayat_row.get('predikat', '-')}**")
                            st.write(f"Catatan guru: {riwayat_row.get('catatan_guru') or '-'}")
        except Exception as e:
            st.error(f"Gagal mengambil riwayat tahfidz: {e}")

# PROGRAM GATE: HALAMAN TES BACA TAHSIN UNTUK SISWA TAHSIN
if st.session_state.get("login_role") == "siswa" and program_saya == "Tahsin" and st.session_state.get("siswa_pilih") is None:
    # ===== TES BACA QUR'AN - SISWA =====
    if st.session_state.get("login_role") == "siswa" and st.session_state.get("siswa_pilih") is None:
        st.divider()
        st.header("🎙️ Tes Membaca Al-Qur'an")
        st.write("Bagian ini untuk penelitian PAI. Bacaan kamu akan dinilai guru.")

        nama_siswa_bacaan = st.session_state.get("login_nama") or st.text_input(
            "Nama Siswa", key="nama_bacaan"
        )
        # Kelas otomatis dari login, tidak perlu diisi lagi
        kelas_siswa_bacaan = st.session_state.get("kelas", "Tahsin")
        program_bacaan = st.session_state.get("program", "Tahsin")
        st.caption(f"Kelas: **{kelas_siswa_bacaan}** | Program: **{program_bacaan}**")
        # ===== DAFTAR SURAH JUZ 30 FULL (78-114) =====
        SURAH_JUZ30 = [
            "78. An-Naba'",
            "79. An-Nazi'at",
            "80. 'Abasa",
            "81. At-Takwir",
            "82. Al-Infitar",
            "83. Al-Mutaffifin",
            "84. Al-Insyiqaq",
            "85. Al-Buruj",
            "86. At-Tariq",
            "87. Al-A'la",
            "88. Al-Ghasyiyah",
            "89. Al-Fajr",
            "90. Al-Balad",
            "91. Asy-Syams",
            "92. Al-Lail",
            "93. Ad-Dhuha",
            "94. Asy-Syarh",
            "95. At-Tin",
            "96. Al-'Alaq",
            "97. Al-Qadr",
            "98. Al-Bayyinah",
            "99. Az-Zalzalah",
            "100. Al-'Adiyat",
            "101. Al-Qari'ah",
            "102. At-Takatsur",
            "103. Al-'Asr",
            "104. Al-Humazah",
            "105. Al-Fil",
            "106. Quraisy",
            "107. Al-Ma'un",
            "108. Al-Kautsar",
            "109. Al-Kafirun",
            "110. An-Nasr",
            "111. Al-Lahab",
            "112. Al-Ikhlas",
            "113. Al-Falaq",
            "114. An-Nas",
        ]

        surah_bacaan = st.selectbox(
            "Pilih Surah (Juz 30)", SURAH_JUZ30, key="surah_tes_bacaan"
        )
        # ===== AYAT DITAMPILKAN BESAR + NAVIGASI PER HALAMAN =====
        # Reset halaman setiap kali siswa mengganti surah.
        if st.session_state.get("surah_aktif_tes") != surah_bacaan:
            st.session_state.surah_aktif_tes = surah_bacaan
            st.session_state.halaman_ayat_tes = 0

        ayat_full = AYAT_JUZ30.get(surah_bacaan, "")
        if ayat_full:
            baris_ayat = ayat_full.split("\n")
            PER_HALAMAN = 5
            total_halaman = (len(baris_ayat) + PER_HALAMAN - 1) // PER_HALAMAN
            hal = st.session_state.get("halaman_ayat_tes", 0)
            hal = max(0, min(hal, total_halaman - 1))
            mulai = hal * PER_HALAMAN
            potongan = baris_ayat[mulai:mulai + PER_HALAMAN]

            if hal == 0:
                st.markdown(
                    f"<div dir='rtl' style='text-align:center; font-family:serif; "
                    f"font-size:25px; line-height:2; padding:8px 0 2px 0;'>"
                    f"{BASMALAH}</div>",
                    unsafe_allow_html=True,
                )

            st.markdown(
                f"<div dir='rtl' style='background:#fff; color:#111; padding:22px; "
                f"border-radius:14px; text-align:right; font-family:serif; "
                f"font-size:30px; line-height:2.2; margin:12px 0;'>"
                f"{'<br>'.join(potongan)}</div>",
                unsafe_allow_html=True,
            )
            st.caption(
                f"Halaman {hal + 1} dari {total_halaman} • "
                f"Ayat/baris {mulai + 1}–{min(mulai + PER_HALAMAN, len(baris_ayat))}"
            )

            # Tampilkan tombol navigasi hanya jika surah memiliki lebih dari satu halaman.
            if total_halaman > 1:
                kolom_sebelumnya, kolom_tengah, kolom_selanjutnya = st.columns([1, 1, 1])
                with kolom_sebelumnya:
                    if st.button("⬅️ Sebelumnya", disabled=(hal == 0), key="ayat_tes_sebelumnya"):
                        st.session_state.halaman_ayat_tes = hal - 1
                        st.rerun()
                with kolom_selanjutnya:
                    if st.button("Selanjutnya ➡️", disabled=(hal >= total_halaman - 1), key="ayat_tes_selanjutnya"):
                        st.session_state.halaman_ayat_tes = hal + 1
                        st.rerun()

            # Simpan teks halaman yang sedang ditampilkan bersama rekaman.
            ayat_bacaan = "\n".join(potongan)
        else:
            st.info("Ayat untuk surah ini belum diisi. Ketik manual di bawah:")
            ayat_bacaan = st.text_area(
                "Ayat yang dibaca",
                "",
                key=f"ayat_manual_tes_{SURAH_JUZ30.index(surah_bacaan)}",
            )

        st.info(
            "1. Klik tombol mikrofon di bawah\n"
            "2. Baca dengan tartil & jelas\n"
            "3. Klik Stop, lalu klik Kirim"
        )
        audio_bacaan = st.audio_input("Rekam Bacaan Kamu", key="audio_quran")

        if audio_bacaan is not None:
            st.audio(audio_bacaan)
            if st.button("📤 Kirim Bacaan ke Guru", key="kirim_bacaan"):
                if not nama_siswa_bacaan:
                    st.error("Nama siswa tidak ditemukan. Silakan masuk kembali.")
                else:
                    try:
                        waktu_nama = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
                        nama_aman = "".join(
                            c if c.isalnum() or c in ("-", "_") else "_"
                            for c in nama_siswa_bacaan.strip()
                        )
                        file_name = (
                            f"{nama_aman}_{waktu_nama}.wav"
                        )
                        supabase.storage.from_("audio-bacaan").upload(
                            file_name,
                            audio_bacaan.getvalue(),
                            {"content-type": "audio/wav", "upsert": "true"},
                        )
                        audio_url = supabase.storage.from_("audio-bacaan").get_public_url(file_name)

                        supabase.table("bacaan_quran").insert({
                            "nama_siswa": nama_siswa_bacaan,
                            "kelas": kelas_siswa_bacaan,
                            "surah": surah_bacaan,
                            "ayat_text": ayat_bacaan,
                            "audio_url": audio_url,
                            "status": "menunggu",
                        }).execute()

                        st.success("✅ Berhasil dikirim! Silakan tunggu penilaian guru.")
                        st.balloons()
                    except Exception as e:
                        st.error(f"Gagal kirim: {e}")

if st.session_state["login_role"]=="tim" and st.session_state["siswa_pilih"] is None:
    if st.button("📋 Riwayat / Story Siswa (Khusus Tim)", use_container_width=True):
        st.session_state["lihat_riwayat"]=True; st.session_state["kategori_pilih"]=None; st.session_state["lihat_nilai"]=False; st.session_state["lihat_saran"]=False; st.session_state["lihat_setoran"]=False; st.session_state["lihat_baca"]=False; st.rerun()
if st.session_state["siswa_pilih"] is None:
    jml_baru = len([s for s in get_saran() if not s["balasan"]]) if st.session_state["login_role"]=="tim" else len([s for s in get_saran() if s["pengirim"]==st.session_state["login_nama"] and s["balasan"]])
    label_saran = f"💬 Kotak Saran / Kritik / Keluhan ({jml_baru} Baru)" if jml_baru>0 else "💬 Kotak Saran / Kritik / Keluhan"
    if st.button(label_saran, use_container_width=True):
        st.session_state["lihat_saran"]=True; st.session_state["kategori_pilih"]=None; st.session_state["lihat_nilai"]=False; st.session_state["lihat_riwayat"]=False; st.session_state["lihat_setoran"]=False; st.session_state["lihat_baca"]=False; catat_aktivitas("Buka Kotak Saran"); st.rerun()
if st.session_state["siswa_pilih"] is None:
    jml_setoran_baru = len([s for s in get_setoran() if not s["koreksi"]]) if st.session_state["login_role"]=="tim" else len([s for s in get_setoran() if s["pengirim"]==st.session_state["login_nama"] and s["koreksi"]])
    if st.session_state.get("login_role") == "siswa":
        label_program_setoran = {
            "Iqro": "📗 Setoran Iqro",
            "Tahsin": "📖 Setoran Tahsin",
            "Tahfidz": "⭐ Setoran Tahfidz",
        }.get(program_saya, "🎙️ Setoran Saya")
        label_setoran = f"{label_program_setoran} ({jml_setoran_baru} Baru)" if jml_setoran_baru > 0 else label_program_setoran
    else:
        label_setoran = f"🎙️ Setoran / Penilaian Semua Program ({jml_setoran_baru} Baru)" if jml_setoran_baru > 0 else "🎙️ Setoran / Penilaian Semua Program"
    if st.button(label_setoran, use_container_width=True):
        st.session_state["lihat_setoran"]=True; st.session_state["kategori_pilih"]=None; st.session_state["lihat_nilai"]=False; st.session_state["lihat_riwayat"]=False; st.session_state["lihat_saran"]=False; st.session_state["lihat_baca"]=False; catat_aktivitas("Buka Setoran Suara"); st.rerun()

# ===== SETORAN SUARA - HANYA UPLOAD =====
if st.session_state.get("lihat_setoran") and st.session_state["siswa_pilih"] is None:
    st.markdown("<div style='background-color: rgba(20,50,35,0.95); padding:18px; border-radius:15px; text-align:center; border:2px solid #F9D423;'><h2 style='color:#F9D423; margin:0;'>🎙️ Setoran Suara / Koreksi Bacaan</h2><p style='color:white;'>Iqro | Tahsin | Tahfidz - Pilih Surat Juz 30 + Upload Suara</p></div>", unsafe_allow_html=True)
    st.write("")
    st.markdown("<p style='color:white; font-weight:bold; font-size:17px;'>📤 Kirim Setoran Baru:</p>", unsafe_allow_html=True)
    semua_program_setoran = ["Iqro", "Tahsin", "Tahfidz"]
    if st.session_state.get("login_role") == "siswa":
        # Siswa hanya dapat menyetor pada program akun miliknya sendiri.
        opsi_program_setoran = [program_saya] if program_saya in semua_program_setoran else ["Tahsin"]
    else:
        # Tim/Guru dapat memilih dan menilai seluruh program.
        opsi_program_setoran = semua_program_setoran
    kat_setoran = st.selectbox(
        "Kategori Setoran:",
        opsi_program_setoran,
        index=0,
        key="kat_setoran",
    )
    surat_juz30 = st.selectbox("📖 Pilih Surat Juz 30 (untuk setoran Tahsin / Tahfidz):", ["-- Ketik Sendiri / Bukan Juz 30 --"] + JUZ30_SURAH, key="surat_juz30")

    judul_setoran = st.text_input("Materi / Ayat / Judul Setoran:", placeholder="Contoh: Iqro 2 Hal. 5 atau keterangan tambahan setoran", key="judul_setoran")
    ket_setoran = st.text_area("Keterangan (opsional):", placeholder="Contoh: Mohon dikoreksi makhraj huruf... / Ayat yang ingin diperhatikan...", height=70, key="ket_setoran")

    # ===== BACAAN LENGKAP JUZ 30 UNTUK TAHSIN & TAHFIDZ =====
    # Iqro tetap menggunakan cara lama: isi halaman/materi secara manual, tanpa teks surat.
    bacaan_juz30_selesai = False
    teks_surat_berhasil_dimuat = False
    if kat_setoran in ("Tahsin", "Tahfidz"):
        if surat_juz30 == "-- Ketik Sendiri / Bukan Juz 30 --":
            st.info("Pilih surat Juz 30 terlebih dahulu. Teks Arab lengkap akan muncul otomatis untuk Tahsin dan Tahfidz.")
        else:
            # Perubahan pilihan surat oleh pengguna memulai sesi baca baru dari ayat pertama.
            if (st.session_state.get("setoran_surat_pilihan_terakhir") != surat_juz30
                    or st.session_state.get("setoran_kategori_terakhir") != kat_setoran):
                st.session_state["setoran_surat_pilihan_terakhir"] = surat_juz30
                st.session_state["setoran_kategori_terakhir"] = kat_setoran
                st.session_state["setoran_surat_mulai"] = surat_juz30
                st.session_state["setoran_surat_aktif"] = surat_juz30
                st.session_state["setoran_ayat_ke"] = 0
                st.session_state["setoran_juz30_selesai"] = False
                st.session_state["setoran_rentang_selesai"] = False

            if "setoran_surat_aktif" not in st.session_state:
                st.session_state["setoran_surat_aktif"] = surat_juz30
            if "setoran_ayat_ke" not in st.session_state:
                st.session_state["setoran_ayat_ke"] = 0
            if "setoran_juz30_selesai" not in st.session_state:
                st.session_state["setoran_juz30_selesai"] = False
            if "setoran_rentang_selesai" not in st.session_state:
                st.session_state["setoran_rentang_selesai"] = False

            bacaan_juz30_selesai = bool(st.session_state.get("setoran_juz30_selesai", False))
            if kat_setoran == "Tahsin":
                st.markdown("""
                <div class="qori-mode-tahsin" style="background:#FFFFFF !important; color:#000000 !important; padding:14px; border-radius:12px; border:3px solid #1A5C2A;">
                    <p style="color:#000000 !important; -webkit-text-fill-color:#000000 !important; font-size:17px; font-weight:900 !important; line-height:1.6; margin:0;">
                    📖 Mode Tahsin: baca ayat dengan memperhatikan makhraj, sifat huruf, panjang-pendek, dan hukum tajwid.
                    </p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info("🧠 Mode Tahfidz: baca dan hafalkan ayat secara bertahap. Gunakan tombol Next untuk melanjutkan.")

            if not bacaan_juz30_selesai:
                surat_aktif = st.session_state["setoran_surat_aktif"]
                try:
                    nomor_surat_aktif = int(re.search(r"\((\d+)\)", surat_aktif).group(1))
                    daftar_ayat = ambil_ayat_surat_quran(nomor_surat_aktif)
                    teks_surat_berhasil_dimuat = True
                except Exception as err:
                    daftar_ayat = []
                    st.error("Teks surat belum berhasil dimuat. Periksa koneksi internet lalu tekan tombol Muat Ulang Bacaan.")
                    if st.button("🔄 Muat Ulang Bacaan", key=f"muat_ulang_{st.session_state.get('setoran_surat_aktif','surat')}"):
                        ambil_ayat_surat_quran.clear()
                        st.rerun()

                if daftar_ayat:
                    mulai_ayat = int(st.session_state.get("setoran_ayat_ke", 0))
                    akhir_ayat = min(mulai_ayat + 5, len(daftar_ayat))
                    indeks_surat = JUZ30_SURAH.index(surat_aktif)
                    indeks_mulai = JUZ30_SURAH.index(st.session_state.get("setoran_surat_mulai", surat_juz30))
                    st.markdown(f"### 📖 {surat_aktif}")
                    st.caption(f"Surat {indeks_surat + 1} dari 37 dalam Juz 30 | Ayat {mulai_ayat + 1}–{akhir_ayat} dari {len(daftar_ayat)}")

                    for ayat in daftar_ayat[mulai_ayat:akhir_ayat]:
                        teks_arab = html.escape(str(ayat.get("text", "")))
                        nomor_ayat = ayat.get("numberInSurah", "")
                        st.markdown(
                            f"<div dir='rtl' style='text-align:right; font-family:serif; font-size:30px; line-height:2.1; background:#fff; color:#111; padding:18px; border-radius:12px; margin:10px 0;'>"
                            f"{teks_arab} <span style='font-size:19px; color:#9a7610;'>۞ {nomor_ayat}</span></div>",
                            unsafe_allow_html=True,
                        )

                    st.progress(min(akhir_ayat / max(len(daftar_ayat), 1), 1.0))
                    st.caption(f"Progress surat: {akhir_ayat}/{len(daftar_ayat)} ayat")

                    # ===== ALUR PER POTONG: BACA -> UPLOAD SUARA -> NEXT =====
                    # Setiap potongan berisi maksimal 5 ayat dan disimpan sebagai setoran tersendiri.
                    nama_pengguna = st.session_state.get("login_nama", "Siswa")
                    nama_key = re.sub(r"[^A-Za-z0-9_-]", "_", str(nama_pengguna))
                    kunci_potong = f"{nama_key}_{kat_setoran}_{nomor_surat_aktif}_{mulai_ayat}"
                    flag_upload = f"setoran_terunggah_{kunci_potong}"
                    rentang_ayat = f"Ayat {mulai_ayat + 1}-{akhir_ayat}"
                    judul_dasar_potong = f"{surat_aktif} - {rentang_ayat}"
                    judul_potong = judul_dasar_potong
                    if judul_setoran.strip():
                        judul_potong += f" - {judul_setoran.strip()}"
                    # Cek database juga, agar status upload tidak hilang setelah refresh/login ulang.
                    sudah_tersimpan_db = CONN.execute(
                        "SELECT 1 FROM setoran WHERE pengirim=? AND kategori=? AND judul LIKE ? LIMIT 1",
                        (nama_pengguna, kat_setoran, judul_dasar_potong + "%"),
                    ).fetchone() is not None
                    if sudah_tersimpan_db:
                        st.session_state[flag_upload] = True

                    if not st.session_state.get(flag_upload, False):
                        st.markdown("### 🎤 Langkah 1: Baca, lalu upload suara untuk potongan ini")
                        st.caption(f"Rekaman ini khusus untuk {surat_aktif}, {rentang_ayat}.")
                        # Satu-satunya kotak upload: gunakan uploader Streamlit langsung.
                        # Kotak HTML judul upload yang sebelumnya berada di atas dihapus
                        # agar tidak muncul dua kotak putih bertumpuk.
                        st.caption(f"File suara untuk {surat_aktif}, {rentang_ayat}.")
                        audio_potong = st.file_uploader(
                            "📥 Upload Suara Bacaan (maksimal 5 ayat):",
                            type=["mp3", "wav", "m4a", "ogg", "webm", "opus", "aac"],
                            key=f"uploader_potong_{kunci_potong}",
                        )
                        if audio_potong:
                            st.audio(audio_potong)
                            if st.button(
                                "✅ Simpan Suara Potongan Ini",
                                key=f"simpan_potong_{kunci_potong}",
                                use_container_width=True,
                            ):
                                if st.session_state.get("login_role") == "siswa":
                                    label_potong = f"{nama_pengguna} | Kelas: {DATA_SISWA.get(nama_pengguna, {}).get('kategori', kat_setoran)}"
                                else:
                                    label_potong = f"{NAMA_LENGKAP_TIM.get(nama_pengguna, nama_pengguna)} | {TIM_PENYUSUN.get(nama_pengguna, 'Tim')}"
                                tambah_setoran(
                                    nama_pengguna,
                                    label_potong,
                                    kat_setoran,
                                    judul_potong,
                                    ket_setoran.strip(),
                                    None,
                                    "",
                                    audio_potong.getvalue(),
                                    audio_potong.name,
                                    time.strftime("%d/%m/%Y %H:%M", time.localtime()),
                                )
                                catat_aktivitas(f"Kirim Setoran {kat_setoran} - {judul_potong}")
                                st.session_state[flag_upload] = True
                                st.success(f"Suara {rentang_ayat} berhasil disimpan ke Daftar Setoran.")
                                st.rerun()
                        st.info("⏳ Tombol Next akan terbuka setelah suara untuk potongan ini disimpan.")
                    else:
                        st.success(f"✅ Suara {rentang_ayat} sudah tersimpan di Daftar Setoran.")

                    b_prev, b_next = st.columns(2)
                    tombol_prev_disabled = (mulai_ayat == 0 and indeks_surat == indeks_mulai)
                    with b_prev:
                        if st.button("⬅️ Sebelumnya", key=f"prev_{nomor_surat_aktif}_{mulai_ayat}", use_container_width=True, disabled=tombol_prev_disabled):
                            if mulai_ayat >= 5:
                                st.session_state["setoran_ayat_ke"] = mulai_ayat - 5
                            elif indeks_surat > indeks_mulai:
                                surat_sebelumnya = JUZ30_SURAH[indeks_surat - 1]
                                nomor_sebelumnya = int(re.search(r"\((\d+)\)", surat_sebelumnya).group(1))
                                ayat_sebelumnya = ambil_ayat_surat_quran(nomor_sebelumnya)
                                st.session_state["setoran_surat_aktif"] = surat_sebelumnya
                                st.session_state["setoran_ayat_ke"] = ((len(ayat_sebelumnya) - 1) // 5) * 5
                            st.rerun()
                    with b_next:
                        if st.button(
                            "➡️ Next / Lanjut Bacaan" if st.session_state.get(flag_upload, False) else "🔒 Next / Upload Suara Dulu",
                            key=f"next_{nomor_surat_aktif}_{mulai_ayat}",
                            use_container_width=True,
                            disabled=not st.session_state.get(flag_upload, False),
                        ):
                            if akhir_ayat < len(daftar_ayat):
                                st.session_state["setoran_ayat_ke"] = akhir_ayat
                            elif indeks_surat + 1 < len(JUZ30_SURAH):
                                st.session_state["setoran_surat_aktif"] = JUZ30_SURAH[indeks_surat + 1]
                                st.session_state["setoran_ayat_ke"] = 0
                            else:
                                if st.session_state.get("setoran_surat_mulai") == JUZ30_SURAH[0]:
                                    st.session_state["setoran_juz30_selesai"] = True
                                else:
                                    st.session_state["setoran_rentang_selesai"] = True
                            st.rerun()

            if st.session_state.get("setoran_juz30_selesai", False):
                bacaan_juz30_selesai = True
                st.balloons()
                st.success("🎉 JUZ 30 SELESAI! Seluruh potongan suara dari An-Naba sampai An-Nas sudah dikirim satu per satu ke Daftar Setoran.")
            elif st.session_state.get("setoran_rentang_selesai", False):
                st.success("✅ Rangkaian bacaan dari surat yang dipilih sampai An-Nas selesai. Semua potongan suara sudah dikirim satu per satu ke Daftar Setoran.")

    # ===== IQRO: SETORAN PER HALAMAN =====
    if kat_setoran == "Iqro":
        iqro_level_pilih = st.selectbox("Pilih jilid:", list(IQRO_BACA.keys()), key="setoran_iqro_level")
        if st.session_state.get("setoran_iqro_level_terakhir") != iqro_level_pilih:
            st.session_state["setoran_iqro_level_terakhir"] = iqro_level_pilih
            st.session_state["setoran_iqro_halaman"] = 1
        if "setoran_iqro_halaman" not in st.session_state:
            st.session_state["setoran_iqro_halaman"] = 1
        halaman_iqro = int(st.session_state["setoran_iqro_halaman"])
        nama_pengguna_iqro = st.session_state.get("login_nama", "Siswa")
        nama_key_iqro = re.sub(r"[^A-Za-z0-9_-]", "_", str(nama_pengguna_iqro))
        kunci_iqro = f"{nama_key_iqro}_{iqro_level_pilih.replace(' ', '_')}_{halaman_iqro}"
        flag_iqro = f"setoran_iqro_terunggah_{kunci_iqro}"
        judul_iqro = f"{iqro_level_pilih} - Halaman {halaman_iqro}"
        sudah_iqro_db = CONN.execute(
            "SELECT 1 FROM setoran WHERE pengirim=? AND kategori='Iqro' AND judul LIKE ? LIMIT 1",
            (nama_pengguna_iqro, judul_iqro + "%"),
        ).fetchone() is not None
        if sudah_iqro_db:
            st.session_state[flag_iqro] = True
        st.markdown(f"### 📖 {judul_iqro}")
        st.info("Baca halaman yang sedang dipelajari dari buku Iqro, kemudian upload rekaman khusus halaman ini.")
        if not st.session_state.get(flag_iqro, False):
            st.markdown(
                f"<div style='background:#FFFFFF; padding:12px; border-radius:12px; border:2px solid #1A5C2A;'>"
                f"<p style='color:#000000; font-size:16px; font-weight:bold; margin:0;'>🎤 Upload Suara Bacaan Iqro:</p>"
                f"<p style='color:#333333; font-size:14px; margin:0;'>Pilih rekaman untuk {html.escape(judul_iqro)}.</p></div>",
                unsafe_allow_html=True,
            )
            audio_iqro = st.file_uploader(
                "Pilih file suara di sini:",
                type=["mp3", "wav", "m4a", "ogg", "webm", "opus", "aac"],
                key=f"uploader_{kunci_iqro}",
                label_visibility="collapsed",
            )
        else:
            audio_iqro = None
        if st.session_state.get(flag_iqro, False):
            st.success(f"✅ Rekaman {judul_iqro} sudah tersimpan di Daftar Setoran.")
        elif audio_iqro:
            st.audio(audio_iqro)
            if st.button("✅ Simpan Suara Halaman Ini", key=f"simpan_{kunci_iqro}", use_container_width=True):
                if st.session_state.get("login_role") == "siswa":
                    label_iqro = f"{nama_pengguna_iqro} | Kelas: {DATA_SISWA.get(nama_pengguna_iqro, {}).get('kategori', 'Iqro')}"
                else:
                    label_iqro = f"{NAMA_LENGKAP_TIM.get(nama_pengguna_iqro, nama_pengguna_iqro)} | {TIM_PENYUSUN.get(nama_pengguna_iqro, 'Tim')}"
                judul_simpan_iqro = judul_iqro + (f" - {judul_setoran.strip()}" if judul_setoran.strip() else "")
                tambah_setoran(
                    nama_pengguna_iqro, label_iqro, "Iqro", judul_simpan_iqro,
                    ket_setoran.strip(), None, "", audio_iqro.getvalue(), audio_iqro.name,
                    time.strftime("%d/%m/%Y %H:%M", time.localtime()),
                )
                catat_aktivitas(f"Kirim Setoran Iqro - {judul_simpan_iqro}")
                st.session_state[flag_iqro] = True
                st.success("Rekaman halaman Iqro berhasil disimpan.")
                st.rerun()
        if st.session_state.get(flag_iqro, False):
            if st.button("➡️ Next Halaman Iqro", key=f"next_{kunci_iqro}", use_container_width=True):
                st.session_state["setoran_iqro_halaman"] = halaman_iqro + 1
                st.rerun()
        else:
            st.info("⏳ Simpan suara halaman ini terlebih dahulu untuk membuka tombol Next Halaman.")

    # Untuk Tahsin/Tahfidz yang bukan bacaan Juz 30, tetap sediakan unggah manual.
    mode_setoran_manual = kat_setoran in ("Tahsin", "Tahfidz") and surat_juz30 == "-- Ketik Sendiri / Bukan Juz 30 --"
    boleh_upload_setoran = mode_setoran_manual
    audio_file = None
    if boleh_upload_setoran:
        # ===== KOTAK CARA KIRIM SUARA - TULISAN HITAM TEBAL =====
        st.markdown("""
        <div style='background:#FFD54F; padding:14px; border-radius:12px; border:3px solid #FF8F00;'>
        <p style='color:#000000 !important; font-size:17px; font-weight:900; margin:0 0 6px 0;'>🎤 Cara Kirim Suara di HP:</p>
        <p style='color:#000000 !important; font-size:15px; font-weight:700; line-height:1.6; margin:0;'>
        1. Rekam bacaan menggunakan Perekam HP atau Voice Note WA.<br>
        2. Upload file rekaman di bawah ini.<br>
        3. Dengarkan kembali sebelum dikirim.</p>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        # ===== SATU KOTAK: UPLOAD REKAM SUARA LANGSUNG KIRIM =====
        audio_file = st.file_uploader(
            "📥 Upload Rekam Suara Langsung Kirim:",
            type=["mp3", "wav", "m4a", "ogg", "webm", "opus", "aac"],
            key="audio_file_setoran"
        )
        if audio_file:
            st.success(f"✅ Suara terpilih: {audio_file.name} - Dengarkan dahulu sebelum dikirim.")
            st.audio(audio_file)

        if st.button("📩 Kirim Setoran ke Tim", use_container_width=True):
            judul_final = judul_setoran.strip()
            if mode_setoran_manual and not judul_final:
                judul_final = "Setoran non-Juz 30"
            if not judul_final:
                st.warning("⚠️ Isi materi / halaman Iqro yang disetorkan terlebih dahulu.")
            elif not audio_file:
                st.warning("⚠️ File suara belum diunggah. Rekam melalui WA / Perekam HP lalu upload di atas.")
            else:
                if st.session_state["login_role"]=="siswa":
                    label = f"{st.session_state['login_nama']} | Kelas: {DATA_SISWA.get(st.session_state['login_nama'],{}).get('kategori','-')}"
                else:
                    label = f"{NAMA_LENGKAP_TIM.get(st.session_state['login_nama'], st.session_state['login_nama'])} | {TIM_PENYUSUN.get(st.session_state['login_nama'],'Tim')}"
                audio_bytes = audio_file.getvalue(); audio_nama = audio_file.name
                # Setoran ini hanya memakai rekaman suara; foto tidak diminta.
                tambah_setoran(st.session_state["login_nama"], label, kat_setoran, judul_final, ket_setoran.strip(), None, "", audio_bytes, audio_nama, time.strftime("%d/%m/%Y %H:%M", time.localtime(time.time())))
                catat_aktivitas(f"Kirim Setoran {kat_setoran} - {judul_final[:30]}")
                st.success("✅ Setoran terkirim! Tim akan mendengarkan & mengoreksi.")
                time.sleep(0.5); st.rerun()
    elif surat_juz30 != "-- Ketik Sendiri / Bukan Juz 30 --":
        st.caption("Setoran Tahsin/Tahfidz Juz 30 dikirim per potongan maksimal 5 ayat. Upload suara potongan di bawah teks ayat, lalu tekan Next.")
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
                        warna_nilai = "#FF5252" if nilai_level < KKM else "#69F0AE"
                        isi_nilai = f"<span style='color:{warna_nilai};font-weight:bold;'>{nilai_level}/250</span><br><small>{info_level['percobaan']}x main</small>"
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
            st.caption("KKM Game: 75 — nilai di bawah 75 berwarna merah; nilai 75 ke atas berwarna hijau.")

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
    st.markdown("<div style='background-color: rgba(20,50,35,0.95); padding:18px; border-radius:15px; text-align:center; border:2px solid #F9D423;'><h2 style='color:#F9D423; margin:0;'>📊 Daftar Hasil Nilai Ujian</h2><p style='color:white;'>KKM = 75 | Nilai >= 75 = Tuntas | Nilai < 75 = Belum Tuntas</p></div>", unsafe_allow_html=True)
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
        # Siapkan data nilai ujian dalam format Excel (.xlsx).
        data_ujian_export = []
        for nama_export in daftar_tampil:
            info_export = DATA_SISWA[nama_export]
            nilai_export = hasil.get(nama_export)
            status_export = (
                "Tuntas" if nilai_export is not None and nilai_export >= KKM
                else ("Belum Tuntas" if nilai_export is not None else "Belum Ujian")
            )
            data_ujian_export.append({
                "Nama": nama_export,
                "Jenis Kelamin": info_export["jk"],
                "Kategori": info_export["kategori"],
                "Nilai": nilai_export if nilai_export is not None else "",
                "Status": status_export,
                "Jumlah Ujian": ulang.get(nama_export, 0),
            })

        df_ujian = pd.DataFrame(
            data_ujian_export,
            columns=["Nama", "Jenis Kelamin", "Kategori", "Nilai", "Status", "Jumlah Ujian"]
        )
        buffer_ujian = io.BytesIO()
        with pd.ExcelWriter(buffer_ujian, engine="openpyxl") as writer_ujian:
            df_ujian.to_excel(writer_ujian, index=False, sheet_name="Nilai Ujian")

        # Kotak 1 - Keterangan unduhan Ujian.
        st.markdown(
            "<p style='text-align:center; font-weight:bold;'>"
            "📥 Download Daftar Hasil Nilai Ujian (Excel)</p>",
            unsafe_allow_html=True,
        )

        # Kotak 2 - Tombol unduhan Ujian di tengah, sama seperti Game.
        col_ujian_kiri, col_ujian_tengah, col_ujian_kanan = st.columns([1, 1, 1])
        with col_ujian_tengah:
            st.download_button(
                "⬇️ Download",
                data=buffer_ujian.getvalue(),
                file_name="daftar_hasil_nilai_ujian_qori_ai.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
                key="download_daftar_hasil_nilai_ujian_tim",
            )
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
    if st.button("⬅️ Tutup Daftar Nilai Ujian", use_container_width=True):
        st.session_state["lihat_nilai"]=False; st.rerun()
    st.stop()

# ===== UJIAN =====
if st.session_state["siswa_pilih"]:
    nama = st.session_state["siswa_pilih"]
    preview_tim = bool(st.session_state.get("preview_tim_ujian")) and st.session_state.get("login_role") == "tim"

    if st.session_state["login_role"] == "siswa" and nama != st.session_state["login_nama"]:
        st.error("⛔ Kamu hanya boleh ujian atas nama sendiri!")
        if st.button("Kembali", key="kembali_akses_ujian"):
            st.session_state["siswa_pilih"] = None
            st.rerun()
        st.stop()

    if preview_tim:
        kat = st.session_state.get("preview_kategori_ujian", "Tahsin")
        nama_tampil = f"Preview Tim ({kat})"
    else:
        info = DATA_SISWA.get(nama, {"kategori": "Iqro", "level": "Pemula", "jk": "-"})
        kat = info["kategori"]
        nama_tampil = nama

    if st.session_state["waktu_mulai"] is None:
        if not preview_tim:
            sesi_tersimpan = ambil_sesi_ujian(nama)
        else:
            sesi_tersimpan = None
        if sesi_tersimpan:
            st.session_state["waktu_mulai"] = sesi_tersimpan[0]
            st.session_state["seed_acak"] = sesi_tersimpan[1]
        else:
            st.session_state["waktu_mulai"] = time.time()
            if not preview_tim:
                simpan_sesi_ujian(nama, st.session_state["waktu_mulai"], st.session_state["seed_acak"])
    sisa = DURASI_UJIAN - (time.time()-st.session_state["waktu_mulai"])
    if sisa<=0: sisa=0; st.session_state["waktu_habis"]=True
    if not st.session_state["ujian_selesai"] and st_autorefresh:
        st_autorefresh(interval=1000, key="timer_refresh")
    menit=int(sisa//60); detik=int(sisa%60)
    st.markdown(f"<div style='background-color: rgba(20,50,35,0.92); padding:20px; border-radius:15px; text-align:center;'><h2 style='color:#F9D423; margin:0;'>{'Preview Soal Tim' if preview_tim else 'Assalamualaikum, ' + nama_tampil} 👋</h2><p style='color:white;'>Kelas: {kat} | Soal: 25 | Nilai: Benar x 4 | Waktu: 10 Menit | KKM: 75 | Sisa: {menit:02d}:{detik:02d}</p></div>", unsafe_allow_html=True)
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
        st.session_state["ujian_selesai"] = True
        st.session_state["hasil_ujian"] = {"benar": benar, "nilai": nilai}
        if not preview_tim:
            simpan_hasil(nama, nilai)
            hapus_sesi_ujian(nama)
            catat_aktivitas(f"Selesai Ujian (Waktu Habis) - Nilai {nilai}")
        else:
            st.info("Mode Preview Tim: hasil percobaan ini tidak disimpan ke nilai siswa.")
        st.rerun()
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
            st.session_state["ujian_selesai"] = True
            st.session_state["hasil_ujian"] = {"benar": benar, "nilai": nilai}
            if not preview_tim:
                simpan_hasil(nama, nilai)
                hapus_sesi_ujian(nama)
                catat_aktivitas(f"Selesai Ujian - Nilai {nilai}")
            else:
                catat_aktivitas(f"Preview Ujian {kat} selesai oleh Tim (nilai tidak disimpan)")
            st.rerun()
    if st.session_state["ujian_selesai"] and st.session_state["hasil_ujian"]:
        h=st.session_state["hasil_ujian"]; benar=h["benar"]; nilai=h["nilai"]
        warna="#FF5252" if nilai<KKM else "#FFFFFF"
        st.success(f"🎉 {'HASIL PREVIEW TIM' if preview_tim else 'HASIL ' + nama} - Kelas {kat}")
        st.markdown(f"<div style='background-color: rgba(0,0,0,0.65); padding:15px; border-radius:10px; text-align:center;'><h1 style='color:{warna};'>Nilai: {nilai}</h1><p style='color:white;'>Benar: {benar} / 25 | KKM: 75 | {'❌ Belum Tuntas - Klik Remedial di bawah!' if nilai<KKM else '✅ Tuntas!'}</p><p style='color:white;'>Perhitungan: ({benar} ÷ 25) × 100 = {nilai}</p></div>", unsafe_allow_html=True)
        if nilai==100: st.balloons()
        st.markdown("<div style='background-color: rgba(0,0,0,0.65); padding:10px; border-radius:10px;'><p style='color:white; font-weight:bold;'>Pembahasan Kunci Jawaban:</p></div>", unsafe_allow_html=True)
        for i in range(25): st.markdown(f"<p style='color:white;'>No.{i+1} = {kunci[i]}</p>", unsafe_allow_html=True)
        col_r,col_k = st.columns(2)
        with col_r:
            if nilai < KKM:
                if st.button("🔁 Remedial - Ulangi Lagi", use_container_width=True):
                    for k in list(st.session_state.keys()):
                        if k.startswith("soal_"):
                            del st.session_state[k]
                    st.session_state["seed_acak"] += 1
                    st.session_state["soal_acak"] = None
                    st.session_state["kat_acak"] = None
                    st.session_state["waktu_mulai"] = time.time()
                    if not preview_tim:
                        simpan_sesi_ujian(nama, st.session_state["waktu_mulai"], st.session_state["seed_acak"])
                    st.session_state["waktu_habis"] = False
                    st.session_state["ujian_selesai"] = False
                    st.session_state["hasil_ujian"] = None
                    st.session_state["jawaban_tersimpan"] = {}
                    st.rerun()
        with col_k:
            if st.button("🏠 Kembali ke Beranda", use_container_width=True):
                if not preview_tim:
                    hapus_sesi_ujian(nama)
                st.session_state["siswa_pilih"] = None
                st.session_state["preview_tim_ujian"] = False
                st.session_state["preview_kategori_ujian"] = None
                st.session_state["soal_acak"] = None
                st.session_state["kunci_acak"] = None
                st.session_state["kat_acak"] = None
                st.session_state["waktu_mulai"] = None
                st.session_state["waktu_habis"] = False
                st.session_state["ujian_selesai"] = False
                st.session_state["hasil_ujian"] = None
                st.session_state["kategori_pilih"] = None
                st.session_state["jawaban_tersimpan"] = {}
                st.rerun()
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
            except Exception as e:
                st.error(f"Error asli: {e}")
