# Generated by Django 5.1.2 on 2024-11-02 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='way_of_payment',
            field=models.CharField(choices=[('cash', 'Cash'), ('credit_card', 'Credit Card'), ('debit_card', 'Debit Card'), ('bank_transfer', 'Bank Transfer'), ('other', 'Other')], default='cash', max_length=20),
        ),
    ]
