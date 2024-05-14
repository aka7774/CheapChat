import os
import re
import torch
import datetime
import json
import csv
import gc
import requests
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from transformers import TextStreamer, TextIteratorStreamer
from transformers import GenerationConfig, AutoConfig, GPTQConfig, AwqConfig

tokenizer = None
model = None
loaded_model_name = None
loaded_dtype = None
config = {}
tsv = []

def model_set(model_name, dtype = 'int4'):
    global tokenizer, model, loaded_model_name, loaded_dtype, tsv

    if loaded_model_name == model_name and loaded_dtype == dtype:
        return

    del model
    del tokenizer
    model = None
    tokenizer = None
    gc.collect()
    torch.cuda.empty_cache()

    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    
    if dtype == 'int4':
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map="auto",
            trust_remote_code=True,
            quantization_config=BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch.bfloat16,
            ),
        )
    elif dtype == 'int8':
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map="auto",
            trust_remote_code=True,
            quantization_config=BitsAndBytesConfig(
                torch_dtype=torch.bfloat16,
                load_in_8bit=True,
            ),
        )
    elif dtype == 'fp16':
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map="auto",
            trust_remote_code=True,
            torch_dtype=torch.float16,
        )
    elif dtype == 'bf16':
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map="auto",
            trust_remote_code=True,
            torch_dtype=torch.bfloat16,
        )
    else:
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            trust_remote_code=True,
            device_map="auto",
        )

    loaded_model_name = model_name
    loaded_dtype = dtype

def trim_output(output):
    global tsv
    for row in tsv:
        if len(row) > 2 and row[2] == 'resub':
            rep = re.compile(row[0], re.MULTILINE | re.DOTALL)
            output = re.sub(rep, row[1], output)
        elif row[0] in output:
            if len(row) == 1:
                row[1] = ''
            output = output.replace(row[0], row[1])

    return output

def chat(args: dict):
    global tokenizer, model, loaded_model_name, config, tsv
    
    if 'model' in args:
        args['model_name'] = args['model']
        del args['model']

    if not tokenizer or 'model_name' in args and loaded_model_name != args['model_name']:
        if 'dtype' in args:
            model_set(args['model_name'], args['dtype'])
        else:
            model_set(args['model_name'])

    config.update(args)

    if config['is_messages']:
        messages = []
        messages.append({"role": "system", "content": args['instruction']})
        if args['input']:
            messages.append({"role": "user", "content": args['input']})
        tprompt = tokenizer.apply_chat_template(conversation=messages, add_generation_prompt=True, tokenize=False)
    else:
        tprompt = config['template'].format(bos_token=tokenizer.bos_token, instruction=args['instruction'], input=args['input'])

    if config['output_tokens']:
        config['max_new_tokens'] = config['output_tokens']
        del config['output_tokens']

    kwargs = config.copy()
    for k in ['model_name', 'template', 'instruction', 'input', 'location', 'endpoint', 'model', 'dtype', 'is_messages', 'input_tokens']:
        if k in kwargs:
            del kwargs[k]

    with torch.no_grad():
        token_ids = tokenizer.encode(tprompt, add_special_tokens=False, return_tensors="pt")
        if config['is_messages']:
            output_ids = model.generate(
                input_ids=token_ids.to(model.device),
                do_sample=True,
                **kwargs,
            )
        else:
            output_ids = model.generate(
                input_ids=token_ids.to(model.device),
                do_sample=True,
                pad_token_id=tokenizer.pad_token_id,
                bos_token_id=tokenizer.bos_token_id,
                eos_token_id=tokenizer.eos_token_id,
                **kwargs,
            )
    out = output_ids.tolist()[0][token_ids.size(1) :]
    output = tokenizer.decode(out, skip_special_tokens=True)

    content = trim_output(output)
    
    del output_ids
    del output

    return content, tprompt

def request(args: dict):
    url = args['endpoint']
    config.update(args)
    tprompt = config['template'].format(instruction=args['instruction'], input=args['input'])
    data = {}
    data['prompt'] = tprompt
    data['stop'] = ["###"]

    kwargs = config.copy()
    for k in ['model_name', 'template', 'instruction', 'input', 'location', 'endpoint', 'model', 'dtype', 'is_messages']:
        if k in kwargs:
            del kwargs[k]
    kwargs.update(data)
    
    if 'output_tokens' in kwargs:
        kwargs['max_tokens'] = kwargs['output_tokens']
        del kwargs['output_tokens']

    if 'repetition_penalty' in kwargs:
        kwargs['repeat_penalty'] = kwargs['repetition_penalty']
        del kwargs['repetition_penalty']

    print(kwargs)
    res = requests.post(url, json.dumps(kwargs), headers={'Content-Type': 'application/json'})
    jo = res.json()
    body = jo['choices'][0]['text']

    content = trim_output(body)

    return content, jo
