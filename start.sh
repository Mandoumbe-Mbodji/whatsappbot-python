#!/bin/bash

# Exit early on errors
set -eu

# Python buffers stdout. Without this, you won't see what you "print" in the Activity Logs
export PYTHONUNBUFFERED=true
chmod +w templates/styles.css

python3 -m pip install -U pip
pip install Flask Flask-SQLAlchemy

# Install the requirements
python3 -m pip install -r requirements.txt

# Run a glorious Python 3 server
python3 server.py