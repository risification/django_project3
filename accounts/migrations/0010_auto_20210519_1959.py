# Generated by Django 3.2 on 2021-05-19 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20210505_1911'),
    ]

    operations = [
        migrations.AlterField(
            model_name='education',
            name='start_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='warcraft',
            name='start_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='warcraft',
            name='start_pose',
            field=models.DateField(),
        ),
    ]
