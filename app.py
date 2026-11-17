def tanya_gemini(prompt):
    # Coba 3 nama model, mana yang jalan dipake
    for nama_model in ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{nama_model}:generateContent?key={API_KEY}"
            data = {"contents": [{"parts": [{"text": prompt}]}]}
            req = urllib.request.Request(url, data=json.dumps(data).encode("utf-8"), headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=60) as res:
                hasil = json.loads(res.read().decode("utf-8"))
            return hasil["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            # Kalau 404, coba model berikutnya
            if "404" in str(e):
                continue
            raise e
    raise Exception("Semua model Gemini lagi gak bisa diakses, coba lagi 1 menit ya!")
