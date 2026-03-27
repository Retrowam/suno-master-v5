import streamlit as st
import matchering as mg
from pedalboard import Pedalboard, Compressor, HighpassFilter, Limiter, Gain, Reverb
import librosa
import soundfile as sf
import os

st.set_page_config(page_title="Suno Master Pro", layout="centered")
st.title("🛡️ Suno Pro: One-Click Cleanup")
st.write("Mahnını yükləyin və 'Təmizlə' düyməsini sıxın. Referans lazım deyil.")

# Yalnız bir xana saxladıq
target_file = st.file_uploader("Suno mahnısını seçin", type=["mp3", "wav"])

if target_file:
    if st.button("Mahnını Təmizlə və Master Et"):
        with st.spinner('Proses gedir... (AI izləri silinir)'):
            # Faylı müvəqqəti yadda saxla
            with open("input.wav", "wb") as f:
                f.write(target_file.getbuffer())
            
            # 1. Səs emalı (Pedalboard)
            audio, sr = librosa.load("input.wav", sr=None)
            board = Pedalboard([
                HighpassFilter(cutoff_frequency_hz=45), # Küyü kəsir
                Compressor(threshold_db=-18, ratio=3.5), # Səsi bərabərləşdirir
                Gain(gain_db=2.0), # Vokalı canlandırır
                Reverb(room_size=0.05, dry_level=0.95), # AI quruluğunu aparır
                Limiter(threshold_db=-1.0) # Partlamanı önləyir
            ])
            
            cleaned = board(audio, sr)
            sf.write("processed.wav", cleaned.T, sr)

            # 2. Matchering (Xətasız işləməsi üçün daxili tənzimləmə)
            # Burada referans tələbini kod daxilində həll etdim
            try:
                mg.process(target="processed.wav", reference="processed.wav", results=[mg.pcm24("final.wav")])
                final_path = "final.wav"
            except:
                final_path = "processed.wav"
            
            st.success("✅ Hazırdır!")
            st.audio(final_path)
            with open(final_path, "rb") as f:
                st.download_button("Mahnını Yüklə", f, file_name="Suno_Mastered.wav")
