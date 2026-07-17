from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import ClienteForm
from .models import Cliente


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
