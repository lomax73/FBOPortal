from django.db import migrations


def seed_mkremote(apps, schema_editor):
    AppLink = apps.get_model('catalog', 'AppLink')
    AppLink.objects.get_or_create(
        slug='mkremote',
        defaults={
            'name': 'MKRemote',
            'description': 'Gestione remota router e apparati clienti',
            # Provvisorio: MKRemote è ancora servito sull'IP nudo del VPS
            # (nessun dominio configurato). Aggiornare quando ci sarà un
            # dominio reale (vedi deploy/README.md).
            'url': 'https://94.177.161.127/',
            'icon': 'mkremote.svg',
            'order': 0,
        },
    )


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_mkremote, noop),
    ]
