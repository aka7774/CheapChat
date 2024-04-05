import os
from anthropic import Anthropic

from func.config import cfg

def infer(messages, opt):
    client = Anthropic(
        api_key=cfg['anthropic_key'],
    )

    system = ''
    for i, v in enumerate(messages):
        if v['role'] == 'system':
            system += messages[i]['content']
            del messages[i]

    message = client.messages.create(
        max_tokens=opt['max_new_tokens'],
        system=system,
        messages=messages,
        model=opt['model'],
    )
    return message.content[0].text, message
