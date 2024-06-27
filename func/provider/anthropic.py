from anthropic import Anthropic

from func.config import cfg

def infer(instruction = '', input = '', messages = {}, opt = {}):
    system, _, messages = build_messages(instruction, input, messages)

    kwargs = {
        "api_key": cfg['anthropic_key'],
    }
    client = Anthropic(**kwargs)

    kwargs = {
        "model": opt['model'],
        "system": system,
        "messages": messages,
    }
    for k in ['temperature', 'top_p', 'top_k', 'timeout']:
        if k in opt:
            kwargs[k] = opt[k]
    if 'max_new_tokens' in opt and opt['max_new_tokens']:
        kwargs['max_tokens'] = opt['max_new_tokens']
    # penaltyは設定できないっぽい(2024-04-26)
    if 'stream' in opt and opt['stream']:
        kwargs['stream'] = True

    return client.messages.create(**kwargs)

def build_messages(instruction = '', input = '', messages = {}):
    # anthropic では system は別途指定する
    # 誤って messages で指定されていたら system に集約してあげる
    for i, v in enumerate(messages):
        if v['role'] == 'system':
            instruction += messages[i]['content']
            del messages[i]
    # user は使える
    if len(input) > 0:
        messages.append({"role": "user", "content": input})
    return instruction, None, messages

def content(response):
    return response.content[0].text
