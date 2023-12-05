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

    def test_profile_view_shows_update_button_only_for_correct_user(self):
        # Case 1
        # Logged user is equal to profile__user
        self.client.login(
            username=self.user_data['user'],
            password=self.user_data['password']
        )
        response = self.client.get(
            reverse('authors:profile',
                    args=[self.user.profile.pk])
        )
        content = response.content.decode('utf-8')
        self.assertIn('Update profile', content)

        # Case 2
        # Logged user and profile__user are different
        self.client.logout()
        response = self.client.get(
            reverse('authors:profile',
                    args=[self.user.profile.pk])
        )
        content = response.content.decode('utf-8')
        self.assertNotIn('Update profile', content)

    def test_profile_bio_shows_default_information_if_empty(self):
        response = self.client.get(
            reverse('authors:profile',
                    args=[self.user.profile.pk])
        )
        content = response.content.decode('utf-8')
        self.assertIn('This user doesn\'t have any information yet.', content)
