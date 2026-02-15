import streamlit as st
import os
from openai import OpenAI
from deep_translator import GoogleTranslator
from gtts import gTTS
from moviepy.editor import VideoFileClip, AudioFileClip

st.set_page_config(page_title="Smart AI Dubber")
st.title("Smart AI Dubber")
st.write("Upload any video and convert it to Tamil or Hindi instantly.")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

uploaded_file = st.file_uploader("Upload Video", type=["mp4"])
language = st.selectbox("Select Output Language", ["Tamil", "Hindi"])

if uploaded_file is not None:
    st.success("Video Uploaded Successfully!")

    if st.button("Process Video"):
        try:
            with open("input.mp4", "wb") as f:
                f.write(uploaded_file.read())

            with st.spinner("Processing... Please wait ⏳"):

                # Extract audio from video
                video = VideoFileClip("input.mp4")
                video.audio.write_audiofile("audio.mp3")

                # Send audio to OpenAI Whisper API
                with open("audio.mp3", "rb") as audio_file:
                    transcript = client.audio.transcriptions.create(
                        model="gpt-4o-mini-transcribe",
                        file=audio_file
                    )

                original_text = transcript.text

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

                final_video = video.set_audio(AudioFileClip("output_audio.mp3"))
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

        except Exception as e:
            st.error(f"Error occurred: {e}")