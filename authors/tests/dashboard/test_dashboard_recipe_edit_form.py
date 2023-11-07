import pytest
from parameterized import parameterized
from django.urls import reverse
from .test_dashboard_base import DashboardTestBase


@pytest.mark.slow
class DashboardRecipeEditFormTest(DashboardTestBase):
    def setUp(self):
        self.form_data = {
            'title': 'Recipe title',
            'description': 'Recipe descrption',
            'preparation_time': '1',
            'preparation_time_unit': 'Hora',
            'servings': '1',
            'servings_unit': 'Pessoa',
            'preparation_steps': 'recipe preparation steps',
        }
        super().setUp()

    @parameterized.expand([
        ('title', 'This field can not be empty.'),
        ('description', 'This field can not be empty.'),
        ('preparation_time', 'This field can not be empty.'),
        ('preparation_time_unit', 'This field can not be empty.'),
        ('servings', 'This field can not be empty.'),
        ('servings_unit', 'This field can not be empty.'),
    ])
    def test_fields_can_not_be_empty(self, field, error):
        self.form_data[field] = ''
        self.create_unpublished_recipe()
        response = self.client.post(
            reverse('authors:recipe_edit', kwargs={'id': 1}),
            data=self.form_data)
        self.assertIn(error, response.context['form'].errors[field])

    def test_form_is_updating_a_recipe(self):
        title_needed = 'That is what I am looking for'
        self.form_data['title'] = title_needed
        self.create_unpublished_recipe()
        response = self.client.post(
            reverse('authors:recipe_edit', kwargs={'id': 1}),
            data=self.form_data, follow=True)
        self.assertIn(title_needed, response.content.decode('utf-8'))
