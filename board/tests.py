import googletrans
from googletrans import Translator

# print(googletrans.LANGUAGES)

text1 = "Hello welcome to my website!"

tr = Translator()
#_ 객체 생성(번역가)
print(tr.detect(text1))

trans1 = tr.translate(text1, src='en', dest='ja')
#_ 영어를 일본어로 번역
trans1 = tr.translate(text1, src='en', dest='ko')
#_ 영어를 한국어로 번역
print("English to Japanese: ", trans1.text)