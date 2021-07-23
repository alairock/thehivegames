#!/usr/bin/env sh

####
# IMPORTANT:
# This will start the backend portion
# but you will also need to run the frontend separately.
# Use ./startfedev.sh to start frontend and proxy
####


export PYTHONPATH=$PYTHONPATH:.


# if the poetry binary is not installed, install it
if ! [ -x "$(command -v poetry)" ]; then
    echo "Installing poetry..."
    if ! [ -x "$(command -v pipx)" ]; then
        echo "Installing poetry using conventional methods"
        curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
    else
        echo "Installing poetry using pipx"
        pipx install poetry
    fi
else
    echo "poetry is already installed"
fi

poetry install
poetry run python run.py
