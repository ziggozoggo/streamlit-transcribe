## Streamlit Whisper MVP app

Install:
* add directories:
    * ./data/audio 
    * ./data/video
    * ./data/res
* check settings.settings.py for:
    * WHISPER_LANG (default 'ru')
    * WHISPER_MODEL (default 'base')

For demo file download&
* create ./data/sample folder
* add sample.mp4 video file


Run app:
```
$ streamlit run streamlit_whisper.py --server.port 8000 --server.maxUploadSize 20
```