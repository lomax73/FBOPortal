from pathlib import Path

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.text import slugify
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from weasyprint import HTML

from .forms import ElementoRackForm, PosizioneFormSet, ProgettoForm, RackForm
from .models import ElementoRack, Posizione, Progetto, Rack, RackAllegato


def sync_posizioni(elemento):
    """Crea/rimuove le Posizione di un elemento per allinearle a n_posizioni."""
    esistenti = {p.numero: p for p in elemento.posizioni.all()}
    for numero in range(1, elemento.n_posizioni + 1):
        if numero not in esistenti:
            Posizione.objects.create(elemento=elemento, numero=numero)
    for numero, posizione in esistenti.items():
        if numero > elemento.n_posizioni:
            posizione.delete()


def elementi_con_offset(rack):
    """Elementi del rack con il numero di porta assoluto di partenza
    (numerazione continua nel rack, es. pannello B parte da 25 se A ne ha 24)."""
    offset = 0
    risultato = []
    for elemento in rack.elementi.all():
        risultato.append((elemento, offset))
        offset += elemento.n_posizioni
    return risultato


# --- Progetto -----------------------------------------------------------

class ProgettoListView(LoginRequiredMixin, ListView):
    model = Progetto
    template_name = 'rackreport/progetto_list.html'
    context_object_name = 'progetti'


class ProgettoDetailView(LoginRequiredMixin, DetailView):
    model = Progetto
    template_name = 'rackreport/progetto_detail.html'
    context_object_name = 'progetto'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rack_list = []
        for rack in self.object.rack_set.prefetch_related('elementi__posizioni', 'allegati'):
            rack_list.append({
                'rack': rack,
                'elementi': [
                    {'elemento': elemento, 'offset': offset, 'riepilogo': elemento.esito_riepilogo()}
                    for elemento, offset in elementi_con_offset(rack)
                ],
            })
        context['rack_list'] = rack_list
        return context


class ProgettoCreateView(LoginRequiredMixin, CreateView):
    model = Progetto
    form_class = ProgettoForm
    template_name = 'rackreport/progetto_form.html'

    def get_success_url(self):
        return reverse('progetto-detail', args=[self.object.pk])


class ProgettoUpdateView(LoginRequiredMixin, UpdateView):
    model = Progetto
    form_class = ProgettoForm
    template_name = 'rackreport/progetto_form.html'

    def get_success_url(self):
        return reverse('progetto-detail', args=[self.object.pk])


class ProgettoDeleteView(LoginRequiredMixin, DeleteView):
    model = Progetto
    template_name = 'rackreport/progetto_confirm_delete.html'
    success_url = reverse_lazy('progetto-list')


# --- Rack -----------------------------------------------------------------

class RackCreateView(LoginRequiredMixin, CreateView):
    model = Rack
    form_class = RackForm
    template_name = 'rackreport/rack_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.progetto = get_object_or_404(Progetto, pk=kwargs['progetto_pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['progetto'] = self.progetto
        return context

    def form_valid(self, form):
        form.instance.progetto = self.progetto
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('progetto-detail', args=[self.progetto.pk])


class RackUpdateView(LoginRequiredMixin, UpdateView):
    model = Rack
    form_class = RackForm
    template_name = 'rackreport/rack_form.html'

    def get_success_url(self):
        return reverse('progetto-detail', args=[self.object.progetto_id])


class RackDeleteView(LoginRequiredMixin, DeleteView):
    model = Rack
    template_name = 'rackreport/rack_confirm_delete.html'

    def get_success_url(self):
        return reverse('progetto-detail', args=[self.object.progetto_id])


# --- ElementoRack -----------------------------------------------------------

class ElementoRackCreateView(LoginRequiredMixin, CreateView):
    model = ElementoRack
    form_class = ElementoRackForm
    template_name = 'rackreport/elemento_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.rack = get_object_or_404(Rack, pk=kwargs['rack_pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rack'] = self.rack
        return context

    def form_valid(self, form):
        form.instance.rack = self.rack
        response = super().form_valid(form)
        sync_posizioni(self.object)
        return response

    def get_success_url(self):
        return reverse('elemento-posizioni', args=[self.object.pk])


