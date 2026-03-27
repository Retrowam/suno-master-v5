import streamlit as st
import matchering as mg
from pedalboard import Pedalboard, Compressor, HighpassFilter, Limiter, Gain, Reverb, Chorus
import librosa
import soundfile as sf
import os

st.set_page_config(page_title="Suno Master Pro (Final)", layout="centered")
st.title("🛡️ Suno Pro: Ultimate Studio Cleanup")
st.write("Suno mahnısını yükləyin və 'Təmizlə' düyməsini sıxın.")

target_file = st.file_uploader("Suno mahnısını seçin", type=["mp3", "wav"])

if target_file:
    if st.button("Mükəmməl Master Et"):
        with st.spinner('Professional təmizləmə prosesi gedir...'):
            with open("input.wav", "wb") as f:
                f.write(target_file.getbuffer())
            
            audio, sr = librosa.load("input.wav", sr=None)
            
            # Professional Studiya Zənciri
            board = Pedalboard([
                HighpassFilter(cutoff_frequency_hz=45), # Alt küyləri kəsir
                Compressor(threshold_db=-20, ratio=4, attack_ms=10, release_ms=100), # Balans
                Gain(gain_db=3.0), # Enerji verir
                Chorus(rate_hz=0.5, depth=0.1, centre_delay_ms=7), # Vokala "canlılıq" qatır
                Reverb(room_size=0.1, dry_level=0.9), # AI quruluğunu silir
                Limiter(threshold_db=-0.1) # Maksimum səs ucalığı
            ])
            
            cleaned = board(audio, sr)
            sf.write("processed.wav", cleaned.T, sr)

            # Referanssız professional spectral matching
            try:
                mg.process(target="processed.wav", reference="processed.wav", results=[mg.pcm24("final.wav")])
                final_path = "final.wav"
            except:
                final_path = "processed.wav"
            
            st.success("✅ Mahnı professional səviyyədə master olundu!")
            st.audio(final_path)
            with open(final_path, "rb") as f:
                st.download_button("Mahnını Yüklə", f, file_name="Suno_Studio_Final.wav")
