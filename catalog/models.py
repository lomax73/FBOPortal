from django.db import models

from .fields import EncryptedCharField


class AppLink(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.CharField(max_length=255, blank=True)
    url = models.URLField()
    icon = models.CharField(
        max_length=100,
        blank=True,
        help_text='Nome file dentro static/img/, es. mkremote.svg. Se vuoto, viene mostrata l\'iniziale del nome.',
    )
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    internal_base_url = models.URLField(
        'URL base API interna', blank=True,
        help_text="Es. https://127.0.0.1:8444 — l'app chiamata via loopback, non l'URL pubblico sopra. "
                   "Lasciare vuoto se questa app non espone la gestione utenti.",
    )
    api_token = EncryptedCharField(
        blank=True, null=True,
        help_text='Stesso valore di INTERNAL_API_TOKEN nel .env di quella app. Cifrato a riposo.',
    )

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    @property
    def user_management_enabled(self):
        return bool(self.internal_base_url and self.api_token)
