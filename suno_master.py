import streamlit as st
import matchering as mg
from pedalboard import Pedalboard, Compressor, HighpassFilter, Limiter, Gain, Reverb, Chorus
import librosa
import soundfile as sf
import numpy as np

st.set_page_config(page_title="Suno Master Pro: Stereo Edition", layout="centered")
st.title("🎧 Suno Pro: Stereo Studio Master")

target_file = st.file_uploader("Suno mahnısını yükləyin", type=["mp3", "wav"])

if target_file:
    if st.button("Stereo Masteri Başlat"):
        with st.spinner('Səs təmizlənir və stereo dərinlik qatılır...'):
            with open("input.wav", "wb") as f:
                f.write(target_file.getbuffer())
            
            # Səsi stereo olaraq oxuyuruq
            audio, sr = librosa.load("input.wav", sr=None, mono=False)
            
            # Əgər səs monodursa (1 kanal), onu süni stereo (2 kanal) edirik
            if audio.ndim == 1:
                audio = np.vstack((audio, audio))
            
            # Professional Stereo Emal Zənciri
            board = Pedalboard([
                HighpassFilter(cutoff_frequency_hz=45),
                Compressor(threshold_db=-18, ratio=3.5),
                # Chorus və Reverb-in 'wet' ayarlarını artıraraq stereo genişlik yaradırıq
                Chorus(rate_hz=1.0, depth=0.25, centre_delay_ms=7), 
                Reverb(room_size=0.15, dry_level=0.8, wet_level=0.2, width=1.0),
                Gain(gain_db=2.5),
                Limiter(threshold_db=-0.1)
            ])
            
            # Emal edirik
            processed = board(audio, sr)
            sf.write("stereo_base.wav", processed.T, sr)

            # Final Master (Matchering)
            try:
                mg.process(target="stereo_base.wav", reference="stereo_base.wav", results=[mg.pcm24("final_stereo.wav")])
                output = "final_stereo.wav"
            except Exception as e:
                output = "stereo_base.wav"
            
            st.success("✅ Stereo Master tamamlandı!")
            st.audio(output)
            with open(output, "rb") as f:
                st.download_button("Stereo Mahnını Yüklə", f, file_name="Suno_Studio_Stereo.wav")
