from django import forms
from recipes.models import Recipe
from recipes.validators import RecipeValidator
from django.core.exceptions import ValidationError

from django.utils.translation import gettext_lazy as _


class BaseRecipeForm(forms.ModelForm):
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
                    ('Hour', _('Hour')),
                    ('Minute', _('Minute')),
                ]
            ),
            'servings_unit': forms.Select(
                choices=[
                    ('People', _('People')),
                    ('Slice', _('Slice')),
                    ('Servings', _('Servings')),
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

    def clean(self):
        super_clean = super().clean()
        RecipeValidator(
            data=super_clean,
            errorClass=ValidationError
        )
        return super_clean
