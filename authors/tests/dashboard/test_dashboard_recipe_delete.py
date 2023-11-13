from .test_dashboard_base import DashboardTestBase
from django.urls import reverse


class DashboardRecipeDeleteTest(DashboardTestBase):
    def test_dashboard_recipe_delete_view_can_not_accept_get(self):
        response = self.client.get(reverse('authors:recipe_delete'))
        self.assertEqual(response.status_code, 404)

    def test_dashboard_recipe_delete_view_deletes_a_recipe(self):
        recipe = self.create_unpublished_recipe()
        response = self.client.post(
            reverse('authors:recipe_delete'),
            data={'recipe_id': recipe.pk},
            follow=True
        )
        content = response.content.decode('utf-8')
        self.assertIn('Your recipe has been deleted!', content)
