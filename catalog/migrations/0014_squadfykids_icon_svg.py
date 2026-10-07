from django.db import migrations


def set_svg_icon(apps, schema_editor):
    AppLink = apps.get_model('catalog', 'AppLink')
    AppLink.objects.filter(slug='squadfykids').update(icon='squadfy-kids.svg')


def set_png_icon(apps, schema_editor):
    AppLink = apps.get_model('catalog', 'AppLink')
    AppLink.objects.filter(slug='squadfykids').update(icon='squadfy-kids.png')


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0013_seed_preventify'),
    ]

    operations = [
        migrations.RunPython(set_svg_icon, set_png_icon),
    ]
