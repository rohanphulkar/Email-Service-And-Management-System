from django.contrib import admin
from .models import Email

class EmailAdmin(admin.ModelAdmin):
    list_display = ['subject', 'sender', 'get_recipient']
    list_filter = ['sender']
    search_fields = ['subject', 'sender']

admin.site.register(Email, EmailAdmin)