import os
from anthropic import Anthropic

from func.config import cfg

def infer(messages, opt):
    client = Anthropic(
        api_key=cfg['anthropic_key'],
    )

    for i, v in enumerate(messages):
        if v['role'] == 'system':
            messages[i]['role'] = 'user'

    message = client.messages.create(
        max_tokens=opt['max_new_tokens'],
        messages=messages,
        model=opt['model'],
    )
    return message.content, message
