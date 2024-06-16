Разворачивание проекта:

В папке backend:
1) Создать и активировать виртуальное окружение
2) Установить пакеты:

    python3 -m pip install -r requirements.txt

3) Создать .env файл по аналогии с .


Running Locally with Docker
~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Build the images::

    docker-compose up --build

2. View the site at http://localhost:8000/



4) Выполнить миграции:

    python3 manage.py makemigrations
    python3 manage.py migrate

5) Перелить базу:

    python ../scripts/insert_data.py

6) Создать админа:

    python manage.py shell -c "exec(open('../scripts/create_users/create_base_superuser.py').read())"

Static files such as CSS, JavaScript or image files can be found in the
``backend/static`` subdirectory.

Templates can be found in the ``backend/templates`` subdirectory.






