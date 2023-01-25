#!/usr/bin/env bash


source /code/.venv/bin/activate

exec /entr/wait-for-it.sh $POSTGRES_HOST:$POSTGRES_PORT -- "$@"
