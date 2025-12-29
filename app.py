import streamlit as st
import assemblyai as aai
from pytube import YouTube
import os
import re

# Konfigurasi Halaman
st.set_page_config(page_title="YT Summarizer (Pytube)", page_icon="🎥")

def validate_url(url):
    """Cek apakah URL YouTube valid"""
    pattern = r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
    return re.match(pattern, url)

def download_audio_pytube(url):
    """Mengunduh audio menggunakan pytube"""
    yt = YouTube(url)
    # Ambil stream audio dengan bitrate terendah agar cepat (cukup untuk transkripsi)
    audio = yt.streams.filter(only_audio=True).first()
    # Download file
    out_file = audio.download(filename="audio_temp.mp4")
    # Ubah nama/ekstensi ke .m4a agar konsisten
    final_file = "audio_temp.m4a"
    if os.path.exists(final_file):
        os.remove(final_file)
    os.rename(out_file, final_file)
    return final_file

# --- UI ---
st.title("🎥 YouTube AI Summarizer")
st.caption("Versi Pytube - Lebih ringan untuk server cloud")

with st.sidebar:
    api_key = st.text_input("AssemblyAI API Key", type="password")
    st.info("Dapatkan kunci di [assemblyai.com](https://www.assemblyai.com)")

video_url = st.text_input("Tempel Link YouTube:", placeholder="https://www.youtube.com/watch?v=...")

if st.button("Proses Video ✨"):
    if not api_key or not video_url:
        st.error("API Key dan URL wajib diisi!")
    elif not validate_url(video_url):
        st.error("URL YouTube tidak valid!")
    else:
        audio_path = None
        try:
            with st.status("Sedang diproses...", expanded=True) as status:
                # 1. Download
                st.write("📥 Mengunduh audio (Pytube)...")
                audio_path = download_audio_pytube(video_url)
                
                # 2. Transcribe
                st.write("🎙️ Mentranskripsi dengan AssemblyAI...")
                aai.settings.api_key = api_key
                transcriber = aai.Transcriber()
                transcript = transcriber.transcribe(audio_path)
                
                if transcript.status == aai.TranscriptStatus.error:
                    st.error(f"Kesalahan: {transcript.error}")
                else:
                    # 3. Summarize
                    st.write("📝 Meringkas isi video...")
                    summary = transcript.lemur.summarize(
                        context="Buat ringkasan detail dalam Bahasa Indonesia dengan poin-poin penting."
                    )
                    
                    status.update(label="Selesai!", state="complete")
                    
                    st.subheader("📋 Ringkasan Video")
                    st.markdown(summary.response)
                    
                    with st.expander("Lihat Teks Transkrip"):
                        st.write(transcript.text)

        except Exception as e:
            st.error(f"Terjadi kesalahan: {str(e)}")
        
        finally:
            # Hapus file sampah
            if audio_path and os.path.exists(audio_path):
                os.remove(audio_path)
