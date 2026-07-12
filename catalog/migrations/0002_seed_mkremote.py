from django.db import migrations


def seed_mkremote(apps, schema_editor):
    AppLink = apps.get_model('catalog', 'AppLink')
    AppLink.objects.get_or_create(
        slug='mkremote',
        defaults={
            'name': 'MKRemote',
            'description': 'Gestione remota router e apparati clienti',
            'url': 'https://mkremote.tuodominio.it/',
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
