from django.test import TestCase
from django.urls import reverse, resolve
from authors import views
from recipes.tests.test_recipe_base import RecipeMixin


class RegisterViewTest(TestCase, RecipeMixin):
    def test_register_is_loading_correct_view(self):
        view = resolve(reverse('authors:register'))
        self.assertIs(view.func, views.register_view)

    def test_register_view_is_rendering_correct_template(self):
        response = self.client.get(reverse('authors:register'))
        self.assertTemplateUsed(response, 'authors/pages/registerView.html')

    def test_register_view_raises_404_if_there_is_no_post_request(self):
        response = self.client.get(reverse('authors:register_create'))
        self.assertEqual(response.status_code, 404)

    def test_register_view_redirects_to_dashboard_if_logged(self):
        self.make_user(username='DummyUser', password='#DummyPassw0rd')
        self.client.login(
            username='DummyUser',
            password='#DummyPassw0rd'
        )
        response = self.client.get(reverse('authors:register'), follow=True)
        content = response.content.decode('utf-8')
        self.assertIn('Your recipes', content)