class ElementoRackUpdateView(LoginRequiredMixin, UpdateView):
    model = ElementoRack
    form_class = ElementoRackForm
    template_name = 'rackreport/elemento_form.html'

    def post(self, request, *args, **kwargs):
        # self.object viene mutato dal binding del ModelForm (form.instance è
        # self.object) già durante form.is_valid(), prima di form_valid(): va
        # letto il valore precedente dal DB qui, non da self.object più sotto.
        self.object = self.get_object()
        self._n_posizioni_precedente = self.object.n_posizioni
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        nuovo_n = form.cleaned_data['n_posizioni']
        if nuovo_n < self._n_posizioni_precedente:
            da_rimuovere = self.object.posizioni.filter(numero__gt=nuovo_n)
            non_vuote = [p for p in da_rimuovere if p.cavo_n or p.descrizione]
            if non_vuote and self.request.POST.get('conferma_riduzione') != '1':
                messages.error(
                    self.request,
                    f'Riducendo a {nuovo_n} posizioni perderai i dati di {len(non_vuote)} '
                    'posizioni già compilate. Conferma per procedere.',
                )
                return self.render_to_response(
                    self.get_context_data(form=form, richiedi_conferma_riduzione=True)
                )
        response = super().form_valid(form)
        sync_posizioni(self.object)
        return response

    def get_success_url(self):
        return reverse('progetto-detail', args=[self.object.rack.progetto_id])


class ElementoRackDeleteView(LoginRequiredMixin, DeleteView):
    model = ElementoRack
    template_name = 'rackreport/elemento_confirm_delete.html'

    def get_success_url(self):
        return reverse('progetto-detail', args=[self.object.rack.progetto_id])


@login_required
def elemento_posizioni(request, pk):
    elemento = get_object_or_404(ElementoRack, pk=pk)
    if request.method == 'POST':
        formset = PosizioneFormSet(request.POST, instance=elemento)
        if formset.is_valid():
            formset.save()
            messages.success(request, 'Posizioni aggiornate.')
            return redirect('progetto-detail', pk=elemento.rack.progetto_id)
    else:
        formset = PosizioneFormSet(instance=elemento)

    offset = dict(elementi_con_offset(elemento.rack)).get(elemento, 0)
    return render(request, 'rackreport/posizioni_form.html', {
        'elemento': elemento,
        'formset': formset,
        'offset': offset,
    })


# --- Allegati -----------------------------------------------------------

@login_required
def rack_allegato_upload(request, pk):
    rack = get_object_or_404(Rack, pk=pk)
    if request.method == 'POST':
        files = request.FILES.getlist('file')
        if not files:
            messages.error(request, 'Seleziona almeno un file da caricare.')
        else:
            for f in files:
                RackAllegato.objects.create(rack=rack, file=f, nome_originale=f.name)
            messages.success(request, f'{len(files)} file caricat{"o" if len(files) == 1 else "i"}.')
    return redirect('progetto-detail', pk=rack.progetto_id)


class RackAllegatoDeleteView(LoginRequiredMixin, DeleteView):
    model = RackAllegato
    template_name = 'rackreport/allegato_confirm_delete.html'

    def get_success_url(self):
        return reverse('progetto-detail', args=[self.object.rack.progetto_id])


# --- Report PDF -----------------------------------------------------------

@login_required
def progetto_report_pdf(request, pk):
    progetto = get_object_or_404(Progetto, pk=pk)
    rack_list = []
    for rack in progetto.rack_set.prefetch_related('elementi__posizioni'):
        rack_list.append({
            'rack': rack,
            'elementi': [
                {'elemento': elemento, 'offset': offset}
                for elemento, offset in elementi_con_offset(rack)
            ],
        })
    html_string = render_to_string('rackreport/report_pdf.html', {
        'progetto': progetto,
        'rack_list': rack_list,
        'now': timezone.localtime(),
        'request': request,
    })
    pdf_bytes = HTML(string=html_string, base_url=request.build_absolute_uri('/')).write_pdf()

    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    filename = f'report-rack-{slugify(progetto.nome)}.pdf'
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response
