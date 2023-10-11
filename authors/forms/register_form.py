from django import forms
from utils.django_form import strong_password
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
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
    username = forms.CharField(
        label='Username',
        error_messages={
            'required': 'Type a valid username.',
            'min_length': 'Your username must have at least 8 characters.',
            'max_length': 'Your username must have at max 150 characters.',
        },
        help_text=(
            'Username must have letters, numbers and one special character. '
            'The special characters allowed are: "@+-_". '
            'It must have at least 8 characters and maximum 150.'
        ),
        min_length=8,
        max_length=150,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Ex.: joedoe22',
            }
        ),
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

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email)
        if len(exists) > 0:
            raise ValidationError('This email already exists',
                                  code='invalid')
        return email

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
