from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib import messages
from .forms import RegisterForm, LoginForm, RecipeEditForm
from recipes.models import Recipe
from utils.pagination import make_pagination
from django.urls import reverse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from recipes.views import PAGES_TO_DISPLAY, RECIPES_PER_PAGE


# Create your views here.
def register_view(req):
    if req.user.is_authenticated:
        return redirect('recipes:home')
    register_form_data = req.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)
    return render(
        req,
        'authors/pages/registerView.html',
        {
            'form': form,
            'form_action': reverse('authors:register_create'),
            'search_bar': False,
        }
    )


def register_create(req):
    if not req.POST:
        raise Http404()

    POST = req.POST
    req.session['register_form_data'] = POST
    form = RegisterForm(POST)
    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        messages.success(req, "Your user has been created, please log in!")
        del (req.session['register_form_data'])
        return redirect('authors:login')
    return redirect('authors:register')


def login_view(req):
    if req.user.is_authenticated:
        return redirect('authors:dashboard')
    login_form_data = req.session.get('login_form_data', None)
    form = LoginForm(login_form_data)
    return render(req, 'authors/pages/loginView.html', {
        'form': form,
        'form_action': reverse('authors:login_create'),
        'search_bar': False,
    })


def login_create(req):
    if not req.POST:
        raise Http404()

    POST = req.POST
    req.session['login_form_data'] = POST
    form = LoginForm(POST)
    redirect_to = 'authors:login'
    if form.is_valid():
        user_auth = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', ''),
        )
        if user_auth is not None:
            messages.success(req, 'You have logged in!')
            login(req, user_auth)
            del (req.session['login_form_data'])
            redirect_to = 'authors:dashboard'
        else:
            messages.error(req, 'Incorrect username or password')
    return redirect(redirect_to)


@login_required(login_url='authors:login', redirect_field_name='next')
def logout_view(req):
    if req.POST and req.POST.get('username') != req.user.username:
        return redirect('authors:login')
    logout(req)
    messages.info(req, 'You have sucessfully logged out')
    return redirect('authors:login')


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
