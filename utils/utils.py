import ffmpeg
import whisper
import os
import glob
import streamlit as st
from zipfile import ZipFile
from datetime import timedelta
from settings import settings


def format_timestamp(
    seconds: float, always_include_hours: bool = False, decimal_marker: str = "."
):
    """Forman timestamp; copy-past from whisper
    """
    assert seconds >= 0, "non-negative timestamp expected"
    milliseconds = round(seconds * 1000.0)

    hours = milliseconds // 3_600_000
    milliseconds -= hours * 3_600_000

    minutes = milliseconds // 60_000
    milliseconds -= minutes * 60_000

    seconds = milliseconds // 1_000
    milliseconds -= seconds * 1_000

    hours_marker = f"{hours:02d}:" if always_include_hours or hours > 0 else ""
    return (
        f"{hours_marker}{minutes:02d}:{seconds:02d}{decimal_marker}{milliseconds:03d}"
    )


def extract_mp3_from_video(input_file: str, output_file: str, ffmpeg_bin='ffmpeg') -> None:
    """Получить аудиодорожку из видео файла

    Args:
        input_file (str): Исходный файл .mp4
        output_file (str): Результат .mp3
        ffmpeg (str): путь до ffmpeg.exe
    """
    ffmpeg_args = {
        'q:a': 0,
        'map': 'a',
    }
    
    stream = ffmpeg.input(input_file)
    stream = ffmpeg.output(stream, output_file, **ffmpeg_args)
    ffmpeg.run(stream, cmd=ffmpeg_bin)

def transcribe_audio(audio_file: str, model=settings.WHISPER_MODEL):
    """Получить массив текста из аудиофайла

    Args:
        audio_file (str): *.mp3 файл
    """
    # Разобраться как передавать параметры  
    # whisper.DecodingOptions(language='rus')

    model = whisper.load_model(model)
    result = model.transcribe(audio_file, language=settings.WHISPER_LANG)

    return result

def save_uploadedfile(uploadedfile) -> str:
    """Сохранение выгруженного файла на диск сервера.
    """
    #if os.path.exists(os.path.join(settings.UPLOADED_VIDEO_FILE_DIR, uploadedfile.name)):
    #    return video_file_name
    
    with open(os.path.join(settings.UPLOADED_VIDEO_FILE_DIR, uploadedfile.name),"wb") as f:
         f.write(uploadedfile.getbuffer())
    st.success(f'Файл {uploadedfile.name} загружен')
    video_file_name = os.path.join(settings.UPLOADED_VIDEO_FILE_DIR, uploadedfile.name)
    return video_file_name

def remove_file(file_name: str) -> None:
    """Удалить файл
    """
    os.remove(file_name)

def output_with_timestamp(whisper_segment_data: dict) -> str:
    """Вывести текст с временными метками
    """
    current_segments = whisper_segment_data['segments']
    res_lines = []
    for segment in current_segments:
        start, end, text = segment["start"], segment["end"], segment["text"]
        line = f"[{format_timestamp(start)} --> {format_timestamp(end)}] {text}"
        res_lines.append(line)
    return '\n'.join(res_lines)

def output_with_timestamp_st(whisper_segment_data: dict) -> None:
    """Вывести текст с временными метками в st.text
    """
    current_segments = whisper_segment_data['segments']
    res_lines = []
    for segment in current_segments:
        start, end, text = segment["start"], segment["end"], segment["text"]
        line = f"[{format_timestamp(start)} --> {format_timestamp(end)}] {text}"
        st.write(line)


def get_srt_from_segmetns(whisper_segment_data: dict, file_name: str):
    """Записать файл субтитров srt"""
    
    current_segments = whisper_segment_data['segments']
    for segment in current_segments:
        startTime = str(0)+str(timedelta(seconds=int(segment['start'])))+',000'
        endTime = str(0)+str(timedelta(seconds=int(segment['end'])))+',000'
        text = segment['text']
        segmentId = segment['id']+1
        segment = f"{segmentId}\n{startTime} --> {endTime}\n{text[1:] if text[0] is ' ' else text}\n\n"

        srt_filename = os.path.join(settings.RES_TXT_PATH, file_name)
        with open(srt_filename, 'a', encoding='utf-8') as srt_file:
            srt_file.write(segment)
    return srt_filename

def get_txt_from_segments(whisper_segment_data: dict, file_name: str):
    """Записать текст 
    """
    current_text = whisper_segment_data['text']
    txt_filename = os.path.join(settings.RES_TXT_PATH, file_name)
    with open(txt_filename, 'w', encoding='utf-8') as txt_file:
        txt_file.write(current_text)
    return txt_filename


def create_res_zip(video_file_name: str):
    """Создать архив с результатом и удалить исходные txt и srt файлы
    """
    with ZipFile(f'{settings.RES_TXT_PATH}{video_file_name}.zip', 'w') as zip_obj:
        for file in glob.glob(f'{settings.RES_TXT_PATH}/*.srt') + glob.glob(f'{settings.RES_TXT_PATH}/*.txt'):
            zip_obj.write(file, os.path.basename(file))
    for file in glob.glob(f'{settings.RES_TXT_PATH}/*.srt') + glob.glob(f'{settings.RES_TXT_PATH}/*.txt'):
        os.remove(file)

def download_res_zip(video_file_name: str):
    """Реализация функционала скачивания архива с результатом в Streamlit
    """
    if os.path.exists(f'{settings.RES_TXT_PATH}{video_file_name}.zip'):
        f_name = f'{settings.RES_TXT_PATH}{video_file_name}.zip'
        with open(f_name, 'rb') as file:
            st.download_button(
                label='Скачать результат',
                data=file,
                file_name=f'{video_file_name}.zip'
            )

def download_res_files(video_file_name: str):
    """Скачать результат работы сервиса - файлы субртитров srt и текст
    """
    if os.path.exists(f'{settings.RES_TXT_PATH}{video_file_name}.srt'):
        f_name = f'{settings.RES_TXT_PATH}{video_file_name}.srt'
        with open(f_name, 'rb') as file:
            st.download_button(
                label='Скачать .srt',
                data=file,
                file_name=f'{video_file_name}.txt'
            )
    
    if os.path.exists(f'{settings.RES_TXT_PATH}{video_file_name}.txt'):
        f_name = f'{settings.RES_TXT_PATH}{video_file_name}.txt'
        with open(f_name, 'rb') as file:
            st.download_button(
            label='Скачать .txt',
            data=file,
            file_name=f'{video_file_name}.txt'
        )

def download_sample(video_file_name: str):
    """Реализация функционала скачивания примера видео-файла;
    """
    f_name = settings.VIDEO_SAMPLE
    with open(f_name, 'rb') as file:
        st.download_button(
            label='Скачать пример',
            data=file,
            file_name=f'{video_file_name}'
        )