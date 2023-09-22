from . import views
from django.urls import path


app_name = 'authors'

urlpatterns = [
    path('register/', views.register, name='register'),
]
