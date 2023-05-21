from django.contrib import admin
from .models import User
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['username','name','gender']
    list_filter = ['username', 'name', 'gender']
    search_fields = ['username', 'name']

admin.site.register(User,UserAdmin)