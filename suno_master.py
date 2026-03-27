import streamlit as st
import matchering as mg
from pedalboard import Pedalboard, Compressor, HighpassFilter, Limiter, Gain, Reverb, Chorus, Distortion, Phaser
import librosa
import soundfile as sf
import numpy as np
import random

def humanize_audio(audio, sr):
    # 1. Mikro-Pitch Shift (Səsi 'insanlaşdırmaq' üçün yüngül dalğalanma)
    # Bu, AI-nın o 'ideal' səsini pozur
    n_steps = random.uniform(-0.05, 0.05)
    audio_shifted = librosa.effects.pitch_shift(audio, sr=sr, n_steps=n_steps)
    return audio_shifted

st.title("🎧 Suno Anti-AI Stealth Master")

target_file = st.file_uploader("Mahnını yüklə", type=["mp3", "wav"])

if target_file:
    if st.button("AI İzlərini Sil və Master Et"):
        with st.spinner('Analizatorlar üçün tələlər qurulur...'):
            with open("input.wav", "wb") as f:
                f.write(target_file.getbuffer())
            
            audio, sr = librosa.load("input.wav", sr=None, mono=False)
            
            # Səsi insanlaşdırma funksiyasından keçiririk
            if audio.ndim > 1:
                audio[0] = humanize_audio(audio[0], sr)
                audio[1] = humanize_audio(audio[1], sr)
            else:
                audio = humanize_audio(audio, sr)
                audio = np.vstack((audio, audio))

            # Aqressiv Gizlətmə Zənciri
            board = Pedalboard([
                HighpassFilter(cutoff_frequency_hz=50),
                # Phaser çox yüngül dalğalanma yaradır ki, AI izi itir
                Phaser(rate_hz=0.1, depth=0.1, centre_frequency_hz=1000, feedback=0.1),
                Distortion(drive_db=3.0), # 'Warmth' üçün saturation
                Compressor(threshold_db=-20, ratio=4),
                Chorus(rate_hz=0.8, depth=0.3),
                Reverb(room_size=0.12, wet_level=0.18),
                Gain(gain_db=2.0),
                Limiter(threshold_db=-0.2)
            ])
            
            processed = board(audio, sr)
            sf.write("stealth_base.wav", processed.T, sr)

            mg.process(target="stealth_base.wav", reference="stealth_base.wav", results=[mg.pcm24("final_stealth.wav")])
            
            st.success("✅ AI izləri texniki olaraq qarışdırıldı!")
            st.audio("final_stealth.wav")
