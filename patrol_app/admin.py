from django.contrib import admin
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name', 'address')
    search_fields = ('first_name', 'last_name', 'address')

admin.site.register(CustomUser, CustomUserAdmin)