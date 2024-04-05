import os
import requests
import json
import re
import datetime

from types import SimpleNamespace

import func.rag
import func.chatgpt
import func.claude3
import func.llm

import func.var
from func.messages import msg, msgcount

from func.config import cfg

def comment(s):
    return ''

def test(s):
    return s if cfg['is_test'] else ''

def msgf(v: str | list):
    msgs = []

    a = []
    if type(v) is list:
        a = v
    elif type(v) is str:
        a = v.splitlines()

    if cfg['location'] == 'Local':
        return "\n".join(a)
        
    if a:
        for line in a:
            if line.lower().startswith('user:'):
                msgs.append({'role': 'user', 'content': line[5:].strip()})
            elif line.lower().startswith('ai:'):
                msgs.append({'role': 'assistant', 'content': line[3:].strip()})
            elif line.lower().startswith('assistant:'):
                msgs.append({'role': 'assistant', 'content': line[10:].strip()})
            elif line.lower().startswith('system:'):
                msgs.append({'role': 'system', 'content': line[7:].strip()})
            else:
                msgs[-1]['content'] += line
        
    return json.dumps(msgs)

def iif(expr, t, f = ''):
    return t if expr else f

def rag(dir, query):
    args = {
        'dir': dir,
        'query': query,
        'k': 1,
    }
    try:
        vector_store = func.rag.vector_load(args)
        result, detail = func.rag.search(vector_store, args)
        return result
    except Exception as e:
        print(e)
        return ''

def infer_prompt(instruction, input = '', opt = {}):
    var = func.var.load_vars()
    var = SimpleNamespace(**var)

    if 'dir' in opt:
        del opt['dir']
    args = opt.copy()
    args['instruction'] = eval("f'''" + instruction + "'''")
    args['input'] = input

    if input:
        messages = prompt_to_messages(args['instruction'])
        messages.append({'role': 'user', 'content': input})
    else:
        # Claude3 must have non-empty content
        messages = [{'role': 'user', 'content': args['instruction']}]

    begin = datetime.datetime.now()

    if opt['location'] == 'Local':
        speech, detail = func.llm.chat(args)
    elif opt['location'] == 'Llama.cpp':
        speech, detail = func.llm.request(args)
    elif opt['location'] == 'OpenAI':
        speech, detail = func.chatgpt.infer(messages, opt)
    elif opt['location'] == 'Anthropic':
        speech, detail = func.claude3.infer(messages, opt)

    time = datetime.datetime.now() - begin
    infer_log(messages, args, str(time), speech, detail)

    return speech, detail, time # json.dumps(messages)

def infer_log(messages, args, time, speech, detail):
    today = datetime.date.today()

    infer_log_txt(args['instruction'], speech)
    del args['instruction']

    os.makedirs("log/speech/", exist_ok=True)
    path = f"log/speech/{today.strftime('%Y-%m-%d')}.log"
    with open(path, 'a') as f:
        f.write("========\n")
        json.dump(messages, f)
        f.write("\n")
        json.dump(args, f)
        f.write("\n")
        f.write(time)
        f.write("\n")
        if type(detail) is str:
            f.write(detail)
        elif type(detail) is dict:
            json.dump(detail, f)
        else:
            pass
        f.write("\n")

def infer_log_txt(prompt, speech):
    today = datetime.date.today()

    os.makedirs("log/speech/", exist_ok=True)
    path = f"log/speech/{today.strftime('%Y-%m-%d')}.txt"
    with open(path, 'a', encoding='utf-8') as f:
        f.write("========\n")
        f.write(f"{prompt}\n--------\n{speech}\n")

def llm(dir, input = '', **kwargs):
    instruction = load_prompt(dir)
    opt = load_options(dir)
    opt.update(dict(kwargs))

    return infer_prompt(instruction, input, opt)

def infer(args: dict):
    dir = args['dir']
    del args['dir']
    return llm(dir, **args)

def prompt_to_messages(prompt):
    msgs = []
    s = 0
    for m in re.finditer('\[\{.*?\}\]', prompt):
        system = prompt[s:m.start()].strip()
        if len(system):
            msgs.append({'role': 'system', 'content': system})
        msgs.extend(json.loads(prompt[m.start():m.end()]))
        s = m.end()
    system = prompt[s:].strip()
    if len(system):
        msgs.append({'role': 'system', 'content': system})

    return msgs

def save_options(dir, cfg):
    path = f"prompt/{dir}.json"
    with open(path, 'w') as f:
        json.dump(cfg, f, indent=4)

    return 'saved.'

def load_options(dir):
    path = f"prompt/{dir}.json"
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_prompt(dir, prompt):
    path = f"prompt/{dir}.txt"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(prompt)

    return f"saved {path}"

def load_prompts():
    prompts = {}
    for name in os.listdir('prompt'):
        if not name.endswith('.txt'):
            continue
        stem, ext = os.path.splitext(name)
        path = f"prompt/{name}"
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                prompts[stem] = f.read()

    return prompts

def load_prompt(dir):
    path = f"prompt/{dir}.txt"
    if not os.path.exists(path):
        raise ValueError('instruction not found: ' + path)
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()
