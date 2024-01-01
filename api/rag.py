import os

import func.rag
import func.apibase
from func.apibase import res

from main import app

from fastapi import Response


@app.post("/api/rag/save")
async def api_rag_save(args: dict) -> func.apibase.ApiResponse:
    func.rag.download(args)
    docs = func.rag.docs_load(args)
    if 'chunk_size' in args and args['chunk_size']:
        docs = func.rag.split(docs, args)
    func.rag.vector_save(docs, args)
    return res(0, "saved.")

@app.post("/api/rag/search")
async def api_rag_search(args: dict) -> func.apibase.ApiResponse:
    vector_store = func.rag.vector_load(args)
    result, detail = func.rag.search(vector_store, args)
    return res(0, result, detail)

@app.post("/api/rag/main")
async def api_rag_main(args: dict) -> func.apibase.ApiResponse:
    func.rag.download(args)
    docs = func.rag.docs_load(args)
    if 'chunk_size' in args and args['chunk_size']:
        docs = func.rag.split(docs, args)
    vector_store = func.rag.vector(docs, args)
    result, detail = func.rag.search(vector_store, args)
    return res(0, result, detail)
