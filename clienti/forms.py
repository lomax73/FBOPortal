from django import forms

from .models import Cliente


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['ragione_sociale', 'indirizzo', 'cap', 'citta', 'provincia', 'piva', 'email', 'telefono', 'note']
