from django import forms
from recipes.models import Recipe


class RecipeEditForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            'cover',
            'title',
            'description',
            'preparation_time',
            'preparation_time_unit',
            'servings',
            'servings_unit',
            'preparation_steps',
        ]
        widgets = {
            'cover': forms.FileInput(
                attrs={
                    'class': 'span-2',
                }
            ),
            'preparation_time_unit': forms.Select(
                choices=[
                    ('Hora', 'Hora'),
                    ('Minuto', 'Minuto'),
                ]
            ),
            'servings_unit': forms.Select(
                choices=[
                    ('Pessoa', 'Pessoa'),
                    ('Pedaço', 'Pedaço'),
                    ('Porção', 'Porção'),
                ]
            ),
            'preparation_steps': forms.Textarea(
                attrs={
                    'class': 'span-2',
                }
            )
        }
        error_messages = {
            'title': {
                'required': 'This field can not be empty.'
            },
            'description': {
                'required': 'This field can not be empty.'
            },
            'preparation_time': {
                'required': 'This field can not be empty.'
            },
            'preparation_time_unit': {
                'required': 'This field can not be empty.'
            },
            'servings': {
                'required': 'This field can not be empty.'
            },
            'servings_unit': {
                'required': 'This field can not be empty.'
            },
        }
