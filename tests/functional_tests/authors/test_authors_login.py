import pytest
from .test_authors_base import FunctionalAuthorsTestBase
from django.urls import reverse
from selenium.webdriver.common.by import By


@pytest.mark.functional_test
class AuthorsLoginFuncionalTest(FunctionalAuthorsTestBase):
    def test_username_field_can_not_be_empty(self):
        self.chrome.get(self.live_server_url + reverse('authors:login'))
        form = self.get_form()
        password_input = self.get_input_by_name(form, 'password')
        password_input.send_keys('#Passw0rdDummy')
        form.submit()
        self.assertIn('Username can not be empty.', self.get_form().text)

    def test_password_field_can_not_be_empty(self):
        self.chrome.get(self.live_server_url + reverse('authors:login'))
        form = self.get_form()
        username_input = self.get_input_by_name(form, 'username')
        username_input.send_keys('UsernameDummy')
        form.submit()
        self.assertIn('Password can not be empty.', self.get_form().text)

    def test_user_can_login_with_valid_data(self):
        data = {
            'username': 'DummyUser',
            'password': '#DummyPassw0rd',
        }
        self.make_user(username=data['username'], password=data['password'])
        self.chrome.get(self.live_server_url + reverse('authors:login'))
        form = self.get_form()
        username_input = self.get_input_by_name(form, 'username')
        username_input.send_keys(data['username'])
        password_input = self.get_input_by_name(form, 'password')
        password_input.send_keys(data['password'])
        form.submit()
        self.assertIn('You have logged in!',
                      self.chrome.find_element(By.TAG_NAME, 'body').text)

    def test_login_create_raises_404_if_there_is_no_post(self):
        self.chrome.get(self.live_server_url + reverse('authors:login_create'))
        self.assertIn('Not Found',
                      self.chrome.find_element(By.TAG_NAME, 'body').text)

    def test_login_with_invalid_credentials(self):
        data = {
            'username': 'DummyUser',
            'password': '#DummyPassw0rd',
        }
        self.chrome.get(self.live_server_url + reverse('authors:login'))
        form = self.get_form()
        username_input = self.get_input_by_name(form, 'username')
        username_input.send_keys(data['username'])
        password_input = self.get_input_by_name(form, 'password')
        password_input.send_keys(data['password'])
        form.submit()
        self.assertIn('Incorrect username or password',
                      self.chrome.find_element(By.TAG_NAME, 'body').text)
