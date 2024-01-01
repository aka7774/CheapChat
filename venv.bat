set PYTHON=python.exe

%PYTHON% -m venv venv
venv\Scripts\activate.bat
python -m pip install -U pip
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
pip install bitsandbytes-windows
pip install -U uvicorn fastapi gradio transformers accelerate sentencepiece scipy tiktoken einops transformers_stream_generator protobuf langchain sentence-transformers faiss-gpu openai websocket websocket-client rel pytchat more_itertools
pip install https://github.com/jllllll/bitsandbytes-windows-webui/releases/download/wheels/bitsandbytes-0.41.1-py3-none-win_amd64.whl
