from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from .models import AppLink


class HomeView(LoginRequiredMixin, ListView):
    model = AppLink
    template_name = 'catalog/home.html'
    context_object_name = 'apps'

    def get_queryset(self):
        return AppLink.objects.filter(is_active=True)
