#! /bin/sh

source venv/bin/activate

exec gunicorn -b :2000 --access-logfile - --error-logfile - pi:app
