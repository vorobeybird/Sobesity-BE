#!/usr/bin/env bash

gunicorn --reload -b 0.0.0.0:5150 --timeout 120 "sobesity.webapp:create_app()" --log-level INFO
