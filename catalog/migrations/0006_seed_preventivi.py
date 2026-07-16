from django.db import migrations


def seed_preventivi(apps, schema_editor):
    AppLink = apps.get_model('catalog', 'AppLink')
    AppLink.objects.get_or_create(
        slug='preventivi',
        defaults={
            'name': 'FBOPreventivi',
            'description': 'Preventivi commerciali per i clienti, con generazione PDF',
            # Provvisorio: stessa IP nuda del VPS, porta dedicata (8445,
            # successiva a Portale:8443 e Collaudi Fibra:8444), finché
            # non esiste un dominio reale (vedi deploy/README.md di
            # FBOPreventivi, quando sarà scritto).
            'url': 'https://94.177.161.127:8445/',
            'icon': 'preventivi.svg',
            'order': 2,
        },
    )


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_applink_api_token_applink_internal_base_url'),
    ]

    operations = [
        migrations.RunPython(seed_preventivi, noop),
    ]
