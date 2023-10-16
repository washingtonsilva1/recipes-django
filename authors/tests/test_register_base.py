from django.test import TestCase
from django.urls import reverse


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
        self.client.post(reverse('authors:register_create'),
                         data=self.form_data)
