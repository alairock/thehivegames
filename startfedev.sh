#!/usr/bin/env sh

####
# IMPORTANT:
# This will start the frontend hotreloading/autoreloading and proxy
# but you will also need to run the backend separately.
# Use ./startbedev.sh to run the backend
####


export PYTHONPATH=$PYTHONPATH:.

# Start database
./scripts/startpg.sh

# run migration
poetry run alembic upgrade head

npm run start --prefix frontend
