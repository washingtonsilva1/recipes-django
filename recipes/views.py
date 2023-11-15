import os
from .models import Recipe
from django.shortcuts import get_list_or_404
from django.http import Http404
from utils.pagination import make_pagination
from django.db.models import Q

from django.views.generic import ListView, DetailView

RECIPES_PER_PAGE = int(os.environ.get('RECIPES_PER_PAGE', 6))
PAGES_TO_DISPLAY = int(os.environ.get('PAGES_TO_DISPLAY', 4))


class RecipesListView(ListView):
    model = Recipe
    context_object_name = 'recipes'
    template_name = 'recipes/pages/home.html'
    ordering = ['-id']

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            is_published=True
        )
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        pagination = make_pagination(
            request=self.request,
            obj_list=ctx['recipes'],
            obj_per_page=RECIPES_PER_PAGE,
            pages_to_display=PAGES_TO_DISPLAY
        )
        ctx.update({
            'recipes': pagination['page'],
            'pagination_range': pagination['page_range'],
            'search_bar': True
        })
        return ctx


class RecipesHomeView(RecipesListView):
    template_name = 'recipes/pages/home.html'


class RecipesCategoryView(RecipesListView):
    template_name = 'recipes/pages/categoryView.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = get_list_or_404(
            qs,
            category__id=self.kwargs.get('id'))
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx.update({
            'title': f'{ctx.get("recipes")[0].category.name} - Category | ',
        })
        return ctx


class RecipesSearchView(RecipesListView):
    template_name = 'recipes/pages/search.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        search_term = self.request.GET.get('q', '').strip()
        if not search_term:
            raise Http404()
        qs = qs.filter(
            Q(title__icontains=search_term) |
            Q(description__icontains=search_term)
        )
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        search_term = self.request.GET.get('q', '').strip()
        ctx.update({
            'additional_query': f'&q={search_term}',
            'search_term': search_term
        })
        return ctx


class RecipeDetailView(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipes/pages/recipeView.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            is_published=True
        )
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx.update({
            'is_detail_view': True,
            'title': f'{ctx.get("recipe").title} | ',
            'search_bar': False,
        })
        return ctx
