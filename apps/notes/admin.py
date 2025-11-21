from django.contrib import admin
from .models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['cat', 'target', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['content']
    raw_id_fields = ['cat', 'target']

