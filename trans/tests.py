from gtts import gTTS

tts = gTTS('hello', lang='en')
tts.save('hello.mp3')
tts = gTTS('안녕하세요', lang='ko')
tts.save('hello.mp3')