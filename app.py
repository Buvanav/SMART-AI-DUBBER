import streamlit as st
import whisper
from deep_translator import GoogleTranslator
from gtts import gTTS
from moviepy.editor import VideoFileClip, AudioFileClip

st.set_page_config(page_title="Smart AI Dubber")
st.title("Smart AI Dubber")
st.write("Upload any video and convert it to Tamil or Hindi instantly.")

uploaded_file = st.file_uploader("Upload Video", type=["mp4"])
language = st.selectbox("Select Output Language", ["Tamil", "Hindi"])

# Load whisper only once
@st.cache_resource
def load_whisper_model():
    return whisper.load_model("tiny")  # tiny model = lighter & faster

model = load_whisper_model()

if uploaded_file is not None:
    st.success("Video Uploaded Successfully!")

    if st.button("Process Video"):

        try:
            with open("input.mp4", "wb") as f:
                f.write(uploaded_file.read())

            with st.spinner("Processing... Please wait ⏳"):

                result = model.transcribe("input.mp4")
                original_text = result["text"]

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

        except Exception as e:
            st.error(f"Error occurred: {e}")