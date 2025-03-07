# Generated by Django 4.2.10 on 2024-07-13 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patrol_app', '0004_customuser_is_paid'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='stripe_card_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='stripe_customer_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='stripe_subscription_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
