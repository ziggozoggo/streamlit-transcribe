## Streamlit Whisper MVP app

Install:
* add directories:
    * ./data/audio 
    * ./data/video
    * ./data/res
* check settings.settings.py for:
    * WHISPER_LANG (default 'ru')
    * WHISPER_MODEL (default 'base')


Run app:
streamlit run streamlit_whisper.py --server.port 8000
