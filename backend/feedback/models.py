import uuid
from django.db.models import (
    Model,
    CharField,
    UUIDField,
    TextField,
    DateTimeField,
    EmailField,
)


class UUIDMixin(Model):
    class Meta:
        abstract = True

    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class Contact(UUIDMixin):
    username = CharField(max_length=200)
    phone = CharField(max_length=20)
    message = TextField(max_length=1000)
    email = EmailField(max_length=200)

    class Meta:
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратная связь'
        db_table = 'feedback'

    def __str__(self):
        return f'Письмо от {self.email}'
