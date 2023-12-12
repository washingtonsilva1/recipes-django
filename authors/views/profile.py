from authors.models import Profile

from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import get_language

from django.contrib import messages


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
            'translation': get_language(),
        })
        return self.render_to_response(ctx)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    context_object_name = 'profile'
    fields = ['bio']
    template_name = 'authors/pages/profile_update.html'
    login_url = reverse_lazy('authors:login')

    def post(self, request, *args, **kwargs):
        messages.success(self.request, 'Your profile has been updated!')
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'search_bar': False,
            'title': f'{ctx["profile"].user.username} | ',
            'translation': get_language(),
        })
        return ctx

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.select_related('user')
        qs = qs.filter(
            user=self.request.user
        )
        return qs

    def get_success_url(self):
        return reverse_lazy('authors:profile', args=[self.get_object().pk])
