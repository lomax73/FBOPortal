import uuid

from django.db import models


class Cliente(models.Model):
    """Anagrafica clienti condivisa: ogni app della famiglia FBO che
    deve riferirsi a un cliente salva solo questo id (UUID), e lo
    risolve a runtime chiamando l'API interna esposta qui sotto —
    nessuna FK cross-database (vedi memoria project-multi-app-
    portal-architecture).

    Campi allineati all'export gestionale usato dall'utente (colonne
    dello stesso nome, vedi clienti/imports.py) per poter importare
    l'anagrafica esistente senza perdere informazioni."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ragione_sociale = models.CharField('Denominazione', max_length=255)
    indirizzo = models.CharField(max_length=255, blank=True)
    citta = models.CharField('Comune', max_length=100, blank=True)
    cap = models.CharField(max_length=10, blank=True)
    provincia = models.CharField(max_length=5, blank=True)
    note_indirizzo = models.CharField(max_length=255, blank=True)
    paese = models.CharField(max_length=100, blank=True, default='Italia')
    email = models.EmailField('Indirizzo e-mail', blank=True)
    referente = models.CharField(max_length=200, blank=True)
    telefono = models.CharField(max_length=50, blank=True)
    piva = models.CharField('P.IVA/TAX ID', max_length=20, blank=True)
    codice_fiscale = models.CharField(max_length=20, blank=True)
    note = models.TextField(blank=True)
    pec = models.EmailField('Indirizzo PEC', blank=True)
    iban = models.CharField(max_length=34, blank=True)
    codice_sdi = models.CharField(max_length=10, blank=True)
    aliquota_iva_predefinita = models.CharField(max_length=50, blank=True)
    termini_pagamento = models.CharField(max_length=50, blank=True)
    indirizzo_spedizione = models.CharField(max_length=255, blank=True)
    sconto_predefinito = models.CharField(max_length=20, blank=True)
    creato_il = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['ragione_sociale']

    def __str__(self):
        return self.ragione_sociale
