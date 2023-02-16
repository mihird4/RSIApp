#!/bin/sh
exec gunicorn --certfile cert.pem --keyfile key.pem -w 4 -b :5000 --access-logfile - --error-logfile - -t 3000 main:app
