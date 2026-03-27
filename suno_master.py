import streamlit as st
import matchering as mg
from pedalboard import Pedalboard, Compressor, HighpassFilter, Limiter, Gain, Reverb, Chorus, Distortion, LowShelfFilter
import librosa
import soundfile as sf
import numpy as np
import random

st.set_page_config(page_title="Suno Stem Master Pro", layout="wide")
st.title("🎧 Suno Stem Master: Professional Anti-AI")

col1, col2, col3 = st.columns(3)
with col1: v_file = st.file_uploader("Vocal (Ana Səs)", type=["wav", "mp3"])
with col2: bv_file = st.file_uploader("Back-Vocal (Varsa)", type=["wav", "mp3"])
with col3: inst_file = st.file_uploader("Instrumental (Musiqi)", type=["wav", "mp3"])

def process_vocal(data, sr, is_back=False):
    # AI-nın o 'ideal' səsini sındırmaq üçün mikro-sürüşmə
    steps = random.uniform(-0.04, 0.04)
    v_shifted = librosa.effects.pitch_shift(data, sr=sr, n_steps=steps)
    
    # Vokal zənciri: İnsanlaşdırma (Warmth + Saturation)
    board = Pedalboard([
        LowShelfFilter(cutoff_frequency_hz=300, gain_db=2.0),
        Distortion(drive_db=2.0), # Səsə canlılıq qatır
        Compressor(threshold_db=-15, ratio=3),
        Chorus(rate_hz=0.5, depth=0.1) if is_back else Gain(gain_db=0)
    ])
    return board(v_shifted, sr)

if v_file and inst_file:
    if st.button("Stem Masteri Başlat"):
        with st.spinner('Stemlər ayrı-ayrılıqda emal olunur və birləşdirilir...'):
            # 1. Yükləmə və Oxuma
            v_audio, sr = librosa.load(v_file, sr=None, mono=False)
            inst_audio, _ = librosa.load(inst_file, sr=sr, mono=False)
            
            # 2. Vokal Emalı (Anti-AI metodları ilə)
            v_processed = process_vocal(v_audio, sr)
            
            # 3. Back-vokal emalı (əgər varsa)
            if bv_file:
                bv_audio, _ = librosa.load(bv_file, sr=sr, mono=False)
                bv_processed = process_vocal(bv_audio, sr, is_back=True)
                # Vokalları birləşdir
                v_final = v_processed + (bv_processed * 0.7) # Back vokal bir az zəif
            else:
                v_final = v_processed

            # 4. Mix (Vokal + Musiqi)
            # Musiqi və vokalın uzunluqlarını bərabərləşdir
            min_len = min(v_final.shape[1], inst_audio.shape[1])
            combined = v_final[:, :min_len] + inst_audio[:, :min_len]
            
            sf.write("pre_master.wav", combined.T, sr)

            # 5. Final Professional Mastering (Matchering)
            mg.process(target="pre_master.wav", reference=inst_file, results=[mg.pcm24("final_stem_master.wav")])
            
            st.success("✅ Stem Master Bitdi! Bu mahnı artıq 'Hybrid' (İnsan+Studiya) statusundadır.")
            st.audio("final_stem_master.wav")
