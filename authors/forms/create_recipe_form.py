from django.core.exceptions import ValidationError
from recipes.models import Recipe
from .base_recipe_form import BaseRecipeForm


class RecipeCreateForm(BaseRecipeForm):
    def clean_title(self):
        title = self.cleaned_data.get('title', '')
        if len(title) < 8:
            raise ValidationError(
                message='Your title must have at least 8 characters.',
                code='invalid'
            )
        recipe_from_db = Recipe.objects.filter(
            title__iexact=title,
        ).first()
        if recipe_from_db:
            raise ValidationError(
                message='A recipe with this title already exists, ' +
                'try another one.',
                code='invalid'
            )
        return title
