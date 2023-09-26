from django.shortcuts import render, redirect
from django.http import Http404
from .forms import RegisterForm


# Create your views here.
def register(req):
    register_form_data = req.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)
    return render(req, 'authors/pages/registerView.html', {'form': form})


def create(req):
    if not req.POST:
        raise Http404()

    POST = req.POST
    req.session['register_form_data'] = POST
    form = RegisterForm(POST)
    return redirect('authors:register')
