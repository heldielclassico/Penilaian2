import streamlit as st
from gensim.models import Word2Vec
from gensim.utils import simple_preprocess

# Judul Aplikasi
st.title("🤖 Gensim Word Similarity UI")
st.write("Masukkan beberapa kalimat untuk melatih model, lalu cari kata yang mirip.")

# Input Data dari Pengguna
text_input = st.text_area("Latih Model (Masukkan kalimat, satu per baris):", 
    "kucing mengejar tikus\nanjing suka bermain bola\ntikus lari dari kucing\nanjing dan kucing berteman")

if st.button("Latih Model"):
    # Preprocessing sederhana
    sentences = [simple_preprocess(line) for line in text_input.split('\n') if line]
    
    if len(sentences) > 0:
        # Train Model
        model = Word2Vec(sentences, vector_size=50, window=5, min_count=1, workers=4)
        st.session_state['model'] = model
        st.success("Model berhasil dilatih!")
    else:
        st.error("Masukkan teks terlebih dahulu.")

# Bagian Pencarian
if 'model' in st.session_state:
    st.divider()
    search_word = st.text_input("Cari kata yang mirip dengan:")
    
    if search_word:
        try:
            model = st.session_state['model']
            results = model.wv.most_similar(search_word.lower(), topn=5)
            
            st.write(f"Kata yang mirip dengan **{search_word}**:")
            for word, score in results:
                st.info(f"**{word}** (Skor Kemiripan: {score:.4f})")
        except KeyError:
            st.warning("Kata tidak ditemukan dalam data pelatihan.")
