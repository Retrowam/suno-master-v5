import streamlit as st
import matchering as mg
from pedalboard import Pedalboard, Compressor, HighpassFilter, Limiter, Gain, Reverb, Chorus, Distortion, LowShelfFilter
import librosa
import soundfile as sf
import numpy as np

st.set_page_config(page_title="Suno Master Pro: Ultimate", layout="centered")
st.title("🎧 Suno Pro: Stereo & Warm Master")

target_file = st.file_uploader("Suno mahnısını yükləyin", type=["mp3", "wav"])

if target_file:
    if st.button("Masteri Başlat"):
        with st.spinner('Səs təmizlənir və insanlaşdırılır...'):
            with open("input.wav", "wb") as f:
                f.write(target_file.getbuffer())
            
            audio, sr = librosa.load("input.wav", sr=None, mono=False)
            if audio.ndim == 1: audio = np.vstack((audio, audio))
            
            # Professional "Humanizer" Zənciri
            board = Pedalboard([
                HighpassFilter(cutoff_frequency_hz=45),
                # 1. BandLab-dakı 'Warm' effekti (Basları yumşaldır, səsə istilik qatır)
                LowShelfFilter(cutoff_frequency_hz=300, gain_db=3.0),
                # 2. 'Saturation' effekti (AI hamarlığını pozub insan nəfəsi qatır)
                Distortion(drive_db=2.5), 
                Compressor(threshold_db=-18, ratio=3.5),
                Chorus(rate_hz=1.0, depth=0.2, centre_delay_ms=7),
                Reverb(room_size=0.1, dry_level=0.8, wet_level=0.15, width=1.0),
                Gain(gain_db=1.5),
                Limiter(threshold_db=-0.1)
            ])
            
            processed = board(audio, sr)
            sf.write("warm_stereo.wav", processed.T, sr)

            try:
                mg.process(target="warm_stereo.wav", reference="warm_stereo.wav", results=[mg.pcm24("final_master.wav")])
                output = "final_master.wav"
            except:
                output = "warm_stereo.wav"
            
            st.success("✅ Mahnı həm təmizləndi, həm də 'Warm' (İnsan) effekti əlavə olundu!")
            st.audio(output)
