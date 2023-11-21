from .models import Tag
from django.contrib import admin


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug']
    list_display_links = ['id', 'slug']
    list_editable = ('name',)
    list_per_page = 10
    search_fields = ['id', 'name', 'slug']
    ordering = ('-id'),
    prepopulated_fields = {
        'slug': ('name',),
    }
