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

    def fill_up_form_with_dummies(self, form):
        dummy_data = {
            'first_name': 'Dummy',
            'last_name': 'Test',
            'email': 'dummy_test@mail.com',
            'username': 'DummyTest',
            'password': '#DummyT3st',
            'password2': '#DummyT3st',
        }
        for field in dummy_data:
            form_field = self.get_input_by_name(form, field)
            form_field.send_keys(dummy_data[field])
        return form
