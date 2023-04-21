import streamlit as st
from utils import utils
# streamlit run your_script.py --server.port 80
st.title("Whisper App")

# upload audio file with streamlit
audio_file = st.file_uploader("Upload Audio", type=['mp3'])

# save audio file on server
if audio_file is not None:
    utils.save_uploadedfile(audio_file)

# make some magic
if st.sidebar.button("Trancribe Audio"):
    if audio_file is not None:
        st.sidebar.success("Trancribing Audio")
        transcription = utils.transcribe_audio(audio_file.name)
        st.sidebar.success("Trancribtion Complete")
        st.text_area(transcription['text'])
    else:
        st.sidebar.error("Please uploed an audio file")
