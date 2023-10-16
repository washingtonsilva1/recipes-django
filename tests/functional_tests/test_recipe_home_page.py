from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from utils.browser import make_chrome_driver
from selenium.webdriver.common.by import By


class RecipeHomePageFunctionalTest(StaticLiveServerTestCase):
    def setUp(self):
        self.chrome = make_chrome_driver('--headless')
        super().setUp()

    def tearDown(self):
        self.chrome.quit()
        super().tearDown()

    def test_home_page_when_there_are_no_recipes(self):
        self.chrome.get(self.live_server_url)
        body = self.chrome.find_element(By.TAG_NAME, 'body')
        self.assertIn('There are no recipes...', body.text)
