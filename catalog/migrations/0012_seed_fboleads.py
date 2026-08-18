from django.db import migrations


def seed_fboleads(apps, schema_editor):
    AppLink = apps.get_model('catalog', 'AppLink')
    AppLink.objects.get_or_create(
        slug='fboleads',
        defaults={
            'name': 'FBOLeads',
            'description': 'Contatti raccolti dai siti web, con assegnazione e archivio',
            # Provvisorio: stessa IP nuda del VPS, porta dedicata (8451,
            # libera: 8444 Collaudi, 8445 Preventivi, 8446 RackReport,
            # 8447 NetVault, 8448 Squadfy), finché non esiste un dominio
            # reale (vedi deploy/README.md di FBOLeads).
            'url': 'https://94.177.161.127:8451/',
            'icon': 'fboleads.svg',
            'order': 7,
        },
    )


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0011_applink_internal_ca_cert'),
    ]

    operations = [
        migrations.RunPython(seed_fboleads, noop),
    ]
