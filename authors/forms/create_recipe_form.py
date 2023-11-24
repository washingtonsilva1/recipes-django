from django import forms
from recipes.models import Recipe
from django.core.exceptions import ValidationError


class RecipeCreateForm(forms.ModelForm):
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
                'required': 'This field can not be empty.',
                'invalid': 'Type a valid number.',
            },
            'preparation_time_unit': {
                'required': 'This field can not be empty.'
            },
            'servings': {
                'required': 'This field can not be empty.',
                'invalid': 'Type a valid number.',
            },
            'servings_unit': {
                'required': 'This field can not be empty.'
            },
            'preparation_steps': {
                'required': 'This field can not be empty.'
            },
        }

    def clean_preparation_time(self):
        preparation_time = self.cleaned_data.get('preparation_time', '')
        if preparation_time < 1:
            raise ValidationError(
                message='Type a number bigger than zero.',
                code='invalid'
            )
        return preparation_time

    def clean_preparation_time_unit(self):
        preparation_time_unit = self.cleaned_data.get(
            'preparation_time_unit',
            ''
        )
        field = self.fields.get('preparation_time_unit')
        choices = [v for v, k in field.widget.choices]
        if preparation_time_unit not in choices:
            raise ValidationError(
                message='Invalid preparation time unit.',
                code='invalid'
            )
        return preparation_time_unit

    def clean_servings(self):
        servings = self.cleaned_data.get('servings', '')
        if servings < 1:
            raise ValidationError(
                message='Type a number bigger than zero.',
                code='invalid'
            )
        return servings

    def clean_servings_unit(self):
        servings_unit = self.cleaned_data.get('servings_unit', '')
        field = self.fields.get('servings_unit')
        choices = [v for v, k in field.widget.choices]
        if servings_unit not in choices:
            raise ValidationError(
                message='Invalid servings unit.',
                code='invalid'
            )
        return servings_unit

    def clean_title(self):
        title = self.cleaned_data.get('title', '')
        if len(title) < 8:
            raise ValidationError(
                message='Your title must have at least 8 characters.',
                code='invalid'
            )
        return title

    def clean_description(self):
        description = self.cleaned_data.get('description', '')
        if len(description) < 10:
            raise ValidationError(
                message='Your description must have at least 10 characters.',
                code='invalid'
            )
        return description

    def clean(self):
        super_cleaned = super().clean()
        title = self.cleaned_data.get('title', '')
        description = self.cleaned_data.get('description', '')
        if description.lower() == title.lower():
            raise ValidationError({
                'description': ValidationError(
                    message='Your description and title can not be the same.',
                    code='invalid'
                )
            })
        return super_cleaned
