from django.db import models


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

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name
