import streamlit as st
import traceback

st.set_page_config(page_title="QORI - Game Al-Barokah", layout="centered")

st.title("QORI - Game Al-Barokah")

try:
    import game_qori
    st.success("File game_qori.py ketemu!")

    if hasattr(game_qori, "main"):
        game_qori.main()
    elif hasattr(game_qori, "run"):
        game_qori.run()
    elif hasattr(game_qori, "app"):
        game_qori.app()
    else:
        st.warning("game_qori.py ketemu, tapi tidak ada fungsi main() / run() di dalamnya.")
        st.write("Isi file game_qori.py sekarang:")
        st.code(open("game_qori.py").read()[:3000])

except Exception as e:
    st.error(f"Error saat load game: {e}")
    st.code(traceback.format_exc())
