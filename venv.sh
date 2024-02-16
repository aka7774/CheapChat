#!/usr/bin/bash

python3 -m venv venv
curl -kL https://bootstrap.pypa.io/get-pip.py | venv/bin/python

venv/bin/python -m pip install -r requirements.txt

cd model
wget https://huggingface.co/skytnt/anime-seg/resolve/main/isnetis.ckpt
cd ..
