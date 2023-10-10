from parameterized import parameterized
from unittest import TestCase
from .test_register_base import RegisterFormTestBase
from django.urls import reverse
from authors.forms import RegisterForm


class RegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('username', 'Ex.: joedoe22'),
        ('first_name', 'Ex.: Joe'),
        ('last_name', 'Ex.: Doe'),
        ('password', 'Type your password'),
        ('password2', 'Confirm your password'),
        ('email', 'Ex.: joedoe@mail.com'),
    ])
    def test_fields_placeholder(self, field, placeholder):
        form = RegisterForm()
        current = form[field].field.widget.attrs['placeholder']
        self.assertEqual(current, placeholder)

    @parameterized.expand([
        ('username', (
            'Username must have letters, numbers and one special character. '
            'The special characters allowed are: "@+-_". '
            'It must have at least 8 characters and maximum 150.'
        )),
        ('password', 'Password must have at least one uppercase and '
         'lowercase letter and one number. The length should be '
         'at least 8 characters.'),
        ('email', 'Please, enter a valid email.'),
    ])
    def test_fields_help_text(self, field, help_text):
        form = RegisterForm()
        current = form[field].field.help_text
        self.assertEqual(current, help_text)

    @parameterized.expand([
        ('username', 'Username'),
        ('password', 'Password'),
        ('password2', 'Confirm password'),
        ('email', 'Email'),
        ('first_name', 'First name'),
        ('last_name', 'Last name'),
    ])
    def test_fields_label(self, field, label):
        form = RegisterForm()
        current = form[field].field.label
        self.assertEqual(current, label)


class RegisterFormIntegrationTest(RegisterFormTestBase):
    @parameterized.expand([
        ('username', 'Type a valid username.'),
        ('password', 'Type a valid password.'),
        ('password2', 'Type your password again.'),
        ('first_name', 'Type your first name.'),
        ('last_name', 'Type your last name.'),
        ('email', 'Type your email.'),
    ])
    def test_fields_can_not_be_empty(self, field, message):
        self.form_data[field] = ' '
        response = self.client.post(reverse('authors:create'),
                                    data=self.form_data, follow=True)
        self.assertIn(message, response.context['form'].errors[field])

    def test_username_field_less_than_eight_characters(self):
        self.form_data['username'] = 'joa'
        msg = 'Your username must have at least 8 characters.'
        response = self.client.post(reverse('authors:create'),
                                    data=self.form_data, follow=True)
        self.assertIn(msg, response.context['form'].errors['username'])

    def test_username_field_bigger_than_max_characters_allowed(self):
        self.form_data['username'] = 'A'*151
        msg = 'Your username must have at max 150 characters.'
        response = self.client.post(reverse('authors:create'),
                                    data=self.form_data, follow=True)
        self.assertIn(msg, response.context['form'].errors['username'])

    def test_password_fields_doesnt_match(self):
        msg = 'Passwords doesn\'t match.'
        self.form_data['password2'] += 'a'
        response = self.client.post(
            reverse('authors:create'), data=self.form_data, follow=True)
        self.assertIn(msg, response.context['form'].errors['password2'])

    def test_password_field_is_not_strong_enough(self):
        msg = 'You password doesn\'t match the requirements.'
        self.form_data['password'] = 'abcdefghjkl'
        self.form_data['password2'] = 'abcdefghjkl'

        response = self.client.post(
            reverse('authors:create'), data=self.form_data, follow=True)
        self.assertIn(msg, response.context['form'].errors['password'])

    def test_email_field_gets_an_error_using_an_existing_email(self):
        msg = 'This email already exists'
        self.create_user()
        response = self.client.post(
            reverse('authors:create'), data=self.form_data, follow=True)
        self.assertIn(msg, response.context['form'].errors['email'])

    def test_username_field_gets_an_error_if_using_existing_username(self):
        msg = 'Um usuário com este nome de usuário já existe.'
        self.create_user()
        response = self.client.post(
            reverse('authors:create'),
            data=self.form_data,
            follow=True,
        )
        self.assertIn(msg, response.context['form'].errors['username'])

    def test_register_form_is_creating_user(self):
        msg = 'Your user has been created, please log in!'
        response = self.client.post(
            reverse('authors:create'), data=self.form_data, follow=True)
        content = response.content.decode('utf-8')
        self.assertIn(msg, content)

    def test_created_user_can_login(self):
        self.form_data.update({
            'username': 'joedoe22',
            'password': '@Joedo1ngthis',
            'password2': '@Joedo1ngthis',
        })
        self.client.post(reverse('authors:create'), data=self.form_data)
        is_auth = self.client.login(
            username=self.form_data['username'],
            password=self.form_data['password'],
            password2=self.form_data['password2'],
        )
        self.assertTrue(is_auth)
