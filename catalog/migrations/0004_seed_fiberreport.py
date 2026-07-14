from django.db import migrations


def seed_fiberreport(apps, schema_editor):
    AppLink = apps.get_model('catalog', 'AppLink')
    AppLink.objects.get_or_create(
        slug='fiberreport',
        defaults={
            'name': 'Collaudi Fibra',
            'description': 'Collaudo attenuazione fibra ottica e report PDF',
            # Provvisorio: stessa IP nuda del VPS, porta dedicata (8444),
            # finché non esiste un dominio reale (vedi deploy/README.md
            # di FBOFiberReport).
            'url': 'https://94.177.161.127:8444/',
            'icon': 'fiberreport.svg',
            'order': 1,
        },
    )


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_mkremote_icon'),
    ]

    operations = [
        migrations.RunPython(seed_fiberreport, noop),
    ]
