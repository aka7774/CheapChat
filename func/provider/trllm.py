import json
import requests

from func.config import cfg

def infer(instruction = '', input = '', messages = {}, opt = {}):
    url = opt['endpoint']
    del opt['endpoint']

    # TODO: check numel?
    del opt['input_tokens']

    opt['instruct'] = instruction
    opt['input'] = input
    opt['messages'] = messages

    res = requests.post(url, json.dumps(opt), headers={'Content-Type': 'application/json'})

    return res.json()

def content(response):
    return response['content']
