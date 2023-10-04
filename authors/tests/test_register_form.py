from parameterized import parameterized
from unittest import TestCase
from django.test import TestCase as DjangoTestCase
from django.urls import reverse
from authors.forms import RegisterForm


class RegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('username', 'Ex.: joedoe22'),
        ('first_name', 'Ex.: Joe'),
        ('last_name', 'Ex.: Doe'),
        ('password', 'Type your password'),
        ('password2', 'Confirm your password'),
        ('email', 'Type your mail'),
    ])
    def test_fields_placeholder(self, field, placeholder):
        form = RegisterForm()
        current = form[field].field.widget.attrs['placeholder']
        self.assertEqual(current, placeholder)

    @parameterized.expand([
        ('password', 'Password must have at least one uppercase and '
         'lowercase letter and one number. The length should be '
         'at least 8 characters.'),
        ('email', 'Enter a valid e-mail!'),
    ])
    def test_fields_help_text(self, field, help_text):
        form = RegisterForm()
        current = form[field].field.help_text
        self.assertEqual(current, help_text)

    @parameterized.expand([
        ('username', 'Username'),
        ('password', 'Password'),
        ('password2', 'Confirm password'),
        ('email', 'E-mail'),
        ('first_name', 'First name'),
        ('last_name', 'Last name'),
    ])
    def test_fields_label(self, field, label):
        form = RegisterForm()
        current = form[field].field.label
        self.assertEqual(current, label)


class RegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self):
        self.form_data = {
            'username': 'user112',
            'password': 'Str0ngpassword1',
            'password2': 'Str0ngpassword1',
            'email': 'mail@example.com',
            'first_name': 'Joe',
            'last_name': 'Doe',
        }
        return super().setUp()

    @parameterized.expand([
        ('username', 'This field can&#x27;t be empty.'),
        ('password', 'This field can&#x27;t be empty.'),
        ('password2', 'This field can&#x27;t be empty.'),
    ])
    def test_fields_can_not_be_empty(self, field, message):
        self.form_data[field] = ' '
        response = self.client.post(reverse('authors:create'),
                                    data=self.form_data, follow=True)
        content = response.content.decode('utf-8')
        self.assertIn(message, content)
