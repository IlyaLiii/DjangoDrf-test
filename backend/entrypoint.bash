#!/bin/bash
set -e

echo "Whait DB..."

echo ../debug/del_db.bash
#psql -h postgres -p 5432 -U $POSTGRES_USER -d $POSTGRES_DB -c "CREATE DATABASE $POSTGRES_DB"

echo "Running migrations"
python manage.py migrate --noinput
python manage.py createcachetable
python manage.py collectstatic --clear --noinput

echo python ../scripts/insert_data.py
python manage.py shell -c "exec(open('../scripts/create_users/create_base_superuser.py').read())"
python manage.py runserver localhost:8000


