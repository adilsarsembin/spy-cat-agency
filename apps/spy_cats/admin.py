from django.contrib import admin
from .models import Cat


@admin.register(Cat)
class CatAdmin(admin.ModelAdmin):
    list_display = ['name', 'breed', 'years_of_experience', 'salary']
    list_filter = ['breed']
    search_fields = ['name', 'breed']

