from django.test import TestCase
from django.contrib.auth.models import User


class FormTestBase(TestCase):
    def setUp(self):
        self.form_data = {
            'username': 'user1123',
            'password': 'Str0ngpassword1',
            'password2': 'Str0ngpassword1',
            'email': 'mail@example.com',
            'first_name': 'Joe',
            'last_name': 'Doe',
        }
        super().setUp()

    def create_user(self):
        User.objects.create_user(
            username=self.form_data['username'],
            email=self.form_data['email'],
            password=self.form_data['password'])
