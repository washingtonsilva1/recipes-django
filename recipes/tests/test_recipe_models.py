from django.core.exceptions import ValidationError
from parameterized import parameterized

from .test_recipe_base import RecipeTestBase, Recipe


class TestRecipeModel(RecipeTestBase):
    def setUp(self):
        self.recipe = self.make_recipe()
        super().setUp()

    def make_recipe_no_defaults(self):
        recipe = Recipe(
            title='Recipe\'s Title',
            description='Recipe\'s Description',
            slug='recipe-slug', preparation_time=1,
            preparation_time_unit='Minutos', servings=1,
            servings_unit='Pessoa',
            preparation_steps='How to do the recipe, step by step...',
            category=self.make_category(category_name='second_category'),
            user=self.make_user(username='second_user')
        )
        recipe.full_clean()
        recipe.save()
        return recipe

    @parameterized.expand([
        ('title', 65),
        ('description', 150),
        ('preparation_time_unit', 65),
        ('servings_unit', 65),
    ])
    def test_recipe_title_raises_error_if_bigger_than_65_chars(self, field,
                                                               max_length):
        setattr(self.recipe, field, 'A' * (max_length + 1))
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    def test_recipe_is_published_default_is_false(self):
        recipe = self.make_recipe_no_defaults()
        self.assertFalse(recipe.is_published,
                         msg='Recipe is_published is not False!')

    def test_recipe_preparation_steps_is_html_default_is_false(self):
        recipe = self.make_recipe_no_defaults()
        self.assertFalse(recipe.preparation_steps_is_html,
                         msg='Recipe preparation_steps_is_html is not False')

    def test_recipe_string_representation(self):
        title_needed = 'Recipe Text Representation'
        self.recipe.title = title_needed
        self.recipe.full_clean()
        self.recipe.save()
        self.assertEqual(
            title_needed,
            str(self.recipe),
            msg=f'Recipe title must be {title_needed} ' +
            f'but {self.recipe} was received')
