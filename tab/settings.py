import os
import json

from func.config import cfg, save_settings

def fn_apply_settings(is_test, openai_key):
    cfg['is_test'] = is_test
    cfg['openai_key'] = openai_key

    save_settings(cfg)

    return 'saved.'

def gr_tab_settings(gr):
    with gr.Tab('Settings'):
        info = gr.Markdown()
        apply_settings = gr.Button(value='Apply settings')
        with gr.Row():
            with gr.Column(scale=1):
                is_test = gr.Checkbox(
                    value=cfg['is_test'],
                    label='enable test()',
                    show_label=True,
                    interactive=True,
                    )
                openai_key = gr.Textbox(
                    value=cfg['openai_key'],
                    label='OpenAI Key',
                    show_label=True,
                    interactive=True,
                    show_copy_button=True,
                    )

    setting_inputs = [is_test, openai_key]
    
    apply_settings.click(
        fn=fn_apply_settings,
        inputs=setting_inputs,
        outputs=[info],
        )
