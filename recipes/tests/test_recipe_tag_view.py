from .test_recipe_base import RecipeTestBase
from recipes.views import RecipesTagView
from tag.models import Tag

from django.urls import resolve, reverse


class RecipeTagViewTest(RecipeTestBase):
    def test_recipe_tag_view_is_using_correct_view(self):
        view = resolve(reverse('recipes:search_tag', args=['any-thing']))
        self.assertIs(view.func.view_class, RecipesTagView)

    def test_recipe_tag_view_is_rendering_correct_template(self):
        response = self.client.get(
            reverse('recipes:search_tag', args=['any-thing'])
        )
        self.assertTemplateUsed(response, 'recipes/pages/tag.html')

    def test_recipe_tag_view_shows_tag_on_title(self):
        # CASE 1
        # The tag doesn't exist.
        # Expected title: No recipes found - Tag | Recipes
        response = self.client.get(
            reverse('recipes:search_tag', args=['any-thing'])
        )
        content = response.content.decode('utf-8')
        self.assertIn(
            '<title>No recipes found - Tag | Recipes</title>',
            content
        )
        # CASE 2
        # The tag exists.
        # Expected title: Fried - Tag | Recipes
        tag = Tag.objects.create(name='Fried')
        response = self.client.get(
            reverse('recipes:search_tag', args=[tag.slug])
        )
        content = response.content.decode('utf-8')
        self.assertIn(
            '<title>Fried - Tag | Recipes</title>',
            content
        )

    def test_recipe_tag_view_is_showing_correct_recipes(self):
        tag = Tag.objects.create(name='Fried')
        r1 = self.make_recipe(title='This is Title One', is_published=True)
        r2 = self.make_recipe(title='This is Title Two', is_published=True)
        r1.tags.add(tag)
        response = self.client.get(
            reverse('recipes:search_tag', args=[tag.slug])
        )
        self.assertIn(r1, response.context['recipes'].object_list)
        self.assertNotIn(r2, response.context['recipes'].object_list)
