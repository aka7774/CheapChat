import os
import json
import gradio as gr

import tab.prompt
import tab.rag
import tab.var
import tab.messages
import tab.settings
import tab.batch
import tab.varn
from tab.refresh import create_refresh_button

from func.config import cfg


with gr.Blocks() as demo:
    title = gr.Markdown('# akachat')
    info = gr.Markdown()
    tab.prompt.gr_tab(gr)
    tab.rag.gr_tab(gr)
    tab.var.gr_tab(gr)
    tab.messages.gr_tab(gr)
    tab.settings.gr_tab(gr)
    tab.batch.gr_tab(gr)
    tab.varn.gr_tab(gr)

if __name__ == '__main__':
    demo.launch()
