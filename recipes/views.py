from django.shortcuts import render


def home(req):
    return render(req, 'recipes/home.html')
