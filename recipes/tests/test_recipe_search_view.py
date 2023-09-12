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

    def test_recipe_search_view_doesnt_show_unpublished_recipes(self):
        self.make_recipe(title='Recipe unpublished', is_published=False)
        response = self.client.get(
            reverse('recipes:search') + '?q=Recipe%20unpublished')
        self.assertEqual(len(response.context['recipes']), 0)

    def test_recipe_search_view_gets_recipe_by_title(self):
        title = 'Title to search'
        self.make_recipe(title=title)
        response = self.client.get(reverse('recipes:search') + f'?q={title}')
        content = response.content.decode('utf-8')
        self.assertIn(title, content)

    def test_recipe_search_view_gets_recipe_by_description(self):
        description = 'Description to search'
        self.make_recipe(description=description)
        response = self.client.get(
            reverse('recipes:search') + f'?q={description}')
        content = response.content.decode('utf-8')
        self.assertIn(description, content)

    def test_recipe_search_view_gets_recipe_by_title_and_description(self):
        title = 'Title to search'
        description = 'Description to search'
        self.make_recipe(title=title, description=description)
        response_one = self.client.get(
            reverse('recipes:search') + f'?q={title}')
        content_one = response_one.content.decode('utf-8')
        response_two = self.client.get(
            reverse('recipes:search') + f'?q={description}')
        content_two = response_two.content.decode('utf-8')
        self.assertIn(title, content_one)
        self.assertIn(description, content_two)
