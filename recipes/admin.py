from django.contrib import admin
from .models import Category, Recipe


class CategoryAdmin(admin.ModelAdmin):
    ...


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


# Register your models here.
admin.site.register(Category, CategoryAdmin)
