from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from catalog.models import AppLink

from . import services
from .forms import UserCreateForm, UserUpdateForm


@login_required
def user_list(request):
    rows = []
    errors = []
    apps = [a for a in AppLink.objects.all() if a.user_management_enabled]
    for app_link in apps:
        try:
            users = services.list_users(app_link)
        except services.RemoteAppError as exc:
            errors.append({'app': app_link, 'error': str(exc)})
            continue
        for user in users:
            rows.append({'app': app_link, 'user': user})

    rows.sort(key=lambda r: (r['app'].name, r['user']['username']))
    return render(request, 'useradmin/user_list.html', {
        'rows': rows,
        'errors': errors,
        'has_managed_apps': bool(apps),
    })


@login_required
def user_create(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            app_link = get_object_or_404(AppLink, pk=form.cleaned_data['app'])
            try:
                services.create_user(
                    app_link,
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password'],
                    email=form.cleaned_data['email'],
                )
            except services.RemoteAppError as exc:
                messages.error(request, f'Errore creando l\'utente su {app_link.name}: {exc}')
            else:
                messages.success(request, f'Utente creato su {app_link.name}.')
                return redirect('user-list')
    else:
        form = UserCreateForm()
    return render(request, 'useradmin/user_form.html', {'form': form})


@login_required
def user_update(request, app_pk, user_id):
    app_link = get_object_or_404(AppLink, pk=app_pk)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST)
        if form.is_valid():
            fields = {
                'email': form.cleaned_data['email'],
                'is_active': form.cleaned_data['is_active'],
            }
            if form.cleaned_data['new_password']:
                fields['password'] = form.cleaned_data['new_password']
            try:
                services.update_user(app_link, user_id, **fields)
            except services.RemoteAppError as exc:
                messages.error(request, f'Errore modificando l\'utente su {app_link.name}: {exc}')
            else:
                messages.success(request, f'Utente aggiornato su {app_link.name}.')
                return redirect('user-list')
    else:
        initial = {
            'email': request.GET.get('email', ''),
            'is_active': request.GET.get('is_active') == '1',
        }
        form = UserUpdateForm(initial=initial)
    return render(request, 'useradmin/user_form.html', {
        'form': form, 'app_link': app_link, 'username': request.GET.get('username', ''),
    })


@login_required
def user_delete(request, app_pk, user_id):
    app_link = get_object_or_404(AppLink, pk=app_pk)
    username = request.GET.get('username', '')
    if request.method == 'POST':
        try:
            services.delete_user(app_link, user_id)
        except services.RemoteAppError as exc:
            messages.error(request, f'Errore eliminando l\'utente su {app_link.name}: {exc}')
        else:
            messages.success(request, f'Utente eliminato da {app_link.name}.')
        return redirect('user-list')
    return render(request, 'useradmin/user_confirm_delete.html', {'app_link': app_link, 'username': username})
