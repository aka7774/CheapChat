#!/usr/bin/bash

if [ ! -e venv ]; then
	python3 -m venv venv
	curl -kL https://bootstrap.pypa.io/get-pip.py | venv/bin/python

	venv/bin/python -m pip install transformers accelerate sentencepiece bitsandbytes scipy uvicorn fastapi
fi

venv/bin/python -m uvicorn main:app --port $1
