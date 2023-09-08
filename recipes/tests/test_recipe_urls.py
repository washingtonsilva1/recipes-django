from django.test import TestCase
from django.urls import reverse


class RecipeURLsTest(TestCase):
    def test_recipes_home_url_is_correct(self):
        url = reverse('recipes:home')
        self.assertEqual(url, '/')

    def test_recipes_category_url_is_correct(self):
        url = reverse('recipes:category', kwargs=({'id': 1}))
        self.assertEqual(url, '/recipes/category/1/')

    def test_recipes_recipe_url_is_correct(self):
        url = reverse('recipes:recipe', args=[1])
        self.assertEqual(url, '/recipes/1/')

    def test_recipes_search_url_is_correct(self):
        url = reverse('recipes:search')
        self.assertEqual(url, '/recipes/search/')
