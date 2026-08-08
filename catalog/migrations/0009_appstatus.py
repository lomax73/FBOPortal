from django.db import migrations, models


def seed_statuses(apps, schema_editor):
    AppStatus = apps.get_model('catalog', 'AppStatus')
    AppStatus.objects.get_or_create(
        slug='produzione',
        defaults=dict(name='In produzione', color='#2f9e5c', description='App stabile, in uso quotidiano.'),
    )
    AppStatus.objects.get_or_create(
        slug='beta',
        defaults=dict(name='Beta', color='#2563eb', description="Funzionante ma ancora in evoluzione attiva."),
    )
    AppStatus.objects.get_or_create(
        slug='sviluppo',
        defaults=dict(name='In sviluppo', color='#e0a213', description="Non ancora pronta per l'uso quotidiano."),
    )
    AppStatus.objects.get_or_create(
        slug='manutenzione',
        defaults=dict(name='In manutenzione', color='#d92d20', description='Temporaneamente instabile o in intervento.'),
    )


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0008_alter_applink_options_applink_dev_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Es. "In produzione" — è il titolo mostrato sotto il pallino sulla card.', max_length=50, unique=True)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('color', models.CharField(default='#2f9e5c', help_text='Colore esadecimale, es. #2f9e5c. Usato sia per il pallino sia per il titolo.', max_length=7)),
                ('description', models.CharField(blank=True, help_text='Visibile solo in questa pagina di configurazione, non sulle card.', max_length=255)),
            ],
            options={
                'verbose_name': 'stato app',
                'verbose_name_plural': 'stati app',
                'ordering': ['name'],
            },
        ),
        migrations.RunPython(seed_statuses, noop),
    ]
