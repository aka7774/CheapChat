import os
import google.generativeai as genai

from func.config import cfg


def infer(messages, opt):
    genai.configure(api_key=cfg['google_key'])

    #for m in genai.list_models():
    #  if 'generateContent' in m.supported_generation_methods:
    #    print(m.name)

    model = genai.GenerativeModel(opt['model'])

    system = ''
    for i, v in enumerate(messages):
        system += messages[i]['content']

    response = model.generate_content(system)

    return response.text, response
