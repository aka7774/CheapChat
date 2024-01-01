import func.messages
from tab.refresh import create_refresh_button

from func.config import cfg

def gr_tab_messages(gr):
    with gr.Tab('messages'):
        info = gr.Markdown()
        with gr.Row():
            messages = gr.Dataframe(
                value=func.messages.load_list(),
                headers=func.messages.load_header(),
            )
        with gr.Row():
            messages_raw = gr.Textbox(
                value=func.messages.load_raw(),
                lines=10,
                label='raw jsonl',
                show_label=True,
                interactive=True,
                show_copy_button=True,
            )
        save_button = gr.Button(value='save')

    save_button.click(
        fn=func.messages.save_raw,
        inputs=[messages_raw],
        outputs=[messages],
        )
