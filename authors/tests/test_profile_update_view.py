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
        self.client.login(
            username=self.user_data['user'],
            password=self.user_data['password'],
        )
        super().setUp()

    def test_profile_returns_404_if_requesting_user_is_not_the_right_one(self):
        u2 = self.make_user()
        response = self.client.get(
            reverse('authors:profile_update',
                    args=[u2.profile.pk])
        )
        self.assertEqual(404, response.status_code)

    def test_profile_update_view_is_updating_users_profile(self):
        new_bio = 'That is a new bio for my profile!'
        response = self.client.post(
            reverse('authors:profile_update', args=[self.user.profile.pk]),
            data={
                'bio': new_bio
            },
            follow=True
        )
        content = response.content.decode('utf-8')
        self.assertIn('Your profile has been updated!', content)
        self.assertIn(new_bio, content)

    def test_profile_update_view_is_rendering_username_on_title(self):
        response = self.client.get(
            reverse('authors:profile_update',
                    args=[self.user.profile.pk])
        )
        content = response.content.decode('utf-8')
        self.assertIn(f'<title>{self.user.username} | Recipe', content)
