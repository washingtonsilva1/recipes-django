from django.shortcuts import render, get_list_or_404, get_object_or_404
from .models import Recipe


def home(req):
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')
    return render(req, 'recipes/pages/home.html',
                  {'recipes': recipes})


def category(req, id):
    recipes = get_list_or_404(Recipe.objects.filter(
        category__id=id,
        is_published=True).order_by('-id'))
    return render(req, 'recipes/pages/categoryView.html',
                  {'recipes': recipes,
                   'title': f'{recipes[0].category.name} - Category | '})


def recipe(req, id):
    recipe = get_object_or_404(Recipe, pk=id, is_published=True)
    return render(req, 'recipes/pages/recipeView.html',
                  {'recipe': recipe, 'is_detail_view': True,
                   'title': f'{recipe.title} | '})


def search(req):
    ...
