from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


app_name = 'recipes'

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<int:id>/', views.category, name='category'),
    path('recipes/<int:id>/', views.recipe, name='recipe'),
    path('recipes/search/', lambda request: ..., name='search'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
