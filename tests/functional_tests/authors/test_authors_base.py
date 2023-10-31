from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from utils.browser import make_chrome_driver
from recipes.tests.test_recipe_base import RecipeMixin
from selenium.webdriver.common.by import By


class FunctionalAuthorsTestBase(StaticLiveServerTestCase, RecipeMixin):
    def setUp(self):
        self.chrome = make_chrome_driver()
        super().setUp()

    def tearDown(self):
        self.chrome.quit()
        super().tearDown()

    def get_form(self):
        return self.chrome.find_element(
            By.XPATH,
            '/html/body/main/div[2]/form'
        )

    def get_input_by_name(self, form, name):
        return form.find_element(
            By.XPATH,
            f'//input[@name="{name}"]')
