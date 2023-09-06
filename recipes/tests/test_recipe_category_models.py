from .test_recipe_base import RecipeTestBase
from django.core.exceptions import ValidationError


class TestRecipeCategoryModel(RecipeTestBase):
    def setUp(self):
        self.category = self.make_category(category_name='Category Testing')
        super().setUp()

    def test_recipe_category_string_representation_is_correct(self):
        self.assertEqual(str(self.category), self.category.name)

    def test_recipe_category_name_raises_error_if_bigger_than_65_chars(self):
        self.category.name = 'A' * 66
        with self.assertRaises(ValidationError):
            self.category.full_clean()
