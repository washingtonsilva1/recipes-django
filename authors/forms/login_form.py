from django import forms
from django.utils.translation import gettext_lazy as _


class LoginForm(forms.Form):
    username = forms.CharField(
        label=_('Username'),
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Type your username',
            }
        ),
        error_messages={
            'required': 'Username can not be empty.',
        }

    )
    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Type your password'
            }
        ),
        error_messages={
            'required': 'Password can not be empty.',
        }
    )
