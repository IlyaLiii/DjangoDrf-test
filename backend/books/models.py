import uuid

from django.contrib.postgres.fields import ArrayField
from django.db.models import (
    Model,
    CharField,
    UUIDField,
    BigIntegerField,
    TextField,
    DateTimeField,
    Index
)


class UUIDMixin(Model):
    class Meta:
        abstract = True

    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class Book(UUIDMixin):
    STATUS_CHOICE = [
        ('PUBLISH', 'Опубликована'),
        ('MEAP', 'Предзаказ'),
    ]

    title = CharField(
        max_length=250,
        verbose_name='Тайтлы',
        null=False,
        blank=False,
    )
    page_count = BigIntegerField(
        verbose_name='Количество страниц',
        null=True,
        blank=False,
    )
    image = CharField(
        max_length=200,
        verbose_name='Обложка',
        null=True,
        blank=False,
    )
    status = CharField(
        max_length=20,
        choices=STATUS_CHOICE,
        verbose_name='Статус',
        null=False,
        blank=False,
    )
    authors = ArrayField(base_field=CharField(
        max_length=200,
        verbose_name='Авторы',
        blank=False,
    ))
    categories = ArrayField(base_field=CharField(
        max_length=50,
        verbose_name='Категории',
        blank=False,
        null=False,
    ))
    pub_date = DateTimeField(
        verbose_name='Дата публикации',
        null=True,
        blank=True,
    )
    isbn = CharField(
        verbose_name='ISBN',
        max_length=40,
        null=True,
        blank=True,
        unique=True,
    )
    short_description = TextField(
        verbose_name='Короткое описание',
        null=True,
        blank=False,
    )
    long_description = TextField(
        verbose_name='Полное описание',
        null=True,
        blank=False,
    )

    subcategories = ArrayField(base_field=CharField(
        max_length=50,
        verbose_name='Сабкатегории',
        blank=True,
    ), null=True,
        blank=True
    )

    class Meta:
        db_table = 'books'
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

        get_latest_by = 'pub_date'

        indexes = [
            Index(fields=['isbn', 'status', 'pub_date'],
                  name='%(class)s_main'),
            Index(fields=['isbn', 'status', 'pub_date'],
                  name='%(class)s_second'),
        ]

    def __str__(self):
        return self.title
