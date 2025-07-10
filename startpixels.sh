#!/bin/bash
# start pixels

# OLA reload (ArtNet might not be available):
curl http://127.0.0.1:9090/reload

source /home/gunther/.venv/bin/activate

cd ~/Dokumente/python/pixels
python pixels.py
