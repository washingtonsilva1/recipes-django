from django.urls import reverse, resolve
from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeSearchViewTest(RecipeTestBase):
    def test_recipe_search_view_is_correct(self):
        view = resolve(reverse('recipes:search'))
        self.assertIs(view.func, views.search)

    def test_recipe_search_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:search') + '?q=recipe')
        self.assertTemplateUsed(
            response, 'recipes/pages/search.html')

    def test_recipe_search_view_raises_404_if_no_search_term(self):
        response = self.client.get(reverse('recipes:search'))
        self.assertEqual(response.status_code, 404)

    def test_recipe_search_view_term_escaped(self):
        search = '<script>alert("hello, world!")</script>'
        response = self.client.get(reverse('recipes:search') + f'?q={search}')
        content = response.content.decode('utf-8')
        self.assertIn(
            '&lt;script&gt;alert(&quot;hello, world!&quot;)&lt;/script&gt;',
            content
        )
