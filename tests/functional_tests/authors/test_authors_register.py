import pytest
from .test_authors_base import FunctionalAuthorsTestBase
from django.urls import reverse
from selenium.webdriver.common.by import By


@pytest.mark.functional_test
class AuthorsRegisterFunctionalTest(FunctionalAuthorsTestBase):
    def prepare_form_callback(self, callback):
        self.chrome.get(self.live_server_url +
                        reverse('authors:register'))
        form = self.get_form()
        self.fill_up_form_with_dummies(form)
        callback(form)
        return form

    def test_register_form_username_is_empty(self):
        def callback(form):
            username = self.get_input_by_name(form, 'username')
            username.clear()
            username.send_keys(' ')
            form.submit()
            self.assertIn('Type a valid username.', self.get_form().text)
        self.prepare_form_callback(callback)

    def test_register_form_first_name_is_empty(self):
        def callback(form):
            first_name = self.get_input_by_name(form, 'first_name')
            first_name.clear()
            first_name.send_keys(' ')
            form.submit()
            self.assertIn('Type your first name.', self.get_form().text)
        self.prepare_form_callback(callback)

    def test_register_form_last_name_is_empty(self):
        def callback(form):
            last_name = self.get_input_by_name(form, 'last_name')
            last_name.clear()
            last_name.send_keys(' ')
            form.submit()
            self.assertIn('Type your last name.', self.get_form().text)
        self.prepare_form_callback(callback)

    def test_register_form_invalid_email(self):
        def callback(form):
            email = self.get_input_by_name(form, 'email')
            email.clear()
            email.send_keys('email@mail')
            form.submit()
            self.assertIn('Your email is not valid.',
                          self.get_form().text)
        self.prepare_form_callback(callback)

    def test_register_form_passwords_are_not_equal(self):
        def callback(form):
            password = self.get_input_by_name(form, 'password')
            password.clear()
            password.send_keys('#Passw0rd1')
            password2 = self.get_input_by_name(form, 'password2')
            password2.clear()
            password2.send_keys('#Passw0rd2')
            form.submit()
            self.assertIn('Passwords doesn\'t match.',
                          self.get_form().text)
        self.prepare_form_callback(callback)

    def test_register_form_creates_user_with_valid_data(self):
        def callback(form):
            form.submit()
            self.assertIn(
                'Your user has been created, please log in!',
                self.chrome.find_element(By.TAG_NAME, 'body').text)
        self.prepare_form_callback(callback)
