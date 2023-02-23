#!/usr/bin/env bash


source $VENV_FOLDER/bin/activate

exec /entr/wait-for-it.sh $POSTGRES_HOST:$POSTGRES_PORT -- "$@"
