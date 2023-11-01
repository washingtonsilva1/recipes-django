import pytest
from django.test import TestCase
from authors import views
from django.urls import resolve, reverse
from recipes.tests.test_recipe_base import RecipeMixin


@pytest.mark.fast
class DashboardViewUnitTest(TestCase, RecipeMixin):
    def test_dashboard_loads_correct_view(self):
        view = resolve(reverse('authors:dashboard'))
        self.assertIs(view.func, views.dashboard_view)

    def test_dashboard_render_correct_template(self):
        self.user_data = {
            'username': 'DummyUser',
            'password': '#DummyPassw0rd',
        }
        self.make_user(
            username=self.user_data['username'],
            password=self.user_data['password'],
        )
        self.client.login(
            username=self.user_data['username'],
            password=self.user_data['password'],
        )
        response = self.client.get(reverse('authors:dashboard'))
        self.assertTemplateUsed(response, 'authors/pages/dashboardView.html')
