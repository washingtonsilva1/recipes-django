from . import views
from django.urls import path

from rest_framework.routers import SimpleRouter

rest_framework_router = SimpleRouter()
rest_framework_router.register(
    'api',
    viewset=views.AuthorsAPIViewSet,
    basename='authors-api'
)

app_name = 'authors'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('login/create/', views.login_create, name='login_create'),
    path('register/create/', views.register_create, name='register_create'),
    # Flake8: noqa
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/recipe/create/',
         views.DashboardRecipeCreate.as_view(), name='recipe_create'),
    path('dashboard/recipe/delete/',
         views.DashboardRecipeDelete.as_view(), name='recipe_delete'),
    path('dashboard/recipe/<int:id>/update/',
         views.DashboardRecipeEdit.as_view(), name='recipe_edit'),
    path('profile/<int:id>/', views.ProfileView.as_view(), name='profile'),
    path('profile/<int:pk>/update/',
         views.ProfileUpdateView.as_view(), name='profile_update'),
]

urlpatterns += rest_framework_router.urls
