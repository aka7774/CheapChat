import os

import func.sd
import func.apibase
from func.apibase import res

from main import app

from fastapi import Response


@app.post("/api/sd/main")
async def api_sd_main(args: dict) -> func.apibase.ApiResponse:
    webp_b64 = func.sd.infer(args)
    return res(0, webp_b64)

@app.post("/api/sd/raw")
async def api_llm_raw(args: dict) -> Response:
    content = func.sd.raw(args)
    return Response(content=content, media_type="image/webp")
