from django.db import migrations


def seed_preventify(apps, schema_editor):
    AppLink = apps.get_model('catalog', 'AppLink')
    AppStatus = apps.get_model('catalog', 'AppStatus')

    in_produzione = AppStatus.objects.filter(name='In produzione').first()

    AppLink.objects.get_or_create(
        slug='preventify',
        defaults={
            'categoria': 'interna',
            'name': 'Preventify',
            'description': "Preventivi Nanopower e moduli d'ordine",
            'url': 'https://preventify.fbosolution.it/',
            'icon': 'preventify.svg',
            'order': 8,
            'dev_status': in_produzione,
        },
    )


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0012_seed_fboleads'),
    ]

    operations = [
        migrations.RunPython(seed_preventify, noop),
    ]
