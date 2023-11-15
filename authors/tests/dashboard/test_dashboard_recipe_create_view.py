from authors import views
import pytest
from .test_dashboard_base import DashboardTestBase
from django.urls import reverse, resolve


@pytest.mark.fast
class DashboardRecipeCreateViewTest(DashboardTestBase):
    def test_recipe_create_view_is_loading_correct_view(self):
        view = resolve(reverse('authors:recipe_create'))
        self.assertIs(view.func.view_class, views.DashboardRecipeCreate)

    def test_recipe_create_view_is_rendering_correct_template(self):
        response = self.client.get(reverse('authors:recipe_create'))
        self.assertTemplateUsed(response,
                                'authors/pages/edit_recipeView.html')

    def test_recipe_create_view_redirects_if_not_logged(self):
        self.client.logout()
        response = self.client.get(
            reverse('authors:recipe_create'),
            follow=True
        )
        content = response.content.decode('utf-8')
        self.assertIn('<h2>Login</h2>', content)
