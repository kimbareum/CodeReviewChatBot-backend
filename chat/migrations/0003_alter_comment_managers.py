# Generated by Django 4.2.3 on 2023-07-31 10:08

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='comment',
            managers=[
                ('all_objects', django.db.models.manager.Manager()),
            ],
        ),
    ]
