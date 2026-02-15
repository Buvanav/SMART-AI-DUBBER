import streamlit as st
import whisper
from deep_translator import GoogleTranslator
from gtts import gTTS
from moviepy.editor import VideoFileClip, AudioFileClip
import os

st.set_page_config(page_title="Smart AI Dubber")

st.title("Smart AI Dubber")
st.write("Upload any video and convert it to Tamil or Hindi instantly.")

uploaded_file = st.file_uploader("Upload Video", type=["mp4"])
language = st.selectbox("Select Output Language", ["Tamil", "Hindi"])

if uploaded_file is not None:

    with open("input.mp4", "wb") as f:
        f.write(uploaded_file.read())

    st.success("Video Uploaded Successfully!")

    with st.spinner("Processing... Please wait ⏳"):

        model = whisper.load_model("base")
        result = model.transcribe("input.mp4")

        original_text = result["text"]
        detected_language = result["language"]

        st.write("Detected Language:", detected_language)

        if language == "Tamil":
            target_lang = "ta"
        else:
            target_lang = "hi"

        translated_text = GoogleTranslator(
            source='auto',
            target=target_lang
        ).translate(original_text)

        tts = gTTS(translated_text, lang=target_lang)
        tts.save("output_audio.mp3")

        video = VideoFileClip("input.mp4")
        audio = AudioFileClip("output_audio.mp3")
        final_video = video.set_audio(audio)
        final_video.write_videofile("output.mp4")

    st.success("✅ Conversion Completed!")

    st.video("output.mp4")

    with open("output.mp4", "rb") as file:
        st.download_button(
            label="Download Dubbed Video",
            data=file,
            file_name="dubbed_video.mp4",
            mime="video/mp4"
        )