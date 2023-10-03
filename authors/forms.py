import re
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


def set_attribute(field, attribute, value):
    field.widget.attrs[attribute] = value


def set_placeholder(field, placeholder):
    set_attribute(field, 'placeholder', placeholder)


def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')
    if not regex.match(password):
        raise ValidationError(
            'You password doesn\'t match the requirements.', code='invalid')
    return True


class RegisterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        set_placeholder(
            field=self.fields['username'], placeholder='Ex.: joedoe22')
        set_placeholder(
            field=self.fields['first_name'], placeholder='Ex.: Joe')
        set_placeholder(
            field=self.fields['last_name'], placeholder='Ex.: Doe')
        set_placeholder(
            field=self.fields['email'], placeholder='Type your mail')

    password = forms.CharField(
        label='Password',
        error_messages={
            'required': 'This field can\'t be empty.'
        },
        help_text='Password must have at least one uppercase and '
        'lowercase letter and one number. The length should be '
        'at least 8 characters.',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Type your password'
            }
        ),
        validators=[strong_password]
    )
    password2 = forms.CharField(
        label='Confirm password',
        error_messages={
            'required': 'This field can\'t be empty.'
        },
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Confirm your password'}
        )
    )

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
        ]

        labels = {
            'first_name': 'First name',
            'last_name': 'Last name',
            'username': 'Username',
            'email': 'E-mail',
        }

        error_messages = {
            'username': {
                'required': 'This field can\'t be empty.',
            }
        }

        help_texts = {
            'email': 'Enter a valid e-mail!',
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password != password2:
            raise ValidationError(
                {'password2': ValidationError(
                    'Passwords doesn\'t match.',
                    code='invalid')
                 }
            )
