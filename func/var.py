import os

def save_var(key, value):
    path = f"vars/{key}.txt"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(value)
        
    return f"saved {path}"

def load_vars():
    vars = {}
    for key in os.listdir('vars'):
        if not key.endswith('.txt'):
            continue
        stem, ext = os.path.splitext(key)
        vars[stem] = load_var(stem)

    return vars

def load_var(key):
    path = f"vars/{key}.txt"
    with open(path, 'r') as f:
        return f.read()
