@echo off

set INSTALL_DIR=%~dp0
cd /d %INSTALL_DIR%
mkdir dl

bitsadmin /transfer nuget https://aka.ms/nugetclidl %INSTALL_DIR%dl\nuget.exe
%INSTALL_DIR%dl\nuget.exe install python -Version 3.10.13 -ExcludeVersion -OutputDirectory .
move python\tools python310
rmdir /s /q python

set PYTHON=%INSTALL_DIR%python310\python.exe
set PATH=%PATH%;%INSTALL_DIR%python310\Scripts
bitsadmin /transfer pip https://bootstrap.pypa.io/get-pip.py %INSTALL_DIR%dl\get-pip.py
%PYTHON% %INSTALL_DIR%dl\get-pip.py

%PYTHON% -m venv venv
venv\Scripts\python -m pip install -U pip
venv\Scripts\pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
venv\Scripts\pip install -U uvicorn fastapi gradio transformers accelerate sentencepiece scipy tiktoken einops transformers_stream_generator protobuf langchain langchain-community sentence-transformers openai websocket websocket-client rel pytchat more_itertools
venv\Scripts\pip install https://github.com/jllllll/bitsandbytes-windows-webui/releases/download/wheels/bitsandbytes-0.41.1-py3-none-win_amd64.whl
