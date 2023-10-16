from parameterized import parameterized
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class LoginFormIntegrationTest(TestCase):
    def setUp(self):
        self.login_data = {
            'username': 'randomuser',
            'password': 'R4nd0mPassword'
        }
        super().setUp()

    @parameterized.expand([
        ('username', 'Este campo é obrigatório.'),
        ('password', 'Este campo é obrigatório.'),
    ])
    def test_fields_shows_an_error_if_empty(self, field, message):
        self.login_data[field] = ''
        response = self.client.post(reverse('authors:login_create'),
                                    data=self.login_data, follow=True)
        self.assertIn(message, response.context['form'].errors[field])

    def test_login_with_invalid_credentials_shows_an_error_message(self):
        response = self.client.post(reverse('authors:login_create'),
                                    data=self.login_data, follow=True)
        content = response.content.decode('utf-8')
        self.assertIn('Incorrect username or password', content)

    def test_login_form_is_logging(self):
        User.objects.create_user(
            username=self.login_data['username'],
            password=self.login_data['password'],
            email='mail@mail.com'
        )
        response = self.client.post(reverse('authors:login_create'),
                                    data=self.login_data, follow=True)
        content = response.content.decode('utf-8')
        self.assertIn('You have logged in!', content)
