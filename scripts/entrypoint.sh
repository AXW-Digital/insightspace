#!/bin/sh
python manage.py migrate --noinput
python manage.py collectstatic --noinput
uwsgi --http :8000 --master --enable-threads --module insightproject.wsgi