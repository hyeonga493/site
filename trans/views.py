from django.shortcuts import render
import googletrans
#_ 구글 번역
from gtts import gTTS
#_ 음성 기능

def index(request):

    bf = request.GET.get('bf','')
    fr = request.GET.get('fr','')
    to = request.GET.get('to','')

    context={
        "ndict" : googletrans.LANGUAGES,
        #_ 번역 포함 언어 불러오기
        'fr' : fr,
        'to' : to,
    }   

    if bf :
        trans = googletrans.Translator()
        #_ 번역가 생성
        after = trans.translate(bf, src=fr, dest=to)
        af = after.text
        sbf = gTTS(bf, lang=fr)
        saf = gTTS(af, lang=to)
        print(af)
        context.update({
            'bf' : bf,
            'af' : af,
            'sbf' : sbf,
            'saf' : saf
        })    

    return render(request, 'trans/index.html',context)
