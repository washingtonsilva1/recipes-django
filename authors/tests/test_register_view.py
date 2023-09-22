from django.test import TestCase
from django.urls import reverse, resolve
from authors import views


class RegisterViewTest(TestCase):
    def test_register_is_loading_correct_view(self):
        view = resolve(reverse('authors:register'))
        self.assertIs(view.func, views.register)

    def test_register_view_is_rendering_correct_template(self):
        response = self.client.get(reverse('authors:register'))
        self.assertTemplateUsed(response, 'authors/pages/registerView.html')
