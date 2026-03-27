import streamlit as st
import matchering as mg
from pedalboard import Pedalboard, Compressor, HighpassFilter, Limiter, Gain, Reverb, Chorus, StereoWidener
import librosa
import soundfile as sf

st.set_page_config(page_title="Suno Master Pro: Stereo Edition", layout="centered")
st.title("🎧 Suno Pro: Stereo Studio Master")

target_file = st.file_uploader("Suno mahnısını yükləyin", type=["mp3", "wav"])

if target_file:
    if st.button("Stereo Masteri Başlat"):
        with st.spinner('Səs genişləndirilir və studiya keyfiyyətinə salınır...'):
            with open("input.wav", "wb") as f:
                f.write(target_file.getbuffer())
            
            audio, sr = librosa.load("input.wav", sr=None, mono=False) # Mono=False mütləqdir
            
            # Professional Stereo Zənciri
            board = Pedalboard([
                HighpassFilter(cutoff_frequency_hz=40),
                Compressor(threshold_db=-18, ratio=3.5),
                StereoWidener(amount=1.5), # Səsi sağa və sola yayır (Həqiqi Stereo)
                Chorus(rate_hz=0.5, depth=0.1),
                Reverb(room_size=0.1, dry_level=0.85, wet_level=0.15),
                Gain(gain_db=2.0),
                Limiter(threshold_db=-0.1)
            ])
            
            # Səsi emal edirik
            processed = board(audio, sr)
            sf.write("stereo_base.wav", processed.T, sr)

            # Final Master
            try:
                mg.process(target="stereo_base.wav", reference="stereo_base.wav", results=[mg.pcm24("final_stereo.wav")])
                output = "final_stereo.wav"
            except:
                output = "stereo_base.wav"
            
            st.success("✅ Stereo Master tamamlandı! İndi GPT-yə bir də atarsan.")
            st.audio(output)
            with open(output, "rb") as f:
                st.download_button("Stereo Mahnını Yüklə", f, file_name="Suno_True_Stereo.wav")
