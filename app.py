import json
import gradio as gr

import cheapchat

INPUT_VARS = 10

def fn_chat(model, dtype, *args):
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
        'input': '',
        }
    return vars['var1'], cheapchat.chat(args), jd

def fn_load(jd):
    vars = json.loads(str(jd))
    inputs = []
    for i in range(1, INPUT_VARS + 1):
        inputs.append(vars[f'var{i}'])
        
    return inputs

with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column(scale=1):
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
            model = gr.Textbox(value='elyza/ELYZA-japanese-Llama-2-7b-fast-instruct', label='model', show_label=True, interactive=True, show_copy_button=True)
            dtype = gr.Textbox(value='int4', label='dtype', show_label=True, interactive=True, show_copy_button=True)
            chat_button = gr.Button(value='chat')
            said = gr.Textbox(label='said', show_label=True, show_copy_button=True)
            prompt = gr.Textbox(label='prompt', show_label=True, show_copy_button=True)
            jd = gr.Textbox(label='json', show_label=True, interactive=True, show_copy_button=True)
            load_button = gr.Button(value='load')

    inp = [model, dtype]
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
