from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib import messages
from .forms import RegisterForm, LoginForm
from django.urls import reverse


# Create your views here.
def register(req):
    register_form_data = req.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)
    return render(req, 'authors/pages/registerView.html',
                  {
                      'form': form,
                      'form_action': reverse('authors:register_create'),
                  })


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
    return redirect('authors:register')


def login(req):
    form = LoginForm()
    return render(req, 'authors/pages/loginView.html', {
        'form': form,
        'form_action': reverse('authors:login_create'),
    })


def login_create(req):
    ...
