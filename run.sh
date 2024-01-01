#!/usr/bin/bash

if [ ! -e venv ]; then
	bash venv.sh
fi

venv/bin/python -m uvicorn main:app --host '0.0.0.0' --port $1
