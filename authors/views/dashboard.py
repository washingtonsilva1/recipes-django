from recipes.models import Recipe
from utils.pagination import make_pagination
from authors.forms.edit_recipe_form import RecipeEditForm
from authors.forms.create_recipe_form import RecipeCreateForm

from django.conf import settings
from django.views import View
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.utils.text import slugify
from django.utils.translation import get_language
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_view(req):
    recipes = Recipe.objects.filter(
        user=req.user,
        is_published=False).order_by('-id')
    pagination = make_pagination(
        request=req,
        obj_list=recipes,
        obj_per_page=settings.RECIPES_PER_PAGE,
        pages_to_display=settings.PAGES_TO_DISPLAY,
    )
    return render(req, 'authors/pages/dashboardView.html', {
        'recipes': pagination['page'],
        'pagination_range': pagination['page_range'],
        'search_bar': False,
        'translation': get_language(),
    })


class DashboardRecipeView(View):
    def get_recipe(self, id):
        return get_object_or_404(
            Recipe,
            pk=id,
            user=self.request.user,
            is_published=False
        )

    def get_page(self, template, **kwargs):
        return render(
            self.request,
            template,
            {
                'translation': get_language(),
                **kwargs,
            }
        )


@method_decorator(
    login_required(redirect_field_name='next', login_url='authors:login'),
    name='dispatch'
)
class DashboardRecipeEdit(DashboardRecipeView):
    def get(self, *args, **kwargs):
        recipe = self.get_recipe(kwargs.get('id'))
        form = RecipeEditForm(instance=recipe)
        return self.get_page(
            template='authors/pages/edit_recipeView.html',
            form=form,
            recipe=recipe,
            search_bar=False,
            title=f'{recipe.title} | '
        )

    def post(self, *args, **kwargs):
        recipe = self.get_recipe(kwargs.get('id'))
        form = RecipeEditForm(
            data=self.request.POST or None,
            files=self.request.FILES or None,
            instance=recipe
        )
        if form.is_valid():
            r = form.save(commit=False)
            r.user = self.request.user
            r.slug = slugify(r.title)
            r.is_published = False
            r.preparation_steps_is_html = False
            r.save()
            messages.success(self.request, 'Your recipe has been updated!')
            return redirect('authors:dashboard')
        return self.get_page(
            template='authors/pages/edit_recipeView.html',
            form=form,
            recipe=recipe,
            search_bar=False,
            title=f'{recipe.title} | '
        )


@method_decorator(
    login_required(redirect_field_name='next', login_url='authors:login'),
    name='dispatch'
)
class DashboardRecipeCreate(DashboardRecipeView):
    def get(self, *args, **kwargs):
        form = RecipeCreateForm(
            data=self.request.POST or None,
            files=self.request.FILES or None
        )
        return self.get_page(
            template='authors/pages/create_recipeView.html',
            form=form,
            title='Create a recipe | ',
            search_bar=False
        )

    def post(self, *args, **kwargs):
        form = RecipeCreateForm(
            data=self.request.POST or None,
            files=self.request.FILES or None
        )
        if form.is_valid():
            r = form.save(commit=False)
            r.user = self.request.user
            r.is_published = False
            r.preparation_steps_is_html = False
            r.save()
            messages.success(self.request, 'Your recipe has been created!')
            return redirect('authors:dashboard')
        return self.get_page(
            template='authors/pages/create_recipeView.html',
            form=form,
            title='Create a recipe | ',
            search_bar=False
        )


@method_decorator(
    login_required(redirect_field_name='next', login_url='authors:login'),
    name='dispatch'
)
class DashboardRecipeDelete(DashboardRecipeView):
    def post(self, *args, **kwargs):
        recipe = self.get_recipe(self.request.POST.get('recipe_id'))
        recipe.delete()
        messages.success(self.request, 'Your recipe has been deleted!')
        return redirect('authors:dashboard')
