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

    @parameterized.expand([
        ('servings', 'Type a number bigger than zero.'),
        ('preparation_time', 'Type a number bigger than zero.'),
    ])
    def test_fields_can_not_be_lower_than_one(self, field, error):
        self.form_data[field] = '0'
        self.create_unpublished_recipe()
        response = self.client.post(
            reverse('authors:recipe_edit', args=(1,)),
            data=self.form_data
        )
        self.assertIn(error, response.context['form'].errors[field])

    @parameterized.expand([
        ('servings_unit', 'Invalid servings unit.'),
        ('preparation_time_unit', 'Invalid preparation time unit.'),
    ])
    def test_select_fields_can_not_be_changed(self, field, error):
        self.form_data[field] = 'ThisIsNotAValidValue'
        self.create_unpublished_recipe()
        response = self.client.post(
            reverse('authors:recipe_edit', args=(1,)),
            data=self.form_data
        )
        self.assertIn(error, response.context['form'].errors[field])

    @parameterized.expand([
        ('title', 'Your title must have at least 8 characters.'),
        ('description', 'Your description must have at least 10 characters.'),
    ])
    def test_field_lower_than_the_expected(self, field, error):
        self.form_data[field] = 'A'*5
        self.create_unpublished_recipe()
        response = self.client.post(
            reverse('authors:recipe_edit', args=(1,)),
            data=self.form_data
        )
        self.assertIn(error, response.context['form'].errors[field])

    def test_recipe_can_not_have_an_existing_title(self):
        title_to_use = 'A random recipe title'
        self.form_data['title'] = title_to_use
        self.create_unpublished_recipe(title=title_to_use)
        recipe = self.create_unpublished_recipe()
        response = self.client.post(
            reverse('authors:recipe_edit', args=(recipe.pk,)),
            data=self.form_data,
        )
        self.assertIn(
            'A recipe with this title already exists, try another one.',
            response.context['form'].errors['title']
        )

    def test_fields_title_and_description_need_to_be_different(self):
        self.form_data['description'] = self.form_data['title']
        self.create_unpublished_recipe()
        response = self.client.post(
            reverse('authors:recipe_edit', args=(1,)),
            data=self.form_data
        )
        self.assertIn(
            'Your description and title can not be the same.',
            response.context['form'].errors['description']
        )

    def test_form_is_updating_a_recipe(self):
        title_needed = 'That is what I am looking for'
        self.form_data['title'] = title_needed
        self.create_unpublished_recipe()
        response = self.client.post(
            reverse('authors:recipe_edit', kwargs={'id': 1}),
            data=self.form_data, follow=True)
        self.assertIn(title_needed, response.content.decode('utf-8'))
