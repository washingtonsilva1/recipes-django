from authors.models import Profile

from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView


class ProfileView(TemplateView):
    template_name = 'authors/pages/profile.html'

    def get(self, *args, **kwargs):
        ctx = super().get_context_data(**kwargs)
        profile_id = ctx.get('id')
        profile = get_object_or_404(
            Profile.objects.filter(
                pk=profile_id,
            ).select_related('user'),
            pk=profile_id
        )
        ctx.update({
            'title': f'{profile.user.username} | ',
            'profile': profile,
            'search_bar': False,
        })
        return self.render_to_response(ctx)
