from django import forms
from django.forms import inlineformset_factory

from .models import ElementoRack, Posizione, Progetto, Rack


class ProgettoForm(forms.ModelForm):
    class Meta:
        model = Progetto
        fields = ['nome', 'cliente', 'sito', 'data_intervento', 'note']
        widgets = {
            'data_intervento': forms.DateInput(attrs={'type': 'date'}),
            'note': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cliente'].queryset = self.fields['cliente'].queryset.order_by('ragione_sociale')


class RackForm(forms.ModelForm):
    class Meta:
        model = Rack
        fields = ['nome', 'note', 'ordine']


class ElementoRackForm(forms.ModelForm):
    class Meta:
        model = ElementoRack
        fields = ['tipo', 'etichetta', 'n_posizioni', 'ordine']


PosizioneFormSet = inlineformset_factory(
    ElementoRack,
    Posizione,
    fields=['cavo_n', 'tipo_cavo', 'descrizione', 'posizione_in_campo', 'esito_test'],
    extra=0,
    can_delete=False,
)
