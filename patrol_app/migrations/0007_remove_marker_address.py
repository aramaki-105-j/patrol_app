# Generated by Django 4.2.10 on 2024-07-15 00:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patrol_app', '0006_marker_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='marker',
            name='address',
        ),
    ]
