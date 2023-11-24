import json
import gradio as gr

import cheapchat

INPUT_VARS = 10

def fn_chat(input, model, dtype, max_new_tokens, temperature, top_p, repetition_penalty, *args):
    cheapchat.model_set(model, dtype)
    print(args)

    a = list(args)
    vars = {}
    for i in range(1, INPUT_VARS + 1):
        vars[f'var{i}'] = a.pop(0)
    jd = json.dumps(vars)

    for i in range(INPUT_VARS, 1 - 1, -1):
        vars[f'var{i}'] = vars[f'var{i}'].format(**vars)

    args = {
        'prompt': vars['var1'],
        'input': input,
        'max_new_tokens': int(max_new_tokens),
        'temperature': float(temperature),
        'top_p': float(top_p),
        'repetition_penalty': float(repetition_penalty),
        }
    return vars['var1'], cheapchat.chat(args), jd

def fn_load(jd):
    vars = json.loads(str(jd))
    inputs = []
    for i in range(1, INPUT_VARS + 1):
        inputs.append(vars[f'var{i}'])
        
    return inputs

with gr.Blocks() as demo:
    with gr.Tab('Chat'):
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown('prompt(=var1)')
                inputs = []
                for i in range(1, INPUT_VARS + 1):
                    inputs.append(gr.Textbox(
                        lines=5,
                        label=f'var{i}',
                        show_label=True,
                        interactive=True,
                        show_copy_button=True,
                        ))

            with gr.Column(scale=1):
                input = gr.Textbox(label='input', show_label=True, interactive=True, show_copy_button=True)
                chat_button = gr.Button(value='chat')
                said = gr.Textbox(label='said', show_label=True, show_copy_button=True)
                prompt = gr.Textbox(label='prompt', show_label=True, show_copy_button=True)
                jd = gr.Textbox(label='json', show_label=True, interactive=True, show_copy_button=True)
                load_button = gr.Button(value='load')

    with gr.Tab('Settings'):
        with gr.Row():
            with gr.Column(scale=1):
                model = gr.Textbox(value='elyza/ELYZA-japanese-Llama-2-7b-fast-instruct', label='model', show_label=True, interactive=True, show_copy_button=True)

                gr.Examples(
                    [
                        ['elyza/ELYZA-japanese-Llama-2-7b-fast-instruct'],
                        ['cyberagent/calm2-7b-chat'],
                        ['stabilityai/japanese-stablelm-instruct-ja_vocab-beta-7b'],
                        ['stabilityai/japanese-stablelm-instruct-gamma-7b'],
                        ['rinna/youri-7b-instruction'],
                        ['rinna/youri-7b-chat'],
                        ['llm-jp/llm-jp-13b-instruct-full-jaster-dolly-oasst-v1.0'],
                        ['stockmark/stockmark-13b-instruct'],                
                    ],
                    [model],
                )

                dtype = gr.Textbox(value='int4', label='dtype', show_label=True, interactive=True, show_copy_button=True)

                gr.Examples(
                    [
                        ['int4'],
                        ['int8'],
                        ['fp16'],
                    ],
                    [dtype],
                )
            with gr.Column(scale=1):
                max_new_tokens = gr.Textbox(value='256', label='max_new_tokens', show_label=True, interactive=True, show_copy_button=True)
                temperature = gr.Textbox(value='1.0', label='temperature', show_label=True, interactive=True, show_copy_button=True)
                top_p = gr.Textbox(value='1.0', label='top_p', show_label=True, interactive=True, show_copy_button=True)
                repetition_penalty = gr.Textbox(value='1.0', label='repetition_penalty', show_label=True, interactive=True, show_copy_button=True)
    
    inp = [input, model, dtype, max_new_tokens, temperature, top_p, repetition_penalty]
    inp.extend(inputs)
    chat_button.click(
        fn=fn_chat,
        inputs=inp,
        outputs=[prompt, said, jd],
        )

    load_button.click(
        fn=fn_load,
        inputs=jd,
        outputs=inputs,
        )

demo.launch()
