from django.shortcuts import render
from .forms import RegisterForm


# Create your views here.
def register(req):
    if req.POST:
        form = RegisterForm(req.POST)
    else:
        form = RegisterForm()
    return render(req, 'authors/pages/registerView.html', {'form': form})
