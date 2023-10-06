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

    first_name = forms.CharField(
        label='First name',
        error_messages={
            'required': 'Type your first name.',
        },
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Ex.: Joe',
            }
        ),
    )
    last_name = forms.CharField(
        label='Last name',
        error_messages={
            'required': 'Type your last name.',
        },
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Ex.: Doe'
            }
        ),
    )
    email = forms.EmailField(
        label='Email',
        error_messages={
            'required': 'Type your email.',
        },
        help_text='Please, enter a valid email.',
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Ex.: joedoe@mail.com',
            }
        )
    )
    password = forms.CharField(
        label='Password',
        error_messages={
            'required': 'Type a valid password.'
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
            'required': 'Type your password again.'
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
            'username': 'Username',
        }

        error_messages = {
            'username': {
                'required': 'Type a valid username.',
            }
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
