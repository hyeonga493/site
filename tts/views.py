from django.shortcuts import render
import googletrans
from gtts import gTTS

def fnmake():
    from random import randint as ri
    st = ""
    for i in range(10):
        st += chr(ri(97,122))
    return st
    
def index(request):
    context = {
        'ndict' : googletrans.LANGUAGES
    }
    
    if request.method == "POST":
        bf = request.POST.get('bf')
        to = request.POST.get('to')
        tts = gTTS(bf, lang=to)
        fname = fnmake()
        tts.save(f"media/tts/{fname}.mp3")
        #_ {} 파일 이름은 신중하게 정해야 함 > 함수 작성
        context.update({
            'bf' : bf,
            'to' : to,
            'fn' : fname
        })
    return render(request, 'tts/index.html', context)
