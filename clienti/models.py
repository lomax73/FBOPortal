import uuid

from django.db import models


class Cliente(models.Model):
    """Anagrafica clienti condivisa: ogni app della famiglia FBO che
    deve riferirsi a un cliente salva solo questo id (UUID), e lo
    risolve a runtime chiamando l'API interna esposta qui sotto —
    nessuna FK cross-database (vedi memoria project-multi-app-
    portal-architecture)."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ragione_sociale = models.CharField(max_length=200)
    indirizzo = models.CharField(max_length=255, blank=True)
    cap = models.CharField(max_length=10, blank=True)
    citta = models.CharField(max_length=100, blank=True)
    provincia = models.CharField(max_length=2, blank=True)
    piva = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    telefono = models.CharField(max_length=30, blank=True)
    note = models.TextField(blank=True)
    creato_il = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['ragione_sociale']

    def __str__(self):
        return self.ragione_sociale
