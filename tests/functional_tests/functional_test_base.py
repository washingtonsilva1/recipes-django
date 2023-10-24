from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from utils.browser import make_chrome_driver
from recipes.tests.test_recipe_base import RecipeMixin


class FunctionalTestBase(StaticLiveServerTestCase, RecipeMixin):
    def setUp(self):
        self.chrome = make_chrome_driver()
        super().setUp()

    def tearDown(self):
        self.chrome.quit()
        super().tearDown()

    def get_chrome_element(self, filter, element):
        return self.chrome.find_element(filter, element)
