from django.test import TestCase
from django.urls import reverse, resolve
from authors import views


class RegisterViewTest(TestCase):
    def test_register_is_loading_correct_view(self):
        view = resolve(reverse('authors:register'))
        self.assertIs(view.func, views.register_view)

    def test_register_view_is_rendering_correct_template(self):
        response = self.client.get(reverse('authors:register'))
        self.assertTemplateUsed(response, 'authors/pages/registerView.html')

    def test_register_view_raises_404_if_there_is_no_post_request(self):
        response = self.client.get(reverse('authors:register_create'))
        self.assertEqual(response.status_code, 404)
