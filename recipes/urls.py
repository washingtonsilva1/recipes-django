from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


app_name = 'recipes'

urlpatterns = [
    path('', views.RecipesHomeView.as_view(), name='home'),
    path(
        'recipes/search/',
        views.RecipesSearchView.as_view(),
        name='search'
    ),
    path(
        'recipes/category/<int:id>/',
        views.RecipesCategoryView.as_view(),
        name='category'
    ),
    path('recipes/<int:id>/', views.detail, name='detail'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
