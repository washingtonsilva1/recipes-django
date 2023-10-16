from django.test import TestCase
from django.urls import resolve, reverse
from authors import views


class LoginViewTest(TestCase):
    def test_login_is_loading_correct_view(self):
        view = resolve(reverse('authors:login'))
        self.assertIs(view.func, views.login_view)

    def test_login_view_is_rendering_correct_template(self):
        response = self.client.get(reverse('authors:login'))
        self.assertTemplateUsed(response, 'authors/pages/loginView.html')
