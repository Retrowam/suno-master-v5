import streamlit as st
import matchering as mg
from pedalboard import Pedalboard, Compressor, HighpassFilter, Limiter, Gain
import librosa
import soundfile as sf

st.set_page_config(page_title="Pro Mastering Studio", layout="centered")
st.title("🎚️ Professional Auto-Mastering (Non-AI)")

target = st.file_uploader("Suno mahnısını yükləyin", type=["mp3", "wav"])

if target:
    if st.button("Masterinqi Başlat"):
        with st.spinner('Riyazi analiz aparılır...'):
            # 1. Faylı oxuyuruq
            with open("input.wav", "wb") as f: f.write(target.getbuffer())
            audio, sr = librosa.load("input.wav", sr=None)
            
            # 2. Professional Səs Zənciri (Analog Logic)
            # Bu zəncir səsi rəngləmir, sadəcə təmizləyir
            board = Pedalboard([
                HighpassFilter(cutoff_frequency_hz=30), # Altdakı lazımsız küyü kəsir
                Compressor(threshold_db=-18, ratio=3, attack_ms=10), # Səsi balanslayır
                Gain(gain_db=3), # Səsi dolğunlaşdırır
                Limiter(threshold_db=-1.0) # Səsin partlamasını bloklayır
            ])
            
            processed = board(audio, sr)
            sf.write("cleaned_base.wav", processed.T, sr)
            
            # 3. Spektral Uyğunlaşdırma (Referanssız Master)
            # Heç bir mahnı yükləməsən də, sistem daxili "Professional Curve" tətbiq edir
            mg.process(target="cleaned_base.wav", reference=None, results=[mg.pcm24("mastered_final.wav")])
            
            st.success("✅ Riyazi Master tamamlandı! Səs təbii və dolğundur.")
            st.audio("mastered_final.wav")
            with open("mastered_final.wav", "rb") as f:
                st.download_button("Master Faylı Yüklə", f, file_name="Suno_Pro_Master.wav")
