import ffmpeg
import whisper
import os
import streamlit as st

def extract_mp3_from_video(input_file: str, output_file: str, ffmpeg_bin:str) -> None:
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

def transcribe_audio(audio_file: str, model='base'):
    """Получить массив текста из аудиофайла

    Args:
        audio_file (str): *.mp3 файл
    """
    # Разобраться как передавать параметры  
    # whisper.DecodingOptions(language='rus')

    model = whisper.load_model(model)
    result = model.transcribe(audio_file)

    return result

def save_uploadedfile(uploadedfile):
    """Сохранение выгруженного файла на диск сервера.
    """
    with open(os.path.join(uploadedfile.name),"wb") as f:
         f.write(uploadedfile.getbuffer())
    return st.success("Saved File:{} to tempDir".format(uploadedfile.name))
