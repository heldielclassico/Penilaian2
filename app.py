from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline

def get_free_summary(video_id):
    # Ambil teks
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    text = " ".join([i['text'] for i in transcript])
    
    # Gunakan model summarization gratis
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    
    # Ringkas (membatasi input teks agar tidak overload)
    summary = summarizer(text[:1024], max_length=130, min_length=30, do_sample=False)
    return summary[0]['summary_text']
