#!/bin/bash

## User defined vars
USE_VENV=true # Use virtual environmnet for python
VENV_DIR= # /path/to/venv/dir

## Scripts
VENV_ACTIVATE="$VENV_DIR/bin/activate"

if [ $USE_VENV ]; then
    echo "Checking if $VENV_DIR exists"

    if [ -e $VENV_ACTIVATE ]; then
        source $VENV_ACTIVATE
    else
        echo "$VENV_ACTIVATE does not exist. Create virtual Python environment before running this script."
        exit 1
    fi
fi

python3 -m pip install jsonpatch
python3 -m pip install PyYAML==6.0.3
python3 -m pip install ansible-core==2.20
python3 -m pip install kubernetes==35.0.0
ansible-galaxy collection install community.general
ansible-galaxy collection install kubernetes.core
