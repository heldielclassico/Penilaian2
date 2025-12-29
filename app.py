import assemblyai as aai

# 1. Konfigurasi API Key
# Dapatkan di https://www.assemblyai.com/dashboard
aai.settings.api_key = "f998640f0b7043a6b0f3e949cef8ffac"

def summarize_youtube_video(video_url):
    print(f"Sedang memproses video: {video_url}")
    
    # 2. Inisialisasi Transcriber
    transcriber = aai.Transcriber()

    # 3. Proses Transkripsi
    # AssemblyAI akan otomatis menggunakan yt-dlp untuk ambil audio dari YouTube
    transcript = transcriber.transcribe(video_url)

    if transcript.status == aai.TranscriptStatus.error:
        return f"Transkripsi Gagal: {transcript.error}"

    # 4. Membuat Ringkasan dengan LeMUR
    # Kita meminta AI untuk meringkas poin-poin penting
    prompt = "Berikan ringkasan singkat dalam bahasa Indonesia dari video ini, fokus pada poin-poin utama."
    
    result = transcript.lemur.summarize(
        context=prompt,
        answer_format="bullet points"
    )

    return {
        "text_lengkap": transcript.text,
        "ringkasan": result.response
    }

# --- Contoh Penggunaan ---
URL_VIDEO = "https://www.youtube.com/watch?v=zD_4R6-YV8Q" # Ganti dengan URL video Anda

hasil = summarize_youtube_video(URL_VIDEO)

if isinstance(hasil, dict):
    print("\n=== RINGKASAN VIDEO ===")
    print(hasil['ringkasan'])
    print("\n=== SEBAGIAN TEKS TRANSKRIP ===")
    print(hasil['text_lengkap'][:500] + "...") 
else:
    print(hasil)
