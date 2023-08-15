from django.http import HttpResponse
from django.shortcuts import render


def home(req):
    return render(req, 'recipes/home.html',
                  context={'name': 'Deivison'}, status=200)


def contact(req):
    return HttpResponse('Contato!')


def about(req):
    return HttpResponse('Sobre!')
