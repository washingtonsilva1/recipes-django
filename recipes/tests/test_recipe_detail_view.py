from django.urls import reverse, resolve
from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeDetailViewTest(RecipeTestBase):
    def test_recipe_detail_view_is_correct(self):
        view = resolve(reverse('recipes:detail', args=[1]))
        self.assertIs(view.func, views.detail)

    def test_recipe_detail_view_returns_404_if_not_exists(self):
        response = self.client.get(reverse('recipes:detail', args=[1]))
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_view_template_loads_recipes(self):
        recipe = self.make_recipe(title='A new recipe arrives')
        response = self.client.get(reverse('recipes:detail', args=[recipe.id]))
        self.assertIn('A new recipe arrives', response.content.decode('utf-8'))

    def test_recipe_detail_view_template_doenst_load_unpublished_recipe(self):
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(
            reverse('recipes:detail', kwargs={'id': recipe.id}))
        self.assertEqual(response.status_code, 404)
