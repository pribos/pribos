import re
from datetime import datetime
from pytz import timezone

"""
header['name'] : From -> 회사

title - 메일 제목
message - 메일 본문
"""

# 아래 4줄은 gmail API 연동되어 메일 정보 가져온 상태라고 가정
# # 일단 집어넣자..
# header = {}

# # 메일 정보 받아온 상태라고 가정
# header['name'] = '예시컴퍼니'

# 메일 예시
#mail = {"title": "Title of the Series: The number of the Season (Korean)", "message": "Hello Miyeon,\nI hope you are having a great day!\nWe have a new project that has become available\nif you are interested. Here’s a breakdown -\nTitle: 제목 예시\n# of episodes: (...)\nRuntime: ~45m\nClient/spec: Disney +\nContent: 작품명 예시\nGenre: Documentary\nProject Management Software: ATS\nTask: Translation\nRate: $8/hour\nTranslation Instructions: (...)\nSchedule: 8/11/2019 09:00 UTC"}
#mail = {"title": "Availability Check- Korean- Metadata Task", "message": "Hello,\nI hope you are doing good 🙂\nWould you be available to take up the following Metadata translation?"}
#mail = {"title": "Project ID - Project Name KO", "message": "Dear Elliot,\nHope you’re well!\nWould you be available to help transcribe\n(...) I’ve also attached a sample template you could use."}

# 메일 다 소문자로 만들기
def lowercase(string):
    return string.lower()

mail['title'] = lowercase(mail['title'])
mail['message'] = lowercase(mail['message'])

# 일단 리스트에서 추출....
language_pair = ['korean', 'ko', 'english', 'en', 'chinese', 'zh', 'japanese', 'ja', 'spanish', 'es', 'french', 'fr', 'german', 'de', 'portuguese', 'pt', 'russian', 'ru', 'thai', 'th', 'vietnamese', 'vi', 'arabic', 'ar']
language_pair_translation = ['korean-english', 'ko-en', 'korean-chinese', 'ko-zh', 'korean-japanese', 'ko-ja', 'korean-spanish', 'ko-es', 'korean-french', 'ko-fr', 'korean-german', 'ko-de', 'korean-portuguese', 'ko-pt', 'korean-russian', 'ko-ru', 'korean-thai', 'ko-th', 'korean-vietnamese', 'ko-vi', 'korean-arabic', 'ko-ar', 'english-korean', 'en-ko', 'english-chinese', 'en-zh', 'english-japanese', 'en-ja', 'english-spanish', 'en-es', 'english-french', 'en-fr', 'english-german', 'en-de', 'english-portuguese', 'en-pt', 'english-russian', 'en-ru', 'english-thai', 'en-th', 'english-vietnamese', 'en-vi', 'english-arabic', 'en-ar', 'chinese-korean', 'zh-ko', 'chinese-english', 'zh-en', 'chinese-japanese', 'zh-ja','japanese-korean', 'ja-ko',  'chinese-english', 'zh-en', 'spanish-korean', 'es-ko', 'french-korean', 'fr-ko', 'german-korean', 'de-ko', 'portuguese-korean', 'pt-ko', 'russian-korean', 'ru-ko', 'thai-korean', 'th-ko', 'vietnamese-korean', 'vi-ko', 'arabic-korean', 'ar-ko']
# 국가명, 국가 코드를 리스트로 만들어 차라리 거기 안에 있으면 추출하는 게 나을까?

# 메일 정보에 name 이라고 보낸 사람 정보가 있음. 그게 의뢰 회사.
mail['company'] = header['name']

# todo - 더 깔끔하게 할 수 있는 방법 찾습니다....
# 더 자주 나오는 순으로 앞에다 배열하면 시간이 조금 덜 걸릴까?
for rt in ['runtime', '러닝타임', '런타임', '러닝 타임', '시간', '영상길이', '영상 길이']:
    # 맘에 안들지만 일단...
    for line in mail['message'].split('\n'):
        if rt in line:
            # 그룹으로 시간정보만 추출..
            mail['runtime'] = re.match(f"{rt}\D+"+"(\d{0,2}(?:h|H|시간)?.*\d{0,2}(?:m|M|분|minute)?)", line).group(1)
            break

