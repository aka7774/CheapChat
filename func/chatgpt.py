import openai

from func.config import cfg

openai.api_key = cfg['openai_key']

def infer(messages):
    response = openai.chat.completions.create(
                model=cfg['openai_model'],
                messages=messages,
            )
    return response.choices[0].message.content
