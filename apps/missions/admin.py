from django.contrib import admin
from .models import Mission


@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    list_display = ['title', 'cat', 'is_completed', 'created_at']
    list_filter = ['is_completed', 'created_at']
    search_fields = ['title', 'description']
    raw_id_fields = ['cat']

