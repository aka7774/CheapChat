#!/usr/bin/bash

if [ ! -e venv ]; then
	bash venv.sh
fi

venv/bin/python -m uvicorn main:app --port $1
