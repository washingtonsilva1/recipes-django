from django.test import TestCase
from django.urls import reverse, resolve
from recipes import views
from recipes.models import Category, Recipe, User


class RecipeViewsTest(TestCase):
    def test_recipes_home_view_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipes_home_view_returns_status_code_200_ok(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEquals(response.status_code, 200)

    def test_recipes_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipes_home_returns_not_found_if_there_are_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn('There are no recipes', response.content.decode('utf-8'))

    def test_recipes_home_template_loads_recipes(self):
        category = Category.objects.create(name='First category')
        user = User.objects.create_user(
            first_name='first',
            last_name='last',
            username='deivison',
            email='deivisonwashington@gmail.com',
            password='DeivisonWashington'
        )
        recipe = Recipe.objects.create(
            title='Testing recipes',
            description='Recipe description',
            slug='testing-recipes',
            preparation_time=5,
            preparation_time_unit='Hours',
            servings=1,
            servings_unit='Pessoa',
            preparation_steps='Recipe\'s steps',
            preparation_steps_is_html=False,
            is_published=True,
            category=category,
            user=user,
        )
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.context['recipes'].first(), recipe)

    def test_recipes_category_view_is_correct(self):
        view = resolve(reverse('recipes:category', args=[1]))
        self.assertIs(view.func, views.category)

    def test_recipes_category_returns_404_if_not_exists(self):
        response = self.client.get(reverse('recipes:category', args=[1]))
        self.assertEqual(response.status_code, 404)

    def test_recipes_recipe_view_is_correct(self):
        view = resolve(reverse('recipes:recipe', args=[1]))
        self.assertIs(view.func, views.recipe)

    def test_recipes_recipe_returns_404_if_not_exists(self):
        response = self.client.get(reverse('recipes:recipe', args=[1]))
        self.assertEqual(response.status_code, 404)
