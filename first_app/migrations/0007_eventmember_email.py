# Generated by Django 3.1.1 on 2020-11-19 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0006_remove_eventmember_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventmember',
            name='email',
            field=models.EmailField(default='', max_length=100),
        ),
    ]
