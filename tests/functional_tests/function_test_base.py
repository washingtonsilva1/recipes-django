from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from utils.browser import make_chrome_driver


class FunctionalTestBase(StaticLiveServerTestCase):
    def setUp(self):
        self.chrome = make_chrome_driver()
        super().setUp()

    def tearDown(self):
        self.chrome.quit()
        super().tearDown()
