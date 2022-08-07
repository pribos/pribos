import re

"""
header['name'] : From -> 회사

title - 메일 제목
message - 메일 본문
"""


# 일단 집어넣자.. 
header = {} 
header['name'] = '예시컴퍼니'

mail = {"title": "Title of the Series: The number of the Season (Korean)", "message": "Hello Miyeon,\nI hope you are having a great day!\nWe have a new project that has become available\nif you are interested. Here’s a breakdown -\nTitle: 제목 예시\n# of episodes: (...)\nRuntime: ~45m\nClient/spec: Disney +\nContent: 작품명 예시\nGenre: Documentary\nProject Management Software: ATS\nTask: Translation\nRate: $8/hour\nTranslation Instructions: (...)\nSchedule: until 8/11/2019"}

# 메일 다 소문자로 만들기
def lowercase(string):
    return string.lower()

mail['title'] = lowercase(mail['title'])
mail['message'] = lowercase(mail['message'])

# 일단 리스트에서 추출....
language_pair : ['korean', 'ko', 'english', 'en', 'chinese', 'zh', 'japanese', 'ja', 'spanish', 'es', 'french', 'fr', 'german', 'de', 'portuguese', 'pt', 'russian', 'ru', 'thai', 'th', 'vietnamese', 'vi', 'arabic', 'ar']
language_pair_translation : ['korean-english', 'ko-en', 'korean-chinese', 'ko-zh', 'korean-japanese', 'ko-ja', 'korean-spanish', 'ko-es', 'korean-french', 'ko-fr', 'korean-german', 'ko-de', 'korean-portuguese', 'ko-pt', 'korean-russian', 'ko-ru', 'korean-thai', 'ko-th', 'korean-vietnamese', 'ko-vi', 'korean-arabic', 'ko-ar', 'english-korean', 'en-ko', 'english-chinese', 'en-zh', 'english-japanese', 'en-ja', 'english-spanish', 'en-es', 'english-french', 'en-fr', 'english-german', 'en-de', 'english-portuguese', 'en-pt', 'english-russian', 'en-ru', 'english-thai', 'en-th', 'english-vietnamese', 'en-vi', 'english-arabic', 'en-ar', 'chinese-korean', 'zh-ko', 'chinese-english', 'zh-en', 'chinese-japanese', 'zh-ja','japanese-korean', 'ja-ko',  'chinese-english', 'zh-en', 'spanish-korean', 'es-ko', 'french-korean', 'fr-ko', 'german-korean', 'de-ko', 'portuguese-korean', 'pt-ko', 'russian-korean', 'ru-ko', 'thai-korean', 'th-ko', 'vietnamese-korean', 'vi-ko', 'arabic-korean', 'ar-ko']
# 국가명, 국가 코드를 리스트로 만들어 차라리 거기 안에 있으면 추출하는 게 나을까?

# 메일 정보에 name 이라고 보낸 사람 정보가 있음. 그게 의뢰 회사.
mail['company'] = header['name']

for rt in ['runtime', '러닝타임', '런타임', '러닝 타임', '시간']:
    # 맘에 안들지만 일단... 
    for line in mail['message'].split('\n'):
        if rt in line:
            mail['runtime'] = re.match(r'\d{0-2}?[h|H|시간]?.\d{0-2}[m|M|분|minutes]', line).group()
            print(mail['runtime'])
# runtime
# content
# task # 메타데이터 번역, 영상번역, 산업번역, 출판번역 등 - 유저가 고르게 해야 함

