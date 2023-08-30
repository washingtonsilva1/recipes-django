from django.test import TestCase
from django.urls import reverse, resolve
from . import views


class RecipeURLsTest(TestCase):
    def test_recipes_home_url_is_correct(self):
        url = reverse('recipes:home')
        self.assertEqual(url, '/')

    def test_recipes_category_url_is_correct(self):
        url = reverse('recipes:category', kwargs=({'id': 1}))
        self.assertEqual(url, '/category/1/')

    def test_recipes_recipe_url_is_correct(self):
        url = reverse('recipes:recipe', args=[1])
        self.assertEqual(url, '/recipes/1/')


class RecipeViewsTest(TestCase):
    def test_recipes_home_view_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipes_category_view_is_correct(self):
        view = resolve(reverse('recipes:category', args=[1]))
        self.assertIs(view.func, views.category)

    def test_recipes_recipe_view_is_correct(self):
        view = resolve(reverse('recipes:recipe', args=[1]))
        self.assertIs(view.func, views.recipe)
