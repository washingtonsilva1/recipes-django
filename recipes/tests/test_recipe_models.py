from .test_recipe_base import RecipeTestBase


class TestRecipeModel(RecipeTestBase):
    def setUp(self):
        self.recipe = self.make_recipe()
        super().setUp()
