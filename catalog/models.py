from django.db import models
from django.utils.text import slugify

from .fields import EncryptedCharField


class AppStatus(models.Model):
    name = models.CharField(
        max_length=50, unique=True,
        help_text='Es. "In produzione" — è il titolo mostrato sotto il pallino sulla card.',
    )
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    color = models.CharField(
        max_length=7, default='#2f9e5c',
        help_text='Colore esadecimale, es. #2f9e5c. Usato sia per il pallino sia per il titolo.',
    )
    description = models.CharField(
        max_length=255, blank=True,
        help_text="Visibile solo in questa pagina di configurazione, non sulle card.",
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'stato app'
        verbose_name_plural = 'stati app'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class AppLink(models.Model):
    class Categoria(models.TextChoices):
        INTERNA = 'interna', 'Applicazioni interne'
        CLIENTE = 'cliente', 'Applicazioni clienti'

    categoria = models.CharField(
        max_length=20,
        choices=Categoria.choices,
        default=Categoria.INTERNA,
        help_text="Sezione del launcher in cui compare la card.",
    )
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
    dev_status = models.ForeignKey(
        AppStatus, on_delete=models.PROTECT, related_name='apps',
        null=True, blank=True,
        help_text="Mostrato come pallino colorato con etichetta sulla card.",
    )

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
        ordering = ['-categoria', 'order', 'name']

    def __str__(self):
        return self.name

    @property
    def user_management_enabled(self):
        return bool(self.internal_base_url and self.api_token)
