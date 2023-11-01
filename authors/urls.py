from . import views
from django.urls import path
from django.http import HttpResponse


app_name = 'authors'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('login/create/', views.login_create, name='login_create'),
    path('register/create/', views.register_create, name='register_create'),
    # Flake8: noqa
    path('dashboard/', views.dashboard_view, name='dashboard'),
]
