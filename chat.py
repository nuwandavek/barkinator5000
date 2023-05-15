import os
import openai

PAST_NUM = 5
OPENAI_KEY = os.getenv("OPENAI_LUCY_KEY")
assert OPENAI_KEY, "The openai key is not set!"
openai.api_key = OPENAI_KEY


def character_respond(character_script, message):
  prompt = f"""You are a character in a video game. Use the below notes, stick to the story exactly.
  {character_script}
  Answer the query enclosed in the <Query> tag. Limit the response to fewer than 3 sentences.
  <Query>{message}</Query>
  """
  ipt = [{'role': 'user', 'content': prompt}]
  resp = get_chatgpt_response(ipt)
  return resp.strip().strip('\"')


def get_chatgpt_response(messages):
  completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=messages,
    temperature=0.5
  )
  return completion.choices[0].message.content
