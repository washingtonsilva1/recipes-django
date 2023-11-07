from django import forms
from recipes.models import Recipe


class RecipeEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.get('preparation_steps').widget.attrs['class'] = 'span-2'

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
                ]),
            'servings_unit': forms.Select(
                choices=[
                    ('Pessoa', 'Pessoa'),
                    ('Pedaço', 'Pedaço'),
                    ('Porção', 'Porção'),
                ]),
        }
