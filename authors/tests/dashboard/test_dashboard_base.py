from django.test import TestCase
from recipes.tests.test_recipe_base import RecipeMixin


class DashboardTestBase(TestCase, RecipeMixin):
    def setUp(self):
        self.user_data = {
            'username': 'DummyUser',
            'password': '#DummyPassw0rd',
        }
        self.user = self.make_user(
            username=self.user_data['username'],
            password=self.user_data['password'],
        )
        self.client.login(
            username=self.user_data['username'],
            password=self.user_data['password'],
        )
        super().setUp()

    def create_unpublished_recipe(self, title='A title for a recipe'):
        recipe = self.make_recipe(title=title)
        recipe.user = self.user
        recipe.is_published = False
        recipe.save()
        return recipe
