from django.db import migrations


def seed_fboleads(apps, schema_editor):
    AppLink = apps.get_model('catalog', 'AppLink')
    AppLink.objects.get_or_create(
        slug='fboleads',
        defaults={
            'name': 'FBOLeads',
            'description': 'Contatti raccolti dai siti web, con assegnazione e archivio',
            # Dominio dedicato (lead.fbosolution.it), sostituisce l'IP nudo
            # su porta dedicata (vedi deploy/README.md di FBOLeads).
            'url': 'https://lead.fbosolution.it/',
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
