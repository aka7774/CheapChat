import google.generativeai as genai

from func.config import cfg

def infer(instruction = '', input = '', messages = {}, opt = {}):
    _, _, messages = build_messages(instruction, input, messages)

    kwargs = {
        "api_key": cfg['google_key'],
    }
    client = genai.configure(**kwargs)

    kwargs = {
        "model": opt['model'],
    }

    # どんなオプションが指定できるかわからない(2024-04-26)

    model = genai.GenerativeModel(**kwargs)

    #for m in genai.list_models():
    #  if 'generateContent' in m.supported_generation_methods:
    #    print(m.name)

    return model.generate_content(messages)

def build_messages(instruction = '', input = '', messages = {}):
    # google では system と user を同時に使えない
    # instruction が指定されていたら user に変換してあげる
    if len(instruction) > 0:
        messages.insert(0, {"role": "user", "parts": [instruction]})
    # content じゃなくて parts[] なので変換する
    for i, v in enumerate(messages):
        if 'content' in messages[i]:
            messages[i]['parts'] = [messages[i]['content']]
            del messages[i]['content']
    # user は使える
    if len(input) > 0:
        messages.append({"role": "user", "parts": [input]})
    return None, None, messages

def content(response):
    return response.text
