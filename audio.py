from gtts import gTTS

def text_to_audio(text):
    tts = gTTS(text)
    filename = "output.mp3"
    tts.save(filename)
    return filename