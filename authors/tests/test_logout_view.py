from authors import views
from .test_form_base import FormTestBase
from django.urls import resolve, reverse


class LogoutViewTest(FormTestBase):
    def setUp(self):
        super().setUp()
        self.create_user()
        self.client.login(
            username=self.form_data['username'],
            password=self.form_data['password']
        )

    def test_logout_is_loading_correct_view(self):
        view = resolve(reverse('authors:logout'))
        self.assertIs(view.func, views.logout_view)

    def test_logout_view_is_logging_out_user(self):
        response = self.client.post(
            reverse('authors:logout'),
            data={'username': self.form_data['username']},
            follow=True
        )
        content = response.content.decode('utf-8')
        self.assertIn('You have sucessfully logged out', content)

    # flake8:noqa
    def test_logout_view_redirects_logged_user_to_dashboard_if_there_is_no_post_request(self):
        response = self.client.get(reverse('authors:logout'), follow=True)
        self.assertRedirects(response, reverse('authors:dashboard'))

    def test_logout_view_redirects_logged_user_to_dashboard_if_data_does_not_match(self):
        response = self.client.post(
            reverse('authors:logout'),
            data={'username': f'{self.form_data["username"]}1'},
            follow=True
        )
        self.assertRedirects(response, reverse('authors:dashboard'))
