import func.var
from tab.refresh import create_refresh_button

from func.config import cfg

def gr_tab(gr):
    with gr.Tab('var'):
        info = gr.Markdown()
        with gr.Row():
            with gr.Column(min_width=400):
                var_key = gr.Dropdown(
                    choices=func.var.load_vars(),
                    label='key',
                    show_label=True,
                    interactive=True,
                    allow_custom_value=True,
                )
            load_button = gr.Button(value='load')
            save_button = gr.Button(value='save')
            create_refresh_button(gr, var_key, lambda: None, lambda: {'choices': func.var.load_vars()}, 'refresh-button', interactive=True)

        with gr.Row():
            var_value = gr.Textbox(
                lines=10,
                label='value',
                show_label=True,
                interactive=True,
                show_copy_button=True,
                )

    load_button.click(
        fn=func.var.load_var,
        inputs=[var_key],
        outputs=[var_value],
        )

    save_button.click(
        fn=func.var.save_var,
        inputs=[var_key, var_value],
        outputs=[info],
        )
