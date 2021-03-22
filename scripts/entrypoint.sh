#!/bin/sh

set -e

python manage.py migrate --noinput
python manage.py collectstatic --noinput

uwsgi --socket :8000 --master --enable-threads --module insightproject.wsgi