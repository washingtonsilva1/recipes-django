from django.test import TestCase
from django.urls import resolve, reverse

from authors import views
from recipes.tests.test_recipe_base import RecipeMixin


class LoginViewTest(TestCase, RecipeMixin):
    def test_login_is_loading_correct_view(self):
        view = resolve(reverse('authors:login'))
        self.assertIs(view.func, views.login_view)

    def test_login_view_is_rendering_correct_template(self):
        response = self.client.get(reverse('authors:login'))
        self.assertTemplateUsed(response, 'authors/pages/loginView.html')

    def test_login_view_redirects_to_dashboard_if_logged(self):
        self.make_user(username='DummyUser', password='@DummyPassw0rd')
        self.client.login(username='DummyUser', password='@DummyPassw0rd')
        response = self.client.get(reverse('authors:login'))
        self.assertRedirects(response, reverse('authors:dashboard'))
