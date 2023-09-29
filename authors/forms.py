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
            field=self.fields['username'], placeholder='Ex.: jojobiza21k')
        set_placeholder(
            field=self.fields['first_name'], placeholder='Ex.: Jonathan')
        set_placeholder(
            field=self.fields['last_name'], placeholder='Ex.: Joestar')
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
                'placeholder': 'Re-type your password'
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
            'first_name': 'First Name',
            'last_name': 'Last Name',
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
            'password': 'Password must have at least one uppercase and '
            'lowercase letter and one number. The length should be '
            'at least 8 characters.',
        }

        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Type your username'
            }),
        }

    def clean_first_name(self):
        data = self.cleaned_data.get('first_name')

        if 'Attention' in data:
            raise ValidationError(
                'You can\'t type "%(value)s" here!',
                code='invalid',
                params={'value': 'Attention'})

        return data

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
