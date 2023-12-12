from authors.forms import RegisterForm

from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import Http404
from django.utils.translation import get_language
from django.utils.translation import gettext as _


def register_view(req):
    if req.user.is_authenticated:
        return redirect('authors:dashboard')
    register_form_data = req.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)
    register_translate = _('Register')
    return render(
        req,
        'authors/pages/registerView.html',
        {
            'title': f'{register_translate} | ',
            'form': form,
            'form_action': reverse('authors:register_create'),
            'search_bar': False,
            'translation': get_language(),
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
