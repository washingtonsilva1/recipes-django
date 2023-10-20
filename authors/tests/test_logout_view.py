from authors import views
from .test_form_base import FormTestBase
from django.urls import resolve, reverse


class LogoutViewTest(FormTestBase):
    def test_logout_is_loading_correct_view(self):
        view = resolve(reverse('authors:logout'))
        self.assertIs(view.func, views.logout_view)

    def test_logout_view_redirect_to_login_when_not_logged(self):
        response = self.client.get(
            reverse('authors:logout'),
            follow=True)
        self.assertEqual(reverse('authors:login'),
                         response.request.get('PATH_INFO'))

    def test_logout_view_is_logging_out_user(self):
        self.create_user()
        self.client.post(
            reverse('authors:login_create'),
            data={'username': self.form_data['username'],
                  'password': self.form_data['password']})
        response = self.client.post(reverse('authors:logout'),
                                    data={
            'username': self.form_data['username'],
        }, follow=True)
        content = response.content.decode('utf-8')
        self.assertIn('You have sucessfully logged out', content)
