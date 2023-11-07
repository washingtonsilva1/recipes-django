import pytest
from authors import views
from .test_dashboard_base import DashboardTestBase
from django.urls import resolve, reverse


@pytest.mark.fast
class DashboardViewUnitTest(DashboardTestBase):
    def test_dashboard_loads_correct_view(self):
        view = resolve(reverse('authors:dashboard'))
        self.assertIs(view.func, views.dashboard_view)

    def test_dashboard_render_correct_template(self):
        response = self.client.get(reverse('authors:dashboard'))
        self.assertTemplateUsed(response, 'authors/pages/dashboardView.html')
