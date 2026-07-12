from django.db import migrations


def set_icon(apps, schema_editor):
    AppLink = apps.get_model('catalog', 'AppLink')
    AppLink.objects.filter(slug='mkremote').update(icon='mkremote.svg')


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_seed_mkremote'),
    ]

    operations = [
        migrations.RunPython(set_icon, noop),
    ]
