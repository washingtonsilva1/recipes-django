from django.test import TestCase

from utils.utils import generate_random_string
from recipes.models import Category, Recipe, User


class RecipeMixin:
    def make_category(self, category_name='Category'):
        return Category.objects.create(name=category_name)

    def make_user(self, username=None, email='email@provider.com',
                  password='secretphrase'):
        if username is None:
            username = generate_random_string(5)
        return User.objects.create_user(username, email, password)

    def make_recipe(self, title='Recipe\'s Title',
                    description='Recipe\'s Description',
                    slug='recipe-slug', preparation_time=1,
                    preparation_time_unit='Minutos', servings=1,
                    servings_unit='Pessoa',
                    preparation_steps='How to do the recipe, step by step...',
                    preparation_steps_is_html=False, is_published=True,
                    category=None, user_data=None):
        slug = f'{slug}-{generate_random_string(3)}'

        if category is None:
            category = {}

        if user_data is None:
            user_data = {}

        return Recipe.objects.create(
            title=title,
            description=description,
            slug=slug,
            preparation_time=preparation_time,
            preparation_time_unit=preparation_time_unit,
            servings=servings,
            servings_unit=servings_unit,
            preparation_steps=preparation_steps,
            preparation_steps_is_html=preparation_steps_is_html,
            is_published=is_published,
            category=self.make_category(**category),
            user=self.make_user(**user_data)
        )

    def make_recipe_sample(self, qt=5):
        recipes = []
        for i in range(qt):
            kwargs = {
                'title': f'Recipe title {i}',
                'slug': f'recipe-slug-{i}',
                'user_data': {'username': f'{i}'}
            }
            recipes.append(self.make_recipe(**kwargs))
        return recipes


class RecipeTestBase(TestCase, RecipeMixin):
    def setUp(self):
        super().setUp()
