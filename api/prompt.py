import os

import func.prompt
import func.apibase
from func.apibase import res

from main import app

from fastapi import Response


@app.post("/api/prompt/infer")
async def api_prompt_infer(args: dict) -> func.apibase.ApiResponse:
    content, messages = func.prompt.infer(args)
    return res(0, content, {'messages': messages})

@app.post("/api/prompt/stream")
async def api_prompt_stream(args: dict) -> Response:
    content, messages = func.prompt.infer(args)
    return Response(content=content, media_type="text/plain")

@app.post("/api/prompt/save")
async def api_prompt_save(args: dict) -> func.apibase.ApiResponse:
    func.prompt.save(args)
    return res(0, "saved.")
