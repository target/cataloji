#!/bin/sh

exec /usr/local/bin/gunicorn -b 0.0.0.0:5000 --access-logfile - "cataloji:create_app()"
