from django.contrib import admin
from .models import Category, Recipe


class CategoryAdmin(admin.ModelAdmin):
    ...


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    ...


# Register your models here.
admin.site.register(Category, CategoryAdmin)
