if api_key:
    client = genai.Client(api_key=api_key)
    model = "gemini-2.5-flash"
if klik_iqro:
    if st.session_state["kategori_pilih"] == "Iqro":
        st.session_state["kategori_pilih"] = None
    else:
        st.session_state["kategori_pilih"] = "Iqro"

if klik_tahsin:
    if st.session_state["kategori_pilih"] == "Tahsin":
        st.session_state["kategori_pilih"] = None
    else:
        st.session_state["kategori_pilih"] = "Tahsin"

if klik_tahfidz:
    if st.session_state["kategori_pilih"] == "Tahfidz":
        st.session_state["kategori_pilih"] = None
    else:
        st.session_state["kategori_pilih"] = "Tahfidz"

# Tampilkan lurus di bawah tombolnya
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

prompt = st.chat_input("Tulis pertanyaanmu di sini...")
if prompt_awal:
    prompt = prompt_awal

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    with st.chat_message("assistant"):
        try:
response = client.models.generate_content(model=model, contents=f"Kamu adalah QORI AI, guru ngaji yang ramah untuk anak Madrasah Aliyah Al Barokah. Jawab dengan bahasa Indonesia yang mudah, sopan, dan islami. Pertanyaan: {prompt}")
            st.write(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.write("Maaf, sedang ada gangguan. Coba lagi ya.")

st.markdown("<p style='text-align:center; font-size:12px; margin-top:20px; background-color:white; padding:8px; border-radius:10px;'> QORI AI - Madrasah Aliyah Al Barokah ✨ خَيْرُكُمْ مَنْ تَعَلَّمَ الْقُرْآنَ وَعَلَّمَهُ ✨ Sebaik-baik kalian adalah yang belajar Al-Qur'an dan mengajarkannya</p>", unsafe_allow_html=True)
