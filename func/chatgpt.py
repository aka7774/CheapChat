from openai import OpenAI

from func.config import cfg

def infer(messages, opt):
    if opt['endpoint']:
        client = OpenAI(
            api_key=cfg['openai_key'],
            base_url=opt['endpoint'],
        )
    else:
        client = OpenAI(
            api_key=cfg['openai_key'],
        )
    response = client.chat.completions.create(
                model=opt['model'],
                messages=messages,
            )

    return response.choices[0].message.content
