# Generated by Django 3.2.25 on 2024-04-13 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_transaction_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='billing_month',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]