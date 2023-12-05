from django.test import TestCase
from django.urls import reverse
from recipes.tests.test_recipe_base import RecipeMixin


class ProfileViewTest(TestCase, RecipeMixin):
    def setUp(self):
        self.user_data = {
            'user': 'dummy_user',
            'password': '#DummyPassw0rd'
        }
        self.user = self.make_user(
            username=self.user_data['user'],
            password=self.user_data['password']
        )
        super().setUp()

    def test_profile_returns_404_if_requesting_user_is_not_the_right_one(self):
        self.client.login(
            username=self.user_data['user'],
            password=self.user_data['password'],
        )
        u2 = self.make_user()
        response = self.client.get(
            reverse('authors:profile_update',
                    args=[u2.profile.pk])
        )
        self.assertEqual(404, response.status_code)
