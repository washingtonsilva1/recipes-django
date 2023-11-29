from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required


@login_required(login_url='authors:login', redirect_field_name='next')
def logout_view(req):
    if not req.POST:
        return redirect('authors:dashboard')

    if req.POST.get('username') and \
            req.POST.get('username') != req.user.username:
        return redirect('authors:dashboard')
    logout(req)
    messages.info(req, 'You have sucessfully logged out')
    return redirect('authors:login')
