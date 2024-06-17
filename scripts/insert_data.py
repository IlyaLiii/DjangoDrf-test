import os
import uuid
from dataclasses import fields, astuple
from pathlib import Path

from load_json import Parser
import psycopg2
from psycopg2.extras import register_uuid
from dotenv import dotenv_values

from load_json import Parser
from books import Book

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = os.path.join(BASE_DIR, 'backend/.env')

FILE_NAME = 'books.json'
PROJECT_DIR = Path.cwd().parent

FILE_PATH = PROJECT_DIR / f'data/{FILE_NAME}'

CONFIG = {
    **dotenv_values(ENV_PATH)
}

DSN = {
    'dbname': 'DB',
    'user': 'USER',
    'password': 'PASSWORD',
    'host': 'postgres',
    'port': 5432,
}


class Loader:
    def __init__(self, DSN: dict):
        self.DSN = DSN

    def load_into_pg(self):
        with psycopg2.connect(**self.DSN) as pg_conn:
            cursor = pg_conn.cursor()
            prsr = Parser(FILE_PATH)
            json_data = prsr.validate()
            psycopg2.extras.register_uuid()

            for item in json_data:
                dataclass_dict_data = Book(
                    id=uuid.uuid4(),
                    title=item.get('title'),
                    pub_date=item.get('publishedDate'),
                    page_count=item.get('pageCount'),
                    image=item.get('thumbnailUrl'),
                    status=item.get('status'),
                    authors=item.get('authors'),
                    categories=item.get('categories'),
                    isbn=item.get('isbn'),
                    short_description=item.get('shortDescription'),
                    long_description=item.get('longDescription'),
                )

                column_names = [field.name for field in fields(dataclass_dict_data)]
                col_count = ', '.join(["%s"] * len(column_names))
                bind_values = cursor.mogrify(
                    '({})'.format(col_count), astuple(dataclass_dict_data),
                ).decode("utf-8")
                string_column_names = ", ".join(column_names)
                query = (
                    'INSERT INTO books ({}) VALUES {} \
                    ON CONFLICT (isbn) DO NOTHING'.format(
                        string_column_names, bind_values,
                    ),
                )
                cursor.execute(query[0])
