import streamlit as st
import matchering as mg
import os
from pedalboard import Pedalboard, Compressor, HighpassFilter, LowpassFilter, Gain
from pedalboard.io import AudioFile
import librosa
import soundfile as sf

st.set_page_config(page_title="Suno Pro v5 Mastering", layout="wide")

st.title("🚀 Suno Pro v5: AI Cleanup & Mastering Studio")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    target = st.file_uploader("Suno mahnısını yükləyin (Mütləq)", type=["mp3", "wav"])
with col2:
    reference = st.file_uploader("Nümunə/Referans mahnı (İsteğe bağlı)", type=["mp3", "wav"])

if target:
    if st.button("Prosesi Başlat (Professional Mode)"):
        with st.spinner('AI izləri təmizlənir və referans tətbiq olunur...'):
            # Faylları müvəqqəti yadda saxlayırıq
            with open("temp_target.wav", "wb") as f: f.write(target.getbuffer())
            
            output_file = "Suno_Pro_Final_Master.wav"
            
            # 1. MƏRHƏLƏ: Section D üzrə AI təmizləmə (Pedalboard)
            input_audio, sr = librosa.load("temp_target.wav", sr=None)
            board = Pedalboard([
                HighpassFilter(cutoff_frequency_hz=40),
                LowpassFilter(cutoff_frequency_hz=16500),
                Compressor(threshold_db=-18, ratio=4),
                Gain(gain_db=2)
            ])
            cleaned_audio = board(input_audio, sr)
            sf.write("cleaned.wav", cleaned_audio.T, sr)

            # 2. MƏRHƏLƏ: Referans varsa Mastering
            if reference:
                with open("temp_ref.wav", "wb") as f: f.write(reference.getbuffer())
                mg.process(target="cleaned.wav", reference="temp_ref.wav", results=[mg.pcm24(output_file)])
            else:
                os.rename("cleaned.wav", output_file)

            st.success("✅ Mahnınız professional səviyyəyə gətirildi!")
            st.audio(output_file)
            with open(output_file, "rb") as f:
                st.download_button("Professional Mahnını Yüklə", f, file_name=output_file)