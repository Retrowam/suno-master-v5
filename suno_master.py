import streamlit as st
import matchering as mg
from pedalboard import Pedalboard, Compressor, HighpassFilter, Limiter, Gain, Reverb, Chorus, Distortion, Phaser
import librosa
import soundfile as sf
import numpy as np
import random
import os

st.set_page_config(page_title="Suno Anti-AI Stealth", layout="centered")
st.title("🎧 Suno Anti-AI Stealth Master")

target_file = st.file_uploader("Mahnını yüklə", type=["mp3", "wav"])

if target_file:
    if st.button("AI İzlərini Sil və Master Et"):
        with st.spinner('AI detektorları üçün tələlər qurulur...'):
            # Giriş faylını saxlayırıq
            input_path = "input_raw.wav"
            with open(input_path, "wb") as f:
                f.write(target_file.getbuffer())
            
            # Səsi oxuyuruq
            audio, sr = librosa.load(input_path, sr=None, mono=False)
            
            # 1. Humanize: Mikro pitch-shift (AI hamarlığını pozmaq üçün)
            def humanize(data, rate):
                steps = random.uniform(-0.06, 0.06)
                return librosa.effects.pitch_shift(data, sr=rate, n_steps=steps)

            if audio.ndim > 1:
                audio[0] = humanize(audio[0], sr)
                audio[1] = humanize(audio[1], sr)
            else:
                audio = humanize(audio, sr)
                audio = np.vstack((audio, audio))

            # 2. Stealth Effects Chain
            board = Pedalboard([
                HighpassFilter(cutoff_frequency_hz=48),
                Phaser(rate_hz=0.15, depth=0.1, feedback=0.1),
                Distortion(drive_db=2.8),
                Compressor(threshold_db=-20, ratio=4),
                Chorus(rate_hz=0.9, depth=0.25),
                Reverb(room_size=0.1, wet_level=0.15),
                Gain(gain_db=1.8),
                Limiter(threshold_db=-0.2)
            ])
            
            processed = board(audio, sr)
            
            # Matchering üçün iki fərqli fayl yaradırıq (Xətanın qarşısını almaq üçün)
            target_path = "stealth_target.wav"
            ref_path = "input_raw.wav" # Orijinalı referans kimi istifadə edirik
            sf.write(target_path, processed.T, sr)

            final_output = "final_stealth_master.wav"
            
            try:
                # Target və Reference fərqli olduğu üçün artıq xəta verməyəcək
                mg.process(target=target_path, reference=ref_path, results=[mg.pcm24(final_output)])
                
                st.success("✅ Stealth Master hazır! AI izləri qarışdırıldı.")
                st.audio(final_output)
                with open(final_output, "rb") as f:
                    st.download_button("Master Mahnını Yüklə", f, file_name="Final_Stealth_Master.wav")
            except Exception as e:
                st.error(f"Masterinq xətası: {e}")
                st.info("Alternativ olaraq stealth variantı təqdim edilir:")
                st.audio(target_path)
