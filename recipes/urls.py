from . import views
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

recipes_api_router = SimpleRouter()
recipes_api_router.register(
    '',
    views.RecipesAPIViewSet,
    basename='recipes-api'
)

app_name = 'recipes'

urlpatterns = [
    path('', views.RecipesHomeView.as_view(), name='home'),
    path(
        'recipes/search/',
        views.RecipesSearchView.as_view(),
        name='search'
    ),
    path(
        'recipes/tags/<slug:slug>/',
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
    path(
        'recipes/api/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'recipes/api/token/verify/',
        TokenVerifyView.as_view(),
        name='token_verify'
    ),
    path(
        'recipes/api/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
    path(
        'recipes/api/',
        include(recipes_api_router.urls)
    ),
    path(
        'recipes/tags/api/<int:pk>/',
        views.tags_api_detail,
        name='tags_api_detail'
    ),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
