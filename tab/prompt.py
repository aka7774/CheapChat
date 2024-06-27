import os
import json

from types import SimpleNamespace

import func.prompt
import func.models
from tab.refresh import create_refresh_button

from func.config import cfg

ds = None

# gradio issue #7282
def fn_ds():
    global ds
    samples = func.models.get_examples()
    if ds:
        ds.samples = samples
    return samples

def fn_load(name):
    instruction = func.prompt.load_prompt(name)
    opt = func.prompt.load_options(name)
    opt = SimpleNamespace(**opt)

    return instruction, opt.provider, opt.endpoint, opt.model, opt.qtype, opt.dtype, opt.inst_template, opt.chat_template, opt.input_tokens, opt.max_new_tokens, opt.temperature, opt.top_p, opt.top_k, opt.repetition_penalty

def fn_save(prompt_name, instruction, provider, endpoint, model, qtype, dtype, inst_template, chat_template, input_tokens, max_new_tokens, temperature, top_p, top_k, repetition_penalty):
    func.prompt.save_prompt(prompt_name, instruction)
    opt = {
        'provider': provider,
        'endpoint': endpoint,
        'model': model,
        'qtype': qtype,
        'dtype': dtype,
        'inst_template': inst_template,
        'chat_template': chat_template,
        'input_tokens': int(input_tokens),
        'max_new_tokens': int(max_new_tokens),
        'temperature': float(temperature),
        'top_p': float(top_p),
        'top_k': int(top_k),
        'repetition_penalty': float(repetition_penalty),
    }
    func.prompt.save_options(prompt_name, opt)
    
    return 'saved.'

def fn_chat(instruction, user_input, provider, endpoint, model, qtype, dtype, inst_template, chat_template, input_tokens, max_new_tokens, temperature, top_p, top_k, repetition_penalty):
    opt = {
        'provider': provider,
        'endpoint': endpoint,
        'model': model,
        'qtype': qtype,
        'dtype': dtype,
        'inst_template': inst_template,
        'chat_template': chat_template,
        'input_tokens': int(input_tokens),
        'max_new_tokens': int(max_new_tokens),
        'temperature': float(temperature),
        'top_p': float(top_p),
        'top_k': int(top_k),
        'repetition_penalty': float(repetition_penalty),
    }

    r, d, t = func.prompt.infer_prompt(instruction, user_input, opt)

    jd = ''
    try:
        jd = json.dumps(vars(d))
    except:
        pass

    return [r, jd, t]

def fn_reload():
    return list(func.prompt.load_prompts().keys())

