         ###**Разворачивание проекта:

В папке backend:
1. Создать и активировать виртуальное окружение
2. Установить пакеты:
\```python
   python3 -m pip install -r requirements.txt
\```
3. Создать .env файл по аналогии с .env.example


         ###Running Locally with Docker
~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Build the images::

    docker-compose up --build

2. View the site at http://localhost:8000/


Static files such as CSS, JavaScript or image files can be found in the
``backend/static`` subdirectory.

Templates can be found in the ``backend/templates`` subdirectory.

         ###API
~~~~~~~~~~~~~~~~~~~~~~~~~~~

** API Находится по пути: <http://localhost:8000/api/v1/>

** SWAGGER: <http://localhost:8000/api/v1/swagger/>

** Book: <http://localhost:800/api/v1/books/>

** BookDetail: <http://localhost:800/api/v1/books/`uuid`> + 5 Books

** Categories: <http://localhost:800/api/v1/books/`uuid`/categories/>

** Subcategories: <http://localhost:800/api/v1/books/`uuid`/categories/subcategories>

** BooksByCategory:  <http://localhost:800/api/v1/category/`str`/>

** Login: <http://localhost:8000/api/v1/auth/login/>

** Feedback: <http://localhost:8000/feedback/>

** AdminPanel: <http://localhost:8000/admin/>





