import os
import json
import gradio as gr

from tab.prompt import gr_tab_prompt
from tab.rag import gr_tab_rag
from tab.var import gr_tab_var
from tab.messages import gr_tab_messages
from tab.settings import gr_tab_settings
from tab.batch import gr_tab_batch
from tab.varn import gr_tab_varn
from tab.refresh import create_refresh_button

from func.config import cfg


with gr.Blocks() as demo:
    title = gr.Markdown('# akachat')
    info = gr.Markdown()
    gr_tab_prompt(gr)
    gr_tab_rag(gr)
    gr_tab_var(gr)
    gr_tab_messages(gr)
    gr_tab_settings(gr)
    gr_tab_batch(gr)
    gr_tab_varn(gr)

# init
#func.chat.model_set('elyza/ELYZA-japanese-Llama-2-7b-fast-instruct', 'int4')

#from main import app
#app = gr.mount_gradio_app(app, demo, path="/gradio")

demo.launch()
