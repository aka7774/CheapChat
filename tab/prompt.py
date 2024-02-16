import os
import json

from types import SimpleNamespace

import func.prompt
import func.models
from tab.refresh import create_refresh_button

from func.config import cfg

def fn_load(name):
    instruction = func.prompt.load_prompt(name)
    opt = func.prompt.load_options(name)
    opt = SimpleNamespace(**opt)

    return instruction, opt.location, opt.endpoint, opt.model, opt.dtype, opt.is_messages, opt.template, opt.max_new_tokens, opt.temperature, opt.top_p, opt.top_k, opt.repetition_penalty

def fn_save(prompt_name, instruction, location, endpoint, model, dtype, is_messages, template, max_new_tokens, temperature, top_p, top_k, repetition_penalty):
    func.prompt.save_prompt(prompt_name, instruction)
    opt = {
        'location': location,
        'endpoint': endpoint,
        'model': model,
        'dtype': dtype,
        'is_messages': is_messages,
        'template': template,
        'max_new_tokens': int(max_new_tokens),
        'temperature': float(temperature),
        'top_p': float(top_p),
        'top_k': int(top_k),
        'repetition_penalty': float(repetition_penalty),
    }
    func.prompt.save_options(prompt_name, opt)
    
    return 'saved.'

def fn_chat(instruction, user_input, location, endpoint, model, dtype, is_messages, template, max_new_tokens, temperature, top_p, top_k, repetition_penalty):
    opt = {
        'location': location,
        'endpoint': endpoint,
        'model': model,
        'dtype': dtype,
        'is_messages': is_messages,
        'template': template,
        'max_new_tokens': int(max_new_tokens),
        'temperature': float(temperature),
        'top_p': float(top_p),
        'top_k': int(top_k),
        'repetition_penalty': float(repetition_penalty),
    }

    r, p = func.prompt.infer_prompt(instruction, user_input, opt)
    return [r, p]

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
                    location = gr.Radio(
                        choices=['Local', 'OpenAI'],
                        value=opt['location'],
                        label='location',
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

                    dtype = gr.Dropdown(
                        value=opt['dtype'],
                        choices=['int4','int8','fp16', 'bf16'],
                        label='dtype',
                        show_label=True,
                        interactive=True,
                        allow_custom_value=True,
                    )
                    template = gr.Textbox(
                        value=opt['template'],
                        lines=3,
                        label='template',
                        show_label=True,
                        interactive=True,
                        show_copy_button=True,
                        )
                    is_messages = gr.Checkbox(
                        value=opt['is_messages'],
                        label='is_messages',
                        show_label=True,
                        interactive=True,
                        )
                with gr.Column(scale=1):
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
                gr.Examples(
                    func.models.get_examples(),
                    [location, endpoint, model, dtype, is_messages, template, max_new_tokens, temperature, top_p, top_k, repetition_penalty],
                )

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
                said = gr.Textbox(label='said', show_label=True, show_copy_button=True)
                processed = gr.Textbox(
                    lines=15,
                    label='processed',
                    show_label=True,
                    interactive=False,
                    show_copy_button=True,
                    )

    load_button.click(
        fn=fn_load,
        inputs=[prompt_name],
        outputs=[instruction, location, endpoint, model, dtype, is_messages, template, max_new_tokens, temperature, top_p, top_k, repetition_penalty],
        )

    save_button.click(
        fn=fn_save,
        inputs=[prompt_name, instruction, location, endpoint, model, dtype, is_messages, template, max_new_tokens, temperature, top_p, top_k, repetition_penalty],
        outputs=[info],
        )

    chat_button.click(
        fn=fn_chat,
        inputs=[instruction, user_input, location, endpoint, model, dtype, is_messages, template, max_new_tokens, temperature, top_p, top_k, repetition_penalty],
        outputs=[said, processed],
        )
