import pytest
from tests.functional_tests.function_test_base import FunctionalTestBase
from selenium.webdriver.common.by import By


@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(FunctionalTestBase):
    def test_recipe_home_page_when_there_are_no_recipes(self):
        self.chrome.get(self.live_server_url)
        body = self.chrome.find_element(By.TAG_NAME, 'body')
        self.assertIn('There are no recipes...', body.text)
