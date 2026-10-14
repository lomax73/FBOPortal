from django.db import migrations


def seed_adl(apps, schema_editor):
    AppLink = apps.get_model('catalog', 'AppLink')
    AppStatus = apps.get_model('catalog', 'AppStatus')

    in_produzione = AppStatus.objects.filter(name='In produzione').first()

    AppLink.objects.get_or_create(
        slug='adl',
        defaults={
            'categoria': 'cliente',
            'name': 'ADL Consulting',
            'description': "Gestionale dell'agenzia di creator: calendario, collaborazioni, obiettivi, analitiche ed economia",
            'url': 'https://app.adlconsulting.info/',
            'icon': 'adl-consulting.svg',
            'order': 2,
            'dev_status': in_produzione,
        },
    )


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0015_seed_squadfykids'),
    ]

    operations = [
        migrations.RunPython(seed_adl, noop),
    ]
