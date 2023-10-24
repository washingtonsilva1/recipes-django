from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from utils.browser import make_chrome_driver
from recipes.tests.test_recipe_base import RecipeMixin


class FunctionalRecipesTestBase(StaticLiveServerTestCase, RecipeMixin):
    def setUp(self):
        self.chrome = make_chrome_driver()
        super().setUp()

    def tearDown(self):
        self.chrome.quit()
        super().tearDown()
