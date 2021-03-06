# Generated by Django 3.2 on 2021-05-05 13:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20210505_1901'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='dossier',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='accounts.dossier'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='education',
            name='dossier',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='accounts.dossier'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='warcraft',
            name='dossier',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='accounts.dossier'),
            preserve_default=False,
        ),
    ]
