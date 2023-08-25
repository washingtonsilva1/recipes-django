from django.shortcuts import render
from utils.recipe.factory import make_recipe
from .models import Recipe


def home(req):
    recipes = Recipe.objects.all().order_by('-id')
    return render(req, 'recipes/pages/home.html',
                  {'recipes': recipes})


def category(req, id):
    recipes = Recipe.objects.filter(category__id=id).order_by('-id')
    return render(req, 'recipes/pages/home.html',
                  {'recipes': recipes})


def recipe(req, id):
    return render(req, 'recipes/pages/recipeView.html',
                  {'recipe': make_recipe(), 'is_detail_view': True})
