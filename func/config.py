import os
import json

def save_settings(cfg):
    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump(cfg, f, indent=4)

def load_settings():
    cfg_default = {
        'is_test': True,
        'openai_key': '',
    }
    if os.path.exists('config.json'):
        with open('config.json', 'r', encoding='utf-8') as f:
            cfg = json.load(f)
    else:
        cfg = {}

    for k, v in cfg_default.items():
        cfg.setdefault(k, v)

    return cfg
    
cfg = load_settings()
