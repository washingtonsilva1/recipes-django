from .test_recipe_base import RecipeTestBase
from django.core.exceptions import ValidationError


class TestRecipeModel(RecipeTestBase):
    def setUp(self):
        self.recipe = self.make_recipe()
        super().setUp()

    def test_recipe_title_raises_error_if_larger_than_65_chars(self):
        self.recipe.title = 'test' * 17
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()
