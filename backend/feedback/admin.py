from django.contrib import admin
from feedback.models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('email', 'username')
    search_fields = ('username', 'email')
