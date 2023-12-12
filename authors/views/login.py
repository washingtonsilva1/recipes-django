from authors.forms import LoginForm

from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import Http404
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.utils.translation import get_language


def login_view(req):
    if req.user.is_authenticated:
        return redirect('authors:dashboard')
    login_form_data = req.session.get('login_form_data', None)
    form = LoginForm(login_form_data)
    return render(req, 'authors/pages/loginView.html', {
        'form': form,
        'form_action': reverse('authors:login_create'),
        'search_bar': False,
        'translation': get_language(),
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
