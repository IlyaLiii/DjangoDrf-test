import datetime
import uuid
from uuid import uuid4
from dataclasses import dataclass, field


class Updateable(object):
    def update(self, new):
        for key, value in new.items():
            if hasattr(self, key):
                setattr(self, key, value)
@dataclass
class Book(Updateable):
    title: str
    pub_date: datetime.datetime
    page_count: int
    image: str
    status: str
    authors: list
    categories: list
    isbn: str
    short_description: any
    long_description: any
    id: uuid.UUID = field(default=uuid4())

