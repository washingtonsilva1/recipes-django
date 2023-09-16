from django.core.paginator import Paginator
from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import Http404
from .models import Recipe
from django.db.models import Q


def home(req):
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')
    paginator = Paginator(recipes, 9)

    page_number = req.GET.get('page', '1')
    page_obj = paginator.get_page(page_number)
    return render(req, 'recipes/pages/home.html',
                  {'recipes': page_obj})


def category(req, id):
    recipes = get_list_or_404(Recipe.objects.filter(
        category__id=id,
        is_published=True).order_by('-id'))
    return render(req, 'recipes/pages/categoryView.html',
                  {'recipes': recipes,
                   'title': f'{recipes[0].category.name} - Category | '})


def detail(req, id):
    recipe = get_object_or_404(Recipe, pk=id, is_published=True)
    return render(req, 'recipes/pages/recipeView.html',
                  {'recipe': recipe, 'is_detail_view': True,
                   'title': f'{recipe.title} | '})


def search(req):
    search_term = req.GET.get('q', '').strip()
    if not search_term:
        raise Http404()
    recipes = Recipe.objects.filter(
        Q(is_published=True),
        Q(title__icontains=search_term) |
        Q(description__icontains=search_term),
    ).order_by('-id')
    return render(req, 'recipes/pages/search.html', context={
        'search_term': search_term,
        'recipes': recipes,
    })
