# Generated by Django 3.1.1 on 2020-11-23 00:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0012_auto_20201122_2249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventoptions',
            name='event',
            field=models.CharField(default='', max_length=100),
        ),
    ]
