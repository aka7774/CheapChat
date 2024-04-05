import os
import json

from types import SimpleNamespace

import func.prompt
import gradio

import func.models
from tab.refresh import create_refresh_button

from func.config import cfg


def fn_select(message: gradio.SelectData, log):
    print(message.index)
    print(message.value)
    log.clear()
    log.append((None, ('audio.wav', )))
    log.append((None, ('audio.wav', )))
    
    return log

def fn_chat(message, chatbot, log):
    chatbot.append((message, 'bot'))
    
    generated = 'https://pbs.twimg.com/profile_images/1753800047362482176/238XMI-1_400x400.jpg'

    log += message + "\n"
    return "", generated, chatbot, log

def gr_tab(gr):
    with gr.Tab('chat'):
        with gr.Row():
            chatbot = gr.Chatbot(height='800px', label='messages')
            generated = gr.Image(value='https://pbs.twimg.com/profile_images/1753800047362482176/238XMI-1_400x400.jpg', interactive=False, label='generated girl')
        text = gr.Textbox(label='input')
        log = gr.Textbox(label='log')

    # chatbot.select(
        # fn=fn_select,
        # inputs=[audiolog],
        # outputs=[audiolog],
    # )

    text.submit(
        fn=fn_chat,
        inputs=[text, chatbot, log],
        outputs=[text, generated, chatbot, log],
    )
