from django.contrib import admin

from books.models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date', 'isbn', 'short_description')
    list_filter = ('status',)
    search_fields = ('title', 'authors', 'status', 'pub_date',)
