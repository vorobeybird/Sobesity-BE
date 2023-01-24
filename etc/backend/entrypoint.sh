#!/usr/bin/env bash


echo activate venv
source ./.venv/bin/activate
echo activated

exec ./wait-for-it.sh $POSTGRES_APP_HOST:$POSTGRES_APP_PORT -- "$@"
