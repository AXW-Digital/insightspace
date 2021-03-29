#!/bin/sh
python manage.py migrate --noinput
python manage.py collectstatic --noinput
uwsgi --socket :8000 --master --enable-threads -b 32768 --module insightproject.wsgi