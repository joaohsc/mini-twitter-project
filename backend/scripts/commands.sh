#!/bin/sh

set -e

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  echo "🟡 Waiting for Postgres Database Startup ($POSTGRES_HOST $POSTGRES_PORT) ..."
  sleep 2
done

echo "✅ Postgres Database Started Successfully ($POSTGRES_HOST:$POSTGRES_PORT)"

if [[ $CREATE_SUPERUSER ]];
then
  python manage.py createsuperuser --no-input
fi

python manage.py collectstatic --noinput

if [[ $DEBUG ]];
then
  python manage.py makemigrations --noinput
fi

python manage.py migrate --noinput
python manage.py runserver 0.0.0.0:8000