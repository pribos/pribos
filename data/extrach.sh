#! /bin/bash
mail = {"title": "Title of the Series: The number of the Season (Korean)", "message": "Hello Miyeon,\nI hope you are having a great day!\nWe have a new project that has become available\nif you are interested. Here’s a breakdown -\nTitle: 제목 예시\n# of episodes: (...)\nRuntime: ~45m\nClient/spec: Disney +\nContent: 작품명 예시\nGenre: Documentary\nProject Management Software: ATS\nTask: Translation\nRate: $8/hour\nTranslation Instructions: (...)\nSchedule: until 8/11/2019"}

print(grep runtime | mail["message"])