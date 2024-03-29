from ..models import Recipe
from utils.pagination import make_pagination
from tag.models import Tag

from django.conf import settings
from django.shortcuts import get_list_or_404
from django.http import Http404, JsonResponse
from django.db.models import Q
from django.forms.models import model_to_dict
from django.views.generic import ListView, DetailView
from django.utils.translation import get_language
from django.utils.translation import gettext as _


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
        qs = qs.select_related('user', 'category')
        qs = qs.prefetch_related('user__profile')
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        pagination = make_pagination(
            request=self.request,
            obj_list=ctx['recipes'],
            obj_per_page=settings.RECIPES_PER_PAGE,
            pages_to_display=settings.PAGES_TO_DISPLAY
        )
        ctx.update({
            'recipes': pagination['page'],
            'pagination_range': pagination['page_range'],
            'search_bar': True,
            'translation': get_language(),
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
        category_translation = _('Category')
        ctx.update({
            'title': f'{ctx.get("recipes")[0].category.name} - '
            f'{category_translation} | ',
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
        qs = qs.select_related('user')
        qs = qs.prefetch_related('tags')
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx.update({
            'is_detail_view': True,
            'title': f'{ctx.get("recipe").title} | ',
            'search_bar': False,
            'translation': get_language()
        })
        return ctx


class RecipeDetailApiView(RecipeDetailView):
    def render_to_response(self, context, **response_kwargs):
        recipe = self.get_context_data().get('recipe')
        recipe_dict = model_to_dict(recipe)
        if recipe_dict['cover']:
            recipe_dict['cover'] = self.request.build_absolute_uri('/') + \
                recipe_dict['cover'].url[1:]
        else:
            recipe_dict['cover'] = ''
        del ([
            recipe_dict['is_published'],
            recipe_dict['preparation_steps_is_html']
        ])
        recipe_dict.update({
            'user': recipe.user.username,
            'created_at': str(recipe.created_at),
            'updated_at': str(recipe.updated_at),
        })
        return JsonResponse(
            recipe_dict,
            safe=False
        )


class RecipesTagView(RecipesListView):
    template_name = 'recipes/pages/tag.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        slug = self.kwargs.get('slug', '')
        qs = qs.filter(
            tags__slug=slug
        )
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        slug = self.kwargs.get('slug', '')
        tag_title = Tag.objects.filter(
            slug=slug
        ).first()
        if not tag_title:
            tag_title = 'No recipes found'
        ctx.update({
            'title': tag_title,
        })
        return ctx
