from openai import OpenAI

from func.config import cfg

def infer(instruction = '', input = '', messages = {}, opt = {}):
    _, _, messages = build_messages(instruction, input, messages)

    kwargs = {
        "api_key": cfg['openai_key'],
    }    
    if 'endpoint' in opt and opt['endpoint']:
        kwargs['base_url'] = opt['endpoint']
    client = OpenAI(**kwargs)

    kwargs = {
        "model": opt['model'],
        "messages": messages,
    }
    # 'top_k', 
    for k in ['temperature', 'top_p', 'timeout', 'presence_penalty', 'frequency_penalty']:
        if k in opt:
            kwargs[k] = opt[k]
    if 'max_new_tokens' in opt and opt['max_new_tokens']:
        kwargs['max_tokens'] = opt['max_new_tokens']
    # とりあえず
    if 'repetition_penalty' in opt and opt['repetition_penalty']:
        kwargs['frequency_penalty'] = opt['repetition_penalty']
    if 'stream' in opt and opt['stream']:
        kwargs['stream'] = True
    return client.chat.completions.create(**kwargs)

def build_messages(instruction = '', input = '', messages = {}):
    # openai では messages にすべてまとまる
    if len(instruction) > 0:
        messages.insert(0, {"role": "system", "content": instruction})
    if len(input) > 0:
        messages.append({"role": "user", "content": input})
    return None, None, messages

def content(response):
    return response.choices[0].message.content
