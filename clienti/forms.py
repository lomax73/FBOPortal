from django import forms

from .models import Cliente


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = [
            'ragione_sociale', 'indirizzo', 'citta', 'cap', 'provincia', 'note_indirizzo', 'paese',
            'email', 'referente', 'telefono', 'piva', 'codice_fiscale', 'note', 'pec', 'iban',
            'codice_sdi', 'aliquota_iva_predefinita', 'termini_pagamento', 'indirizzo_spedizione',
            'sconto_predefinito',
        ]
        widgets = {
            'note': forms.Textarea(attrs={'rows': 3}),
        }
