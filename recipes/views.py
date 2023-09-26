import os
from .models import Recipe
from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import Http404
from utils.pagination import make_pagination
from django.db.models import Q

PER_PAGE = int(os.environ.get('PER_PAGE', 6))
PAGES_DISPLAY = int(os.environ.get('PAGES_DISPLAY', 4))


def home(req):
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')
    pagination = make_pagination(
        request=req,
        obj_list=recipes,
        obj_per_page=PER_PAGE,
        pages_to_display=PAGES_DISPLAY
    )
    return render(req, 'recipes/pages/home.html',
                  {'recipes': pagination['page'],
                   'pagination_range': pagination['page_range']})


def category(req, id):
    recipes = get_list_or_404(Recipe.objects.filter(
        category__id=id,
        is_published=True).order_by('-id'))
    pagination = make_pagination(
        request=req,
        obj_list=recipes,
        obj_per_page=PER_PAGE,
        pages_to_display=PAGES_DISPLAY
    )
    return render(req, 'recipes/pages/categoryView.html',
                  {'recipes': pagination['page'],
                   'pagination_range': pagination['page_range'],
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
    pagination = make_pagination(
        request=req,
        obj_list=recipes,
        obj_per_page=9,
        pages_to_display=4
    )
    return render(req, 'recipes/pages/search.html', context={
        'search_term': search_term,
        'additional_query': f'&q={search_term}',
        'recipes': pagination['page'],
        'pagination_range': pagination['page_range']
    })
