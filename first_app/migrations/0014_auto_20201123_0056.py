# Generated by Django 3.1.1 on 2020-11-23 00:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0013_auto_20201123_0035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventoptions_attendee',
            name='attendee_email',
            field=models.EmailField(default='', max_length=100),
        ),
    ]
