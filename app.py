import assemblyai as aai

aai.settings.api_key = "f998640f0b7043a6b0f3e949cef8ffac"
transcriber = aai.Transcriber()

# AssemblyAI bisa langsung menerima URL YouTube di beberapa versi SDK-nya
transcript = transcriber.transcribe("https://www.youtube.com/watch?v=example")
print(transcript.export_subtitles_vtt())

Buatkan requirments nya
