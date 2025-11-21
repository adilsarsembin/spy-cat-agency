from django.contrib import admin
from .models import Target


@admin.register(Target)
class TargetAdmin(admin.ModelAdmin):
    list_display = ['name', 'mission', 'is_completed', 'created_at']
    list_filter = ['is_completed', 'created_at']
    search_fields = ['name', 'description']
    raw_id_fields = ['mission']

