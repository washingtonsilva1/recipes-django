from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.contrib import messages
from .forms import RegisterForm, LoginForm
from django.urls import reverse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required


# Create your views here.
def register_view(req):
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
            redirect_to = 'recipes:home'
        else:
            messages.error(req, 'Incorrect username or password')
    return redirect(redirect_to)


@login_required(login_url='authors:login', redirect_field_name='next')
def logout_view(req):
    if not req.POST or req.POST and req.POST.get('username') != req.user.username:
        return redirect('authors:login')
    logout(req)
    messages.info(req, 'You have sucessfully logged out')
    return redirect('authors:login')


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_view(req):
    return render(req, 'authors/pages/dashboardView.html', {
        'search_bar': False,
    })
