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
    def test_placeholders_are_correct(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(current_placeholder, placeholder)
