import time
import uuid
from pathlib import Path

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from . import imports as clienti_imports
from .forms import ClienteForm
from .models import Cliente

IMPORT_TMP_DIR = Path(settings.BASE_DIR) / 'clienti_import_tmp'


class ClienteListView(LoginRequiredMixin, ListView):
    model = Cliente
    template_name = 'clienti/cliente_list.html'
    context_object_name = 'clienti'


class ClienteCreateView(LoginRequiredMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'clienti/cliente_form.html'
    success_url = reverse_lazy('cliente-list')


class ClienteUpdateView(LoginRequiredMixin, UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'clienti/cliente_form.html'
    success_url = reverse_lazy('cliente-list')


class ClienteDeleteView(LoginRequiredMixin, DeleteView):
    model = Cliente
    template_name = 'clienti/cliente_confirm_delete.html'
    success_url = reverse_lazy('cliente-list')


def _cleanup_stale_imports(max_age_seconds=3600):
    """Rimuove i file di staging di import abbandonati (mai confermati né
    annullati esplicitamente) più vecchi di un'ora."""
    if not IMPORT_TMP_DIR.exists():
        return
    now = time.time()
    for f in IMPORT_TMP_DIR.glob('*.xlsx'):
        if now - f.stat().st_mtime > max_age_seconds:
            f.unlink(missing_ok=True)


@login_required
def cliente_import_upload(request):
    if request.method == 'POST':
        file_obj = request.FILES.get('file')
        if not file_obj:
            messages.error(request, 'Seleziona un file .xlsx da importare.')
            return redirect('cliente-import')
        try:
            rows = clienti_imports.parse_rows(file_obj)
        except clienti_imports.ImportError_ as exc:
            messages.error(request, str(exc))
            return redirect('cliente-import')
        if not rows:
            messages.error(request, 'Nessuna riga con "Denominazione" trovata nel file.')
            return redirect('cliente-import')

        IMPORT_TMP_DIR.mkdir(exist_ok=True)
        _cleanup_stale_imports()
        token = uuid.uuid4().hex
        with open(IMPORT_TMP_DIR / f'{token}.xlsx', 'wb') as dest:
            for chunk in file_obj.chunks():
                dest.write(chunk)

        esistenti = {r.lower() for r in Cliente.objects.values_list('ragione_sociale', flat=True)}
        for row in rows:
            row['gia_presente'] = row['ragione_sociale'].lower() in esistenti

        return render(request, 'clienti/cliente_import_preview.html', {'rows': list(enumerate(rows)), 'token': token})

    return render(request, 'clienti/cliente_import_upload.html')


@login_required
def cliente_import_confirm(request):
    if request.method != 'POST':
        return redirect('cliente-import')

    token = request.POST.get('token', '')
    path = IMPORT_TMP_DIR / f'{token}.xlsx'
    if not token or not path.exists():
        messages.error(request, 'Il file caricato non è più disponibile: ricarica l\'import.')
        return redirect('cliente-import')

    with open(path, 'rb') as f:
        rows = clienti_imports.parse_rows(f)

    selected = {int(i) for i in request.POST.getlist('riga')}
    creati = 0
    for i, row in enumerate(rows):
        if i not in selected:
            continue
        row.pop('gia_presente', None)
        Cliente.objects.create(**row)
        creati += 1

    path.unlink(missing_ok=True)
    messages.success(request, f'{creati} client{"e" if creati == 1 else "i"} importat{"o" if creati == 1 else "i"}.')
    return redirect('cliente-list')


def _check_token(request):
    expected = getattr(settings, 'INTERNAL_API_TOKEN', '')
    provided = request.headers.get('Authorization', '')
    return bool(expected) and provided == f'Token {expected}'


def _serialize(cliente):
    return {
        'id': str(cliente.id),
        'ragione_sociale': cliente.ragione_sociale,
        'indirizzo': cliente.indirizzo,
        'cap': cliente.cap,
        'citta': cliente.citta,
        'provincia': cliente.provincia,
        'piva': cliente.piva,
        'email': cliente.email,
        'telefono': cliente.telefono,
        'note': cliente.note,
    }


class InternalClienteListView(View):
    """API interna di sola lettura per le app satellite (es. FBOPreventivi):
    raggiungibile solo da localhost (regola Nginx), token come ulteriore
    difesa — stesso schema di accounts/api/internal/ nelle app satellite,
    ma qui è il Portale a fare da "callee" invece che da chiamante."""

    def get(self, request):
        if not _check_token(request):
            return JsonResponse({'detail': 'Non autorizzato.'}, status=403)
        clienti = Cliente.objects.all().order_by('ragione_sociale')
        return JsonResponse({'clienti': [_serialize(c) for c in clienti]})


class InternalClienteDetailView(View):
    def get(self, request, pk):
        if not _check_token(request):
            return JsonResponse({'detail': 'Non autorizzato.'}, status=403)
        cliente = get_object_or_404(Cliente, pk=pk)
        return JsonResponse(_serialize(cliente))
