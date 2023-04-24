import streamlit as st
import os
from utils import utils
from settings import settings

# streamlit run streamlit_whisper.py --server.port 8000 --server.maxUploadSize 20
# streamlit run your_script.py --server.maxUploadSize 200
st.title("Транскрибирование видео (RU)")
st.markdown(settings.HIDE_MENU, unsafe_allow_html=True)

if os.path.exists(settings.VIDEO_SAMPLE):
    utils.download_sample('sample.mp4')

# Flags 
# for download buttons
download_files_exists = False

# upload video file with streamlit
video_file = st.file_uploader('Загрузить видео-файл', type=['mp4'])

# save video file on server
if video_file is not None:
    video_file_full_name = utils.save_uploadedfile(video_file)
    video_file_name = os.path.splitext(video_file.name)[0]
    download_files_exists = True

# take audio from video file
if st.sidebar.button("Первичная обработка видео"):
    if video_file is not None:
        st.sidebar.success("Получение звуковой дорожки...")
        utils.extract_mp3_from_video(video_file_full_name, settings.TMP_AUDIO_FILE)
        st.sidebar.success("Звуковая дорожка получена")
    else:
        st.sidebar.error("Пожалуйста, загрузите видео-файл (mp4)")

#make some magic
if st.sidebar.button("Получить текст"):
    if settings.TMP_AUDIO_FILE is not None:
        st.sidebar.success("Обработка звуковой дорожки...")
        transcription = utils.transcribe_audio(settings.TMP_AUDIO_FILE)
        st.sidebar.success("Процесс завершён")
        utils.output_with_timestamp_st(transcription)
        srt_file = utils.get_srt_from_segmetns(transcription, f'{video_file_name}.srt')
        txt_file = utils.get_txt_from_segments(transcription, f'{video_file_name}.txt')
        zip_file = utils.create_res_zip(video_file_name)
        utils.remove_file(video_file_full_name)
        utils.remove_file(settings.TMP_AUDIO_FILE)
    else:
        st.sidebar.error("Что-то пошло не так...")

if download_files_exists:
    utils.download_res_zip(video_file_name)
    

