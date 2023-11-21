from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline

from .models import Category, Recipe
from tag.models import Tag


class CategoryAdmin(admin.ModelAdmin):
    ...


class TagInline(GenericStackedInline):
    model = Tag
    fields = ('name',)
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at',
                    'is_published', 'user')
    list_display_links = ('title',)
    list_editable = ('is_published',)
    search_fields = ('title', 'description', 'preparation_steps', 'slug')
    list_filter = ('is_published', 'category', 'user',
                   'preparation_steps_is_html')
    ordering = ('-id',)
    list_per_page = 10
    prepopulated_fields = {
        'slug': ('title',)
    }
    inlines = [
        TagInline,
    ]


# Register your models here.
admin.site.register(Category, CategoryAdmin)
