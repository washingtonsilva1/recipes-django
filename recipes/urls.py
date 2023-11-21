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
        'recipes/api/v1/',
        views.RecipeApiListView.as_view(),
        name='recipes_api'
    ),
    path(
        'recipes/tags/<slug:slug>',
        views.RecipesTagView.as_view(),
        name='search_tag'
    ),
    path(
        'recipes/category/<int:id>/',
        views.RecipesCategoryView.as_view(),
        name='category'
    ),
    path(
        'recipes/<int:pk>/',
        views.RecipeDetailView.as_view(),
        name='detail'
    ),
    path(
        'recipes/api/v1/<int:pk>/',
        views.RecipeDetailApiView.as_view(),
        name='detail_api'
    ),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
