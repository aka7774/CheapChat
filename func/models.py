import json

def load():
    with open('models.json', 'r', encoding='utf-8') as f:
        models = json.load(f)

    return models

def get_examples():
    examples = []
    for model in models.keys():
        r = []
        for k, v in models[model].items():
            r.append(v)
        examples.append(r)

    return examples

def get_head_options():
    return models[list(models.keys())[0]]

models = load()
