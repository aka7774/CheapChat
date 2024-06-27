import json
import requests

from func.config import cfg

def infer(instruction = '', input = '', messages = {}, opt = {}):
    _, _, messages = build_messages(instruction, input, messages)

    url = opt['endpoint']
    del opt['endpoint']

    opt['messages'] = messages
    if 'input_tokens' in opt and opt['input_tokens']:
        opt['options'] = {'num_ctx': opt['input_tokens']}

    # なんかjsonの中身だけが変わったものがやってくるので扱いづらい・・・
    opt['stream'] = False

    res = requests.post(url, json.dumps(opt), headers={'Content-Type': 'application/json'})

    return res.json()

def build_messages(instruction = '', input = '', messages = {}):
    # openai では messages にすべてまとまる
    if len(instruction) > 0:
        messages.insert(0, {"role": "system", "content": instruction})
    if len(input) > 0:
        messages.append({"role": "user", "content": input})
    return None, None, messages

def content(response):
    return response['message']['content']
