import pytest
from parameterized import parameterized
from .test_dashboard_base import DashboardTestBase
from django.urls import reverse


@pytest.mark.slow
class DashboardRecipeCreateFormTest(DashboardTestBase):
    def setUp(self):
        self.form_data = {
            'title': 'Recipe Title',
            'description': 'Recipe Description',
            'preparation_time': '10',
            'preparation_time_unit': 'Minuto',
            'servings': '1',
            'servings_unit': 'Porção',
            'preparation_steps': 'Faça isso e depois fala aquilo',
        }
        super().setUp()

    @parameterized.expand([
        ('title', 'This field can not be empty.'),
        ('description', 'This field can not be empty.'),
        ('preparation_time', 'This field can not be empty.'),
        ('preparation_time_unit', 'This field can not be empty.'),
        ('servings', 'This field can not be empty.'),
        ('servings_unit', 'This field can not be empty.'),
        ('preparation_steps', 'This field can not be empty.'),
    ])
    def test_recipe_data_can_not_be_empty(self, field, error):
        self.form_data[field] = ''
        response = self.client.post(
            reverse('authors:recipe_create'),
            data=self.form_data,
        )
        self.assertIn(error, response.context['form'].errors[field])

    @parameterized.expand([
        ('title', 'Your title must have at least 8 characters.'),
        ('description', 'Your description must have at least 10 characters.'),
    ])
    def test_recipe_title_and_description_lower_than_expected(self, field, error):
        self.form_data[field] = 'a'*3
        response = self.client.post(
            reverse('authors:recipe_create'),
            data=self.form_data,
        )
        self.assertIn(error, response.context['form'].errors[field])

    def test_recipe_can_not_have_same_title_and_description(self):
        self.form_data['description'] = self.form_data['title']
        response = self.client.post(
            reverse('authors:recipe_create'),
            data=self.form_data,
        )
        self.assertIn(
            'Your description and title can not be the same.',
            response.context['form'].errors['description']
        )

    @parameterized.expand([
        ('servings', 'Type a number bigger than zero.'),
        ('preparation_time', 'Type a number bigger than zero.'),
    ])
    def test_recipe_can_not_have_servings_and_time_lower_than_one(self, field, error):
        self.form_data[field] = '0'
        response = self.client.post(
            reverse('authors:recipe_create'),
            data=self.form_data,
        )
        self.assertIn(error, response.context['form'].errors[field])

    @parameterized.expand([
        ('servings_unit', 'Invalid servings unit.'),
        ('preparation_time_unit', 'Invalid preparation time unit.'),
    ])
    def test_select_fields_can_not_be_changed(self, field, error):
        self.form_data[field] = 'ThisIsNotAValidValue'
        response = self.client.post(
            reverse('authors:recipe_create'),
            data=self.form_data
        )
        self.assertIn(error, response.context['form'].errors[field])

    def test_recipe_create_form_is_creating_a_recipe(self):
        response = self.client.post(
            reverse('authors:recipe_create'),
            data=self.form_data,
            follow=True
        )
        self.assertIn(
            'Your recipe has been created!',
            response.content.decode('utf-8')
        )
