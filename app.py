import yt_dlp
import os

def download_audio(url):
    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'outtmpl': 'audio_temp.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
        }],
        # Header tambahan agar tidak terdeteksi bot
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return "audio_temp.m4a"

# --- Di dalam blok tombol 'Mulai Ringkas' ---
try:
    with st.status("Sedang memproses...", expanded=True) as status:
        st.write("Mengunduh audio dari YouTube secara manual...")
        audio_file = download_audio(video_url)
        
        st.write("Mengunggah dan mentranskripsi...")
        aai.settings.api_key = api_key
        transcriber = aai.Transcriber()
        
        # Kirim file lokal ke AssemblyAI, bukan URL YouTube langsung
        transcript = transcriber.transcribe(audio_file)
        
        # Hapus file setelah selesai agar hemat ruang
        if os.path.exists(audio_file):
            os.remove(audio_file)
