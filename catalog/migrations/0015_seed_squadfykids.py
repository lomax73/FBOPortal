from django.db import migrations


def seed_squadfykids(apps, schema_editor):
    AppLink = apps.get_model('catalog', 'AppLink')
    AppStatus = apps.get_model('catalog', 'AppStatus')

    in_produzione = AppStatus.objects.filter(name='In produzione').first()

    AppLink.objects.get_or_create(
        slug='squadfykids',
        defaults={
            'categoria': 'cliente',
            'name': 'Squadfy Kids',
            'description': "Gestione corsi di calcio per cuccioli e condivisione esercizi tra formatori (LET'S KICK)",
            'url': 'https://squadfy.letskick.it/',
            'icon': 'squadfy-kids.svg',
            'order': 1,
            'dev_status': in_produzione,
        },
    )


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0014_squadfykids_icon_svg'),
    ]

    operations = [
        migrations.RunPython(seed_squadfykids, noop),
    ]
