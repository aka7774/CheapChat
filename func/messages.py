import os
import json
import subprocess

def msg(limit = 0):
    messages = []
    lines = load_lines()
    if limit:
        lines = lines[:-limit]
    for line in lines:
        messages.append(json.loads(line))

    return messages

def msgcount():
    path = "log/messages.jsonl"
    cmd = f"wc -l {path}"
    count = subprocess.check_output(cmd.split()).decode().split()[0]

    return count

def load_list(limit = 0):
    messages = []
    for d in msg(limit):
        messages.append([d['role'], d['content']])

    return messages

def load_header():
    return ['role', 'content']

def load_lines():
    path = "log/messages.jsonl"
    if not os.path.exists(path):
        return []
    with open(path, 'r') as f:
        lines = f.readlines()

    return lines

def load_raw():
    path = "log/messages.jsonl"
    if not os.path.exists(path):
        return ''
    with open(path, 'r') as f:
        body = f.read()

    return body

def save_raw(jsonl):
    path = "log/messages.jsonl"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(jsonl)
        
    return load_list()
