import pytest
from authors import views
from django.urls import reverse, resolve
from .test_dashboard_base import DashboardTestBase


@pytest.mark.fast
class DashboardRecipeEditViewTest(DashboardTestBase):
    def test_dashboard_recipe_edit_is_loading_correct_view(self):
        view = resolve(reverse('authors:recipe_edit', kwargs={'id': 1}))
        self.assertIs(view.func.view_class, views.DashboardRecipeEdit)

    def test_dashboard_recipe_edit_is_using_correct_template(self):
        self.create_unpublished_recipe()
        response = self.client.get(reverse('authors:recipe_edit',
                                           kwargs={'id': 1}))
        self.assertTemplateUsed(response,
                                'authors/pages/edit_recipeView.html')
