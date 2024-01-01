import os

import func.prompt
import func.llm
import func.apibase
from func.apibase import res

from main import app

from fastapi import Response


@app.post("/api/llm/main")
async def api_llm_main(args: dict) -> func.apibase.ApiResponse:
    content, messages = func.prompt.infer(args)
    return res(0, content, {'messages': messages})

@app.post("/api/llm/raw")
async def api_llm_raw(args: dict) -> Response:
    content, messages = func.prompt.infer(args)
    return Response(content=content, media_type="text/plain")

@app.post("/api/llm/save")
async def api_llm_save(args: dict) -> func.apibase.ApiResponse:
    func.llm.save(args)
    return res(0, "saved.")
