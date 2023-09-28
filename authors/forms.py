from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


def set_attribute(field, attribute, value):
    field.widget.attrs[attribute] = value


def set_placeholder(field, placeholder):
    set_attribute(field, 'placeholder', placeholder)


class RegisterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        set_placeholder(
            field=self.fields['username'], placeholder='Ex.: jojobiza21k')
        set_placeholder(
            field=self.fields['first_name'], placeholder='Ex.: Jonathan')
        set_placeholder(
            field=self.fields['last_name'], placeholder='Ex.: Joestar')

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
            'password': 'Password',
            'email': 'E-mail',
        }

        error_messages = {
            'username': {
                'required': 'This field can\'t be empty.'
            },
            'password': {
                'required': 'This field can\'t be empty.'
            }
        }

        help_texts = {
            'email': 'Enter a valid e-mail!'
        }

        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Type your username'
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Type your password'
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
