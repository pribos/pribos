import os
import openai
from backend.file import mailfile

openai.api_key = os.getenv("OPENAI_API_KEY")

response = openai.Completion.create(
  model="text-davinci-002",
  prompt=f"Could you convert the following paragraph (in Quotes):{mailfile}",
  temperature=0,
  max_tokens=100,
  top_p=1,
  frequency_penalty=0.2,
  presence_penalty=0
)