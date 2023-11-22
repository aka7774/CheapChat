import os

import cheapchat

from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )

@app.post("/api/chat")
async def api_chat(args: dict) -> Response:
    return Response(content=cheapchat.chat(args), media_type="text/plain")


# init
cheapchat.model_set('elyza/ELYZA-japanese-Llama-2-7b-fast-instruct', 'int4')
