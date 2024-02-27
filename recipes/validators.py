from collections import defaultdict
from recipes.models import Recipe
from utils.utils import parse_str_to_int

from django.core.exceptions import ValidationError


class RecipeValidator:
    def __init__(self, data, errors=None, errorClass=None):
        self.errors = defaultdict(list) if errors is None else errors
        self.errorClass = ValidationError if errorClass is None else errorClass
        self.data = data
        self.clean()

    def clean(self):
        self.clean_fields()
        title = self.data.get('title', '')
        description = self.data.get('description', '')
        if description.lower() == title.lower():
            self.errors['description'].append(
                'Your description and title can not be the same.',
            )
        if self.errors:
            raise self.errorClass(self.errors)

    def clean_fields(self):
        methods = [m for m in dir(self) if m != 'clean_fields'
                   and m.find('clean_') >= 0]
        methods.reverse()
        for m in methods:
            object_method = getattr(self, m)
            object_method()

    def clean_title(self):
        title = self.data.get('title', '')
        if len(title) < 8:
            self.errors['title'].append(
                'Your title must have at least 8 characters.',
            )
        recipe_from_db = Recipe.objects.filter(
            title__iexact=title,
        ).first()
        if recipe_from_db:
            self.errors['title'].append(
                'A recipe with this title already exists, ' +
                'try another one.',
            )

    def clean_description(self):
        description = self.data.get('description', '')
        if len(description) < 10:
            self.errors['description'].append(
                'Your description must have at least 10 characters.',
            )

    def clean_servings(self):
        servings = self.data.get('servings', '')
        if parse_str_to_int(servings) < 1:
            self.errors['servings'].append(
                'Type a number bigger than zero.'
            )

    def clean_preparation_time(self):
        preparation_time = self.data.get('preparation_time', '')
        if parse_str_to_int(preparation_time) < 1:
            self.errors['preparation_time'].append(
                'Type a number bigger than zero.'
            )
