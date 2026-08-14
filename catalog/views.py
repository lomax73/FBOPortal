from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView

from .forms import AppStatusForm
from .models import AppLink, AppStatus


class HomeView(LoginRequiredMixin, ListView):
    model = AppLink
    template_name = 'catalog/home.html'
    context_object_name = 'apps'

    def get_queryset(self):
        return AppLink.objects.filter(is_active=True)


@login_required
def app_status_list(request):
    apps = AppLink.objects.all()
    statuses = AppStatus.objects.all()

    if request.method == 'POST':
        for app in apps:
            value = request.POST.get(f'status_{app.pk}', '')
            app.dev_status_id = int(value) if value else None
            app.save(update_fields=['dev_status'])
        messages.success(request, 'Stati aggiornati.')
        return redirect('app-status-list')

    return render(request, 'catalog/app_status_list.html', {'apps': apps, 'statuses': statuses})


@login_required
def app_description_list(request):
    apps = AppLink.objects.all()

    if request.method == 'POST':
        for app in apps:
            app.description = request.POST.get(f'description_{app.pk}', '').strip()
            app.save(update_fields=['description'])
        messages.success(request, 'Descrizioni aggiornate.')
        return redirect('app-description-list')

    return render(request, 'catalog/app_description_list.html', {'apps': apps})


@login_required
def status_config_list(request):
    statuses = AppStatus.objects.all()
    return render(request, 'catalog/status_config_list.html', {'statuses': statuses})


@login_required
def status_config_create(request):
    if request.method == 'POST':
        form = AppStatusForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Stato creato.')
            return redirect('status-config-list')
    else:
        form = AppStatusForm()
    return render(request, 'catalog/status_config_form.html', {'form': form, 'is_new': True})


@login_required
def status_config_update(request, pk):
    status = get_object_or_404(AppStatus, pk=pk)
    if request.method == 'POST':
        form = AppStatusForm(request.POST, instance=status)
        if form.is_valid():
            form.save()
            messages.success(request, 'Stato aggiornato.')
            return redirect('status-config-list')
    else:
        form = AppStatusForm(instance=status)
    return render(request, 'catalog/status_config_form.html', {'form': form, 'status': status, 'is_new': False})


@login_required
def status_config_delete(request, pk):
    status = get_object_or_404(AppStatus, pk=pk)
    apps_using_it = status.apps.all()
    if request.method == 'POST':
        if apps_using_it.exists():
            messages.error(
                request,
                f'Impossibile eliminare "{status.name}": è ancora assegnato a {apps_using_it.count()} app. '
                'Cambia prima il loro stato dalla pagina "Stato app".',
            )
            return redirect('status-config-list')
        status.delete()
        messages.success(request, 'Stato eliminato.')
        return redirect('status-config-list')
    return render(request, 'catalog/status_config_confirm_delete.html', {
        'status': status, 'apps_using_it': apps_using_it,
    })
