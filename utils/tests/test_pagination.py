import pytest
from utils.pagination import make_pagination_range
from django.urls import reverse
from recipes.tests.test_recipe_base import RecipeTestBase


@pytest.mark.slow
class PaginationTest(RecipeTestBase):
    def test_pagination_range_returns_a_pagination_range(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            pages=4,
            current=1)
        self.assertEqual([1, 2, 3, 4], pagination['pagination'])

    def test_first_range_is_static_if_current_page_is_shorter_than_the_middle(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            pages=4,
            current=1)
        self.assertEqual([1, 2, 3, 4], pagination['pagination'])

    def test_range_changes_if_larger_than_the_middle(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            pages=4,
            current=3)
        self.assertEqual([2, 3, 4, 5], pagination['pagination'])

    def test_range_is_static_if_near_last_page(self):
        # The range only changes if is at third to last page.
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            pages=4,
            current=18)
        self.assertEqual([17, 18, 19, 20], pagination['pagination'])
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            pages=4,
            current=19)
        self.assertEqual([17, 18, 19, 20], pagination['pagination'])
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            pages=4,
            current=20)
        self.assertEqual([17, 18, 19, 20], pagination['pagination'])

    def test_pagination_displaying_nine_recipes_per_page(self):
        with self.settings(RECIPES_PER_PAGE=9):
            for i in range(10):
                kwargs = {'slug': f'recipe-slug-{i}',
                          'user_data': {'username': f'{i}'}}
                self.make_recipe(**kwargs)
            response = self.client.get(reverse('recipes:home'))
            paginator = response.context['recipes'].paginator
            self.assertEqual(len(paginator.get_page(1)), 9)

    def test_pagination_displaying_less_than_nine_recipes(self):
        # that occurs when there are less than nine recipes to display
        with self.settings(RECIPES_PER_PAGE=9):
            for i in range(3):
                kwargs = {'slug': f'recipe-slug-{i}',
                          'user_data': {'username': f'{i}'}}
                self.make_recipe(**kwargs)
            response = self.client.get(reverse('recipes:home'))
            paginator = response.context['recipes'].paginator
            self.assertEqual(len(paginator.get_page(1)), 3)

    def test_pagination_displaying_correct_amount_of_pages(self):
        with self.settings(RECIPES_PER_PAGE=9):
            for i in range(18):
                kwargs = {'slug': f'recipe-slug-{i}',
                          'user_data': {'username': f'{i}'}}
                self.make_recipe(**kwargs)
            response = self.client.get(reverse('recipes:home'))
            recipes = response.context['recipes']
            paginator = recipes.paginator
            self.assertEqual(paginator.num_pages, 2)
