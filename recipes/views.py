from django.shortcuts import render
# from utils.recipe.factory import make_recipe
from .models import Recipe
from django.http import Http404


def home(req):
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')
    return render(req, 'recipes/pages/home.html',
                  {'recipes': recipes})


def category(req, id):
    recipes = Recipe.objects.filter(
        category__id=id, is_published=True).order_by('-id')

    if not recipes:
        raise Http404('Not found')

    return render(req, 'recipes/pages/categoryView.html',
                  {'recipes': recipes,
                   'title': f'{recipes.first().category.name} - Category | '})


def recipe(req, id):
    recipe = Recipe.objects.get(pk=id)
    return render(req, 'recipes/pages/recipeView.html',
                  {'recipe': recipe, 'is_detail_view': True})
