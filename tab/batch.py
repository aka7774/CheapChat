import func.batch
import func.prompt

from func.config import cfg
from func.models import models

def gr_tab(gr):
    with gr.Tab('batch'):
        info = gr.Markdown()
        b_options = gr.Textbox(
            value='{}',
            lines=10,
            label='options',
            show_label=True,
            interactive=True,
            show_copy_button=True,
        )
        b_prompts = gr.Textbox(
            value="\n".join(list(func.prompt.load_prompts().keys())),
            lines=10,
            label='prompts',
            show_label=True,
            interactive=True,
            show_copy_button=True,
        )
        b_models = gr.Textbox(
            value="\n".join(list(models.keys())),
            lines=10,
            label='models',
            show_label=True,
            interactive=True,
            show_copy_button=True,
        )
        b_temps = gr.Textbox(
            value='0.9',
            lines=5,
            label='temps',
            show_label=True,
            interactive=True,
            show_copy_button=True,
        )
        b_inputs = gr.Textbox(
            lines=5,
            label='input',
            show_label=True,
            interactive=True,
            show_copy_button=True,
        )
        run_button = gr.Button(value='Run')

    run_button.click(
        fn=func.batch.run,
        inputs=[b_options, b_prompts, b_models, b_temps, b_inputs],
        outputs=[info],
        )
