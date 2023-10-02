from parameterized import parameterized
from django.test import TestCase
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
