import func.rag
from tab.refresh import create_refresh_button

from func.config import cfg

def fn_search(dir, query):
    args = {
        'dir': dir,
        'query': query,
        'k': 1,
    }
    vector_store = func.rag.vector_load(args)
    result, detail = func.rag.search(vector_store, args)

    return result

def gr_tab_rag(gr):
    with gr.Tab('RAG'):
        info = gr.Markdown()
        with gr.Row():
            with gr.Column(min_width=400):
                rag_dir = gr.Dropdown(
                    choices=func.rag.load_dirs(),
                    label='rag_dir',
                    show_label=True,
                    interactive=True,
                    allow_custom_value=True,
                )
            with gr.Accordion("Zip Upload"):
                chunk_size = gr.Textbox(
                    value=0,
                    label='(optional) chunk_size if split',
                    show_label=True,
                    interactive=True,
                )
                rag_zip = gr.UploadButton(
                    label='Zip Upload and save rag_dir',
                    interactive=True,
                )
                create_refresh_button(gr, rag_dir, lambda: None, lambda: {'choices': func.rag.load_dirs()}, 'refresh-button', interactive=True)

        with gr.Row():
            with gr.Column(scale=1):
                query = gr.Textbox(
                    lines=1,
                    label='query',
                    show_label=True,
                    interactive=True,
                    show_copy_button=True,
                    )
                search_button = gr.Button(value='search')

            with gr.Column(scale=1):
                result = gr.Textbox(label='result', show_label=True, show_copy_button=True)

    search_button.click(
        fn=fn_search,
        inputs=[rag_dir, query],
        outputs=[result],
        )
        
    rag_zip.upload(
        fn=func.rag.upload,
        inputs=[rag_dir, chunk_size, rag_zip],
        outputs=[info],
        )
