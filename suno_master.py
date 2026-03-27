import streamlit as st
import matchering as mg
from pedalboard import Pedalboard, Compressor, HighpassFilter, Limiter, Gain, Reverb, Distortion, LowShelfFilter
import librosa
import soundfile as sf
import numpy as np
import os

st.set_page_config(page_title="Suno Stem Master: Clear & Human", layout="wide")
st.title("🎧 Suno Clear Stem Master")

col1, col2 = st.columns(2)
with col1: v_file = st.file_uploader("Vocal (Vocalremover-dən)", type=["wav", "mp3"])
with col2: inst_file = st.file_uploader("Music (Vocalremover-dən)", type=["wav", "mp3"])

def process_vocal_clean(data, sr):
    # Heç bir Pitch Shift (titrəmə) yoxdur!
    board = Pedalboard([
        LowShelfFilter(cutoff_frequency_hz=250, gain_db=3.0),
        Distortion(drive_db=1.8), # 'Warm' effektini verir, amma titrətmir
        Compressor(threshold_db=-18, ratio=3.0),
        Reverb(room_size=0.1, dry_level=0.9, wet_level=0.08)
    ])
    return board(data, sr)

if v_file and inst_file:
    if st.button("Masteri Başlat (Təmiz Variant)"):
        with st.spinner('Mahnı bərpa olunur...'):
            with open("v_raw.wav", "wb") as f: f.write(v_file.getbuffer())
            with open("i_raw.wav", "wb") as f: f.write(inst_file.getbuffer())
            
            v_audio, sr = librosa.load("v_raw.wav", sr=None, mono=False)
            i_audio, _ = librosa.load("i_raw.wav", sr=sr, mono=False)
            
            # Vokalı təmiz və isti şəkildə emal edirik
            v_final = process_vocal_clean(v_audio, sr)
            
            # Mix: Vokal artıq daha uca və aydındır
            min_len = min(v_final.shape[1], i_audio.shape[1])
            combined = (v_final[:, :min_len] * 1.2) + (i_audio[:, :min_len] * 0.8)
            
            sf.write("pre_master.wav", combined.T, sr)
            
            try:
                mg.process(target="pre_master.wav", reference="i_raw.wav", results=[mg.pcm24("final_clear_master.wav")])
                st.success("✅ Mahnı artıq 'quyudan çıxdı' və təmizdir!")
                st.audio("final_clear_master.wav")
            except:
                st.audio("pre_master.wav")
