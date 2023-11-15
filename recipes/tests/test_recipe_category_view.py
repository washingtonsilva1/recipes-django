from django.urls import reverse, resolve
from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeCategoryViewTest(RecipeTestBase):
    def test_recipe_category_view_is_correct(self):
        view = resolve(reverse('recipes:category', args=[1]))
        self.assertIs(view.func.view_class, views.RecipesCategoryView)

    def test_recipe_category_view_returns_404_if_there_are_no_recipes(self):
        response = self.client.get(reverse('recipes:category', args=[1]))
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_view_template_loads_recipes(self):
        needed_title = 'Recipe title'
        recipe = self.make_recipe(title=needed_title)
        response = self.client.get(
            reverse('recipes:category', args=[recipe.category.id]))
        content = response.content.decode('utf-8')
        self.assertIn(needed_title, content)

    def test_recipe_category_view_doesnt_loads_unpublished_recipes(self):
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(
            reverse('recipes:category', kwargs={'id': recipe.category.id}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_view_title_displays_category_title(self):
        category_needed = 'A new category'
        recipe = self.make_recipe(
            category={'category_name': category_needed}
        )
        response = self.client.get(
            reverse('recipes:category', args=(recipe.category.id,))
        )
        self.assertEqual(
            f'{category_needed} - Category | ',
            response.context['title']
        )
