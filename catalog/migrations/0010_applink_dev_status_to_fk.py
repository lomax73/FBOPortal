import django.db.models.deletion
from django.db import migrations, models


def migrate_values(apps, schema_editor):
    AppLink = apps.get_model('catalog', 'AppLink')
    AppStatus = apps.get_model('catalog', 'AppStatus')
    by_slug = {status.slug: status for status in AppStatus.objects.all()}
    for link in AppLink.objects.all():
        status = by_slug.get(link.dev_status_old)
        if status:
            link.dev_status_new_id = status.id
            link.save(update_fields=['dev_status_new'])


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0009_appstatus'),
    ]

    operations = [
        migrations.RenameField(model_name='applink', old_name='dev_status', new_name='dev_status_old'),
        migrations.AddField(
            model_name='applink',
            name='dev_status_new',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='apps', to='catalog.appstatus',
                help_text='Mostrato come pallino colorato con etichetta sulla card.',
            ),
        ),
        migrations.RunPython(migrate_values, noop),
        migrations.RemoveField(model_name='applink', name='dev_status_old'),
        migrations.RenameField(model_name='applink', old_name='dev_status_new', new_name='dev_status'),
    ]
