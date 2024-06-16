from datetime import datetime
import json
from pathlib import Path
from typing import Any

from bs4 import BeautifulSoup

import requests

FILE_NAME = 'books.json'
PROJECT_DIR = Path.cwd().parent

FILE_PATH = PROJECT_DIR / f'data/{FILE_NAME}'


class Parser:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_json(self) -> list:
        with open(self.file_path, 'r') as f:
            json_data = json.load(f)

        return json_data

    def get_len_data(self) -> int:
        return len(self.load_json())

    @staticmethod
    def check_isbn_is_digit(isbn: str) -> bool:
        return True if isbn.isdigit() else False

    def get_isbn(self):
        # В одном item нет isbn
        pass

    ###publishedDate
    def formating_pub_date(self, data: str) -> datetime:
        return datetime.strptime(data.split('T')[0], '%Y-%m-%d')

    # def get_pub_date(self, isbn: str) ->:
    #
    # r = requests.get(f'https://books.google.com/books?vid={isbn}')
    #
    # soup = BeautifulSoup(r.text, 'html.parser')
    # div = soup.find('div', class_='bookinfo_sectionwrap')
    # rows = div.find_all('span')
    # return rows[5].text

    ##categories
    def p_and_s_validate(self, categories: list) -> list:
        for i in categories:
            if i == 'P':
                categories[categories.index(i)] = 'Perl'
            if i == 'S':
                categories[categories.index(i)] = 'Software'
        return categories

    def remove_empty_category(self, categories: list):
        return [x for x in categories if x != '']

    #authors
    def remove_empty_authors(self, authors: list) -> list:
        return [x for x in authors if x != '']

    def remove_extra_in_authors(self, authors: list) -> list:
        if 'friends' in authors:
            authors.remove('friends')
        elif 'editors' in authors:
            authors.remove('editors')
        return authors

    def validate(self) -> list:
        json_data = self.load_json()

        for item in json_data:

            # валидация pageCount
            # if item.get('pageCount') == 0:
            #     print('kek', item.get('pageCount'))
            #     item.update(pageCount=self.get_page_count(item.get('isbn')))
            #     print(item.get('pageCount'))

            # валидация thumbnailUrl
            if not item.get('thumbnailUrl'):
                item.update(thumbnailUrl=None)

            # валидация longDescription
            if not item.get('longDescription'):
                item.update(longDescription=None)

            # валидация shortDescription
            if not item.get('shortDescription'):
                item.update(shortDescription=None)

            # валидация publishedDate
            if item.get('publishedDate'):
                dt = self.formating_pub_date(item.get('publishedDate').get('$date'))
                item.update(publishedDate=dt)

            if not item.get('publishedDate'):
                item.update(publishedDate=None)

            # валидация isbn-номера
            # try:
            #     if not self.check_isbn_is_digit(item.get('isbn')):
            #         item.update(isbn=self.replace_chr_in_isbn(item.get('isbn')))
            #
            # except AttributeError as e:
            #     item.update(isbn=None)
            if not item.get('isbn'):
                item.update(isbn=None)

            # валидация categories
            if not item.get('categories'):
                item.update(categories=['New'])
            elif 'P' in item.get('categories') or 'S' in item.get('categories'):
                item.update(categories=self.p_and_s_validate(item.get('categories')))
            elif '' in item.get('categories'):
                item.update(categories=self.remove_empty_category(item.get('categories')))

            # валидация authors
            if '' in item.get('authors'):
                item.update(authors=self.remove_empty_authors(item.get('authors')))
            if 'friends' in item.get('authors') or 'editors' in item.get('authors'):
                item.update(authors=self.remove_extra_in_authors(item.get('authors')))

        return json_data

    def check_post_data(self, **kwargs) -> dict:

        if not kwargs.get('shortDescription'):
            kwargs.update(shortDescription='')

        elif not kwargs.get('longDescription'):
            kwargs.update(longDescription='')

        elif not kwargs.get('publishedDate'):
            kwargs.update(publishedDate=None)

        elif not kwargs.get('isbn'):
            kwargs.update(isbn=0)

        return kwargs.get('item')
