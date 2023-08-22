from django.shortcuts import render
from utils.recipe.factory import make_recipe


def home(req):
    return render(req, 'recipes/pages/home.html',
                  {'recipes': [make_recipe() for _ in range(10)]})


def recipe(req, id):
    return render(req, 'recipes/pages/recipeView.html',
                  {'recipe': make_recipe(), 'is_detail_view': True})
