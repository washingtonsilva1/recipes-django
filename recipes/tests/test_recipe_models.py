from django.core.exceptions import ValidationError
from parameterized import parameterized

from .test_recipe_base import RecipeTestBase


class TestRecipeModel(RecipeTestBase):
    def setUp(self):
        self.recipe = self.make_recipe()
        super().setUp()

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