for lp in language_pair:
    if lp in mail['title']:
        mail['work_language'] = re.search(f"{lp}", mail['title']).group()
        break

# project name - 보통 메일 이름에 있음 -> 얘는 머신러닝 필요
# 메일에서 작업 언어정보를 빼고
mail['project_name'] = mail['title'].replace(mail['work_language'], '')
# 특수문자 제거
mail['project_name'] = re.sub(r"[^A-Za-z0-9가-힣 ]", '', mail['project_name']).strip()

# 메일 제목에서 필요없는 단어들 추가하기
remove_words = ['availability check', '번역 요청', '번역요청']
# remove words 제거
for word in remove_words:
    if word in mail['project_name']:
        mail['project_name'] = re.sub(f"{word}", '', mail['project_name']).strip()

# client
# 메일 이름에 들어가는 경우가 있어 얘도 머신러닝 분류가 있어야 함
for client in ['client', '클라이언트', '고객']:
    for line in mail['message'].split('\n'):
        if client in line:
            if client == 'client':
                # spec이 왜 들어가는진 모르겠지만 이렇게 바꿔주기로..
                line = line.replace('client/spec', 'client')
            mail['client'] = re.sub(r"[^A-Za-z0-9가-힣+ ]", '', line).split(client)[1].strip()
            break

# content - name of their production

# software
for software in ['software', '납품자료']:
    for line in mail['message'].split('\n'):
        if software in line:
            mail['software'] = re.sub(r"[^A-Za-z0-9가-힣 ]", '', line).split(software)[1].strip()
            break

# deadline, due
# 메일에 어떤 형식으로 오는지 보고 더 추가해야 함
# %Z 추가되어야 함
formats = ['%Y-%m-%d %H:%M %Z', '%m/%d/%Y %H:%M %Z', '%m/%d/%y %H:%M %Z']
for deadline in ['deadline', 'schedule', '납품일정', '납품 일정', '납기일자', '납기 일자', '스케줄']:
    for line in mail['message'].split('\n'):
        if deadline in line:
            date_part = re.sub(r"[^A-Za-z0-9가-힣/:+ ]", '', line).split(deadline)[1]
            deadline_mail = re.search(r"\d.+", date_part).group()

            # 삼중포문.. 정말 하고싶지 않았는데요... 더 나은 방법 찾습니다..
            for format in formats:
                try:
                    tz = deadline_mail.split(' ')[-1]
                    deadline_mail = datetime.strptime(deadline_mail, format)

                    # 메일에 적힌 시간대 기준 마감시간
                    mail['deadline_tz'] = timezone(tz).localize(deadline_mail)
                    
                    # 한국 시간 기준 마감시간 
                    mail['deadline_kst'] = mail['deadline_tz'].astimezone(timezone('Asia/Seoul'))
                    break

                except ValueError:
                    # 나중엔 로그로 남길 것
                    print("ValueError :", deadline_mail)

# rate
for rate in ['rate', '요율', '계약금']:
    for line in mail['message'].split('\n'):
        if rate in line:
            mail['rate'] = re.sub(r"[^A-Za-z0-9가-힣/$]", '', line).split(rate)[1]


# task # 메타데이터 번역, 영상번역, 산업번역, 출판번역 등 - 유저가 고르게 해야 함
for task in ['available', '작업']:
    for line in mail['message'].split('\n'):
        if task in line:
            mail['task'] = ''.join(re.sub(r"[^A-Za-z0-9가-힣 ]", '', line).split(task)[1:]).strip()

remove_words = ['to', 'help', 'the', 'following', 'take', 'up']
# remove words 제거
for word in remove_words:
    if word in mail['task']:
        mail['task'] = re.sub(f"{word}", '', mail['task']).strip()