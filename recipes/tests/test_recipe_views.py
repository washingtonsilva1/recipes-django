from django.urls import reverse, resolve
from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeViewsTest(RecipeTestBase):
    def test_recipes_home_view_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipes_home_view_returns_status_code_200_ok(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEquals(response.status_code, 200)

    def test_recipes_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipes_home_returns_not_found_if_there_are_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn('There are no recipes', response.content.decode('utf-8'))

    def test_recipes_home_template_loads_recipes(self):
        needed_title = 'A New Recipe'
        self.make_recipe(title=needed_title)
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        self.assertIn(needed_title, content)

    def test_recipes_home_template_doesnt_load_unpublished_recipes(self):
        self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        self.assertIn('There are no recipes', content)

    def test_recipes_category_view_is_correct(self):
        view = resolve(reverse('recipes:category', args=[1]))
        self.assertIs(view.func, views.category)

    def test_recipes_category_returns_404_if_not_exists(self):
        response = self.client.get(reverse('recipes:category', args=[1]))
        self.assertEqual(response.status_code, 404)

    def test_recipes_category_template_loads_recipes(self):
        needed_title = 'Recipe title'
        self.make_recipe(title=needed_title)
        response = self.client.get(reverse('recipes:category', args=[1]))
        content = response.content.decode('utf-8')
        self.assertIn(needed_title, content)

    def test_recipes_recipe_view_is_correct(self):
        view = resolve(reverse('recipes:recipe', args=[1]))
        self.assertIs(view.func, views.recipe)

    def test_recipes_recipe_returns_404_if_not_exists(self):
        response = self.client.get(reverse('recipes:recipe', args=[1]))
        self.assertEqual(response.status_code, 404)

    def test_recipes_recipe_template_loads_recipes(self):
        self.make_recipe(title='A new recipe arrives')
        response = self.client.get(reverse('recipes:recipe', args=[1]))
        self.assertIn('A new recipe arrives', response.content.decode('utf-8'))
