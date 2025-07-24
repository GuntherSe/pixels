#!/bin/bash
# start fullscreen coloring

# OLA reload (ArtNet might not be available):
curl http://127.0.0.1:9090/reload

source $HOME/.venv/bin/activate

if [ -d "$HOME/Dokumente" ]; then
  cd $HOME/Dokumente/python/pixels
else
  cd $HOME/Documents/python/pixels
fi

python colorscreen.py
