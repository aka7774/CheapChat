import os
import re
import torch
import datetime
import json
import csv
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

tokenizer = None
model = None
loaded_model_name = None
config = {}
tsv = []

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )

def model_set(model_name, dtype = 'int4'):
    global tokenizer, model, loaded_model_name, config, tsv

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    if dtype == 'int4':
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map="auto",
            quantization_config=BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch.bfloat16,
            ),
        )
    elif dtype == 'int8':
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map="auto",
            quantization_config=BitsAndBytesConfig(
                torch_dtype=torch.int8,
                load_in_8bit=True,
            ),
        )
    elif dtype == 'fp16':
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map="auto",
            torch_dtype=torch.float16,
        )
    elif dtype == 'bf16':
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map="auto",
            torch_dtype=torch.bfloat16,
        )
    else:
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map="auto",
        )

    loaded_model_name = model_name

    dir = f"config/{model_name}"
    if os.path.exists(dir):
        with open(f"{dir}/args.json", 'r', encoding='utf-8') as fp:
            config = json.load(fp)

        with open(f"{dir}/template.txt", 'r', encoding='utf-8') as fp:
            config['template'] = fp.read().strip()

        with open(f"{dir}/system.txt", 'r', encoding='utf-8') as fp:
            config['system'] = fp.read().strip()

        with open(f"{dir}/prompt.txt", 'r', encoding='utf-8') as fp:
            config['prompt'] = fp.read().strip()

        with open(f"{dir}/trim.tsv", 'r', encoding='utf-8') as fp:
            tsvf = csv.reader(fp, delimiter='\t')
            tsv = []
            for row in tsvf:
                tsv.append(row)

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
    
    if 'model_name' in args and loaded_model_name != args['model_name']:
        if 'dtype' in args:
            model_set(args['model_name'], args['dtype'])
        else:
            model_set(args['model_name'])

    print(args['input'])

    begin = datetime.datetime.now()

    config.update(args)
    tprompt = config['template'].format(bos_token=tokenizer.bos_token, system=config['system'], prompt=config['prompt'], input=args['input'])

    kwargs = config.copy()
    for k in ['model_name', 'template', 'system', 'prompt', 'input']:
        if k in kwargs:
            del kwargs[k]

    with torch.no_grad():
        token_ids = tokenizer.encode(tprompt, add_special_tokens=False, return_tensors="pt")
        output_ids = model.generate(
            token_ids.to(model.device),
            do_sample=True,
            pad_token_id=tokenizer.pad_token_id,
            bos_token_id=tokenizer.bos_token_id,
            eos_token_id=tokenizer.eos_token_id,
            **kwargs,
        )
    out = output_ids.tolist()[0][token_ids.size(1) :]
    output = tokenizer.decode(out, skip_special_tokens=True)

    print(config)

    print(output)

    content = trim_output(output)

    print(datetime.datetime.now() - begin)
    
    return content

@app.post("/api/chat")
async def api_chat(args: dict) -> Response:
    return Response(content=chat(args), media_type="text/plain")


# init
model_set('elyza/ELYZA-japanese-Llama-2-7b-fast-instruct', 'int8')
