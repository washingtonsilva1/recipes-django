from django.test import TestCase

from recipes.models import Category, Recipe, User


class RecipeTestBase(TestCase):
    def make_category(self, category_name='Category'):
        return Category.objects.create(name=category_name)

    def make_user(self, username='user', email='email@provider.com',
                  password='secretphrase'):
        return User.objects.create_user(username, email, password)

    def make_recipe(self, title='recipe title',
                    description='recipe description',
                    slug='recipe-slug', preparation_time=1,
                    preparation_time_unit='Minutos', servings=1,
                    servings_unit='Pessoa(s)',
                    preparation_steps='how to do the recipe, step by step...',
                    preparation_steps_is_html=False, is_published=True,
                    category=None, user_data=None):
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
