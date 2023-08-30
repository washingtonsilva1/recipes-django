from django.test import TestCase
from django.urls import reverse, resolve
from recipes import views


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

    def test_recipes_home_view_status_code_200_ok(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEquals(response.status_code, 200)

    def test_recipes_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipes_home_view_recipes_not_found(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn('There are no recipes', response.content.decode('utf-8'))
