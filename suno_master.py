import streamlit as st
import matchering as mg
from pedalboard import Pedalboard, Compressor, HighpassFilter, Limiter, Gain, Reverb, Distortion, LowShelfFilter, HighShelfFilter
import librosa
import soundfile as sf
import numpy as np
import random
import os

st.set_page_config(page_title="Suno Stem Master Pro", layout="wide")
st.title("🎧 Suno Stem Master: Professional Anti-AI & Clear Mix")

col1, col2, col3 = st.columns(3)
with col1: v_file = st.file_uploader("Vocal (Ana Səs)", type=["wav", "mp3"])
with col2: bv_file = st.file_uploader("Back-Vocal (Varsa)", type=["wav", "mp3"])
with col3: inst_file = st.file_uploader("Instrumental (Musiqi)", type=["wav", "mp3"])

def process_vocal(data, sr):
    # AI 'hamarlığını' pozmaq üçün mikro-pitch shift
    steps = random.uniform(-0.05, 0.05)
    v_shifted = librosa.effects.pitch_shift(data, sr=sr, n_steps=steps)
    
    board = Pedalboard([
        LowShelfFilter(cutoff_frequency_hz=300, gain_db=2.5), # İstilik
        Distortion(drive_db=1.5), # Canlılıq
        Compressor(threshold_db=-18, ratio=3.5),
        Reverb(room_size=0.1, wet_level=0.1)
    ])
    return board(v_shifted, sr)

def process_instrumental(data, sr):
    # İnstrumentalı 'nəfəs aldırmaq' və kərpic effektini silmək üçün
    board = Pedalboard([
        HighpassFilter(cutoff_frequency_hz=40),
        HighShelfFilter(cutoff_frequency_hz=8000, gain_db=1.5), # Parlaqlıq
        Compressor(threshold_db=-12, ratio=2.0), # Yumşaq sıxılma
        Limiter(threshold_db=-1.0) # Pikləri qorumaq
    ])
    return board(data, sr)

if v_file and inst_file:
    if st.button("Stem Masteri Başlat"):
        with st.spinner('Fayllar emal olunur...'):
            # Faylları diskə yazırıq (Xətanın həlli üçün)
            with open("v_temp.wav", "wb") as f: f.write(v_file.getbuffer())
            with open("i_temp.wav", "wb") as f: f.write(inst_file.getbuffer())
            
            v_audio, sr = librosa.load("v_temp.wav", sr=None, mono=False)
            i_audio, _ = librosa.load("i_temp.wav", sr=sr, mono=False)
            
            # Vokal və İnstrumental emalı
            v_final = process_vocal(v_audio, sr)
            i_final = process_instrumental(i_audio, sr)
            
            # Mix (Birləşdirmə)
            min_len = min(v_final.shape[1], i_final.shape[1])
            combined = (v_final[:, :min_len] * 1.1) + (i_final[:, :min_len] * 0.9)
            
            sf.write("pre_master.wav", combined.T, sr)
            
            # Matchering (Final Cilalama)
            try:
                # 'reference' üçün diskdəki fayl yolunu veririk
                mg.process(target="pre_master.wav", reference="i_temp.wav", results=[mg.pcm24("final_master.wav")])
                st.success("✅ Master Bitdi!")
                st.audio("final_master.wav")
            except Exception as e:
                st.error(f"Xəta: {e}")
                st.info("Alternativ master təqdim olunur:")
                st.audio("pre_master.wav")
