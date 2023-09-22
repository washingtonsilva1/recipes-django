from django.shortcuts import render


# Create your views here.
def register(req):
    return render(req, 'authors/pages/registerView.html')
