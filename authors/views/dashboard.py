from recipes.models import Recipe
from recipes.views import PAGES_TO_DISPLAY, RECIPES_PER_PAGE
from utils.pagination import make_pagination
from authors.forms.edit_recipe_form import RecipeEditForm
from authors.forms.create_recipe_form import RecipeCreateForm

from django.shortcuts import redirect, render, get_object_or_404
from django.http import Http404
from django.utils.text import slugify
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_view(req):
    recipes = Recipe.objects.filter(
        user=req.user,
        is_published=False).order_by('-id')
    pagination = make_pagination(
        request=req,
        obj_list=recipes,
        obj_per_page=RECIPES_PER_PAGE,
        pages_to_display=PAGES_TO_DISPLAY,
    )
    return render(req, 'authors/pages/dashboardView.html', {
        'recipes': pagination['page'],
        'pagination_range': pagination['page_range'],
        'search_bar': False,
    })


@login_required(redirect_field_name='next', login_url='authors:login')
def dashboard_recipe_edit_view(req, id):
    recipe = get_object_or_404(Recipe,
                               pk=id, user=req.user, is_published=False)
    form = RecipeEditForm(data=req.POST or None,
                          files=req.FILES or None, instance=recipe)

    if form.is_valid():
        form_recipe = form.save(commit=False)
        form_recipe.slug = slugify(form_recipe.title)
        form_recipe.user = req.user
        form_recipe.is_published = False
        form_recipe.preparation_steps_is_html = False
        form_recipe.save()
        messages.success(req, 'Your recipe has been updated!')
        return redirect('authors:dashboard')

    return render(req, 'authors/pages/edit_recipeView.html', {
        'recipe': recipe,
        'form': form,
        'title': f'{recipe.title} | ',
        'search_bar': False,
    })


@login_required(redirect_field_name='next', login_url='authors:login')
def dashboard_recipe_create_view(req):
    form = RecipeCreateForm(data=req.POST or None, files=req.FILES or None)

    if form.is_valid():
        recipe = form.save(commit=False)
        recipe.user = req.user
        recipe.preparation_steps_is_htmp = False
        recipe.is_published = False
        recipe.save()
        messages.success(req, 'Your recipe has been created!')
        return redirect('authors:dashboard')

    return render(req, 'authors/pages/create_recipeView.html', {
        'title': 'Create a recipe | ',
        'search_bar': False,
        'form': form,
    })


@login_required(redirect_field_name='next', login_url='authors:login')
def dashboard_recipe_delete_view(req):
    if not req.POST:
        raise Http404()

    post_data = req.POST

    recipe = get_object_or_404(
        Recipe,
        id=post_data.get('recipe_id'),
        user=req.user,
        is_published=False
    )
    recipe.delete()
    messages.success(req, 'Your recipe has been deleted!')
    return redirect('authors:dashboard')
