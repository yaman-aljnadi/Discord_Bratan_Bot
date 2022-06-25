from gtts import gTTS

tts = gTTS(text='Good morning', lang='en')
tts.save("good.mp3")