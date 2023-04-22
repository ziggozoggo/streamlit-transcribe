import streamlit as st
import os
from utils import utils
from settings import settings

footer = """
<style>
footer{
    visibility: hidden;
}
footer:after{
    content:'Comrade Mazzay 2023';
    display: block;
    postition: relative;
    color: tomato;
    padding: 5px;
    top: 3px;
}
</style>
"""

# streamlit run streamlit_whisper.py --server.port 8000
st.title("Транскрибирование видео (RU)")
st.markdown(settings.HIDE_MENU, unsafe_allow_html=True)

# Flags 
# for download buttons
download_files_exists = False

# upload video file with streamlit
video_file = st.file_uploader('Загрузить видео-файл', type=['mp4'])

# with st.form('my_form', clear_on_submit=True):
#     video_file = st.file_uploader('Загрузить видео-файл', type=['mp4'])
#     submitted = st.form_submit_button("Submit")
#     if submitted:
#         video_file_full_name = utils.save_uploadedfile(video_file)
#         print(video_file_full_name)
#         video_file_name = os.path.splitext(video_file.name)[0]
#         download_files_exists = True

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



# upload audio file with streamlit
# audio_file = st.file_uploader("Upload Audio", type=['mp3'])

# save audio file on server
# if audio_file is not None:
#     utils.save_uploadedfile(audio_file)


#make some magic
if st.sidebar.button("Получить текст"):
    if settings.TMP_AUDIO_FILE is not None:
        st.sidebar.success("Обработка звуковой дорожки...")
        transcription = utils.transcribe_audio(settings.TMP_AUDIO_FILE)
        st.sidebar.success("Процесс завершён")
        #st.text_area(transcription['text'])
        utils.output_with_timestamp_st(transcription)
        srt_file = utils.get_srt_from_segmetns(transcription, f'{video_file_name}.srt')
        txt_file = utils.get_txt_from_segments(transcription, f'{video_file_name}.txt')
        zip_file = utils.create_res_zip(video_file_name)
        #st.text_area(utils.output_with_timestamp(transcription))
        #with open(srt_file, 'rb') as f:
        #    st.download_button('Скачать .srt', f, file_name=f'{video_file_name}.srt')
        # with open(txt_file, 'rb') as f:
        #     st.download_button('Скачать .txt', f, file_name=f'{video_file_name}.txt')
        utils.remove_file(video_file_full_name)
        utils.remove_file(settings.TMP_AUDIO_FILE)
    else:
        st.sidebar.error("Что-то пошло не так...")

if download_files_exists:
    #utils.download_res_files(video_file_name)
    utils.download_res_zip(video_file_name)

# if download_files_exists:
#     if os.path.exists(f'{settings.RES_TXT_PATH}{video_file_name}.srt'):
#         f_name = f'{settings.RES_TXT_PATH}{video_file_name}.srt'
#         with open(f_name, 'rb') as file:
#             st.download_button(
#             label='Скачать .srt',
#             data=file,
#             file_name=f_name
#         )
        
    
#     if os.path.exists(f'{settings.RES_TXT_PATH}{video_file_name}.txt'):
#         f_name = f'{settings.RES_TXT_PATH}{video_file_name}.txt'
#         with open(f_name, 'rb') as file:
#             st.download_button(
#             label='Скачать .txt',
#             data=file,
#             file_name=f_name
#         )
    

