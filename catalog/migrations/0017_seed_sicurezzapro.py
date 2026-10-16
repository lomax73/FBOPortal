from django.db import migrations


def seed_sicurezzapro(apps, schema_editor):
    AppLink = apps.get_model('catalog', 'AppLink')
    AppStatus = apps.get_model('catalog', 'AppStatus')

    in_produzione = AppStatus.objects.filter(name='In produzione').first()

    AppLink.objects.get_or_create(
        slug='sicurezzapro',
        defaults={
            'categoria': 'cliente',
            'name': 'SicurezzaPro',
            'description': 'Gestione documentale della sicurezza sul lavoro (D.Lgs. 81/08): lavoratori e attestati, scadenze, attrezzature, redazione POS',
            'url': 'https://sicurezza.i-bel.it/',
            'icon': 'sicurezzapro.svg',
            'order': 3,
            'dev_status': in_produzione,
        },
    )


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0016_seed_adl'),
    ]

    operations = [
        migrations.RunPython(seed_sicurezzapro, noop),
    ]
