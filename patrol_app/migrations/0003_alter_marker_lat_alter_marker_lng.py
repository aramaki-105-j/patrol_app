# Generated by Django 4.2.10 on 2024-07-09 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patrol_app', '0002_alter_marker_id_alter_review_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marker',
            name='lat',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='marker',
            name='lng',
            field=models.FloatField(null=True),
        ),
    ]