def gr_tab(gr):
    with gr.Tab('prompt'):
        info = gr.Markdown()
        with gr.Row():
            with gr.Column(min_width=400):
                prompt_name = gr.Dropdown(
                    choices=fn_reload(),
                    label='name',
                    show_label=True,
                    interactive=True,
                    allow_custom_value=True,
                )
            load_button = gr.Button(value='load')
            save_button = gr.Button(value='save')
            create_refresh_button(gr, prompt_name, lambda: None, lambda: {'choices': fn_reload()}, 'refresh-button', interactive=True)

        with gr.Accordion('Prompt Options', open=False):
            opt = func.models.get_head_options()

            with gr.Row():
                with gr.Column(scale=1):
                    provider = gr.Radio(
                        choices=['trllm', 'ollama', 'openai', 'anthropic', 'googleai'],
                        value=opt['provider'],
                        label='provider',
                        show_label=True,
                        interactive=True,
                        )
                    endpoint = gr.Textbox(
                        value=opt['endpoint'],
                        label='endpoint(openai.api_base)',
                        show_label=True,
                        interactive=True,
                        show_copy_button=True,
                    )
                    model = gr.Textbox(
                        value=opt['model'],
                        label='model',
                        show_label=True,
                        interactive=True,
                        show_copy_button=True,
                    )
                    qtype = gr.Dropdown(
                        value=opt['qtype'],
                        choices=['', 'bnb', 'gptq', 'gguf', 'awq'],
                        label='qtype',
                        interactive=True,
                    )
                    dtype = gr.Dropdown(
                        value=opt['dtype'],
                        choices=['', '4bit', '8bit', 'fp16', 'bf16'],
                        label='dtype',
                        interactive=True,
                        allow_custom_value=True,
                    )
                    inst_template = gr.Textbox(
                        value=opt['inst_template'],
                        lines=10,
                        label='inst_template',
                        interactive=True,
                        show_copy_button=True,
                        )
                    chat_template = gr.Textbox(
                        value=opt['chat_template'],
                        lines=10,
                        label='chat_template',
                        interactive=True,
                        show_copy_button=True,
                        )
                with gr.Column(scale=1):
                    input_tokens = gr.Textbox(
                        value=opt['input_tokens'],
                        label='input_tokens',
                        show_label=True,
                        interactive=True,
                        show_copy_button=True,
                        )
                    max_new_tokens = gr.Textbox(
                        value=opt['max_new_tokens'],
                        label='max_new_tokens',
                        show_label=True,
                        interactive=True,
                        show_copy_button=True,
                        )
                    temperature = gr.Textbox(
                        value=opt['temperature'],
                        label='temperature',
                        show_label=True,
                        interactive=True,
                        show_copy_button=True,
                        )
                    top_p = gr.Textbox(
                        value=opt['top_p'],
                        label='top_p',
                        show_label=True,
                        interactive=True,
                        show_copy_button=True,
                        )
                    top_k = gr.Textbox(
                        value=opt['top_k'],
                        label='top_k',
                        show_label=True,
                        interactive=True,
                        show_copy_button=True,
                        )
                    repetition_penalty = gr.Textbox(
                        value=opt['repetition_penalty'],
                        label='repetition_penalty',
                        show_label=True,
                        interactive=True,
                        show_copy_button=True,
                        )
            with gr.Accordion('Preset', open=False):
                ds = gr.Dataset(
                    samples=fn_ds(),
                    components=[provider, endpoint, model, qtype, dtype, inst_template, chat_template, input_tokens, max_new_tokens, temperature, top_p, top_k, repetition_penalty],
                    samples_per_page = -1,
                )
                #create_refresh_button(gr, ds, lambda: None, lambda: {'samples': fn_ds()}, 'refresh-button', interactive=True)

        with gr.Row():
            with gr.Column(scale=1):
                instruction = gr.Textbox(
                    lines=20,
                    label='instruction',
                    show_label=True,
                    interactive=True,
                    show_copy_button=True,
                    )
                user_input = gr.Textbox(
                    lines=1,
                    label='input',
                    show_label=True,
                    interactive=True,
                    show_copy_button=True,
                    )
                chat_button = gr.Button(value='chat')

            with gr.Column(scale=1):
                said = gr.Textbox(label='said', show_copy_button=True)
                time = gr.Textbox(label='time', show_copy_button=True)
                detail = gr.Textbox(
                    lines=15,
                    label='detail',
                    interactive=False,
                    show_copy_button=True,
                    )

    load_button.click(
        fn=fn_load,
        inputs=[prompt_name],
        outputs=[instruction, provider, endpoint, model, qtype, dtype, inst_template, chat_template, input_tokens, max_new_tokens, temperature, top_p, top_k, repetition_penalty],
        )

    save_button.click(
        fn=fn_save,
        inputs=[prompt_name, instruction, provider, endpoint, model, qtype, dtype, inst_template, chat_template, input_tokens, max_new_tokens, temperature, top_p, top_k, repetition_penalty],
        outputs=[info],
        )

    chat_button.click(
        fn=fn_chat,
        inputs=[instruction, user_input, provider, endpoint, model, qtype, dtype, inst_template, chat_template, input_tokens, max_new_tokens, temperature, top_p, top_k, repetition_penalty],
        outputs=[said, detail, time],
        )
