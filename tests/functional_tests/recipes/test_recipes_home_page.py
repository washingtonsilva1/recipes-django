import pytest
from django.utils.translation import gettext as _
from .test_recipes_base import FunctionalRecipesTestBase
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(FunctionalRecipesTestBase):
    def test_recipe_home_page_when_there_are_no_recipes(self):
        with self.settings(RECIPES_PER_PAGE=3):
            self.chrome.get(self.live_server_url)
            body = self.chrome.find_element(By.TAG_NAME, 'body')
            self.assertIn(_('No recipes were found'), body.text)

    def test_recipe_home_search_input_get_correct_recipe(self):
        with self.settings(RECIPES_PER_PAGE=3):
            title_needed = 'That is what I need'
            recipes = self.make_recipe_sample()
            recipes[0].title = title_needed
            recipes[0].save()
            # Steps:
            # 1. Get to the page OK
            # 2. Get to the search input OK
            # 3. Search a recipe OK
            # 4. Look if the searched recipe was found OK
            self.chrome.get(self.live_server_url)
            input = self.chrome.find_element(
                By.XPATH,
                "//input[@placeholder='Search a recipe']"
            )
            input.send_keys(recipes[0].title)
            input.send_keys(Keys.ENTER)
            self.assertIn(
                title_needed,
                self.chrome.find_element(By.CLASS_NAME,
                                         'main-content-list').text)

    def test_recipe_home_pagination_more_than_one_page(self):
        with self.settings(RECIPES_PER_PAGE=3):
            self.make_recipe_sample(6)
            # STEPS
            # 1 - Get to the page
            # 2 - Get to the pagination
            # 3 - See if there are more than one page
            self.chrome.get(self.live_server_url)
            pages = self.chrome.find_elements(By.CLASS_NAME, "pag-item")
            self.assertEqual(2, len(pages))
