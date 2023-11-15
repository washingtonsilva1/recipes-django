from django.urls import reverse, resolve
from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeHomeViewTest(RecipeTestBase):
    def test_recipe_home_view_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func.view_class, views.RecipesHomeView)

    def test_recipe_home_view_returns_status_code_200_ok(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_view_returns_not_found_if_there_are_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn('There are no recipes', response.content.decode('utf-8'))

    def test_recipe_home_view_template_loads_recipes(self):
        needed_title = 'A New Recipe'
        self.make_recipe(title=needed_title)
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        self.assertIn(needed_title, content)

    def test_recipe_home_view_template_doesnt_load_unpublished_recipes(self):
        self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        self.assertIn('There are no recipes', content)
